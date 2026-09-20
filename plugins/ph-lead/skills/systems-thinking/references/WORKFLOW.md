# Systems Thinking Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Anti-patterns (catch yourself)

- **Solving the symptom, not the structure.** Fixing the visible pain without touching the incentives or loop that produces it just relocates the pain. Ask what system makes this the rational outcome.
- **The boundary is "everything".** A map that includes the whole company can't drive a decision. Draw it tight enough to act on; note key externalities as interfaces rather than expanding scope.
- **Abstractions masquerading as variables.** "Alignment", "quality", "morale" aren't map variables until you can say how you'd observe them. If you can't define or measure it, it doesn't belong in the map yet.
- **Wishful incentives.** Assuming actors will behave against their own incentives is how interventions backfire. Model what they actually optimize for.
- **Fixing the metric, breaking the system (Goodhart).** Optimizing a proxy invites gaming. Pair every target with a guardrail and watch the loop it creates.
- **Over-correcting through delays.** Acting as if effects are immediate causes oscillation. Where a delay exists, expect overshoot and dampen the response.

## Framing the focal problem (decision-ready)

Rewrite "we need to build X" into "we need to achieve Y under constraints Z." If the problem is a list of symptoms, pick one focal symptom as an entry point — not the assumed root cause.

## System boundary (useful, not complete)

Pick an actionable boundary. Too narrow ignores externalities (partners, incentives, culture); too wide becomes "everything" and prevents decisions. The boundary should carry: goal + time horizon, in-scope actors and interfaces, explicit non-scope, and 1–3 outcome metrics plus 3–7 leading indicators.

## Actors + incentives

For each actor capture: incentives (what they optimize for), constraints (what they can't do), power/agency (what they can influence), and likely behavior if nothing changes. Don't forget invisible actors when relevant — policies and compliance, cultural norms ("this is how we do things"), legacy platform constraints, and funding/allocation and performance-review structures.

## System map (variables + causal links)

Keep it simple and testable. Prefer concrete variables (time-to-resolution, feature adoption, incident rate) over abstractions. Express links as "A increases/decreases B", optionally noting a time delay. If you can't define a variable or how you'd observe it, leave it out.

## Feedback loops + delays

Classify loops: reinforcing (R) amplifies change (growth loops, death spirals); balancing (B) stabilizes (capacity limits, budget caps, policy enforcement). Give each loop a short "so what": what pattern it creates over time and what it optimizes for. Common delay-driven traps: over-correcting (oscillation), fixing the metric and breaking the system (Goodhart), and firefighting loops that starve prevention.

## Second-/third-order effects

For each candidate move: 1st order is the immediate local effect; 2nd order is what other actors do in response; 3rd order is longer-term constraints, norm changes, and path dependence. Always include who wins/loses and how they might respond, which constraints tighten or loosen, and what new loop you might create — intentionally or accidentally.

## Leverage points + interventions

Leverage categories that matter in leadership contexts:

- **Incentives:** what gets rewarded or punished
- **Information flows:** who sees what, when (dashboards, transparency)
- **Rules/policies:** definitions, SLAs, decision rights
- **Buffers/capacity:** staffing, WIP limits, throttles
- **Tools/automation:** eliminate recurring manual work
- **Interfaces:** contracts between teams, APIs, handoffs

Design each intervention with an owner and sequencing, leading indicator(s), guardrail metric(s) to prevent harm, and a rollback or stop condition if risks materialize. If a score comes back low, fix these first, in order: boundary and success measures, actor/incentive realism, then testable causal links.
