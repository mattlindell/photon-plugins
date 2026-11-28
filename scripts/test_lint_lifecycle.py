from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
_spec = importlib.util.spec_from_file_location(
    "lint_lifecycle", Path(__file__).with_name("lint-lifecycle.py")
)
assert _spec and _spec.loader
lint_lifecycle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint_lifecycle)

TRACKER = "docs/agents/issue-tracker.md"
SEED = "plugins/ph-plan/skills/setup-ph-plan/references/issue-tracker-demo.md"

TABLE = """| Event | Actor | Action |
| --- | --- | --- |
| `start` | agent | → In Progress |
| `review requested` | automation | → In Review |
| `PR merged` | automation | → Done |
| `halt` | agent | → Todo (unassign) |"""

CLEAN = f"""# Issue tracker: Demo

## Work item lifecycle

{TABLE}

Notes on anything the table can't express.

## Conventions

| Event | Actor | Action |
| --- | --- | --- |
| this table | is | outside the section |
"""

NO_SECTION = """# Issue tracker: Demo

## Conventions

Nothing about the lifecycle.
"""


class LintLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.write(TRACKER, CLEAN)

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text(text, encoding="utf-8", newline="\n")

    def run_lint(self) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = lint_lifecycle.main(["--root", str(self.root)])
        return code, out.getvalue()

    def assert_fails(self, rule: str, fragment: str) -> None:
        code, out = self.run_lint()
        self.assertEqual(code, 1, out)
        self.assertIn(f"[{rule}]", out)
        self.assertIn(fragment, out)

    def test_clean_tracker_passes(self) -> None:
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_clean_seed_passes(self) -> None:
        self.write(SEED, CLEAN)
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_seed_without_section_passes(self) -> None:
        self.write(SEED, NO_SECTION)
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_tracker_without_section_fails(self) -> None:
        self.write(TRACKER, NO_SECTION)
        self.assert_fails("missing-section", TRACKER)

    def test_missing_tracker_file_fails(self) -> None:
        (self.root / TRACKER).unlink()
        self.assert_fails("missing-file", TRACKER)

    def test_section_without_table_fails(self) -> None:
        self.write(TRACKER, "## Work item lifecycle\n\nProse only.\n\n## Next\n")
        self.assert_fails("missing-table", TRACKER)

    def test_table_in_fence_does_not_count(self) -> None:
        self.write(TRACKER, f"## Work item lifecycle\n\n```markdown\n{TABLE}\n```\n")
        self.assert_fails("missing-table", TRACKER)

    def test_wrong_columns_fail(self) -> None:
        self.write(TRACKER, CLEAN.replace("| Event | Actor | Action |", "| Event | Who | Do |", 1))
        self.assert_fails("columns", "Event | Who | Do")

    def test_missing_event_fails(self) -> None:
        self.write(TRACKER, CLEAN.replace("| `PR merged` | automation | → Done |\n", ""))
        self.assert_fails("missing-event", "`PR merged`")

    def test_wrong_event_fails(self) -> None:
        self.write(TRACKER, CLEAN.replace("`review requested`", "`PR opened`"))
        code, out = self.run_lint()
        self.assertEqual(code, 1, out)
        self.assertIn("[unknown-event] `PR opened`", out)
        self.assertIn("[missing-event] no `review requested` row", out)

    def test_duplicate_event_fails(self) -> None:
        self.write(TRACKER, CLEAN.replace("`halt`", "`start`"))
        self.assert_fails("duplicate-event", "`start` has 2 rows")

    def test_unknown_actor_fails(self) -> None:
        self.write(TRACKER, CLEAN.replace("| `start` | agent |", "| `start` | robot |"))
        self.assert_fails("unknown-actor", f"{TRACKER}:7")

    def test_bad_seed_with_section_fails(self) -> None:
        self.write(SEED, CLEAN.replace("| `halt` | agent |", "| `halt` | human |"))
        self.assert_fails("unknown-actor", SEED)


if __name__ == "__main__":
    _ = unittest.main()
