#!/usr/bin/env bash
# Safely remove a git worktree.
#
# Usage: remove-worktree.sh <branch-or-path> [--force]
#
# Refuses to remove a worktree with uncommitted changes or unpushed commits
# unless --force is given. Prunes empty parent directories under
# <repo>.worktrees/ (e.g. fix/ after removing fix/foo).

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: $0 <branch-or-path> [--force]" >&2
  exit 2
fi

target="$1"
force=0
if [ "${2:-}" = "--force" ]; then
  force=1
fi

common_dir="$(git rev-parse --path-format=absolute --git-common-dir)"
main_repo_root="$(dirname "$common_dir")"

# Resolve target to an absolute worktree path
worktree_path=""
if [ -d "$target" ]; then
  worktree_path="$(git -C "$target" rev-parse --path-format=absolute --show-toplevel)"
else
  # Treat target as a branch name and look it up in the worktree list
  worktree_path="$(git -C "$main_repo_root" worktree list --porcelain \
    | awk -v ref="refs/heads/$target" '
      /^worktree / { wt = substr($0, 10) }
      /^branch /   { if ($2 == ref) print wt }
    ')"
  if [ -z "$worktree_path" ]; then
    echo "ERROR: no worktree found for branch '$target'" >&2
    exit 1
  fi
fi

if [ "$worktree_path" = "$main_repo_root" ]; then
  echo "ERROR: refusing to remove the main checkout at $worktree_path" >&2
  exit 1
fi

# Safety checks
if [ "$force" -eq 0 ]; then
  # Only block on modified tracked files / staged changes; untracked files
  # (synced .env etc.) shouldn't block removal.
  if [ -n "$(git -C "$worktree_path" status --porcelain --untracked-files=no)" ]; then
    echo "ERROR: worktree $worktree_path has uncommitted changes (use --force to override)" >&2
    exit 1
  fi
  # Check for unpushed commits on the worktree's current branch
  current_branch="$(git -C "$worktree_path" rev-parse --abbrev-ref HEAD)"
  upstream="$(git -C "$worktree_path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  if [ -n "$upstream" ]; then
    ahead="$(git -C "$worktree_path" rev-list --count "$upstream..HEAD")"
    if [ "$ahead" -gt 0 ]; then
      echo "ERROR: branch '$current_branch' has $ahead unpushed commit(s) (use --force to override)" >&2
      exit 1
    fi
  fi
fi

# Always pass --force to git itself: by this point our script-level checks have
# verified the worktree is safe to remove by our criteria (no tracked
# modifications, no unpushed commits — unless --force was given). git's own
# safety check otherwise refuses to delete a worktree with any untracked files
# (e.g. .env synced via sync-untracked), which is what we want it to remove.
git -C "$main_repo_root" worktree remove --force "$worktree_path"

# Prune empty parent directories under <repo>.worktrees/
worktree_root="$(dirname "$main_repo_root")/$(basename "$main_repo_root").worktrees"
dir="$(dirname "$worktree_path")"
while [ "$dir" != "$worktree_root" ] && [ "$dir" != "/" ]; do
  rmdir "$dir" 2>/dev/null || break
  dir="$(dirname "$dir")"
done

echo "Removed worktree at $worktree_path" >&2
