---
name: finishing
description: Use when all tasks are complete. Presents completion options and enforces test gate. Work is never left in limbo.
---

# Finishing Skill

> **Core Principle**: Tests must pass before completion. Work is never abandoned without explicit choice.

## Pre-Completion Gate

> [!CRITICAL]
> TESTS MUST PASS before presenting options.

### Step 1: Run Full Test Suite

```bash
[project test command]
```

### Step 2: Check Results

| Result | Action |
|--------|--------|
| All pass | Proceed to options |
| Any fail | STOP - fix first |

**DO NOT present completion options with failing tests.**

---

## The Five Options

After tests pass, present EXACTLY these options:

```
Work complete. Tests passing. Choose:

1. Merge locally     - Merge to [base] and delete branch
2. Create PR         - Push and open pull request
3. Keep as-is        - No action, branch remains
4. Partial rollback  - Undo selected recent tasks
5. Discard           - Delete all work (requires confirmation)
```

---

## Option Details

### Option 1: Merge Locally

```bash
git checkout [base-branch]
git merge [feature-branch]
git branch -d [feature-branch]
```

Result: Work merged, feature branch deleted

### Option 2: Create Pull Request

```bash
git push -u origin [feature-branch]
gh pr create --title "[title]" --body "[body]"
```

Result: PR created, branch preserved for review

### Option 3: Keep As-Is

No commands executed.

Result: Branch remains for future work

### Option 4: Partial Rollback

For selective undo of recent work without discarding everything.

**Step 1: List recent commits/tasks**

```
Recent changes (newest first):

1. [commit-hash] [task-id] - [description]
2. [commit-hash] [task-id] - [description]
3. [commit-hash] [task-id] - [description]

Select commits to revert [comma-separated, e.g., 1,2]:
```

**Step 2: Revert selected commits**

```bash
git revert [commit-hash-1] [commit-hash-2] --no-commit
git commit -m "Revert: [tasks reverted]"
```

**Step 3: Re-run tests after revert**

| Result | Action |
|--------|--------|
| All pass | Return to options menu |
| Any fail | Warn user, offer to abort revert |

Result: Selected work undone, branch still exists

---

### Option 5: Discard

**Requires typed confirmation: "discard"**

Only after confirmation:
```bash
git checkout [base-branch]
git branch -D [feature-branch]
```

Result: All work deleted

---

## Rules

| Rule | Why |
|------|-----|
| Never add explanations | Keep options scannable |
| Never default to an option | User must explicitly choose |
| Never proceed without choice | Prevents abandoned work |
| Discard requires confirmation | Prevents accidental loss |

---

## Option Presentation Format

```
┌─────────────────────────────────────────────────┐
│ All tasks complete. Tests passing.              │
├─────────────────────────────────────────────────┤
│ 1. Merge locally     - Merge to main, cleanup   │
│ 2. Create PR         - Push and open PR         │
│ 3. Keep as-is        - Branch remains           │
│ 4. Partial rollback  - Undo selected tasks      │
│ 5. Discard           - Delete work (confirm)    │
└─────────────────────────────────────────────────┘

Choose [1-5]:
```

---

## Deviation Logging

Work abandoned without finishing workflow:

```yaml
- id: [auto]
  timestamp: [now]
  expected: "Finishing skill invoked after task completion"
  actual: "Session ended without completion choice"
  root_cause: incomplete_workflow
  fix: |
    Always invoke finishing skill after all tasks complete.
    Add reminder to orchestration skill chain.
```

---

## Integration with Orchestration

This skill is the final step in the workflow chain:

```
orchestration → executor → verification → reviewer → finishing
```

The `orchestration` skill should invoke `finishing` when:
- All tasks marked complete
- All verifications passed
- All reviews approved

---

## Worktree Cleanup

If using git worktrees:

| Option | Worktree Action |
|--------|-----------------|
| 1. Merge | Remove worktree |
| 2. PR | Keep worktree |
| 3. Keep | Keep worktree |
| 4. Partial rollback | Keep worktree |
| 5. Discard | Remove worktree |

```bash
# Remove worktree
git worktree remove [path]
```