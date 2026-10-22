#!/usr/bin/env python3
"""Check that no model-invocable skill hands off to a human-only skill.

Usage:
    python scripts/lint-handoffs.py

Exits 1 on any Handoff not covered by ALLOWLIST, or on an ALLOWLIST entry that
no longer covers one, so it works as a pre-commit or CI gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

from _manifest import entries, load_marketplace, skill_dirs, source_dir
from _markdown import frontmatter_scalars, unfenced_lines

SPAN = re.compile(r"`([^`\n]+)`")

ALLOWLIST: frozenset[str] = frozenset(
    {
        "ph-build:babysit",  # PV-136
        "ph-build:blast-radius",  # PV-136
        "ph-build:diagnosing-bugs",  # PV-136
        "ph-build:dispatch",  # PV-136
    }
)


class Skill(NamedTuple):
    plugin: str
    name: str
    directory: Path
    human_only: bool

    @property
    def qualified(self) -> str:
        return f"{self.plugin}:{self.name}"


class Handoff(NamedTuple):
    caller: Skill
    path: Path
    line: int
    target: Skill


def load_skills() -> dict[str, Skill]:
    skills: dict[str, Skill] = {}
    for entry in entries(load_marketplace()):
        plugin = entry.get("name", "")
        for directory in skill_dirs(source_dir(entry)):
            path = Path(directory)
            text = (path / "SKILL.md").read_text(encoding="utf-8", errors="replace")
            fields = frontmatter_scalars(text)
            skill = Skill(
                plugin=plugin,
                name=fields.get("name", path.name),
                directory=path,
                human_only=fields.get("disable-model-invocation", "").lower() == "true",
            )
            skills[skill.qualified] = skill
    return skills


def owned_files(skill: Skill, skills: dict[str, Skill]) -> list[Path]:
    nested = [
        other.directory
        for other in skills.values()
        if other.directory != skill.directory and skill.directory in other.directory.parents
    ]
    return sorted(
        path
        for path in skill.directory.rglob("*.md")
        if "node_modules" not in path.parts and not any(n in path.parents for n in nested)
    )


def is_pointer(span: str) -> bool:
    return span.startswith("/")


def resolve(span: str, caller: Skill, skills: dict[str, Skill]) -> Skill | None:
    plugin, _, name = span.rpartition(":")
    return skills.get(f"{plugin or caller.plugin}:{name}")


def handoffs(caller: Skill, skills: dict[str, Skill]) -> list[Handoff]:
    found: list[Handoff] = []
    for path in owned_files(caller, skills):
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in unfenced_lines(text):
            for span in (s.strip() for s in SPAN.findall(line)):
                if is_pointer(span):
                    continue
                target = resolve(span, caller, skills)
                if target and target.human_only:
                    found.append(Handoff(caller, path, lineno, target))
    return found


def main() -> int:
    skills = load_skills()

    found: list[Handoff] = []
    for caller in skills.values():
        if not caller.human_only:
            found.extend(handoffs(caller, skills))

    flagged = [h for h in found if h.caller.qualified not in ALLOWLIST]
    stale = sorted(ALLOWLIST - {h.caller.qualified for h in found})

    print(f"(allowlisted: {', '.join(sorted(ALLOWLIST))})")

    if flagged:
        print(f"Handoffs into human-only skills ({len(flagged)}):")
        for h in flagged:
            print(f"  {h.path.as_posix()}:{h.line}  {h.caller.qualified} -> {h.target.qualified}")
        print(
            "Spell a step the human takes as a Pointer (`/name`), or make the target"
            " model-invocable. See Handoff and Pointer in CONTEXT.md."
        )
    if stale:
        print(f"Stale allowlist entries ({len(stale)}), no Handoff left to cover:")
        for qualified in stale:
            print(f"  {qualified}")
    if flagged or stale:
        return 1

    print("No model-invocable skill hands off to a human-only skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
