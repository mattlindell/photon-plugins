# NOTICE

Seven of the thirteen skills in `ph-lib` derive from MIT-licensed upstream work.
All upstream copyright notices and license terms are preserved.

Forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude) at
`a0a531f0e341144d12f0a26218b295ad5e8453a1` (v0.9.27), which is itself a port of
Lauren Tan's Cursor `pstack` plus skills from Cursor's `cursor-team-kit`.

This is a hard fork. We do not track upstream — the SHA above is pinned so that
anyone can answer what this diverged from. See
[ADR-0001](../../docs/adr/0001-fork-pstack-rather-than-depend-on-it.md).

## Upstream sources

| Skill | Upstream | Copyright | License |
| --- | --- | --- | --- |
| `skills/primitives/unslop/` | cursor/plugins/pstack | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) |
| `skills/primitives/technical-writing/` | cursor/plugins/pstack | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) |
| `skills/operator-tools/automate-me/` | cursor/plugins/pstack | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) |
| `skills/operator-tools/bro/` | cursor/plugins/pstack | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) |
| `skills/operator-tools/recall/` | cursor/plugins/pstack | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) |
| `skills/operator-tools/reflect/` | cursor/plugins/pstack | (c) 2026 Lauren Tan | MIT — [LICENSE-pstack](../../LICENSE-pstack) |
| `skills/operator-tools/what-did-i-get-done/` | cursor/plugins/cursor-team-kit | (c) 2026 Cursor | MIT — [LICENSE-cursor-team-kit](../../LICENSE-cursor-team-kit) |

`recall` does not appear in upstream's own NOTICE tables, but `CHANGES.md`
documents it as an import with a transcript-path substitution applied. It is
attributed to Lauren Tan here on that basis.

## Own work

`codebase-design`, `writing-for-agents`, `caveman`, `handoff`, `teach`, and
`wait-what` are (c) 2026 Matt Lindell, MIT, and carry no upstream lineage. They
were moved here from the `technical-director` plugin.

## Modifications

Per the MIT license, modifications are permitted. Changes to the imported skills
in this plugin:

- Frontmatter: the five imported operator tools gained
  `disable-model-invocation: true`, and their descriptions were rewritten as
  human-facing one-liners with trigger lists stripped, per this repository's
  convention for user-invoked skills.
- `reflect`: the stamped `## Models` section, which named Claude model slugs and
  pointed at upstream's generator, was replaced with a tier-and-cap table. Tiers
  name an effort rung rather than a model, so the skill ports across harnesses.
- `recall`: its dependency on the `why` skill was made optional with a defined
  fallback, so the library does not depend on a consumer.
- `automate-me`: its pointer to the `poteto-mode` skill, which this fork does not
  carry, was redirected to `writing-for-agents`.
- `automate-me`, `reflect`: Codex platform-mapping links were removed; the
  referenced file is not part of this fork.
- Portability sidecars (`agents/openai.yaml`) were added to all seven.
