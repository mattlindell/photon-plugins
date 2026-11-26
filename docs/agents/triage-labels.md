# Triage Labels

The skills speak in terms of five canonical triage roles. In Linear these are **labels** (children of the workspace-level **"Agentic State Machine"** label group), distinct from workflow *statuses* (see `issue-tracker.md`, which also defines the `<TEAM>` placeholder). Each role maps 1:1 to an existing label, with no overrides.

| Canonical role    | Linear label      | Meaning                                  |
| ----------------- | ----------------- | ---------------------------------------- |
| `needs-triage`    | `needs-triage`    | Maintainer needs to evaluate this issue  |
| `needs-info`      | `needs-info`      | Waiting on reporter for more information |
| `ready-for-agent` | `ready-for-agent` | Fully specified, ready for an AFK agent  |
| `ready-for-human` | `ready-for-human` | Requires human implementation            |
| `wontfix`         | `wontfix`         | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), add the corresponding Linear label **by name** to the issue's existing labels, using whatever Linear access the runner has. These labels already exist, so don't create new ones. Replace the label set only when you mean to drop the others.

Raw label UUIDs (for disambiguation or to skip a lookup) live in `docs/agents/linear-ids.local.md` (gitignored, not committed); resolve by name if that file is absent.

> The labels are defined at the **workspace** level, not on the team, so a label listing scoped to
> `<TEAM>` returns nothing. List them unscoped.
