---
name: parallel-dispatch
description: Use when facing multiple tasks or failures. Provides decision framework for concurrent vs sequential execution. Invoke before dispatching multiple subagents.
---

# Parallel Dispatch Skill

> **Core Principle**: Parallelize only when tasks are truly independent.

## Decision Framework

```
┌─────────────────────────────────────────┐
│ Are tasks independent?                  │
│ (fixing one won't affect others)        │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
       YES                  NO
        │                   │
        ▼                   ▼
┌───────────────┐    ┌──────────────────┐
│ Will they     │    │   SEQUENTIAL     │
│ edit the same │    │   Execute one    │
│ files?        │    │   at a time      │
└───────┬───────┘    └──────────────────┘
        │
    ┌───┴───┐
    │       │
   NO      YES
    │       │
    ▼       ▼
┌────────┐ ┌──────────────────┐
│PARALLEL│ │   SEQUENTIAL     │
│  OK    │ │   Avoid conflicts│
└────────┘ └──────────────────┘
```

---

## When to Parallelize

✅ **Safe for Parallel:**
- Independent test failures in different files
- Unrelated bugs in separate subsystems
- Documentation updates to different sections
- Adding features to isolated modules

❌ **Must be Sequential:**
- Failures that share root causes
- Tasks editing the same files
- Changes with dependencies between them
- Shared resource access (database, API limits)

---

## Parallel Dispatch Contract

Each parallel agent receives:

| Requirement | Why |
|-------------|-----|
| Isolated scope | One file or subsystem only |
| No shared resources | Prevent race conditions |
| Independent success criteria | Can be verified alone |
| Merge review after | Catch any conflicts |

---

## Dispatch Template

For each parallel task:

```yaml
task_id: [unique identifier]
scope: [specific file or subsystem]
isolation:
  files_to_edit: [list]
  files_read_only: [list]
  shared_resources: none
success_criteria:
  - [criterion 1]
  - [criterion 2]
```

---

## Post-Parallel Merge Protocol

After all parallel agents complete:

1. **Collect** all outputs
2. **Check** for conflicting changes (same lines edited)
3. **Verify** each independently
4. **Merge** if no conflicts
5. **Run** full test suite
6. **Report** combined results

---

## Example: Parallel Decision

**Scenario**: 6 test failures across 3 files

```
tests/auth.test.ts    - 2 failures (login, logout)
tests/api.test.ts     - 3 failures (get, post, delete)
tests/utils.test.ts   - 1 failure (formatDate)
```

**Analysis**:
- Are they independent? YES - different test files, different functionality
- Will they edit same files? NO - each test file has its own implementation
- Decision: **PARALLEL**

**Dispatch**:
- Agent 1: auth.test.ts failures
- Agent 2: api.test.ts failures
- Agent 3: utils.test.ts failures

---

## Example: Sequential Decision

**Scenario**: 3 failures all mentioning "database connection"

**Analysis**:
- Are they independent? NO - likely shared root cause
- Decision: **SEQUENTIAL** - fix database issue first, others may resolve

---

## Integration with Orchestration

This skill is invoked from `orchestration` skill when:
- Multiple tasks are identified
- Multiple failures need investigation
- Batch execution is planned

Chain: `orchestration` → `parallel-dispatch` (decision) → `executor` (dispatch)

---

## Deviation Logging

Parallel dispatch conflicts logged:

```yaml
- id: [auto]
  timestamp: [now]
  expected: "Independent tasks"
  actual: "Conflicting edits to same file"
  root_cause: improper_parallelization
  fix: |
    Add file-level isolation check before parallel dispatch.
    Require explicit file lists in task contracts.
```