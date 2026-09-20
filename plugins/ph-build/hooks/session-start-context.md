<EXTREMELY_IMPORTANT>
You have ph-build.

Before writing code for any non-trivial task — a feature, bug fix, refactor,
migration, or performance work — invoke the `ph-build:dispatch` skill and follow
it. Pure questions and trivial one-line edits do not need it.

**Ask first whether the thinking has already been done.** Look for a spec,
ticket, or design doc for this work and read its `settled:` block. A settled
dimension is a decision someone already made — build on it, do not re-derive it.
Re-opening a settled question is the most expensive mistake available here.

- All four dimensions settled → build it directly on the `scoped` tier. No
  exploration phase, no multi-agent panels.
- Nothing settled, and **no spec exists at all** → this work has not been
  planned. Route to `ph-plan:intake` rather than planning it yourself. If nobody
  is available and the change is reversible, take `dispatch`'s single bounded
  orientation pass and proceed.

**The expensive machinery is off by default.** `architect`, `arena`,
`interrogate`, and `swarm` turn on for one reason: the work touches a one-way
door — a schema change, public API surface, data deletion, auth, or billing.
Vague but reversible work just gets built.

Direct entry when the intent is already specific: `ph-build:how` (how a
subsystem works), `ph-build:why` (why it is that way), `ph-build:tdd` (a
reproducible failure), `ph-build:babysit` (drive a PR green).

**ph-build requires ph-lib.** Check that `ph-lib` skills are in your available
skills. If they are not, say so plainly in your first reply and continue
degraded — `ph-lib:unslop` and `ph-lib:codebase-design` are referenced by these
skills and will be missing.

If you were dispatched as a subagent with a **scoped brief** — file paths, a
named change, stated success criteria — ignore this block. The orchestrating
session already applied it when shaping your dispatch, and re-entering the
router would multiply the fan-out it already priced.

If you were handed a **ticket reference** instead, this block applies to you:
you are the entry point, not a delegate inside one.

User instructions (CLAUDE.md, AGENTS.md, direct requests) take precedence.
</EXTREMELY_IMPORTANT>
