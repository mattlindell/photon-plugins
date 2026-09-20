#!/usr/bin/env python3
"""Check that every relative markdown link and heading anchor resolves.

Usage:
    python scripts/lint-links.py [path ...]            # defaults to plugins/ and docs/
    python scripts/lint-links.py --exclude product-team

Skips fenced code blocks and template placeholders, both of which legitimately
contain example links that point nowhere.

Exits 1 if anything is broken, so it works as a pre-commit or CI gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

FENCE = re.compile(r"^\s*(```|~~~)")
LINK = re.compile(r"\]\((?!https?:|mailto:)([^)]+)\)")
# Illustrative targets: (link), (<some thing>), (path/to/x). A target containing
# < or > is a template slot by convention.
PLACEHOLDER = re.compile(r"^(link|url|path|\.\.\.)$|[<>]")
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)


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


def unfenced_lines(text: str) -> list[tuple[int, str]]:
    """Lines outside fenced code blocks, as (1-based lineno, line)."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((lineno, line))
    return out


def check(path: Path) -> list[Problem]:
    problems: list[Problem] = []
    text = path.read_text(encoding="utf-8", errors="replace")

    for lineno, line in unfenced_lines(text):
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

    excluded: set[str] = {e for spec in args.exclude for e in str(spec).split(",") if e}
    roots = [Path(p) for p in (args.paths or ["plugins", "docs"])]

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

    print("All relative links and anchors resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
