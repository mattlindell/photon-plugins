# NOTICE

Most of `ph-build` derives from MIT-licensed upstream work. All upstream
copyright notices and license terms are preserved.

Forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude) at
`a0a531f0e341144d12f0a26218b295ad5e8453a1` (v0.9.27), Michael Denyer's port of
Lauren Tan's (poteto) Cursor `pstack` plus seven skills from Cursor's
`cursor-team-kit`. A further six skills derive from
[Matt Pocock's skills](https://github.com/mattpocock/skills).

This is a **hard fork**. We carry none of upstream's sync tooling
([ADR-0001](../../docs/adr/0001-fork-pstack-rather-than-depend-on-it.md));
changes are ported by hand at each sync review. Each upstream-derived file
carries a lineage state, defined in
[ADR-0004](../../docs/adr/0004-lineage-states-for-upstream-derived-skills.md):
**tracked** files are reviewed through the pin, **derived** files keep their
lineage but are no longer synced. See [Lineage](#lineage).

| Upstream | Reviewed through |
| --- | --- |
| pstack-claude | `903e7385382389806c59d6989b6274e24165082b` (v0.9.101, 2026-10-21) |
| Matt Pocock's skills | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` (v1.3.1+47, 2026-10-19) |

## Upstream sources

**(c) 2026 Lauren Tan, MIT — [LICENSE-pstack](../../LICENSE-pstack)**

`architect`, `arena`, `babysit`, `benchmark-checklist`, `blast-radius`,
`correct`, `create-verification-skill`, `explain` (upstream `teach`),
`figure-it-out`, `how`, `interrogate`,
`maintain-verification-skill`, `no-comments`, `setup-ph-build` (upstream
`setup-pstack`), `show-me-your-work`, `swarm`, `typescript-best-practices`,
`why`, all 24 `principles/principle-*`, `agents/comment-sicko.md`, every file
under `skills/dispatch/playbooks/` except `implement-a-ticket.md`,
`skills/dispatch/references/bugbot-triage.md`, and `skills/dispatch/scripts/`.

**(c) 2026 Michael Denyer, MIT — [LICENSE-pstack](../../LICENSE-pstack)**

The pstack-claude port's own additions, carried alongside Lauren Tan's work:
the `babysit` skill, which upstream notes as independently authored by the port
rather than taken from Cursor's pstack; `skills/dispatch/references/merge-safety.md`;
and port-authored changes synced into the files above, including the `watch-pr`
and `worktree-audit` scripts under `skills/dispatch/scripts/` and the
`show-me-your-work` log script.

**(c) 2026 Matt Pocock, MIT — [LICENSE-pocock-skills](../../LICENSE-pocock-skills)**

`code-review`, `diagnosing-bugs`, `git-guardrails-claude-code`,
`setup-pre-commit`, `tdd`, and `wizard`. These came in through the old
`technical-director` plugin, whose skills were all taken from Pocock's
repository. `tdd` also absorbed upstream pstack's escape-hatch conditions.
`correct` merges in the categories from Pocock's `retro` skill: navigation
pointers, tool economy, information access, and no-ops.

**(c) 2026 Cursor, MIT — [LICENSE-cursor-team-kit](../../LICENSE-cursor-team-kit)**

`deslop`, `fix-ci`, `fix-merge-conflicts`, `get-pr-comments`,
`make-pr-easy-to-review`, `thermo-nuclear-code-quality-review`.
`thermo-nuclear-review` comes from Cursor's `thermos` plugin, whose MIT license
text is identical to `cursor-team-kit`'s.

## Lineage

Upstream paths are relative to each upstream repository's root. Every
pstack-claude path sits under `plugins/pstack/`, shortened to `…/` below.

### pstack-claude

| Here | Upstream | State |
| --- | --- | --- |
| `skills/architect/` | `…/skills/architect/` | tracked, reviewed through `903e738` |
| `skills/arena/` | `…/skills/arena/` | tracked, reviewed through `903e738` |
| `skills/babysit/` | `…/skills/babysit/` | tracked, reviewed through `903e738` |
| `skills/benchmark-checklist/` | `…/skills/benchmark-checklist/` | tracked, reviewed through `903e738` |
| `skills/blast-radius/` | `…/skills/blast-radius/` | tracked, reviewed through `903e738` |
| `skills/correct/` | `…/skills/correct/` | tracked, reviewed through `903e738` |
| `skills/create-verification-skill/` | `…/skills/create-verification-skill/` | tracked, reviewed through `903e738` |
| `skills/deslop/` | `…/skills/deslop/` | tracked, reviewed through `903e738` |
| `skills/explain/` | `…/skills/teach/` | tracked, reviewed through `903e738` |
| `skills/figure-it-out/` | `…/skills/figure-it-out/` | tracked, reviewed through `903e738` |
| `skills/fix-ci/` | `…/skills/fix-ci/` | tracked, reviewed through `903e738` |
| `skills/fix-merge-conflicts/` | `…/skills/fix-merge-conflicts/` | tracked, reviewed through `903e738` |
| `skills/get-pr-comments/` | `…/skills/get-pr-comments/` | tracked, reviewed through `903e738` |
| `skills/how/` | `…/skills/how/` | tracked, reviewed through `903e738` |
| `skills/interrogate/` | `…/skills/interrogate/` | tracked, reviewed through `903e738` |
| `skills/maintain-verification-skill/` | `…/skills/maintain-verification-skill/` | tracked, reviewed through `903e738` |
| `skills/make-pr-easy-to-review/` | `…/skills/make-pr-easy-to-review/` | tracked, reviewed through `903e738` |
| `skills/no-comments/` | `…/skills/no-comments/` | tracked, reviewed through `903e738` |
| `skills/setup-ph-build/` | `…/skills/setup-pstack/` | **derived**, forked from `a0a531f` |
| `skills/show-me-your-work/` | `…/skills/show-me-your-work/` | tracked, reviewed through `903e738` |
| `skills/swarm/` | `…/skills/swarm/` | tracked, reviewed through `903e738` |
| `skills/tdd/` (escape-hatch conditions only) | `…/skills/tdd/` | **derived**, forked from `a0a531f` |
| `skills/thermo-nuclear-code-quality-review/` | `…/skills/thermo-nuclear-code-quality-review/` | tracked, reviewed through `903e738` |
| `skills/thermo-nuclear-review/` | `…/skills/thermo-nuclear-review/` | tracked, reviewed through `903e738` |
| `skills/typescript-best-practices/` | `…/skills/typescript-best-practices/` | tracked, reviewed through `903e738` |
| `skills/why/` | `…/skills/why/` | tracked, reviewed through `903e738` |
| `skills/principles/principle-*/` (all 24) | `…/skills/principle-*/` | tracked, reviewed through `903e738` |
| `skills/dispatch/playbooks/` (all but `implement-a-ticket.md`) | `…/skills/poteto-mode/playbooks/` | tracked, reviewed through `903e738` |
| `skills/dispatch/references/` | `…/skills/poteto-mode/references/` | tracked, reviewed through `903e738` |
| `skills/dispatch/scripts/` | `…/skills/poteto-mode/scripts/` | tracked, reviewed through `903e738` |
| `agents/comment-sicko.md` | `…/agents/comment-sicko.md` | tracked, reviewed through `903e738` |

`setup-ph-build` is derived because its tier ladder, caps, and policy file
replace upstream's `models.json` generator, so upstream's model-policy changes
cannot apply to it. `dispatch/SKILL.md` is own work: it replaces upstream's
`poteto-mode/SKILL.md` outright, while the playbooks, references, and scripts
under it stay tracked against `poteto-mode`'s.

### Matt Pocock's skills

| Here | Upstream | State |
| --- | --- | --- |
| `skills/code-review/` | `skills/engineering/code-review/` | tracked, reviewed through `5beb35b` |
| `skills/correct/` (`retro` categories only) | `skills/engineering/retro/` | tracked, reviewed through `5beb35b` |
| `skills/diagnosing-bugs/` | `skills/engineering/diagnosing-bugs/` | tracked, reviewed through `5beb35b` |
| `skills/git-guardrails-claude-code/` | `skills/misc/git-guardrails-claude-code/` | tracked, reviewed through `5beb35b` |
| `skills/setup-pre-commit/` | `skills/misc/setup-pre-commit/` | tracked, reviewed through `5beb35b` |
| `skills/tdd/` | `skills/engineering/tdd/` | tracked, reviewed through `5beb35b` |
| `skills/wizard/` | `skills/engineering/wizard/` | tracked, reviewed through `5beb35b` |

`tdd` and `correct` each carry both lineages, so each appears in both tables.

## Own work

**(c) 2026 Matt Lindell, MIT.** `skills/dispatch/SKILL.md` (new — replaces
upstream's `poteto-mode` router), `skills/dispatch/playbooks/implement-a-ticket.md`,
`claude-md`, `commit`, `worktree`, `agents/implement.md`,
`agents/code-review.md`, and `hooks/session-start-context.md`.

## Modifications

Per the MIT license, modifications are permitted. This fork is editorial, not
mechanical — the changes below are the point of forking rather than depending.

**Cost model.** Upstream has no mechanism that lowers rigor because work is
already specified; its only escape hatches key on task *triviality*. This fork
adds one:

- `dispatch` reads a `settled:` block before anything else and skips the phases
  owning already-closed dimensions.
- Expensive multi-agent work is gated behind **one-way doors** rather than
  running unconditionally.
- Every fan-out skill gained a **hard cap** it did not have. `swarm` had no
  default and no ceiling; `arena`'s invitation to "spawn more" is removed;
  `why` capped at four investigators; `maintain-verification-skill` capped at
  five readers.
- `opening-a-pr` ran `interrogate` plus `/deslop` plus `/no-comments` on the tail
  of *every* playbook — a flat four agents per run. `interrogate` is now
  conditional on a one-way door.
- `feature` step 4's mandatory delegation ("no skip-with-reason escape") is now
  conditional on size and on one-way doors.
- `show-me-your-work` spawned a cross-model reviewer every run; now conditional.
- `architect` Phase C keeps its no-human-checkpoint default, correct for an
  unattended harness, but gained a one-way-door exception.

**Model policy.** Upstream stamps Claude model slugs into skill bodies from a
`models.json` via a generator. Both are dropped. Skills now name a **tier** on a
strict ladder (`scan` < `scoped` < `judgment` < `divergent` < `panel`); the
tier-to-model mapping is per-harness and written by `setup-ph-build`, which also
holds the caps and per-playbook budgets. No model identifier appears in any
skill body.

**Dropped.** `poteto-mode` (rewritten as `dispatch`), the `poteto-agent` agent,
and four playbooks whose cost is unbounded by design: `orchestrate` ("dozens to
hundreds of subagents"), `autopilot-full`, `autopilot-stack`, and
`multi-phase-plan` (13 swarm lanes per PR head, and it duplicates
`ph-plan:scout`). Upstream's `tdd` merged into this fork's `tdd`. Codex
platform-mapping pointers and the `.codex-plugin` build are not carried.

**Invocation.** Every upstream skill was model-invocable, which is why the
machinery fired unprompted. `architect`, `arena`, `interrogate`, `swarm`,
`thermo-nuclear-review`, `thermo-nuclear-code-quality-review`, and
`maintain-verification-skill` are now user-invoked only, as is `correct`.
Capability retained; auto-invocation removed. `thermo-nuclear-review` runs
inline; upstream's `thermo-nuclear-review-subagent` agent is not carried.

**Cross-plugin.** References to skills that moved to `ph-lib` are namespaced.
References into `ph-plan` are optional with a defined fallback, so `ph-build`
runs standalone.
