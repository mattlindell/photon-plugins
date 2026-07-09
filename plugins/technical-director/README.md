# technical-director

A Claude Code plugin for technical direction. Twenty-five skills shamelessly copied from [Matt Pocock's skill
repository](https://github.com/mattpocock/skills) covering diagnosis, domain modeling, planning, issue triage, TDD,
codebase design and architecture, prototyping, implementation, and the meta-tools that keep a project's process tight —
organized into engineering, productivity, and misc buckets.

**Version:** 3.0.0
**Author:** Matt Lindell
**License:** MIT

---

## Plugin Structure

```text
plugins/technical-director/
  .claude-plugin/
    plugin.json
  README.md
  skills/
    engineering/
      README.md
      ask-matt/SKILL.md
      code-review/SKILL.md
      codebase-design/
        SKILL.md
        DEEPENING.md
        DESIGN-IT-TWICE.md
      diagnosing-bugs/
        SKILL.md
        scripts/hitl-loop.template.sh
      domain-modeling/
        SKILL.md
        ADR-FORMAT.md
        CONTEXT-FORMAT.md
      grill-with-docs/SKILL.md
      implement/SKILL.md
      improve-codebase-architecture/
        SKILL.md
        HTML-REPORT.md
      prototype/
        SKILL.md
        LOGIC.md
        UI.md
      research/SKILL.md
      resolve-merge-conflicts/SKILL.md
      setup-matt-pocock-skills/
        SKILL.md
        domain.md
        issue-tracker-github.md
        issue-tracker-gitlab.md
        issue-tracker-local.md
        triage-labels.md
      tdd/
        SKILL.md
        mocking.md
        tests.md
      to-spec/SKILL.md
      to-tickets/SKILL.md
      triage/
        SKILL.md
        AGENT-BRIEF.md
        OUT-OF-SCOPE.md
      wayfinder/SKILL.md
    productivity/
      README.md
      caveman/SKILL.md
      grill-me/SKILL.md
      grilling/SKILL.md
      handoff/SKILL.md
      teach/
        SKILL.md
        GLOSSARY-FORMAT.md
        LEARNING-RECORD-FORMAT.md
        MISSION-FORMAT.md
        RESOURCES-FORMAT.md
      writing-great-skills/
        SKILL.md
        GLOSSARY.md
    misc/
      README.md
      git-guardrails-claude-code/
        SKILL.md
        scripts/block-dangerous-git.sh
      setup-pre-commit/
        SKILL.md
        defaults/prettierrc.json
```

---

## Skills

### Engineering

The Matt Pocock workflow pattern — design → spec → tickets → implement → refactor, anchored on `CONTEXT.md` and `docs/adr/`. Skills marked **(user)** are user-invoked only (`disable-model-invocation: true`); the rest carry trigger phrasing so the model can reach for them on its own.

| Skill                                 | Description                                                                                                                                          |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ask-matt** _(user)_                 | A router over the skills — ask which skill or flow fits your situation and it maps the path.                                                         |
| **grill-with-docs** _(user)_          | Grilling session that also builds the domain model — sharpens terminology and updates `CONTEXT.md` and ADRs as decisions crystallize.                |
| **improve-codebase-architecture** _(user)_ | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.                   |
| **setup-matt-pocock-skills** _(user)_ | Scaffold the per-repo config (issue tracker, triage labels, domain doc layout) the other engineering skills consume. Run once per repo.             |
| **to-spec** _(user)_                  | Turn the current conversation into a spec and publish it to the issue tracker — no interview, just synthesis of what you've already discussed.        |
| **to-tickets** _(user)_               | Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges — as text in a local file, or native blocking links on a real tracker. |
| **implement** _(user)_                | Implement a piece of work from a spec or set of tickets, leaning on `tdd` at pre-agreed seams, then reviewing the result.                            |
| **wayfinder** _(user)_                | Plan a huge chunk of work — more than one agent session can hold — as a shared map of investigation tickets, resolved one at a time until the way to the destination is clear. |
| **triage** _(user)_                   | Move issues and external PRs through a state machine of triage roles — categorize, verify, grill if needed, and write agent-ready briefs.            |
| **prototype**                         | Build a throwaway prototype — a runnable terminal app for state/business-logic questions, or several radically different UI variations on one route. |
| **diagnosing-bugs**                   | Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimize → hypothesize → instrument → fix → regression-test.       |
| **research**                          | Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.  |
| **tdd**                               | Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.                                  |
| **domain-modeling**                   | Actively build and sharpen a project's domain model — challenge terms, stress-test with scenarios, write the glossary and ADRs inline.              |
| **codebase-design**                   | Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.                          |
| **code-review**                       | Two-axis review of the diff since a fixed point — Standards (repo coding standards plus a Fowler smell baseline) and Spec (faithful to the originating spec or ticket?) — run as parallel sub-agents. |
| **resolve-merge-conflicts**           | Resolve an in-progress git merge/rebase conflict by tracing each change to its original intent, then running the project's checks.                   |

### Productivity

General workflow tools, not code-specific. **(user)** marks user-invoked-only skills.

| Skill                            | Description                                                                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **grill-me** _(user)_            | Get relentlessly interviewed about a plan or design — the stateless sibling of `grill-with-docs`, for plans that don't live in a repo. |
| **handoff** _(user)_             | Compact the current conversation into a handoff document so another agent can continue the work.                                  |
| **teach** _(user)_               | Learn a concept over multiple sessions, using the current directory as a stateful workspace.                                       |
| **writing-great-skills** _(user)_ | Reference for writing and editing skills well: the vocabulary and principles that make a skill predictable.                       |
| **caveman**                      | Ultra-compressed communication mode that drops filler and pleasantries while keeping full technical accuracy (~75% fewer tokens).  |
| **grilling**                     | Interview the user relentlessly about a plan or design, resolving each branch of the decision tree one question at a time.         |

### Misc

Repo and tooling guardrails that don't fit the engineering workflow.

| Skill                          | Description                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **git-guardrails-claude-code** | Install a Claude Code `PreToolUse` hook that blocks dangerous git commands (`push`, `reset --hard`, `clean`, `branch -D`, etc.) before they execute. |
| **setup-pre-commit**           | Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests for JavaScript/TypeScript projects.                               |

---

## Common Workflows

**Not sure where to start?** Run **ask-matt** — a router that walks you to the skill or flow that fits your situation.

**Idea → ship (the main flow):**

1. **grill-with-docs** - sharpen the idea by interview against `CONTEXT.md` and ADRs
2. **to-spec** - synthesize the resolved design into a spec work item
3. **to-tickets** - break the spec into a set of tracer-bullet tickets, each declaring its blocking edges
4. **implement** - build each ticket (fresh session per ticket), leaning on **tdd** at pre-agreed seams

**Bug → fix:**

1. **diagnosing-bugs** - reproduce, minimize, hypothesize, find root cause
2. **triage** - route the bug through the state machine and write an agent-ready brief
3. **tdd** - implement the fix test-first

**Architecture improvement:**

1. **improve-codebase-architecture** - find deepening opportunities, pick one, grill it
2. **codebase-design** - apply the deep-module vocabulary to the chosen refactor
3. **to-tickets** → **implement** - land each refactor incrementally, behind tests

---

## Issue Tracker

Skills that publish artifacts (specs, work items, fix plans) - `to-spec`, `to-tickets`, `wayfinder`, and `triage` -
read the project's `CLAUDE.md` for an "Issue Tracker" section to determine where to
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
