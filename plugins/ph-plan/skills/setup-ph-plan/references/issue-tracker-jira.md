# Issue tracker: Jira

Tickets for this repo live in Jira, in project `<PROJECT_KEY>` on `<SITE>`. Where specs, scout maps, and research findings live is set in **Specs, maps, and research** below. `CONTEXT.md` and `docs/adr/` stay in this repo (see `domain.md`).

Use whatever access to Jira the runner already has for every operation below, and the same for the wiki when specs live there. When an operation isn't available through that access, tell the person instead of switching to a different connection.

## Instance

- **Site:** `<SITE>`
- **Jira project:** `<PROJECT_KEY>`
- **Ticket issue type:** `<ISSUE_TYPE>`
- **Effort issue type:** `<EFFORT_TYPE>`, the type one level above `<ISSUE_TYPE>` in the project's hierarchy

## Efforts

An **effort** is a body of work planned together. In Jira, each effort is a **parent issue** of type `<EFFORT_TYPE>` in `<PROJECT_KEY>`. Its tickets are its children. Its description is the effort's index: a line on what the effort is for, then a link to each spec, map, and research artifact.

A spec or ticket names its effort, usually by the parent's key. When nothing names it and more than one effort fits, ask. When a skill publishes the first artifact for new work, create the effort parent first.

Title artifacts by kind so people and agents can find them: `Spec: <name>`, `Map: <effort>`, `Research: <topic>`.

## Jira conventions

- Every ticket is a `<ISSUE_TYPE>` issue whose parent is the effort.
- Fields skills use: `summary`, `description` (Markdown), and `labels`. Triage state is in `triage-labels.md`.
- **Create:** an issue in `<PROJECT_KEY>` with type `<ISSUE_TYPE>` and the effort as its parent.
- **Sub-issue of another ticket:** keep the effort as the parent, and write `Part of <PROJECT_KEY>-<n>` as the first line of the description.
- **Read:** the ticket by key, then its comments. The comments often carry the constraints that matter.
- **Search:** JQL, for example `parent = <PROJECT_KEY>-<effort> AND statusCategory != Done ORDER BY created ASC`.
- **Comment:** add a comment to the ticket. **Edit labels or fields:** edit the ticket.
- **Labels:** Jira creates a label the first time an issue uses it. Never create labels ahead of time.
- **Transition:** list the ticket's available transitions, then use the one whose target status is in the Done category. Never guess transition ids.
- **Blocking:** link type **Blocks**. The blocker "blocks" the blocked ticket. A ticket is unblocked when every "is blocked by" issue is in the Done category.

## Specs, maps, and research

### In the wiki

Specs, maps, and research findings are pages in the `<SPACE_KEY>` space. Each effort has an **effort page**, a child of "`<SPECS_PAGE>`", titled with the effort's name and linked from the effort parent's description. Every artifact for the effort is a child of its effort page.

- **Create every page as an unpublished draft.** A person publishes it.
- **Read:** a page by id or URL. For an unpublished page, read the draft version. **Update:** update the draft until the page is published.
- **Find a page:** search skips drafts. List the effort page's children instead and match the title.
- **Spec:** a child page titled `Spec: <name>`. Link it from the effort parent's description and from each ticket built from it.
- **Research finding:** a child page titled `Research: <topic>`, linked from the ticket that asked the question.
- **Map:** a child page titled `Map: <effort>`.

### As Jira issues

Specs, maps, and research findings are `<ISSUE_TYPE>` issues under the effort parent, beside its tickets. The title prefix tells them apart from tickets.

- **Spec:** an issue titled `Spec: <name>`, with the spec as its description. Link it from the effort parent's description and from each ticket built from it.
- **Research finding:** an issue titled `Research: <topic>`, linked from the ticket that asked the question with link type **Relates**.
- **Map:** an issue titled `Map: <effort>` and labeled `scout:map`.
- Specs, maps, and research findings never carry triage labels.

## When a skill says "publish to the issue tracker"

A ticket becomes a `<ISSUE_TYPE>` issue under the effort parent. A spec or PRD goes where **Specs, maps, and research** says, linked from the effort parent's description.

Triage labels go on tickets only. When a skill asks you to label a spec, skip it. The spec's `settled:` block shows whether it's ready.

## When a skill says "fetch the relevant ticket"

Read the ticket by key (for example `<PROJECT_KEY>-123`), then read its comments. For a spec, read it where **Specs, maps, and research** says.

## Scouting operations

Used by `/scout`. The **map** goes where **Specs, maps, and research** says. Its **children** are Jira tickets under the effort parent.

- **Map:** `Map: <effort>`. It holds the Destination, Notes, Decisions so far, Not yet specified, and Out of scope sections.
- **Child ticket:** a `<ISSUE_TYPE>` issue under the effort parent, labeled `scout:<type>` (`research`, `prototype`, `grilling`, or `task`), with the question in the description.
- **Blocking:** Blocks links, as above.
- **Frontier:** JQL `parent = <PROJECT_KEY>-<effort> AND labels in (scout:research, scout:prototype, scout:grilling, scout:task) AND statusCategory != Done AND assignee is EMPTY ORDER BY created ASC`. Drop any issue with an open "is blocked by" link. The first one left wins.
- **Claim:** assign the ticket to the current user. This is the session's first write.
- **Resolve:** post the answer as a comment, or as a `Research:` artifact linked from the comment. Transition the ticket to Done. Then append a one-line pointer (the gist plus the issue link) to the map's Decisions so far.
