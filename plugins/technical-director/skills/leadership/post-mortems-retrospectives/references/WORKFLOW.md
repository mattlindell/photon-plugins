# Post-mortem & Retro Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Anti-patterns (catch yourself)

- **Blame wearing a systems costume.** "We lacked a check" is systemic; "X should have caught it" is blame with better grammar. If a factor names a person, rewrite it as the condition that let the mistake happen.
- **Story time before fact time.** Jumping to "why" before the timeline is built bakes in the loudest person's theory. Lock the facts first.
- **The grade is the meeting.** Spending the retro defending or litigating the OKR score wastes the learning. The number is a prompt, not the point.
- **Orphan actions.** "We should communicate better" / "be more careful" have no owner, date, or signal — they change nothing. Every action names all three.
- **Kill criteria as theater.** A trigger whose committed action is "discuss it" is not a trigger. Pre-commit to pause/pivot/kill/escalate/invest, or drop it.
- **Learnings that stay local.** A brilliant retro no one outside the team hears is a private diary. Socialize it or it repeats elsewhere.

## Blameless framing & roles

Good reviews fail when the **goal is ambiguous**. Set it explicitly: learning + improvement, not judgment.

Minimum roles:
- **Facilitator:** protects process, timeboxes, and psychological safety.
- **Scribe:** captures facts, decisions, and actions live.
- **Decision owner:** commits to actions and follow-through (may be the facilitator).

Language and ground rules (copy/paste):
- If "post-mortem" reads punitive, call it a **retrospective** or **learning review**.
- "We are here to improve systems, not judge individuals."
- "Assume people acted reasonably given what they knew at the time."
- "Performance topics, if any, are handled separately through the right channels."

## Facts & timeline (no opinions yet)

Two common failure modes: the doc becomes opinionated storytelling without timestamps, and the timeline drops the "invisible work" (hand-offs, waiting, approvals).

- Put **timestamps** everywhere you can.
- Mark each line **fact** vs. **hypothesis** explicitly.
- If you can't cite evidence, label it a hypothesis to confirm — don't launder it into a fact.

## Contributing factors (systems lens)

Prompting questions: What made this outcome **likely**? What constraints or incentives shaped behavior? Where did we rely on heroics, tribal knowledge, or unowned components?

Clusters to sweep:
- **People:** skills coverage, on-call load, staffing, handoffs.
- **Process:** change management, reviews, incident roles, decision latency.
- **Product/UX:** guardrails, unsafe defaults, user confusion.
- **Tech:** architecture, dependencies, observability, test gaps.
- **Comms:** stakeholder awareness, escalation paths, ambiguous ownership.
- **Environment:** traffic spikes, vendor outages, seasonality.

## Learnings & decisions (learning > grading)

For an OKR/goal retro, keep the number secondary to "what system produced this result?" and "what would make 1.0 plausible next time?"

Decision types to consider:
- **Fix now** (bug, reliability, UX).
- **Guardrail** (safe defaults, limits, feature flags).
- **Instrumentation** (alerts, dashboards, missing metrics).
- **Runbook/training** (operational readiness).
- **Process change** (reviews, approvals, decision rights).
- **Scope change** (de-scope, postpone, kill/pivot).

## Action tracker (the follow-through mechanism)

- Every action carries **owner**, **due date**, **success signal**, and **follow-up date**.
- Prefer actions that remove entire classes of failure, not one instance.
- Limit "fix now" items to what fits capacity; park the rest explicitly instead of pretending they'll happen.

## Kill criteria / triggers (pre-commit to action)

Kill criteria only work if you pre-commit. Each one needs:
- **Signal:** observable threshold (metric drop, incident count, adoption stall).
- **Window:** how long before it counts.
- **Action:** pause / pivot / kill / escalate / invest.
- **Owner:** who declares and executes it.

Examples:
- "If activation doesn't improve by +2pp over 4 weeks after shipping feature X, we pause new scope and run 5 user interviews."
- "If we hit 2+ S0 incidents in a month for subsystem Y, we freeze feature work and fund reliability for 2 sprints."

## Dissemination & learning rituals

Retros fail when learnings stay local. Lightweight options:
- A weekly/biweekly **Impact & Learnings Review** (30 min): top learnings (not status), what we changed (decisions), what's next (experiments).
- A single shared **learning log** channel or doc with a consistent format.

Shareout heuristic: a leader should be able to read the TL;DR and answer "what changed because of this?"
