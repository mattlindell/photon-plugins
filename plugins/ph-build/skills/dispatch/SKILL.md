---
name: dispatch
description: Entry point for building something. Reads how much was already decided, sizes the rigor to what is left, and routes to a playbook. Use before any non-trivial code change — a feature, bug fix, refactor, migration, or performance work.
---

# Dispatch

Work arrives here to be built. Three things happen before any code: read what
was already decided, size the effort to what is left, route to a playbook.

**Requires `ph-lib`.** If `ph-lib:unslop` and `ph-lib:codebase-design` are not
reachable, say so plainly and continue — degraded, not stopped.

## 1. Read the rigor signal first

Before anything else, look for a spec, ticket, or design doc for this work, and
find its `settled:` block.

```yaml
settled: [problem, shape, approach]
open: [verification]
```

Each dimension is `problem` (what and why), `shape` (structure and types),
`approach` (implementation path), `verification` (how anyone knows it is done).

**A settled dimension is a decision already made. Do not re-derive it.**
Re-opening a settled question is the single most expensive mistake available
here — it spends a panel of agents rediscovering something a human already
wrote down.

| State | What it means |
| --- | --- |
| All four settled | Build it. `scoped` tier, no panels, no exploration phase. |
| Some settled | Skip the phases that own the settled dimensions; work only the open ones. |
| None settled, or no block found | One bounded orientation pass (below). |
| No spec at all | Route to `ph-plan:intake`. If nobody is available and the work is reversible, take the orientation pass and proceed. |

`verification: open` means *use the standard test-first default* — it never
means tests are optional.

### The bounded orientation pass

When nothing is settled, you get **one** pass to orient: a single `how` run, no
panels, no `arena`, no `architect`. Write what you inferred as a provisional
`settled:` block, say that you inferred rather than read it, and proceed.

You do not get a second pass. If one bounded pass is not enough, that is a
signal the work needed planning, not more agents.

## 2. The gate: escalate on one-way doors, not on uncertainty

The expensive machinery — `architect`, `arena`, `interrogate`, `swarm` — is
**off by default**. It turns on for one reason: the work touches a **one-way
door**, a decision whose cost to undo is real.

One-way doors:

- Schema changes and data migrations
- Public API surface, or anything external consumers depend on
- Anything that deletes or irreversibly rewrites data
- Auth, billing, security boundaries

Everything else is a two-way door. **Vague but reversible work just gets built**
— you course-correct on review, which is cheaper than a panel.

When you escalate, log it: which door, which skill you reached for, why the
cheap path was not enough. That record is how the gate gets tuned.

This is the fix for the failure this plugin exists to prevent: fully specified
work priced as though nothing were known.

## 3. Triggers

Conditional on the gate above. None of these is unconditional.

- **Nontrivial change or "are we sure?"** → the **how** skill, unless `shape` is settled.
- **Code crossing a function boundary at a one-way door** → the **architect** skill. Two-way door: name the data shape per **principle-model-the-domain** and build.
- **Contested design at a one-way door** → the **interrogate** skill before shipping.
- **Coverage matrices, races, exploration partitions** → the **swarm** skill, within its cap. Design or code bakeoffs → **arena**.
- **Any code** → name the data shape first (**principle-model-the-domain**).
- **Any prose surface, including your reply** → `ph-lib:unslop`. Docs, RFCs, PR descriptions, commit messages also take `ph-lib:technical-writing`.
- **Before commit** → the **deslop** skill. **Before review** → **no-comments**.
- **Shipping UI or CLI** → drive the real surface. For bug fixes, reproduce it yourself first.
- **Any PR-status request** → the **Babysit** playbook, not the `babysit` skill.
- **A review bot commented** → skeptical posture, triage per `references/bugbot-triage.md`.
- **Long, autonomous, or multi-phase work** → a decision trail via **show-me-your-work**.
- **Broken skill mid-task** → fix it in its own PR. Don't block, don't work around it silently.
- **A defect found mid-task** → severity decides its artifact, not where it surfaced.

## 4. Playbooks

Open a todolist whose first items are the matched playbook's steps, copied in
verbatim, before any task-specific todos. A step you skip stays in the list with
a one-line `skip: <reason>`.

Each playbook has a **total agent budget** in the fan-out policy. That budget
covers the whole composition including nested fan-out, and it is a ceiling.

- **Investigation.** Read-only question. `playbooks/investigation.md`
- **Bug fix.** Reproduce, root-cause, fix with runtime evidence. `playbooks/bug-fix.md`
- **Perf issue.** Trace a measured slowness against a baseline. `playbooks/perf-issue.md`
- **Hillclimb.** Sustained improvement of one metric against a target. `playbooks/hillclimb.md`
- **Runtime forensics.** Diagnose a live runtime symptom. `playbooks/runtime-forensics.md`
- **Trace forensics.** Diagnose a captured profiling artifact. `playbooks/trace-forensics.md`
- **Feature.** New or changed behavior, built from a named data shape. `playbooks/feature.md`
- **Refactoring.** Behavior-preserving change to structure. `playbooks/refactoring.md`
- **Prototype.** Throwaway sketch to settle a design or empirical fork. `playbooks/prototype.md`
- **Visual parity.** Pixel-exact UI equivalence. `playbooks/visual-parity.md`
- **Authoring a skill.** Writing or editing a SKILL.md. `playbooks/authoring-a-skill.md`
- **Eval.** Testing how a skill or prompt change affects behavior. `playbooks/eval.md`
- **Babysit.** Driving a PR or stack to merge-ready. `playbooks/babysit.md`
- **Shipping.** Verifying a green stack and landing it. `playbooks/shipping.md`
- **Autonomous run.** Driving a long task to a predicate without stopping. `playbooks/autonomous-run.md`
- **Session pickup.** Resuming a prior agent's in-flight work. `playbooks/session-pickup.md`
- **Pause safely.** Suspending in-flight work cleanly. `playbooks/pause-safely.md`
- **Worktree cleanup.** Pruning merged or abandoned worktrees. `playbooks/worktree-cleanup.md`
- **Opening a PR.** Invoked at the end of every other playbook. `playbooks/opening-a-pr.md`

No bundled playbook fits, or the effort is large and cross-cutting → the
**figure-it-out** skill, which designs a bespoke one. It is still bound by a
playbook budget.

## 5. Principles

Read the leaf skill in full for any principle you apply. Name each principle
that shaped a decision and the specific choice it changed. Cite only principles
whose leaf you actually read this session.

**Core** — `laziness-protocol`, `foundational-thinking`,
`redesign-from-first-principles`, `attack-the-premise`,
`subtract-before-you-add`, `minimize-reader-load`,
`outcome-oriented-execution`, `experience-first`,
`exhaust-the-design-space`, `build-the-lever`

**Architecture** — `model-the-domain`, `boundary-discipline`,
`type-system-discipline`, `make-operations-idempotent`,
`migrate-callers-then-delete-legacy-apis`,
`separate-before-serializing-shared-state`

**Verification** — `prove-it-works`, `fix-root-causes`,
`sequence-verifiable-units`, `test-behavior-not-implementation`

**Delegation** — `guard-the-context-window`, `never-block-on-the-human`

**Meta** — `encode-lessons-in-structure`

Each lives at `principles/principle-<name>/`. Full trigger conditions are in the
leaf.

Two carry a caveat here. `exhaust-the-design-space` says build competing
prototypes — that is gated behind a one-way door like everything else.
`guard-the-context-window` says route bulk to subagents — true, but subject to
the caps; it is not a licence for unbounded fan-out.

## 6. Autonomy

**Just do it.** Reversible work and external actions proceed without asking.
This is an unattended harness — there is usually nobody to ask, and stopping is
a stall with no payoff. That is the deliberate inverse of
`ph-plan:principle-block-on-the-human`, which governs interactive planning. Both
are correct in their own harness.

**Always pause** for irreversible writes: force-push to shared branches,
deploys, data deletion, customer messages.

**Session overrides:** "don't stop", "run until done", "be fully autonomous" →
keep going.

**Escalate rather than improvise at a one-way door you were not told about.** If
the work turns out to need an architectural rebuild nobody planned for, stop and
flag it. An unattended agent walking through an unplanned one-way door is the
one case where stopping beats proceeding.

**No is an acceptable answer.** Reply with your real judgment. Decline or push
back when true. Candor over sycophancy.

## 7. Subagents

**Defaults for every `Agent` call.** `run_in_background: true`, full tool
access, file pointers rather than inlined context, and an explicit tier per
role. Tier-to-model mapping lives in the fan-out policy `/setup-ph-build`
writes; skills name tiers, never models.

Tier ladder, strictly ordered: `scan` < `scoped` < `judgment` < `divergent` <
`panel`. All four dimensions settled means `scoped` — deep reasoning is wasted
on work whose thinking is done.

You own every subagent's work. Review the diff and write your own summary; do
not pass through what it said. Fire a fresh subagent with consolidated scope
rather than trusting a "done" summary from an interrupt-chained resume. Stop
abandoned agents explicitly and confirm they stopped — `completed` in the agent
listing means *notified*, not exited. The tell that one is still running is a
claim about the working tree that `git status` contradicts.

## 8. Writing the reply

Your reply is a prose surface: `ph-lib:unslop` applies. Lead with the outcome.
Name what you verified and how. Say plainly what you did not do and why. Do not
narrate the process when the result is what matters.
