#!/usr/bin/env bash
# Copy untracked config files from the main checkout into a worktree.
#
# Usage: sync-untracked.sh <worktree-path> [--include-deps]
#
# Defaults: any untracked file whose basename matches `.env`, `.env.*`, or `.envrc`,
# anywhere in the main checkout (excluding .git/ and node_modules/). Preserves
# relative paths.
#
# --include-deps additionally copies node_modules/ and vendor/ at any depth where
# they exist in the main checkout. This is a real recursive copy (no hardlinks,
# no symlinks) so a later `pnpm install` / `composer install` in the worktree
# won't corrupt the main checkout's dependency tree. The copy is fast on CoW
# filesystems (ReFS, APFS, btrfs) and pays full cost elsewhere.

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: $0 <worktree-path> [--include-deps]" >&2
  exit 2
fi

worktree_path="$(git -C "$1" rev-parse --path-format=absolute --show-toplevel)"
include_deps=0
if [ "${2:-}" = "--include-deps" ]; then
  include_deps=1
fi

common_dir="$(git -C "$worktree_path" rev-parse --path-format=absolute --git-common-dir)"
main_repo_root="$(dirname "$common_dir")"

if [ "$worktree_path" = "$main_repo_root" ]; then
  echo "ERROR: target path is the main checkout, not a worktree" >&2
  exit 1
fi

copied_count=0

copy_file() {
  local src="$1"
  local rel="${src#$main_repo_root/}"
  local dst="$worktree_path/$rel"
  mkdir -p "$(dirname "$dst")"
  cp -p "$src" "$dst"
  echo "  $rel" >&2
  copied_count=$((copied_count + 1))
}

copy_dir() {
  local src="$1"
  local rel="${src#$main_repo_root/}"
  local dst="$worktree_path/$rel"
  if [ -e "$dst" ]; then
    return 0
  fi
  mkdir -p "$(dirname "$dst")"
  # Real recursive copy — no hardlinks/symlinks
  cp -R "$src" "$dst"
  echo "  $rel/ (recursive copy)" >&2
  copied_count=$((copied_count + 1))
}

echo "Syncing untracked config from $main_repo_root..." >&2

# Find .env*, .envrc files in the main checkout, excluding .git/ and node_modules/
while IFS= read -r -d '' f; do
  copy_file "$f"
done < <(
  find "$main_repo_root" \
    \( -name .git -o -name node_modules -o -name vendor \) -prune -o \
    -type f \( -name '.env' -o -name '.env.*' -o -name '.envrc' \) -print0
)

if [ "$include_deps" -eq 1 ]; then
  echo "Copying dependency directories (real copy, may be slow on non-CoW filesystems)..." >&2
  while IFS= read -r -d '' d; do
    copy_dir "$d"
  done < <(
    find "$main_repo_root" \
      -name .git -prune -o \
      -type d \( -name node_modules -o -name vendor \) -prune -print0
  )
fi

if [ "$copied_count" -eq 0 ]; then
  echo "Nothing to sync." >&2
else
  echo "Synced $copied_count item(s) into $worktree_path." >&2
fi
