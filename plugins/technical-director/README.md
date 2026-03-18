# technical-director

A Claude Code plugin for project management and technical direction. It provides twelve skills covering the full lifecycle from design exploration through implementation planning, issue tracking, and codebase improvement.

**Version:** 1.0.0
**Author:** Matt Lindell
**License:** MIT

---

## Plugin Structure

```text
plugins/technical-director/
  .claude-plugin/
    plugin.json
  skills/
    design-an-interface/SKILL.md
    git-guardrails-claude-code/SKILL.md
    git-guardrails-claude-code/scripts/block-dangerous-git.sh
    grill-me/SKILL.md
    improve-codebase-architecture/SKILL.md
    improve-codebase-architecture/REFERENCE.md
    prd-to-issues/SKILL.md
    prd-to-plan/SKILL.md
    request-refactor-plan/SKILL.md
    setup-pre-commit/SKILL.md
    setup-pre-commit/defaults/prettierrc.json
    tdd/SKILL.md
    tdd/deep-modules.md
    tdd/interface-design.md
    tdd/mocking.md
    tdd/refactoring.md
    tdd/tests.md
    triage-issue/SKILL.md
    ubiquitous-language/SKILL.md
    write-a-prd/SKILL.md
```

---

## Skills

Skills provide structured workflows for planning, design, implementation, and process improvement. They are designed to work with any configured issue tracker (GitHub, Jira, Confluence, local files) — see "Issue Tracker Configuration" below.

### Design & Planning

| Skill                   | Description                                                                                                                                                                                           |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **grill-me**            | Systematically resolve a design's decision tree by interviewing the user, narrowing the design space with each resolved decision until all branches are discrete enough to act on.                    |
| **design-an-interface** | Generate multiple radically different interface designs using parallel sub-agents, compare them, and synthesize the best approach. Based on "Design It Twice" from "A Philosophy of Software Design". |
| **write-a-prd**         | Create a PRD through user interview, codebase exploration, and module design. Cross-references grill-me for the interview phase. Publishes to the project's configured document tracker.              |
| **prd-to-plan**         | Break a PRD into a phased implementation plan using tracer-bullet vertical slices, saved as a local Markdown file in `./plans/`.                                                                      |
| **prd-to-issues**       | Break a PRD into independently-grabbable work items using tracer-bullet vertical slices. Creates work items in the project's configured tracker with dependency ordering.                             |

### Implementation

| Skill                | Description                                                                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **tdd**              | Test-driven development with red-green-refactor workflow. Includes reference documents on good/bad tests, mocking guidelines, deep modules, interface design for testability, and refactoring. |
| **setup-pre-commit** | Set up Husky pre-commit hooks with lint-staged, Prettier, ESLint integration, type checking, and tests for JavaScript/TypeScript projects.                                                     |

### Issue Management

| Skill                     | Description                                                                                                                                                                   |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **triage-issue**          | Investigate a reported bug, find its root cause through codebase exploration, and create a work item with a TDD fix plan. Mostly hands-off — minimizes questions to the user. |
| **request-refactor-plan** | Plan a refactor through detailed user interview, then create a work item with a tiny-commits implementation plan.                                                             |

### Architecture & Process

| Skill                             | Description                                                                                                                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **improve-codebase-architecture** | Explore a codebase to surface architectural friction, propose module-deepening refactors using parallel sub-agent interface designs, and create RFC work items.                        |
| **ubiquitous-language**           | Extract a DDD-style ubiquitous language glossary from conversation, flagging ambiguities and proposing canonical terms. Saves to `UBIQUITOUS_LANGUAGE.md`.                             |
| **git-guardrails-claude-code**    | Set up a Claude Code hook that blocks dangerous git commands (push, reset --hard, clean, branch -D) before they execute. Includes a bundled script for project or global installation. |

---

## Issue Tracker Configuration

Several skills create external artifacts (PRDs, work items, RFCs). These skills check the project's `CLAUDE.md` for an "Issue Tracker" section to determine where to publish. If no tracker is configured, the skill will ask and suggest adding the preference to `CLAUDE.md`.

Example `CLAUDE.md` configuration:

```markdown
## Issue Tracker

- **Documents (PRDs)**: Confluence via Atlassian Cloud MCP — space: PROJ
- **Work items**: Jira via Atlassian Cloud MCP — project: PROJ
- Link work items back to their parent Confluence document
```

Or for GitHub-only projects:

```markdown
## Issue Tracker

GitHub — use `gh issue create` for all issues and PRDs.
```

---

## Common Workflows

**Design → Plan → Build:**

1. **grill-me** — resolve the design's decision tree
2. **write-a-prd** — formalize into a PRD (skips interview if grill-me already ran)
3. **prd-to-plan** or **prd-to-issues** — break into phases or work items
4. **tdd** — implement each slice test-first

**Bug → Fix:**

1. **triage-issue** — investigate, find root cause, create work item with TDD fix plan
2. **tdd** — implement the fix following the plan

**Architecture improvement:**

1. **improve-codebase-architecture** — explore, find friction, design interfaces, create RFC
2. **request-refactor-plan** — plan the refactor with tiny commits

---

## Installation

**From a plugin marketplace:**

```bash
claude plugin install technical-director
```

**For local development (point to the plugin directory):**

```bash
claude --plugin-dir /path/to/plugins/technical-director
```
