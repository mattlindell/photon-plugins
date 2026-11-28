# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Work item lifecycle

What happens to a ticket's status, and who does it, at each event of an unattended ticket run. Perform a row only when its actor is `agent`. Leave `automation` rows alone: the tracker makes those moves, so don't perform or check them. A `none` row has nothing to do. A row changes the assignee only when its action says so.

| Event | Actor | Action |
| --- | --- | --- |
| `start` | none | no status change |
| `review requested` | none | no status change |
| `PR merged` | none | no status change |
| `halt` | none | no status change |

A local issue has no workflow status. Its `Status:` line holds the triage role, which the Halt steps already change. A Stall has no row because it changes no status.

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Scouting operations

Used by `/scout`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md`. It holds the Destination, Notes, Decisions so far, Not yet specified, and Out of scope sections.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions so far in `map.md`.
