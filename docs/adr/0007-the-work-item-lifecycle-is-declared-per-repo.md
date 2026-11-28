# The work item lifecycle is declared per repo

Each repo records its Work item lifecycle as a `## Work item lifecycle` table
in `docs/agents/issue-tracker.md`. The table says what happens to a ticket's
status, and who does it, at each event of an Unattended ticket run. Skills
read status names and transitions from that table and never hardcode them.
This amends [ADR-0005](0005-the-tracker-holds-the-claim.md): the Claim clock
starts when the ticket enters the `start` status, not In Progress.

Before this, an unattended ticket run moved its ticket's status only if the
Foreman had claimed it. A ticket handed straight to `implement` stayed in Todo
while an agent built it. The Foreman wrote "In Progress" and "To Do" as
literal strings, which breaks on any workflow with different names. The
playbook moved a ticket to "the review status `issue-tracker.md` names" when a
PR opened, but no template named one. On a Linear repo that move duplicated an
automation, and on a Jira repo it never happened. Nothing recorded which
transitions a tracker makes on its own, so an agent could not tell a step it
owns from a step it would race.

## Decisions

**Transitions are per-repo data, not skill text.** The table has three
columns: Event, Actor, and Action.

- There are exactly four events: `start`, `review requested`, `PR merged`,
  and `halt`. A fixed set means every repo's table reads the same way.
- The actor is `agent`, `automation`, or `none`.
- The action is a target status, an optional transition id (for example
  `→ Review (transition 31)`), and an optional assignee change. With no
  assignee change, the assignee is left as is.
- Prose after the table covers anything the table can't express.

`setup-ph-plan` drafts the table from the tracker's statuses and asks which
transitions the tracker already performs. `scripts/lint-lifecycle.py` checks
the table's shape in CI.

**Automation rows are hands-off.** A ticket run neither performs nor checks a
transition whose actor is `automation`. The tracker makes that move, and an
agent that also made it would race the tracker or duplicate it. The one
exception is the Foreman's claim, which moves the ticket to the `start` status
even when that row's actor is `automation`. A Claim needs its clock before any
branch or PR exists.

**A status move never stops a build.** The agent tries the recorded transition
id first. If the tracker rejects it, the agent fetches the available
transitions and uses the one whose target is the named status. If none
matches, it notifies and skips the move.

**Halt and Stall are separate outcomes.** A Halt means something is wrong with
the task: a one-way door the run was not told about, a collision with a live
ADR, or a ticket too big for one session. The ticket goes back to triage and
takes the `halt` row. A Stall means something is wrong with the agent process:
lapsed auth, a missing tool, or a harness failure. The ticket keeps
`ready-for-agent`, its status, and its assignee, and takes the `agent-stalled`
Claim role, so a human only needs to unblock it. The test is whether rerunning
the same ticket in a fixed environment would succeed. If it would, the stop is
a Stall. If the run can't tell, it halts. A Stall has no table row because it
changes no status.

**The Claim clock is the `start` status.** ADR-0005 measured Claim age from
the ticket entering In Progress. It now measures from the ticket entering the
`start` row's status: in Jira, `status CHANGED TO "<start status>"`, and in
Linear, `startedAt`.

## Consequences

- **A repo without the section falls back to In Progress and To Do.** The
  Foreman claims into In Progress. A ticket run makes no status moves except
  on a Halt of a claimed ticket, which it moves to To Do. Without that move,
  the halted ticket would stay in In Progress, where the Foreman never claims.
  An unclaimed run moves nothing. The run's reply suggests rerunning
  `/ph-plan:setup-ph-plan`.
- **The assignee belongs to the human by default.** An agent may be acting as
  the user, who assigns tickets to themselves so the tickets show up in their
  tools. Only a row that names an assignee change changes it. The Foreman
  still assigns on claim, because the assignee is part of a Claim.
- **A changed workflow costs a notification, not a dead run.** A stale
  transition id falls back to a lookup by status, and a missing status skips
  the move.
- **Whether an automation actually fired goes unchecked.** That belongs to the
  tracker, and checking it would bring back the race this ADR removes.
