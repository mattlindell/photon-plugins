#!/usr/bin/env python3
"""Derive the semver bump each plugin needs from what actually changed.

Usage:
    python scripts/bump-versions.py                      # check against origin/main
    python scripts/bump-versions.py --base <ref>         # check against another ref
    python scripts/bump-versions.py --worktree           # include uncommitted work
    python scripts/bump-versions.py --apply              # write the bumps
    python scripts/bump-versions.py --format github      # annotations for CI

Impact is read from *structure*, not from diff size. A one-line change can be
breaking (adding `disable-model-invocation` removes the model's reach) while a
500-line deletion inside a reference file is a patch, so line counts are not
used at all.

  major  skill removed or renamed - skill `name:` changed - plugin removed or
         renamed - `disable-model-invocation` added - agent or command removed
  minor  skill, agent, command, or plugin added - `disable-model-invocation`
         removed
  patch  everything else

Conventional-commit types in the range can raise that floor but never lower it:
`feat` implies at least minor, and `!` or a `BREAKING CHANGE:` footer implies
major. Structure wins ties because it is derived from the artifact rather than
from what someone remembered to type.

The committed version only has to be *at or above* the floor. Bumping higher
than the tool asks is always fine, so pre-bumping locally never trips the check.

Exit codes: 0 satisfied - 1 below floor - 2 below floor on a major - 3 bad ref.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Literal, NamedTuple, cast

from _manifest import (
    MARKETPLACE_PATH,
    PLUGINS_DIR,
    UNREGISTERED,
    Marketplace,
    PluginManifest,
    entries,
    load_marketplace,
    plugin_manifest_path,
    write_json,
)

Level = Literal["patch", "minor", "major"]
LEVELS: tuple[Level, ...] = ("patch", "minor", "major")

WORKTREE = "WORKTREE"  # sentinel: read from disk, not from a git ref

FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
CONVENTIONAL = re.compile(r"\b(feat|fix|refactor|chore|docs|perf|test)(\(([^)]*)\))?(!)?:")


class Row(NamedTuple):
    plugin: str
    previous: str
    current: str
    level: Level | None  # None marks a newly added plugin
    why: str
    satisfied: bool


def sh(*args: str) -> str | None:
    """Run a git command, returning stdout or None when it fails.

    Output is decoded as UTF-8 explicitly: the default on Windows is the ANSI
    codepage, which raises on the em dashes and arrows in these skills and makes
    every read look like an absent file.
    """
    result = subprocess.run(
        args, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
    )
    return result.stdout if result.returncode == 0 else None


def higher(a: Level, b: Level) -> Level:
    return a if LEVELS.index(a) >= LEVELS.index(b) else b


def parse_version(version: str) -> tuple[int, int, int]:
    parts = (version or "0.0.0").split(".")
    parts += ["0"] * (3 - len(parts))
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return (0, 0, 0)


def bump(version: str, level: Level) -> str:
    major, minor, patch = parse_version(version)
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def read_at(ref: str, path: str) -> str | None:
    """File content at a ref, or None if it did not exist there.

    The WORKTREE sentinel reads the working tree instead, so the check can run on
    uncommitted changes before a PR exists.
    """
    posix = path.replace(os.sep, "/")
    if ref == WORKTREE:
        target = Path(posix)
        return target.read_text(encoding="utf-8", errors="replace") if target.exists() else None
    return sh("git", "show", f"{ref}:{posix}")


def frontmatter(text: str | None) -> dict[str, str]:
    if not text:
        return {}
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def tree_files(ref: str, prefix: str) -> set[str]:
    """Paths under prefix at ref. Empty when the prefix does not exist."""
    if ref == WORKTREE:
        root = Path(prefix.rstrip("/"))
        if not root.exists():
            return set()
        return {p.as_posix() for p in root.rglob("*") if p.is_file()}
    out = sh("git", "ls-tree", "-r", "--name-only", ref, "--", prefix)
    return set(out.splitlines()) if out else set()


def skill_map(ref: str, plugin: str) -> dict[str, dict[str, str]]:
    """Skill directory -> frontmatter fields, at a ref."""
    prefix = f"{PLUGINS_DIR}/{plugin}/"
    return {
        path.rsplit("/", 1)[0]: frontmatter(read_at(ref, path))
        for path in tree_files(ref, prefix)
        if path.endswith("/SKILL.md")
    }


def component_files(ref: str, plugin: str, kind: str) -> set[str]:
    prefix = f"{PLUGINS_DIR}/{plugin}/{kind}/"
    return {p for p in tree_files(ref, prefix) if p.endswith(".md")}


def plugins_at(ref: str) -> set[str]:
    """Plugin directory names at a ref, excluding unregistered ones."""
    # plugins/<name>/<something> — anything shallower is not inside a plugin.
    depth_inside_a_plugin = 3
    names = {
        parts[1]
        for parts in (p.split("/") for p in tree_files(ref, f"{PLUGINS_DIR}/"))
        if len(parts) >= depth_inside_a_plugin
    }
    return names - set(UNREGISTERED)


def is_hidden(fields: dict[str, str]) -> bool:
    return fields.get("disable-model-invocation", "").lower() == "true"


def content_changed(base: str, head: str, path: str) -> bool:
    """Whether anything under path differs, in one git call."""
    if head == WORKTREE:
        status = sh("git", "status", "--porcelain", "--", path)
        if status and status.strip():
            return True
        diff = sh("git", "diff", "--name-only", base, "--", path)
    else:
        diff = sh("git", "diff", "--name-only", base, head, "--", path)
    return bool(diff and diff.strip())


def classify(plugin: str, base: str, head: str) -> tuple[Level | None, list[str]]:
    """Structural bump level for one plugin, with human-readable reasons."""
    level: Level = "patch"
    reasons: list[str] = []
    before, after = skill_map(base, plugin), skill_map(head, plugin)

    for gone in sorted(set(before) - set(after)):
        level = higher(level, "major")
        reasons.append(f"skill removed: {gone.rsplit('/', 1)[-1]}")
    for added in sorted(set(after) - set(before)):
        level = higher(level, "minor")
        reasons.append(f"skill added: {added.rsplit('/', 1)[-1]}")

    for path in sorted(set(before) & set(after)):
        old, new = before[path], after[path]
        if old.get("name") != new.get("name"):
            level = higher(level, "major")
            reasons.append(f"skill renamed: {old.get('name')} -> {new.get('name')}")
        if not is_hidden(old) and is_hidden(new):
            level = higher(level, "major")
            reasons.append(f"no longer model-invocable: {new.get('name')}")
        elif is_hidden(old) and not is_hidden(new):
            level = higher(level, "minor")
            reasons.append(f"now model-invocable: {new.get('name')}")

    for kind in ("agents", "commands"):
        old_files = component_files(base, plugin, kind)
        new_files = component_files(head, plugin, kind)
        for gone in sorted(old_files - new_files):
            level = higher(level, "major")
            reasons.append(f"{kind[:-1]} removed: {gone.rsplit('/', 1)[-1]}")
        for added in sorted(new_files - old_files):
            level = higher(level, "minor")
            reasons.append(f"{kind[:-1]} added: {added.rsplit('/', 1)[-1]}")

    if not reasons:
        if not content_changed(base, head, f"{PLUGINS_DIR}/{plugin}"):
            return None, []
        reasons.append("content changed")
    return level, reasons


def commit_floor(base: str, head: str, plugin: str) -> Level:
    """Highest level implied by conventional-commit subjects touching a plugin."""
    rev = "HEAD" if head == WORKTREE else head
    log = sh("git", "log", "--format=%s%n%b%n--", f"{base}..{rev}")
    if not log:
        return "patch"

    level: Level = "patch"
    for message in log.split("\n--\n"):
        if not message.strip():
            continue
        match = CONVENTIONAL.search(message.strip().splitlines()[0])
        if not match:
            continue
        scope = (match.group(3) or "").strip()
        if scope and scope not in (plugin, "marketplace", "*"):
            continue
        if match.group(4) or "BREAKING CHANGE" in message:
            level = higher(level, "major")
        elif match.group(1) == "feat":
            level = higher(level, "minor")
    return level


def manifest_version(ref: str, plugin: str) -> str | None:
    raw = read_at(ref, plugin_manifest_path(plugin))
    if not raw:
        return None
    return cast(PluginManifest, json.loads(raw)).get("version", "0.0.0")


def build_rows(base: str, head: str) -> list[Row]:
    rows: list[Row] = []
    for plugin in sorted(plugins_at(head)):
        current = manifest_version(head, plugin)
        if current is None:
            continue

        previous = manifest_version(base, plugin)
        if previous is None:
            rows.append(Row(plugin, "-", current, None, "new plugin", True))
            continue

        level, reasons = classify(plugin, base, head)
        if level is None:
            continue
        level = higher(level, commit_floor(base, head, plugin))
        floor = bump(previous, level)
        satisfied = parse_version(current) >= parse_version(floor)
        rows.append(Row(plugin, previous, current, level, "; ".join(reasons[:4]), satisfied))
    return rows


def report(rows: list[Row]) -> list[Row]:
    width = max(len(r.plugin) for r in rows)
    print(f"{'plugin':<{width}}  {'base':<8}  {'current':<8}  {'needs':<6}  why")

    shortfalls: list[Row] = []
    for row in rows:
        if row.level is None:
            print(
                f"{row.plugin:<{width}}  {row.previous:<8}  {row.current:<8}  {'-':<6}  {row.why}"
            )
            continue
        floor = bump(row.previous, row.level)
        mark = "ok" if row.satisfied else f"BELOW -> needs >= {floor}"
        print(
            f"{row.plugin:<{width}}  {row.previous:<8}  {row.current:<8}  "
            f"{row.level:<6}  {row.why}  [{mark}]"
        )
        if not row.satisfied:
            shortfalls.append(row)
    return shortfalls


def apply_bumps(shortfalls: list[Row], base: str, roster_changed: bool) -> None:
    marketplace: Marketplace = load_marketplace()
    by_name = {e.get("name", ""): e for e in entries(marketplace)}

    for row in shortfalls:
        if row.level is None:
            continue
        floor = bump(row.previous, row.level)
        path = plugin_manifest_path(row.plugin)
        manifest = cast(PluginManifest, json.loads(Path(path).read_text(encoding="utf-8")))
        manifest["version"] = floor
        write_json(path, manifest)
        if row.plugin in by_name:
            by_name[row.plugin]["version"] = floor
        print(f"applied: {row.plugin} -> {floor}")

    if shortfalls or roster_changed:
        raw = read_at(base, MARKETPLACE_PATH)
        previous_meta = "0.0.0"
        if raw:
            previous_meta = (
                cast(Marketplace, json.loads(raw)).get("metadata", {}).get("version", "0.0.0")
            )
        metadata = marketplace.setdefault("metadata", {})
        metadata["version"] = bump(previous_meta, "minor" if roster_changed else "patch")
        write_json(MARKETPLACE_PATH, marketplace)
        print(f"marketplace -> {metadata['version']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--base", default="origin/main")
    _ = parser.add_argument("--head", default="HEAD")
    _ = parser.add_argument("--worktree", action="store_true", help="include uncommitted changes")
    _ = parser.add_argument("--apply", action="store_true", help="write the bumps")
    _ = parser.add_argument("--format", choices=("text", "github"), default="text")
    args = parser.parse_args(argv)

    base = str(args.base)
    head = WORKTREE if bool(args.worktree) else str(args.head)

    if sh("git", "rev-parse", "--verify", base) is None:
        print(f"base ref not found: {base}", file=sys.stderr)
        return 3

    rows = build_rows(base, head)
    if not rows:
        print(f"No plugin changes against {base}.")
        return 0

    shortfalls = report(rows)

    if bool(args.apply):
        apply_bumps(shortfalls, base, plugins_at(base) != plugins_at(head))
        return 0

    if not shortfalls:
        print("\nAll plugin versions are at or above the required floor.")
        return 0

    print(
        f"\n{len(shortfalls)} plugin(s) below the floor. Fix with:"
        f"\n  python scripts/bump-versions.py --base {base} --apply"
    )

    worst: Level = "patch"
    for row in shortfalls:
        if row.level is None:
            continue
        worst = higher(worst, row.level)
        if str(args.format) == "github":
            kind = "error" if row.level == "major" else "warning"
            print(
                f"::{kind} file={plugin_manifest_path(row.plugin)}::"
                f"{row.plugin} needs version >= {bump(row.previous, row.level)} "
                f"({row.level} change)"
            )

    return 2 if worst == "major" else 1


if __name__ == "__main__":
    sys.exit(main())
