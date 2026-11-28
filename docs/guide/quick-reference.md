# Quick reference

This page is for developers who already use Claude Code every day. Each section
is the short version of one guide page and links to it. When this page and a
full page disagree, the full page is right.

Terms link to [CONTEXT.md](../../CONTEXT.md), the repo's one glossary.

## Setup

Close any open Claude Code sessions, then run these commands in a terminal.
`ph-plan` and `ph-build` call `ph-lib` skills, so install all three.

```bash
claude plugin marketplace add https://github.com/mattlindell/photon-plugins
claude plugin install ph-lib@photon-plugins
claude plugin install ph-plan@photon-plugins
claude plugin install ph-build@photon-plugins
```

`claude plugin list` shows all three as enabled. Claude Code also needs access to
your [issue tracker](../../CONTEXT.md#issue-tracker): GitHub, GitLab, Jira,
Linear, or local markdown. For GitHub or GitLab, sign in to `gh` or `glab`. If
you reach your tracker through an MCP server, check with `/mcp`.

Then set up each repo once. Start Claude Code in the repo root and run
`/ph-plan:setup-ph-plan`.

- Pick your tracker's route. GitHub, GitLab, and local markdown ask nothing
  more. Jira asks where specs live, then for the site, project key, and issue
  types. Linear asks for the team key and project name, and on a public repo it
  can keep them in a gitignored `docs/agents/linear-ids.local.md`. Pick
  **Other** only when no route fits your tracker.
- Keep the default triage labels.
- Check the `issue-tracker.md` draft for your tracker and values, then let the
  skill write the files. On Linear with the local file, the values are in the
  `linear-ids.local.md` draft, and `issue-tracker.md` keeps placeholders.

Commit `docs/agents/issue-tracker.md`, `triage-labels.md`, `domain.md`, and the
`## Agent skills` section in `CLAUDE.md` or `AGENTS.md`. Don't commit a
`*.local.md` file.

Full page: [Setup](setup.md). If a step fails, see its
[Troubleshooting](setup.md#troubleshooting) section.

## Reading the plan

Every spec and ticket that `ph-plan` writes opens with a settled block:

```yaml
settled: [problem, shape, approach]
open: [verification]
```

Each name is a [dimension](../../CONTEXT.md#dimension). There are four:
`problem` (what and why), `shape` (structure and types), `approach` (how to
build it), and `verification` (how anyone knows it's done). A settled dimension
is a decision someone already made, so don't reopen it. `verification: open`
means the builder writes tests first. It doesn't mean tests are optional.

Hand a spec or ticket to `/ph-build:dispatch` with its key or link, for example
`/ph-build:dispatch SF-43`. `dispatch` reads the comments too, and sizes the
build to what's open:

| Settled block | What `ph-build` does |
| --- | --- |
| All four settled | Builds at the `scoped` [tier](../../CONTEXT.md#tier), with no exploration phase and no panels. |
| Some settled | Works only on the open dimensions. |
| None settled, or no block | One orientation pass, then a provisional block that it says it inferred. |
| No spec at all | Routes to `/ph-plan:intake`. If nobody can plan it and the work is easy to undo, it takes the orientation pass and continues. |

A [one-way door](../../CONTEXT.md#one-way-door) is a schema change or data
migration, a public API, anything that deletes or permanently rewrites data,
or an auth, billing, or security boundary. If the block settles the door,
`ph-build` builds it and a reviewer that didn't write the change must pass it.
If the block leaves it open, `ph-build` stops, hands you a decision ticket, and
names the skill that fits. These skills run several agents at once, so only you
can start them:

| Skill | Use it for |
| --- | --- |
| `/ph-build:architect` | A shape that crosses a function boundary |
| `/ph-build:interrogate` | An adversarial review of a design or diff by several models |
| `/ph-build:swarm` | Coverage matrices, race conditions, or exploring a large space in parts |
| `/ph-build:arena` | Comparing competing designs or implementations |

If you think a settled decision is wrong, stop the part it touches. Comment
with your evidence and tag the person who settled it. Don't edit the block
yourself, and don't build around the decision.

Full page: [Reading the plan](reading-the-plan.md).

## Writing the plan

| Command | What it does |
| --- | --- |
| `/ph-plan:intake` | Starts new work. Routes to `grilling`, or to `scout` for work too big for a session or two. |
| `/ph-plan:grilling` | Asks the whole frontier of questions each round, until every decision is made. Each question has a recommended answer, and "yes" accepts it. |
| `/ph-plan:define-done` | Closes `verification` with one way to prove the work is done. |
| `/ph-plan:to-spec` | Writes the agreed plan as one spec, where your `issue-tracker.md` says specs live. |
| `/ph-plan:to-tickets` | Splits the plan into tickets, each with its own settled block and its blocking links. |
| `/ph-plan:scout` | Charts a [scout map](../../CONTEXT.md#scout-map) of decision tickets, then resolves its tickets one per session. Run it again with the map to continue. |

Most days you type only `/ph-plan:intake` and `/ph-build:dispatch`. `intake`
hands off to `grilling`. When `problem`, `shape`, and `approach` are settled,
`define-done` closes `verification` in the same session. After you confirm the
shared understanding, the session ends in `to-spec`, `to-tickets`, or both.

Answer every question in a round, numbered to match: `Q1 yes. Q2 no, ...`. Say
"I don't know" instead of guessing. A dimension that can't close in the session
becomes a [decision ticket](../../CONTEXT.md#decision-ticket) with a `closes:`
line, and it blocks the work that waits for it. A design session with
`ph-lib:codebase-design`, `/ph-plan:prototype`, or `/ph-plan:research` resolves
it, depending on what's missing. Write the settled block honestly, because it
tells the builder how much thinking is left.

Work that already has a ticket goes to `/ph-plan:triage`, which checks the
ticket and grills it into shape if it needs that. A question about existing
code goes to `ph-build:how`, or to `ph-build:why` for the reasons behind it.

Full page: [Writing the plan](writing-the-plan.md).

## House standard

This section is for the person who sets up how a team tracks work. A house
standard is one template for `docs/agents/issue-tracker.md` that every repo's
file comes from, so that every repo puts the same artifact in the same place.
Start from the built-in template for your tracker, in
[`plugins/ph-plan/skills/setup-ph-plan/references/`](../../plugins/ph-plan/skills/setup-ph-plan/references/),
and change it.

- Tickets live in the tracker. Specs, maps, and research live together, beside
  the tickets or in a wiki. `CONTEXT.md` and the ADRs stay in the repo.
- The standard names what an [effort](../../CONTEXT.md#effort) is on your
  tracker, and the exact phrase a spec or ticket uses to name its effort.
- Titles use fixed prefixes: `Spec: <name>`, `Map: <effort>`,
  `Research: <topic>`. Work tickets and decision tickets get no prefix.
- House-wide values are literal text in the template. Per-repo values are
  placeholders in angle brackets, such as `<PROJECT_KEY>`.
- Don't add a connection method, such as a CLI or an MCP server, that the
  built-in template leaves out.
- Private values and each person's connection preference go in a gitignored
  `docs/agents/*.local.md` file. The setup skill adds `*.local.*` to
  `.gitignore` only on the route that offers the local file. On any other
  route, add it yourself.
- Keep the template in one place with a change history, not in a product repo.
  Change the template first, then every repo's `issue-tracker.md`.

To set up a repo from the standard, run `/ph-plan:setup-ph-plan` and pick your
tracker's route. Tell the skill to replace its `issue-tracker.md` draft with
your template, with this repo's values filled in, before it writes the file.
With **Other**, paste the filled-in template when the skill asks you to describe
your workflow.

Full page: [House standard](house-standard.md).
