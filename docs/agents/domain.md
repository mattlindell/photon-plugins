# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CLAUDE.md`** at the repo root — the marketplace's structural conventions (plugin layout, frontmatter rules, naming, the registry-update checklist) live there, not in a `CONTEXT.md`. Read it first for anything touching plugin or skill structure.
- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

This is a **single-context** repo — one `CONTEXT.md` + `docs/adr/` at the repo root:

```text
/
├── CLAUDE.md
├── CONTEXT.md
├── docs/
│   ├── adr/
│   │   ├── 0001-skill-category-folders.md
│   │   └── 0002-openai-portability-sidecars.md
│   └── agents/
└── plugins/
```

Note that `plugins/*` is **not** a monorepo — each plugin is a content bundle (agents, skills, commands), not a separately-built package. Multi-context layout — a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files — does not apply here, and shouldn't be adopted just because `plugins/` has several entries.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

This repo's vocabulary is largely fixed by Claude Code itself — **plugin**, **skill**, **agent**, **command**, **marketplace**, **frontmatter**, **sidecar**. Use those terms as Claude Code uses them; don't coin alternatives.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0002 (OpenAI portability sidecars) — but worth reopening because…_
