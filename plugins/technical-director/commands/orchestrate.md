---
description: Orchestrate a complex task using atomic subagent execution with verification
argument-hint: <task description>
allowed-tools: [Task, Read, Write, Glob, Grep, WebSearch, WebFetch, TodoWrite, Bash, AskUserQuestion]
---

# Orchestrate Command

You have been invoked with: `/orchestrate $ARGUMENTS`

## Protocol

You are now operating as the **Orchestrator**. Follow the orchestration skill protocol exactly.

---

### Phase 0: Pre-Flight Checklist

Before decomposing the task, verify prerequisites:

| Check | Command | Pass Condition |
|-------|---------|----------------|
| Git clean | `git status` | No uncommitted changes (or user confirms proceed) |
| Tests pass | `[project test command]` | Exit code 0 (skip if no tests) |
| Correct branch | `git branch --show-current` | On feature branch, not main/master |

```
IF any check fails:
  1. Warn user with details
  2. Ask: "Proceed anyway? [yes/no]"
  3. If no → abort
  4. If yes → continue with caution note
```

> [!CRITICAL]
> Do NOT skip pre-flight for code modification tasks.
> Pre-flight may be skipped for read-only tasks (research, analysis).

---

### Phase 1: Task Decomposition

Analyze the user's request: `$ARGUMENTS`

1. Identify atomic units that can be executed independently
2. Determine dependencies between units
3. **Check parallel-dispatch skill**: Can any tasks run concurrently?
4. Create a task list using TodoWrite

---

### Phase 2: Parallel Dispatch Decision

Before dispatching, consult the `parallel-dispatch` skill:

```
Are tasks independent? ─┬─ YES ─► Will they edit same files? ─┬─ NO ─► PARALLEL
                        │                                      └─ YES ─► SEQUENTIAL
                        └─ NO ─► SEQUENTIAL
```

If PARALLEL: Dispatch multiple executors concurrently
If SEQUENTIAL: Dispatch one at a time

---

### Phase 3: Batch Execution

Execute tasks in batches of 3 (configurable):

```
BATCH_SIZE = 3

for each batch:
  1. Dispatch batch to executor(s)
  2. Verify all outputs
  3. Report batch results
  4. **PAUSE** - Ask user: "Continue? [yes/no/abort]"
  5. Wait for response
  6. If abort → stop
  7. If continue → next batch
```

> [!CRITICAL]
> DO NOT proceed past batch boundary without user acknowledgment.

---

### Phase 4: Dispatch

For each atomic task, dispatch to the `executor` subagent:

```
Task tool call:
  subagent_type: "technical-director:executor"
  description: "[3-5 word summary]"
  prompt: |
    Task: [Single atomic instruction]

    Input:
    [Structured data if needed]

    Success Criteria:
    - [Criterion 1]
    - [Criterion 2]
```

---

### Phase 5: Verify

After each executor response, invoke `verification` skill:

| Check | Action if Failed |
|-------|------------------|
| Schema compliance | Log deviation, retry with schema reminder |
| Understanding match | Refine task, retry |
| Confidence >= 0.7 | Flag for review or verify independently |
| Evidence supports output | Request additional evidence |

**Track fix attempts**: If 3+ fixes fail on same issue → invoke `systematic-debugging` skill

---

### Phase 6: Review (if code changes)

If tasks involved code changes, dispatch to `reviewer` agent:

```
Task tool call:
  subagent_type: "technical-director:reviewer"
  description: "Review [feature] implementation"
  prompt: |
    Review the following changes against requirements:

    Requirements:
    - [Original requirements]

    Files changed:
    - [List of files]
```

Remember: Stage 2 (code quality) is BLOCKED until Stage 1 (spec compliance) passes.

---

### Phase 7: Completion

After all tasks verified and reviewed:

1. Invoke `verification` skill one final time for overall result
2. Invoke `finishing` skill to present options:
   - Merge locally
   - Create PR
   - Keep as-is
   - Discard

---

## Batch Report Format

After each batch:

```
┌─────────────────────────────────────────────┐
│ Batch N/M Complete                          │
├─────────────────────────────────────────────┤
│ ✓ Task 1: [status]                          │
│ ✓ Task 2: [status]                          │
│ ✓ Task 3: [status]                          │
├─────────────────────────────────────────────┤
│ Remaining: [count] tasks                    │
│                                             │
│ Continue? [yes/no/abort]                    │
└─────────────────────────────────────────────┘
```

---

## Skill Chain Reference

| When | Invoke |
|------|--------|
| Before any "done" claim | `verification` skill |
| Multiple independent tasks | `parallel-dispatch` skill |
| 3+ failed fix attempts | `systematic-debugging` skill |
| Writing code | `tdd` skill |
| Need code review | `reviewer` agent |
| All tasks complete | `finishing` skill |

---

## Begin

Decompose and execute: `$ARGUMENTS`
