# photon-plugins

Claude Code plugin marketplace — reusable agents, skills, and commands distributed as git-based plugins.

## Project Structure

```text
.claude-plugin/marketplace.json  — marketplace metadata and plugin registry
plugins/
  ph-plan/                       — middle-down planning: intake, grilling, domain modeling, scout, triage, to-spec/to-tickets, define-done + 6 principles
  ph-build/                      — unattended implementation, forked from pstack: dispatch router, playbooks, tdd, code-review + 23 principles + 3 agents + SessionStart hook
  ph-lib/                        — shared library: 4 primitives that ph-plan/ph-build require, 9 operator tools. Not a hat
  ph-lead/                       — engineering leadership and people management (24 skills + router)
  ph-pm/                         — Jira, Confluence, Atlassian admin/templates, scrum, portfolio, meeting analysis, team comms (bundles the Atlassian MCP)
  ph-php/                        — WordPress, Laravel, Sage, WooCommerce, CI3 (agents + skills + commands)
  ph-npo/                        — nonprofit operations (org profile, grants, budgets, donor comms, social media, volunteers, Givebutter)
  product-team/                  — unregistered, awaiting cleanup
```

Each plugin follows this structure:

```text
plugin-name/
  .claude-plugin/plugin.json                 — plugin metadata (name, version, description, author)
  agents/                                    — plugin-level agents with YAML frontmatter (name, description, model, color); auto-discovered, never listed in plugin.json
  skills/skill-name/SKILL.md                 — implementation patterns with YAML frontmatter (name, description)
  skills/<category>/skill-name/SKILL.md      — skills may be grouped under a category folder (see ph-lib, ph-build)
  skills/<...>/skill-name/agents/openai.yaml — optional portability sidecar (see below)
  commands/command-name.md                   — interactive scaffolding workflows (no frontmatter)
```

Skill category folders (e.g. `skills/engineering/`, `skills/productivity/`) are optional. When used, each category folder should contain a `README.md` listing its skills. Claude Code discovers skills regardless of nesting depth.

## Seams

One plugin per **hat** — the role someone is wearing when they install it — with
one deliberate exception, `ph-lib`, which is a library other plugins require.
See [ADR-0002](docs/adr/0002-ph-lib-is-a-library-not-a-hat.md).

The two development plugins split on **harness**, not phase. `ph-plan` is
interactive and its skills block on the human; `ph-build` is unattended and its
skills proceed. Rules that look contradictory across them are usually the same
rule correctly inverted. The handoff is a written `settled:` block naming which
of the four dimensions (`problem`, `shape`, `approach`, `verification`) are
closed — that is what lets `ph-build` price work by what is still unknown.

Vocabulary is defined in [CONTEXT.md](CONTEXT.md). Do not add implementation
decisions there; those go in `docs/adr/`.

## Checks

```bash
python scripts/validate-marketplace.py              # registry vs disk, pinned arrays, manifest traps
python scripts/lint-links.py --exclude product-team # relative links + heading anchors
python scripts/bump-versions.py --worktree          # semver floor for what you changed
```

All three run in CI on every PR (`.github/workflows/checks.yml`).

Run all three before any commit that touches plugin structure. `lint-links.py`
matters most after a rename — a renamed heading silently orphans every anchor
pointing at it, which is how two bugs shipped during the reorganization.

`lint-links.py` reports 5 pre-existing failures in `product-team`, which is
unregistered and awaiting cleanup — hence the `--exclude`. Drop the flag once
that plugin is fixed.

### Versioning

Bumps are derived from **structure, not diff size**. A one-line change can be
breaking (adding `disable-model-invocation` removes the model's reach) while a
500-line deletion in a reference file is a patch.

| Change | Bump |
| --- | --- |
| Skill or plugin removed or renamed; skill `name:` changed; `disable-model-invocation` added; agent or command removed | **major** |
| Skill, plugin, agent, or command added; `disable-model-invocation` removed | **minor** |
| Everything else | **patch** |

A `feat:` commit or a `!` / `BREAKING CHANGE:` footer can raise that floor but
never lower it. The check only requires the committed version to be **at or
above** the floor, so bumping higher — or pre-bumping locally — always passes.

CI **blocks** on a missing major and warns on the rest: a removed or renamed
skill is unambiguous and actually breaks someone, while minor-versus-patch
carries real judgment. Fix any complaint with
`python scripts/bump-versions.py --apply`, which writes `plugin.json` and the
matching `marketplace.json` entry together so the two cannot drift.

## Conventions

### Frontmatter

- **Agents** require `name`, `description`, `model` in YAML frontmatter
- **Skills** require `name`, `description` in YAML frontmatter (max 1024 chars). What belongs in it depends on how the skill is invoked:
  - **Model-invoked** (no `disable-model-invocation`) — the description is the skill's always-loaded context pointer, so it must carry trigger conditions. House style is a short identity clause, then the triggers: `Test-driven development. Use when the user wants to build features or fix bugs test-first…`. One trigger per distinct branch; collapse synonyms that rename a single branch.
  - **User-invoked** (`disable-model-invocation: true`) — the description is human-facing only. Write a one-line summary with trigger lists **stripped**: nothing but the human can invoke the skill, so triggers are dead weight in every context window.

  See `ph-lib`'s `writing-for-agents` skill (and its `SKILL-MECHANICS.md`) for the reasoning behind both.
- **Commands** use no frontmatter — they start with a markdown heading and prose instructions
- `disable-model-invocation: true` on a skill makes it user-invoked only (typed as `/skill-name`); omit it when the description carries enough trigger phrasing for the model to reach for the skill on its own

### Portability Sidecars (`agents/openai.yaml`)

A skill may carry an `agents/openai.yaml` alongside its `SKILL.md` so the same folder can be consumed by an OpenAI-based agent harness. Claude Code ignores the file.

Coverage is currently partial, and that is a known gap rather than a rule: `ph-lib` 13/13, `ph-plan` 11/19, `ph-build` 7/56, `ph-lead` 0/24. The skills that have one are those carried over from the old `technical-director`; everything forked from pstack, plus the new skills and principle leaves, does not have one yet. Add a sidecar when you touch a skill that lacks one.

**Two unrelated things are both called `agents/`.** A plugin-level `agents/` holds Claude Code agents (`.md` with `name`/`description`/`model`); a skill-level `skills/<...>/<skill>/agents/` holds only the `openai.yaml` sidecar. `ph-build` has both.

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

**IMPORTANT: In `plugin.json`, `repository` must be a string URL, never an object.** The `{"type": "git", "url": "…"}` form — which the official `plugin-dev` manifest reference documents in its "complete plugin" example — causes Claude Code to **silently discover zero skills** from that plugin. No error, no warning; the plugin loads and every skill vanishes. Verified against `ph-lib` on 2026-09-19: with the object form, 0 skills; with the string form, all of them. After editing any `plugin.json`, confirm skills still resolve:

```bash
claude -p --plugin-dir plugins/<name> --model haiku --max-turns 1 \
  "Without using any tools: list your available skills starting with '<name>:'." < /dev/null
```

Only model-invocable skills appear in that listing — skills with `disable-model-invocation: true` are correctly absent. Check those with `claude -p --plugin-dir plugins/<name> --max-turns 2 "/<name>:<skill>"`.

**IMPORTANT: When adding or removing a plugin, you MUST update both the plugin's own `plugin.json` AND `.claude-plugin/marketplace.json` at the root.** Also update the root `README.md` plugin table.

**IMPORTANT: When adding or removing a skill within an existing plugin, bump the plugin's minor version in both `plugin.json` and `.claude-plugin/marketplace.json`, and update the marketplace `description` if the new/removed skill changes the plugin's surface area.** Update the plugin's own `README.md` skills table and structure tree.

**Renaming or removing a skill is a breaking change** — anyone invoking `/old-name` loses it. Bump the plugin's **major** version, not the minor.

Some plugins (`ph-plan`, `ph-build`, `ph-lib`, `ph-lead`, `ph-pm`) pin an explicit `skills` array in `plugin.json`. **When that array is present it must list every skill directory exactly** — a stale or missing path silently drops the skill from the plugin. After adding, removing, or renaming a skill in one of those plugins, verify with:

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

## Agent skills

### Issue tracker

Issues live in **Linear**. Use the `linearis` CLI first, the Linear MCP as fallback. The team and project identifiers are not committed (this repo is public) — resolve them from `docs/agents/linear-ids.local.md`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles are Linear labels under the workspace-level "Agentic State Machine" group, each label string equal to its role name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
