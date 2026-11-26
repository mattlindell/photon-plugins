from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
_spec = importlib.util.spec_from_file_location(
    "lint_upstreams", Path(__file__).with_name("lint-upstreams.py")
)
assert _spec and _spec.loader
lint_upstreams = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint_upstreams)

PIN = "b" * 40
FORK = "a" * 40
REPO = "https://github.com/example/skills"

RECORD: dict[str, Any] = {
    "upstreams": [
        {
            "name": "example",
            "repository": REPO,
            "fork_point": {"sha": FORK, "version": "v1.0.0"},
            "pin": {
                "sha": PIN,
                "version": "v1.1.0",
                "committed": "2026-10-01",
                "reviewed": "2026-10-02",
            },
            "log": [
                {
                    "date": "2026-10-02",
                    "from": FORK,
                    "to": PIN,
                    "pr": "https://github.com/example/fork/pull/1",
                    "outcomes": {
                        "plugins/demo/skills/alpha/": "ported",
                        "plugins/demo/skills/beta/": "diverged",
                    },
                    "candidates": [{"name": "gamma", "decision": "declined"}],
                }
            ],
        }
    ]
}

NOTICE = """# NOTICE

Forked from example at `aaaaaaa` (v1.0.0). See [UPSTREAMS.md](../../UPSTREAMS.md).

### example

| Here | Upstream | State |
| --- | --- | --- |
| `skills/alpha/` | `skills/alpha/` | tracked |
| `skills/beta/` | `skills/beta/` | **derived**, forked from `aaaaaaa` |

| Not | Lineage |
| --- | --- |
| `skills/whatever/` | free text with a stray state |
"""

ROW = (
    f"| [example]({REPO}) | [`bbbbbbb`]({REPO}/commit/{PIN}) "
    "| v1.1.0 | 2026-10-01 | 2026-10-02 | `aaaaaaa` (v1.0.0) |"
)

BLOCK = f"""{lint_upstreams.BEGIN}
| Upstream | Pin | Version | Committed | Reviewed | Forked from |
| --- | --- | --- | --- | --- | --- |
{ROW}
{lint_upstreams.END}"""

UPSTREAMS = f"# Upstreams\n\nIntro.\n\n{BLOCK}\n\nOutro.\n"


class LintUpstreams(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        for skill in ("alpha", "beta"):
            (self.root / "plugins" / "demo" / "skills" / skill).mkdir(parents=True)
        self.record = copy.deepcopy(RECORD)
        self.write_record()
        self.write("plugins/demo/NOTICE.md", NOTICE)
        self.write("UPSTREAMS.md", UPSTREAMS)

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text(text, encoding="utf-8", newline="\n")

    def read(self, rel: str) -> str:
        return (self.root / rel).read_text(encoding="utf-8")

    def write_record(self) -> None:
        self.write("upstreams.json", json.dumps(self.record, indent=2))

    @property
    def upstream(self) -> dict[str, Any]:
        return self.record["upstreams"][0]

    def run_lint(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = lint_upstreams.main(["--root", str(self.root), *args])
        return code, out.getvalue()

    def assert_fails(self, rule: str, fragment: str) -> None:
        code, out = self.run_lint()
        self.assertEqual(code, 1, out)
        self.assertIn(f"[{rule}]", out)
        self.assertIn(fragment, out)

    def test_clean_tree_passes(self) -> None:
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_rule1_full_sha_in_notice_fails(self) -> None:
        self.write("plugins/demo/NOTICE.md", NOTICE.replace("`aaaaaaa` (v1.0.0)", f"`{FORK}`"))
        self.assert_fails("pin-restated", "NOTICE.md:3")

    def test_rule1_reviewed_through_in_notice_fails(self) -> None:
        restated = NOTICE + "\nTracked skills are Reviewed through the pin.\n"
        self.write("plugins/demo/NOTICE.md", restated)
        self.assert_fails("pin-restated", '"reviewed through"')

    def test_rule2_malformed_state_fails(self) -> None:
        self.write(
            "plugins/demo/NOTICE.md",
            NOTICE.replace("| tracked |", "| tracked, reviewed via `bbbbbbb` |"),
        )
        self.assert_fails("lineage-state", "NOTICE.md:9")

    def test_rule3_unknown_upstream_fails(self) -> None:
        self.write("plugins/demo/NOTICE.md", NOTICE.replace("### example", "### elsewhere"))
        self.assert_fails("unknown-upstream", "'elsewhere'")

    def test_rule4_log_not_ending_at_pin_fails(self) -> None:
        self.upstream["pin"]["sha"] = "c" * 40
        self.write_record()
        self.run_lint("--apply")  # keep rule 5 quiet so only rule 4 speaks
        self.assert_fails("log-pin", "ends at bbbbbbb, but the Pin is ccccccc")

    def test_rule5_stale_block_fails(self) -> None:
        self.write("UPSTREAMS.md", UPSTREAMS.replace("v1.1.0", "v1.0.9"))
        self.assert_fails("stale-block", "run lint-upstreams.py --apply")

    def test_rule5_missing_markers_fail(self) -> None:
        self.write("UPSTREAMS.md", "# Upstreams\n")
        self.assert_fails("stale-block", "markers not found")

    def test_rule6_tracked_after_two_diverged_fails(self) -> None:
        second = copy.deepcopy(self.upstream["log"][0])
        second["from"] = PIN
        second["to"] = PIN
        second["outcomes"] = {"plugins/demo/skills/alpha/": "diverged"}
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/alpha/"] = "diverged"
        self.upstream["log"].append(second)
        self.write_record()
        self.assert_fails("demotion", "plugins/demo/skills/alpha/ is still tracked")

    def test_rule4_broken_log_chain_fails(self) -> None:
        second = copy.deepcopy(self.upstream["log"][0])
        second["from"] = "c" * 40
        self.upstream["log"].append(second)
        self.write_record()
        self.assert_fails("log-pin", "log[1] starts at ccccccc, but log[0] ended at bbbbbbb")

    def test_rule6_newest_entry_must_cover_every_tracked_row(self) -> None:
        del self.upstream["log"][0]["outcomes"]["plugins/demo/skills/alpha/"]
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/*/"] = "ported"
        self.write_record()
        self.assert_fails("demotion", "no outcome for tracked plugins/demo/skills/alpha/")

    def test_rule6_skipped_review_cannot_hide_a_tracked_skill(self) -> None:
        gap = copy.deepcopy(self.upstream["log"][0])
        gap["from"] = PIN
        gap["outcomes"] = {"plugins/demo/skills/beta/": "no-change"}
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/alpha/"] = "diverged"
        self.upstream["log"].append(gap)
        self.write_record()
        self.assert_fails("demotion", "no outcome for tracked plugins/demo/skills/alpha/")

    def test_rule6_one_diverged_passes(self) -> None:
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/alpha/"] = "diverged"
        self.write_record()
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_rule7_missing_outcome_path_fails(self) -> None:
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/renamed/"] = "ported"
        self.write_record()
        self.assert_fails("missing-path", "plugins/demo/skills/renamed/ does not exist")

    def test_rule7_glob_path_resolves(self) -> None:
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/*/"] = "ported"
        self.write_record()
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_unrecorded_outside_backfill_is_a_shape_error(self) -> None:
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/alpha/"] = "unrecorded"
        self.write_record()
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("unrecorded is allowed only in a backfilled entry", out)
        self.upstream["log"][0]["backfilled"] = True
        self.write_record()
        self.assertEqual(self.run_lint()[0], 0)

    def test_owed_needs_a_ticket(self) -> None:
        self.upstream["log"][0]["outcomes"]["plugins/demo/skills/alpha/"] = "owed"
        self.write_record()
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("owed needs a ticket", out)

    def test_apply_regenerates_a_stale_block_and_is_idempotent(self) -> None:
        stale = UPSTREAMS.replace("v1.1.0", "v1.0.9").replace("2026-10-01", "2026-09-30")
        self.write("UPSTREAMS.md", stale)
        code, out = self.run_lint("--apply")
        self.assertEqual(code, 0, out)
        self.assertEqual(self.read("UPSTREAMS.md"), UPSTREAMS)
        code, out = self.run_lint("--apply")
        self.assertEqual(code, 0, out)
        self.assertNotIn("Regenerated", out)
        self.assertEqual(self.read("UPSTREAMS.md"), UPSTREAMS)


if __name__ == "__main__":
    _ = unittest.main()
