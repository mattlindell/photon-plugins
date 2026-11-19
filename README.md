# photon-plugins

Claude Code plugins built around one idea: **planning and building are
different jobs, and an agent should know which one it's doing.**

- **`ph-plan`** runs with a human present. It interviews, models the domain,
  and ends every session in a written spec that records which of four
  dimensions (`problem`, `shape`, `approach`, `verification`) are settled.
- **`ph-build`** runs unattended. It reads that spec and spends rigor only on
  what's still open. Fully settled work goes straight to implementation.
  Multi-agent panels (architecture runners, competing candidates, cross-model
  review) turn on only for one-way doors such as schema changes, public APIs,
  auth, billing, or data deletion, and every fan-out has a hard cap.

Thinking done up front makes execution cheaper, and the contract that
carries it is a few lines of YAML.

## What's in here

- **Unattended ticket draining.** `ph-build:foreman` picks up
  `ready-for-agent` tickets from the tracker and builds them test-first,
  reviewed, and shipped as PRs, with the tracker holding the claim
  ([ADR-0005](docs/adr/0005-the-tracker-holds-the-claim.md)).
- **Rules that look contradictory are the same rule, inverted per harness.**
  `ph-plan` has `block-on-the-human`; `ph-build` has `never-block-on-the-human`.
- **The marketplace is checked like code.** Four validators run in CI (registry
  vs. disk, link and anchor integrity, handoff rules, semver floors derived
  from structural change), the check scripts are type-checked, and every
  Action is SHA-pinned.
- **Upstream lineage is tracked per skill.** Each adapted skill records the
  commit it was reviewed through and whether it's still synced
  ([ADR-0004](docs/adr/0004-lineage-states-for-upstream-derived-skills.md)).

## Plugins

| Plugin | What it's for |
| --- | --- |
| [ph-plan](plugins/ph-plan/) | Interactive planning: intake, grilling, domain modeling, scouting, triage, specs and tickets. 13 skills, 6 principles. Requires `ph-lib`. |
| [ph-build](plugins/ph-build/) | Unattended implementation: a dispatch router, 19 playbooks, TDD, code review, PR babysitting, and `foreman`. 36 skills, 24 principles, 3 agents. Requires `ph-lib`. |
| [ph-lib](plugins/ph-lib/) | Shared library `ph-plan` and `ph-build` require: deep-module design, technical writing, `unslop`, writing for agents, plus 9 operator tools. 13 skills. |
| [ph-lead](plugins/ph-lead/) | Engineering leadership: 1:1s, hard conversations, delegation, managing up, OKRs, org design. 24 skills with a router. |
| [ph-pm](plugins/ph-pm/) | Jira, Confluence, scrum analytics, portfolio risk, meeting-transcript analysis. 8 skills; bundles the Atlassian MCP. |
| [ph-php](plugins/ph-php/) | WordPress, Laravel, Sage/Roots, WooCommerce, CodeIgniter 3. 16 skills, 4 scaffold commands. |
| [ph-npo](plugins/ph-npo/) | Nonprofit operations: grants, budgets, donor comms, volunteers, Givebutter. 7 skills. |

Design decisions are in [docs/adr/](docs/adr/); vocabulary is in [CONTEXT.md](CONTEXT.md).

## Installation

### 1. Add the marketplace

```bash
/plugin marketplace add mattlindell/photon-plugins
```

This makes all plugins available for installation but does not load anything into your context.

### 2. Install a plugin

```bash
/plugin install ph-build@photon-plugins
```

### 3. Browse available plugins

```bash
/plugin
```

Use the Discover tab to see all available plugins from installed marketplaces.

## Local Development

To test a plugin locally without installing from the marketplace:

```bash
claude --plugin-dir /path/to/photon-plugins/plugins/ph-build
```

## Acknowledgments

- Plugin structure and approach inspired by [wshobson/agents](https://github.com/wshobson/agents).
- Eleven `ph-plan` skills, six `ph-build` skills, and six `ph-lib` skills are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills). See [plugins/ph-plan/NOTICE.md](plugins/ph-plan/NOTICE.md) and [LICENSE-pocock-skills](LICENSE-pocock-skills).
- Most of `ph-build` and seven `ph-lib` skills are forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude), Michael Denyer's port of Lauren Tan's (poteto) Cursor `pstack` and Cursor's `cursor-team-kit`. See [plugins/ph-build/NOTICE.md](plugins/ph-build/NOTICE.md), [plugins/ph-lib/NOTICE.md](plugins/ph-lib/NOTICE.md), [LICENSE-pstack](LICENSE-pstack), and [LICENSE-cursor-team-kit](LICENSE-cursor-team-kit).
- Each NOTICE records which upstream commit its skills were reviewed through and whether each skill is still synced. See [ADR-0004](docs/adr/0004-lineage-states-for-upstream-derived-skills.md).
- The `ph-lead` skills are adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled from Lenny's Podcast — since substantially rewritten.

## License

Released under the [MIT License](LICENSE) — use these however you want.
