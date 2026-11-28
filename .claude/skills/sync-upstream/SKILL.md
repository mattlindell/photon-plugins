---
name: sync-upstream
description: Run one Sync review of an upstream as a single PR, ending with the Sync log entry and the Pin move.
argument-hint: <upstream name from upstreams.json>
disable-model-invocation: true
---

# Sync upstream

Run one Sync review of the upstream named in `$ARGUMENTS`, as one PR. The rules
are [ADR-0004](../../../docs/adr/0004-lineage-states-for-upstream-derived-skills.md)
(lineage states, demotion) and [ADR-0006](../../../docs/adr/0006-upstream-record.md)
(the record, Pin means *reviewed*). The vocabulary is in
[CONTEXT.md](../../../CONTEXT.md#upstream): Pin, Sync review, Sync log, Tracked,
Derived.

The commit order is the contract. Ports, then demotions, then version bumps, and
the Sync log entry with the Pin move is the **last** commit. Every commit before
it leaves the old Pin in place.

## 1. Analyze

Branch from an up-to-date `main` as `chore/sync-<name>-<YYYY-MM-DD>`, then keep
a clone for porting:

```bash
clone="$(mktemp -d)/<name>"
python .claude/skills/sync-upstream/scripts/analyze_upstream.py <name> --clone-into "$clone" > "$clone.md"
```

The report lists every Tracked path with its commits since the Pin, the Tracked
paths upstream left alone, and the candidates: upstream changes under no lineage
row, grouped by upstream skill. It also prints the new Pin's `sha`, `version`,
and `committed` fields. A non-zero exit means the record, a NOTICE row, or the
clone is wrong. Fix that in its own PR; a review cannot run against a bad
record.

Done when the report exists and every Tracked path appears in it exactly once.

## 2. Triage and port

Give every Tracked path one outcome, including the unchanged ones:

| Outcome | When |
| --- | --- |
| `ported` | You applied the upstream change, in full or the parts that fit. |
| `no-change` | Upstream did not touch the path, or touched it in ways that need nothing here. |
| `diverged` | The change matters upstream but cannot apply here because this skill no longer shares upstream's shape. |
| `owed` | The change fits but is too large for this PR. File a ticket per [`docs/agents/issue-tracker.md`](../../../docs/agents/issue-tracker.md) and record `{"state": "owed", "ticket": "<key>"}`. The Pin still moves past it. |

Read each change with `git -C "$clone" show <sha> -- <upstream path>`, then the
file it lands in here. The NOTICE row maps the upstream path to ours. Several
skills were renamed, and the NOTICE's Layout note says which companion files moved into
`references/`. Port onto that path. Write ported text in American English and
in this repository's names (`ph-lib:`, tier names, `CONTEXT.md`), as the NOTICE
Modifications section describes.

Commit each ported skill on its own, naming the upstream short SHAs in the
body.

Done when every Tracked path in the report has an outcome and a one-line
reason.

## 3. Candidates

Decide each candidate group: `adopted`, `declined`, or `owed` with a ticket. A
group marked **previously declined** stays declined unless its new commits
change the case. Say what changed if you reopen it. The group of changes outside
any upstream skill needs a decision only where it adds something this
marketplace could carry, such as an agent or a playbook.

Adopting a candidate adds a skill. Follow the add-a-skill steps in `CLAUDE.md`,
add a `tracked` row to the right NOTICE lineage table, and record the new path as
`ported` in step 5. A large adoption is `owed` instead.

## 4. Demote

Change a NOTICE row from `tracked` to `` **derived**, forked from `<short sha>` ``
when:

- its outcome is `diverged` and the report says its last outcome was also
  `diverged`. It forks from the old Pin.
- the report says upstream **deleted** it. It forks from the commit the report
  names, the last one that carried the file. Its outcome is `diverged`.
- the report names one deleted skill under a glob row, such as
  `principle-*`. Add a row for that skill alone, beside the glob row, and demote
  the new row. Update any count in the glob row's text. The glob row stays
  `tracked` and keeps its own outcome.

Add a sentence under the table saying why, as the existing derived rows have.
Commit the demotions together.

## 5. Record and move the Pin

Run `python scripts/bump-versions.py --worktree`. Apply and commit any bump it
asks for before this step.

Append one entry to this upstream's `log` in `upstreams.json`:

- `date`: today. `from`: the old Pin SHA. `to`: the new Pin SHA from the report.
- `pr`: this PR's URL. Predict its number as one past the highest issue or PR
  number in the repository (`gh api 'repos/{owner}/{repo}/issues?state=all&per_page=1' --jq '.[0].number'`),
  and check it once the PR exists.
- `outcomes`: every path that was Tracked when the review started, keyed exactly
  as its NOTICE row, including any you just demoted.
- `candidates`: every decided group, by name, with `ticket` on an `owed` one.

Replace `pin` with the report's new Pin and set `reviewed` to today. Then run
`python scripts/lint-upstreams.py --apply` to regenerate the `UPSTREAMS.md` table
and commit `upstreams.json` with `UPSTREAMS.md`. Nothing is committed after this.

## 6. Check and open the PR

Run every check in `CLAUDE.md`'s Checks section. That covers the five repo
checks, and the script and plugin tests when a port touched a script. Fix
failures in a commit before the record commit, never after it.

Push and open the PR titled `chore(upstreams): sync <name> to <short sha>`. Its
description holds the report from step 1, a table of every Tracked path with its
outcome and reason, the candidate decisions, the demotions, and the owed
tickets. If the PR number differs from the one you predicted, amend the record
commit's `pr` and force-push the branch with `--force-with-lease`.

Delete the clone.
