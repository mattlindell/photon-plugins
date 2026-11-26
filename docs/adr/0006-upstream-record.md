# Upstream record

Each upstream's Pin, fork point, and Sync log live in one machine-readable file,
`upstreams.json` at the repository root. `NOTICE.md` files no longer restate any
upstream SHA for a tracked skill. This amends
[ADR-0004](0004-lineage-states-for-upstream-derived-skills.md), whose "NOTICE
records" column put a "reviewed through" SHA on every tracked row.

Under ADR-0004 the Pocock pin appeared in three NOTICE headers and about thirty
table rows, the pstack pin in two headers and about thirty more. Nothing checked
that they agreed, the current version could not be found at a glance, and the
demotion rule depended on a skip history nobody recorded.

## Decisions

**`upstreams.json` is the source of truth.** Per upstream: name, repository URL,
fork point (SHA, version), Pin (SHA, version label, commit date, reviewed date),
and the Sync log. Each log entry records date, from and to SHA, PR link, a
per-skill `outcomes` map, and a `candidates` list of untracked upstream
additions with the decision taken on each.

- `outcomes` keys are repository paths as they appear in NOTICE lineage rows.
  A skill with two lineages appears under each upstream's entry separately.
- An outcome is `ported`, `no-change`, `diverged`, or `owed`. `owed` carries a
  ticket reference.
- A fifth outcome, `unrecorded`, is allowed only in an entry marked
  `backfilled`, where git history does not say what a review decided. The
  demotion rule treats it as not diverged.
- Every entry records an outcome for every path that is tracked when it is
  written. A review that leaves a skill out would make the demotion rule count
  two non-adjacent `diverged` outcomes as consecutive.

**A Pin means reviewed, not applied.** ADR-0004 moved the pin only after every
port it covered had landed, so one large deferred port would stall the pin for
the whole upstream and the pin would stop saying what had been read. A deferred
port is now recorded as `owed` and the Pin moves past it.

**`UPSTREAMS.md` is the human view.** A short page: what each upstream is, how
to run a Sync review, and a Pin table generated from the JSON between marker
comments. Nothing in it is hand-copied from the JSON.

**NOTICE rows keep lineage, not pins.** A tracked row reads `tracked` and
inherits the Pin. A derived row keeps `**derived**, forked from <sha>`, because
that value is genuinely per-skill.

**A check enforces it.** `scripts/lint-upstreams.py` fails when a NOTICE carries
a full SHA or a "reviewed through" phrase; a lineage state is malformed; a NOTICE
names an upstream absent from the JSON; the newest log entry does not end at the
Pin, or an entry does not start where the one before it ended; the generated
block is stale; the newest entry omits a tracked row, or a skill is still
`tracked` after two consecutive `diverged` outcomes; or an `outcomes` path does
not exist on disk.
`--apply` rewrites the generated block.

**A repo-local skill runs the review.** `.claude/skills/sync-upstream/` performs
analysis, ports, demotions, the log entry, and the Pin move as one PR, with the
log and Pin commit last. It ships in no plugin.

## Considered options

**Keep NOTICE files as the truth and check that they agree.** Rejected. It
leaves sixty-odd copies of two values and still has nowhere to record per-skill
outcomes.

**A markdown `UPSTREAMS.md` holding pins and log as tables.** Rejected. Two
scripts must parse the record, and a hand-maintained markdown table is a fragile
parse target that grows without bound.

**Generate NOTICE tables from the JSON.** Rejected. The NOTICE carries license
obligations and editorial notes that do not belong in a data file, and
generating it edges toward the sync tooling ADR-0001 declined.

## Consequences

- This is a record, not sync tooling. Ports remain manual, as ADR-0001 accepted.
- The demotion rule of ADR-0004 becomes mechanically checkable.
- Past reviews are backfilled from git history. Where history does not record
  a per-skill outcome, the entry says so rather than inventing one.
