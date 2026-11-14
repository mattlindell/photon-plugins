"""Kiro Crew driver for ``ph-build:foreman``. Implements ``references/DRIVERS.md``.

Runs as a Crew script cron, so a quiet tick costs no tokens. Each tick starts
one top-level Worker session per hand-off file, then starts the foreman when
its interval has passed and no fresh lock is held. It keeps no slot logic:
the foreman counts slots from the tracker.
"""

from __future__ import annotations

import json
import secrets
import time
from pathlib import Path
from typing import Any

from kiro_crew.cron_script import Report, Skip  # pyright: ignore[reportMissingImports]

CONFIG = Path.home() / ".kiro" / "crew" / "workspace" / "ph-foreman" / "config.json"

WORKER_PROMPT = """You are an unattended ph-build Worker for {key}: {title}.

1. Call `set_project` with `{repo}`.
2. Invoke the `ph-build:dispatch` skill with `{key}` as the work.
"""


def run(ctx: Any) -> None:
    if not CONFIG.exists():
        raise Skip()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if not cfg.get("repos"):
        raise Skip()
    handoff = Path(cfg.get("handoff_dir") or CONFIG.parent / "handoff")
    handoff.mkdir(parents=True, exist_ok=True)
    try:
        folder = _folder_id(ctx, cfg.get("session_folder", "ph-foreman"))
    except RuntimeError:
        raise Skip() from None

    started = _start_workers(ctx, handoff, folder)
    _start_foreman(ctx, cfg, handoff, folder)
    if started:
        raise Report("ph-foreman started workers:\n" + "\n".join(started))
    raise Skip()


def _folder_id(ctx: Any, name: str) -> str:
    for folder in ctx.list_session_folders():
        if folder.get("name") == name and not folder.get("parent_id"):
            return folder["id"]
    return ctx.create_session_folder(name)["id"]


def _start_workers(ctx: Any, handoff: Path, folder: str) -> list[str]:
    """Send each hand-off to its own session.

    An opened session is remembered by ticket key until its send succeeds, so
    neither a retry nor the Foreman rewriting the file opens a second one.
    """
    slots_path = CONFIG.parent / "slots.json"
    slots: dict[str, str] = (
        json.loads(slots_path.read_text(encoding="utf-8")) if slots_path.exists() else {}
    )
    started: list[str] = []
    for path in sorted(handoff.glob("*.json")):
        try:
            ticket = json.loads(path.read_text(encoding="utf-8"))
            key, prompt = ticket["key"], WORKER_PROMPT.format(**ticket)
        except (ValueError, KeyError):
            continue
        try:
            if key not in slots:
                slots[key] = ctx.open_session(f"ph: {key}", folder_id=folder)
                slots_path.write_text(json.dumps(slots), encoding="utf-8")
            ctx.set_session_mode(slots[key], "trust")
            ctx.send_to_session(slots[key], prompt)
        except RuntimeError:
            continue
        path.unlink()
        del slots[key]
        slots_path.write_text(json.dumps(slots), encoding="utf-8")
        started.append(f"{key}: {ticket['title']}")
    return started


def _start_foreman(ctx: Any, cfg: dict[str, Any], handoff: Path, folder: str) -> None:
    """Start the Foreman when its interval has passed and no fresh lock is held.

    The lock carries a token. The Foreman deletes the lock when it finishes, but
    only while it still holds that token, so a late finisher never releases a
    lock that a later run took.
    """
    now = time.time()
    lock = CONFIG.parent / "foreman.lock"
    last = CONFIG.parent / "foreman.last"
    if lock.exists() and now - lock.stat().st_mtime < cfg.get("lock_stale_secs", 7200):
        return
    if last.exists():
        since_last = now - float(last.read_text(encoding="utf-8"))
        if since_last < cfg.get("foreman_every_secs", 3600):
            return

    token = secrets.token_hex(8)
    inputs = {
        "repos": cfg["repos"],
        "max_workers": cfg.get("max_workers", 2),
        "orphan_minutes": cfg.get("orphan_minutes", 30),
        "reaper_minutes": cfg.get("reaper_minutes", 360),
        "handoff_dir": str(handoff),
        "lock": str(lock),
        "lock_token": token,
    }
    lock.write_text(token, encoding="utf-8")
    try:
        slot = ctx.open_session("ph-foreman", folder_id=folder)
        ctx.set_session_mode(slot, "trust")
        ctx.send_to_session(slot, "/ph-build:foreman " + json.dumps(inputs))
    except RuntimeError:
        lock.unlink()
        return
    last.write_text(str(now), encoding="utf-8")
