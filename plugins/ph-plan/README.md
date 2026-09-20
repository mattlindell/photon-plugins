# ph-plan

**Middle-down planning** — deciding and writing down the specifics of something
that will be coded. Thirteen skills and six principles.

This is the hat you wear when you are the person who decides what gets built.
Its counterpart, `ph-build`, is the hat anyone wears to build it.

**Requires [`ph-lib`](../ph-lib/).**

## The harness is the seam

`ph-plan` is **interactive**. A human is present, and their judgment is the
cheapest way to resolve an ambiguity — so these skills ask, and wait.

`ph-build` is **unattended**. Nobody is there, so blocking to ask is a stall with
no payoff — those skills proceed and let you course-correct on review.

Rules that look contradictory across the two plugins are usually the same rule,
correctly inverted for its harness. `ph-plan:principle-block-on-the-human` and
`ph-build:principle-never-block-on-the-human` are the clearest pair.

## The four dimensions

Every task carries four axes of uncertainty. Each is **settled** or **open** —
there is no partial state.

| Dimension | The question it answers | Usually closed by |
| --- | --- | --- |
| `problem` | What are we solving, and why | `triage`, `grilling`, `to-spec` |
| `shape` | What structure and types it takes | `grilling`, `ph-lib:codebase-design` |
| `approach` | How it gets built | `grilling`, `prototype`, `research` |
| `verification` | How anyone knows it is done | `define-done` |

Planning writes the result onto the spec or ticket as a fenced block:

```yaml
settled: [problem, shape, approach]
open: [verification]
```

That block is the **rigor signal**. `ph-build` reads it to decide how much effort
the work still needs — which is the whole point of the split. Work that arrived
already thought through should cost less to execute than work that arrived vague.
Overstating it means a builder skips a question nobody answered, so be honest.

A dimension that cannot be closed in session does not stay open and unowned. It
becomes a **decision ticket** declaring `closes: <dimension>`, blocking the work
that depends on it. Whoever resolves it updates the blocked tickets on close.

## Skills

Entry point: **`intake`** — the only model-invocable router here. It makes one
binary decision and hands off.

| Skill | Invocation | What it does |
| --- | --- | --- |
| `intake` | model | Entry point for work that does not exist yet. Routes to `grilling` or `scout` |
| `grilling` | model | Relentless interview over a design tree, in rounds, until the frontier is empty. Maintains the domain model inline and ends in a spec or tickets |
| `scout` | user | Map an effort too big for one session as decision tickets on the tracker, resolved one at a time |
| `domain-modeling` | model | Build and sharpen the glossary and ADRs |
| `prototype` | model | Throwaway artifact to answer a design question. Closes `approach` |
| `research` | model | Investigate against primary sources, capture findings in the repo |
| `improve-codebase-architecture` | user | Scan for deepening opportunities, report, grill through them |
| `triage` | user | Move issues and external PRs through the triage state machine. Closes `problem` |
| `to-spec` | user | Turn the conversation into a spec on the tracker |
| `to-tickets` | user | Break a plan into tracer-bullet tickets with blocking edges |
| `define-done` | user | Decide one verification methodology and attach it to every ticket in the set |
| `to-questionnaire` | user | Turn a decision you cannot answer into a questionnaire for someone else |
| `setup-ph-plan` | user | Configure a repo: issue tracker, triage labels, doc layout |

## Principles (6)

Leaf skills — the model reads them, they never appear in your slash menu. The
deliberate inverse of `ph-build`'s set.

- `block-on-the-human` — the person in front of you is the cheapest resolver
- `walk-the-tree` — ask the whole frontier at once; never guess past an unasked question
- `close-or-block-the-dimension` — settled or ticketed, never merely discussed
- `write-it-down` — a decision that was not recorded did not happen
- `name-the-destination` — know what done looks like before decomposing
- `one-way-doors-first` — settle irreversible decisions while changing your mind is cheap

## Structure

```text
ph-plan/
  .claude-plugin/plugin.json
  skills/
    <13 skills>
    principles/           — 6 leaf skills
```

## Setup

Run `/ph-plan:setup-ph-plan` once per repo. It configures the issue tracker, the
triage label vocabulary, and the domain-doc layout that `to-spec`, `to-tickets`,
`triage`, and `scout` all read.
