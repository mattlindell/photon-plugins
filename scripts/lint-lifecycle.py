#!/usr/bin/env python3
"""Check every Work item lifecycle table against the contract in ADR-0007.

Usage:
    python scripts/lint-lifecycle.py [--root PATH]

This repo's docs/agents/issue-tracker.md must carry the section. A
setup-ph-plan issue-tracker-*.md seed is checked only when it carries one.
Exits 1 on any problem, so it works as a pre-commit or CI gate.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple

from _markdown import unfenced_lines

HEADING = "## Work item lifecycle"
COLUMNS = ("Event", "Actor", "Action")
EVENTS = ("start", "review requested", "PR merged", "halt")
ACTORS = frozenset({"agent", "automation", "none"})

TRACKER_DOC = Path("docs/agents/issue-tracker.md")
SEED_GLOB = "plugins/ph-plan/skills/setup-ph-plan/references/issue-tracker-*.md"


class Row(NamedTuple):
    line: int
    event: str
    actor: str
    action: str


class Problem(NamedTuple):
    where: str
    rule: str
    message: str


def cells(line: str) -> list[str]:
    return [c.strip().strip("`").strip() for c in line.strip().strip("|").split("|")]


def section(text: str) -> list[tuple[int, str]] | None:
    """Unfenced lines under the lifecycle heading, up to the next H2 or higher."""
    lines = unfenced_lines(text)
    for i, (_, line) in enumerate(lines):
        if line.rstrip() == HEADING:
            body = lines[i + 1 :]
            end = next(
                (j for j, (_, ln) in enumerate(body) if ln.startswith(("# ", "## "))),
                len(body),
            )
            return body[:end]
    return None


def table(body: list[tuple[int, str]]) -> tuple[int, list[str], list[Row]] | None:
    """The first pipe table in the section: header line, header cells, data rows."""
    start = next((i for i, (_, ln) in enumerate(body) if ln.lstrip().startswith("|")), None)
    if start is None:
        return None
    block: list[tuple[int, str]] = []
    for lineno, line in body[start:]:
        if not line.lstrip().startswith("|"):
            break
        block.append((lineno, line))
    header_line, header = block[0]
    rows = [
        Row(lineno, *[*cells(line), "", "", ""][:3])
        for lineno, line in block[2:]  # skip the header and its separator
    ]
    return header_line, cells(header), rows


def check_text(where: str, text: str, *, required: bool) -> list[Problem]:
    body = section(text)
    if body is None:
        if required:
            return [Problem(where, "missing-section", f"no `{HEADING}` section")]
        return []

    found = table(body)
    if found is None:
        return [Problem(where, "missing-table", f"`{HEADING}` has no table")]
    header_line, header, rows = found

    if tuple(header) != COLUMNS:
        return [
            Problem(
                f"{where}:{header_line}",
                "columns",
                f"columns are {' | '.join(header)}, expected {' | '.join(COLUMNS)}",
            )
        ]

    problems: list[Problem] = []
    for row in rows:
        at = f"{where}:{row.line}"
        if row.event not in EVENTS:
            problems.append(Problem(at, "unknown-event", f"`{row.event}` is not an event"))
        if row.actor not in ACTORS:
            problems.append(
                Problem(
                    at,
                    "unknown-actor",
                    f"`{row.actor}` is not an actor; use one of {', '.join(sorted(ACTORS))}",
                )
            )

    counts = Counter(row.event for row in rows)
    for event in EVENTS:
        if counts[event] == 0:
            problems.append(Problem(where, "missing-event", f"no `{event}` row"))
        elif counts[event] > 1:
            problems.append(
                Problem(where, "duplicate-event", f"`{event}` has {counts[event]} rows")
            )
    return problems


def check(root: Path) -> list[Problem]:
    targets = [(root / TRACKER_DOC, True)]
    targets += [(seed, False) for seed in sorted(root.glob(SEED_GLOB))]

    problems: list[Problem] = []
    for path, required in targets:
        where = path.relative_to(root).as_posix()
        if not path.is_file():
            problems.append(Problem(where, "missing-file", "file not found"))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        problems += check_text(where, text, required=required)
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    _ = parser.add_argument("--root", type=Path, default=Path(), help="repository root")
    args = parser.parse_args(argv)
    root: Path = args.root

    problems = check(root)
    if problems:
        print(f"Work item lifecycle problems ({len(problems)}):")
        for p in problems:
            print(f"  {p.where}  [{p.rule}] {p.message}")
        print("See docs/adr/0007-the-work-item-lifecycle-is-declared-per-repo.md.")
        return 1

    print("Every Work item lifecycle table matches the contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
