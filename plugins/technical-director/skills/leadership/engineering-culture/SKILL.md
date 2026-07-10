---
name: "engineering-culture"
description: "Build or refresh engineering culture as a delivery system: diagnose what is real in the code and the pipeline, express it as a culture code, align teams with architecture (Conway's Law), raise clock speed and DevEx, and fix a specific practice or run a blameless postmortem right now."
disable-model-invocation: true
---

# Engineering Culture

## Culture shows up in the code and the pipeline, not the wiki

Anchor every choice below to four ideas:

- **The delivery system is the culture.** What the CI logs, the open PRs, and the on-call rotation reveal is the real culture — the values doc is not. Diagnose the system with evidence before you rewrite anything.
- **Org shape drives architecture (Conway's Law).** Teams ship their communication structure. Design team boundaries and ownership deliberately, or the architecture will inherit the accidents of your org chart.
- **Velocity and stability rise together.** Sustainable speed comes from small batches, reliable CI, and good tests — not heroics. Hero culture and quality theater both slow you down; measure with DORA plus quality, not vanity metrics.
- **Blameless learning compounds.** Treat failures as system signals, not personal faults. A blameless postmortem culture turns incidents into reliability; blame culture buries the truth you need to improve.

## When to use / not

Use to diagnose engineering culture as a delivery system, write an engineering culture code, align team structure with architecture (Conway's Law), raise clock speed and DevEx, define a cross-functional workflow contract, or fix a specific engineering practice or moment right now.

Do **not** use for: an active incident or outage — follow your runbook / on-call process (offer a blameless postmortem afterward); HR/legal policy, investigations, or employee relations — route to HR/legal; a purely technical task with no culture/org/process angle (e.g. "set up CI") — just do the work; or full roadmap prioritization across many bets — use **prioritizing-roadmap**.

## Pick the branch

| The user wants… | Branch |
|---|---|
| To build or refresh the whole engineering culture + delivery system | **A — Engineering-culture operating system** |
| To diagnose what the culture and delivery system actually are today | **B — Capability & delivery snapshot** |
| To write the engineering culture code (principles → behaviors) | **C — Culture code** |
| To align team structure with architecture | **D — Conway's Law alignment** |
| To ship faster and safer / improve DevEx | **E — Clock speed & delivery** |
| To fix one engineering practice or handle a moment right now | **F — Practice fix (the workhorse)** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) — ask ≤5 at a time, then proceed on labeled assumptions; never request secrets, credentials, or proprietary identifiers, and use redacted summaries.

## Branch A — Build the engineering-culture operating system

1. **Frame goals and route risk.** Confirm what should be more true in 4–12 weeks, the constraints, and the non-negotiables (compliance, security, quality guardrails). If the request is an active incident or an HR/legal matter, pause and route it.
   **Done when:** the target state is observable and incident/HR topics are routed away from this skill.
2. **Build the capability & delivery snapshot** (Branch B) so change rests on evidence, not opinion.
   **Done when:** the snapshot separates stated from lived culture, includes a capability map, and has a DORA baseline (or labeled instrumentation gaps).
3. **Write the engineering culture code** (Branch C) from 2–4 priority shifts.
   **Done when:** each principle has behaviors, a decision rule, an anti-pattern, and one observable signal.
4. **Align org with architecture** (Branch D) and **raise clock speed / DevEx** (Branch E).
   **Done when:** Conway misalignments have transition steps and trade-offs, and the delivery backlog has owners and metrics.
5. **Plan rollout and reinforcement.** Design a 30/60/90 with rituals, onboarding for the workflow contract, and metrics with guardrails (DORA + quality + DevEx). Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** reinforcement exists beyond "publish the doc," with owners and measurable signals.
6. **Quality gate and finalize.** Pass [references/CHECKLISTS.md](references/CHECKLISTS.md), score with [references/RUBRIC.md](references/RUBRIC.md), propose the smallest 1–2 experiments to start this week, and close with **Risks / Open questions / Next steps**.

Deliverable: an **Engineering Culture Operating System** — capability snapshot, culture code, org↔architecture brief, clock-speed/DevEx backlog, workflow contract, and rollout + measurement plan.

## Branch B — Capability & delivery snapshot (diagnose first)

Capture what is true today before touching anything. Build a capability map across **technical**, **architectural**, **cultural**, and **management/lean** capabilities; distinguish stated vs lived culture; establish a DORA baseline (deploy frequency, lead time, change failure rate, MTTR) or label the gaps; and run a value-stream timeline on 1–2 recent changes (idea → prod → learn). Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md); template: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** the snapshot is evidence-based (2–5 anonymized examples per symptom), has a capability map, and carries a DORA baseline or explicitly labeled instrumentation gaps.

## Branch C — Engineering culture code

Write 3–7 principles. For each: definition, do/don't behaviors, decision rules for common engineering dilemmas (ship vs polish, review depth, tech-debt trade-offs), anti-patterns, and healthy signals. Prefer articulating what already works; make each principle observable in code, PRs, or on-call — not a slogan. Template: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** each principle is behavior-based with a decision rule, at least one anti-pattern, and an observable signal or metric.

## Branch D — Conway's Law alignment

Map team dependencies (who blocks whom) against architecture ownership boundaries (who owns what), then find the misalignments — multiple teams editing one critical area, an ownerless shared component, or a platform bottleneck with no product interface. Propose team boundary/ownership changes, explicit interfaces (APIs, contracts, SLAs), and standardization where inconsistent expectations create friction (leveling, on-call, code review, incident process). Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md); template: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** each misalignment has a proposed change with transition steps and explicit trade-offs (what gets worse).

## Branch E — Clock speed & delivery

Define clock-speed targets (deploy frequency, lead time) paired with quality guardrails (change failure rate, MTTR). Find the bottlenecks in the value stream and convert them into a prioritized DevEx backlog — make CI boring, shrink batch size, add progressive delivery, improve observability and rollback confidence. Set the cross-functional workflow contract (idea → issue → PR → deploy → learn; review SLAs; who can deploy) and AI-assisted development norms (allowed uses, required human checks, no silent changes). Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md); template: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** each backlog item has an owner, an effort range, a dependency note, and a leading indicator; every speed target ships paired with a guardrail.

## Branch F — Practice fix (the workhorse)

The frequent, in-the-moment use: fix one engineering practice or handle a specific moment now — run a blameless postmortem after an incident, repair a code-review norm that is causing friction, or make a tech-debt call (pay down vs defer). Name the behavior or pattern observed, tie it to the principle or metric at stake, choose the practice change or ritual to run, and set a follow-up. Working sheet: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** the moment is handled as a system fix (behavior/pattern → impact → the practice or principle it touches), kept blameless, with a concrete follow-up and owner.

## Examples

- *"Our delivery is slow and incidents are rising — build us a real engineering culture and delivery system."* → **Branch A**: evidence-based capability snapshot with a DORA baseline, culture code, Conway alignment, clock-speed backlog, and a 30/60/90 rollout.
- *"We just had a production incident — help me run the postmortem so it doesn't turn into blame."* → **Branch F**: a blameless postmortem tied to the learning/reliability principle, with follow-ups limited to system fixes, not fault.
- *"We have a P1 outage right now — what do I do?"* → out of scope: this is active incident response — follow your runbook and on-call process first; offer to run a blameless postmortem (Branch F) once it is resolved.
