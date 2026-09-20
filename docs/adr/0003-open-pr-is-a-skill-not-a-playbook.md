# open-pr is a skill, not a playbook

`ph-build` has two routes into building code and, until this decision, only one
of them could reach the procedure for opening a PR. Anything entering through
`dispatch` lands in a playbook whose last step is "Run **Opening a PR**" — seven
playbooks do this. The `implement` agent never touches `dispatch`; it runs tdd,
code-review, and commit, then stops, because pushing and opening a PR are
outward-facing acts it waits for a human to authorize. So the best PR document
in the repo was structurally unreachable from the route a human actually drives,
and `deslop` and `no-comments` — which that document mandates — had never fired
on it.

The prose moved to `plugins/ph-build/skills/open-pr/SKILL.md` and
`skills/dispatch/playbooks/opening-a-pr.md` was deleted. `dispatch` keeps the
bullet, retargeted, so the seven callers are untouched and the same text serves
both routes.

## Considered options

**A skill that points at the playbook file.** Rejected. A `SKILL.md` whose body
is one pointer buys nothing, and the pointer would cross from a skill into
another skill's private `playbooks/` directory.

**A skill that restates the playbook.** Rejected outright — two copies of a
procedure drift, which is the same argument [ADR-0002](0002-ph-lib-is-a-library-not-a-hat.md)
makes for `ph-lib`.

**Make `implement` call `dispatch`.** Rejected. It couples the two routes to get
one file, and `implement` stops before outward-facing acts on purpose.

## Consequences

- **A playbook is a named end-to-end procedure that sequences skills.** Opening a
  PR was never that. It is one procedure a human invokes, which is what a skill
  is here. The count in the manifests drops to 18 playbooks, and `dispatch`'s
  section 4 list now carries one bullet that resolves outside `playbooks/`.
- **It ships user-invoked** (`disable-model-invocation: true`). Reading a file is
  not invoking it, so an unattended `dispatch` subagent still reaches the body by
  path. The version cost picks the direction. Removing the flag later is a minor
  bump and adding it later is a major one, so ship the cheap direction first.
- **One body covers two audiences.** The main body addresses a human on a
  finished branch. A closing section carries the unattended rules and the
  worktree discipline, which only applies when there is fan-out.
- **A dangling pointer here would pass CI.** `scripts/lint-links.py` matches
  markdown link syntax and cannot see the backtick paths `dispatch` uses, so
  `grep -rn "opening-a-pr" plugins/` is the check that actually guards the
  retarget. Extending the validator is filed separately.
