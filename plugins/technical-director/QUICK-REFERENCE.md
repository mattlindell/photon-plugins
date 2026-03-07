# Technical Director Quick Reference

Single-page reference for the orchestration framework.

---

## Skill Triggers

| Trigger | Skill | Why |
|---------|-------|-----|
| About to claim "done" | `verification` | Evidence before claims |
| Multiple independent tasks | `parallel-dispatch` | Decide concurrency |
| 3+ failed fixes | `systematic-debugging` | Stop guessing, find root cause |
| Writing code | `tdd` | Test first, always |
| Creating implementation plan | `writing-plans` | Exact code, not descriptions |
| Entering unfamiliar codebase | `context-gathering` | Understand before acting |
| All tasks complete | `finishing` | Present options, enforce test gate |

---

## Confidence Thresholds

| Range | Action | Meaning |
|-------|--------|---------|
| **< 0.5** | REJECT | Guessing, insufficient info |
| **0.5-0.7** | FLAG | Uncertain, verify manually |
| **>= 0.7** | ACCEPT | Reasonable confidence (subject to other checks) |

### Confidence Calibration

| Score | Use When |
|-------|----------|
| 0.95-1.0 | Verified from authoritative source, no ambiguity |
| 0.8-0.95 | High confidence, single reliable source |
| 0.7-0.8 | Reasonable confidence, some inference |
| 0.5-0.7 | Uncertain, multiple interpretations |
| < 0.5 | Guessing, speculation |

---

## Executor Schema

Required fields in every executor response:

```yaml
understood: |     # Task restatement
approach: |       # How you will execute
observations: |   # Raw findings
blockers: null    # Or description of blockers
output: |         # The result
confidence: 0.0   # Float 0-1
evidence:
  - [sources]
```

---

## Reviewer Stages

```
Stage 1: Spec Compliance
   ↓ (MUST PASS)
Stage 2: Code Quality
```

> [!CRITICAL]
> Stage 2 is BLOCKED until Stage 1 passes.

---

## Batch Execution

```
BATCH_SIZE = 3

for each batch:
  1. Execute
  2. Verify
  3. Report
  4. PAUSE - User confirms
  5. Continue or abort
```

---

## Deviation Logging

When something goes wrong:

```yaml
- id: [auto]
  timestamp: [ISO 8601]
  expected: [what should happen]
  actual: [what did happen]
  root_cause: misinterpretation | schema_violation | unsupported_claim | blocked | low_confidence | timeout
  fix: |
    [Concrete change to prevent recurrence]
```

Location: `.claude/plugins/technical-director/deviations/log.yaml`

---

## Key Assertions

- [ ] Evidence before claims
- [ ] Test before code
- [ ] Verify before complete
- [ ] Investigate before fix (after 3 failures)
- [ ] Understand before act
- [ ] Schema compliance on every response

---

## Forbidden Language

Never use in completion claims:

```
"should work", "probably", "seems to", "I believe",
"I think", "Great!", "Done!", "Perfect!"
```

---

## Parallel Dispatch Decision

```
Independent tasks? ─┬─ YES ─► Same files? ─┬─ NO ─► PARALLEL
                    │                       └─ YES ─► SEQUENTIAL
                    └─ NO ─► SEQUENTIAL
```

---

## Pre-Flight Checklist

Before code modifications:

| Check | Command |
|-------|---------|
| Git clean | `git status` |
| Tests pass | `[test command]` |
| Correct branch | `git branch --show-current` |

---

## Timeout Escalation

| Time | Action |
|------|--------|
| 2 min | Log warning |
| 5 min | Flag as stuck |
| 10 min | Escalate to user |

---

## Finishing Options

After all tasks complete (tests must pass first):

1. **Merge locally** - Merge to base, delete branch
2. **Create PR** - Push and open PR
3. **Keep as-is** - No action, branch remains
4. **Discard** - Delete work (requires confirmation)

---

## TDD Cycle

```
RED    → Write failing test → Watch it fail
GREEN  → Implement minimum → Watch it pass
REFACTOR → Clean code → All tests pass
```

---

## 5-Step Verification

Before any completion claim:

1. **IDENTIFY**: What command proves the claim?
2. **RUN**: Execute fresh (not cached)
3. **READ**: Examine complete output
4. **VERIFY**: Binary decision (YES/NO)
5. **CLAIM**: Make claim WITH evidence

---

## Core Principles

1. You are the only decision-maker
2. Atomic tasks only
3. Structured contracts
4. Full observability
5. Verification separate from execution
6. Evidence before claims
7. Schema as enforcement
8. Batch execution with checkpoints
9. Closed-loop improvement
10. Tests as completion gate
