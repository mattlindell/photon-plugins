---
name: "running-design-reviews"
description: "Run high-signal design reviews and critiques — plan the review around a real decision, facilitate feedback in Value/Ease/Delight order, and synthesize it into prioritized changes with owners."
disable-model-invocation: true
---

# Running Design Reviews

## A review that changes the work

Anchor every choice below to four ideas:

- **Every review has a decision.** "Get feedback" is not a review. Name what changes after it, and let the requested-feedback questions all serve that decision.
- **Value before Ease before Delight.** Confirm it solves the right problem, then remove friction, then polish. Don't argue pixels while the concept is unresolved.
- **Observation + impact, not preference.** Capture what breaks and why it matters — not "I'd do it differently." The Sponsor/DRI breaks ties by returning to goals and constraints; no design-by-committee.
- **Demo, don't deck; then write it down.** Anchor the review in a live artifact, and record the decisions and tradeoffs — an undocumented review doesn't change anything.

## When to use / not

Use to plan and run a design review, prep and facilitate a critique that's coming up, synthesize messy feedback into a change plan, or run an async review when you can't meet live.

Do **not** use for: a design with **no defined problem, user, or goal** yet — do problem definition first; **build-ready specs / acceptance criteria** — that's a spec-writing task; **evidence from real users** — that's usability testing, not expert critique; or **launch planning, comms, and rollout** — that's shipping.

## Pick the branch

| The user wants… | Branch |
|---|---|
| To plan and run a design review end-to-end | **A — Plan & run** |
| To prep and facilitate a critique that's coming up | **B — Prep & facilitate** |
| To turn a pile of comments into a prioritized change plan | **C — Synthesize feedback** |
| To review without meeting live | **D — Async review** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) — ask ≤5 at a time, then proceed on labeled assumptions; never request secrets or credentials.

## Branch A — Plan & run a design review

The spine. Turn an artifact and a decision into prioritized, owned changes.

1. **Lock the decision and scope.** Pick the review type (concept / flow / content / polish / ship-readiness), write "After this review we will decide ___," and mark what's in and out of scope. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** everyone can answer "what changes after this review?" and scope boundaries are explicit.
2. **Set the requested feedback.** Specify 1–3 feedback questions that map to the decision, and name what reviewers should *not* comment on yet (defer aesthetics until Value/Ease hold).
   **Done when:** each feedback question ties directly to the decision, with out-of-scope feedback named.
3. **Assign roles and prep the demo.** Name a Presenter, Facilitator, Note-taker, and a Sponsor/DRI who owns "why" and the core concept, and plan a live demo (happy path + top edge case) with a pre-read: problem → user → success criteria → constraints → options → risks → links. Brief template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** roles are assigned, decision rights are clear, and a reviewer could give useful feedback from the pre-read alone.
4. **Run it, then synthesize and decide.** Open with the big picture, then evaluate in order — Value, Ease, Delight — capturing feedback as observation + impact + suggestion. Deduplicate, resolve conflicts by returning to goals, prioritize the top 3 by user impact and risk, and record decisions, tradeoffs, owners, and a re-review gate. Pass [references/CHECKLISTS.md](references/CHECKLISTS.md) / [references/RUBRIC.md](references/RUBRIC.md) and close with **Risks / Open questions / Next steps**.
   **Done when:** the top issues each have an owned action, decisions and tradeoffs are written down, and the checklist passes.

Deliverable: a design review pack — brief/pre-read, agenda + facilitation script, prioritized feedback log, decision record, and a follow-up + next-review plan.

## Branch B — Prep & facilitate a critique

The workhorse. You have a crit on the calendar and need to walk in ready to run it — not design a program.

1. **Write the one-page brief.** Decision, requested feedback (1–3 questions), what's out of scope, and links. Brief and agenda templates: [references/TEMPLATES.md](references/TEMPLATES.md).
2. **Pick the agenda.** Timebox to 30/45/60 min: context → live demo → feedback capture → synthesis + decisions.
3. **Load the facilitation prompts.** Keep the room in Value → Ease → Delight order, make reviewers state observation + impact before solutions, and timebox solutioning so it doesn't drift into design-by-committee.

**Done when:** a one-page brief + timeboxed agenda exists, the feedback log table is ready to fill, and the Sponsor/DRI is named to break ties.

## Branch C — Synthesize messy feedback

You already have a pile of comments and need signal. Deduplicate, categorize each item as Value / Ease / Delight, assign severity, resolve conflicts by returning to the goal → user → constraint (not by vote-counting), and convert the top items into explicit changes with owners and due dates. Feedback-log and decision-record templates: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** the top 3 issues are clear, each has a proposed action and owner, and conflicting comments were reconciled against goals rather than averaged.

## Branch D — Async review

When you can't meet live: share the pre-read (and a short walkthrough video if useful), request feedback via 1–3 explicit questions, require it logged into the same Value/Ease/Delight table, then synthesize and circulate a decision record + change plan. Async variant notes: [references/WORKFLOW.md](references/WORKFLOW.md).

**Done when:** feedback is captured in the shared log against the requested questions, and a decision record + change plan is circulated.

## Examples

- *"We have a new onboarding flow in Figma — run a 45-minute review to choose Flow A vs. B before next sprint."* → **Branch A**: brief with the decision, timed agenda, feedback log by Value/Ease/Delight, decision record with owners, follow-up.
- *"Turn these 30 messy Figma comments into a prioritized list of what to change."* → **Branch C**: deduplicated log with severities, top-3 changes with owners, conflicts reconciled against goals.
- *"Can you give me general feedback on this Dribbble shot?"* (no user, goal, or decision) → out of scope: ask for the decision, target user, and success criteria first; without product context, decline the full pack.
