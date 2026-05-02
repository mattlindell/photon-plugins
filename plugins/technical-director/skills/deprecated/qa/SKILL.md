---
name: qa
description: Interactive QA session where the user reports several bugs or issues conversationally and the agent files a work item for each in the project's configured tracker (GitHub, Jira, beads, or local), exploring the codebase in the background for context and domain language. Use when user wants to do a QA pass, report multiple bugs in one session, file issues conversationally, or mentions "QA session". For a single bug with full root-cause investigation, use triage-issue.
---

# QA Session

Run an interactive QA session. The user describes problems they're encountering. You clarify, explore the codebase for context, and file work items in the project's configured tracker that are durable, user-focused, and use the project's domain language.

## Tracker Resolution

Read the project's `CLAUDE.md` for an "Issue Tracker" section to determine where to publish. Common configurations:

| Tracker | How to publish |
| --- | --- |
| GitHub | `gh issue create --title "..." --body "..."` |
| Jira | Atlassian MCP - use the project key from `CLAUDE.md` |
| Beads | `bd create` - see the agent's `bd prime` context for the full command surface |
| Local | Append a Markdown file under the path specified in `CLAUDE.md` (e.g. `./issues/<slug>.md`) |

If no tracker is configured, ask the user which to use at the start of the session, then offer to record the choice in `CLAUDE.md`.

## For each issue the user raises

### 1. Listen and lightly clarify

Let the user describe the problem in their own words. Ask **at most 2-3 short clarifying questions** focused on:

- What they expected vs what actually happened
- Steps to reproduce (if not obvious)
- Whether it's consistent or intermittent

Do NOT over-interview. If the description is clear enough to file, move on.

### 2. Explore the codebase in the background

While talking to the user, kick off an Agent (subagent_type=Explore) in the background to understand the relevant area. The goal is NOT to find a fix - it's to:

- Learn the domain language used in that area (check UBIQUITOUS_LANGUAGE.md)
- Understand what the feature is supposed to do
- Identify the user-facing behavior boundary

This context helps you write a better issue - but the issue itself should NOT reference specific files, line numbers, or internal implementation details.

### 3. Assess scope: single item or breakdown?

Before filing, decide whether this is a **single work item** or needs to be **broken down** into multiple items.

Break down when:

- The fix spans multiple independent areas (e.g. "the form validation is wrong AND the success message is missing AND the redirect is broken")
- There are clearly separable concerns that different people could work on in parallel
- The user describes something that has multiple distinct failure modes or symptoms

Keep as a single item when:

- It's one behavior that's wrong in one place
- The symptoms are all caused by the same root behavior

### 4. File the work item(s)

File work items using the configured tracker's tooling (see Tracker Resolution above). Do NOT ask the user to review first - just file and share URLs/IDs.

Work items must be **durable** - they should still make sense after major refactors. Write from the user's perspective.

#### For a single item

Use this template:

```
## What happened

[Describe the actual behavior the user experienced, in plain language]

## What I expected

[Describe the expected behavior]

## Steps to reproduce

1. [Concrete, numbered steps a developer can follow]
2. [Use domain terms from the codebase, not internal module names]
3. [Include relevant inputs, flags, or configuration]

## Additional context

[Any extra observations from the user or from codebase exploration that help frame the issue - e.g. "this only happens when using the Docker layer, not the filesystem layer" - use domain language but don't cite files]
```

#### For a breakdown (multiple items)

Create items in dependency order (blockers first) so you can reference real IDs.

Use this template for each sub-item:

```text
## Parent

`<parent-id>` (if you created a tracking item) or "Reported during QA session"

## What's wrong

[Describe this specific behavior problem - just this slice, not the whole report]

## What I expected

[Expected behavior for this specific slice]

## Steps to reproduce

1. [Steps specific to THIS issue]

## Blocked by

- `<work-item-id>` (if this item can't be fixed until another is resolved)

Or "None - can start immediately" if no blockers.

## Additional context

[Any extra observations relevant to this slice]
```

When creating a breakdown:

- **Prefer many thin items over few thick ones** - each should be independently fixable and verifiable
- **Mark blocking relationships honestly** - if item B genuinely can't be tested until item A is fixed, say so. If they're independent, mark both as "None - can start immediately"
- **Create items in dependency order** so you can reference real IDs in "Blocked by"
- **Maximize parallelism** - the goal is that multiple people (or agents) can grab different items simultaneously

#### Rules for all item bodies

- **No file paths or line numbers** - these go stale
- **Use the project's domain language** (check UBIQUITOUS_LANGUAGE.md if it exists)
- **Describe behaviors, not code** - "the sync service fails to apply the patch" not "applyPatch() throws on line 42"
- **Reproduction steps are mandatory** - if you can't determine them, ask the user
- **Keep it concise** - a developer should be able to read the item in 30 seconds

After filing, print all work item URLs/IDs (with blocking relationships summarized) and ask: "Next issue, or are we done?"

### 5. Continue the session

Keep going until the user says they're done. Each item is independent - don't batch them.
