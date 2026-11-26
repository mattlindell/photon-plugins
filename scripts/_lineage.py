"""NOTICE lineage tables: which skill here derives from which upstream path, in what state.

A lineage table is any NOTICE table whose last column is `State`. The heading above
it names the upstream as `upstreams.json` does (ADR-0006). The first cell names the
path here; the first other cell holding a backtick span names the upstream path.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

from _markdown import unfenced_lines

TRACKED = "tracked"
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
SPAN = re.compile(r"`([^`\n]+)`")
ELLIPSIS = "…/"
# "Every pstack-claude path sits under `plugins/pstack/`, shortened to `…/` below."
ELLIPSIS_PREFIX = re.compile(r"under\s+`([^`\n]+)`,\s+shortened\s+to\s+`…/`")


class Row(NamedTuple):
    """One row of a NOTICE lineage table."""

    notice: str
    line: int
    upstream: str
    path: str
    source: str
    state: str


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def lineage_rows(root: Path, notice: Path) -> tuple[list[Row], list[tuple[str, str]]]:
    """Every lineage row in `notice`, plus (where, message) for rows that name no path.

    `path` is repo-relative, as Sync log outcome keys are. `source` is the upstream
    path with the NOTICE's `…/` shorthand expanded, or "" when the row names none.
    """
    rel = notice.relative_to(root).as_posix()
    plugin_dir = notice.parent.relative_to(root).as_posix()
    text = notice.read_text(encoding="utf-8")
    prefix = match.group(1) if (match := ELLIPSIS_PREFIX.search(text)) else None
    lines = unfenced_lines(text)
    rows: list[Row] = []
    malformed: list[tuple[str, str]] = []
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
            malformed.append((f"{rel}:{lineno}", "row names no path in its first cell"))
            continue
        source = next((m.group(1) for c in row[1:-1] if (m := SPAN.search(c))), "")
        if prefix and source.startswith(ELLIPSIS):
            source = prefix.removesuffix("/") + "/" + source.removeprefix(ELLIPSIS)
        rows.append(Row(rel, lineno, heading, f"{plugin_dir}/{span.group(1)}", source, row[-1]))
    return rows, malformed
