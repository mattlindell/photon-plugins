---
name: "planning-under-uncertainty"
description: "Plan and lead execution when outcomes are uncertain: diagnose reality, turn assumptions into falsifiable hypotheses and experiments, and build a plan with buffers, contingencies, and pivot triggers."
disable-model-invocation: true
---

# Planning Under Uncertainty

## Learn your way to a plan

Anchor every choice below to four ideas:

- **Diagnose before acting.** Especially in a crisis, separate symptoms from causes and hold several falsifiable hypotheses before committing to a story. Bias toward reversible actions until uncertainty drops.
- **Winning is learning, not "wins."** Every experiment must answer "what will we do differently depending on the result?" A falsified assumption that changes a decision is a success, not a failure.
- **Data is a compass, not a GPS.** Use directional signals and disprove-fast tests; pair every metric with a guardrail so you don't optimize the wrong thing. Avoid false precision.
- **Plans state what you'll do when uncertainty resolves.** Good plans don't claim certainty; they carry buffers, contingencies, and explicit "if X then Y" triggers for pivot, rollback, or escalation.

## When to use / not

Use to design an experiment, run a wartime crisis response, build a full uncertainty plan for an ambiguous initiative, or stand up a learning cadence.

Do **not** use for: disagreement on the underlying problem (use `problem-definition`); choosing among many options (use `prioritizing-roadmap`); a clear plan that only needs dates and stakeholder cadence (use `managing-timelines`); or a decision-ready PRD/spec (use `writing-prds` / `writing-specs-designs`).

## Pick the branch

| The user wants... | Branch |
|---|---|
| To design a test for one assumption now | **A - Design an experiment** |
| To respond to a live crisis (drop/incident) | **B - Wartime response** |
| A full plan for an ambiguous initiative | **C - Full uncertainty plan** |
| To set up the learning ritual and comms | **D - Cadence + comms** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) - ask <=5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A - Design an experiment

The workhorse. Turn one assumption into a test you can run this week. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **State the assumption and the decision it blocks.** What would you do differently once you know?
2. **Write it falsifiably.** "If we do X for segment Y, then Z changes by A because M." Name the compass signal and one guardrail. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
3. **Pick the fastest disproving test.** Smoke test, five customer calls, prototype, A/B, or ops drill - with an owner, sample, and duration.
4. **Write the decision rule.** "If we see <threshold> by <date>, we scale / pivot / stop."

**Done when:** the hypothesis is falsifiable, tied to a decision, and has the fastest viable test with an owner and a decision rule.

## Branch B - Wartime response

For a live crisis - a metric drop, incident, or growth collapse. Diagnose first; act reversibly. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Declare wartime.** State the decision needed (rollback / patch / hold) and by when; restrict changes to reduce noise.
2. **Diagnose before acting.** Separate symptoms from causes; write 3-7 hypotheses, including uncomfortable ones, and what evidence would falsify each.
3. **Run rapid, reversible tests.** Move at a daily or 48-hour tempo; keep actions reversible until uncertainty drops.
4. **Set the triggers.** "If <signal> crosses <threshold>, we rollback / pivot / escalate by <when>," with a named decision owner.

**Done when:** causes are being tested rather than assumed, and there are written rollback/escalation triggers with an owner.

## Branch C - Full uncertainty plan

For an ambiguous initiative in peacetime. Produce a pack a stakeholder can approve async. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Frame the decision and mode.** Objective, why now, success + guardrails, horizon, and the decision owner.
   **Done when:** you can state what you're optimizing for and the decision needed by a date.
2. **Diagnose reality.** Separate symptoms from hypotheses; make at least one hypothesis contradict the team's intuition.
   **Done when:** the "what we know / don't know" split is explicit.
3. **Build the uncertainty map.** Assumptions with confidence and impact; the top five unknowns, each with a validation method and owner.
   **Done when:** every top unknown has a validation method and an owner.
4. **Define hypotheses + decision rules.** Turn top unknowns into falsifiable hypotheses (or run Branch A per unknown), each tied to a stop/pivot/scale decision.
   **Done when:** each hypothesis ties to a decision and winning is defined as learning.
5. **Design the experiment portfolio.** Balance fast/cheap and slower/high-confidence tests; set a review cadence.
   **Done when:** at least one fast test can run within the next 1-2 weeks.
6. **Build Plan v0 with buffers + triggers.** Phases with learning gates, explicit buffers, contingencies (A/B/C), and "if X then Y" triggers.
   **Done when:** there's a clear "if X happens, we do Y" for the top risks and unknowns.
7. **Gate and finalize.** Run [references/CHECKLISTS.md](references/CHECKLISTS.md), score with [references/RUBRIC.md](references/RUBRIC.md), and include Risks / Open questions / Next steps with owners and time bounds.
   **Done when:** a stakeholder can approve async and the team can execute without re-litigating the ambiguity.

## Branch D - Cadence + comms

For standing up the learning ritual around an uncertain effort. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Set cadence to the mode.** Wartime: daily or 48-hour reviews on the top hypotheses. Peacetime: weekly learning review plus a biweekly decision checkpoint.
2. **Stand up the ritual.** A runnable review agenda (what changed, what we learned, what we decide, next tests, risks) and a durable decision log.
3. **Standardize the update.** A stakeholder format: status, this week's learning, decisions made/needed with owners, next tests, and risks.

**Done when:** the cadence, a runnable agenda, a decision log, and a stakeholder update format all exist.

## Examples

- *"We think onboarding is hurting conversion but aren't sure why."* -> **Branch C**: uncertainty map, a qual+quant experiment portfolio, and a Plan v0 committed to learning milestones rather than premature delivery dates.
- *"Retention dropped 15% this week after a release - rollback or patch?"* -> **Branch B**: diagnosis-first hypotheses, rapid reversible tests, tight guardrails, and explicit rollback/escalation triggers.
- *"Write a full PRD for Feature X."* -> out of scope: clarify the uncertainty here first, then use `writing-prds` once hypotheses, constraints, and decision gates are clear.
