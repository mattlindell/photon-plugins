# NOTICE

Eleven of the thirteen skills in `ph-plan` derive from
[Matt Pocock's skills](https://github.com/mattpocock/skills), MIT-licensed. All
upstream copyright notices and license terms are preserved.

**(c) 2026 Matt Pocock, MIT — [LICENSE-pocock-skills](../../LICENSE-pocock-skills)**

This is a hard fork. Nothing syncs upstream automatically; changes are ported by
hand at each sync review. Each skill below carries a lineage state, defined in
[ADR-0004](../../docs/adr/0004-lineage-states-for-upstream-derived-skills.md):
**tracked** skills are reviewed through the pin, **derived** skills keep their
lineage but are no longer synced.

**Reviewed through:** `5beb35b040e3de97e54fa9e386d7e42d15c295c2` (v1.3.1+47,
2026-10-19). The previous sync was `84fdeffd12f2ee307994d1eb6feb48173b6e0502`
(v1.2.3, 2026-08-06), which recorded no pin.

## Upstream sources

Upstream paths are relative to the root of `mattpocock/skills`.

| Skill | Upstream | State |
| --- | --- | --- |
| `skills/domain-modeling/` | `skills/engineering/domain-modeling/` | tracked, reviewed through `5beb35b` |
| `skills/grilling/` | `skills/productivity/grilling/` | tracked, reviewed through `5beb35b` |
| `skills/improve-codebase-architecture/` | `skills/engineering/improve-codebase-architecture/` | tracked, reviewed through `5beb35b` |
| `skills/prototype/` | `skills/engineering/prototype/` | tracked, reviewed through `5beb35b` |
| `skills/research/` | `skills/engineering/research/` | tracked, reviewed through `5beb35b` |
| `skills/scout/` | `skills/engineering/wayfinder/` | **derived**, forked from `84fdeff` |
| `skills/setup-ph-plan/` | `skills/engineering/setup-matt-pocock-skills/` | tracked, reviewed through `5beb35b` |
| `skills/to-questionnaire/` | `skills/productivity/to-questionnaire/` | tracked, reviewed through `5beb35b` |
| `skills/to-spec/` | `skills/engineering/to-spec/` | tracked, reviewed through `5beb35b` |
| `skills/to-tickets/` | `skills/engineering/to-tickets/` | tracked, reviewed through `5beb35b` |
| `skills/triage/` | `skills/engineering/triage/` | tracked, reviewed through `5beb35b` |

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
