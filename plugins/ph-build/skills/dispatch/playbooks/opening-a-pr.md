### Opening a PR

Invoked at the end of every other playbook.

**Worktree.** Work from a git worktree off main; subagents inherit it. Multiple `Agent` calls on the same branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Dirty branch with unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally. Before you commit, merge, or deploy from a worktree, list the live agents and stop every one that holds it, including grandchildren you never launched; a delegate's children do not inherit its brief, so a read-only instruction never reaches them. Confirm each stop, then run `git status` and read the tree you are about to ship.

**Commits.** Commit liberally; rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit; new commit when separable.

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

**Forge.** Resolve the forge before the first PR operation and keep that choice for create, edit, view, watch, and merge. GitHub CLI (`gh`) is the default. If `command -v origin` succeeds and Origin can resolve the repository, prefer `origin pr ...`; if Origin is absent or cannot resolve the repository, stay on `gh` and record the fallback. Do not require Graphite (`gt`).

**Size and stacks.** Prefer five narrow PRs to one large PR. A stack is a base-branch chain. The root PR targets trunk; each child branch rebases onto its parent's exact tip and its PR targets the parent branch. Create a child with `origin pr create --status open --base <parent-branch>` or `gh pr create --base <parent-branch>` according to the resolved forge. Retarget an existing child with `origin pr edit <pr> --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`. Branch from trunk only for independent work. Rebase on trunk before substantial stack work.

**Readiness.** Open every PR ready, never as a draft. With Origin, pass `--status open`; with `gh`, omit `--draft`. Some PR tools default to draft, so check every creation call. If a PR still opens as a draft, run `origin pr ready <number>` or `gh pr ready <number>` according to the resolved forge. Run `origin pr view <number>` or `gh pr view <number>` before you refer to PR status.

**Babysit.** Opening a PR does not start a babysit. Post the URL and keep building. Finish the phase or stack first. Run a separate babysit pass only when the user asks for one after the whole stack exists, per `babysit.md`. A babysit for each new PR stalls the build and spends checks on commits that later waves restart. Push back when feedback drifts from intent.

A subagent that opens a PR always calls the Skill tool twice, for `deslop` and `no-comments` — both are single-pass and cheap. It runs `interrogate` **only** when the change touches a one-way door (schema, public API, irreversible data handling, auth, billing); `interrogate` is a three-model panel and must not ride along on every PR. It returns the URL and does not babysit. Return to the parent.
