#!/usr/bin/env python3
"""Validate the marketplace against what is actually on disk.

Usage:
    python scripts/validate-marketplace.py

Checks:
  - every registered plugin source exists and its plugin.json name matches
  - no plugin.json uses the object form of `repository`, which makes Claude Code
    silently discover zero skills from that plugin
  - every pinned `skills` array matches the SKILL.md files on disk exactly
  - no plugin directory is unregistered (product-team is a known exception)
  - every SKILL.md carries name and description

Exits 1 on any failure, so it works as a pre-commit or CI gate.
"""

from __future__ import annotations

import sys
from pathlib import Path

from _manifest import (
    PLUGINS_DIR,
    UNREGISTERED,
    entries,
    load_marketplace,
    load_plugin,
    plugin_manifest_path,
    skill_dirs,
    source_dir,
)

FRONTMATTER_WINDOW = 2000


def check_registered(failures: list[str]) -> set[str]:
    """Validate each registry entry; return the set of registered directories."""
    registered: set[str] = set()
    marketplace = load_marketplace()

    for entry in entries(marketplace):
        name = entry.get("name", "<unnamed>")
        src = source_dir(entry)
        registered.add(Path(src).name)

        if not Path(src).is_dir():
            failures.append(f"source missing: {src}")
            continue
        if not Path(plugin_manifest_path(Path(src).name)).exists():
            failures.append(f"no plugin.json: {src}")
            continue

        manifest = load_plugin(Path(src).name)
        if manifest.get("name") != name:
            failures.append(f"name mismatch: {manifest.get('name')} vs {name}")

        if isinstance(manifest.get("repository"), dict):
            failures.append(f"{name}: repository is an object — this silently drops every skill")

        pinned = manifest.get("skills")
        if pinned is not None:
            on_disk = sorted(f"./{Path(d).relative_to(src).as_posix()}" for d in skill_dirs(src))
            if on_disk != sorted(pinned):
                failures.append(
                    f"{name}: pinned skills array does not match disk "
                    f"({len(pinned)} pinned vs {len(on_disk)} on disk)"
                )
    return registered


def check_unregistered(registered: set[str], failures: list[str]) -> None:
    on_disk = {p.name for p in Path(PLUGINS_DIR).iterdir() if p.is_dir()}
    stray = on_disk - registered - set(UNREGISTERED)
    if stray:
        failures.append("unregistered plugin dirs: " + ", ".join(sorted(stray)))


def check_frontmatter(failures: list[str]) -> int:
    count = 0
    for skill in Path(PLUGINS_DIR).rglob("SKILL.md"):
        count += 1
        head = skill.read_text(encoding="utf-8", errors="replace")[:FRONTMATTER_WINDOW]
        if "\nname:" not in head:
            failures.append(f"no name: {skill.as_posix()}")
        if "description:" not in head:
            failures.append(f"no description: {skill.as_posix()}")
    return count


def main() -> int:
    failures: list[str] = []

    registered = check_registered(failures)
    check_unregistered(registered, failures)
    skill_count = check_frontmatter(failures)

    print(f"registered plugins: {len(registered)}")
    print(f"skills on disk: {skill_count}")

    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print("\nAll marketplace + manifest checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
