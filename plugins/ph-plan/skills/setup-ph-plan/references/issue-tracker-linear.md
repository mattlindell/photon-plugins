# Issue tracker: Linear

Tickets for this repo live in Linear, in team `<TEAM>` and project `<PROJECT>`. Specs, scout maps, and research findings live as Linear Documents attached to that project. `CONTEXT.md` and `docs/adr/` stay in this repo (see `domain.md`).

Use whatever access to Linear the runner already has for every operation below. When an operation isn't available through that access, tell the person instead of switching to a different connection.

Address teams, projects, milestones, labels, and statuses by name. You don't need raw IDs.

## Coordinates

| Placeholder | Meaning |
| --- | --- |
| `<TEAM>` | The team key. It's also the issue-key prefix (`<TEAM>-123`). |
| `<PROJECT>` | The project every ticket and Document for this repo belongs to. |

The values live in `docs/agents/linear-ids.local.md`, which is gitignored. Read it first and substitute throughout this file. It may also record how this machine prefers to reach Linear; follow that when it does. If the file is missing, ask before writing anything to Linear. Don't guess a team or project, and don't create issues outside them.

## Efforts

An **effort** is a body of work planned together. In Linear, each effort is a **project milestone** in `<PROJECT>`:

- **Tickets** are issues in `<PROJECT>`, assigned to the effort's milestone.
- **Specs, maps, and research** are Documents attached to `<PROJECT>`. Documents can't attach to a milestone, so link each one from the milestone's description instead.
- **The milestone description** is the effort's index: a line on what the effort is for, then a link to each Document.

A spec or ticket names its effort, usually as `Effort: milestone <name>`. When nothing names it and more than one milestone fits, ask. When a skill publishes the first artifact for new work, create the milestone first.

Title Documents by kind so people and agents can find them: `Spec: <name>`, `Map: <effort>`, `Research: <topic>`.

## Workflow states

Linear records state as a **status**, not a label. Read the team's statuses by name. Each has a type: backlog, unstarted, started, completed, or canceled. An issue is **closed** when its status type is completed or canceled.

The five triage roles are labels, not statuses. See `triage-labels.md`.

## Work item lifecycle

What happens to a ticket's status, and who does it, at each event of an unattended ticket run. Perform a row only when its actor is `agent`. Leave `automation` rows alone: the tracker makes those moves, so don't perform or check them. A `none` row has nothing to do. A row changes the assignee only when its action says so.

| Event | Actor | Action |
| --- | --- | --- |
| `start` | agent | → In Progress |
| `review requested` | agent | → In Review |
| `PR merged` | automation | → Done |
| `halt` | agent | → Todo |

Linear's GitHub integration moves the ticket to `Done` when a PR that names the ticket key merges. When the integration also moves it to `In Review` as the PR opens, the `review requested` row is `automation`. A Stall has no row because it changes no status.

## Conventions

- **Create a ticket:** an issue in team `<TEAM>`, project `<PROJECT>`, and the effort's milestone. Write the description in Markdown with real newlines.
- **Read a ticket:** the issue by key, with its comments. The comments often carry the constraints that matter.
- **List or search tickets:** filter issues by project, milestone, label, status, or assignee.
- **Sub-issue of another ticket:** set the issue's parent.
- **Comment:** add a comment to the issue.
- **Apply or remove labels:** add the label to the issue's existing set. Don't replace the set unless you mean to drop the other labels.
- **Close:** move the issue to a completed status (`Done`) or a canceled one.
- **Blocking:** Linear's native **blocks / blocked by** relation. A ticket is unblocked when every issue blocking it is closed. Where a relation can't be created, put `Blocked by: <TEAM>-<n>, <TEAM>-<n>` at the top of the description.
- **Create a missing label:** create it at the workspace level, so every team shares one copy.

## Branch naming

When a skill says "get onto a working branch", use the first of these that answers:

1. A branch pattern the repo states in `CLAUDE.md`, `CONTRIBUTING.md`, or a lint check.
2. The issue's generated branch name. Linear returns it as `branchName` on the issue.
3. The ticket key and title, slugified and lowercased: `<TEAM>-123-short-title` becomes `nw-123-short-title` for team `NW`.

Rename an inherited branch only when it doesn't already carry the ticket key. Orchestrators create worktrees and bind tasks to branch names, so adding a prefix to a branch that already carries the key can break that binding.

The ticket key must reach Linear through the branch name or the PR body. If the branch can't carry it, name the ticket in the PR description.

## Pull requests as a triage surface

Not applicable. Incoming requests, bugs, and features are triaged as Linear issues. Code review happens on PRs, but PRs aren't a request surface.

## When a skill says "publish to the issue tracker"

- **A ticket** becomes an issue in the effort's milestone, as in **Create a ticket** above.
- **A spec, PRD, or research finding** becomes a Document attached to `<PROJECT>`, titled `Spec: <name>` or `Research: <topic>`. Link it from the milestone description. Link a research Document from the ticket that asked the question too.

Triage labels go on issues only. When a skill asks you to label a spec, skip it. The spec's `settled:` block shows whether it's ready.

## When a skill says "fetch the relevant ticket"

Read the issue by key (for example `<TEAM>-123`) with its comments. For a spec, read the Document the ticket or milestone description links to.

## Scouting operations

Used by `/scout`. The **map** is a Document and its **children** are issues in the effort's milestone.

- **Map:** a Document attached to `<PROJECT>`, titled `Map: <effort>` and linked from the milestone description. It holds the Destination, Notes, Decisions so far, Not yet specified, and Out of scope sections. A Document carries no labels, so its title and the milestone link identify it, not a `scout:map` label.
- **Child ticket:** an issue in the milestone, labeled `scout:<type>` (`research`, `prototype`, `grilling`, or `task`), with the question in the description. Create the label if it's missing.
- **Blocking:** blocks / blocked by relations, as above.
- **Frontier:** the milestone's issues that carry a `scout:<type>` label, are not closed, and have no assignee. Drop any with an open blocker. The oldest left wins.
- **Claim:** assign the issue to the current user. This is the session's first write.
- **Resolve:** post the answer as a comment, or as a `Research:` Document linked from the comment. Close the issue. Then append a one-line pointer (the gist plus the issue link) to the map Document's Decisions so far.
