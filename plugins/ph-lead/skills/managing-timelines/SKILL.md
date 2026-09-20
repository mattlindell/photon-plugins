---
name: "managing-timelines"
description: "Manage a deadline, launch date, or delivery target: build the plan, rescue a slipping date, prep a status update, or set commit/forecast/target dates. Use when the user mentions a deadline, launch or ship date, milestone plan, delivery timeline, or schedule; wants to turn a date into phases and milestones; is asked 'when can you ship?' and needs to commit; has a milestone going red or a deadline slipping and needs options; needs a weekly status/RAG update or an exec review cadence; or is planning an AI/ML feature that demos fast but is slow to production."
---

# Managing Timelines

## Only commit what you control

Anchor every choice below to four ideas:

- **Commit only within control.** Use precise date language - commitment, forecast, target - and never present a forecast as a promise. Commit to the next phase output; forecast the rest.
- **Scope is the lever.** When a real date is at risk, trade scope before you add people or ask for heroics - "trade, don't add." A pre-agreed cut list beats a panicked last-minute cut.
- **No surprises - surface risk early.** RAG status earns its keep only when a red produces a concrete decision and ask. Stakeholders should hear about a slip while there is still time to act.
- **Demo is not production.** Especially for AI/ML, "fast demo, slow production" is the trap. Plan the outer loop - evaluation, safety, reliability, rollout - as first-class milestones.

## When to use / not

Use to turn a date into an executable plan, rescue a slipping deadline, prep a status update or review, define what you can actually commit to, or plan a demo-to-production path.

Do **not** use for: defining the problem or outcome (use `problem-definition`); choosing which initiatives matter most (use `prioritizing-roadmap`); cutting scope to fit an appetite or timebox as the primary goal (use `scoping-cutting`); or writing a decision-ready PRD or build-ready spec (use `writing-prds` / `writing-specs-designs`).

## Pick the branch

| The user wants… | Branch |
|---|---|
| To turn a deadline or launch into a full plan | **A — Build the plan** |
| Options for a deadline that is slipping right now | **B — Rescue a slip** |
| This week's status update or exec review | **C — Status + review** |
| To answer "when can you ship?" without a full plan | **D — Commitment model** |
| An AI/ML feature planned demo-to-production | **E — Demo to production** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) — ask ≤5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A — Build the plan

The full setup. Produce a **Timeline Management Pack**.

1. **Classify the date.** Fixed external / fixed internal / target / window; name the "why now" and the variable that can move (scope, resources, quality, or date).
   **Done when:** you can say "the date is <type> because <reason>; the lever we will trade is <x>."
2. **Set the commitment model.** Define what you commit to now (usually the next phase output), what you forecast, and what stays a target; attach confidence + top risks + next re-forecast date.
   **Done when:** every date is labeled commit, forecast, or target.
3. **Build the phase plan with gates.** Discovery → Solutioning → Build → Launch; each phase ends in an artifact and a go/no-go gate; commit only within control. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** every phase has a concrete output and a decision gate.
4. **Create the milestone tracker.** Deliverable-based milestones with owners, dependencies, dates, confidence, and RAG; write action-oriented RAG definitions. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** milestones are outcomes (not activities) and critical dependencies are explicit.
5. **Set governance.** A short weekly review agenda, escalation triggers, and a decision log; a red must yield a concrete ask.
   **Done when:** a red status produces a decision, not just a warning.
6. **Protect the date.** If it is real, treat it like P0: reduce WIP, defer nonessential work, and install change control ("trade, don't add") with a pre-ordered cut list and freeze points.
   **Done when:** new scope cannot enter without an explicit trade and the decision owner's approval.
7. **Assemble comms + finalize.** Weekly update template + escalation note; close with **Risks / Open questions / Next steps**. Pass [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md).
   **Done when:** a stakeholder can approve async and the team executes without re-litigating dates every week.

## Branch B — Rescue a slip

The workhorse. A milestone went yellow/red or the date is at risk right now. Produce a decision-ready escalation note, not a system.

1. **Name the gap.** Which committed date or milestone is at risk, by how much, and what triggered it.
   **Done when:** the slip is quantified against a specific commitment.
2. **Diagnose the cause.** Scope creep, under-estimation, a dependency or vendor block, capacity loss, or quality debt surfacing late - pick the real driver, not the symptom. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** the root cause is named, not just "we are behind."
3. **Lay out the four levers.** Cut scope / move date / add resources / lower quality (only if allowed), each with its cost and impact; use the pre-agreed cut list if one exists. Sheet: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** each option has a concrete trade and consequence.
4. **Recommend and escalate.** Write the escalation note: what is red, impact if unchanged, options, your recommendation, and the decision needed by a date with an owner.
   **Done when:** the note names one recommended option and a decision owner + deadline.

## Branch C — Status + review

The recurring cadence output. Produce this week's stakeholder update (and a review agenda if you run the meeting).

1. **Refresh RAG.** Update each milestone's status; a color change must have a reason and an ask.
2. **Lead with what changed.** Open on movement since the last update, not a re-list of everything. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
3. **Surface decisions.** Pull every decision needed into one place with owner + deadline; never bury them.
4. **Run the short agenda** (if facilitating): RAG (yellow/red only) → decisions/asks → scope changes → next week.

**Done when:** the update answers "what changed and what do you need from me," every yellow/red has an ask, and the meeting (if any) ends with owned decisions rather than status.

## Branch D — Commitment model

When stakeholders press for a date and you do not need a full pack. Produce a short commit/forecast/target statement.

1. **Split known from unknown.** Separate the scoped, near-term work from the uncertain remainder.
2. **Assign the ladder.** Commit to the scoped near-term, forecast the rest with confidence + top risks, keep the far horizon a target. Language snippets: [references/TEMPLATES.md](references/TEMPLATES.md).
3. **Set the re-forecast checkpoint.** Name when you will firm the next commitment (e.g., "after solutioning on <date>").

**Done when:** each date carries commit/forecast/target language and stakeholders know which dates are promises and when the next one lands.

## Branch E — Demo to production

An AI/ML (or any prototype-first) feature where the demo is fast and production is slow. Produce a plan that separates the two.

1. **Split the two timelines.** Time-to-demo (validate direction) vs time-to-production (make it safe and reliable); state the gap explicitly.
2. **Add the outer loop.** Evaluation harness + acceptance metrics, data readiness + privacy review, guardrails + fallback, monitoring + runbook, and gradual rollout + rollback - each as a milestone with an owner. Prompts: [references/TEMPLATES.md](references/TEMPLATES.md).
3. **Pre-wire expectations.** Communicate the demo-to-production gap up front in commit/forecast/target language so a slick demo is not mistaken for a ship date.

**Done when:** demo and production are separate milestones with separate dates, the outer loop is owned, and stakeholders know the demo is a signal, not a commitment.

## Examples

- *"We're launching at an industry event on May 15 — build the milestone plan and comms for Sales/Marketing/Execs."* → **Branch A**: fixed date treated as P0, phases + gates, RAG cadence, change control, and clear escalation triggers.
- *"Our beta milestone just went red and the date's at risk."* → **Branch B**: quantify the slip, diagnose the real cause, lay out cut/shift/add/quality with costs, and hand over one recommendation plus a decision owner and deadline.
- *"Decide what we should build this quarter and set dates for everything."* → out of scope: use `prioritizing-roadmap` first, then apply this skill to the chosen initiative(s).
