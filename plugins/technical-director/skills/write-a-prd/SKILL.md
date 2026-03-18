---
name: write-a-prd
description: Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
---

# Write a PRD

**If the conversation already contains a resolved decision tree from a prior grill-me session**, skip directly to step 4 — the problem, codebase context, and design decisions are already established.

## Process

### 1. Capture the problem

Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

### 2. Explore the codebase

Explore the repo to verify their assertions and understand the current state of the codebase.

### 3. Resolve the decision tree

Invoke the **grill-me** skill to systematically interview the user, resolving each branch of the design's decision tree until all decisions are discrete enough to act on.

### 4. Sketch modules

Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

### 5. Write the PRD

Once you have a complete understanding of the problem and solution, use the template below to write the PRD.

Publish the PRD using the project's configured document tracker (check the project's CLAUDE.md for an "Issue Tracker" section). If no tracker is configured, ask the user where PRDs should be created (e.g., GitHub issue, Confluence page, local markdown file) and suggest they add it to CLAUDE.md for future sessions.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
