#!/usr/bin/env bash
# Create a git worktree as a sibling of the main repo.
#
# Usage: create-worktree.sh <branch> [source-branch]
#
# Rules:
#   - Worktree path: <parent>/<repo>.worktrees/<branch>
#   - Branch names with slashes (e.g. fix/foo) are preserved in the path
#   - Runs `git fetch` first so remote-only source branches resolve
#   - If <branch> exists locally, checks it out into the new worktree
#   - If <branch> is new, branches from <source-branch>:
#       - refs/heads/<source> if present locally
#       - else refs/remotes/origin/<source>
#       - else error
#   - Refuses to run if the source branch is checked out anywhere with uncommitted changes
#   - Refuses to create a new unprefixed branch in a gitflow-style repo
#
# Prints the absolute path of the new worktree on the final line.

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: $0 <branch> [source-branch]" >&2
  exit 2
fi

branch="$1"
source_branch="${2:-}"

# Find the main repo root via git-common-dir (works from inside a worktree too).
# --path-format=absolute (git 2.31+) returns a native-style absolute path so
# subsequent `git -C` invocations work correctly on Windows.
common_dir="$(git rev-parse --path-format=absolute --git-common-dir)"
main_repo_root="$(dirname "$common_dir")"

repo_name="$(basename "$main_repo_root")"
parent_dir="$(dirname "$main_repo_root")"
worktree_root="$parent_dir/$repo_name.worktrees"
worktree_path="$worktree_root/$branch"

if [ -e "$worktree_path" ]; then
  echo "ERROR: $worktree_path already exists" >&2
  exit 1
fi

# Fetch up front so remote-only refs and out-of-date refs are usable
echo "Fetching from origin..." >&2
git -C "$main_repo_root" fetch --quiet origin || true

branch_exists_local=0
if git -C "$main_repo_root" show-ref --verify --quiet "refs/heads/$branch"; then
  branch_exists_local=1
fi

# Verify source branch is clean IF it's checked out somewhere
verify_clean_if_checked_out() {
  local ref="$1"
  local checked_out_path
  checked_out_path="$(git -C "$main_repo_root" worktree list --porcelain \
    | awk -v ref="refs/heads/$ref" '
      /^worktree / { wt = substr($0, 10) }
      /^branch /   { if ($2 == ref) print wt }
    ')"
  if [ -n "$checked_out_path" ]; then
    # Only block on modified tracked files / staged changes; untracked files
    # (e.g. .env) are expected and handled by sync-untracked.
    if [ -n "$(git -C "$checked_out_path" status --porcelain --untracked-files=no)" ]; then
      echo "ERROR: source branch '$ref' is checked out at $checked_out_path and has uncommitted changes" >&2
      echo "       Commit, stash, or discard those changes first." >&2
      exit 1
    fi
  fi
}

mkdir -p "$worktree_root"

if [ "$branch_exists_local" -eq 1 ]; then
  verify_clean_if_checked_out "$branch"
  git -C "$main_repo_root" worktree add "$worktree_path" "$branch" >&2
else
  # Hard-fail if repo uses gitflow naming and the new branch has no prefix
  if [[ "$branch" != */* ]]; then
    gitflow_count="$(git -C "$main_repo_root" for-each-ref --format='%(refname:short)' refs/heads \
      | grep -c '/' || true)"
    if [ "$gitflow_count" -gt 0 ]; then
      echo "ERROR: this repo uses gitflow-style prefixes (e.g. feat/, fix/) but '$branch' has none." >&2
      echo "       Re-run with a prefixed branch name (e.g. feat/$branch or fix/$branch)." >&2
      exit 1
    fi
  fi

  if [ -z "$source_branch" ]; then
    source_branch="$(git -C "$main_repo_root" rev-parse --abbrev-ref HEAD)"
  fi

  # Resolve source: prefer local branch, fall back to remote-tracking
  if git -C "$main_repo_root" show-ref --verify --quiet "refs/heads/$source_branch"; then
    verify_clean_if_checked_out "$source_branch"
    git -C "$main_repo_root" worktree add "$worktree_path" -b "$branch" "$source_branch" >&2
  elif git -C "$main_repo_root" show-ref --verify --quiet "refs/remotes/origin/$source_branch"; then
    echo "Source branch '$source_branch' exists only on origin; branching from origin/$source_branch." >&2
    git -C "$main_repo_root" worktree add "$worktree_path" -b "$branch" --track "origin/$source_branch" >&2
  else
    echo "ERROR: source branch '$source_branch' does not exist locally or on origin" >&2
    exit 1
  fi
fi

# Absolute path on final line — consumers should read the last line.
# Use git's path-format=absolute so the output is native-style (Windows-friendly).
git -C "$worktree_path" rev-parse --path-format=absolute --show-toplevel
