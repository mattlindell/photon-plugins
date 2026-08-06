# photon-plugins

Claude Code plugin marketplace — reusable agents, skills, and commands distributed as git-based plugins.

## Project Structure

```text
.claude-plugin/marketplace.json  — marketplace metadata and plugin registry
plugins/
  php-development/               — WordPress, Laravel, Sage, WooCommerce, CI3 (agents + skills + commands)
  technical-director/            — engineering (diagnosis, domain modeling, specs/tickets, triage, TDD, code review, research, codebase design, wizards), leadership, productivity, and misc skills + implement/code-review agents
  developer-workflow/            — daily-workflow skills (CLAUDE.md, commit, worktree)
  nonprofit-toolkit/             — nonprofit operations skills (org profile, grants, budgets, donor comms, social media, volunteers)
  project-manager/               — Jira, Confluence, Atlassian admin/templates, scrum, portfolio, meeting analysis, team comms (bundles the Atlassian MCP)
```

Each plugin follows this structure:

```text
plugin-name/
  .claude-plugin/plugin.json                 — plugin metadata (name, version, description, author)
  agents/                                    — plugin-level agents with YAML frontmatter (name, description, model, color); auto-discovered, never listed in plugin.json
  skills/skill-name/SKILL.md                 — implementation patterns with YAML frontmatter (name, description)
  skills/<category>/skill-name/SKILL.md      — skills may be grouped under a category folder (see technical-director)
  skills/<...>/skill-name/agents/openai.yaml — optional portability sidecar (see below)
  commands/command-name.md                   — interactive scaffolding workflows (no frontmatter)
```

Skill category folders (e.g. `skills/engineering/`, `skills/productivity/`) are optional. When used, each category folder should contain a `README.md` listing its skills. Claude Code discovers skills regardless of nesting depth.

## Conventions

### Frontmatter

- **Agents** require `name`, `description`, `model` in YAML frontmatter
- **Skills** require `name`, `description` in YAML frontmatter (max 1024 chars). What belongs in it depends on how the skill is invoked:
  - **Model-invoked** (no `disable-model-invocation`) — the description is the skill's always-loaded context pointer, so it must carry trigger conditions. House style is a short identity clause, then the triggers: `Test-driven development. Use when the user wants to build features or fix bugs test-first…`. One trigger per distinct branch; collapse synonyms that rename a single branch.
  - **User-invoked** (`disable-model-invocation: true`) — the description is human-facing only. Write a one-line summary with trigger lists **stripped**: nothing but the human can invoke the skill, so triggers are dead weight in every context window.

  See `technical-director`'s `writing-for-agents` skill (and its `SKILL-MECHANICS.md`) for the reasoning behind both.
- **Commands** use no frontmatter — they start with a markdown heading and prose instructions
- `disable-model-invocation: true` on a skill makes it user-invoked only (typed as `/skill-name`); omit it when the description carries enough trigger phrasing for the model to reach for the skill on its own

### Portability Sidecars (`agents/openai.yaml`)

A skill may carry an `agents/openai.yaml` alongside its `SKILL.md` so the same folder can be consumed by an OpenAI-based agent harness. Claude Code ignores the file. Every `technical-director` skill outside `skills/leadership/` has one.

**Two unrelated things are both called `agents/`.** A plugin-level `agents/` holds Claude Code agents (`.md` with `name`/`description`/`model`); a skill-level `skills/<...>/<skill>/agents/` holds only the `openai.yaml` sidecar. `technical-director` has both.

```yaml
interface:
  display_name: "Ask Matt"
  short_description: "Find the right skill or workflow"
policy:
  allow_implicit_invocation: false # mirrors disable-model-invocation: true
```

**IMPORTANT: `policy.allow_implicit_invocation: false` and `disable-model-invocation: true` must agree.** When a skill has a sidecar and you change one flag, change the other — omit the whole `policy` block for model-invocable skills.

### Naming

- Directories: kebab-case
- Files carrying data or seed content: kebab-case (`issue-tracker-github.md`, `triage-labels.md`, `mocking.md`)
- **Reference companions to a `SKILL.md` are UPPERCASE**: `DEEPENING.md`, `ADR-FORMAT.md`, `PHASE-BOUNDARIES.md`, `SKILL-MECHANICS.md`, and the leadership set (`INTAKE`, `WORKFLOW`, `TEMPLATES`, `CHECKLISTS`, `RUBRIC`). The case is the signal — uppercase means "reference reached by a pointer from `SKILL.md`", which is why it doesn't follow the kebab-case rule above.
- Skill content that exceeds ~500 lines should split into `SKILL.md` (overview) + an uppercase reference file
- Utility scripts go in a `scripts/` subdirectory within the skill

### Plugin Registry

**IMPORTANT: When adding or removing a plugin, you MUST update both the plugin's own `plugin.json` AND `.claude-plugin/marketplace.json` at the root.** Also update the root `README.md` plugin table.

**IMPORTANT: When adding or removing a skill within an existing plugin, bump the plugin's minor version in both `plugin.json` and `.claude-plugin/marketplace.json`, and update the marketplace `description` if the new/removed skill changes the plugin's surface area.** Update the plugin's own `README.md` skills table and structure tree.

**Renaming or removing a skill is a breaking change** — anyone invoking `/old-name` loses it. Bump the plugin's **major** version, not the minor.

Some plugins (`technical-director`, `project-manager`) pin an explicit `skills` array in `plugin.json`. **When that array is present it must list every skill directory exactly** — a stale or missing path silently drops the skill from the plugin. After adding, removing, or renaming a skill in one of those plugins, verify with:

```bash
# every SKILL.md on disk vs. every path in the skills array — output should be empty
cd plugins/<plugin-name>
diff <(find skills -name SKILL.md | xargs -n1 dirname | sed 's|^|./|' | sort) \
     <(python -c "import json;[print(p) for p in json.load(open('.claude-plugin/plugin.json'))['skills']]" | tr -d '\r' | sort)
```

Docs to update on any skill change, in this order: the category `README.md` → the plugin `README.md` (skills table, structure tree, skill count, version) → the root `README.md` plugin table → `.claude-plugin/marketplace.json`. Skill counts appear in four places — plugin `description` (both files), plugin `README.md` intro, and the root `README.md` table.

## Testing Locally

```bash
claude --plugin-dir plugins/plugin-name
```
