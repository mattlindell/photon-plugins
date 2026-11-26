# NOTICE

Eleven of the thirteen skills in `ph-plan` derive from
[Matt Pocock's skills](https://github.com/mattpocock/skills), MIT-licensed. All
upstream copyright notices and license terms are preserved.

**(c) 2026 Matt Pocock, MIT — [LICENSE-pocock-skills](../../LICENSE-pocock-skills)**

This is a hard fork. Nothing syncs upstream automatically; we port changes by
hand at each sync review. Each skill below carries a lineage state, defined in
[ADR-0004](../../docs/adr/0004-lineage-states-for-upstream-derived-skills.md):
**tracked** skills are synced at each review, **derived** skills keep their
lineage but are no longer synced. The current Pin is in
[UPSTREAMS.md](../../UPSTREAMS.md).

## Upstream sources

Upstream paths are relative to the root of `mattpocock/skills`.

### pocock-skills

| Skill | Upstream | State |
| --- | --- | --- |
| `skills/domain-modeling/` | `skills/engineering/domain-modeling/` | tracked |
| `skills/grilling/` | `skills/productivity/grilling/` | tracked |
| `skills/improve-codebase-architecture/` | `skills/engineering/improve-codebase-architecture/` | tracked |
| `skills/prototype/` | `skills/engineering/prototype/` | tracked |
| `skills/research/` | `skills/engineering/research/` | tracked |
| `skills/scout/` | `skills/engineering/wayfinder/` | **derived**, forked from `84fdeff` |
| `skills/setup-ph-plan/` | `skills/engineering/setup-matt-pocock-skills/` | tracked |
| `skills/to-questionnaire/` | `skills/productivity/to-questionnaire/` | tracked |
| `skills/to-spec/` | `skills/engineering/to-spec/` | tracked |
| `skills/to-tickets/` | `skills/engineering/to-tickets/` | tracked |
| `skills/triage/` | `skills/engineering/triage/` | tracked |

`scout` is derived because its tracker labels, `closes:` decision tickets, and
claim-before-dispatch are ours. The `wayfinder` fixes in the `5beb35b` sync had
to be re-derived for it rather than applied.

## Own work

**(c) 2026 Matt Lindell, MIT.** `define-done`, `intake`, and the six
`principles/principle-*` leaf skills.

## Modifications

Per the MIT license, modifications are permitted. The planning front-end is the
reason this plugin exists, and the imported skills were reshaped around it:

- Skills that close a Dimension write a `settled:` block onto the spec or
  ticket, which `ph-build` reads to size its rigor.
- `wayfinder` became `scout` and `setup-matt-pocock-skills` became
  `setup-ph-plan`.
- The domain doc stays `CONTEXT.md`, where upstream uses `GLOSSARY.md`.
- Companion files that upstream keeps beside `SKILL.md` live in each skill's
  `references/` directory here, under their upstream filenames. That covers
  `domain-modeling`, `improve-codebase-architecture`, `prototype`,
  `setup-ph-plan`'s seed templates, and `triage`. Port upstream changes to them
  at the new path.
