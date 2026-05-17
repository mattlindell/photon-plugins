#requires -Version 7
<#
.SYNOPSIS
    Safely remove a git worktree.

.DESCRIPTION
    Refuses to remove a worktree with uncommitted changes or unpushed commits
    unless -Force is given. Prunes empty parent directories under
    <repo>.worktrees/ (e.g. fix/ after removing fix/foo).
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Target,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

$commonDir = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRepoRoot = (Split-Path $commonDir -Parent)

# Resolve target to an absolute worktree path
$worktreePath = $null
if (Test-Path $Target -PathType Container) {
    $worktreePath = (git -C $Target rev-parse --path-format=absolute --show-toplevel).Trim()
} else {
    $list = git -C $mainRepoRoot worktree list --porcelain
    $currentWt = $null
    foreach ($line in $list) {
        if ($line -match '^worktree (.+)$') { $currentWt = $Matches[1] }
        elseif ($line -match '^branch refs/heads/(.+)$' -and $Matches[1] -eq $Target) {
            $worktreePath = $currentWt
            break
        }
    }
    if (-not $worktreePath) {
        Write-Error "no worktree found for branch '$Target'"
        exit 1
    }
}

if ($worktreePath -eq $mainRepoRoot) {
    Write-Error "refusing to remove the main checkout at $worktreePath"
    exit 1
}

if (-not $Force) {
    # Only block on modified tracked files / staged changes; untracked files
    # (synced .env etc.) shouldn't block removal.
    $status = git -C $worktreePath status --porcelain --untracked-files=no
    if ($status) {
        Write-Error "worktree $worktreePath has uncommitted changes (use -Force to override)"
        exit 1
    }
    $currentBranch = (git -C $worktreePath rev-parse --abbrev-ref HEAD).Trim()
    $upstream = git -C $worktreePath rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null
    if ($LASTEXITCODE -eq 0 -and $upstream) {
        $ahead = [int]((git -C $worktreePath rev-list --count "$($upstream.Trim())..HEAD").Trim())
        if ($ahead -gt 0) {
            Write-Error "branch '$currentBranch' has $ahead unpushed commit(s) (use -Force to override)"
            exit 1
        }
    }
}

# Always pass --force to git itself: by this point our script-level checks have
# verified the worktree is safe to remove by our criteria (no tracked
# modifications, no unpushed commits — unless -Force was given). git's own
# safety check otherwise refuses to delete a worktree with any untracked files
# (e.g. .env synced via sync-untracked), which is what we want it to remove.
git -C $mainRepoRoot worktree remove --force $worktreePath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Prune empty parent directories under <repo>.worktrees/
$worktreeRoot = Join-Path (Split-Path $mainRepoRoot -Parent) ((Split-Path $mainRepoRoot -Leaf) + '.worktrees')
$dir = Split-Path $worktreePath -Parent
while ($dir -and $dir -ne $worktreeRoot -and (Test-Path $dir)) {
    if (@(Get-ChildItem -LiteralPath $dir -Force).Count -eq 0) {
        Remove-Item -LiteralPath $dir -Force
        $dir = Split-Path $dir -Parent
    } else {
        break
    }
}

Write-Host "Removed worktree at $worktreePath"
