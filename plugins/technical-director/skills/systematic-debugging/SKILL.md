---
name: systematic-debugging
description: Invoke when debugging failures. MANDATORY when 3+ fix attempts have failed. Enforces root cause investigation before fixes.
---

# Systematic Debugging Skill

> **Core Principle**: No fixes without root cause investigation first.

## The 3+ Fix Rule

> [!CRITICAL]
> If you have attempted 3 or more fixes without success, STOP.
> This indicates an architectural problem, not an isolated bug.
> Escalate to user with analysis.

---

## Four Phases

### Phase 1: Investigate

Before attempting ANY fix:

| Action | Purpose |
|--------|---------|
| Read error messages completely | Errors tell you what's wrong |
| Reproduce the issue | Confirm you're fixing the right thing |
| Check recent changes | What changed before it broke? |
| Trace data flow | Follow the data from input to error |
| Gather diagnostic evidence | Logs, stack traces, state dumps |

**Output**: Clear statement of what's happening and where

### Phase 2: Analyze

Compare broken state to working state:

| Action | Purpose |
|--------|---------|
| Find working examples | What does correct behavior look like? |
| Compare differences | What's different between working and broken? |
| Check assumptions | What are you assuming that might be wrong? |
| Review dependencies | What does this code depend on? |

**Output**: List of differences between working and broken states

### Phase 3: Hypothesize

Form a specific, testable hypothesis:

| Good Hypothesis | Bad Hypothesis |
|-----------------|----------------|
| "The null check on line 42 doesn't handle undefined" | "Something's wrong with the data" |
| "The API returns 404 when ID contains spaces" | "The API is broken" |
| "State updates before render completes" | "It's a timing issue" |

**Test minimally**: Change ONE thing to test the hypothesis

**Output**: Specific hypothesis with test plan

### Phase 4: Implement

Only after phases 1-3:

1. Write failing test that demonstrates the bug
2. Implement single fix addressing root cause
3. Verify fix works
4. Verify no regressions (run full test suite)

**Output**: Fix with evidence it works

---

## Red Flags: Restart the Process

If you catch yourself doing any of these, STOP and restart from Phase 1:

| Red Flag | What's Wrong |
|----------|--------------|
| Guessing at fixes | Skipped investigation |
| "Let me try this..." | No hypothesis |
| Multiple changes at once | Can't isolate cause |
| "One more fix should do it" | Sunk cost fallacy |
| Pretending to understand | Incomplete analysis |

---

## The 3+ Fix Escalation

After 3 failed fix attempts:

```
┌─────────────────────────────────────────────┐
│ 3+ Fix Attempts Failed                       │
├─────────────────────────────────────────────┤
│ This pattern indicates:                      │
│ - Fundamental design problem                 │
│ - Missing understanding of the system        │
│ - Wrong level of abstraction                 │
│                                              │
│ Recommended actions:                         │
│ 1. Document what was tried                   │
│ 2. Describe current understanding            │
│ 3. Identify knowledge gaps                   │
│ 4. Escalate to user/architect                │
└─────────────────────────────────────────────┘
```

---

## Debugging Report Template

After investigation, report:

```yaml
issue:
  symptom: "[What the user sees]"
  location: "[File:line or component]"
  reproducibility: "[Always/Sometimes/Rarely]"

investigation:
  error_message: "[Exact error]"
  stack_trace: "[Relevant frames]"
  recent_changes: "[What changed]"
  data_state: "[Relevant data at failure point]"

analysis:
  working_comparison: "[What works vs what doesn't]"
  differences_found:
    - "[Difference 1]"
    - "[Difference 2]"
  assumptions_checked:
    - "[Assumption]: [Valid/Invalid]"

hypothesis:
  statement: "[Specific hypothesis]"
  test_plan: "[How to test]"
  test_result: "[What happened]"

fix:
  change: "[What was changed]"
  verification: "[How verified]"
  regression_check: "[Test results]"
```

---

## Integration with Orchestration

This skill is invoked when:
- `orchestration` detects 3+ failed fix attempts
- User explicitly requests debugging help
- `verification` skill repeatedly fails

Chain: `orchestration` → (3+ failures) → `systematic-debugging` → `executor`

---

## Deviation Logging

Skipped debugging logged:

```yaml
- id: [auto]
  timestamp: [now]
  expected: "Systematic debugging after 3+ failures"
  actual: "Continued attempting fixes without investigation"
  root_cause: skipped_debugging
  fix: |
    Enforce systematic-debugging skill after 3 failures.
    Add counter to orchestration skill.
```
