# NOTICE

All thirteen skills in `ph-lib` derive from MIT-licensed upstream work. All
upstream copyright notices and license terms are preserved.

Seven are forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude)
at `a0a531f0e341144d12f0a26218b295ad5e8453a1` (v0.9.27), Michael Denyer's port of
Lauren Tan's (poteto) Cursor `pstack` plus skills from Cursor's `cursor-team-kit`.
The other six derive from [Matt Pocock's skills](https://github.com/mattpocock/skills).

This is a hard fork. We carry none of upstream's sync tooling
([ADR-0001](../../docs/adr/0001-fork-pstack-rather-than-depend-on-it.md));
changes are ported by hand at each sync review. Each skill carries a lineage
state, defined in
[ADR-0004](../../docs/adr/0004-lineage-states-for-upstream-derived-skills.md):
**tracked** skills are reviewed through the pin, **derived** skills keep their
lineage but are no longer synced.

| Upstream | Reviewed through |
| --- | --- |
| pstack-claude | `903e7385382389806c59d6989b6274e24165082b` (v0.9.101, 2026-10-21) |
| Matt Pocock's skills | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` (v1.3.1+47, 2026-10-19) |

## Upstream sources

Upstream paths are relative to each upstream repository's root. Every
pstack-claude path sits under `plugins/pstack/`, shortened to `…/` below.

| Skill | Original source | pstack-claude path | Copyright | License | State |
| --- | --- | --- | --- | --- | --- |
| `skills/primitives/unslop/` | cursor/plugins/pstack | `…/skills/unslop/` | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) | tracked, reviewed through `903e738` |
| `skills/primitives/technical-writing/` | cursor/plugins/pstack | `…/skills/technical-writing/` | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) | tracked, reviewed through `903e738` |
| `skills/operator-tools/automate-me/` | cursor/plugins/pstack | `…/skills/automate-me/` | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) | tracked, reviewed through `903e738` |
| `skills/operator-tools/bro/` | cursor/plugins/pstack | `…/skills/bro/` | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) | tracked, reviewed through `903e738` |
| `skills/operator-tools/recall/` | cursor/plugins/pstack | `…/skills/recall/` | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) | tracked, reviewed through `903e738` |
| `skills/operator-tools/reflect/` | cursor/plugins/pstack | `…/skills/reflect/` | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) | tracked, reviewed through `903e738` |
| `skills/operator-tools/what-did-i-get-done/` | cursor/plugins/cursor-team-kit | `…/skills/what-did-i-get-done/` | (c) 2026 Cursor | MIT — [LICENSE-cursor-team-kit](../../LICENSE-cursor-team-kit) | tracked, reviewed through `903e738` |

`recall` does not appear in upstream's own NOTICE tables, but `CHANGES.md`
documents it as an import with a transcript-path substitution applied. It is
attributed to Lauren Tan here on that basis.

Port-authored changes from pstack-claude synced into `reflect`, `recall`, and
`automate-me` (the transcript-directory helper and its callers) are (c) 2026
Michael Denyer, MIT — [LICENSE-pstack](../../LICENSE-pstack).

### Pocock lineage

`codebase-design`, `writing-for-agents`, `caveman`, `handoff`, `teach`, and
`wait-what` are (c) 2026 Matt Pocock, MIT —
[LICENSE-pocock-skills](../../LICENSE-pocock-skills). They were moved here from
the `technical-director` plugin, whose skills were all taken from Pocock's
repository, and have since been edited in this repository.

| Skill | Upstream | State |
| --- | --- | --- |
| `skills/primitives/codebase-design/` | `skills/engineering/codebase-design/` | tracked, reviewed through `5beb35b` |
| `skills/primitives/writing-for-agents/` | `skills/productivity/writing-for-agents/` | tracked, reviewed through `5beb35b` |
| `skills/operator-tools/caveman/` | `skills/productivity/caveman/` | **derived**, forked from `0a4b767` |
| `skills/operator-tools/handoff/` | `skills/productivity/handoff/` | tracked, reviewed through `5beb35b` |
| `skills/operator-tools/teach/` | `skills/productivity/teach/` | tracked, reviewed through `5beb35b` |
| `skills/operator-tools/wait-what/` | `skills/productivity/wait-what/` | tracked, reviewed through `5beb35b` |

`caveman` is derived because upstream deleted it in `7d3ada9` (2026-05-31), so
there is nothing left to sync against. `0a4b767` is the last upstream commit
that carries it.

## Modifications

Per the MIT license, modifications are permitted. Changes to the imported skills
in this plugin:

- Frontmatter: the five imported operator tools gained
  `disable-model-invocation: true`, and their descriptions were rewritten as
  human-facing one-liners with trigger lists stripped, per this repository's
  convention for user-invoked skills.
- `reflect`: the stamped `## Models` section, which named Claude model slugs and
  pointed at upstream's generator, was replaced with a `## Fan-out` section
  stating a fixed four agents on the `judgment` tier. Tiers name an effort rung
  rather than a model, so the skill ports across harnesses. The four in-body
  links to the old `#models` anchor were repointed.
- `recall`: its dependency on the `why` skill was made optional with a defined
  fallback, so the library does not depend on a consumer.
- `automate-me`: its pointer to the `poteto-mode` skill, which this fork does not
  carry, was redirected to `writing-for-agents`.
- `automate-me`, `reflect`: Codex platform-mapping links were removed; the
  referenced file is not part of this fork.
- Portability sidecars (`agents/openai.yaml`) were added to all seven.
