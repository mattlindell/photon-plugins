### Implement a ticket

**Not a playbook — an entry adapter.** It is the bookend to **Opening a PR**:
that one closes every run; this one opens the ones that arrive as a bare tracker
reference and nothing else. Run it before the playbook table, then follow the
playbook it picks to the end.

1. **Resolve the reference.** Fetch the ticket per *Read the rigor signal first*.
   A reference you have not fetched carries no rigor signal to read. Then make
   the `start` writes in [Tracker writeback](#events), before any other write.
2. **Ground yourself in the domain.** Read `CONTEXT.md` (or the layout named in
   `docs/agents/domain.md`) so your test names and interface vocabulary use the
   project's words, and read the ADRs covering the area you are about to touch.
   **A ticket that contradicts a live ADR is a Halt**: stop per
   [Halt or Stall](#halt-or-stall) rather than building on either side of the
   collision.
3. **Get onto a working branch.** Confirm you are not on the default branch. If
   you are, branch from it, naming the branch by the precedence in
   `docs/agents/issue-tracker.md`. A branch you inherited that already carries
   the ticket key stays as it is.
4. **Classify the work.** The `settled:` block sizes the rigor; the ticket's own
   shape picks the playbook — new or changed behavior is **Feature**, a
   reproducible defect is **Bug fix**, structure without behavior is
   **Refactoring**. Name the one you picked and why.
5. **Hand off.** Open the todolist with that playbook's steps and run it. It
   ends in **Opening a PR**, and the ticket key reaches the tracker through
   either the branch name or the `## Why` section — confirm one of the two
   carries it. Once the PR is open, make the `review requested` writes in
   [Tracker writeback](#events).

## Tracker writeback

Every unattended ticket run writes to the tracker the same way, whether a
Foreman claimed the ticket or someone ran `implement` by hand. Three layers sit
on a ticket, and each has its own source:

- **Ticket status** follows the `## Work item lifecycle` table in
  `docs/agents/issue-tracker.md`: one row per event, each with an actor and an
  action.
- **Agentic state** (`ready-for-agent`, `needs-triage`) is written as
  `docs/agents/triage-labels.md` records it.
- **Claim role** (`agent-claimed`, `agent-working`, `agent-stalled`) is written
  as the "Claim roles" section of `triage-labels.md` maps it. With no such
  section, each Claim role is a plain label named after the role.

A role change replaces the previous role in one update, so a ticket never
carries two Claim roles or two triage roles. Where the tracker does not enforce
that (Jira labels), remove the old role and add the new one in the same call.
When `triage-labels.md` is missing, make no role writes; every other write
still applies.

### Applying a lifecycle row

- **Act only on `agent` rows.** A row whose actor is `automation` belongs to
  the tracker, and a row whose actor is `none` belongs to nobody. Never perform
  or check either.
- **Move the status.** Use the transition id the action records, if any. If
  the tracker rejects it, or the action records none, fetch the available
  transitions and use the one whose target is the named status. On a tracker
  that sets status directly, such as Linear, set the named status. When the
  ticket already sits in that status, skip the move.
- **A status move never stops the run.** When no transition reaches the named
  status, or the move fails, notify and skip the move. A failed move is neither
  a Halt nor a Stall.
- **Leave the assignee alone** unless the action names an assignee change. The
  agent may be acting as the human the ticket is assigned to.
- **No lifecycle section.** When `issue-tracker.md` has no
  `## Work item lifecycle` section, make no status or assignee moves, with one
  exception: a Halt on a ticket that carried a Claim role at `start` moves it
  to To Do. The Foreman's fallback moved that ticket to In Progress, and it
  claims only from a To Do status, so without the move the ticket could never
  be claimed again. End the reply by suggesting `/ph-plan:setup-ph-plan` to
  record the table.

### Events

- **`start`.** The run's first writes, right after the fetch:
  1. If the ticket carries a Claim role, replace it with `agent-working`. A
     ticket with no Claim role was not claimed; add none.
  2. Apply the `start` row, claimed or not.
- **`review requested`.** When the PR opens, ready and never as a draft:
  1. Remove any Claim role, whichever one is set. A ticket reaped to
     `agent-stalled` while the run was still going counts too.
  2. Apply the `review requested` row.

  Post no comment: the ticket key in the branch name or the PR's `## Why` links
  the PR.
- **`PR merged`.** Happens after the run ends. The run writes nothing for it.

### Halt or Stall

A run that stops without a PR stops in one of two ways, and the cause decides
which. **If rerunning the same ticket, unchanged, in a fixed environment would
succeed, it is a Stall. Otherwise it is a Halt. When you cannot tell, halt.**

| Halt: the task is wrong | Stall: the process broke |
| --- | --- |
| A one-way door the `settled:` block leaves open | Lapsed auth: tracker, git host, or model provider |
| A collision with a live ADR | A missing tool, such as the repo's test runner binary or a CLI |
| A ticket too big for one session | A harness failure: crash, quota, or a dead subagent runtime |

**Halt** hands the ticket back to triage:

1. Remove any Claim role.
2. Replace `ready-for-agent` with `needs-triage`.
3. Apply the `halt` row. With no lifecycle section, move a claimed ticket to
   To Do instead, as [Applying a lifecycle row](#applying-a-lifecycle-row)
   says.
4. Post one comment that names the blocker.
5. Notify.

**Stall** leaves the ticket ready for a rerun once a human fixes the
environment:

1. Replace any Claim role with `agent-stalled`, or add `agent-stalled` when
   there is none.
2. Keep `ready-for-agent`, the Ticket status, and the assignee. Apply no
   lifecycle row.
3. Post one comment that names what broke and what fixes it.
4. Notify.

When the broken thing is the tracker itself, such as lapsed tracker auth, its
writes fail too. Put the comment's text in the notification instead.

Notify through the harness's notification tool when it has one. Otherwise, put
the blocker in your reply.

## Definition of done

These sit on top of the playbook's own exit conditions. Every item is
checkable; report the work complete only when all of them hold:

- Every acceptance criterion on the ticket maps to at least one test, and each
  of those tests was observed **red** before it went green.
- The full test suite passes on a final run.
- Typechecking and the repo's linter pass.
- The **code-review** skill has run, and neither axis returned
  `CHANGES REQUIRED`: every blocking finding is fixed. Non-blocking notes may
  stand as they are, with no fix and no justification required.
- The work is committed and the PR is open.

## Edge cases

- **The suite is already red at `HEAD`.** You cannot tell your red from ambient
  red. Capture the failing set before writing anything, treat only new failures
  as yours, and report the pre-existing set separately — it is not yours to fix
  unless the ticket says so.
- **The repo has no test runner.** Test-first is the whole method. Pick one that
  fits the stack, stand it up, and name the choice in the PR — a framework
  chosen in the open is a decision a reviewer can reverse. A runner the repo
  already uses whose binary is missing here is a Stall, not this case.
- **The ticket is underspecified.** Take the defensible reading, record it at the
  top of your reply, and build. Where the ambiguity reaches a one-way door
  instead, halt.
- **The ticket is bigger than one session.** Halt early rather than
  half-build it, and recommend `ph-plan:to-tickets` in the halt comment to
  split it along its blocking edges.

**Reply:** the ticket key and title, the playbook you routed to and why, then
that playbook's own reply. Name every tracker write you made or skipped. With no
lifecycle section, end with the `/ph-plan:setup-ph-plan` suggestion.
