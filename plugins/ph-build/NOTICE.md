# NOTICE

Most of `ph-build` derives from MIT-licensed upstream work. All upstream
copyright notices and license terms are preserved.

Forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude) at
`a0a531f0e341144d12f0a26218b295ad5e8453a1` (v0.9.27), which is itself a port of
Lauren Tan's Cursor `pstack` plus seven skills from Cursor's `cursor-team-kit`.

This is a **hard fork**. We do not track upstream and carry none of its sync
tooling — the SHA above is pinned so anyone can answer what this diverged from.
See [ADR-0001](../../docs/adr/0001-fork-pstack-rather-than-depend-on-it.md).

## Upstream sources

**(c) 2026 Lauren Tan, MIT — [LICENSE-pstack](../../LICENSE-pstack)**

`architect`, `arena`, `babysit`, `blast-radius`, `create-verification-skill`,
`explain` (upstream `teach`), `figure-it-out`, `how`, `interrogate`,
`maintain-verification-skill`, `no-comments`, `setup-ph-build` (upstream
`setup-pstack`), `show-me-your-work`, `swarm`, `typescript-best-practices`,
`why`, all 23 `principles/principle-*`, `agents/comment-sicko.md`, every file
under `skills/dispatch/playbooks/`, `skills/dispatch/references/bugbot-triage.md`,
and `skills/dispatch/scripts/`.

Upstream's `babysit` skill is noted there as independently authored by the
pstack-claude port rather than taken from Cursor's pstack; it travels under the
same MIT terms.

**(c) 2026 Cursor, MIT — [LICENSE-cursor-team-kit](../../LICENSE-cursor-team-kit)**

`deslop`, `fix-ci`, `fix-merge-conflicts`, `get-pr-comments`,
`make-pr-easy-to-review`, `thermo-nuclear-code-quality-review`.

## Own work

**(c) 2026 Matt Lindell, MIT.** `dispatch` (new — replaces upstream's
`poteto-mode` router), `code-review`, `diagnosing-bugs`, `implement`, `wizard`,
`git-guardrails-claude-code`, `setup-pre-commit`, `claude-md`, `commit`,
`worktree`, `agents/implement.md`, `agents/code-review.md`, and
`hooks/session-start-context.md`. `tdd` is own work that absorbed upstream's
escape-hatch conditions.

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
`thermo-nuclear-code-quality-review`, and `maintain-verification-skill` are now
user-invoked only. Capability retained; auto-invocation removed.

**Cross-plugin.** References to skills that moved to `ph-lib` are namespaced.
References into `ph-plan` are optional with a defined fallback, so `ph-build`
runs standalone.
