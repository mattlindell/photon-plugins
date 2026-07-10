# Engineering Culture Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Principles (the checks behind the stance)

1. **Culture shows up in the code and the pipeline.** Diagnose the delivery system (CI, PRs, on-call), not the values doc.
   *Check:* every claimed problem has evidence — an example, a metric, or an observed behavior — or is labeled "needs data."
2. **Org shape drives architecture (Conway's Law).** Design team boundaries and ownership deliberately.
   *Check:* the team-dependency map and the architecture-ownership map line up; no critical area is ownerless.
3. **Velocity and stability rise together.** Small batches, reliable CI, and good tests make shipping fast and safe.
   *Check:* every clock-speed target ships paired with a quality guardrail (change failure rate, MTTR).
4. **Blameless learning compounds.** Treat failures as system signals, not personal faults.
   *Check:* postmortems produce system/process fixes with owners — never punishment items.
5. **Reinforce via practice, not proclamation.** Culture spreads through rituals, review norms, onboarding, and what leaders merge.
   *Check:* the rollout names rituals and owners, not just a published document.

## Anti-patterns (catch yourself)

- **Hero culture.** Rewarding all-nighters and firefighting normalizes the conditions that cause fires. Reward the boring, repeatable systems that prevent them.
- **Blame-driven postmortems.** Hunting for the person who "caused" it buries the systemic causes and teaches people to hide problems. Fix the system, not the person.
- **Vanity metrics.** Lines of code, commit counts, and raw story-point velocity measure activity, not outcomes. Anchor on DORA + quality + DevEx.
- **Quality theater.** Mandatory approvals, heavyweight process, and gatekeeping reviews that catch nothing but slow everything. Make CI boring instead.
- **Announcing the doc and calling it done.** A culture code with no rituals, review norms, or leader modeling changes nothing. Reinforcement is the work.
- **Reorg-first.** Redrawing the org chart before understanding the architecture and its dependencies just reshuffles the friction.
- **"Move fast" without guardrails.** Raising deploy frequency while ignoring change failure rate and MTTR trades a velocity problem for a reliability one.

## Culture as a delivery system (capability map)

Map the current state across four capability buckets (from DevOps research and practice):

- **Technical:** CI reliability, automated testing, build/deploy automation, observability, feature flags.
- **Architectural:** loose coupling, clear ownership boundaries, stable interfaces, evolvable architecture.
- **Cultural:** ownership, collaboration, blameless learning, willingness to simplify, attention to customer impact.
- **Management/lean:** small batches, WIP limits, clear priorities, fast feedback loops, continuous-improvement rituals.

Output a capability map with evidence and gaps, not slogans.

## Evidence collection (keep it lightweight)

Prefer quick signals over heavy process:

- 2–5 anonymized examples per symptom.
- A value-stream timeline for 1–2 recent changes (idea → prod → learn).
- A minimal baseline of metrics (DORA if available; otherwise best-effort proxies, labeled).
- A quick coupling/ownership scan (where everything depends on everything).

If evidence is missing, label the assumption and propose an instrumentation spike as a backlog item.

## Conway's Law analysis (org ↔ architecture fit)

1. Draw a simple map of teams and their dependencies (who blocks whom).
2. Draw a simple map of architecture ownership boundaries (what team owns what).
3. Identify misalignments:
   - multiple teams editing the same critical area
   - unclear owner for shared components
   - platform as a bottleneck without a product interface
4. Propose changes:
   - adjust boundaries/ownership
   - define explicit interfaces (APIs, contracts, SLAs)
   - standardize policies where inconsistent expectations create friction (leveling, on-call, code review, incident process)

Sequence carefully: understand the architecture and dependencies before you move boxes on the org chart.

## Clock speed (safe shipping + experimentation)

Define clock speed using a small set of concrete targets:

- Deploy frequency (or release frequency)
- Lead time for changes (idea → prod)
- Change failure rate + MTTR (guardrails)
- Experiment throughput (experiments shipped per week; time-to-learn)

Then identify bottlenecks and propose improvements:

- "Make CI boring": reduce flakes, shorten builds, stabilize the test suite.
- Progressive delivery (canaries, feature flags, staged rollouts).
- Improve observability and rollback confidence.
- Reduce batch size and normalize incrementalism.

Speed targets and quality guardrails move together — never publish one without the other.

## Cross-functional workflow contract (shared toolchain)

The goal is not "make everyone code." The goal is **shared visibility and shared operating rhythms**.

Define:

- Where work lives (issues, docs, PRs) and who is responsible for updates.
- Expectations for PR descriptions, review SLAs, and decision logging.
- How non-engineers contribute safely (issues, copy/config changes, feature flags, content via PRs).
- How experimentation is requested, built, launched, and analyzed (owner, approval, guardrails).

## AI-assisted development norms (humans as architects)

Make norms explicit so adoption increases quality rather than chaos:

- Allowed uses (boilerplate, tests, refactors, scaffolding, documentation, migration helpers).
- Required human checks (design intent, security/privacy, correctness, integration, performance).
- "No silent changes" rule: AI-authored code requires clear diffs, tests, and reviewer context.
- Parallelization norms: async handoffs, spec-first tickets, multiple agents in parallel with a human integrator.

## Tech-debt policy (pay down vs defer)

Make the trade-off explicit rather than implicit:

- Name where the debt hurts (velocity, reliability, DevEx) and estimate the cost of carrying it per sprint/quarter.
- Budget a standing fraction of capacity for debt paydown so it is not perpetually crowded out.
- For each item, decide: pay down now, schedule, or accept and revisit by a date — with an owner and a checkpoint.
- Watch for debt that shows up as a Conway misalignment or a CI/flakiness bottleneck; fix the cause, not the symptom.

## Rollout and reinforcement

Treat this like a change program, not a document:

- Pick 1–2 rituals to start (weekly delivery review, blameless retro, architecture/ownership review).
- Train on the workflow contract (especially non-engineers, if included).
- Add lightweight measurement and publish progress.
- Make standardization explicit: what is optional vs required across teams.
