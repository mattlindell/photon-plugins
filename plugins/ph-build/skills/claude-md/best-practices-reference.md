# CLAUDE.md Best Practices Reference

Evaluation criteria and checklists for creating, auditing, and triaging CLAUDE.md content.
Consult this file during CREATE step 4, AUDIT step 2, and TRIAGE step 2.

## The Removal Test

For every line in CLAUDE.md, ask: "If I remove this line, will Claude make mistakes?"
If the answer is no, the line does not belong.

## Include Checklist

Content that belongs in CLAUDE.md (if it passes the removal test):

| Content                     | Why                             | Example                                              |
| --------------------------- | ------------------------------- | ---------------------------------------------------- |
| Project context (1-2 lines) | Immediate orientation           | "SaaS document automation — Next.js, Express, MySQL" |
| Essential commands          | Claude uses these exact strings | `npm run dev`, `npm run test`, `npm run build`       |
| Directory map               | Shows where code lives          | `src/routes/` — API endpoints                        |
| Non-default conventions     | Rules Claude wouldn't guess     | "Use Zustand stores, never Redux"                    |
| Common gotchas              | Prevents repeated mistakes      | "Always run sync-pricing before build"               |
| Workflow rules              | Can't be inferred from code     | "Branch naming: feat/JIRA-123-description"           |

## Exclude Checklist

Content that does NOT belong in CLAUDE.md:

| Content                            | Why                                                  |
| ---------------------------------- | ---------------------------------------------------- |
| Standard language conventions      | Claude already knows TypeScript/Python/etc. patterns |
| Detailed API documentation         | Reference by plain path with a "Read when" trigger   |
| Code style enforced by linters     | Don't send an LLM to do a linter's job               |
| File-by-file codebase descriptions | Claude can read files itself                         |
| Obvious instructions               | "Write clean code" wastes tokens                     |
| Frequently changing information    | Goes stale, causes confusion                         |

## Structure Template

CLAUDE.md should follow this section order:

```markdown
# Project Name

One-line description of what this project does and its tech stack.

## Commands
[Essential commands: dev, test, build, lint — only what exists]

## Project Structure
[Top-level directory overview — what lives where]

## Conventions
[Non-obvious, non-default patterns only]

## Reference Documents
### [Doc Name] — `docs/filename.md`
**Read when:** [trigger condition]
[2-3 line summary]
```

## Line Budget

- **Target:** Under 200 lines
- **Warning:** 200-300 lines — flag for pruning
- **Critical:** Over 300 lines — must prune before adding anything

Every line consumes context window budget that could be spent on actual code.

## Progressive Disclosure Mechanisms

Progressive disclosure means content loads *only when needed* — not at session start. Use these to keep CLAUDE.md lean:

| Mechanism             | Best For                                          | How                                                      |
| --------------------- | ------------------------------------------------- | -------------------------------------------------------- |
| `docs/` with triggers | READMEs, detailed SOPs, API architecture docs, long-form style guides, migration playbooks | Reference the file by plain path with a "Read when" trigger; Claude reads it on demand |
| `.claude/rules/`      | Team-wide coding rules, review checklists         | Markdown files auto-load alongside CLAUDE.md             |
| `.claude/skills/`     | Domain knowledge, specialized workflows           | Load on-demand based on relevance                        |

**`@imports` are NOT progressive disclosure.** The `@path/to/file.md` syntax eager-loads the referenced file (recursively, up to 5 levels deep) into context at session start — functionally identical to pasting its contents inline. Use `@imports` only to *organize* always-needed content across files (e.g. `@~/.claude/personal-prefs.md`), never to defer loading. For anything that should load only when relevant, use a plain path with a "Read when" trigger instead.

## File Placement Hierarchy

| Location              | Scope                           | Commit?         |
| --------------------- | ------------------------------- | --------------- |
| `~/.claude/CLAUDE.md` | All sessions, all projects      | No (personal)   |
| `./CLAUDE.md`         | Project root                    | Yes             |
| `./CLAUDE.local.md`   | Personal project overrides      | No (.gitignore) |
| `parent/CLAUDE.md`    | Inherited by child directories  | Yes             |
| `child/CLAUDE.md`     | Loaded when working in that dir | Yes             |
| `.claude/rules/*.md`  | Auto-loaded alongside CLAUDE.md | Yes             |

## AUDIT Evaluation Criteria

When auditing an existing CLAUDE.md, check each of these:

1. **Line count** — Over 200? Flag. Over 300? Critical.
2. **Duplication** — Anything already in `~/.claude/CLAUDE.md` or `.claude/rules/`?
3. **Stale content** — Commands that don't match package.json scripts? References to files/dirs that don't exist?
4. **Noise** — Standard conventions? Linter-enforced rules? Obvious instructions? File-by-file descriptions?
5. **Structure** — Follows the section order template? Has essential commands? Directory overview?
6. **Progressive disclosure** — Large reference content inline that should be moved to a separate file referenced by a plain path with a "Read when" trigger? (Note: `@imports` eager-load, so they don't reduce context cost — only deferred reads do.)
7. **Emphasis** — Critical rules using IMPORTANT or YOU MUST for adherence?

## Triage Destination Bias

When triaging session learnings, bias AWAY from CLAUDE.md. Most learnings belong elsewhere:

| Learning Type                             | Destination             | Reasoning                            |
| ----------------------------------------- | ----------------------- | ------------------------------------ |
| Personal corrections/preferences          | Memory (feedback type)  | Personal to user, not project        |
| User role/context                         | Memory (user type)      | About the person, not the code       |
| Team coding standards                     | `.claude/rules/`        | Rules auto-load, keep CLAUDE.md thin |
| External resource pointers                | Memory (reference type) | Not project context Claude needs     |
| Project-level gotchas that cause mistakes | CLAUDE.md               | Only these pass the removal test     |

**Default assumption:** A learning goes to memory or rules unless it clearly passes the removal test for CLAUDE.md.

## Memory File Format

When the TRIAGE pathway writes to memory, use this format:

```markdown
---
name: <memory-name>
description: <one-line description>
type: <user|feedback|project|reference>
---

<memory content>
```

Write each memory as its own file in `~/.claude/projects/<project>/memory/` and add a pointer to `MEMORY.md` index.

## Maintenance Signals

Signs that CLAUDE.md needs attention:

- **Claude ignores a rule** → File is too long. Prune it.
- **Claude asks questions already answered** → Phrasing is ambiguous. Rewrite it.
- **Claude repeats mistakes** → Missing a gotcha. Add it (if it passes removal test).
