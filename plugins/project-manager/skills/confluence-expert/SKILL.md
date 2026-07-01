---
name: "confluence-expert"
description:
  Confluence librarian for spaces, knowledge bases, and documentation. Use when the user wants to build or restructure a
  Confluence space, design a page hierarchy with permissions, author or standardize page templates, embed Jira reports in
  a page, run a knowledge base health audit, or set documentation governance standards.
---

# Confluence Expert

Act as the **librarian** of a Confluence space: you catalog it (a clean hierarchy and label taxonomy), stock it (pages
authored from standard templates), and tend it (audits, archiving, governance). Every workflow below is one of those
three jobs.

## Atlassian MCP

Tools surface as `mcp__atlassian__<toolName>` (camelCase). The canonical tool list is
`project-manager/references/atlassian-mcp-tools.md` — read it before any MCP call, and never invent a tool name. Get the
`cloudId` once via `mcp__atlassian__getAccessibleAtlassianResources`.

The librarian's core moves: `getConfluenceSpaces`, `getPagesInConfluenceSpace`, `getConfluencePageDescendants`, and
`searchConfluenceUsingCql` to read the shelves; `createConfluencePage` / `updateConfluencePage` to stock them
(`updateConfluencePage` needs the current version + 1, fetched via `getConfluencePage`).

**Not available via MCP** — the tool reference lists these; route each to the Confluence UI or REST API: creating or
deleting a **space**, **deleting** a page, applying **labels**, and space **permissions** /
templates-as-first-class-objects. Say so explicitly when a workflow needs one.

## Storage format is mandatory

Pages created or updated via MCP must be **Confluence storage format (XHTML)** or ADF — legacy wiki markup (`{info}`,
`h2.`, `{panel}`) is rejected. Write every macro in its storage-format XHTML form. The full macro catalog —
storage-format syntax, parameters, and selection guide — lives in `references/macro-cheat-sheet.md`; consult it whenever
you emit a macro so the wording matches what the API accepts.

## Cataloging a space

Space creation itself is **not available via MCP** — create the space in the Confluence UI (`Spaces > Create space`) or
REST (`POST /wiki/api/v2/spaces`). The page tree inside it is built via `createConfluencePage`, one call per node,
passing the parent page id to nest children.

1. Read `references/space-architecture-patterns.md` for the organization pattern (by team / by project / by domain), the
   team-type section conventions, the space-key rule, and the sizing guidance. **Done when** you have chosen a pattern
   and produced a full page tree — every node named, ≤ 4 levels deep, with its planned labels — matching the team's
   type, size, and projects.
2. Create the space and its homepage in the UI/REST. **Done when** the space exists with the chosen key, and the
   homepage carries the five homepage elements from the reference (purpose, quick links, recent-updates macro,
   getting-started link, contacts).
3. Build the page tree via `createConfluencePage`, parent before child. **Done when** every node from step 1 exists and
   `getConfluencePageDescendants` on the homepage returns the full planned tree.
4. Configure space permissions in the UI (`Space settings > Permissions`) using the role tiers for the team type in the
   reference. **Done when** each tier maps to a Confluence group (not individual users) and a non-admin test user sees
   exactly the intended access level.

## Stocking pages from templates

`references/templates.md` is the template library (meeting notes, decision log, technical spec, how-to, requirements,
retrospective, status report) — copy the matching template as the page's starting body. For org-wide template lifecycle
(design patterns, reusable components, storage-format scaffolding), the `atlassian-templates` skill is the source; reach
for it when you need a governed, deployable XHTML body rather than the markdown skeletons in `templates.md`.

1. Match the request to a template in `references/templates.md`; if none fits, define the repeatable structure yourself.
   **Done when** you have a body whose every placeholder is either filled or explicitly marked for the author.
2. Convert the body to storage-format XHTML, using `references/macro-cheat-sheet.md` for any macro. **Done when** the
   body contains zero wiki-markup macros (`{...}`) — all are `<ac:structured-macro>` form.
3. Create or update the page. **Done when** `getConfluencePage` returns the new body at the expected version and the
   rendered page shows every macro resolving (no unrendered markup, no broken Jira/excerpt references).

## Embedding Jira reports

1. Confirm the JQL or issue set with the user; collaborate with the Jira Expert skill for the query. **Done when** you
   have a validated JQL string or explicit issue keys.
2. Embed via the storage-format `jira` macro (syntax and columns in `references/macro-cheat-sheet.md`), then create or
   update the page. **Done when** the rendered page shows the Jira macro returning the expected rows, not an error
   lozenge.

## Auditing and governing the collection

Run a **content health audit** before any restructure or governance review, then act on it.

1. Export the space's page inventory (title, last-modified, view count, author, labels, word count) via
   `getPagesInConfluenceSpace` / `searchConfluenceUsingCql`. **Done when** the inventory covers every page in the target
   space or spaces.
2. Score every page against the five audit dimensions and thresholds in the **Content Health Audit** section of
   `references/space-architecture-patterns.md`. **Done when** each page is classified on all five dimensions — no page
   left unjudged.
3. Split the findings into an **archive list** and an **update backlog** per the reference, then execute: apply the
   `archived` label and move per the Archive Process (labels/moves via the UI, since label tools aren't on the MCP);
   split, expand, or complete backlog pages against the Page Quality Standards. **Done when** every flagged page appears
   on exactly one list and each list item has an owner and a next action.
4. Set the review cadence from the Content Governance section of the reference (critical monthly, standard quarterly,
   archive annually). **Done when** each retained page has a review cycle assigned.

## Escalate to an Atlassian admin

Route to the admin (not MCP, not the space UI) for: org-wide templates, cross-space permissions, blueprint
configuration, global automation rules, and space export/import.

## Related skills

- **Jira Expert** (`project-manager/jira-expert/`) — the JQL and issue linking behind embedded Jira macros
- **Atlassian Templates** (`project-manager/atlassian-templates/`) — org-wide template lifecycle and storage-format
  template bodies
