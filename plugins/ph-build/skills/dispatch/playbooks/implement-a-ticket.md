### Implement a ticket

**Not a playbook — an entry adapter.** It is the bookend to **Opening a PR**:
that one closes every run; this one opens the ones that arrive as a bare tracker
reference and nothing else. Run it before the playbook table, then follow the
playbook it picks to the end.

1. **Resolve the reference.** Fetch the ticket per *Read the rigor signal first*.
   A reference you have not fetched carries no rigor signal to read. If the
   ticket carries a Claim role, take it to `agent-working` now, before any other
   write (see [Tracker writeback](#tracker-writeback)).
2. **Ground yourself in the domain.** Read `CONTEXT.md` (or the layout named in
   `docs/agents/domain.md`) so your test names and interface vocabulary use the
   project's words, and read the ADRs covering the area you are about to touch.
   **A ticket that contradicts a live ADR halts the run** — escalate per
   *Autonomy* rather than building on either side of the collision.
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
   carries it. Once the PR is open, write back per
   [Tracker writeback](#tracker-writeback).

## Tracker writeback

Every unattended ticket run reports to the tracker the same way, whether a
Foreman started it or someone ran `implement` by hand. Read the repo's
`docs/agents/triage-labels.md` for how roles are written. Its "Claim roles"
section maps `agent-claimed`, `agent-working`, and `agent-stalled`. With no such
section, each Claim role is a plain label named after the role.

A role change replaces the previous role in one update, so a ticket never
carries two Claim roles. Where the tracker does not enforce that (Jira labels),
remove the old role and add the new one in the same call. The same goes for the
triage roles.

- **Start.** Only when the ticket already carries a Claim role, replace it with
  `agent-working` as the run's first write. A ticket with no Claim role was not
  claimed, so leave Claim roles alone for the whole run.
- **PR opened.** Remove any Claim role, whichever one is set. A ticket reaped to
  `agent-stalled` while the run was still going counts too. Move the ticket to
  the review status `docs/agents/issue-tracker.md` names, or leave it In
  Progress when it names none. Post no comment: the ticket key in the branch
  name links the PR.
- **Halt.** A run that stops without a PR, for any reason, hands the ticket back
  to a human:
  1. Remove any Claim role.
  2. Apply `needs-triage` as `triage-labels.md` records it, replacing
     `ready-for-agent`.
  3. Unassign the ticket and move it to To Do.
  4. Post one comment that names the blocker.
  5. Notify through the harness's notification tool when it has one. Otherwise,
     put the blocker in your reply.

  When `triage-labels.md` is missing, skip steps 1 through 3, and still comment
  and notify.

## Definition of done

These sit on top of the playbook's own exit conditions. Every item is
checkable; report the work complete only when all of them hold:

- Every acceptance criterion on the ticket maps to at least one test, and each
  of those tests was observed **red** before it went green.
- The full test suite passes on a final run.
- Typechecking and the repo's linter pass.
- The **code-review** skill has run, and every finding is either fixed or listed
  with a reason it was left.
- The work is committed and the PR is open.

## Edge cases

- **The suite is already red at `HEAD`.** You cannot tell your red from ambient
  red. Capture the failing set before writing anything, treat only new failures
  as yours, and report the pre-existing set separately — it is not yours to fix
  unless the ticket says so.
- **The repo has no test runner.** Test-first is the whole method. Pick one that
  fits the stack, stand it up, and name the choice in the PR — a framework
  chosen in the open is a decision a reviewer can reverse.
- **The ticket is underspecified.** Take the defensible reading, record it at the
  top of your reply, and build. Where the ambiguity reaches a one-way door
  instead, escalate per *Autonomy*.
- **The ticket is bigger than one session.** Say so early. Recommend
  `ph-plan:to-tickets` to split it along its blocking edges instead of
  half-building it.

**Reply:** the ticket key and title, the playbook you routed to and why, then
that playbook's own reply.
