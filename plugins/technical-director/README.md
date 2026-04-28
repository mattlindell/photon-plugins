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

### Design & Exploration

| Skill                   | Description                                                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **grill-me**            | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree.                                      |
| **domain-model**        | Grilling session that challenges a plan against the existing domain model, sharpens terminology, and updates `CONTEXT.md` / ADRs inline as decisions crystallise.            |
| **design-an-interface** | Generate multiple radically different interface designs for a module using parallel sub-agents, compare them, and synthesise the best approach. ("Design It Twice".)         |
| **zoom-out**            | Ask the agent to step up a layer of abstraction and produce a map of relevant modules and callers when working in unfamiliar code.                                           |
| **ubiquitous-language** | Extract a DDD-style glossary from the current conversation, flag ambiguities, and propose canonical terms. Saves to `UBIQUITOUS_LANGUAGE.md`.                                |
| **caveman**             | Ultra-compressed communication mode that drops fillers and pleasantries while keeping full technical accuracy (~75% fewer tokens).                                           |

### Planning & Issue Management

| Skill                     | Description                                                                                                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **to-prd**                | Synthesise the current conversation and codebase context into a PRD and submit it as a GitHub issue. No interview — uses what the agent already knows.                  |
| **to-issues**             | Break a plan, spec, or PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices, ordered by dependency.                                        |
| **triage-issue**          | Investigate a reported bug, find its root cause through codebase exploration, and create a GitHub issue with a TDD fix plan. Mostly hands-off.                           |
| **github-triage**         | Triage *existing* GitHub issues through a label-based state machine — sort incoming bugs/feature requests and prepare them for an AFK agent.                             |
| **qa**                    | Interactive QA session: the user reports problems conversationally, the agent clarifies, explores, and files issues using the project's domain language.                 |
| **request-refactor-plan** | Plan a refactor through a detailed user interview, then file it as a GitHub issue with a tiny-commits implementation plan.                                               |

### Implementation

| Skill                          | Description                                                                                                                                                                 |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **tdd**                        | Red-green-refactor workflow with reference docs on good/bad tests, mocking, deep modules, interface design for testability, and refactoring.                                |
| **setup-pre-commit**           | Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests for JavaScript/TypeScript projects.                                                      |
| **git-guardrails-claude-code** | Install a Claude Code `PreToolUse` hook that blocks dangerous git commands (`push`, `reset --hard`, `clean`, `branch -D`, etc.) before they execute.                        |

### Architecture & Meta

| Skill                             | Description                                                                                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **improve-codebase-architecture** | Find deepening opportunities in a codebase, informed by `CONTEXT.md` and `docs/adr/`. Surfaces friction and proposes module-deepening refactors.                         |
| **write-a-skill**                 | Create new agent skills with proper structure, progressive disclosure, and bundled resources.                                                                            |

---

## Common Workflows

**Design → PRD → Issues → Build:**

1. **grill-me** or **domain-model** — resolve the design's decision tree (use `domain-model` if the project has `CONTEXT.md` / ADRs)
2. **design-an-interface** — explore multiple module shapes if APIs are in play
3. **to-prd** — synthesise into a PRD GitHub issue
4. **to-issues** — break the PRD into vertical-slice issues
5. **tdd** — implement each slice test-first

**Bug → Fix:**

1. **triage-issue** — investigate, find root cause, create issue with TDD fix plan
2. **tdd** — implement the fix following the plan

**Inbound issue triage:**

1. **qa** — user reports problems, agent files issues during the session
2. **github-triage** — sort the existing backlog through the label state machine

**Architecture improvement:**

1. **improve-codebase-architecture** — find deepening opportunities, propose interface designs
2. **request-refactor-plan** — plan the refactor with tiny commits

---

## Issue Tracker

Skills that publish artifacts (PRDs, issues, RFCs) target GitHub by default and use `gh` for all operations. The repo is inferred from `git remote`.

If a project uses a different tracker, add an "Issue Tracker" section to the project's `CLAUDE.md` and the skills will adapt:

```markdown
## Issue Tracker

- **Documents (PRDs)**: Confluence via Atlassian Cloud MCP — space: PROJ
- **Work items**: Jira via Atlassian Cloud MCP — project: PROJ
- Link work items back to their parent Confluence document
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
