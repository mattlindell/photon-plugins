# Upstreams

This marketplace hard-forks two MIT-licensed upstreams and ports their changes
by hand. This page shows where each one stands. The record behind it is
[`upstreams.json`](upstreams.json).

| Upstream | What it is | Feeds |
| --- | --- | --- |
| pstack-claude | Michael Denyer's port of Lauren Tan's (poteto) Cursor `pstack`, plus skills from Cursor's `cursor-team-kit` | Most of `ph-build`, seven `ph-lib` skills |
| pocock-skills | Matt Pocock's `skills` repository | Eleven `ph-plan` skills, six `ph-build` skills, six `ph-lib` skills |

## Pins

The Pin is the upstream commit the last Sync review read through. It means
*reviewed*, not *applied*: a port deferred out of a review is recorded as owed
in the Sync log, and the Pin moves past it. Compare a Pin against the
upstream's recent commits to decide whether a sync is worth running.

<!-- BEGIN GENERATED: pins. Edit upstreams.json, then run lint-upstreams.py --apply -->
| Upstream | Pin | Version | Committed | Reviewed | Forked from |
| --- | --- | --- | --- | --- | --- |
| [pstack-claude](https://github.com/michael-denyer/pstack-claude) | [`903e738`](https://github.com/michael-denyer/pstack-claude/commit/903e7385382389806c59d6989b6274e24165082b) | v0.9.101 | 2026-10-21 | 2026-10-23 | `a0a531f` (v0.9.27) |
| [pocock-skills](https://github.com/mattpocock/skills) | [`5beb35b`](https://github.com/mattpocock/skills/commit/5beb35b040e3de97e54fa9e386d7e42d15c295c2) | v1.3.1+47 | 2026-10-19 | 2026-10-23 | `84fdeff` (v1.2.3) |
<!-- END GENERATED: pins -->

The pocock-skills fork point is the earliest recorded sync. The skills came in
earlier through the old `technical-director` plugin, which recorded no SHA.

## Why a hard fork

We carry none of upstream's sync tooling and take only what fits our cost model
and harness split. Each decision has an ADR:

- [ADR-0001](docs/adr/0001-fork-pstack-rather-than-depend-on-it.md): fork pstack
  rather than depend on it.
- [ADR-0004](docs/adr/0004-lineage-states-for-upstream-derived-skills.md): each
  upstream-derived skill is Tracked, Derived, or Own, and two consecutive
  `diverged` outcomes demote a Tracked skill to Derived.
- [ADR-0006](docs/adr/0006-upstream-record.md): Pins and the Sync log live in
  `upstreams.json`, and NOTICE files keep lineage and copyright only.

Each plugin's `NOTICE.md` lists which of its skills come from which upstream,
and whether each is Tracked or Derived:
[ph-build](plugins/ph-build/NOTICE.md), [ph-lib](plugins/ph-lib/NOTICE.md),
[ph-plan](plugins/ph-plan/NOTICE.md).

## Running a Sync review

Run `/sync-upstream <name>` from this repository once you have decided the
upstream has changes worth taking. The repo-local `sync-upstream` skill is not
built yet. Until it is, a review follows the same steps by hand, as one PR:

1. List the upstream's commits since the Pin that touch a Tracked path, and any
   upstream skills we do not carry.
2. Port what fits, one commit per change. Defer a large port as `owed` with a
   ticket instead of holding the Pin back.
3. Demote any skill whose outcome is `diverged` for the second review running.
   Its NOTICE row becomes `**derived**, forked from <short sha>`.
4. As the last commit, append a Sync log entry to `upstreams.json` with an
   outcome for every Tracked path and a decision for every candidate, move the
   Pin, and run `python scripts/lint-upstreams.py --apply`.
