---
name: "jira-expert"
description:
  Use when working in Jira — running or writing JQL, creating and editing issues, transitioning issues, linking, logging
  work, designing a workflow, planning automation rules, building dashboards or reports, or configuring projects, custom
  fields, and schemes. Routes each operation by MCP reach and points at JQL, workflow, and automation references.
---

# Atlassian Jira Expert

Every Jira operation splits on one question: is it **in reach** of the Atlassian MCP, or **out of reach**? In-reach
operations (issues, JQL, transitions, comments, links, worklogs) are direct MCP calls. Out-of-reach operations
(projects, sprints, boards, filters, custom fields, workflow/permission schemes, automation rules) are **not available
via MCP** — you design them here, then route the user to the Jira web UI or REST API to apply them. Deciding reach
first, every time, is what keeps this skill from inventing tools that do not exist.

The canonical tool list is
[`project-manager/references/atlassian-mcp-tools.md`](../../references/atlassian-mcp-tools.md). Tools surface as
`mcp__atlassian__<toolName>` (camelCase). **Never invent a tool name — if a capability is not in that list, it is out of
reach.** Obtain `cloudId` once per session via `mcp__atlassian__getAccessibleAtlassianResources`; most tools require it.

## In-reach operations (direct MCP calls)

Consult [`atlassian-mcp-tools.md`](../../references/atlassian-mcp-tools.md) for exact parameters and required-field
discovery; the calls below are the common paths.

- **Create an issue** — check required fields with `getJiraIssueTypeMetaWithFields` first, then
  `createJiraIssue (cloudId, projectKey, issueTypeName, summary, …)`.
- **Run a JQL search** — `searchJiraIssuesUsingJql (cloudId, jql=…)`. Construct the JQL live (see below).
- **Edit fields** — `editJiraIssue (cloudId, issueIdOrKey, fields=…)`.
- **Change status** — status moves go through transitions, never field edits: `getTransitionsForJiraIssue` to read
  available transitions, then `transitionJiraIssue` with the chosen id.
- **Comment / log work / link** — `addCommentToJiraIssue`, `addWorklogToJiraIssue`, `createIssueLink` (link type from
  `getIssueLinkTypes`).

Completion: the MCP call returns success and a follow-up read (`getJiraIssue` or `searchJiraIssuesUsingJql`) confirms
the resulting state matches what the user asked for.

## Out-of-reach operations (design here, apply via UI/REST)

These are **not available via MCP**. For each, produce the full design in this session, then hand the user the exact UI
path or REST endpoint to apply it — never claim to have applied it yourself.

| Operation                                            | Where it is applied                                                    |
| ---------------------------------------------------- | ---------------------------------------------------------------------- |
| Create/archive a **project**                         | Jira UI `Projects > Create project` or REST `POST /rest/api/3/project` |
| Create a **sprint** / configure boards               | Jira Software UI or REST `POST /rest/agile/1.0/sprint`                 |
| Create/share a **filter**                            | Jira UI `Filters > Save as` or REST `POST /rest/api/3/filter`          |
| **Custom fields**, screens                           | Jira admin UI `Settings > Issues`                                      |
| **Workflow** / permission / notification **schemes** | Jira admin UI `Settings > Issues > Workflows`                          |
| **Automation rules**                                 | Jira Automation UI                                                     |

Completion: the design is complete and the user has the applied-elsewhere path — meaning every configuration decision
the operation needs is made (below), with nothing left for the user to invent.

## Writing JQL

Construct JQL directly against the pattern library in [`references/jql-examples.md`](references/jql-examples.md) — reach
for it whenever you need a working query for a request phrased in natural language ("high priority bugs assigned to me",
"stale issues", "sprint spillover", velocity, cycle time). It groups queries by sprint, user/team, date range, status,
priority/type, component/version, and reporting, and includes a performance section (specific project first, functions
over hardcoded sprints, avoid leading wildcards). Adapt the closest example, then execute with
`searchJiraIssuesUsingJql`.

Completion: the query parses and runs (balanced quotes and parentheses, no leading/trailing `AND`/`OR`, valid
`ORDER BY`), and its result set answers the request — verified by executing it, not by inspection alone.

## Designing a workflow

Reach for [`references/WORKFLOWS.md`](references/WORKFLOWS.md) whenever the user wants to design, review, or
troubleshoot a workflow — it holds status categories, transition/condition/validator/post-function catalogs,
post-function ordering rules, scheme configuration, and the Design Validation Checklist.

1. Map process states to the four Jira status categories (`To Do`, `In Progress`, `Done`) per WORKFLOWS.md, mirroring
   the team's real process.
   - Completion: every state maps to exactly one category and represents a distinct work state where the item waits for
     a different action.
2. Define transitions, conditions, validators, and post-functions using the catalogs in WORKFLOWS.md; order
   post-functions so "Generate change history" and "Fire event" stay last.
   - Completion: every state has a reachable path in and out (except terminal states, which need only a path in), and
     every rejected/reopened state has a path back.
3. Validate the design against the Design Validation Checklist in WORKFLOWS.md.
   - Completion: every checklist anti-pattern is checked and no Error-severity hit remains (too-few/too-many states, no
     terminal state, dead-end, unreachable, undefined state reference, circular no-exit); Warning/Info hits are
     confirmed intentional.
4. Hand the user the apply path: build in Jira admin UI `Settings > Issues > Workflows`, deploy to a test project, walk
   sample issues through every transition, then associate with production. Confirm expected transitions via
   `getTransitionsForJiraIssue` and walk them with `transitionJiraIssue` on a sample issue.
   - Completion: the user has the UI path plus the test-project verification steps, and every designed transition
     surfaced and fired on the sample issue.

## Planning automation rules

Every rule is one **trigger** → optional **conditions** → one or more **actions**. Reach for
[`references/AUTOMATION.md`](references/AUTOMATION.md) for the trigger/condition/action catalogs, smart values, and
production-ready recipes, and [`references/automation-examples.md`](references/automation-examples.md) for
ready-to-adapt rules grouped by purpose (assignment, status sync, notification, field, escalation, sprint, approval,
integration, quality, documentation, time tracking).

1. Pick the trigger and the JQL/field conditions that scope it, and specify each action with its smart values, adapting
   the closest recipe from the reference files.
   - Completion: the rule names its single trigger, its conditions, and every action — each smart value resolved against
     the catalog in AUTOMATION.md so no placeholder is left undefined.
2. Hand the user the apply path: build in the Jira Automation UI, test in a sandbox project, add rate limits to prevent
   trigger loops, then enable and monitor the audit log.
   - Completion: the user has the sandbox-test and rate-limit steps, since automation mistakes are destructive and
     loop-prone.

## Building dashboards and reports

Dashboards and their gadgets are configured in the Jira UI (out of reach). Design the gadget set — Filter Results,
Sprint Burndown, Velocity Chart, Created vs Resolved, status Pie Chart — and back each JQL-driven gadget with a query
from [`references/jql-examples.md`](references/jql-examples.md) (its reporting and saved-filter sections cover velocity,
bug rate, cycle time, and standup filters). Save frequently-run queries as shared filters rather than re-running ad hoc
JQL.

Completion: every gadget has a named JQL filter behind it, and the user has the UI path to add gadgets and share the
dashboard.

## Reference material

- **JQL** — [`references/jql-examples.md`](references/jql-examples.md): query library by category plus performance
  guidance.
- **Workflows** — [`references/WORKFLOWS.md`](references/WORKFLOWS.md): status categories, transitions, conditions,
  validators, post-functions, schemes, Design Validation Checklist.
- **Automation** — [`references/AUTOMATION.md`](references/AUTOMATION.md) and
  [`references/automation-examples.md`](references/automation-examples.md): triggers, conditions, actions, smart values,
  recipes.
- **MCP tools** — [`../../references/atlassian-mcp-tools.md`](../../references/atlassian-mcp-tools.md): canonical tool
  list and the reach boundary.

## Escalation and handoffs

- **Atlassian Admin** ([`../atlassian-admin/`](../atlassian-admin/)) — new permission schemes, org-wide workflow
  schemes, user provisioning, licensing, system-wide configuration.
- **Scrum Master** — sprint board configuration, backlog prioritization views, team filters, velocity/burndown setup.
- **Senior PM** — portfolio reporting, cross-project dashboards, executive visibility, multi-project dependencies.
- **Confluence Expert** ([`../confluence-expert/`](../confluence-expert/)) — documentation pages that complement Jira
  workflows.
