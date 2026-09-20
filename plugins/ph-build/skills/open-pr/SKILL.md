---
name: open-pr
description: Take a finished branch to an open pull request: clean it, commit what is outstanding, push, and write the body against this repo's standard.
disable-model-invocation: true
---

# Open a PR

The branch is finished. This takes it to an open PR in one pass: read the tree,
clean it, commit what is outstanding, push, open, and hand back the URL.

Stop at the URL. Driving the PR to green is a separate command,
`/ph-build:babysit`, so three branches can open before anything watches checks.

## Start state

Run `git status` and read the tree you are about to ship.

**Refuse on the default branch.** If `HEAD` is the remote's default branch, stop
and say so. Do not branch on the user's behalf. Every other start state is
cheap to recover from. This one is not, so stop instead of guessing.

Fix every other start state and keep going. Uncommitted work, a missing
upstream, and sprawling history each have a step below.

1. Run `/ph-build:deslop` over the diff.
2. Run `/ph-build:no-comments`.
3. Commit anything outstanding, per `../commit/SKILL.md`. A dirty tree must not
   silently ship a partial branch.
4. Rebase into small, ordered commits. Each commit is a future PR: landable,
   ordered to tell the story. Amend when the fix belongs in a just-made commit;
   open a new commit when the change is separable.
5. Push, and set upstream when the branch has none: `git push -u origin HEAD`.

## Forge

Resolve the forge before the first PR operation and keep that choice for create,
edit, view, watch, and merge. GitHub CLI (`gh`) is the default. If
`command -v origin` succeeds and Origin can resolve the repository, prefer
`origin pr ...`; if Origin is absent or cannot resolve the repository, stay on
`gh` and record the fallback. Do not require Graphite (`gt`).

## Writing

Write every PR title and PR description with `ph-lib:technical-writing`, then
apply `ph-lib:unslop`. Apply every technical-writing layer except Diátaxis. Use
one word for each action, keep articles, and avoid `-ing` when a plain verb
works.

### Titles

Use gitmoji plus Conventional Commits, in the form
`<emoji> type(scope): subject`. Pick the emoji from
`../commit/gitmoji-reference.md`. Use `feat`, `fix`, `docs`, `refactor`,
`test`, `chore`, or `perf` as the type. Use the
changed area, such as `ph-build` or `dispatch`, as the scope. Keep the subject
short and imperative. Name a real symbol when one carries the change. For
example, `✨ feat(ph-build): add open-pr skill`. Do not add a trailing period.

### Descriptions

The PR body is a briefing, not the lab notebook. A reviewer who has the diff
should learn why the change exists, what is out of scope, and how you proved the
change works. The squash commit body is the PR body. If the body would make the
squash commit longer than about 40 lines, cut the body.

Use these sections in order. **Drop a section when it has nothing to say** — the
body is a briefing, not a form.

- `## Why`. State the intent and approach in one or two short paragraphs. Do not
  list SHAs or rebase genealogy. Do not add a "based on main" preamble.
- `## Scope`. Use bullets to list real symbols and paths. Name both sides of a
  rename or retarget. State what is in and out only when the boundary matters.
  Do not write a file-by-file essay.
- `## Tradeoffs`. Name only rejected alternatives that a reviewer would otherwise
  ask about. Skip this section when there was no real choice.
- `## Blast Radius`. In one to three sentences, name who or what the change
  touches and why the change is safe or risky. State the continuing cost if main
  stays red without the fix.
- `## Verification`. Name each real run path and its outcome. For a performance
  change, report one primary number with its unit in `before → after` form. Link
  the arena or swarm directory for the remaining evidence. Do not include
  sample-size methodology, swarm recitals, or metric tables.

After these sections, attach videos or screenshots when they prove a claim. Do
not paste full SHAs, swarm or arena lane recitals, lever-correction essays,
file-by-file checklists, or "CLEAN" verdicts. Put these details in a linked
artifact. Do not use `## Summary` or `## Test plan` boilerplate. A commit body
does not restate its subject.

## Size and stacks

Prefer five narrow PRs to one large PR. A stack is a base-branch chain. The root
PR targets trunk; each child branch rebases onto its parent's exact tip and its
PR targets the parent branch. Create a child with
`origin pr create --status open --base <parent-branch>` or
`gh pr create --base <parent-branch>` according to the resolved forge. Retarget
an existing child with `origin pr edit <pr> --base <parent-branch>` or
`gh pr edit <pr> --base <parent-branch>`. Branch from trunk only for independent
work. Rebase on trunk before substantial stack work.

## Readiness

Open every PR ready, never as a draft. With Origin, pass `--status open`; with
`gh`, omit `--draft`. Some PR tools default to draft, so check every creation
call. If a PR still opens as a draft, run `origin pr ready <number>` or
`gh pr ready <number>` according to the resolved forge. Run
`origin pr view <number>` or `gh pr view <number>` before you refer to PR
status.

## After it opens

Transition the ticket the branch names. Where the tracker is Linear and the
branch carries the issue key, that is
`linearis issues update <KEY> --status "In Review"`. The forge integration links
the PR to the issue by branch name, so the body needs no magic word.

Then print the URL and stop. Opening a PR does not start a babysit — finish the
phase or the whole stack first, and run `/ph-build:babysit` when the user asks
for one. A babysit per PR stalls the build and spends checks on commits that
later waves restart.

## When an unattended agent runs this

A `dispatch` subagent reaches this file by path and follows the same procedure,
with three additions.

**`/ph-build:deslop` and `/ph-build:no-comments` are not optional.** Both are
single-pass and cheap, and an unattended run has no reviewer behind it.

**Worktree discipline.** Work from a git worktree off main; subagents inherit
it. Multiple `Agent` calls on the same branch each get their own worktree, or
`git fetch && git reset --hard origin/<branch>` between them. Dirty branch with
unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from
main, redo minimally. Before you commit, merge, or deploy from a worktree, list
the live agents and stop every one that holds it, including grandchildren you
never launched; a delegate's children do not inherit its brief, so a read-only
instruction never reaches them. Confirm each stop before reading the tree.

**Return the URL to the parent and do not babysit.** Push back when feedback
drifts from intent.
