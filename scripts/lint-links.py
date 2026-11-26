#!/usr/bin/env python3
"""Check that every relative markdown link, heading anchor, and backtick path resolves.

A backtick path such as `playbooks/feature.md` is checked only when its first
segment is a directory beside the file, at its skill root, or at its plugin root.
Anything else names a file the consumer owns.

Under docs/, a skill or command reference must name one that exists under plugins/:
`plugin:skill` or `/plugin:skill` anywhere outside a code fence, and a bare `/name`
when it opens a backtick span. A skill counts only when its plugin is registered in
marketplace.json. The check skips a prefix that is not a directory under plugins/,
such as `pstack:tdd`.

Usage:
    python scripts/lint-links.py [path ...]            # defaults to plugins/, docs/, and .claude/
    python scripts/lint-links.py --exclude product-team

Skips fenced code blocks and template placeholders, both of which legitimately
contain example links that point nowhere.

Exits 1 if anything is broken, so it works as a pre-commit or CI gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from functools import cache
from pathlib import Path
from typing import NamedTuple

from _manifest import MARKETPLACE_PATH, entries, load_marketplace, source_dir
from _markdown import unfenced_lines

LINK = re.compile(r"\]\((?!https?:|mailto:)([^)]+)\)")
# Illustrative targets: (link), (<some thing>), (path/to/x). A target containing
# < or > is a template slot by convention.
PLACEHOLDER = re.compile(r"^(link|url|path|\.\.\.)$|[<>]")
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
BACKTICK = re.compile(r"(?<!`)`([^`\s]+/[^`\s]*\.(?:md|json|ya?ml|py|sh))`(?!`)")
CONSUMER_PREFIXES = ("~", "@", "/", "./")
QUALIFIED = re.compile(r"(?<![\w./:@-])/?([a-z][a-z0-9-]*):([A-Za-z0-9][A-Za-z0-9-]*)(?![\w-])")
SLASH = re.compile(r"`/([A-Za-z][A-Za-z0-9-]*)(?:\s[^`]*)?`")
# Claude Code's own commands, which no plugin defines.
BUILTIN_COMMANDS = frozenset(
    [
        "add-dir",
        "agents",
        "clear",
        "code-review",
        "compact",
        "config",
        "context",
        "cost",
        "doctor",
        "exit",
        "export",
        "help",
        "hooks",
        "init",
        "login",
        "logout",
        "loop",
        "mcp",
        "memory",
        "model",
        "permissions",
        "plugin",
        "resume",
        "review",
        "rewind",
        "security-review",
        "simplify",
        "status",
        "statusline",
        "vim",
    ]
)


class Problem(NamedTuple):
    path: Path
    line: int
    target: str
    reason: str


def slugify(heading: str) -> str:
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def headings(path: Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return {slugify(h) for h in HEADING.findall(text)}


def resolution_bases(path: Path, first_segment: str) -> list[Path]:
    path = path.resolve()
    if first_segment == "..":
        return [path.parent]
    skill = next((p for p in path.parents if (p / "SKILL.md").is_file()), None)
    plugin = next((p for p in path.parents if p.parent.name == "plugins"), None)
    bases = dict.fromkeys(b for b in (path.parent, skill, plugin) if b)
    return [base for base in bases if (base / first_segment).is_dir()]


def check_backtick(path: Path, lineno: int, target: str) -> Problem | None:
    if target.startswith(CONSUMER_PREFIXES) or "*" in target or PLACEHOLDER.search(target):
        return None
    bases = resolution_bases(path, target.split("/", 1)[0])
    if not bases or any((base / target).exists() for base in bases):
        return None
    return Problem(path, lineno, target, "backtick path not found")


@cache
def invocable(root: Path) -> dict[str, frozenset[str]]:
    """Skill directory names and command stems, keyed by plugin.

    A plugin directory missing from the registry maps to nothing, since nobody can
    install it.
    """
    catalog: dict[str, frozenset[str]] = {
        p.name: frozenset() for p in (root / "plugins").iterdir() if p.is_dir()
    }
    for entry in entries(load_marketplace(str(root / MARKETPLACE_PATH))):
        plugin = root / source_dir(entry)
        skills = {s.parent.name for s in plugin.rglob("SKILL.md") if "node_modules" not in s.parts}
        commands = {c.stem for c in plugin.glob("commands/*.md")}
        catalog[entry.get("name", plugin.name)] = frozenset(skills | commands)
    return catalog


def repo_root_for_docs(path: Path) -> Path | None:
    docs = next((p for p in path.resolve().parents if p.name == "docs"), None)
    if docs and (docs.parent / MARKETPLACE_PATH).is_file():
        return docs.parent
    return None


def check_references(catalog: dict[str, frozenset[str]], line: str) -> list[str]:
    unknown: list[str] = []
    for match in QUALIFIED.finditer(line):
        plugin, name = match.groups()
        if plugin in catalog and name not in catalog[plugin]:
            unknown.append(f"{plugin}:{name}")
    every = frozenset().union(*catalog.values(), BUILTIN_COMMANDS)
    unknown.extend(f"/{m.group(1)}" for m in SLASH.finditer(line) if m.group(1) not in every)
    return unknown


def check(path: Path) -> list[Problem]:
    problems: list[Problem] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    root = repo_root_for_docs(path)
    catalog = invocable(root) if root else None

    for lineno, line in unfenced_lines(text):
        if catalog is not None:
            problems.extend(
                Problem(path, lineno, ref, "unknown skill or command")
                for ref in check_references(catalog, line)
            )
        for match in BACKTICK.finditer(line):
            if problem := check_backtick(path, lineno, match.group(1)):
                problems.append(problem)
        for match in LINK.finditer(line):
            target = match.group(1).strip()
            if PLACEHOLDER.search(target):
                continue

            filepart, _, fragment = target.partition("#")
            resolved = (path.parent / filepart).resolve() if filepart else path

            if filepart and not resolved.exists():
                problems.append(Problem(path, lineno, target, "missing file"))
                continue
            if (
                fragment
                and resolved.suffix == ".md"
                and slugify(fragment) not in headings(resolved)
            ):
                problems.append(Problem(path, lineno, target, "no such anchor"))
    return problems


def markdown_files(root: Path, excluded: set[str]) -> list[Path]:
    if root.is_file():
        return [] if any(part in excluded for part in root.parts) else [root]
    return sorted(
        p
        for p in root.rglob("*.md")
        if p.is_file() and not any(part in excluded for part in p.parts)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("paths", nargs="*", default=None)
    _ = parser.add_argument(
        "--exclude", action="append", default=[], help="directory name to skip (repeatable)"
    )
    args = parser.parse_args(argv)

    # Installed dependencies carry their own markdown, which is not ours to lint.
    excluded: set[str] = {"node_modules"} | {
        e for spec in args.exclude for e in str(spec).split(",") if e
    }
    roots = [Path(p) for p in (args.paths or ["plugins", "docs", ".claude"])]

    problems: list[Problem] = []
    for root in roots:
        for path in markdown_files(root, excluded):
            problems.extend(check(path))

    if excluded:
        print(f"(excluded: {', '.join(sorted(excluded))})")

    if problems:
        print(f"Broken links ({len(problems)}):")
        for problem in problems:
            print(
                f"  {problem.path.as_posix()}:{problem.line}  {problem.target}  ({problem.reason})"
            )
        return 1

    print("All relative links, anchors, backtick paths, and skill references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
