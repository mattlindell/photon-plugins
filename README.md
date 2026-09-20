# photon-plugins

A Claude Code plugin marketplace — reusable agents, skills, and commands for a variety of projects and tasks.

## Available Plugins

| Plugin | Description |
| --- | --- |
| [ph-plan](plugins/ph-plan/) | **Middle-down planning** — deciding and writing down what gets built, in an interactive session. Intake routing, grilling, domain modeling, scouting, triage, specs and tickets. Ends in an artifact carrying the four-dimension rigor signal. 13 skills, 6 principles. Requires `ph-lib`. |
| [ph-build](plugins/ph-build/) | **Unattended implementation** — building what was decided, at a cost that tracks what is still unknown. Forked from pstack: reads the rigor signal, gates expensive multi-agent work behind one-way doors, caps every fan-out. 33 skills, 23 principles, 19 playbooks, 3 agents. Requires `ph-lib`. |
| [ph-lib](plugins/ph-lib/) | Shared library. Four primitives that `ph-plan` and `ph-build` reference and require, plus nine operator tools you invoke directly. Not a hat — a dependency. 13 skills. |
| [ph-lead](plugins/ph-lead/) | Engineering leadership and people management: 1:1s, difficult conversations, delegation, managing up, cross-functional collaboration, timelines, meetings and offsites, decision processes, OKRs, org design, culture and rituals. 24 skills with a router. |
| [ph-pm](plugins/ph-pm/) | Atlassian and scrum operations: Jira, Confluence, administration and templates, sprint analytics, portfolio and risk management, meeting-transcript analysis, team communications. 8 skills; bundles the Atlassian Remote MCP server. |
| [ph-php](plugins/ph-php/) | WordPress, Laravel, Sage/Roots, WooCommerce, and CodeIgniter 3 legacy maintenance. 12 skills, 3 agents, 4 scaffold commands. |
| [ph-npo](plugins/ph-npo/) | Nonprofit operations: an organization profile builder that personalizes the rest, plus grant writing, budgets, donor thank-yous, social media, volunteer scheduling, and Givebutter integration. 7 skills. |

`technical-director` and `developer-workflow` are still present on disk but
superseded — their contents now live in `ph-plan`, `ph-build`, `ph-lib`, and
`ph-lead`. They are removed in the final step of the reorganization.
`product-team` is unregistered and awaiting its own cleanup.

### Seams

Each plugin is **one hat** — the role you are wearing when you install it —
with one deliberate exception. `ph-lib` is a library: nobody installs it for
the work they are doing, they install it because `ph-plan` and `ph-build`
require it.

The two development plugins split on **harness**, not on phase. `ph-plan` is
interactive: a human is present, so its skills ask and wait. `ph-build` is
unattended: nobody is there, so its skills proceed and you course-correct on
review. Rules that look contradictory across the two are usually the same rule,
correctly inverted — `ph-plan:principle-block-on-the-human` against
`ph-build:principle-never-block-on-the-human` is the clearest pair.

The handoff between them is a written artifact carrying a `settled:` block: the
four dimensions of a task (`problem`, `shape`, `approach`, `verification`), each
closed or open. `ph-build` reads it to decide how much rigor the work still
needs, so thinking done up front actually buys cheaper execution.

Concepts are defined in [CONTEXT.md](CONTEXT.md); the reorganization is recorded
in [docs/adr/](docs/adr/).

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
- The `ph-plan` skills are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT).
- Most of `ph-build` and seven `ph-lib` skills are forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude) (MIT) at `a0a531f`, itself a port of Lauren Tan's Cursor `pstack` and Cursor's `cursor-team-kit`. See [plugins/ph-build/NOTICE.md](plugins/ph-build/NOTICE.md), [plugins/ph-lib/NOTICE.md](plugins/ph-lib/NOTICE.md), [LICENSE-pstack](LICENSE-pstack), and [LICENSE-cursor-team-kit](LICENSE-cursor-team-kit).
- The `ph-lead` skills are adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled from Lenny's Podcast — since substantially rewritten.

## License

Released under the [MIT License](LICENSE) — use these however you want.
