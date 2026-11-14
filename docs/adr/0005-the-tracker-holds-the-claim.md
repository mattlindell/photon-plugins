# The tracker holds the claim

A Foreman's record that it has taken a ticket is stored on the ticket itself:
the assignee, the time the ticket entered In Progress, and one claim role from
`agent-claimed`, `agent-working`, or `agent-stalled`. Local files are never the
record. The only local state is a hand-off directory, which tells the harness
driver which Workers to start. Each Foreman run first reconciles every live
claim from the tracker. Only after that does it count free slots or claim
anything new.

We first tried local state, in the `ph-heartbeat` setup on Kiro Crew. The
claim lived as a file that moved through `queue/`, `started/`, and `done/`, and
the tracker was updated alongside it. With two records of one fact, any crash
between the two writes left them disagreeing. That produced three defects:

- A halted ticket stayed in `done/`, so it was never picked up again.
- A Worker that died never moved its file out of `started/`, so its slot was
  held forever.
- A claim written to the tracker before its queue file was orphaned when the
  run died in between.

Each defect was the two records diverging. The fix was to have one record, not
better synchronization.

We record claims in fields because fields can be queried and comments can't. A
claim role is a filter (`labels = agent-working`). Neither tracker can query
the age of a label, so the clock is the In Progress transition: in Jira,
`CHANGED TO "In Progress"`, and in Linear, `startedAt`. Comments are kept for
text a human has to read, and only a halt produces one.

## Consequences

- **Recovery comes from reconciling.** An orphan is a ticket still
  `agent-claimed` past its threshold, and it is requeued. A stall is a ticket
  still `agent-working` past its threshold, and it is flagged. Both repairs can
  run any number of times. A lost hand-off directory costs one reconcile.
- **Ticks cost model turns only when there is work.** The driver ticks for
  free. Reconciling runs inside the Foreman's existing model turn, so the
  tracker reads add no extra runs.
- **Each repo must be able to record the roles.** In Jira, labels are created
  on first use. In Linear, they must be created ahead of time. A repo can map
  the roles to a custom field in `triage-labels.md` instead. When the tracker
  rejects a role, the Foreman notifies and claims nothing.
- **Claims are per user, not per Foreman.** Live claims are counted across
  every repo for the current tracker user. Two Foremen running under one
  account share a single pool of Worker slots.
