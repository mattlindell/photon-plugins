# photon-plugins

Claude Code plugin marketplace — reusable agents, skills, and commands distributed as git-based plugins.

## Project Structure

```text
.claude-plugin/marketplace.json  — marketplace metadata and plugin registry
plugins/
  php-development/               — WordPress, Laravel, Sage, WooCommerce, CI3 (agents + skills + commands)
  technical-director/            — diagnosis, planning, issue triage, TDD, refactoring, and process skills
  developer-workflow/            — daily-workflow skills (CLAUDE.md, commit, worktree)
```

Each plugin follows this structure:

```text
plugin-name/
  .claude-plugin/plugin.json                 — plugin metadata (name, version, description, author)
  agents/                                    — strategic decision-makers with YAML frontmatter (name, description, model)
  skills/skill-name/SKILL.md                 — implementation patterns with YAML frontmatter (name, description)
  skills/<category>/skill-name/SKILL.md      — skills may be grouped under a category folder (see technical-director)
  commands/command-name.md                   — interactive scaffolding workflows (no frontmatter)
```

Skill category folders (e.g. `skills/engineering/`, `skills/productivity/`) are optional. When used, each category folder should contain a `README.md` listing its skills. Claude Code discovers skills regardless of nesting depth.

## Conventions

### Frontmatter

- **Agents** require `name`, `description`, `model` in YAML frontmatter
- **Skills** require `name`, `description` in YAML frontmatter — description is critical for agent routing (max 1024 chars, starts with "Use when..." triggering conditions only — do not summarize the skill's workflow)
- **Commands** use no frontmatter — they start with a markdown heading and prose instructions

### Naming

- Directories and files: kebab-case
- Skill content that exceeds ~500 lines should split into SKILL.md (overview) + REFERENCE.md (deep reference)
- Utility scripts go in a `scripts/` subdirectory within the skill

### Plugin Registry

**IMPORTANT: When adding or removing a plugin, you MUST update both the plugin's own `plugin.json` AND `.claude-plugin/marketplace.json` at the root.** Also update the root `README.md` plugin table.

**IMPORTANT: When adding or removing a skill within an existing plugin, bump the plugin's minor version in both `plugin.json` and `.claude-plugin/marketplace.json`, and update the marketplace `description` if the new/removed skill changes the plugin's surface area.** Update the plugin's own `README.md` skills table and structure tree.

## Testing Locally

```bash
claude --plugin-dir plugins/plugin-name
```
