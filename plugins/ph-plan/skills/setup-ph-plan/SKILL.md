---
name: setup-ph-plan
description: Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
disable-model-invocation: true
---

# Set Up ph-plan

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; GitLab, Jira, Linear, and local markdown also have routes)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` — is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use
- `.gitignore` — does it already ignore `*.local.*` or `*.local.md`? This matters only for the Linear route.
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals — a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarize what's present and what's missing. Then take the sections in order — one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches, and drop a section's *question* when exploration already settled it: Section B disappears entirely when `triage` isn't installed, and Section C's choice disappears when there's no monorepo — though its single-context default is still drafted in step 3 and written in step 4.

**Section A — Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it — they need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, create a Jira or Linear issue, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub.** Issues live in the repo's GitHub Issues, through the `gh` CLI.
- **GitLab.** Issues live in the repo's GitLab Issues, through the [`glab`](https://gitlab.com/gitlab-org/cli) CLI.
- **Local markdown.** Issues live as files under `.scratch/<feature>/` in this repo. This suits solo projects and repos without a remote.
- **Jira.** Tickets live in a Jira project. Specs, maps, and research live in a wiki such as Confluence, or as Jira issues.
- **Linear.** Tickets live in a Linear project. Each effort is a milestone, and its specs, maps, and research are Documents attached to the project.
- **Other.** Ask the user to describe the workflow in one paragraph, and record it as freeform prose.

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off** — leave it off and don't raise it; a user who wants external PRs in the triage queue can flip the flag in the file later.

**Jira follow-ups.** Ask where specs, maps, and research live: in a wiki such as Confluence (recommended when the team has one), or as Jira issues. In the template's **Specs, maps, and research** section, keep the subsection that matches, delete the other, and drop the kept subsection's `###` heading. Then collect the template's coordinates and substitute them throughout: the site, project key, ticket issue type, and effort issue type, plus the space key and the page that holds effort pages when specs live in a wiki. Use only standard issue types. Leave out anything that depends on a custom issue type or a custom field.

**Linear follow-ups.** Collect the team key and the project name. Then ask one question:

> Keep the team and project out of the committed file, in a gitignored `docs/agents/linear-ids.local.md`? (recommended: **yes** for a public repo)

On **yes**, keep the `<TEAM>` and `<PROJECT>` placeholders in `issue-tracker.md` and write the local file from [references/linear-ids-local.md](references/linear-ids-local.md) with the values filled in. Its connection-preference section is where a person records which CLI or MCP server their machine uses. Check that `.gitignore` covers the file, and add `*.local.*` if it doesn't. On **no**, replace each placeholder with its value throughout `issue-tracker.md` and delete the paragraph that points at the local file.

Neither the Jira nor the Linear template names a connection method. Don't add one. The agent uses whatever tracker access the runner has.

**Section B — Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you) — an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no — usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`) — collect the overrides so `triage` applies existing labels instead of creating duplicates.

Either way, seed the "Claim roles" section from the template with its defaults. Don't ask about it: `/ph-build:foreman` reads it, and a user who wants a custom field instead of labels can edit the file later.

**Section C — Domain docs.** Default to **single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. This fits almost every repo; write it without asking.

Offer **multi-context** — a root `CONTEXT-MAP.md` pointing to per-context `CONTEXT.md` files — only when exploration found monorepo signals. Then confirm which layout they want.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)
- On the Linear route with the local split, `docs/agents/linear-ids.local.md`

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

When Section B ran on GitHub, GitLab, or Linear, create each configured label the tracker lacks with `gh label create` or `glab label create`. On Linear, create it as a workspace-level label through whatever Linear access the runner has. Skip label creation for Jira, which creates a label the first time an issue uses it, and for local markdown, which has no labels.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [references/issue-tracker-github.md](references/issue-tracker-github.md) — GitHub issue tracker
- [references/issue-tracker-gitlab.md](references/issue-tracker-gitlab.md) — GitLab issue tracker
- [references/issue-tracker-jira.md](references/issue-tracker-jira.md): Jira issue tracker, with specs in a wiki or in Jira
- [references/issue-tracker-linear.md](references/issue-tracker-linear.md): Linear issue tracker, with each effort as a milestone
- [references/linear-ids-local.md](references/linear-ids-local.md): gitignored Linear coordinates and connection preference, written only when the user keeps them local
- [references/issue-tracker-local.md](references/issue-tracker-local.md) — local-markdown issue tracker
- [references/triage-labels.md](references/triage-labels.md) — label mapping (only if `triage` is installed)
- [references/domain.md](references/domain.md) — domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later — re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
