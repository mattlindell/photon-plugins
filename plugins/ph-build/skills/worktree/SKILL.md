---
name: worktree
description: Create, enter, and remove git worktrees following sibling-directory placement rules with branch-name mirroring, source-branch verification, and post-creation file copying. Use when the user asks to create a worktree, start work in a worktree, work on a feature in isolation, set up a sibling checkout, mentions `git worktree`, or invokes the EnterWorktree harness tool. Also use when removing or cleaning up worktrees.
---

# Git Worktree

Enforces a consistent sibling-directory layout for git worktrees and bakes in source-branch verification so the main checkout never gets polluted.

## Placement Rule

Worktrees live as **siblings** of the repo, never inside it:

```text
<parent>/<repo>/                    ← main checkout
<parent>/<repo>.worktrees/<branch>/ ← worktrees here
```

For gitflow-style branch names (`fix/foo`, `feat/bar`), the slash is preserved in the path: `<repo>.worktrees/fix/foo`. For flat branch names, just `<repo>.worktrees/branchname`.

## Workflow: Create

Run these steps without prompting unless one of them fails. The end state is: a sibling worktree exists, untracked config has been synced, and the agent is operating inside the worktree via `EnterWorktree`.

1. **Resolve inputs.** Get `<branch>` from the user. If they didn't name a source, default to the branch currently checked out in the main checkout.

2. **Run create-worktree** from the main repo root:

   ```bash
   # POSIX / Git Bash
   bash ${CLAUDE_PLUGIN_ROOT}/skills/worktree/scripts/create-worktree.sh <branch> [source-branch]
   ```

   ```powershell
   # PowerShell
   & "$env:CLAUDE_PLUGIN_ROOT/skills/worktree/scripts/create-worktree.ps1" <branch> [source-branch]
   ```

   The script:
   - Runs `git fetch` so remote-only source branches and stale refs are resolved correctly
   - Computes the sibling path `<parent>/<repo>.worktrees/<branch>`
   - If `<branch>` exists locally, checks it out into the new worktree
   - If `<branch>` is new, branches from `<source-branch>` (local `refs/heads/<source>` if present, else `refs/remotes/origin/<source>`)
   - Fails if the source branch is checked out anywhere with uncommitted changes
   - Fails if the repo uses gitflow-style prefixes and `<branch>` is new and lacks one
   - Prints the absolute worktree path on its final line — **capture this for steps 3 and 4**

3. **Sync untracked config** into the new worktree:

   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/skills/worktree/scripts/sync-untracked.sh <worktree-path>
   ```

   ```powershell
   & "$env:CLAUDE_PLUGIN_ROOT/skills/worktree/scripts/sync-untracked.ps1" <worktree-path>
   ```

   Default patterns: `.env`, `.env.*`, `.envrc` (anywhere in the tree, excluding `.git/`, `node_modules/`, `vendor/`). Copies preserve relative paths.

   Pass `--include-deps` (`-IncludeDeps` in PowerShell) only when the user explicitly wants `node_modules/` and `vendor/` mirrored. Skip it if the worktree's purpose involves changing `package.json` / `composer.json` — re-running `pnpm install` / `composer install` in the worktree is the right move there, and a stale copied tree just hides the diff. The sync uses a real recursive copy (never hardlinks/symlinks), so a subsequent install in the worktree won't corrupt the main checkout's dependency tree; copies are fast on CoW filesystems (ReFS, APFS, btrfs) and pay full cost on ext4/NTFS.

4. **Enter the worktree.** Call `EnterWorktree` with `path=<absolute-path-from-step-2>`. **Never pass `name`** — that triggers the default `.claude/worktrees/` location, which violates the placement rule.

5. **Begin work** in the worktree. No further confirmation needed unless the user asked for one.

## Workflow: Remove

1. **Confirm intent.** Removing a worktree deletes its working tree on disk.

2. **Run remove-worktree** from the main repo root:

   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/skills/worktree/scripts/remove-worktree.sh <branch-or-path>
   ```

   ```powershell
   & "$env:CLAUDE_PLUGIN_ROOT/skills/worktree/scripts/remove-worktree.ps1" <branch-or-path>
   ```

   The script:
   - Resolves a branch name to its worktree path via `git worktree list`
   - Refuses if the worktree has uncommitted changes or unpushed commits (override with `--force` / `-Force`)
   - Runs `git worktree remove`
   - Prunes empty parent directories (e.g., `<repo>.worktrees/fix/` after removing `fix/foo`)

3. **If the harness is tracking the session**, prefer `ExitWorktree action=remove` over the script — the harness owns its session state.

## Workflow: List / Inspect

Run `git worktree list` from any checkout. Worktrees that don't live under `<repo>.worktrees/` violate the placement rule and should be moved or removed.

## Branch Naming

- Pre-existing branch with gitflow prefix (`fix/foo`) → directory mirrors: `<repo>.worktrees/fix/foo`
- **New** branch in a repo that already uses gitflow prefixes → prefix is required; the create script will fail without one
- New branch in a repo with flat naming → use the branch name as-is: `<repo>.worktrees/branchname`

The create script detects gitflow usage by checking for any local branch containing `/`.

## Common Pitfalls

- **Don't `cd` into the worktree from the agent** — use `EnterWorktree` so the harness tracks the session
- **Don't pass `name` to `EnterWorktree`** — always pass `path`
- **Don't create worktrees inside `<repo>/.claude/worktrees/`** — the default harness location violates the rule
- **Don't skip step 3** — untracked config (`.env`, `.envrc`) won't carry over without it
