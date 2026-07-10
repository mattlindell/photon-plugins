---
name: "organizational-design"
description: "Design or redesign an org structure and operating model: map current-state dependencies, choose a centralized/decentralized and functional/divisional posture, and produce a target blueprint with a transition plan."
disable-model-invocation: true
---

# Organizational Design

## Structure is a trade-off engine

Anchor every choice below to four ideas:

- **Structure trades one thing for another; it doesn't fix strategy.** Every design trades speed against coherence, autonomy against consistency. Make the trade explicit, and never reorg to paper over an unclear strategy - structure won't fix it.
- **Dependencies are the tax.** Most slow orgs are slow because of dependency chains and unclear decision rights, not effort. Design to remove dependencies, not merely move them.
- **Match posture to product coupling.** Centralize where the customer experience must feel integrated; decentralize behind clean interfaces where surfaces can run in parallel.
- **Leaders must know the work.** Layers and manager roles exist to drive craft and outcomes, not to add coordination. Simplify layers wherever managers are detached from the work.

## When to use / not

Use to answer a specific structural question, redesign a whole org or function, decide a centralize-vs-decentralize posture, or plan a transition to a target design.

Do **not** use for: product strategy or vision (use `defining-product-vision` or `working-backwards`); a people-performance problem (use coaching/feedback, not a reorg); compensation bands, leveling, or hiring plans (involve HR/legal); a single high-stakes decision process (use `running-decision-processes`); or a reorg whose real driver is downsizing - involve HR/legal and settle strategy first.

## Pick the branch

| The user wants... | Branch |
|---|---|
| To answer one bounded structural question now | **A - Quick structural call** |
| To design or redesign a whole org / function | **B - Full (re)design** |
| To decide a centralize/decentralize + functional/divisional posture | **C - Operating-model posture** |
| To roll out a design they've already chosen | **D - Transition plan** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) - ask <=5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A - Quick structural call

The workhorse. A bounded question - where a team sits, split/merge two teams, fix one dependency bottleneck, or clarify decision rights for one recurring decision. Produce a one-page recommendation, not a redesign.

1. **State the question and the outcome.** One line: what structural question, and what it should improve (speed, ownership, coherence).
2. **Trace the friction.** Find the dependency chain or decision-rights gap behind it - the fix is often decision rights, not boxes. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
3. **Name the trade.** What gets faster, what gets harder, and confirm the fix removes a dependency rather than just moving it.
4. **Recommend.** The change, the new decision rights, and a 30-day signal that tells you it worked.

**Done when:** the specific question has a recommended answer, the trade-off is explicit, and there's a 30-day signal to check it against.

## Branch B - Full (re)design

For redesigning a whole org or function. Produce a design a leadership team can align on and execute. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Define what you're optimizing.** Translate "we need a reorg" into 3-5 design principles plus success metrics and constraints.
   **Done when:** stakeholders agree on the top trade-off (e.g., speed vs UX coherence) and what counts as success.
2. **Map the org as a system.** Document charters, dependencies, decision rights, and layers; list the top five friction loops.
   **Done when:** the map explains most observed delays and rework with concrete bottlenecks, not just an org chart.
3. **Choose the operating-model posture.** Place the org on both spectrums (see Branch C), or run Branch C and return.
   **Done when:** the posture matches product coupling - integrated experiences have owners; independent surfaces run in parallel behind interfaces.
4. **Generate 2-3 options.** Each with teams, charters, leadership roles, interfaces, and expected dependency changes; make layers explicit.
   **Done when:** each option states what gets faster, what gets worse, and which dependencies are removed vs merely moved.
5. **Score and recommend.** Score with [references/RUBRIC.md](references/RUBRIC.md); pick a recommendation plus a fallback, and split Day 1 changes from follow-on refactors.
   **Done when:** team charters, lead roles, and decision rights are unambiguous.
6. **Design the transition.** Sequence the change and safety rails, or run Branch D and return.
   **Done when:** critical work has continuity and Day 1 decision-making is clear.
7. **Gate and finalize.** Run [references/CHECKLISTS.md](references/CHECKLISTS.md), re-score with the rubric, and include Risks / Open questions / Next steps.
   **Done when:** the pack passes the checklist; if the score is low, do one more intake round (<=5 questions) and revise.

## Branch C - Operating-model posture

For deciding how centralized and how functional a scope should be. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Place it on two spectrums.** Centralized (Apple-like) <-> decentralized (Amazon-like), and functional <-> divisional/value-stream.
2. **Tie the choice to reality.** Match posture to product coupling, UX integration needs, and talent maturity; write what must be standardized vs allowed to vary.
3. **Write the guardrails.** What you won't decentralize without interfaces/standards; what you won't centralize because it creates bottlenecks.

**Done when:** the posture is explicit on both spectrums with guardrails tied to product coupling and execution needs.

## Branch D - Transition plan

For rolling out a design that's already chosen. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Sequence the change.** Pilot, phased, or big-bang with a rationale; protect in-flight work and define the Day 1 operating model (who decides, what meetings exist, where truth lives).
2. **Plan the comms.** A narrative and FAQ per audience (execs, managers, ICs, partners): why now, what changes, what stays, how decisions work, how to escalate.
3. **Add the safety rails.** Continuity plan, morale/attrition and unknown-approver risks, Day 30/60/90 checks, and rollback triggers for high-risk changes.

**Done when:** people-impact risks are surfaced, critical work has continuity, and there's a clear "how decisions work on Day 1."

## Examples

- *"VP Product, ~200 people, teams are slow from cross-team dependencies - redesign for parallelism."* -> **Branch B**: current-state dependency map, decentralization options behind clean interfaces, target blueprint, transition plan protecting the next launch.
- *"We added layers and lost speed - should we go more functional, and how do we make sure managers know the work?"* -> **Branch C** for the posture, then **Branch D** for a layer-reduction rollout with comms and risks.
- *"Design a reorg that helps us cut headcount quickly."* -> out of scope: org design targets outcomes, not downsizing; involve HR/legal and clarify strategy and constraints first.
