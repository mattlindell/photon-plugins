# technical-director

A Claude Code plugin for technical direction. Twenty-two skills shamelessly copied from [Matt Pocock's skill
repository](https://github.com/mattpocock/skills) covering diagnosis, domain modeling, planning, issue triage, TDD,
codebase design and architecture, prototyping, implementation, and the meta-tools that keep a project's process tight —
organized into engineering, productivity, and misc buckets.

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
    engineering/
      README.md
      diagnose/
        SKILL.md
        scripts/hitl-loop.template.sh
      grill-with-docs/
        SKILL.md
        ADR-FORMAT.md
        CONTEXT-FORMAT.md
      improve-codebase-architecture/
        SKILL.md
        DEEPENING.md
        INTERFACE-DESIGN.md
        LANGUAGE.md
      prototype/
        SKILL.md
        LOGIC.md
        UI.md
      setup-matt-pocock-skills/
        SKILL.md
        domain.md
        issue-tracker-github.md
        issue-tracker-gitlab.md
        issue-tracker-local.md
        triage-labels.md
      tdd/
        SKILL.md
        deep-modules.md
        interface-design.md
        mocking.md
        refactoring.md
        tests.md
      to-issues/SKILL.md
      to-prd/SKILL.md
      triage-issue/
        SKILL.md
        AGENT-BRIEF.md
        OUT-OF-SCOPE.md
      zoom-out/SKILL.md
    misc/
      git-guardrails-claude-code/
        SKILL.md
        scripts/block-dangerous-git.sh
      setup-pre-commit/
        SKILL.md
        defaults/prettierrc.json
    productivity/
      README.md
      caveman/SKILL.md
      grill-me/SKILL.md
      handoff/SKILL.md
      write-a-skill/SKILL.md
```

---

## Skills

### Engineering

Skills that comprise the Matt Pocock workflow pattern: design → PRD → issues → TDD → refactor, anchored on `CONTEXT.md` and `docs/adr/`.

| Skill                             | Description                                                                                                                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **diagnose**                      | Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimize → hypothesize → instrument → fix → regression-test.                                                 |
| **grill-with-docs**               | Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates `CONTEXT.md` and ADRs inline.                                                  |
| **improve-codebase-architecture** | Find deepening opportunities in a codebase, informed by `CONTEXT.md` and `docs/adr/`. Surfaces friction and proposes module-deepening refactors.                                               |
| **prototype**                     | Build a throwaway prototype to flesh out a design — either a runnable terminal app for state/business-logic questions, or several radically different UI variations toggleable from one route. |
| **setup-matt-pocock-skills**      | Scaffold the per-repo config (issue tracker, triage label vocabulary, domain doc layout) that the other engineering skills consume.                                                            |
| **tdd**                           | Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.                                                                            |
| **to-issues**                     | Break any plan, spec, or PRD into independently-grabbable work items using vertical slices, with dependencies tracked.                                                                         |
| **to-prd**                        | Turn the current conversation context into a PRD and publish it to the project's issue tracker. No interview - just synthesizes what you've already discussed.                                 |
| **triage-issue**                  | Move issues through a state-machine of triage roles (needs-triage → ready-for-agent / ready-for-human / wontfix), including root-cause investigation and a fix plan.                           |
| **zoom-out**                      | Tell the agent to zoom out and give broader context or a higher-level perspective on an unfamiliar section of code, returning a module map in the project's glossary.                          |

### Productivity

General workflow tools, not code-specific.

| Skill             | Description                                                                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **caveman**       | Ultra-compressed communication mode that drops fillers and pleasantries while keeping full technical accuracy (~75% fewer tokens). |
| **grill-me**      | Get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.                           |
| **handoff**       | Compact the current conversation into a handoff document so another agent can continue the work.                                   |
| **write-a-skill** | Create new agent skills with proper structure, progressive disclosure, and bundled resources.                                      |

### Misc

Repo and tooling guardrails that don't fit the engineering workflow.

| Skill                          | Description                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **git-guardrails-claude-code** | Install a Claude Code `PreToolUse` hook that blocks dangerous git commands (`push`, `reset --hard`, `clean`, `branch -D`, etc.) before they execute. |
| **setup-pre-commit**           | Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests for JavaScript/TypeScript projects.                               |

---

## Common Workflows

**Design → PRD → Issues → Build:**

1. **grill-with-docs** - resolve the design's decision tree against `CONTEXT.md` and ADRs
2. **to-prd** - synthesize the resolved design into a PRD work item
3. **to-issues** - break the PRD into vertical-slice work items
4. **tdd** - implement each slice test-first

**Bug → Fix:**

1. **diagnose** - reproduce, minimize, hypothesize, find root cause
2. **triage-issue** - file the bug with a state-machine label and TDD fix plan
3. **tdd** - implement the fix following the plan

**Onboarding to a new repo:**

1. **setup-matt-pocock-skills** - scaffold `CONTEXT.md`, `docs/adr/`, the issue-tracker config, and triage labels
2. **zoom-out** - get a module map in the project's glossary before touching code

**Architecture improvement:**

1. **improve-codebase-architecture** - find deepening opportunities, propose interface designs
2. **to-issues** - break the proposal into incremental, mergeable refactors
3. **tdd** - land each refactor behind tests

---

## Issue Tracker

Skills that publish artifacts (PRDs, work items, fix plans) - `to-prd`, `to-issues`, `triage-issue`, plus the deprecated
`qa` and `request-refactor-plan` - read the project's `CLAUDE.md` for an "Issue Tracker" section to determine where to
publish. Supported trackers: GitHub (`gh`), GitLab (`glab`), Jira (Atlassian MCP), Beads (`bd`), or local Markdown
files. If no configuration is found, the skill asks the user and offers to record the choice in `CLAUDE.md`. Run
**setup-matt-pocock-skills** to generate the config in one shot.

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
