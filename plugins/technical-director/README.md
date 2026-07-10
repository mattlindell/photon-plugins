# technical-director

A Claude Code plugin for technical direction and engineering leadership. Forty-six skills across two halves:

- **Engineering workflow** — twenty-two skills shamelessly copied from [Matt Pocock's skill
  repository](https://github.com/mattpocock/skills) covering diagnosis, domain modeling, planning, issue triage, TDD,
  codebase design and architecture, prototyping, implementation, and the meta-tools that keep a project's process tight —
  organized into engineering, productivity, and misc buckets.
- **Leadership** — twenty-four skills for managing a team and working across an organization: 1:1s, difficult
  conversations, delegation, managing up, cross-functional collaboration, decisions, timelines, meetings, culture, and
  org design. Six fire on their own; the rest are user-invoked and reachable through the `leadership` router. Adapted
  from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled from Lenny's Podcast — since
  substantially rewritten.

**Version:** 3.1.0
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
        refactoring.md
        tests.md
      to-issues/SKILL.md
      to-prd/SKILL.md
      triage/
        SKILL.md
        AGENT-BRIEF.md
        OUT-OF-SCOPE.md
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
    leadership/
      README.md
      leadership/SKILL.md               # the router (SKILL.md only)
      # each skill below: SKILL.md + references/{INTAKE,WORKFLOW,TEMPLATES,CHECKLISTS,RUBRIC}.md
      building-team-culture/
      coaching-pms/
      cross-functional-collaboration/
      delegating-work/
      energy-management/
      engineering-culture/
      evaluating-trade-offs/
      having-difficult-conversations/
      managing-timelines/
      managing-up/
      organizational-design/
      organizational-transformation/
      planning-under-uncertainty/
      post-mortems-retrospectives/
      running-decision-processes/
      running-design-reviews/
      running-effective-1-1s/
      running-effective-meetings/
      running-offsites/
      setting-okrs-goals/
      stakeholder-alignment/
      systems-thinking/
      team-rituals/
```

---

## Skills

### Engineering

The Matt Pocock workflow pattern — design → PRD → issues → implement → refactor, anchored on `CONTEXT.md` and `docs/adr/`. Skills marked **(user)** are user-invoked only (`disable-model-invocation: true`); the rest carry trigger phrasing so the model can reach for them on its own.

| Skill                                 | Description                                                                                                                                          |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ask-matt** _(user)_                 | A router over the skills — ask which skill or flow fits your situation and it maps the path.                                                         |
| **grill-with-docs** _(user)_          | Grilling session that also builds the domain model — sharpens terminology and updates `CONTEXT.md` and ADRs as decisions crystallize.                |
| **improve-codebase-architecture** _(user)_ | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.                   |
| **setup-matt-pocock-skills** _(user)_ | Scaffold the per-repo config (issue tracker, triage labels, domain doc layout) the other engineering skills consume. Run once per repo.             |
| **to-prd** _(user)_                   | Turn the current conversation into a PRD and publish it to the issue tracker — no interview, just synthesis of what you've already discussed.        |
| **to-issues** _(user)_                | Break any plan, spec, or PRD into independently-grabbable issues using tracer-bullet vertical slices.                                                |
| **implement** _(user)_                | Implement a piece of work from a PRD or set of issues, leaning on `tdd` at pre-agreed seams, then reviewing the result.                              |
| **prototype** _(user)_                | Build a throwaway prototype — a runnable terminal app for state/business-logic questions, or several radically different UI variations on one route. |
| **triage** _(user)_                   | Move issues and external PRs through a state machine of triage roles — categorize, verify, grill if needed, and write agent-ready briefs.            |
| **diagnosing-bugs**                   | Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimize → hypothesize → instrument → fix → regression-test.       |
| **tdd**                               | Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.                                  |
| **domain-modeling**                   | Actively build and sharpen a project's domain model — challenge terms, stress-test with scenarios, write the glossary and ADRs inline.              |
| **codebase-design**                   | Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.                          |
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

### Leadership

Skills for managing a team and working across an organization. Each follows one shape: north-star principles, a branch router (design-a-system vs. a tactical "do this now" path), and reference files (`INTAKE`, `WORKFLOW`, `TEMPLATES`, `CHECKLISTS`, `RUBRIC`). The six unmarked skills fire on their own; **(user)** skills are user-invoked only and reachable through the **leadership** router.

Adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled from Lenny's Podcast — since substantially rewritten into the shape above.

| Skill                                     | Description                                                                                                              |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **leadership**                            | Router over the leadership skills — describe your situation and it points you to the right one.                        |
| **running-effective-1-1s**                | Design a 1:1 operating system or prep a specific 1:1, skip-level, or career conversation.                              |
| **having-difficult-conversations**        | Prep and deliver feedback, performance, promotion-denial, or (HR-gated) layoff/termination conversations.              |
| **managing-timelines**                    | Turn a deadline into a plan or rescue a slipping one — milestones, RAG cadence, scope/change control.                  |
| **managing-up**                           | Manage your boss: weekly updates, escalations and asks, boundary resets, and exec influence.                           |
| **running-effective-meetings**            | Prep or run a specific meeting — decision/strategic/operational formats and meeting hygiene.                           |
| **cross-functional-collaboration**        | Work across teams: defuse a conflict, unblock a dependency, or set decision rights.                                    |
| **building-team-culture** _(user)_        | Team values, norms, and psychological safety.                                                                          |
| **coaching-pms** _(user)_                 | Coach and develop product managers; leveling expectations and growth plans.                                            |
| **delegating-work** _(user)_              | Hand off a task now or design a standing delegation system — decision rights without micromanaging.                    |
| **energy-management** _(user)_            | Redesign your week around energy; recovery routines and burnout prevention.                                            |
| **engineering-culture** _(user)_          | DevEx, clock speed, Conway's Law, blameless practices, and tech-debt calls.                                            |
| **evaluating-trade-offs** _(user)_        | Cost-benefit, build vs buy, opportunity cost, and sunk-cost stop/continue calls.                                       |
| **organizational-design** _(user)_        | Org structure, reorgs, team topology, and decision centralization.                                                     |
| **organizational-transformation** _(user)_ | Move to a product operating model — change management and proof pilots.                                              |
| **planning-under-uncertainty** _(user)_   | Hypotheses, experiments, buffers, and contingencies under ambiguity.                                                   |
| **post-mortems-retrospectives** _(user)_  | Blameless post-mortems and retros — contributing factors, actions, and learning dissemination.                        |
| **running-decision-processes** _(user)_   | Decision memos, RAPID/DACI, one-way vs two-way doors, and a decision log.                                              |
| **running-design-reviews** _(user)_       | Design critique sessions — prioritized feedback and a decision record.                                                 |
| **running-offsites** _(user)_             | Plan and run a team offsite or retreat — run-of-show and follow-through.                                               |
| **setting-okrs-goals** _(user)_           | OKRs and goals with anti-gaming guardrails and a review cadence.                                                        |
| **stakeholder-alignment** _(user)_        | Secure buy-in — pre-briefs, alignment meetings, and decision comms.                                                    |
| **systems-thinking** _(user)_             | Feedback loops, second-order effects, leverage points, and interventions.                                              |
| **team-rituals** _(user)_                 | A team's operating cadence of named, templated recurring rituals.                                                      |

---

## Common Workflows

**Not sure where to start?** Run **ask-matt** — a router that walks you to the skill or flow that fits your situation.

**Idea → ship (the main flow):**

1. **grill-with-docs** - sharpen the idea by interview against `CONTEXT.md` and ADRs
2. **to-prd** - synthesize the resolved design into a PRD work item
3. **to-issues** - break the PRD into independently-grabbable vertical slices
4. **implement** - build each issue (fresh session per issue), leaning on **tdd** at pre-agreed seams

**Bug → fix:**

1. **diagnosing-bugs** - reproduce, minimize, hypothesize, find root cause
2. **triage** - route the bug through the state machine and write an agent-ready brief
3. **tdd** - implement the fix test-first

**Architecture improvement:**

1. **improve-codebase-architecture** - find deepening opportunities, pick one, grill it
2. **codebase-design** - apply the deep-module vocabulary to the chosen refactor
3. **to-issues** → **implement** - land each refactor incrementally, behind tests

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
