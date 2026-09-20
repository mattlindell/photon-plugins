---
name: intake
description: Entry point for work that does not exist yet. Use when the user describes something they want to build, floats an idea, brings a rough or half-formed spec, or asks where to start — before any planning or implementation begins.
---

# Intake

New work enters here. Your only job is one branch, then hand off.

**Is the frontier mapped?** That is: does the user know what the open questions
*are*, even if they lack the answers?

| | Route to | Because |
| --- | --- | --- |
| **Yes** — the unknowns are nameable, the work fits a session or two | `grilling` | Walk the design tree, close the dimensions, end in a spec or tickets |
| **No** — fog of war, more than one session holds, unknowns not yet enumerable | `scout` | Map the frontier onto a tracker first as decision tickets, resolve them one at a time |

Ask the user which it is only when you genuinely cannot tell. The tells for
`scout` are scale ("rewrite", "migrate", "the whole X"), a stated inability to
see the end, or a request that decomposes into questions you cannot yet list.
Everything else is `grilling`.

Both routes end the same way: a written artifact carrying a `settled:` block.
Neither route writes code.

## Not this skill

- Work that **already exists** as an issue or PR → `triage`, which the human
  invokes deliberately.
- Work that is **already specified** and just needs building → `ph-build`, not
  here. Check for a spec with a `settled:` block before assuming otherwise.
- A question about how existing code works → `ph-build:how`, or `ph-build:why`
  for why it is that way. Intake is for work, not for understanding.
