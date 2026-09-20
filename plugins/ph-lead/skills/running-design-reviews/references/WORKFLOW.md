# Design Review Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Anti-patterns (catch yourself)

- **The review with no decision.** "Let's get feedback" produces a pile of opinions no one acts on. If you can't say what changes after, you're not ready to review.
- **Pixel-fighting before the concept holds.** Arguing color and copy while Value and Ease are unresolved wastes the room. Enforce the hierarchy.
- **Preference dressed as feedback.** "I'd do it differently" is noise; "users hit a dead end here, so they'll abandon" is signal. Demand observation + impact.
- **Design-by-committee.** Averaging everyone's taste produces mush. The Sponsor/DRI decides against goals and constraints when feedback conflicts.
- **Slideware instead of the artifact.** Reviewing a deck about the design hides the real friction. Demo the live thing.
- **Feedback that evaporates.** Great crit with no written decisions, owners, or dates changes nothing. Log it and send the follow-up.

## Roles (minimum)

- **Presenter:** walks through the artifact and the decision needed.
- **Facilitator:** keeps time, enforces feedback order, prevents design-by-committee.
- **Sponsor/DRI:** senior owner who focuses on "why," core concept quality, and final calls.
- **Note-taker:** captures feedback in the log and drafts the follow-up.

## Review types (pick one)

- **Concept review:** Is this direction worth pursuing? (Value-dominant)
- **Flow review:** Does the interaction make sense end-to-end? (Ease-dominant)
- **Content review:** Clarity, comprehension, tone, information hierarchy. (Value/Ease)
- **Visual polish review:** Craft, aesthetics, consistency. (Delight-dominant, only after Value/Ease)
- **Ship-readiness review:** Edge cases, states, regressions, accessibility. (High rigor)

## The feedback hierarchy (enforce this order)

1. **Value:** Does this solve the right problem in a way users will want?
2. **Ease:** Can users do it without confusion, excessive effort, or dead ends?
3. **Delight:** Does it feel great? Is the craft/polish appropriate?

When debates devolve into preferences, pull back to: goal → user → constraint → evidence.

## Agenda timeboxes

- **30 min (tight):** context 3 / demo 10 / capture 12 / synthesis + decisions 5.
- **45 min (default):** context 5 / demo 15 / capture 15 / synthesis + decisions 10.
- **60 min (complex flow):** context 5 / demo 20 / capture 20 / synthesis + decisions 15.

## Preventing design-by-committee

- Ask reviewers to state **observations** and **impact** before solutions.
- Require the presenter to restate feedback in their own words before accepting it.
- Timebox solutioning; park deeper explorations as follow-up tasks.
- If feedback conflicts, the Sponsor/DRI decides based on goals and constraints.

## Async review variant

1. Share the pre-read plus a short video walkthrough (optional).
2. Request feedback via 1–3 explicit questions.
3. Require feedback logged into the same Value/Ease/Delight table.
4. Synthesize and circulate a decision record + change plan.
