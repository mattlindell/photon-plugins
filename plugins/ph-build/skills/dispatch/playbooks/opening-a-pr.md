### Opening a PR

Invoked at the end of every other playbook.

Work from a git worktree off trunk, and keep unrelated work out of it. Rebase into small, landable commits; a commit body does not restate its subject. Before you commit, merge, or deploy from a worktree, list the live agents and stop every one that holds it, including grandchildren you never launched. Confirm each stop, then run `git status` and read the tree you are about to ship.

**PRs.** Call the Skill tool with `deslop` over the diff before commit, and with `no-comments` before review. Write every PR title, PR description, and commit body with `ph-lib:technical-writing`, then apply `ph-lib:unslop`. Call the Skill tool once for each. Apply every technical-writing layer except Diátaxis. Use one word for each action, keep articles, and avoid `-ing` when a plain verb works.

**Titles.** Use Conventional Commits in the form `type(scope): subject`. Use `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf` as the type. Use the changed area, such as `ph-build` or `dispatch`, as the scope. Keep the subject short and imperative. Name a real symbol when one carries the change. For example, `fix(ph-build): retarget opening-a-pr babysit trigger`. Do not add a trailing period.

**Descriptions.** The PR body is a one-minute briefing for a reviewer who has the diff, not a lab notebook. It says why the change exists, what it leaves out, what it could break, and how you proved it works. Write short, simple sentences with few identifiers, and no walls of text. The body becomes the squash commit body, so keep that commit under about 40 lines.

Use `##` headings, not bold lead-ins, in this order. Drop a section with nothing to say.

- `## Why`. The problem and the approach, in one to three short sentences. Name the ticket by key when the work came from one — the tracker links the PR through the branch name or through this section, and a branch that does not carry the key leaves this as the only channel. No SHAs, rebase genealogy, or "based on main" preamble.
- `## What changed`. One to three short bullets. Name a real symbol or path only when it carries the change. Name both sides of a rename or retarget.
- `## Scope`. Always present. One to three short items on what the change covers and what it deliberately leaves out, such as a follow-up or a known gap. No symbols, paths, or file-by-file essay.
- `## Tradeoffs`. Only rejected alternatives that a reviewer would otherwise ask about. Skip this section when there was no real choice.
- `## Blast Radius`. One or two sentences on who or what the change touches and why that is safe or risky. If main is red, state the cost of leaving it red.
- `## Verification`. One to three bullets, each a real run path and its outcome. For a performance change, report one primary number with its unit in `before → after` form, and link the arena or swarm directory for the rest. No sample-size methodology, swarm recitals, or metric tables.

After these sections, attach videos or screenshots when they prove a claim. Full SHAs, swarm or arena lane recitals, lever-correction essays, file-by-file checklists, and "CLEAN" verdicts go in a linked artifact, not the body. Do not use `## Summary` or `## Test plan` boilerplate. A commit body does not restate its subject.

Stack follow-ups by base branch. Open PRs ready, through the run's PR tool with `draft: false`. Without one, use `gh pr create` without `--draft`, or `origin pr create --status open` when Origin's CLI resolves the repository. Opening a PR does not start a babysit; post the URL and keep building, and run a babysit pass only when the user asks, per `babysit.md`.

A subagent that opens a PR always calls the Skill tool twice, for `deslop` and `no-comments` — both are single-pass and cheap. When the change touches a one-way door (schema, public API, irreversible data handling, auth, billing), it recommends `/interrogate` in the PR description as the human's step before merge. That three-model panel must not ride along on every PR. It returns the URL and does not babysit. Return to the parent.
