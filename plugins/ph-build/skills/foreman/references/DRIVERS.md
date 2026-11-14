# Foreman drivers

A driver is the thin, harness-specific part of the Foreman. It runs on the
harness's own scheduler. It starts the Foreman on an interval and starts one
Worker for each hand-off file the Foreman writes. It holds no slot logic and no
Claim state. Those live on the tracker, and the Foreman reads them there.

## Contract

A driver must do three things.

### 1. Start the Foreman on an interval, behind a lock

- Start the Foreman when its interval has passed and no fresh lock is held.
- Write the lock before you send the command, with a fresh random token as
  its content. If the send fails, delete the lock again.
- A lock older than its staleness limit does not block, so a crashed Foreman
  cannot wedge the schedule. Set the limit longer than the interval, or the
  lock never blocks anything and a slow run overlaps the next one.
- Make the first message of a new session the command, followed by the inputs
  as one JSON object:

  ```text
  /ph-build:foreman {"repos": ["/abs/repo-a"], "max_workers": 2, "orphan_minutes": 30, "reaper_minutes": 360, "handoff_dir": "/abs/handoff", "lock": "/abs/foreman.lock", "lock_token": "9f3c1a2b"}
  ```

  The keys are defined in the skill's Inputs table. `orphan_minutes` and
  `reaper_minutes` are parameters so you can shorten them for testing and tune
  them per setup. Pass `lock` and `lock_token` so the Foreman can release the
  lock when it finishes. It deletes the lock only while the token still
  matches, so a run that finishes late never releases a later run's lock.

The Foreman is human-only. A driver reaches it by typing the command, which
counts as explicit invocation. Never describe the task in prose and hope a model
picks the skill. The skill's guard refuses that path.

### 2. Start one top-level Worker per hand-off file

For each `<KEY>.json` in the hand-off directory:

- Start a **top-level** session. Never start a subagent. A Worker runs its own
  `dispatch`, which spawns subagents (code-review, architect, swarm). Nesting
  is not reliable across harnesses, so a Worker started as a subagent could not
  do that.
- Point the session at the file's `repo`, then pass the file's `key` to
  `ph-build:dispatch`. The ticket key alone is enough: dispatch runs the
  Implement a ticket adapter, which owns everything the Worker writes back to
  the tracker.
- Delete the file only after the session has received its prompt. When the
  send fails, leave the file so the next tick retries it.
- Never open a second session for a ticket whose send failed, even when the
  Foreman rewrites the file to requeue it. The Crew driver remembers the opened
  session by ticket key until a send succeeds.

### 3. Treat the hand-off directory as disposable

The hand-off directory is the only local Claim state. If you lose it, nothing
needs repair: the next Foreman run requeues any orphaned Claim. A driver may
keep its own scheduling state, such as the lock, the last start time, and the
sessions it opened. It must never keep a record of which tickets are claimed or
how many Worker slots are free. [ADR-0005](../../../../../docs/adr/0005-the-tracker-holds-the-claim.md)
explains why.

## Kiro Crew

`scripts/crew_driver.py` is the Kiro Crew driver. It is a Crew script cron, so
a quiet tick costs no model turns. It opens the Foreman and every Worker as
dashboard sessions in `trust` mode, inside one session folder.

Install it by copying the script into Crew's `crons/` directory and registering
it as a script cron. It reads its configuration from
`~/.kiro/crew/workspace/ph-foreman/config.json`:

```json
{
  "repos": ["D:\\work\\repo-a"],
  "max_workers": 2,
  "orphan_minutes": 30,
  "reaper_minutes": 360,
  "foreman_every_secs": 3600,
  "lock_stale_secs": 7200,
  "handoff_dir": "",
  "session_folder": "ph-foreman"
}
```

An empty `handoff_dir` defaults to `handoff/` beside the config file. The lock,
the time of the last Foreman start, and the open Worker sessions
(`slots.json`) are kept beside it too.

Known risks on Crew:

- `trust` mode turns off Crew's approval layer for Workers. The only gate left
  is dispatch's Autonomy rules, which pause before irreversible writes.
- Crew Bot sessions read `agent.member_acp_backend`, not `agent.acp_backend`.

The tests beside the script use a fake Crew `ctx`. The first real tick is what
proves the fake matches Crew's actual API.

## Other harnesses

None ship yet. A driver for Claude Code's `/loop` or `schedule`, or for any
other harness, follows the contract above. In practice that means a scheduler
hook, a way to open a top-level session with a first message, and a file
listing.
