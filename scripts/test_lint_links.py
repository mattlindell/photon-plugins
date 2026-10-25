from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "lint_links", Path(__file__).with_name("lint-links.py")
)
assert _spec and _spec.loader
lint_links = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint_links)


class BacktickPaths(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.plugin = Path(self._tmp.name) / "plugins" / "demo"
        self.skill = self.plugin / "skills" / "dispatch"
        for rel in (
            "skills/dispatch/SKILL.md",
            "skills/dispatch/playbooks/feature.md",
            "skills/dispatch/references/triage.md",
            "skills/dispatch/scripts/watch.sh",
            "agents/implement.md",
        ):
            path = self.plugin / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            _ = path.write_text("# x\n", encoding="utf-8")

    def lint(self, rel: str, body: str) -> list[tuple[int, str]]:
        path = self.plugin / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text(body, encoding="utf-8")
        return [(p.line, p.target) for p in lint_links.check(path)]

    def test_missing_file_under_anchor_directory_fails(self) -> None:
        for target in (
            "playbooks/gone.md",
            "references/gone.md",
            "scripts/gone.sh",
        ):
            with self.subTest(target=target):
                found = self.lint("skills/dispatch/SKILL.md", f"intro\n\nSee `{target}`.\n")
                self.assertEqual(found, [(3, target)])

    def test_existing_file_passes(self) -> None:
        body = "`playbooks/feature.md` and `scripts/watch.sh`\n"
        self.assertEqual(self.lint("skills/dispatch/SKILL.md", body), [])

    def test_skill_root_anchors_paths_from_nested_files(self) -> None:
        body = "`references/triage.md` and `references/gone.md`\n"
        found = self.lint("skills/dispatch/playbooks/bug.md", body)
        self.assertEqual(found, [(1, "references/gone.md")])

    def test_plugin_root_anchors_paths(self) -> None:
        body = "`agents/implement.md` and `agents/gone.md`\n"
        found = self.lint("skills/dispatch/SKILL.md", body)
        self.assertEqual(found, [(1, "agents/gone.md")])

    def test_parent_paths_resolve_only_from_the_file(self) -> None:
        sibling = self.plugin.parent / "other" / "README.md"
        sibling.parent.mkdir(parents=True)
        _ = sibling.write_text("# x\n", encoding="utf-8")
        body = "`../references/triage.md` and `../other/README.md`\n"
        found = self.lint("skills/dispatch/playbooks/bug.md", body)
        self.assertEqual(found, [(1, "../other/README.md")])

    def test_plugin_root_found_from_inside_the_plugin(self) -> None:
        path = self.skill / "SKILL.md"
        _ = path.write_text("`agents/gone.md`\n", encoding="utf-8")
        cwd = Path.cwd()
        os.chdir(self.plugin)
        self.addCleanup(os.chdir, cwd)
        found = lint_links.check(Path("skills/dispatch/SKILL.md"))
        self.assertEqual([p.target for p in found], ["agents/gone.md"])

    def test_consumer_owned_paths_are_skipped(self) -> None:
        body = "`.claude/hooks/x.sh` `public/entrypoints.json` `docs/adr/0001.md`\n"
        self.assertEqual(self.lint("skills/dispatch/SKILL.md", body), [])

    def test_fenced_paths_are_skipped(self) -> None:
        body = "```markdown\n`playbooks/gone.md`\n```\n"
        self.assertEqual(self.lint("skills/dispatch/SKILL.md", body), [])

    def test_non_path_strings_are_skipped(self) -> None:
        body = (
            "`~/playbooks/gone.md` `@playbooks/gone.md` `/playbooks/gone.md` "
            "`./playbooks/gone.md` `playbooks/*.md` `playbooks/<name>.md` "
            "`playbooks/gone.txt` `gone.md` `playbooks/gone two.md`\n"
        )
        self.assertEqual(self.lint("skills/dispatch/SKILL.md", body), [])


if __name__ == "__main__":
    _ = unittest.main()
