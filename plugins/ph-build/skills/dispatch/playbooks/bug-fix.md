### Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix to subagents, stay in the lead.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix; it does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

Before the fan-out in steps 2-3, check the [focused-fix exception](#focused-fix-exception). Select known non-sensitive fields before printing diagnostic configuration or service responses; do not dump whole configurations or environments.

1. Reproduce it yourself on the matching surface via the driver skill (`run` for CLIs/TUIs, `verify` for UIs) (Non-negotiables). Don't hand the repro to the user. A debug or instrumentation protocol that says to ask the user does not override this; you drive the instrumented runtime. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. Won't reproduce directly, force it: synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with a trace of the affected subsystem and the **why** skill for regression history. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt with Claude Code's `loop` command. Confirm the surviving *mechanism* with runtime evidence before step 3 plans the fix.
3. Plan the fix. If it crosses a function boundary, name the shape first with `ph-lib:codebase-design`. At a one-way door the spec left open, stop per `dispatch`'s gate. Delegate implementation to a subagent using the tier the fan-out policy maps `bug-fix` to (see `dispatch`, Tiers) with a specific scope; review the diff.
4. Verify on the same surface; the original repro now passes. "Inconclusive" or wrong-surface is not a pass; flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history. See the **tdd** skill for the failing-test-first cadence when the bug has a cheap local test path; skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical **sequence-verifiable-units** principle skill, the failing test first and the fix on top.
6. Run **Opening a PR**.

Investigation fans out `how` + `why` as parallel subagents.

For any bug fix, stop at step 3 per `dispatch`'s gate before implementing changes to interfaces, ownership, schema, migration behavior, concurrency or transaction guarantees, or deployment or routing contracts, even within one function, unless the spec settled the decision. Before marking the fix merge-ready, require an independent correctness reviewer for changes to code that enforces a security or data-integrity invariant, including an atomic eligibility guard, even when the fix preserves that invariant. Follow the closed-review-gate rule in `dispatch`'s Subagents section if a reviewer cannot run.

**Reply:** what was broken, root cause, fix, how you verified. Quote the decisive failing and passing output, trimmed to the assertion and the counts.

When publication or deployment is part of the task, also state what code was fixed and verified, what was published, what version and behavior the affected runtime actually served (through the authenticated path when relevant), and any blocker with the next action needed to resolve it. Missing or contradictory runtime evidence leaves the incident unresolved, even after a successful publication. Remove credentials and customer data from quoted evidence.

#### Focused-fix exception

One scoped bug-fix delegate may investigate the reproduced failure with a focused code and local-history read before invoking `how` or `why`. Skip those skills and step 3's `ph-lib:codebase-design` shape pass, even across a function boundary, only when all of these hold:

- Runtime evidence establishes the cause in one subsystem.
- The correction preserves interfaces and state semantics, with no signature, ownership, schema, migration, security, concurrency, transaction, or deployment/routing change. Security changes include authentication, authorization, cryptography, and secret handling.
- A cheap regression check exercises the failure under the relevant runtime settings, and verification on the original surface is available.
- No competing design or contradictory evidence remains.

Record the evidence for these conditions in the existing checklist before the skip. The delegate implements the scoped fix; the lead still plans, reviews the diff, and verifies it. If any condition is false or remains unknown after the focused pass, or later evidence invalidates it, return to steps 2-3 without the exception. Every other step and any required independent review remain in force. Patch size alone never qualifies a fix.
