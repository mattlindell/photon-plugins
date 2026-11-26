#!/usr/bin/env python3
"""Check that upstreams.json, UPSTREAMS.md, and the NOTICE files agree.

Usage:
    python scripts/lint-upstreams.py            # check
    python scripts/lint-upstreams.py --apply    # regenerate the UPSTREAMS.md Pin table, then check

The record is the source of truth (ADR-0006). Exits 1 on any problem, so it
works as a pre-commit or CI gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple

from _markdown import unfenced_lines
from _upstreams import Record, RecordError, load_record, outcome_state

NOTICE_GLOB = "plugins/*/NOTICE.md"
UPSTREAMS_MD = "UPSTREAMS.md"
BEGIN = "<!-- BEGIN GENERATED: pins. Edit upstreams.json, then run lint-upstreams.py --apply -->"
END = "<!-- END GENERATED: pins -->"

FULL_SHA = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
REVIEWED_THROUGH = re.compile(r"reviewed\s+through", re.IGNORECASE)
TRACKED = "tracked"
DERIVED = re.compile(r"\*\*derived\*\*, forked from `[0-9a-f]{7,39}`")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
SPAN = re.compile(r"`([^`\n]+)`")

FIX_STATE = f"a lineage state is `{TRACKED}` or `**derived**, forked from `<short sha>``"


class Problem(NamedTuple):
    rule: str
    where: str
    message: str


class Row(NamedTuple):
    """One row of a NOTICE lineage table."""

    notice: str
    line: int
    upstream: str
    path: str
    state: str


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def lineage_rows(root: Path, notice: Path) -> tuple[list[Row], list[Problem]]:
    """Rows of every table whose last column is State, keyed to the heading above it."""
    rel = notice.relative_to(root).as_posix()
    plugin_dir = notice.parent.relative_to(root).as_posix()
    lines = unfenced_lines(notice.read_text(encoding="utf-8"))
    rows: list[Row] = []
    problems: list[Problem] = []
    heading = ""
    in_table = False
    for i, (lineno, line) in enumerate(lines):
        if match := HEADING.match(line):
            heading = match.group(1)
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        following = lines[i + 1][1] if i + 1 < len(lines) else ""
        if not in_table and SEPARATOR.match(following):
            in_table = cells(line)[-1] == "State"
            continue
        if not in_table or SEPARATOR.match(line):
            continue
        row = cells(line)
        span = SPAN.search(row[0])
        if not span:
            problems.append(
                Problem("lineage-state", f"{rel}:{lineno}", "row names no path in its first cell")
            )
            continue
        rows.append(Row(rel, lineno, heading, f"{plugin_dir}/{span.group(1)}", row[-1]))
    return rows, problems


def check_notice_text(root: Path, notice: Path) -> list[Problem]:
    """Rule 1: a NOTICE restates no Pin."""
    rel = notice.relative_to(root).as_posix()
    problems: list[Problem] = []
    for lineno, line in enumerate(notice.read_text(encoding="utf-8").splitlines(), 1):
        if FULL_SHA.search(line):
            problems.append(
                Problem(
                    "pin-restated",
                    f"{rel}:{lineno}",
                    "full SHA in a NOTICE; the record holds SHAs, use a short one",
                )
            )
        if REVIEWED_THROUGH.search(line):
            problems.append(
                Problem(
                    "pin-restated",
                    f"{rel}:{lineno}",
                    '"reviewed through" in a NOTICE; the Pin lives in upstreams.json',
                )
            )
    return problems


def check_rows(rows: list[Row], record: Record) -> list[Problem]:
    """Rules 2 and 3: every state is well formed, every table names a known upstream."""
    names = {u["name"] for u in record["upstreams"]}
    problems: list[Problem] = []
    reported: set[tuple[str, str]] = set()
    for row in rows:
        where = f"{row.notice}:{row.line}"
        if row.state != TRACKED and not DERIVED.fullmatch(row.state):
            problems.append(Problem("lineage-state", where, f"{row.state!r}; {FIX_STATE}"))
        if row.upstream not in names and (row.notice, row.upstream) not in reported:
            reported.add((row.notice, row.upstream))
            problems.append(
                Problem(
                    "unknown-upstream",
                    where,
                    f"lineage table under heading {row.upstream!r}, which names no upstream"
                    f" in upstreams.json (known: {', '.join(sorted(names))})",
                )
            )
    return problems


def check_log_ends_at_pin(record: Record) -> list[Problem]:
    """Rule 4: the Pin moves only with a recorded review, and reviews chain end to end."""
    problems: list[Problem] = []
    for upstream in record["upstreams"]:
        log = upstream["log"]
        for i in range(1, len(log)):
            start, previous = log[i]["from"], log[i - 1]["to"]
            if start != previous:
                problems.append(
                    Problem(
                        "log-pin",
                        f"upstreams.json: {upstream['name']}",
                        f"log[{i}] starts at {(start or 'null')[:7]},"
                        f" but log[{i - 1}] ended at {previous[:7]}",
                    )
                )
        last = log[-1]["to"]
        pin = upstream["pin"]["sha"]
        if last != pin:
            problems.append(
                Problem(
                    "log-pin",
                    f"upstreams.json: {upstream['name']}",
                    f"newest Sync log entry ends at {last[:7]}, but the Pin is {pin[:7]}",
                )
            )
    return problems


def check_demotions(rows: list[Row], record: Record) -> list[Problem]:
    """Rule 6: two consecutive `diverged` outcomes demote a skill to Derived (ADR-0004).

    The newest entry must name every tracked row, so a review that skips a skill
    cannot make two non-consecutive `diverged` outcomes look adjacent, and a key
    that drifts from its NOTICE row cannot exempt the skill.
    """
    problems: list[Problem] = []
    for upstream in record["upstreams"]:
        history: dict[str, list[str]] = {}
        for entry in upstream["log"]:
            for path, outcome in entry["outcomes"].items():
                history.setdefault(path, []).append(outcome_state(outcome))
        newest = upstream["log"][-1]["outcomes"]
        for row in rows:
            if row.upstream != upstream["name"] or row.state != TRACKED:
                continue
            if row.path not in newest:
                problems.append(
                    Problem(
                        "demotion",
                        f"{row.notice}:{row.line}",
                        f"newest {upstream['name']} Sync log entry has no outcome for"
                        f" tracked {row.path}; every review records one per tracked row",
                    )
                )
            elif history[row.path][-2:] == ["diverged", "diverged"]:
                problems.append(
                    Problem(
                        "demotion",
                        f"{row.notice}:{row.line}",
                        f"{row.path} is still tracked after two consecutive diverged"
                        f" outcomes from {upstream['name']}; mark it **derived**",
                    )
                )
    return problems


def check_outcome_paths(root: Path, record: Record) -> list[Problem]:
    """Rule 7: every outcome names a path that exists, so a rename updates the record."""
    problems: list[Problem] = []
    for upstream in record["upstreams"]:
        seen: set[str] = set()
        for entry in upstream["log"]:
            for path in entry["outcomes"]:
                if path in seen:
                    continue
                seen.add(path)
                exists = any(root.glob(path)) if "*" in path else (root / path).exists()
                if not exists:
                    problems.append(
                        Problem(
                            "missing-path",
                            f"upstreams.json: {upstream['name']}",
                            f"outcome path {path} does not exist",
                        )
                    )
    return problems


def render_pins(record: Record) -> str:
    lines = [
        "| Upstream | Pin | Version | Committed | Reviewed | Forked from |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for upstream in record["upstreams"]:
        repo = upstream["repository"].removesuffix("/")
        pin = upstream["pin"]
        fork = upstream["fork_point"]
        lines.append(
            f"| [{upstream['name']}]({repo}) "
            f"| [`{pin['sha'][:7]}`]({repo}/commit/{pin['sha']}) "
            f"| {pin['version']} | {pin['committed']} | {pin['reviewed']} "
            f"| `{fork['sha'][:7]}` ({fork['version']}) |"
        )
    return "\n".join([BEGIN, *lines, END])


def split_block(text: str) -> tuple[str, str, str] | None:
    """(before, block, after) around the generated markers, or None if absent."""
    start = text.find(BEGIN)
    end = text.find(END, start + 1) if start != -1 else -1
    if start == -1 or end == -1:
        return None
    end += len(END)
    return text[:start], text[start:end], text[end:]


def check_block(root: Path, record: Record) -> list[Problem]:
    """Rule 5: the human view matches the record."""
    path = root / UPSTREAMS_MD
    if not path.exists():
        return [Problem("stale-block", UPSTREAMS_MD, "missing")]
    parts = split_block(path.read_text(encoding="utf-8"))
    if parts is None:
        return [Problem("stale-block", UPSTREAMS_MD, "generated Pin table markers not found")]
    if parts[1] != render_pins(record):
        return [
            Problem(
                "stale-block",
                UPSTREAMS_MD,
                "Pin table does not match upstreams.json; run lint-upstreams.py --apply",
            )
        ]
    return []


def apply(root: Path, record: Record) -> bool:
    """Rewrite the generated block. True when the file changed."""
    path = root / UPSTREAMS_MD
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    parts = split_block(text)
    if parts is None:
        return False
    updated = parts[0] + render_pins(record) + parts[2]
    if updated == text:
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        _ = fh.write(updated)
    return True


def check(root: Path, record: Record) -> list[Problem]:
    rows: list[Row] = []
    problems: list[Problem] = []
    for notice in sorted(root.glob(NOTICE_GLOB)):
        problems += check_notice_text(root, notice)
        found, malformed = lineage_rows(root, notice)
        rows += found
        problems += malformed
    problems += check_rows(rows, record)
    problems += check_log_ends_at_pin(record)
    problems += check_block(root, record)
    problems += check_demotions(rows, record)
    problems += check_outcome_paths(root, record)
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    _ = parser.add_argument(
        "--apply", action="store_true", help="regenerate the UPSTREAMS.md Pin table"
    )
    _ = parser.add_argument("--root", type=Path, default=Path(), help="repository root")
    args = parser.parse_args(argv)
    root: Path = args.root

    try:
        record = load_record(root)
    except RecordError as exc:
        print("upstreams.json does not match the record shape (ADR-0006):")
        for line in str(exc).splitlines():
            print(f"  {line}")
        return 1

    if args.apply and apply(root, record):
        print(f"Regenerated the Pin table in {UPSTREAMS_MD}.")

    problems = check(root, record)
    if problems:
        print(f"Upstream record problems ({len(problems)}):")
        for p in problems:
            print(f"  {p.where}  [{p.rule}] {p.message}")
        return 1

    print("upstreams.json, UPSTREAMS.md, and every NOTICE agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
