# Issue tracker: Linear

Issues, PRDs, and specs for this repo live in **Linear**. There are two ways in:

- **`linearis` CLI (default / fast path)** — a local CLI with JSON output; pipe through `jq`. Faster than the MCP and covers the whole everyday loop: list/search/read, create/update (labels, status, project, `--parent-ticket`, `blocks`/`blocked-by` relations), and discussion threads. **Reach for this first.**
- **Linear MCP (`mcp__linear__*`, fallback)** — broader surface. Use it only for operations the CLI can't do (see "CLI gaps" below) or when a skill explicitly needs an MCP tool.

Both accept **human-readable identifiers** (team key, issue key, project/label names), so no UUIDs are needed on either path.

> **Prerequisite:** the CLI path needs the `linearis` binary on `PATH` and authenticated — it is
> **not** installed by this repo, and neither is its command reference. Matt's fleet installs the
> binary via mise and carries the `linearis-cli` skill as a personal skill at
> `~/.claude/skills/linearis-cli`. Auth: `linearis auth login`, `--api-token <token>`,
> `LINEAR_API_TOKEN`, or `~/.linearis/token`. If `linearis` is unavailable (fresh clone, CI, AFK
> agent without it provisioned), use the **MCP path** for everything instead.

### CLI gaps → use the MCP

- **Creating labels** — `linearis labels` only *lists*; it can't create. New labels → MCP `create_issue_label`. (The triage and Wayfinder label groups already exist, so this is rarely needed.)
- Anything outside the CLI's domains (`issues`, `comments`, `labels`, `projects`, `cycles`, `milestones`, `documents`, `files`, `attachments`, `teams`, `users`, `initiatives`) — check `linearis usage` / `linearis <domain> usage`, and fall back to the MCP if absent.

## Fixed coordinates

Both tools resolve teams, projects, and labels **by name**. **This repo is public, so the workspace,
team, and project identifiers are not committed** — they live in `docs/agents/linear-ids.local.md`
(gitignored), along with the raw UUIDs.

Read that file first and substitute throughout this doc:

| Placeholder | Meaning |
| --- | --- |
| `<TEAM>` | the team key, used as `--team <TEAM>` and as the issue-key prefix (`<TEAM>-123`) |
| `<PROJECT>` | the project name — **quote it**, it contains a space (`--project "<PROJECT>"`) |

Always create issues **scoped to that project and team** unless told otherwise.

> If `linear-ids.local.md` is absent (fresh clone, CI, AFK agent), you cannot resolve `<TEAM>` or
> `<PROJECT>` — **ask before writing anything to Linear.** Don't guess at a team or project name,
> and don't fall back to creating issues unscoped.

## Workflow states (Linear statuses)

Linear models "state" as a status, not a label. The team's statuses, by name: `Backlog`, `Todo`,
`In Progress`, `In Review`, `Done`, `Duplicate`, `Canceled`. Pass the status by name
(CLI `--status`, MCP `state`); raw status IDs live in `linear-ids.local.md`.

The five **triage roles** are Linear *labels*, not statuses — see `triage-labels.md`.

## Conventions

Each operation lists the **CLI (default)** then the **MCP (fallback)**.

- **Create an issue**: `linearis issues create "<title>" --team <TEAM> --project "<PROJECT>" --description "<md>" [--labels a,b] [--status "<name>"]` · MCP `save_issue` with `title`, `description` (real newlines, not `\n`), `team`, and `project`.
- **Read an issue**: `linearis issues read <TEAM>-<n> --with-comment-threads` · MCP `get_issue` + `list_comments`.
- **List / search issues**: `linearis issues list --team <TEAM> --project "<PROJECT>" [--label … --status … --assignee …]` or `linearis issues search "<query>"` · MCP `list_issues`.
- **Comment on an issue**: `linearis issues discuss <TEAM>-<n> --body "<md>"` (start a thread); reply with `linearis issues reply <thread-id> --body "…"` · MCP `save_comment`.
- **Apply / change labels or status**: `linearis issues update <TEAM>-<n> --labels <names> [--label-mode add] [--status "<name>"]` · MCP `save_issue` with the new `labels`/`state`. (Use `--label-mode add` to append rather than overwrite.)
- **Close**: `linearis issues update <TEAM>-<n> --status Done` (or `Canceled`) · MCP `save_issue` transitioning `state`.

## When a skill says "publish to the issue tracker"

Create a Linear issue in the project — `linearis issues create … --team <TEAM> --project "<PROJECT>"` (MCP `save_issue` fallback).

## When a skill says "fetch the relevant ticket"

`linearis issues read <TEAM>-<n> --with-comment-threads` (MCP `get_issue` + `list_comments` fallback).

## Pull requests as a triage surface

Not applicable — Linear is the request surface, not GitHub PRs. Code review happens on GitHub PRs,
but incoming requests/bugs/features are triaged as Linear issues.

## Wayfinding operations

Used by `/wayfinder`. Model the **map** and its **child tickets** as Linear issues:

Wayfinder labels are a workspace-level **"Wayfinder" label group** with children named `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task` — apply the full prefixed name. (These already exist workspace-wide; no seeding needed.)

- **Map**: a single issue labeled `wayfinder:map` holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: an issue linked to the map as a Linear **sub-issue** via `linearis issues create "<title>" --team <TEAM> --project "<PROJECT>" --parent-ticket <TEAM>-<map> --labels wayfinder:<type>` (MCP `save_issue` with `parent` as fallback), where `<type>` is `research` / `prototype` / `grilling` / `task`. Once claimed, assign the ticket to the driving dev.
- **Blocking**: Linear's native **blocks / blocked-by relations** — `linearis issues update <TEAM>-<child> --blocked-by <TEAM>-<blocker>` (MCP fallback). A child is unblocked when every blocker is `Done`/`Canceled`. Query blocked children with `linearis issues list --has-blockers`. Where a relation can't be created, fall back to a `Blocked by: <TEAM>-<n>, <TEAM>-<n>` line at the top of the child body.
- **Frontier query**: `linearis issues list --team <TEAM> --parent <TEAM>-<map>` for the map's open sub-issues (drop completed/canceled statuses); drop any with an open blocker (`--has-blockers` marks these) or an assignee; first in map order wins.
- **Claim**: `linearis issues update <TEAM>-<n> --assignee <me>` — the session's first write.
- **Resolve**: `linearis issues discuss <TEAM>-<n> --body "<answer>"`, `linearis issues update <TEAM>-<n> --status Done`, then append a context pointer to the map's Decisions-so-far.
