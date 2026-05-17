#requires -Version 7
<#
.SYNOPSIS
    Copy untracked config files from the main checkout into a worktree.

.DESCRIPTION
    Defaults: any untracked file whose basename matches `.env`, `.env.*`, or `.envrc`,
    anywhere in the main checkout (excluding .git/, node_modules/, vendor/).
    Preserves relative paths.

    -IncludeDeps additionally copies node_modules/ and vendor/ at any depth where
    they exist in the main checkout. This is a real recursive copy (no hardlinks,
    no symlinks) so a later `pnpm install` / `composer install` in the worktree
    won't corrupt the main checkout's dependency tree. The copy is fast on CoW
    filesystems (ReFS, APFS, btrfs) and pays full cost elsewhere.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$WorktreePath,
    [switch]$IncludeDeps
)

$ErrorActionPreference = 'Stop'

$worktreePath = (git -C $WorktreePath rev-parse --path-format=absolute --show-toplevel).Trim()
$commonDir = (git -C $worktreePath rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRepoRoot = (Split-Path $commonDir -Parent)

if ($worktreePath -eq $mainRepoRoot) {
    Write-Error "target path is the main checkout, not a worktree"
    exit 1
}

$copiedCount = 0

function Copy-OneFile {
    param([string]$Src)
    $rel = $Src.Substring($mainRepoRoot.Length).TrimStart('\', '/')
    $dst = Join-Path $worktreePath $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
    Copy-Item -LiteralPath $Src -Destination $dst -Force
    Write-Host "  $rel"
    $script:copiedCount++
}

function Copy-OneDir {
    param([string]$Src)
    $rel = $Src.Substring($mainRepoRoot.Length).TrimStart('\', '/')
    $dst = Join-Path $worktreePath $rel
    if (Test-Path $dst) { return }
    New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
    # Real recursive copy — no hardlinks/symlinks
    Copy-Item -LiteralPath $Src -Destination $dst -Recurse -Force
    Write-Host "  $rel/ (recursive copy)"
    $script:copiedCount++
}

Write-Host "Syncing untracked config from $mainRepoRoot..."

$excludeDirs = @('.git', 'node_modules', 'vendor')

$envFiles = Get-ChildItem -LiteralPath $mainRepoRoot -Recurse -Force -File -ErrorAction SilentlyContinue |
    Where-Object {
        $relativeParts = $_.FullName.Substring($mainRepoRoot.Length).TrimStart('\', '/') -split '[\\/]'
        $inExcluded = $false
        foreach ($part in $relativeParts) {
            if ($excludeDirs -contains $part) { $inExcluded = $true; break }
        }
        if ($inExcluded) { return $false }
        return ($_.Name -eq '.env' -or $_.Name -like '.env.*' -or $_.Name -eq '.envrc')
    }

foreach ($f in $envFiles) {
    Copy-OneFile -Src $f.FullName
}

if ($IncludeDeps) {
    Write-Host "Copying dependency directories (real copy, may be slow on non-CoW filesystems)..."
    $depDirs = Get-ChildItem -LiteralPath $mainRepoRoot -Recurse -Force -Directory -ErrorAction SilentlyContinue |
        Where-Object {
            $relativeParts = $_.FullName.Substring($mainRepoRoot.Length).TrimStart('\', '/') -split '[\\/]'
            # Exclude anything inside .git
            if ($relativeParts -contains '.git') { return $false }
            return ($_.Name -eq 'node_modules' -or $_.Name -eq 'vendor')
        } |
        # Only top-most occurrence at each branch — skip nested node_modules under another node_modules
        Where-Object {
            $rel = $_.FullName.Substring($mainRepoRoot.Length).TrimStart('\', '/')
            $parts = $rel -split '[\\/]'
            # Count occurrences of node_modules/vendor in the path
            ($parts | Where-Object { $_ -eq 'node_modules' -or $_ -eq 'vendor' }).Count -eq 1
        }

    foreach ($d in $depDirs) {
        Copy-OneDir -Src $d.FullName
    }
}

if ($copiedCount -eq 0) {
    Write-Host "Nothing to sync."
} else {
    Write-Host "Synced $copiedCount item(s) into $worktreePath."
}
