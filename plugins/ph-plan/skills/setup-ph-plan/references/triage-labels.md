# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the "Label in our tracker" column to match whatever vocabulary you actually use.

## Claim roles

`/ph-build:foreman` records a Claim on a ticket with one of three Claim roles. They sit alongside the triage roles and are not part of the triage state machine. A ticket carries at most one Claim role at a time.

| Claim role      | Written as            | Meaning                                       |
| --------------- | --------------------- | --------------------------------------------- |
| `agent-claimed` | label `agent-claimed` | The Foreman has the ticket; no Worker started |
| `agent-working` | label `agent-working` | A Worker is building it                       |
| `agent-stalled` | label `agent-stalled` | The Worker ran too long; a human should look  |

Each role defaults to a plain label named after it. To use a custom field instead, write the field and its value in the "Written as" column, for example `field "Agent Status" = Working`. The Foreman never creates labels or fields, so whatever this table names must already exist on the tracker.
