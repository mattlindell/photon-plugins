---
name: grill-me
description: Use when user wants to stress-test a plan, get grilled on their design, validate decisions, or mentions "grill me".
---

# Grill Me

Systematically resolve a design's decision tree. Each decision narrows the remaining design space, constraining what comes next, until all branches reach decisions discrete enough to act on.

## Process

1. **Identify the root decision** — what is the broadest, most constraining choice that hasn't been made yet? Start there.

2. **Resolve one branch at a time** — ask the user to commit to a decision. Once made, explicitly state what that decision constrains or eliminates before moving to the next branch.

3. **Explore the codebase instead of asking** — if a question can be answered by reading code, config, or existing patterns, investigate first. Only ask the user about things that require judgment or domain knowledge.

4. **Push past vague answers** — if the user says "it depends" or "I'm not sure", propose 2-3 concrete options with trade-offs and ask them to pick. If they genuinely can't decide, flag it as an open question and move to a branch that doesn't depend on it.

5. **Stop when branches are discrete** — a branch is resolved when the remaining decisions are implementation details that don't require design judgment. You're done when all branches reach this point.

## After the interview

Summarize the resolved decision tree: list each decision made, what it constrained, and any flagged open questions that still need resolution.

## Next steps

After completing the interview, the user will typically want to convert the resolved decisions into actionable work. Suggest progressing to either **prd-to-issues** (to create work items) or **prd-to-plan** (to create a local implementation plan).
