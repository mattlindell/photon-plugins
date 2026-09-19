#requires -Version 7
<#
.SYNOPSIS
    Create a git worktree as a sibling of the main repo.

.DESCRIPTION
    Rules:
      - Worktree path: <parent>/<repo>.worktrees/<branch>
      - Branch names with slashes (e.g. fix/foo) are preserved in the path
      - Runs `git fetch` first so remote-only source branches resolve
      - If <Branch> exists locally, checks it out into the new worktree
      - If <Branch> is new, branches from <SourceBranch>:
          * refs/heads/<source> if present locally
          * else refs/remotes/origin/<source>
          * else error
      - Refuses to run if the source branch is checked out anywhere with uncommitted changes
      - Refuses to create a new unprefixed branch in a gitflow-style repo

    Prints the absolute path of the new worktree on the final line.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Branch,
    [Parameter(Position = 1)][string]$SourceBranch
)

$ErrorActionPreference = 'Stop'

$commonDir = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRepoRoot = (Split-Path $commonDir -Parent)
$repoName = Split-Path $mainRepoRoot -Leaf
$parentDir = Split-Path $mainRepoRoot -Parent
$worktreeRoot = Join-Path $parentDir "$repoName.worktrees"
$worktreePath = Join-Path $worktreeRoot $Branch

if (Test-Path $worktreePath) {
    Write-Error "$worktreePath already exists"
    exit 1
}

Write-Information "Fetching from origin..." -InformationAction Continue
git -C $mainRepoRoot fetch --quiet origin 2>$null

$branchExistsLocal = $false
git -C $mainRepoRoot show-ref --verify --quiet "refs/heads/$Branch"
if ($LASTEXITCODE -eq 0) { $branchExistsLocal = $true }

function Test-SourceClean {
    param([string]$Ref)
    $list = git -C $mainRepoRoot worktree list --porcelain
    $checkedOutPath = $null
    $currentWt = $null
    foreach ($line in $list) {
        if ($line -match '^worktree (.+)$') { $currentWt = $Matches[1] }
        elseif ($line -match '^branch refs/heads/(.+)$' -and $Matches[1] -eq $Ref) {
            $checkedOutPath = $currentWt
        }
    }
    if ($checkedOutPath) {
        # Only block on modified tracked files / staged changes; untracked
        # files (e.g. .env) are expected and handled by sync-untracked.
        $status = git -C $checkedOutPath status --porcelain --untracked-files=no
        if ($status) {
            Write-Error "source branch '$Ref' is checked out at $checkedOutPath and has uncommitted changes. Commit, stash, or discard first."
            exit 1
        }
    }
}

New-Item -ItemType Directory -Force -Path $worktreeRoot | Out-Null

if ($branchExistsLocal) {
    Test-SourceClean -Ref $Branch
    git -C $mainRepoRoot worktree add $worktreePath $Branch
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    # Hard-fail if repo uses gitflow naming and the new branch has no prefix
    if ($Branch -notmatch '/') {
        $branches = git -C $mainRepoRoot for-each-ref --format='%(refname:short)' refs/heads
        $gitflowCount = @($branches | Where-Object { $_ -match '/' }).Count
        if ($gitflowCount -gt 0) {
            Write-Error "this repo uses gitflow-style prefixes (e.g. feat/, fix/) but '$Branch' has none. Re-run with a prefixed branch name (e.g. feat/$Branch or fix/$Branch)."
            exit 1
        }
    }

    if (-not $SourceBranch) {
        $SourceBranch = (git -C $mainRepoRoot rev-parse --abbrev-ref HEAD).Trim()
    }

    git -C $mainRepoRoot show-ref --verify --quiet "refs/heads/$SourceBranch"
    $hasLocal = ($LASTEXITCODE -eq 0)

    if ($hasLocal) {
        Test-SourceClean -Ref $SourceBranch
        git -C $mainRepoRoot worktree add $worktreePath -b $Branch $SourceBranch
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        git -C $mainRepoRoot show-ref --verify --quiet "refs/remotes/origin/$SourceBranch"
        if ($LASTEXITCODE -eq 0) {
            Write-Information "Source branch '$SourceBranch' exists only on origin; branching from origin/$SourceBranch." -InformationAction Continue
            git -C $mainRepoRoot worktree add $worktreePath -b $Branch --track "origin/$SourceBranch"
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        } else {
            Write-Error "source branch '$SourceBranch' does not exist locally or on origin"
            exit 1
        }
    }
}

(Resolve-Path $worktreePath).Path
