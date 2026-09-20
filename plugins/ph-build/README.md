# ph-build

**Unattended implementation** — building what was decided, at a cost that tracks
what is still unknown. 32 skills, 23 principles, 19 playbooks, 3 agents.

Its counterpart, [`ph-plan`](../ph-plan/), is the hat you wear when deciding
*what* gets built. **Requires [`ph-lib`](../ph-lib/).**

Forked from [pstack](https://github.com/michael-denyer/pstack-claude) — see
[NOTICE.md](NOTICE.md).

## The problem this solves

pstack is excellent at rigor and has no concept of work that was *already
thought through*. Its only escape hatches key on task **triviality**; nothing
reads a spec and concludes the question is settled. So a fully specified feature
ran the `feature` playbook at 20–36 agents and burned a five-hour token
allotment on thinking a human had already done.

The fix is two mechanisms, not one:

1. **A rigor signal.** `ph-plan` writes which dimensions it closed; `dispatch`
   reads it and skips the phases that own them.
2. **A gate.** Expensive multi-agent work is off by default and turns on for
   one-way doors, not for uncertainty.

Caps bound the worst case. The gate makes the common case cheap. Both are
needed.

## The rigor signal

Every spec or ticket carries which of the four dimensions are closed:

```yaml
settled: [problem, shape, approach]
open: [verification]
```

| State | What `dispatch` does |
| --- | --- |
| All four settled | Build it. `scoped` tier, no panels, no exploration |
| Some settled | Skip the phases owning those dimensions |
| None settled | One bounded orientation pass, then proceed |
| No spec at all | Route to `ph-plan:intake` |

**A settled dimension is a decision already made.** Re-deriving one is the most
expensive mistake available here.

## The gate

`architect`, `arena`, `interrogate`, and `swarm` are **off by default**. They
turn on when the work touches a **one-way door**: a schema change, public API
surface, irreversible data handling, auth, or billing.

Vague but reversible work just gets built — you course-correct on review, which
is cheaper than a panel.

## Tiers and caps

One strict effort ladder, no ties:

`scan` < `scoped` < `judgment` < `divergent` < `panel`

**Skills name tiers, never models.** The tier-to-model mapping is per-harness
and lives in the fan-out policy `/ph-build:setup-ph-build` writes — one file
holding tiers, per-skill caps, and per-playbook budgets, so "what will this cost
me" is one read rather than nine.

All four dimensions settled means `scoped`. Deep reasoning is wasted on work
whose thinking is done.

| Skill | Tier | Cap |
| --- | --- | --- |
| `architect` | `divergent` | 3 runners |
| `arena` | `divergent` | 3 candidates + 1 judge |
| `interrogate` | `panel` | 3 reviewers |
| `swarm` | `scoped` | 6 workers |
| `how` | `scan` | 3 explorers + 1 explainer |
| `why` | `scan` | 4 investigators + 1 synthesizer |
| `maintain-verification-skill` | `scan` | 5 readers |

Per-skill caps do not bound nesting — `architect` runs `how`, `why`, and `arena`
inside itself. That is what the **playbook budgets** are for.

## Entry points

**`dispatch`** is the router, and the `SessionStart` hook points at it. It reads
the rigor signal, applies the gate, and routes to one of 19 playbooks. Type
`/ph-build:dispatch` to enter it by hand; the `implement` agent enters the same
router when a connector hands over a ticket. Work that arrives as a bare tracker
reference passes through the **Implement a ticket** entry adapter first, which
resolves the ticket and picks the playbook.

One method, every entry point. The three surfaces above used to be three
documents that disagreed — see
[ADR-0003](../../docs/adr/0003-agents-are-connector-wrappers-not-method-holders.md).

Direct entry when the intent is specific: `how`, `why`, `tdd`, `babysit`.

The six expensive skills are **user-invoked only** — `architect`, `arena`,
`interrogate`, `swarm`, `thermo-nuclear-code-quality-review`,
`maintain-verification-skill`. Capability kept; auto-invocation removed, because
every upstream skill being model-invocable is why the machinery fired unprompted.

## Agents

Each one is a wrapper: it names the entry condition and points at the skill that
holds the method.

- `implement` — a ticket handed over with no further instruction; enters
  `dispatch`
- `code-review` — a PR or branch reviewed against repo standards and the
  originating spec
- `comment-sicko` — invoked by `no-comments`

## Autonomy

This plugin assumes **nobody is watching**. Reversible work proceeds without
asking; blocking to ask is a stall with no payoff. That is the deliberate
inverse of `ph-plan:principle-block-on-the-human`, and both are correct in their
own harness.

The exception: an **unplanned one-way door**. An unattended agent that discovers
the work needs an architectural rebuild stops and flags it rather than
improvising through.

## Structure

```text
ph-build/
  .claude-plugin/plugin.json
  NOTICE.md                     — upstream attribution
  hooks/                        — SessionStart, points at dispatch
  agents/                       — implement, code-review, comment-sicko
  skills/
    dispatch/
      playbooks/                — 19, plus the implement-a-ticket entry adapter
      references/               — bugbot triage
      scripts/                  — watch-pr, worktree-audit
    <31 skills>
    principles/                 — 23 leaf skills
```

## Setup

Run `/ph-build:setup-ph-build` once per machine. It detects the harness,
proposes a tier-to-model mapping for you to confirm, and writes the fan-out
policy.
