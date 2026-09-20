---
name: commit
description: Use when the user asks to commit changes, write commit messages, or review staged work for committing
user-invocable: true
---

# Commit

Generate atomic, well-formatted commits using conventional commits with gitmoji.

## Workflow

1. **Gather state** — Run `git status` and `git diff --staged`. Also check `git diff` for unstaged changes to understand the full picture.

2. **Analyze changes** — Identify logical groupings of related changes.

3. **Decide whether to split:**
   - Obviously distinct changes (e.g., frontend code vs documentation, unrelated features) → auto-split into separate commits and inform the user.
   - Ambiguous groupings → propose the split and ask for confirmation.

4. **Generate commit message** for each commit:
   - Select gitmoji from `gitmoji-reference.md`
   - Determine conventional commit type and scope
   - Write 1-line summary: imperative mood, under 50 characters, no trailing period
   - Add body only when the change warrants explanation (the "why", not the "what")
   - Add footer for breaking changes or issue references

5. **Stage and commit** — Stage the relevant files for each logical commit and execute.

6. **Report** — Show what was committed.

## Commit Format

```text
<emoji> <type>(<scope>): <summary>

[optional body — explains WHY, not WHAT]

[optional footer — breaking changes, issue refs]
```

## Rules

- Imperative mood ("add" not "added")
- Summary under 50 characters
- No period at end of summary
- One logical change per commit
- Body explains motivation, not implementation details
- Breaking changes: add `!` after type and include `BREAKING CHANGE:` footer

## Types

| Type     | Purpose                               |
| -------- | ------------------------------------- |
| feat     | New feature or functionality          |
| fix      | Bug fix                               |
| docs     | Documentation changes                 |
| style    | Code formatting, structure improvement |
| refactor | Restructuring, no behavior change     |
| perf     | Performance improvement               |
| test     | Adding or updating tests              |
| chore    | Config, tooling, maintenance          |
| ci       | CI/CD pipeline changes                |
| revert   | Reverting a previous commit           |

## Examples

**Single commit:**
```text
✨ feat(auth): add JWT token refresh

Support automatic token refresh when access token expires.
Refresh tokens stored in httpOnly cookies.
```

**Multi-commit split (auto):**
```text
# Commit 1:
♻️ refactor(api): extract validation into middleware

# Commit 2:
📝 docs(api): update endpoint documentation
```

**Breaking change:**
```text
💥 feat(api)!: restructure response format

BREAKING CHANGE: All responses now follow JSON:API spec.
See migration guide in docs/migration-v2.md.
```
