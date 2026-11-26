#!/usr/bin/env python3
"""Sync review analysis: an upstream's commits since its Pin, per Tracked skill, plus candidates.

Usage:
    python .claude/skills/sync-upstream/scripts/analyze_upstream.py <name>
    python .claude/skills/sync-upstream/scripts/analyze_upstream.py <name> --clone-into DIR

Reads `upstreams.json` and every NOTICE lineage table, clones the upstream, and
runs `git log <pin>..HEAD` per Tracked path. A clone, not the GitHub compare
API, because the API truncates large gaps. Changes under no lineage path at all
are candidates, grouped by upstream skill and marked with any earlier decision.

Prints a markdown triage report. Changes nothing in this repository.
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from _lineage import TRACKED, Row, lineage_rows  # noqa: E402
from _upstreams import (  # noqa: E402
    Decision,
    OutcomeState,
    RecordError,
    Upstream,
    load_record,
    outcome_state,
)

NOTICE_GLOB = "plugins/*/NOTICE.md"
OUTSIDE = "(outside any upstream skill)"
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
WILDCARDS = frozenset("*?[")


class AnalysisError(Exception):
    """The analysis cannot run; the message says why."""


class Change(NamedTuple):
    status: str
    path: str


class Commit(NamedTuple):
    sha: str
    date: str
    subject: str
    changes: list[Change]


class Deletion(NamedTuple):
    """An upstream path present at the Pin and gone at HEAD."""

    source: str
    forked_from: str
    """The last upstream commit that carried `source`."""


class TrackedPath(NamedTuple):
    path: str
    source: str
    commits: list[Commit]
    last_outcome: OutcomeState | None
    deletions: list[Deletion]
    """For a glob row, one per matched skill that upstream deleted."""


class Candidate(NamedTuple):
    name: str
    directory: str
    commits: list[Commit]
    prior: Decision | None


class Report(NamedTuple):
    upstream: str
    pin: str
    head: str
    head_version: str
    head_committed: str
    commit_count: int
    tracked: list[TrackedPath]
    candidates: list[Candidate]


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode != 0:
        raise AnalysisError(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout


def version_label(clone: Path, sha: str) -> str:
    """`v1.3.1` at a tag, `v1.3.1+47` past one, the short SHA with no tag behind it."""
    try:
        described = git(clone, "describe", "--tags", "--long", sha).strip()
    except AnalysisError:
        return sha[:7]
    tag, ahead, _ = described.rsplit("-", 2)
    return tag if ahead == "0" else f"{tag}+{ahead}"


def pathspec(source: str) -> str:
    return source.removesuffix("/")


def log(clone: Path, pin: str, specs: Sequence[str]) -> list[Commit]:
    """Commits in pin..HEAD touching `specs`, newest first, with only their matching files."""
    out = git(
        clone,
        "log",
        "--no-renames",
        "--date=short",
        "--format=%x1e%H%x1f%ad%x1f%s",
        "--name-status",
        f"{pin}..HEAD",
        "--",
        *specs,
    )
    commits: list[Commit] = []
    for block in out.split("\x1e")[1:]:
        header, *body = block.strip("\n").split("\n")
        sha, date, subject = header.split("\x1f", 2)
        changes = [Change(*line.split("\t", 1)) for line in body if "\t" in line]
        commits.append(Commit(sha, date, subject, changes))
    return commits


def files_at(clone: Path, rev: str) -> list[str]:
    return git(clone, "ls-tree", "-r", "--name-only", rev).splitlines()


def matching(clone: Path, rev: str, spec: str) -> list[str]:
    """Files at `rev` that `spec` names, by git's own pathspec rules.

    `git ls-tree` takes a pathspec as a literal prefix and never expands a glob,
    so this diffs `rev` against the empty tree, which matches as `git log` does.
    """
    out = git(clone, "diff", "-z", "--name-only", "--no-renames", EMPTY_TREE, rev, "--", spec)
    return [f for f in out.split("\0") if f]


def unit(spec: str, path: str) -> str:
    """The upstream path a lineage row tracks `path` as: one per skill under a glob row."""
    if not WILDCARDS & set(spec):
        return spec
    return "/".join(path.split("/")[: spec.count("/") + 1])


def deletions(
    clone: Path, pin: str, spec: str, at_pin: list[str], at_head: list[str]
) -> list[Deletion]:
    gone = {unit(spec, f) for f in at_pin} - {unit(spec, f) for f in at_head}
    out: list[Deletion] = []
    for source in sorted(gone):
        last = git(clone, "log", "-1", "--format=%H", f"{pin}..HEAD", "--", f":(literal){source}")
        out.append(Deletion(source, git(clone, "rev-parse", f"{last.strip()}^").strip()))
    return out


def skill_dirs(*trees: list[str]) -> list[str]:
    """Every directory holding a SKILL.md in any of `trees`, longest first."""
    dirs = {
        f.removesuffix("SKILL.md")
        for files in trees
        for f in files
        if f == "SKILL.md" or f.endswith("/SKILL.md")
    }
    return sorted(dirs, key=len, reverse=True)


def read_rows(root: Path, name: str) -> list[Row]:
    rows: list[Row] = []
    for notice in sorted(root.glob(NOTICE_GLOB)):
        found, _ = lineage_rows(root, notice)
        rows += [r for r in found if r.upstream == name]
    if not rows:
        raise AnalysisError(f"no NOTICE lineage table is headed {name!r}")
    unnamed = [f"{r.notice}:{r.line}" for r in rows if not r.source]
    if unnamed:
        raise AnalysisError(f"lineage rows name no upstream path: {', '.join(unnamed)}")
    shorthand = [f"{r.notice}:{r.line}" for r in rows if r.source.startswith("…/")]
    if shorthand:
        raise AnalysisError(
            "lineage rows use `…/` but their NOTICE never says what it shortens"
            f" (`under `<prefix>`, shortened to `…/``): {', '.join(shorthand)}"
        )
    return rows


def prior_decisions(upstream: Upstream) -> dict[str, Decision]:
    """The most recent decision on each candidate name across the Sync log."""
    decisions: dict[str, Decision] = {}
    for entry in upstream["log"]:
        for candidate in entry["candidates"]:
            decisions[candidate["name"]] = candidate["decision"]
    return decisions


def last_outcomes(upstream: Upstream) -> dict[str, OutcomeState]:
    outcomes: dict[str, OutcomeState] = {}
    for entry in upstream["log"]:
        for path, outcome in entry["outcomes"].items():
            outcomes[path] = outcome_state(outcome)
    return outcomes


def group_candidates(
    commits: list[Commit], dirs: list[str], decisions: dict[str, Decision]
) -> list[Candidate]:
    """Split each commit's files by the upstream skill directory that holds them."""
    by_dir: dict[str, list[Commit]] = {}
    for commit in commits:
        split: dict[str, list[Change]] = {}
        for change in commit.changes:
            home = next((d for d in dirs if change.path.startswith(d)), "")
            split.setdefault(home, []).append(change)
        for home, changes in split.items():
            by_dir.setdefault(home, []).append(commit._replace(changes=changes))
    candidates: list[Candidate] = []
    for directory, grouped in sorted(by_dir.items(), key=lambda kv: (kv[0] == "", kv[0])):
        name = Path(directory).name if directory else OUTSIDE
        candidates.append(Candidate(name, directory, grouped, decisions.get(name)))
    return candidates


def analyze(root: Path, name: str, clone: Path) -> Report:
    """Clone upstream `name` into `clone` (which must not exist) and triage pin..HEAD."""
    try:
        record = load_record(root)
    except RecordError as exc:
        raise AnalysisError(f"upstreams.json does not match the record shape:\n{exc}") from exc
    upstream = next((u for u in record["upstreams"] if u["name"] == name), None)
    if upstream is None:
        known = ", ".join(u["name"] for u in record["upstreams"])
        raise AnalysisError(f"no upstream named {name!r} in upstreams.json (known: {known})")
    rows = read_rows(root, name)
    pin = upstream["pin"]["sha"]

    result = subprocess.run(
        ["git", "clone", "--quiet", "--no-checkout", upstream["repository"], str(clone)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode != 0:
        raise AnalysisError(f"cloning {upstream['repository']} failed:\n{result.stderr.strip()}")
    if subprocess.run(
        ["git", "-C", str(clone), "cat-file", "-e", f"{pin}^{{commit}}"],
        capture_output=True,
        check=False,
    ).returncode:
        raise AnalysisError(f"the Pin {pin[:7]} is not in the upstream's history")

    head, head_committed = git(clone, "log", "-1", "--format=%H %cs").split()
    commit_count = int(git(clone, "rev-list", "--count", f"{pin}..HEAD"))
    outcomes = last_outcomes(upstream)
    trees = files_at(clone, pin), files_at(clone, "HEAD")

    tracked: list[TrackedPath] = []
    for row in rows:
        if row.state != TRACKED:
            continue
        spec = pathspec(row.source)
        at_pin, at_head = matching(clone, pin, spec), matching(clone, "HEAD", spec)
        if not at_pin and not at_head:
            raise AnalysisError(
                f"{row.notice}:{row.line}: upstream path {row.source} exists neither at"
                " the Pin nor at HEAD; fix the NOTICE row"
            )
        tracked.append(
            TrackedPath(
                row.path,
                row.source,
                log(clone, pin, [spec]),
                outcomes.get(row.path),
                deletions(clone, pin, spec, at_pin, at_head),
            )
        )

    excludes = sorted({f":(exclude){pathspec(r.source)}" for r in rows})
    untracked = log(clone, pin, [".", *excludes])
    candidates = group_candidates(untracked, skill_dirs(*trees), prior_decisions(upstream))
    return Report(
        name,
        pin,
        head,
        version_label(clone, head),
        head_committed,
        commit_count,
        tracked,
        candidates,
    )


def render_commits(commits: list[Commit]) -> list[str]:
    lines: list[str] = []
    for c in commits:
        lines.append(f"- `{c.sha[:7]}` {c.date} {c.subject}")
        lines += [f"  - {ch.status} `{ch.path}`" for ch in c.changes]
    return lines


def render(report: Report) -> str:
    changed = [t for t in report.tracked if t.commits]
    unchanged = [t for t in report.tracked if not t.commits]
    lines = [
        f"# Sync review analysis: {report.upstream}",
        "",
        f"Pin `{report.pin[:7]}` to HEAD `{report.head[:7]}`: {report.commit_count} commits."
        f" {len(changed)} of {len(report.tracked)} Tracked paths changed;"
        f" {len(report.candidates)} candidate groups.",
        "",
        "New Pin, if this review completes:",
        "",
        "```json",
        f'{{"sha": "{report.head}", "version": "{report.head_version}",'
        f' "committed": "{report.head_committed}", "reviewed": "<today>"}}',
        "```",
        "",
        "## Tracked paths with changes",
        "",
    ]
    if not changed:
        lines += ["None.", ""]
    for t in changed:
        lines += [f"### `{t.path}`", "", f"Upstream `{t.source}`."]
        if t.last_outcome == "diverged":
            lines.append("Last outcome was `diverged`: another `diverged` demotes it to Derived.")
        for d in t.deletions:
            split = (
                " Split it out of this glob row into its own row, then demote that row"
                if d.source != pathspec(t.source)
                else " Demote"
            )
            lines.append(
                f"**Deleted upstream:** `{d.source}`.{split} to Derived,"
                f" forked from `{d.forked_from[:7]}`."
            )
        lines += ["", *render_commits(t.commits), ""]
    lines += ["## Tracked paths without changes", ""]
    lines += [f"- `{t.path}`" for t in unchanged] or ["None."]
    lines += ["", "## Candidates", ""]
    if not report.candidates:
        lines += ["None.", ""]
    for c in report.candidates:
        where = f" (`{c.directory}`)" if c.directory else ""
        prior = f", previously **{c.prior}**" if c.prior else ""
        lines += [f"### {c.name}{where}{prior}", "", *render_commits(c.commits), ""]
    return "\n".join(lines).rstrip() + "\n"


def remove_tree(path: Path) -> None:
    """rmtree that also clears the read-only files git writes on Windows."""

    def clear(func: Callable[[str], object], p: str, _: BaseException) -> None:
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onexc=clear)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    _ = parser.add_argument("name", help="upstream name, as in upstreams.json")
    _ = parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root")
    _ = parser.add_argument(
        "--clone-into", type=Path, help="keep the clone here for porting (must not exist)"
    )
    args = parser.parse_args(argv)
    keep: Path | None = args.clone_into
    if keep is not None and keep.exists():
        print(f"{keep} already exists; pass a new directory", file=sys.stderr)
        return 1

    scratch = Path(tempfile.mkdtemp(prefix="sync-upstream-"))
    clone = keep or scratch / "clone"
    try:
        report = analyze(args.root, args.name, clone)
    except AnalysisError as exc:
        print(exc, file=sys.stderr)
        return 1
    finally:
        remove_tree(scratch)
    sys.stdout.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]
    print(render(report), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
