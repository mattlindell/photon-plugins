# photon-plugins

Claude Code plugins built on one idea. Planning and building are different
jobs, and an agent should know which one it's doing.

- **`ph-plan`** runs with a human present. It interviews, models the domain,
  and ends every session in a written spec. The spec records which of four
  dimensions are settled: `problem`, `shape`, `approach`, and `verification`.
- **`ph-build`** runs unattended. It reads that spec and spends effort only on
  the dimensions still open. Fully settled work goes straight to
  implementation. Multi-agent panels, such as parallel architecture drafts,
  competing implementations, and cross-model review, run only for changes
  that are hard to undo. Those are schema changes, public APIs, auth, billing,
  and data deletion. Every fan-out has a hard cap on how many agents it
  starts.

The spec hands this off in a `settled:` block of a few lines of YAML. Each
dimension closed during planning is one that `ph-build` doesn't pay to
explore again.

## What's in here

- **Unattended ticket draining.** `ph-build:foreman` claims `ready-for-agent`
  tickets and hands each one to a worker that builds it test-first, reviews
  it, and opens a PR. The claim is stored on the ticket, never in a local
  file, so a crashed run recovers by rereading the tracker. See
  [ADR-0005](docs/adr/0005-the-tracker-holds-the-claim.md).
- **Rules that look contradictory are one rule applied in two settings.**
  `ph-plan` has a human to ask, so it follows `block-on-the-human`. `ph-build`
  has no one to ask, so it follows `never-block-on-the-human`.
- **CI validates the marketplace.** Five checks run on every PR. They compare
  the plugin registry against the files on disk, resolve every link and
  anchor, enforce handoff rules between plugins, hold the upstream record and
  NOTICE files in agreement, and compute the minimum semver bump from
  structural changes. The check scripts pass type checking
  with basedpyright, and every GitHub Action is pinned to a commit SHA.
- **Each adapted skill tracks its upstream.** [UPSTREAMS.md](UPSTREAMS.md)
  shows the upstream commit each upstream was last reviewed through, and a
  NOTICE file records whether each skill still syncs with it. See
  [ADR-0004](docs/adr/0004-lineage-states-for-upstream-derived-skills.md) and
  [ADR-0006](docs/adr/0006-upstream-record.md).

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

## Local development

To test a plugin locally without installing from the marketplace:

```bash
claude --plugin-dir /path/to/photon-plugins/plugins/ph-build
```

## Acknowledgments

- The structure of `ph-php` was inspired by the [wshobson/agents](https://github.com/wshobson/agents) marketplace. The other plugins follow a different design.
- Eleven `ph-plan` skills, six `ph-build` skills, and six `ph-lib` skills are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills). See [plugins/ph-plan/NOTICE.md](plugins/ph-plan/NOTICE.md) and [LICENSE-pocock-skills](LICENSE-pocock-skills).
- Most of `ph-build` and seven `ph-lib` skills are forked from [pstack-claude](https://github.com/michael-denyer/pstack-claude), Michael Denyer's port of Lauren Tan's (poteto) Cursor `pstack` and Cursor's `cursor-team-kit`. See [plugins/ph-build/NOTICE.md](plugins/ph-build/NOTICE.md), [plugins/ph-lib/NOTICE.md](plugins/ph-lib/NOTICE.md), [LICENSE-pstack](LICENSE-pstack), and [LICENSE-cursor-team-kit](LICENSE-cursor-team-kit).
- The `ph-lead` skills are adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled from Lenny's Podcast. They have since been mostly rewritten.

## License

Released under the [MIT License](LICENSE). Use these however you want.
