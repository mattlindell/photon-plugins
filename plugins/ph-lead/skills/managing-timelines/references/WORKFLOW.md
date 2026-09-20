# Timeline Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Anti-patterns (catch yourself)

- **Date soup.** Handing out a single number when you mean a forecast. Always label commit/forecast/target so a promise reads differently from an estimate.
- **Committing the far horizon.** Promising Build/Launch dates before solutioning and estimation. Commit the next phase output; forecast the rest.
- **Hero mode.** Answering a slip by adding people or hours instead of trading scope. Late-added people usually slow things further - trade, don't add.
- **RAG theater.** Reporting red with no ask. A red without a decision request is just anxiety broadcast to stakeholders.
- **Surprise slips.** Sitting on a risk until it is certain. Surface it while there is still room to act - early amber beats late red.
- **Demo equals done.** Letting a slick prototype set the ship date. Name the outer loop before anyone celebrates.
- **Activity milestones.** "Working on X" is not a milestone. Milestones are deliverables with a done bar and an owner.

## Deadline taxonomy (what kind of date is this?)

- **Fixed external deadline:** tied to an external event, contract, or regulatory requirement. Date is effectively immovable; scope and resources are the levers.
- **Fixed internal deadline:** a leadership commitment; may still be movable, but only via an explicit re-decision.
- **Target date:** a directional date to guide prioritization; can move as uncertainty resolves.
- **Window:** a range ("late March") that tightens over time; useful when uncertainty is high.

Rule of thumb: if details are missing, treat it as a **target/window** and state explicitly what would be required to turn it into a commitment.

## Commitment ladder (use precise language)

Three date types keep you out of date soup:

- **Commitment:** "We will deliver X by D" - only for scoped work within control.
- **Forecast:** "Based on what we know, we expect D" - subject to change as risks resolve.
- **Target:** "We want D" - directional, used for prioritization.

Always attach: confidence + top risks + the next decision point. Never present a forecast as a commitment.

## Phase-based planning (commit only within control)

Recommended lifecycle:

1. **Discovery** (reduce problem uncertainty) - problem framing, user value, success metrics/guardrails, top risks, initial approach options.
2. **Solutioning** (reduce solution uncertainty) - chosen approach, UX/tech outline, dependency plan, estimate range, rollout approach.
3. **Build** (execution) - working increments, QA plan, release-readiness checks.
4. **Launch** (safe release) - rollout/rollback plan, comms, monitoring, post-launch checks.

Commitment pattern: commit to **Discovery/Solutioning end dates** first; commit to Build/Launch only after solutioning and estimation. Set a "next commitment date" - when you will re-forecast (e.g., "we re-forecast on <date> after solutioning").

## RAG that triggers action

Define RAG so it forces decisions:

- **Green:** on track; no decisions needed.
- **Yellow:** risk emerging; needs a decision or assist within about a week.
- **Red:** cannot meet the committed date without a change (scope/date/resources/quality); needs an immediate decision.

Every yellow/red should carry: "what changed since last update," "decision needed" + deadline, and a proposed trade-off (cut/add/shift).

## Diagnosing a slip (Branch B)

Find the real driver before proposing a fix. Common root causes:

- **Scope creep** - work grew quietly; the current scope is not what was estimated.
- **Optimistic estimates** - the plan never fit; no single event caused it.
- **Hidden dependency** - another team, vendor, data, or approval is the actual blocker.
- **Capacity loss** - PTO, attrition, or context-switching drained the assumed capacity.
- **Quality debt** - defects/rework surfacing late in Build or QA.

The four levers, in usual order of preference:

1. **Cut scope** - fastest, cheapest; needs a pre-agreed cut list to move quickly.
2. **Move the date** - honest when scope and quality are fixed; do it once, with a new committed date, not a rolling slip.
3. **Add resources** - rarely helps late (ramp cost, coordination overhead); reserve for early-phase or narrow, parallelizable work.
4. **Lower quality** - only if explicitly allowed and reversible; never for safety, security, or compliance.

If no cut list exists, building one is the first move - you cannot trade scope fast without it.

## Weekly update + review (Branch C)

Default cadence: weekly. Keep the review short so it runs consistently.

- **Agenda:** RAG (yellow/red only) → decisions/asks (owner + deadline) → scope changes and trades → next week's plan.
- **Updates lead with "what changed,"** not a re-list of everything. Bury nothing: asks and decisions go up top with dates.
- **A red has a single escalation path** and one decision owner. If a red produces no ask, it is not ready to report.
- Prefer shared, async-readable updates; a stakeholder should be able to approve without a meeting.

## AI/ML uneven cadence (demo vs production)

For AI/ML, separate the two clocks:

- **Time to first demo** (often short): a prototype to validate direction.
- **Time to production** (often much longer): evaluation, safety, reliability, cost/latency, monitoring, fallback behavior, edge cases, compliance.

Add explicit outer-loop milestones:

- Evaluation harness + acceptance metrics.
- Data readiness + privacy review.
- Guardrails + fallback plan.
- Monitoring + incident response/runbook.
- Gradual rollout + post-launch calibration.

The failure mode is a great demo setting a ship date. Pre-wire the gap in commit/forecast/target language before anyone treats the demo as done.
