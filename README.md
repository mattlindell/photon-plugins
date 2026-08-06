# photon-plugins

A Claude Code plugin marketplace — reusable agents, skills, and commands for a variety of projects and tasks.

## Available Plugins

| Plugin                                            | Description                                                                                                                                                                                                                                                                                |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [php-development](plugins/php-development/)       | WordPress, Laravel, Sage/Roots, WooCommerce, and CodeIgniter 3 legacy maintenance. 3 agents, 12 skills, 4 scaffold commands.                                                                                                                                                               |
| [technical-director](plugins/technical-director/) | Technical direction and engineering leadership: an engineering workflow (diagnosis, domain modeling, specs, issue triage, TDD, codebase design and architecture, prototyping, implementation, human-in-the-loop setup wizards, repo-tooling guardrails), a leadership category (1:1s, difficult conversations, delegation, managing up, cross-functional collaboration, timelines, meetings, decisions, and org design), and productivity tools (grilling, handoffs, teaching, questionnaires, writing for agents). 52 skills. |
| [developer-workflow](plugins/developer-workflow/) | Developer workflow skills for daily tasks: CLAUDE.md authoring/auditing, a conventional-commit + gitmoji commit helper, and a git worktree manager with sibling-placement rules. 3 skills.                                                                                                 |
| [nonprofit-toolkit](plugins/nonprofit-toolkit/)   | Nonprofit operations skills: a foundational organization profile builder plus grant writing, budget creation, donor thank-you communications, social media content, and volunteer scheduling. 6 skills.                                                                                    |
| [project-manager](plugins/project-manager/)       | Project management and Atlassian work: Jira, Confluence, Atlassian administration and templates, Scrum Master sprint analytics, senior-PM portfolio and risk management, meeting-transcript analysis, and internal team communications. 8 skills; bundles the Atlassian Remote MCP server. |

## Installation

### 1. Add the marketplace

```bash
/plugin marketplace add mattlindell/photon-plugins
```

This makes all plugins available for installation but does not load anything into your context.

### 2. Install a plugin

```bash
/plugin install php-development@photon-plugins
```

### 3. Browse available plugins

```bash
/plugin
```

Use the Discover tab to see all available plugins from installed marketplaces.

## Local Development

To test a plugin locally without installing from the marketplace:

```bash
claude --plugin-dir /path/to/photon-plugins/plugins/php-development
```

## Acknowledgments

- Plugin structure and approach inspired by [wshobson/agents](https://github.com/wshobson/agents).
- The `technical-director` engineering skills are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT).
- The `technical-director` leadership skills are adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) (MIT), distilled from Lenny's Podcast — since substantially rewritten.

## License

Released under the [MIT License](LICENSE) — use these however you want.
