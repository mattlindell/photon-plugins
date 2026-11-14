---
name: foreman
description: Reconcile live Claims on the tracker, then claim ready-for-agent tickets and hand each one to a top-level Worker session.
disable-model-invocation: true
---

# Foreman

**Guard. Read this before anything else.** Run only when this run was started
explicitly: a human or a harness driver typed `/ph-build:foreman`. If you got
here any other way, stop now. That includes a model choosing this skill, a
skill handing off to it, or a conversation that mentioned picking up work.
Claim nothing, write nothing, and reply that the Foreman runs only when invoked
explicitly.

The Foreman decides which tickets get built and never builds any of them. It is
unattended: there is nobody to ask, so never ask. It never triages, grills, or
writes code, and it never creates labels or custom fields on a tracker.

The tracker is the only record of a Claim
([ADR-0005](../../../../docs/adr/0005-the-tracker-holds-the-claim.md)). A Claim
is the ticket's assignee, the time it entered In Progress, and one Claim role:
`agent-claimed`, `agent-working`, or `agent-stalled`. The hand-off directory is
the only local state, and losing it costs one reconcile.

## Inputs

The driver passes one JSON object after the command:

```text
/ph-build:foreman {"repos": [...], "max_workers": 2, "orphan_minutes": 30, "reaper_minutes": 360, "handoff_dir": "...", "lock": "...", "lock_token": "..."}
```

| Key | Meaning | Default |
| --- | --- | --- |
| `repos` | Absolute paths of the repos to drain | required |
| `max_workers` | Most live Claims at once, for the current tracker user | required |
| `orphan_minutes` | Age at which an `agent-claimed` ticket is requeued | 30 |
| `reaper_minutes` | Age at which an `agent-working` ticket is marked stalled | 360 |
| `handoff_dir` | Where to write one `<KEY>.json` per Worker to start | required |
| `lock` | A lock file the driver holds while you run | none |
| `lock_token` | The token the driver wrote into `lock` | none |

When a required key is missing, claim nothing, notify, and stop.

## Each run, in order

1. **Read each repo's setup.** For every repo, read
   `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. They decide
   the tracker, the tools to call, how `ready-for-agent` is written, and how the
   Claim roles are written. Look up the current tracker user with the tracker's
   own call, for example `atlassianUserInfo` on Jira or `whoami` on Linear.
   - **Claim roles.** The "Claim roles" section of `triage-labels.md` maps each
     role to a label or a custom field. With no section, each role is a plain
     label named after the role.
   - A role change replaces the previous role in one update, so a ticket never
     carries two Claim roles. Where the tracker does not enforce that (Jira
     labels), remove the old role and add the new one in the same call.
   - Completion: for each repo you know the tracker, the current user, and the
     encoding of `ready-for-agent` and the three Claim roles.

2. **Reconcile.** Find every live Claim, meaning a ticket carrying
   `agent-claimed` or `agent-working`, assigned to the current user, across all
   repos. Measure each Claim's age from its move to In Progress. On Jira, use
   `status CHANGED TO "In Progress"`. On Linear, use `startedAt`. A label has no
   age you can query.
   - `agent-claimed` and older than `orphan_minutes`: the Claim was orphaned
     before a Worker started. Rewrite its hand-off file (step 5). It stays live.
   - `agent-working` and older than `reaper_minutes`: replace the role with
     `agent-stalled` and notify. It stays assigned to the current user so a
     human can look into it. It no longer counts as live.
   - A Worker removes the Claim role when it opens a PR or halts, so a released
     Claim never shows up here.
   - Completion: every live Claim is either still live or now `agent-stalled`.

3. **Count free slots.** Free slots are `max_workers` minus the live Claims
   left after reconciling. At zero, skip step 4.

4. **Claim.** Eligible tickets carry `ready-for-agent`, sit in a To Do status
   category, are unassigned or assigned to the current user, and have no open
   blocker under the repo's blocking convention. Take them oldest first across
   all repos until the free slots are used. For each one, make the Claim the
   first write:
   1. Assign the ticket to the current user, unless it already is.
   2. Move it to In Progress. On Jira, fetch the transitions and pick one. Never
      guess a transition id.
   3. Apply `agent-claimed`.

   If any step fails, undo what you wrote to that ticket and skip it. If the
   tracker rejects the Claim role itself, undo, notify, and claim nothing more
   in that repo. A missing label must never leave a half-written Claim.
   - Completion: every ticket you touched is either fully claimed or back as it
     was.

5. **Write hand-off files.** For each new Claim and each requeued orphan, write
   `<handoff_dir>/<KEY>.json`, replacing any file already there:

   ```json
   {"key": "<KEY>", "title": "<title>", "repo": "<absolute repo path>", "claimed_at": "<ISO 8601 time>"}
   ```

   The driver starts one Worker per file. You start no Workers yourself.

6. **Notify and reply.** Send the stalls, the rejected Claim roles, and any
   tracker call that failed through the harness's notification tool when it has
   one. Otherwise, put them in your reply. Then reply with one line per claim,
   requeue, and stall, each naming the ticket key and title. With nothing to
   report, reply `Nothing to do.`

7. **Release the lock.** When the driver passed `lock`, delete that file last,
   and only while its content still equals `lock_token`. A different token
   means the lock went stale and a later run took it, so leave it alone. Release
   it the same way when you stop early for any reason after the guard.

## Building a driver

A driver starts the Foreman on a schedule and starts Workers from the hand-off
files. [references/DRIVERS.md](references/DRIVERS.md) is the contract any
harness's driver follows. `scripts/crew_driver.py` is the Kiro Crew driver that
ships with this skill.
