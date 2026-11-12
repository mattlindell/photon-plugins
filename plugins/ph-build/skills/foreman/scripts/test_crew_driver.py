"""Tests for the Kiro Crew foreman driver, against a fake Crew ``ctx``.

The fake stands in for Crew's session API, which is the driver's boundary.
Crew itself is not installed in CI, so a stub ``kiro_crew.cron_script`` module
supplies the two control-flow exceptions the driver raises.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import types
import unittest
from pathlib import Path


class Skip(Exception):
    pass


class Report(Exception):
    pass


_stub = types.ModuleType("kiro_crew.cron_script")
_stub.Skip = Skip  # pyright: ignore[reportAttributeAccessIssue]
_stub.Report = Report  # pyright: ignore[reportAttributeAccessIssue]
sys.modules.setdefault("kiro_crew", types.ModuleType("kiro_crew"))
sys.modules["kiro_crew.cron_script"] = _stub

import crew_driver  # noqa: E402

FOREMAN = "/ph-build:foreman "


class FakeCtx:
    """Records what the driver asked Crew to do. Has no ``spawn_run``."""

    def __init__(self) -> None:
        self.folders: list[dict[str, str]] = []
        self.sessions: dict[str, dict[str, object]] = {}
        self.failing_sends = 0

    def list_session_folders(self) -> list[dict[str, str]]:
        return list(self.folders)

    def create_session_folder(self, name: str, *, parent_id: str = "") -> dict[str, str]:
        folder = {"id": f"folder-{len(self.folders)}", "name": name, "parent_id": parent_id}
        self.folders.append(folder)
        return folder

    def open_session(
        self, name: str = "", *, folder_id: str = "", agent: str = "", model: str = ""
    ) -> str:
        slot = f"slot-{len(self.sessions)}"
        self.sessions[slot] = {"name": name, "folder_id": folder_id, "mode": None, "messages": []}
        return slot

    def set_session_mode(self, slot: str, mode: str) -> dict[str, str]:
        self.sessions[slot]["mode"] = mode
        return {}

    def send_to_session(self, slot: str, message: str) -> dict[str, str]:
        if self.failing_sends:
            self.failing_sends -= 1
            raise RuntimeError("gateway unreachable")
        messages = self.sessions[slot]["messages"]
        assert isinstance(messages, list)
        messages.append(message)
        return {}

    def worker_sessions(self) -> list[dict[str, object]]:
        return [s for s in self.sessions.values() if not _is_foreman(s)]

    def foreman_messages(self) -> list[str]:
        return [m for s in self.sessions.values() for m in _messages(s) if m.startswith(FOREMAN)]


def _messages(session: dict[str, object]) -> list[str]:
    messages = session["messages"]
    assert isinstance(messages, list)
    return [str(m) for m in messages]


def _is_foreman(session: dict[str, object]) -> bool:
    return any(m.startswith(FOREMAN) for m in _messages(session))


class DriverTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.state = Path(tmp.name)
        self.handoff = self.state / "handoff"
        self.config = {
            "repos": ["/work/repo-a", "/work/repo-b"],
            "max_workers": 2,
            "orphan_minutes": 30,
            "reaper_minutes": 360,
            "foreman_every_secs": 3600,
            "lock_stale_secs": 7200,
            "handoff_dir": str(self.handoff),
        }
        self.write_config()
        original = crew_driver.CONFIG
        crew_driver.CONFIG = self.state / "config.json"
        self.addCleanup(setattr, crew_driver, "CONFIG", original)
        self.ctx = FakeCtx()

    def write_config(self) -> None:
        (self.state / "config.json").write_text(json.dumps(self.config), encoding="utf-8")

    def hand_off(self, key: str, repo: str = "/work/repo-a") -> Path:
        self.handoff.mkdir(parents=True, exist_ok=True)
        path = self.handoff / f"{key}.json"
        ticket = {
            "key": key,
            "title": f"Title {key}",
            "repo": repo,
            "claimed_at": "2026-11-12T10:00:00Z",
        }
        path.write_text(json.dumps(ticket), encoding="utf-8")
        return path

    def tick(self) -> type[Exception]:
        try:
            crew_driver.run(self.ctx)
        except (Skip, Report) as outcome:
            return type(outcome)
        self.fail("run() must end in Skip or Report")

    def mark_foreman_ran(self, seconds_ago: float) -> None:
        """Pretend a foreman started that long ago and has since finished."""
        (self.state / "foreman.last").write_text(str(time.time() - seconds_ago), encoding="utf-8")

    def test_each_handoff_opens_one_trusted_session_and_is_deleted(self) -> None:
        self.mark_foreman_ran(seconds_ago=0)
        a = self.hand_off("ABC-1", "/work/repo-a")
        b = self.hand_off("ABC-2", "/work/repo-b")

        self.assertIs(self.tick(), Report)

        workers = self.ctx.worker_sessions()
        self.assertEqual(len(workers), 2)
        for session, key, repo in zip(
            sorted(workers, key=lambda s: str(s["name"])),
            ("ABC-1", "ABC-2"),
            ("/work/repo-a", "/work/repo-b"),
            strict=True,
        ):
            self.assertEqual(session["mode"], "trust")
            [message] = _messages(session)
            self.assertIn(key, message)
            self.assertIn(repo, message)
            self.assertIn("ph-build:dispatch", message)
        self.assertFalse(a.exists())
        self.assertFalse(b.exists())

    def test_failed_send_keeps_the_file_and_the_retry_opens_no_second_session(self) -> None:
        self.mark_foreman_ran(seconds_ago=0)
        path = self.hand_off("ABC-3")
        self.ctx.failing_sends = 1

        self.tick()

        self.assertTrue(path.exists())
        self.assertEqual(len(self.ctx.worker_sessions()), 1)

        self.tick()

        [session] = self.ctx.worker_sessions()
        self.assertEqual(len(_messages(session)), 1)
        self.assertFalse(path.exists())

    def test_requeued_handoff_reuses_the_session_a_failed_send_opened(self) -> None:
        self.mark_foreman_ran(seconds_ago=0)
        self.hand_off("ABC-5")
        self.ctx.failing_sends = 1
        self.tick()

        path = self.hand_off("ABC-5")
        self.tick()

        [session] = self.ctx.worker_sessions()
        self.assertEqual(len(_messages(session)), 1)
        self.assertFalse(path.exists())

    def test_malformed_handoff_is_skipped_without_failing_the_tick(self) -> None:
        self.mark_foreman_ran(seconds_ago=0)
        self.handoff.mkdir(parents=True, exist_ok=True)
        broken = self.handoff / "ABC-6.json"
        broken.write_text('{"key": "ABC-6"', encoding="utf-8")
        good = self.hand_off("ABC-7")

        self.assertIs(self.tick(), Report)

        self.assertTrue(broken.exists())
        self.assertFalse(good.exists())
        self.assertEqual(len(self.ctx.worker_sessions()), 1)

    def test_quiet_tick_skips(self) -> None:
        self.mark_foreman_ran(seconds_ago=0)

        self.assertIs(self.tick(), Skip)
        self.assertEqual(self.ctx.sessions, {})

    def test_fresh_lock_blocks_the_foreman(self) -> None:
        (self.state / "foreman.lock").write_text("", encoding="utf-8")

        self.tick()

        self.assertEqual(self.ctx.foreman_messages(), [])

    def test_stale_lock_does_not_block_the_foreman(self) -> None:
        lock = self.state / "foreman.lock"
        lock.write_text("", encoding="utf-8")
        stale = time.time() - self.config["lock_stale_secs"] - 1
        os.utime(lock, (stale, stale))

        self.tick()

        self.assertEqual(len(self.ctx.foreman_messages()), 1)

    def test_foreman_starts_on_its_interval(self) -> None:
        self.tick()
        self.assertEqual(len(self.ctx.foreman_messages()), 1)

        (self.state / "foreman.lock").unlink()
        self.tick()
        self.assertEqual(len(self.ctx.foreman_messages()), 1)

        self.mark_foreman_ran(seconds_ago=self.config["foreman_every_secs"] + 1)
        self.tick()
        self.assertEqual(len(self.ctx.foreman_messages()), 2)

    def test_failed_foreman_send_releases_the_lock_and_retries_next_tick(self) -> None:
        self.ctx.failing_sends = 1
        self.tick()
        self.assertFalse((self.state / "foreman.lock").exists())

        self.tick()
        self.assertEqual(len(self.ctx.foreman_messages()), 1)

    def test_foreman_receives_its_inputs(self) -> None:
        self.tick()

        [message] = self.ctx.foreman_messages()
        inputs = json.loads(message.removeprefix(FOREMAN))
        self.assertEqual(inputs["repos"], ["/work/repo-a", "/work/repo-b"])
        self.assertEqual(inputs["max_workers"], 2)
        self.assertEqual(inputs["orphan_minutes"], 30)
        self.assertEqual(inputs["reaper_minutes"], 360)
        self.assertEqual(Path(inputs["handoff_dir"]), self.handoff)
        self.assertEqual(Path(inputs["lock"]), self.state / "foreman.lock")
        lock = Path(inputs["lock"]).read_text(encoding="utf-8")
        self.assertEqual(inputs["lock_token"], lock)

    def test_foreman_and_workers_share_one_session_folder(self) -> None:
        self.hand_off("ABC-4")

        self.tick()

        self.assertEqual(len(self.ctx.folders), 1)
        folder_ids = {s["folder_id"] for s in self.ctx.sessions.values()}
        self.assertEqual(folder_ids, {self.ctx.folders[0]["id"]})
        self.assertTrue(all(s["mode"] == "trust" for s in self.ctx.sessions.values()))


if __name__ == "__main__":
    unittest.main()
