---
name: "systems-thinking"
description: "Apply systems thinking to a leadership decision: map actors and incentives, find the feedback loops and leverage points, trace second- and third-order effects, and design interventions that don't backfire."
disable-model-invocation: true
---

# Systems Thinking

## Symptoms are downstream of structure

Anchor every choice below to four ideas:

- **Symptoms are downstream of structure.** Recurring pain is a system producing it on purpose. Treat a symptom as an entry point, not the root cause — fixing it without touching the structure just moves the pain.
- **Every move ripples.** Other actors adapt, so second- and third-order effects (and their time delays) matter more than the immediate one. For any move, name who wins, who loses, and what constraint tightens over time.
- **A useful boundary beats a complete one.** Draw the system tight enough to act on and wide enough to catch the externalities that bite. "Everything" prevents decisions; too narrow ignores the incentives and culture that drive behavior.
- **Leverage over effort.** Hunt for the small change with outsized impact — incentives, information flows, rules — and prefer building a system over solving the same problem again next quarter.

## When to use / not

Use to map a complex system, pressure-test a decision's ripple effects, find leverage points for a systemic pain, or turn recurring pain into a reusable system.

Do **not** use when: the problem is simple, linear, and mostly execution (use a project plan/timeline); you need primary research or data you don't have (do discovery first); you need quantitative forecasting or simulation (this produces a qualitative map and risk ledger, not a full model); or the decision is low-impact and fully reversible — don't over-invest in a two-way door.

## Pick the branch

| The user wants… | Branch |
|---|---|
| To map the whole system behind a problem | **A — Map the system** |
| To pressure-test one decision's ripple effects | **B — Second-order check** |
| To find leverage points for a known systemic pain | **C — Leverage + intervention** |
| To turn recurring pain into a reusable system | **D — Build a system** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) — ask ≤5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A — Map the system

The full diagnostic. Produce a shareable system map a reader can act on without a live meeting.

1. **Frame the focal problem + boundary.** Restate the decision or problem (not a solution in disguise), the desired outcome, and the time horizon; draw a boundary that's actionable, with 1–3 outcome metrics and a few leading indicators. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** scope and non-scope are explicit and the problem isn't a solution in disguise.
2. **Map actors + incentives.** Enumerate players with what they optimize for, their constraints, their power, and their likely behavior if nothing changes. Include invisible actors — policies, culture, platform constraints — when relevant. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** at least one incentive conflict is named and no major actor is missing.
3. **Build the causal map + loops.** List concrete, observable variables and directional causal links (A increases/decreases B), mark time delays, then extract the reinforcing and balancing loops with a "so what" for each.
   **Done when:** links are testable (no undefined abstractions like "quality") and 2+ feedback loops each have a stated pattern-over-time.
4. **Trace effects + choose leverage.** Run the second-/third-order ledger on the top 1–3 candidate moves (branch **B**), then pick leverage points and design interventions (branch **C**), including at least one system-build opportunity (branch **D**). Then run [references/CHECKLISTS.md](references/CHECKLISTS.md), score with [references/RUBRIC.md](references/RUBRIC.md), and close with **Risks / Open questions / Next steps**.
   **Done when:** each intervention has an owner, a leading indicator, a guardrail, and a rollback condition, and tradeoffs are explicit.

## Branch B — Second-order check

The workhorse. Pressure-test a specific move's ripple effects fast. Ledger template: [references/TEMPLATES.md](references/TEMPLATES.md).

For the move, list first-order (immediate/local), second-order (how other actors respond and adapt), and third-order (long-term constraints, norm shifts, path dependence) effects. For each, name who wins, who loses, which constraints tighten or loosen, and what new loop you might create.

**Done when:** the move has at least one named unintended consequence and one mitigating action, with winners and losers made explicit.

## Branch C — Leverage + intervention

Find leverage points for a diagnosed systemic pain and turn them into a plan. Leverage categories (incentives, information flows, rules/policies, buffers/capacity, tools, interfaces) and design guidance: [references/WORKFLOW.md](references/WORKFLOW.md); plan table: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** 3–7 leverage points are tied to the loops/effects, and each intervention has an owner, sequencing, a leading indicator, a guardrail, and a stop condition.

## Branch D — Build a system

Convert recurring pain into a reusable process, operating mechanism, or automation instead of re-solving it. Opportunity table: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** the recurring pain, its root-driver hypothesis, the proposed default-on system, and a first small step are written down, with risks named.

## Examples

- *"Our on-call load keeps rising and teams are burned out — map the system and propose leverage points."* → **Branch A** into **C**: actors/incentives map, a firefighting reinforcing loop, an effects ledger for candidate changes, and interventions with guardrails.
- *"We're changing API pricing — what are the second-order effects across partners and segments?"* → **Branch B**: ledger of first/second/third-order effects with winners, losers, and mitigations across customers and partners.
- *"Write a status update about this week's tasks."* → out of scope: this is for systemic patterns, not execution reporting; suggest a project-update format unless there's a system to diagnose.
