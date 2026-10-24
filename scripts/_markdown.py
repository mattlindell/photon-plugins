from __future__ import annotations

import re

FENCE = re.compile(r"^\s*(```|~~~)")
FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
NOT_A_KEY = (" ", "\t", "#", "-")


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


def frontmatter_keys(text: str) -> list[str]:
    return list(frontmatter_scalars(text))


def frontmatter_scalars(text: str | None) -> dict[str, str]:
    if not text:
        return {}
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(NOT_A_KEY):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("\"'")
    return fields
