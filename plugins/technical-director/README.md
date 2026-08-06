# technical-director

A Claude Code plugin for technical direction and engineering leadership. Fifty-two skills across two halves:

- **Engineering workflow** — twenty-eight skills adapted from [Matt Pocock's skill
  repository](https://github.com/mattpocock/skills) covering diagnosis, domain modeling, specs, issue triage, TDD,
  codebase design and architecture, prototyping, implementation, and the meta-tools that keep a project's process tight —
  organized into engineering (18), productivity (8), and misc (2) buckets.
- **Leadership** — twenty-four skills for managing a team and working across an organization: 1:1s, difficult
  conversations, delegation, managing up, cross-functional collaboration, decisions, timelines, meetings, culture, and
  org design. Seven fire on their own (including the router); the rest are user-invoked and reachable through the
  `leadership` router. Adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled
  from Lenny's Podcast — since substantially rewritten.

Plus **two autonomous agents** — `implement` and `code-review` — for harnesses that spin up an agent thread from a bare
ticket or PR (Kepler, and similar). See [Agents](#agents).

**Version:** 4.0.0
**Author:** Matt Lindell
**License:** MIT

---

## Plugin Structure

```text
plugins/technical-director/
  .claude-plugin/
    plugin.json
  README.md
  agents/                             # plugin-level agents (auto-discovered)
    implement.md
    code-review.md
  skills/
    engineering/
      README.md
      # every skill below also carries agents/openai.yaml (see Portability)
      ask-matt/
        SKILL.md
        PHASE-BOUNDARIES.md
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
      wizard/
        SKILL.md
        template.sh
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
      to-questionnaire/SKILL.md
      wait-what/SKILL.md
      writing-for-agents/
        SKILL.md
        SKILL-MECHANICS.md
    misc/
      README.md
      git-guardrails-claude-code/
        SKILL.md
        scripts/block-dangerous-git.sh
      setup-pre-commit/SKILL.md
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

### Portability

Every skill outside `leadership/` carries an `agents/openai.yaml` sidecar giving it a display name, a short description,
and — for user-invoked skills — `policy.allow_implicit_invocation: false`, the OpenAI-side mirror of Claude Code's
`disable-model-invocation: true`. Claude Code ignores these files; they let the same skill folder be consumed by an
OpenAI-based agent harness without a second copy. The `leadership/` skills don't carry them.

---

## Agents

Two agents for **agent-thread harnesses** — Kepler, and anything else that opens a task thread from a bare Jira/Linear
ticket or a PR with no room for instruction up front. Each derives the setup the underlying skill would otherwise open by
asking for, then runs that skill unchanged.

| Agent           | Input                             | Drives                      | Derives for itself                                                     |
| --------------- | --------------------------------- | --------------------------- | ---------------------------------------------------------------------- |
| **implement**   | A ticket key, issue, or spec file | `/tdd`, then `/code-review` | The tracker fetch, the domain grounding from `CONTEXT.md` and ADRs, and the working branch |
| **code-review** | A PR, branch, tag, or SHA         | `/code-review`              | The **fixed point** (from the PR base) and the **spec source** (from the PR's linked ticket) |

They hold no method of their own — `/tdd` and `/code-review` stay the single source of truth, so editing a skill changes
both the interactive flow and the agent. The agent files carry only the kickoff steps and a checkable definition of done.

Deriving is not the same as never asking. Both agents assume a reachable human and spend that reach on decisions that
change the work and can't be looked up. `implement` still stops at `/tdd`'s **pre-agreed seams** gate — proposing a
concrete list to confirm before the first test, since the seams decide where the testing effort lands.

`implement` writes code and commits to the working branch; it does not push or open PRs. `code-review` leaves the
working tree untouched and returns its report in the thread rather than posting to the PR.

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
| **wizard**                            | Generate an interactive bash wizard for the steps only a human can take — provisioning infrastructure, credentials and CI secrets, an unfamiliar third-party dashboard, a one-off migration or cutover. |

### Productivity

General workflow tools, not code-specific. **(user)** marks user-invoked-only skills.

| Skill                            | Description                                                                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **caveman** _(user)_             | Ultra-compressed communication mode that drops filler and pleasantries while keeping full technical accuracy (~75% fewer tokens).  |
| **grill-me** _(user)_            | Get relentlessly interviewed about a plan or design — the stateless sibling of `grill-with-docs`, for plans that don't live in a repo. |
| **handoff** _(user)_             | Compact the current conversation into a handoff document so another agent can continue the work.                                  |
| **teach** _(user)_               | Learn a concept over multiple sessions, using the current directory as a stateful workspace.                                       |
| **to-questionnaire** _(user)_    | Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or together over a meeting. |
| **wait-what** _(user)_           | Fire this the moment a message doesn't land — the agent re-pitches it in plain English with the context you were missing, using your `CONTEXT.md` vocabulary. |
| **grilling**                     | Interview the user relentlessly about a plan or design, resolving each branch of the decision tree one question at a time.         |
| **writing-for-agents**           | Reference for writing documents agents consume: skills, `AGENTS.md` / `CLAUDE.md`, and any doc an agent reaches by a pointer.      |

### Misc

Repo and tooling guardrails that don't fit the engineering workflow.

| Skill                          | Description                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **git-guardrails-claude-code** | Install a Claude Code `PreToolUse` hook that blocks dangerous git commands (`push`, `reset --hard`, `clean`, `branch -D`, etc.) before they execute. |
| **setup-pre-commit**           | Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests for JavaScript/TypeScript projects.                               |

### Leadership

Skills for managing a team and working across an organization. Each follows one shape: north-star principles, a branch router (design-a-system vs. a tactical "do this now" path), and reference files (`INTAKE`, `WORKFLOW`, `TEMPLATES`, `CHECKLISTS`, `RUBRIC`). The seven unmarked skills fire on their own; **(user)** skills are user-invoked only and reachable through the **leadership** router.

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

## Per-repo Setup

The engineering skills read their per-repo configuration from `docs/agents/`, not from inline `CLAUDE.md` prose. Run
**setup-matt-pocock-skills** once per repo to generate it:

| File                            | What it configures                                                     | Consumed by                                  |
| ------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------- |
| `docs/agents/issue-tracker.md`  | Where issues live and how to create, read, and close them              | `to-spec`, `to-tickets`, `wayfinder`, `triage`, `code-review` |
| `docs/agents/triage-labels.md`  | The label strings for the five canonical triage roles                  | `triage` (written only when `triage` is installed) |
| `docs/agents/domain.md`         | Where `CONTEXT.md` and ADRs live, plus the consumer rules for reading them | `domain-modeling`, `grill-with-docs`      |

Setup also adds an `## Agent skills` block to whichever of `CLAUDE.md` / `AGENTS.md` already exists, pointing at those
three files — it never creates the one that isn't there.

Issue trackers supported out of the box: **GitHub** (`gh`), **GitLab** (`glab`), and **local Markdown** under
`.scratch/<feature>/`. Anything else (Jira, Linear, …) is handled as **Other** — describe the workflow in a paragraph
and setup records it as freeform prose in `docs/agents/issue-tracker.md`.

Edit `docs/agents/*.md` directly to adjust things later; re-run **setup-matt-pocock-skills** only to switch trackers or
start over.

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
