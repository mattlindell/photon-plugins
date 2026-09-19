---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea until the frontier is empty, maintaining the domain model as you go and ending in a spec or tickets. Use when the user wants to stress-test their thinking, sharpen a design, or work out what to build, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question should be formatted like so:

```text
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The *decisions* are the user's — put each to them and wait.

## Keep the domain model current as you go

Run the `domain-modeling` skill throughout, not at the end. When a term is resolved, write it to `CONTEXT.md` in that moment — challenge language that conflicts with the existing glossary, sharpen fuzzy terms into canonical ones, and offer an ADR when a decision is hard to reverse, surprising without context, and the result of a real trade-off.

Do not batch this up. A glossary written after the fact records what you remember; a glossary written inline records what was actually decided, and it catches the disagreements while they are still cheap to resolve.

## Track the four dimensions

Every task carries four axes of uncertainty. Know which one each round is working on, and say so:

| Dimension | The question it answers |
| --- | --- |
| `problem` | What are we solving, and why |
| `shape` | What structure and types it takes |
| `approach` | How it gets built |
| `verification` | How anyone knows it is done |

A dimension is either **settled** or **open**. There is no partial state — "mostly agreed" is open.

Grilling can close any of them, and usually closes `problem`, `shape`, and `approach` on its own. `verification` is normally closed by the `define-done` skill once the other three are settled.

## Close or block — never leave a dimension merely discussed

When a dimension cannot be closed in session, it does not stay open and unowned. It becomes a **decision ticket** declaring `closes: <dimension>`, blocking the work that depends on it:

- Needs a design sketch or module boundary worked out → `closes: shape`, resolved with the `ph-lib:codebase-design` vocabulary
- Needs an empirical answer nobody can reason to → `closes: approach`, resolved by `prototype`
- Needs facts from outside the room → `closes: problem` or `closes: approach`, resolved by `research`

Whoever resolves that ticket updates the blocked tickets when they close it, recording which dimension was decided and with what. Sequence irreversible decisions first — a one-way door is cheapest to walk through while you are still in the room with the person who can change their mind.

## Ending the session

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed.

**Do not act on it until the user confirms you have reached a shared understanding.** On confirmation, the outcome is a written artifact carrying the dimension state — a spec via `to-spec`, tickets via `to-tickets`, or both. Sometimes there is no spec document and the work goes straight to the tracker; that is fine, but something is always written down.

```yaml
settled: [problem, shape]
open: [approach, verification]
```

Whatever `ph-build` picks this up with reads that block to decide how much rigor the work still needs. A session that ends in agreement but writes nothing has not saved anyone any effort — it has only moved the thinking into a transcript nobody will read.
