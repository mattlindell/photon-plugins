### Implement a ticket

**Not a playbook — an entry adapter.** It is the bookend to **Opening a PR**:
that one closes every run; this one opens the ones that arrive as a bare tracker
reference and nothing else. Run it before the playbook table, then follow the
playbook it picks to the end.

1. **Resolve the reference.** Fetch the ticket per *Read the rigor signal first*.
   A reference you have not fetched carries no rigor signal to read.
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
   carries it.

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
