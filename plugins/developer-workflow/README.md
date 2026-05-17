# developer-workflow

A Claude Code plugin providing workflow tools for daily development tasks.

**Version:** 1.0.0
**Author:** Matt Lindell <misterphoton@gmail.com>
**License:** MIT

---

## Plugin Structure

```text
plugins/developer-workflow/
  .claude-plugin/
    plugin.json
  skills/
    claude-md/
      SKILL.md
      best-practices-reference.md
    commit/
      SKILL.md
      gitmoji-reference.md
```

---

## Skills

Skills provide concrete implementation patterns, code examples, and best practices that agents route to during development work.

| Skill         | Description                                                       |
| ------------- | ----------------------------------------------------------------- |
| **claude-md** | Create, audit, or triage CLAUDE.md files following best practices |
| **commit**    | Commit workflow with conventional commits and gitmoji             |

---

## Installation

**From the command line:**

```bash
claude plugin install developer-workflow
```

**For local development (point to the plugin directory):**

```bash
claude --plugin-dir /path/to/plugins/developer-workflow
```
