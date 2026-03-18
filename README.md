# photon-plugins

A Claude Code plugin marketplace for PHP development workflows.

## Available Plugins

| Plugin                                            | Description                                                                                                                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [php-development](plugins/php-development/)       | WordPress, Laravel, Sage/Roots, WooCommerce, and CodeIgniter 3 legacy maintenance. 3 agents, 12 skills, 4 scaffold commands.                                                         |
| [technical-director](plugins/technical-director/) | Project management and technical direction: covers the full development lifecycle from design exploration through implementation planning, issue tracking, and codebase improvement. |

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

Plugin structure and approach inspired by [wshobson/agents](https://github.com/wshobson/agents).

## License

MIT
