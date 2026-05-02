# technical-director

A Claude Code plugin for technical direction. It provides seventeen skills covering design exploration, planning, issue triage, TDD, refactoring, codebase architecture, and the meta-tools you need to keep a project's process tight.

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
    caveman/SKILL.md
    design-an-interface/SKILL.md
    domain-model/SKILL.md
    domain-model/ADR-FORMAT.md
    domain-model/CONTEXT-FORMAT.md
    git-guardrails-claude-code/SKILL.md
    git-guardrails-claude-code/scripts/block-dangerous-git.sh
    github-triage/SKILL.md
    github-triage/AGENT-BRIEF.md
    github-triage/OUT-OF-SCOPE.md
    grill-me/SKILL.md
    improve-codebase-architecture/SKILL.md
    improve-codebase-architecture/DEEPENING.md
    improve-codebase-architecture/INTERFACE-DESIGN.md
    improve-codebase-architecture/LANGUAGE.md
    qa/SKILL.md
    request-refactor-plan/SKILL.md
    setup-pre-commit/SKILL.md
    setup-pre-commit/defaults/prettierrc.json
    tdd/SKILL.md
    tdd/deep-modules.md
    tdd/interface-design.md
    tdd/mocking.md
    tdd/refactoring.md
    tdd/tests.md
    to-issues/SKILL.md
    to-prd/SKILL.md
    triage-issue/SKILL.md
    ubiquitous-language/SKILL.md
    write-a-skill/SKILL.md
    zoom-out/SKILL.md
```

---

## Skills

### Engineering

| Skill                             | Description                                                                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **diagnose**                      | Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimize → hypothesize → instrument → fix → regression-test.   |
| **grill-with-docs**               | Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates `CONTEXT.md` and ADRs inline.    |
| **triage**                        | Triage issues through a state machine of triage roles.                                                                                           |
| **improve-codebase-architecture** | Find deepening opportunities in a codebase, informed by `CONTEXT.md` and `docs/adr/`. Surfaces friction and proposes module-deepening refactors. |
| **setup-matt-pocock-skills**      | Scaffold the per-repo config (issue tracker, triage label vocabulary, domain doc layout) that the other engineering skills consume.              |
| **tdd**                           | Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.                              |
| **to-issues**                     | Break any plan, spec, or PRD into independently-grabbable GitHub issues using vertical slices.                                                   |
| **to-prd**                        | Turn the current conversation context into a PRD and submit it as a GitHub issue. No interview - just synthesizes what you've already discussed. |
| **zoom-out**                      | Tell the agent to zoom out and give broader context or a higher-level perspective on an unfamiliar section of code.                              |

### Productivity

| Skill             | Description                                                                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **caveman**       | Ultra-compressed communication mode that drops fillers and pleasantries while keeping full technical accuracy (~75% fewer tokens). |
| **grill-me**      | Get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.                           |
| **write-a-skill** | Create new agent skills with proper structure, progressive disclosure, and bundled resources.                                      |

### Misc

| Skill                          | Description                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **git-guardrails-claude-code** | Install a Claude Code `PreToolUse` hook that blocks dangerous git commands (`push`, `reset --hard`, `clean`, `branch -D`, etc.) before they execute. |
| **setup-pre-commit**           | Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests for JavaScript/TypeScript projects.                               |

### Deprecated

| Skill                     | Description                                                                                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **design-an-interface**   | Generate multiple radically different interface designs for a module using parallel sub-agents, compare them, and synthesize the best approach. ("Design It Twice".) |
| **qa**                    | Interactive QA session: the user reports problems conversationally, the agent clarifies, explores, and files issues using the project's domain language.             |
| **request-refactor-plan** | Plan a refactor through a detailed user interview, then file it as a GitHub issue with a tiny-commits implementation plan.                                           |
| **ubiquitous-language**   | Extract a DDD-style glossary from the current conversation, flag ambiguities, and propose canonical terms. Saves to `UBIQUITOUS_LANGUAGE.md`.                        |

---

## Common Workflows

**Design → PRD → Issues → Build:**

1. **grill-me** or **domain-model** - resolve the design's decision tree (use `domain-model` if the project has `CONTEXT.md` / ADRs)
2. **design-an-interface** - explore multiple module shapes if APIs are in play
3. **to-prd** - synthesize into a PRD work item
4. **to-issues** - break the PRD into vertical-slice work items
5. **tdd** - implement each slice test-first

**Bug → Fix:**

1. **triage-issue** - investigate, find root cause, file a work item with a TDD fix plan
2. **tdd** - implement the fix following the plan

**Inbound issue triage:**

1. **qa** - user reports problems, agent files work items during the session
2. **github-triage** - sort the existing GitHub backlog through the label state machine

**Architecture improvement:**

1. **improve-codebase-architecture** - find deepening opportunities, propose interface designs
2. **request-refactor-plan** - plan the refactor with tiny commits

---

## Issue Tracker

Skills that publish artifacts (PRDs, work items, RFCs) - `to-prd`, `to-issues`, `triage-issue`, `qa`, `request-refactor-plan` - read the project's `CLAUDE.md` for an "Issue Tracker" section to determine where to publish. Supported trackers: GitHub (`gh`), Jira (Atlassian MCP), Beads (`bd`), or local Markdown files. If no configuration is found, the skill asks the user and offers to record the choice in `CLAUDE.md`.

`github-triage` is GitHub-specific and ignores this configuration.

Example `CLAUDE.md` entries:

```markdown
## Issue Tracker

GitHub - use `gh` for all work items. Repo inferred from `git remote`.
```

```markdown
## Issue Tracker

- **Documents (PRDs)**: Confluence via Atlassian MCP - space: PROJ
- **Work items**: Jira via Atlassian MCP - project: PROJ
- Link work items back to their parent Confluence document
```

```markdown
## Issue Tracker

Beads - use `bd create` / `bd ready` / `bd close`. The agent's `bd prime` context covers the full command surface.
```

```markdown
## Issue Tracker

Local - append work items as Markdown files under `./issues/<slug>.md`.
```

---

## Installation

**From the marketplace:**

```bash
/plugin marketplace add mattlindell/photon-plugins
/plugin install technical-director@photon-plugins
```

**For local development:**

```bash
claude --plugin-dir /path/to/plugins/technical-director
```
