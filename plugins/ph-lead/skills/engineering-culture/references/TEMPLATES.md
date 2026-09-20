# Templates (Copy/Paste)

Building blocks for the branches in `../SKILL.md`. Grab the one your branch points to.

## 0) Blameless Postmortem / Practice-Fix Sheet (Branch F — the workhorse)

Fill this in the few minutes before you address a specific engineering moment (an incident postmortem, a review-norm fix, or a tech-debt call).

**Moment / trigger:** ______  **Date:** ______

- **What happened / what I observed** (specific event or pattern, not a label):
  - …
- **Impact** (on users, delivery, reliability, or trust):
  - …
- **Principle or metric at stake** (which culture-code principle or DORA/quality metric this touches):
  - …
- **Contributing factors** (system, process, tooling, decision — not people):
  - …
- **Move** (practice change, norm to write, ritual to run, or tech-debt decision):
  - …
- **Kept blameless?** (focus on the system, not fault): yes / no — how:
  - …
- **Follow-up** (owner + due date; fixes only, no punishment items):
  - …

### Blameless postmortem (60 min) — if the moment is an incident

1. Timeline (10 min): what happened, in order, no blame.
2. Contributing factors (20 min): system, process, tooling, and decision factors — not people.
3. What we learned (15 min): surprises, gaps, near-misses, detection/response delays.
4. Fixes (10 min): owner + due date for each; no punishment items.
5. Close (5 min): restate the learning/reliability principle this reinforces.

### Tech-debt decision (quick) — if the moment is a pay-down-vs-defer call

- Debt item + where it hurts (velocity, reliability, DevEx):
- Cost of carrying it (per sprint/quarter):
- Cost/effort to fix (S/M/L):
- Decision: pay down now / schedule / accept and revisit by <date>:
- Owner + checkpoint:

## 1) Culture + Capability Snapshot

### Context
- Scope (team/org):
- Products/systems in scope:
- Stage:
- Eng size + topology:
- Remote/hybrid:
- Decision owner(s):
- Timeline / forcing function:

### Symptoms (evidence)
- Symptom 1:
  - Evidence/examples (anonymized):
- Symptom 2:
  - Evidence/examples (anonymized):
- Symptom 3 (optional):

### Current delivery system snapshot
- Release/deploy cadence:
- CI/CD maturity (tests, build time, flakes, approvals):
- Rollback strategy:
- On-call / incident process:
- Toolchain (work tracking, docs, code hosting):

### Baseline metrics (best-effort)
- Deploy frequency:
- Lead time for changes:
- Change failure rate:
- MTTR:
- PR cycle time (optional):
- Experiment throughput (optional):
- DevEx sentiment signal (optional):
- Missing instrumentation:

### Capability map (evidence-based)

| Capability bucket | Current state | Evidence | Gap | Candidate initiative |
|---|---|---|---|---|
| Technical |  |  |  |  |
| Architectural |  |  |  |  |
| Cultural |  |  |  |  |
| Management/Lean |  |  |  |  |

### Priority shifts (2–4)
1. Shift:
   - Why now:
   - What changes in behavior:
   - Leading indicators (2–3):

## 2) Engineering Culture Code (v1)

Write **3–7** principles. Each principle must include observable behaviors.

### Principle <n>: <Name>
- What it means:
- Behaviors we expect:
  - Do:
  - Do:
- Behaviors we avoid:
  - Don't:
  - Don't:
- Decision rules (how choices get made):
- Anti-patterns (how this fails):
- How we'll know it's working (signals/metrics):

## 3) Org ↔ Architecture Alignment Brief

### Current org + operating model
- Teams and ownership (today):
- Cross-team dependencies (today):
- Where decisions happen (today):

### Architecture + ownership boundaries
- Key components/services:
- Ownership clarity:
- Coupling hotspots:

### Conway's Law findings (misalignments)
- Misalignment:
  - Impact:
  - Evidence:

### Proposed changes (operating model)
- Team boundary/ownership change:
  - Rationale:
  - Transition plan:
  - Trade-offs:

### Standardization (where consistency matters)
- Leveling definitions (e.g. "senior" expectations):
- Code review standards:
- Incident/retro expectations:
- Release/deploy policy:
- On-call policy:

## 4) Clock Speed + DevEx Improvement Backlog

### Clock speed targets (next 4–12 weeks)
- Target deploy/release cadence:
- Target lead time:
- Guardrails (change failure rate, MTTR, quality):
- Experiment throughput target (optional):

### Bottleneck map (value stream)
- Where work gets stuck:
- Root causes:

### Prioritized backlog

| Initiative | Lever (tech/arch/culture/lean) | Impact | Effort (S/M/L) | Dependencies | Owner | Metric/leading indicator |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

### First 2-week quick wins
- Win:
  - Owner:
  - Expected signal:

## 5) Cross-functional Workflow Contract

### Toolchain + shared artifacts
- Source of truth for work tracking:
- Source of truth for decisions:
- Source of truth for code + changes:

### Work flow (idea → issue → PR → deploy → learn)
1. Intake/spec:
2. Build:
3. Review:
4. Release:
5. Learn:

### Working agreements
- PR expectations (description, tests, rollout notes):
- Review SLA and escalation path:
- Merge/deploy policy (who can deploy, approvals, rollbacks):
- Experiment policy (guardrails, analysis owner):

### Non-engineer participation (if desired)
- Allowed contributions (issues, docs, config, content via PRs):
- Safety rails (review, staging, feature flags):
- Training plan:

### AI-assisted development norms
- Allowed uses:
- Required human checks:
- Documentation expectations (specs, PR context):
- "No silent changes" rule:

## 6) Rollout + Measurement Plan

### 30/60/90 plan
- Next 30 days:
- Days 31–60:
- Days 61–90:

### Rituals + cadence (reinforcement)

| Ritual | Cadence | Purpose | Owner | Output artifact |
|---|---|---|---|---|
|  |  |  |  |  |

### Metrics + guardrails
- Outcome metrics (2–4):
- Leading indicators (2–4):
- Guardrails (2–4):
- Instrumentation gaps + owners:

## 7) Risks / Open Questions / Next Steps

### Risks
- …

### Open questions
- …

### Next steps (smallest experiments first)
- …
