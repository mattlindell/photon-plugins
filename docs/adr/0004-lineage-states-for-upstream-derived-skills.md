# Lineage states for upstream-derived skills

Each skill derived from an upstream (Pocock's `skills`, or `pstack-claude`
including the `cursor-team-kit` skills it carries) records one of three lineage
states in its plugin's `NOTICE.md`: **tracked**, **derived**, or **own**. Until
now a NOTICE pinned one fork SHA per upstream, which answered "what did this
diverge from" but not "which skills does the next sync review need to read".
After one sync, those two questions have different answers per skill, and a
single pin cannot hold both.

| State | Meaning | NOTICE records |
| --- | --- | --- |
| **tracked** | Upstream changes are still ported into it | upstream path, and "reviewed through `<sha>`" |
| **derived** | Lineage only, no longer synced | upstream path, and "forked from `<sha>`" |
| **own** | No upstream text remains | normal authorship only |

Sync reviews compare tracked skills only. A derived skill's upstream is not
read again, which is the point of the state: a skill whose upstream fixes have
to be re-derived rather than applied costs a full review every sync and yields
nothing that applies.

## Demotion rule

A tracked skill becomes derived after **two consecutive sync reviews** in which
its upstream changes were skipped as "diverged" rather than ported. The sync
review makes the move and records it in the NOTICE, with the skill's last
"reviewed through" SHA becoming its "forked from" SHA.

One skip is not enough. A single review can skip a change for reasons local to
that change, and demoting on one would drop skills whose upstream still has
useful fixes coming. Two in a row means the skill and its upstream no longer
share a shape.

## Copyright is a separate obligation

The lineage state governs syncing. It does not govern attribution. Under MIT,
the copyright notice must travel with "all copies or substantial portions" of
the software, so it stays on a skill while any substantial portion of upstream
text survives, whether that skill is tracked or derived. Only **own** drops the
upstream copyright, and a skill reaches own only when no upstream text remains,
never because syncing stopped.

## Considered options

**One pin per upstream, as before.** Rejected. After the first sync, `scout`
(forked from Pocock's `wayfinder`) and `setup-ph-build` (whose tier ladder
replaced upstream's `models.json` generator) could not take upstream's changes,
while their siblings could. One pin claims both were reviewed through the same
commit, which is false for one of them.

**Drop the lineage for skills that stop syncing.** Rejected. It conflates the
two obligations above. Whether we still read a skill's upstream says nothing
about whether its text still derives from it.

## Consequences

- This refines [ADR-0001](0001-fork-pstack-rather-than-depend-on-it.md) rather
  than reversing it. ADR-0001 rejected keeping the fork tracked by sync tooling;
  "tracked" here means a human reads the changelog and ports by hand, which is
  the cost ADR-0001 accepted.
- A tracked pin claims "reviewed through here", so pins move last in a sync,
  after every port they vouch for has landed.
- A skill can carry two lineages with different states. `tdd` is tracked
  against Pocock's `tdd` and derived from pstack's for the escape-hatch
  conditions it absorbed.
