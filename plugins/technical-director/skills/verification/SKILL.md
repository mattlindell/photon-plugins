---
name: verification
description: This skill MUST be invoked before any completion claim, success report, or task transition. Mandates 5-step evidence protocol. Use when about to claim "done", "complete", "working", "fixed", or any success state.
---

# Verification Skill

> **Core Principle**: Evidence before claims, always.

## The 5-Step Mandate

Before ANY completion claim, execute these steps in order:

### 1. IDENTIFY
What command, check, or test proves the claim?
- Be specific: exact command, exact file, exact assertion
- "It should work" is NOT identification

### 2. RUN
Execute the verification fresh.
- Do NOT rely on cached results
- Do NOT rely on memory of previous runs
- Do NOT skip because "I just ran it"

### 3. READ
Examine the complete output.
- Check exit code (0 = success)
- Count results (how many passed/failed?)
- Read error messages fully

### 4. VERIFY
Binary decision: Does the output confirm the claim?
- YES → Proceed to step 5
- NO → Stop. Do not claim completion.

### 5. CLAIM
Only now, make the claim WITH evidence attached.
```
Claim: [what you're claiming]
Evidence: [command run] → [output received]
```

---

## Disqualifying Language

These phrases BLOCK completion claims. If you catch yourself using them, STOP and run verification:

| Phrase | Why It's Blocked |
|--------|------------------|
| "should work" | Uncertainty = unverified |
| "probably" | Uncertainty = unverified |
| "seems to" | Uncertainty = unverified |
| "I believe" | Belief ≠ evidence |
| "I think" | Thought ≠ evidence |
| "Great!" | Celebration before verification |
| "Done!" | Claim before evidence |
| "Perfect!" | Superlative before verification |

---

## What Verification Looks Like

### Good Verification
```
Claim: Tests pass

Evidence:
$ npm test
✓ 47 tests passed
Exit code: 0
```

### Bad "Verification"
```
Tests should pass now since I fixed the bug.
```

---

## Integration with Deviation Log

Unverified claims are logged as deviations:

```yaml
- id: [auto]
  timestamp: [now]
  expected: "Verification before completion claim"
  actual: "Claim made without evidence"
  root_cause: premature_completion
  fix: |
    Enforce verification skill invocation.
    Add reminder to session-start hook.
```

---

## When This Skill Applies

- Before saying "done", "complete", "finished", "working"
- Before committing code
- Before creating PRs
- Before marking tasks complete
- Before reporting success to user
- Before transitioning to next task

> [!CRITICAL]
> IF YOU ARE ABOUT TO CLAIM SUCCESS, YOU MUST VERIFY FIRST.

---

## Verification Assertions

Before any completion claim, these assertions must be TRUE:

```yaml
assertions:
  - name: command_executed
    check: "verification command was run (not remembered)"
    fail_action: "Run the command now"

  - name: output_read
    check: "full output examined (not truncated)"
    fail_action: "Read complete output"

  - name: exit_code_checked
    check: "exit code is 0 (or expected non-zero)"
    fail_action: "Check exit code"

  - name: binary_verdict
    check: "verdict is YES or NO (not 'probably')"
    fail_action: "Make binary decision"

  - name: evidence_attached
    check: "claim includes [command] → [output]"
    fail_action: "Attach evidence to claim"
```

### Assertion Checklist

Before claiming completion, verify each assertion:

| # | Assertion | Check | Pass? |
|---|-----------|-------|-------|
| 1 | `command_executed` | Did I run the command THIS session? | ☐ |
| 2 | `output_read` | Did I read the FULL output? | ☐ |
| 3 | `exit_code_checked` | Is exit code 0 (or expected)? | ☐ |
| 4 | `binary_verdict` | Is my answer YES or NO (not "maybe")? | ☐ |
| 5 | `evidence_attached` | Does my claim include [command] → [output]? | ☐ |

> [!CRITICAL]
> IF ANY assertion fails → STOP. Do not claim completion.

### Why Assertions > Prose Rules

| Prose Rule | Assertion |
|------------|-----------|
| "Make sure to run the command" | `command_executed: TRUE` |
| "Read the output carefully" | `output_read: TRUE` |
| "Check if it worked" | `binary_verdict: YES or NO` |

Assertions are:
- **Testable** - Can be verified mechanically
- **Binary** - TRUE or FALSE, no interpretation
- **Actionable** - Each has a `fail_action`

Prose rules require interpretation. Assertions require compliance.
