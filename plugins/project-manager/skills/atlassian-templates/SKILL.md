---
name: "atlassian-templates"
description:
  Lifecycle owner for Jira and Confluence templates. Use when the user wants to create, modify, deploy, or deprecate an
  org-wide template, blueprint, page layout, or reusable content structure; when standardizing issue or page bodies
  across a space or project; or when another skill needs a deployable storage-format template body.
---

# Atlassian Templates

Own the **lifecycle** of reusable Jira and Confluence templates — create, deploy, govern, deprecate — so content stays
consistent across the org. A Confluence template body ships as **storage-format XHTML**; wiki markup is rejected on
deploy.

## References

- `references/template-design-patterns.md` — reach for it before drafting any body: variable placeholders, reusable
  components (header, decision log, change history, action items), conditional/responsive layouts, and the
  storage-format scaffolding convention that turns a draft into deployable XHTML.
- `references/governance-framework.md` — reach for it whenever the run touches ownership, approval, deprecation, usage
  thresholds, or quality gates: it holds the concrete roles, cadences, and pass/fail checklists.
- `confluence-expert/references/macro-cheat-sheet.md` — reach for it for the storage-format syntax of any macro (toc,
  status `colour`, info/warning/note, expand, jira, code).
- `project-manager/references/atlassian-mcp-tools.md` — the canonical MCP tool list; consult it before naming any
  `mcp__atlassian__*` tool.

## Create a template

1. **Scope it.** Confirm the need against `references/governance-framework.md` approval criteria — serves more than one
   team, does not duplicate an existing template by >60% content overlap. **Done when** you can name the target audience
   and the gap no existing template fills.
2. **Draft the body.** Assemble sections and components per `references/template-design-patterns.md`, using `<at:var>`
   placeholders with meaningful defaults. **Done when** every section carries placeholder text showing expected content
   — no bare headings — and a metadata header (owner, version, status, last-reviewed) is present.
3. **Convert to storage format.** Render the draft as storage-format XHTML, taking each macro's syntax from
   `confluence-expert/references/macro-cheat-sheet.md`. **Done when** the body contains zero wiki-markup macros
   (`{...}`, `h2.`) — every macro is `<ac:structured-macro>` form.
4. **Deploy via MCP.** Create the page per "MCP operations" below. **Done when** `createConfluencePage` returns a page
   id and the read-back verification passes for every target space.
5. **Hand off publishing tasks MCP cannot do.** Apply labels, register a first-class space template, and configure Jira
   description defaults through the UI/REST paths named below. **Done when** each capability MCP lacks is routed to its
   UI/REST home, none left assumed-done.

## Modify a template

1. **Assess impact.** Classify the change (low / medium / high) against `references/governance-framework.md` and gather
   the required reviewers. **Done when** the impact tier and its approval path are named.
2. **Version, then edit.** Bump the version per the governance framework's numbering, keep the prior version reachable,
   and edit the storage-format body. **Done when** the changelog entry is written and the old version is archived, not
   deleted.
3. **Redeploy and migrate.** Update the page via MCP and provide the migration path for existing content. **Done when**
   the read-back verification passes and existing documents have a stated migration path (or are explicitly exempt).

## MCP operations

**Server:** Atlassian Remote MCP, key `atlassian`; tools surface as `mcp__atlassian__<toolName>` (camelCase). Get
`cloudId` once via `getAccessibleAtlassianResources`. Discover exact parameter names from each tool's schema at call
time. Never invent a tool name — if a capability is absent from `project-manager/references/atlassian-mcp-tools.md`,
route it to the UI/REST path that reference names.

**Create a Confluence template page** — pass the storage-format body as `body` to `createConfluencePage` (`cloudId`,
space, `title`, optional parent id). For a batch, repeat per target space.

**Update an existing page** — read current version with `getConfluencePage`, then `updateConfluencePage` (`cloudId`,
`pageId`, `version` = current + 1, new `body`).

**Read-back verification** (run after every create/update, per target): retrieve the page with `getConfluencePage` and
assert the body is non-empty, contains the expected `<ac:structured-macro>` elements, renders without macro errors,
embedded Jira macros resolve against the target project, and task blocks are interactive. On any failure, revert with
`updateConfluencePage` (`version` = current + 1, prior-version body).

**Jira description templates** — MCP cannot configure field defaults, screens, or contexts. It can create issues
pre-filled with template text via `createJiraIssue` (template body as the description) and inspect required fields with
`getJiraIssueTypeMetaWithFields`. Configure a persistent `default_value` on the description field in the Jira admin UI
(`Settings > Issues > Field configurations`) or REST (`/rest/api/3/fieldconfiguration`).

**Not available via MCP** — page labels, first-class space templates/blueprints, and field configuration.
`createConfluencePage` makes ordinary pages that serve as copy-from templates; register a real space template in
`Space settings > Templates`, and apply labels in the Confluence UI.

## Handoffs

Governance framework in `references/governance-framework.md`.

| Partner           | Receives from                                           | Sends to                                         |
| ----------------- | ------------------------------------------------------- | ------------------------------------------------ |
| Senior PM         | Template requirements, reporting/executive formats      | Completed templates, usage analytics             |
| Scrum Master      | Ceremony needs, retro format preferences                | Sprint-ready templates, ceremony structures      |
| Jira Expert       | Issue template requirements, custom field display needs | Issue description templates, JQL query templates |
| Confluence Expert | Space-specific needs, blueprint requirements            | Configured page templates, deployment plans      |
| Atlassian Admin   | Org-wide standards, global deployment, compliance needs | Global templates for approval, compliance status |

Blueprint and global-template deployment is an Atlassian Admin action — hand off rather than attempting it via MCP.
