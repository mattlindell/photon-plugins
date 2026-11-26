from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import analyze_upstream

GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false"]

NOTICE = """# NOTICE

Every example path sits under `pkg/`, shortened to `…/` below.

### example

| Here | Upstream | State |
| --- | --- | --- |
| `skills/alpha/` | `…/skills/alpha/` | tracked |
| `skills/quiet/` | `…/skills/quiet/` | tracked |
| `skills/doomed/` | `…/skills/doomed/` | tracked |
| `skills/principles/principle-*/` | `…/skills/principle-*/` | tracked |
| `skills/rules/rule-*/` | `…/skills/rule-*/` | tracked |
| `skills/forked/` | `…/skills/forked/` | **derived**, forked from `aaaaaaa` |
"""


def run(repo: Path, *args: str) -> str:
    return subprocess.run(
        [*GIT, "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def commit(repo: Path, message: str, files: dict[str, str | None]) -> str:
    for rel, content in files.items():
        path = repo / rel
        if content is None:
            run(repo, "rm", "-q", "-r", rel)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        run(repo, "add", rel)
    run(repo, "commit", "-q", "-m", message)
    return run(repo, "rev-parse", "HEAD")


class AnalyzeTest(unittest.TestCase):
    report: analyze_upstream.Report

    @classmethod
    def setUpClass(cls) -> None:
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        cls.addClassCleanup(tmp.cleanup)
        base = Path(tmp.name)
        upstream = base / "upstream"
        upstream.mkdir()
        run(upstream, "init", "-q", "-b", "main")

        commit(
            upstream,
            "before pin",
            {
                "pkg/skills/alpha/SKILL.md": "a0",
                "pkg/skills/quiet/SKILL.md": "q0",
                "pkg/skills/doomed/SKILL.md": "d0",
                "pkg/skills/principle-one/SKILL.md": "p0",
                "pkg/skills/rule-one/SKILL.md": "r0",
                "pkg/skills/forked/SKILL.md": "f0",
                "pkg/skills/old-extra/SKILL.md": "o0",
            },
        )
        pin = commit(upstream, "pin", {"pkg/skills/alpha/SKILL.md": "a1"})
        run(upstream, "tag", "v1.0.0")
        cls.alpha = commit(upstream, "alpha change", {"pkg/skills/alpha/SKILL.md": "a2"})
        cls.last_doomed = commit(upstream, "doomed tweak", {"pkg/skills/doomed/SKILL.md": "d1"})
        cls.delete = commit(upstream, "drop doomed", {"pkg/skills/doomed": None})
        cls.principle = commit(
            upstream, "principle change", {"pkg/skills/principle-one/SKILL.md": "p1"}
        )
        commit(upstream, "derived change", {"pkg/skills/forked/SKILL.md": "f1"})
        cls.mixed = commit(
            upstream,
            "new skills and readme",
            {
                "pkg/skills/fresh/SKILL.md": "n0",
                "pkg/skills/fresh/references/GUIDE.md": "g0",
                "pkg/skills/declined-one/SKILL.md": "x0",
                "README.md": "r0",
                "pkg/skills/alpha/references/NOTES.md": "an0",
            },
        )

        root = base / "fork"
        (root / "plugins" / "demo").mkdir(parents=True)
        (root / "plugins" / "demo" / "NOTICE.md").write_text(NOTICE, encoding="utf-8")
        record: dict[str, Any] = {
            "upstreams": [
                {
                    "name": "example",
                    "repository": upstream.as_posix(),
                    "fork_point": {"sha": "a" * 40, "version": "v1"},
                    "pin": {
                        "sha": pin,
                        "version": "v2",
                        "committed": "2026-10-01",
                        "reviewed": "2026-10-02",
                    },
                    "log": [
                        {
                            "date": "2026-10-02",
                            "from": "a" * 40,
                            "to": pin,
                            "pr": "https://example.com/pull/1",
                            "outcomes": {
                                "plugins/demo/skills/alpha/": "diverged",
                                "plugins/demo/skills/quiet/": "ported",
                            },
                            "candidates": [{"name": "declined-one", "decision": "declined"}],
                        }
                    ],
                }
            ]
        }
        (root / "upstreams.json").write_text(json.dumps(record), encoding="utf-8")
        cls.report = analyze_upstream.analyze(root, "example", base / "clone")

    def tracked(self, path: str) -> analyze_upstream.TrackedPath:
        return next(t for t in self.report.tracked if t.path == f"plugins/demo/{path}")

    def candidate(self, name: str) -> analyze_upstream.Candidate:
        return next(c for c in self.report.candidates if c.name == name)

    def test_only_commits_after_the_pin_count(self) -> None:
        self.assertEqual(self.report.commit_count, 6)
        self.assertEqual([c.sha for c in self.tracked("skills/alpha/").commits][-1], self.alpha)

    def test_commits_are_grouped_per_tracked_path(self) -> None:
        alpha = self.tracked("skills/alpha/")
        self.assertEqual([c.sha for c in alpha.commits], [self.mixed, self.alpha])
        self.assertEqual(
            alpha.commits[0].changes,
            [analyze_upstream.Change("A", "pkg/skills/alpha/references/NOTES.md")],
        )
        self.assertEqual(self.tracked("skills/quiet/").commits, [])

    def test_glob_row_matches_every_principle(self) -> None:
        principles = self.tracked("skills/principles/principle-*/")
        self.assertEqual([c.sha for c in principles.commits], [self.principle])
        self.assertIsNone(principles.deleted_from)

    def test_glob_row_without_changes_is_present_and_unchanged(self) -> None:
        rules = self.tracked("skills/rules/rule-*/")
        self.assertEqual(rules.commits, [])
        self.assertIsNone(rules.deleted_from)

    def test_derived_rows_are_not_read(self) -> None:
        self.assertNotIn("plugins/demo/skills/forked/", [t.path for t in self.report.tracked])
        self.assertNotIn("forked", [c.name for c in self.report.candidates])

    def test_upstream_deletion_names_the_last_commit_that_carried_it(self) -> None:
        doomed = self.tracked("skills/doomed/")
        self.assertEqual(doomed.deleted_from, self.last_doomed)
        self.assertIsNone(self.tracked("skills/alpha/").deleted_from)

    def test_last_outcome_is_carried_for_the_demotion_rule(self) -> None:
        self.assertEqual(self.tracked("skills/alpha/").last_outcome, "diverged")
        self.assertIsNone(self.tracked("skills/doomed/").last_outcome)

    def test_untracked_changes_are_candidates_grouped_by_skill(self) -> None:
        names = [c.name for c in self.report.candidates]
        self.assertEqual(names, ["declined-one", "fresh", analyze_upstream.OUTSIDE])
        fresh = self.candidate("fresh")
        self.assertEqual(fresh.directory, "pkg/skills/fresh/")
        self.assertEqual(
            [ch.path for ch in fresh.commits[0].changes],
            ["pkg/skills/fresh/SKILL.md", "pkg/skills/fresh/references/GUIDE.md"],
        )
        outside = self.candidate(analyze_upstream.OUTSIDE)
        self.assertEqual([ch.path for ch in outside.commits[0].changes], ["README.md"])

    def test_history_before_the_pin_is_not_a_candidate(self) -> None:
        self.assertNotIn("old-extra", [c.name for c in self.report.candidates])

    def test_previously_declined_candidates_are_marked(self) -> None:
        self.assertEqual(self.candidate("declined-one").prior, "declined")
        self.assertIsNone(self.candidate("fresh").prior)

    def test_new_pin_counts_commits_past_the_last_tag(self) -> None:
        self.assertEqual(self.report.head_version, "v1.0.0+6")

    def test_report_renders_the_triage_sections(self) -> None:
        text = analyze_upstream.render(self.report)
        self.assertIn("another `diverged` demotes it", text)
        self.assertIn(f"forked from `{self.last_doomed[:7]}`", text)
        self.assertIn(
            "### declined-one (`pkg/skills/declined-one/`), previously **declined**", text
        )
        self.assertIn("- `plugins/demo/skills/quiet/`", text)


if __name__ == "__main__":
    unittest.main()
