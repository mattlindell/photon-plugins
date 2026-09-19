# ph-lib

Shared library for the photon plugins. Thirteen skills in two sections.

**This plugin is not a hat.** Every other plugin in this marketplace corresponds
to a role someone is wearing. `ph-lib` does not — nobody installs it because of
the work they are doing. They install it because `ph-plan` and `ph-build` require
it. See [ADR-0002](../../docs/adr/0002-ph-lib-is-a-library-not-a-hat.md).

## Membership

Two sections, two tests. A skill that satisfies neither does not belong here —
that rule is the whole difference between a library and a junk drawer.

**Primitives** — another plugin's router references this, so `ph-build` and
`ph-plan` are broken without it.

**Operator tools** — you invoke this directly. It acts on the conversation or on
the agent system, never on a work product.

## Primitives (4)

| Skill | Invocation | What it does |
| --- | --- | --- |
| `codebase-design` | model | Shared vocabulary for designing deep modules. Referenced by `ph-build:tdd` and `ph-plan:improve-codebase-architecture` |
| `technical-writing` | model | Layered standard for docs, RFCs, PR descriptions, commit messages |
| `unslop` | model | Cut AI tells from any writing. Referenced by both routers |
| `writing-for-agents` | model | Writing SKILL.md, AGENTS.md, and any doc an agent reaches through a pointer |

## Operator tools (9)

All user-invoked — type `/ph-lib:<name>`.

| Skill | What it does |
| --- | --- |
| `automate-me` | Draft or revise a personal `-mode` skill that captures how you work |
| `bro` | Restate the last message in plain human language |
| `caveman` | Compress agent verbosity |
| `handoff` | Compact the conversation into a handoff document for another agent |
| `recall` | Rebuild your recent working context into a current-state brief |
| `reflect` | Review the active transcript and route learnings to concrete skill edits |
| `teach` | Build a durable learning curriculum within this workspace |
| `wait-what` | That last message did not land — re-pitch it |
| `what-did-i-get-done` | Summarize your authored commits over a period |

## Dependency direction

`ph-plan` and `ph-build` depend on `ph-lib`. **`ph-lib` depends on nothing.**

Claude Code has no plugin dependency mechanism — `plugin.json` has no
`dependencies` field — so the requirement is enforced at runtime by `ph-build`'s
`SessionStart` hook, which degrades loudly when `ph-lib` is missing.

One skill here reaches into a hat plugin, and it does so optionally: `recall`
uses `ph-build:why`'s source investigators when they are installed, and runs the
sweep itself when they are not. The library never hard-depends on a consumer.

`reflect` is the one library skill that spawns subagents, but its four agents are
hard-coded — three reviewers on distinct prompt templates plus a synthesizer that
expects all three. It reads no configuration, so it needs nothing from
`ph-build` either.

## Structure

```text
ph-lib/
  .claude-plugin/plugin.json
  NOTICE.md                       — upstream attribution
  skills/
    primitives/                   — 4 skills, model-invocable
    operator-tools/               — 9 skills, user-invoked
```

Each skill carries an `agents/openai.yaml` portability sidecar.

## Attribution

Seven skills derive from MIT-licensed upstream work by Lauren Tan and Cursor. See
[NOTICE.md](NOTICE.md), and the license files at the repository root.
