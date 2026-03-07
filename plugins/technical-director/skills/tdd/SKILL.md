---
name: tdd
description: Use for any code implementation task. Enforces RED-GREEN-REFACTOR cycle. "If you didn't watch it fail, you don't know if it tests the right thing."
---

# Test-Driven Development Skill

> **Core Principle**: If you didn't watch it fail, you don't know if it tests the right thing.

## The Cycle

```
    ┌──────────────────────────────────────────┐
    │                                          │
    ▼                                          │
┌───────┐    ┌───────┐    ┌──────────┐        │
│  RED  │ ──▶│ GREEN │ ──▶│ REFACTOR │ ───────┘
└───────┘    └───────┘    └──────────┘
Write test   Make pass    Clean up
Watch FAIL   Minimal code  Keep green
```

---

## RED Phase

### What to Do
1. Write a single failing test
2. Run the test
3. **Watch it fail**
4. Verify failure is for expected reason

### Why "Watch It Fail" Matters

| Without Watching Fail | With Watching Fail |
|-----------------------|-------------------|
| Test might always pass (bug in test) | Confirms test can fail |
| Test might fail for wrong reason | Confirms test checks right thing |
| No proof test validates behavior | Evidence of validation |

### Red Phase Checklist
- [ ] Test written for ONE behavior
- [ ] Test run
- [ ] Test failed
- [ ] Failure is for expected reason (not typo, import error, etc.)

---

## GREEN Phase

### What to Do
1. Write the **minimum** code to pass the test
2. Run the test
3. **Watch it pass**
4. Nothing more - no extras, no "while I'm here"

### What Minimum Means

| Too Much | Minimum |
|----------|---------|
| Add error handling for edge cases | Just make this test pass |
| Refactor related code | Just make this test pass |
| Add features "we'll need" | Just make this test pass |

### Green Phase Checklist
- [ ] Only code needed for this test written
- [ ] Test run
- [ ] Test passed
- [ ] No other tests broken

---

## REFACTOR Phase

### What to Do
1. Clean up the code
2. Run ALL tests after each change
3. Keep everything green
4. Stop when code is clean

### Safe Refactorings
- Rename for clarity
- Extract methods/functions
- Remove duplication
- Improve structure

### Refactor Phase Checklist
- [ ] Code is clean
- [ ] All tests still pass
- [ ] No new behavior added

---

## Non-Negotiable Rules

> [!CRITICAL]
> These are not guidelines. They are rules.

### Rule 1: Test First
```
Production code written BEFORE failing test → DELETE and restart
```

No exceptions. No "I'll write the test after." That's not TDD.

### Rule 2: Watch It Fail
```
Test not seen failing → Test not trusted
```

Running the test and seeing green immediately means something is wrong.

### Rule 3: Minimal Green
```
Code beyond minimum → Remove it
```

YAGNI (You Aren't Gonna Need It). Add it when a test requires it.

### Rule 4: Keep Tests Green
```
Refactoring breaks tests → Undo and retry smaller
```

Refactoring should never change behavior.

---

## Integration with Verification

TDD is a specialized form of the `verification` skill:

| Verification Step | TDD Equivalent |
|-------------------|----------------|
| IDENTIFY | Write the test |
| RUN | Execute the test |
| READ | Observe failure/pass |
| VERIFY | Expected behavior? |
| CLAIM | Only after green |

---

## Integration with Writing-Plans

Plans should include TDD structure:

```markdown
## Task N: [Name]

1. Write failing test:
   ```typescript
   [complete test code]
   ```

2. Run test:
   ```bash
   [command]
   ```
   Expected: FAIL with "[message]"

3. Implement:
   ```typescript
   [complete implementation]
   ```

4. Run test:
   Expected: PASS
```

---

## Deviation Logging

Code without test logged:

```yaml
- id: [auto]
  timestamp: [now]
  expected: "Failing test written before implementation"
  actual: "Implementation written without test"
  root_cause: untested_code
  fix: |
    Enforce TDD skill for all code tasks.
    Add test-first check to orchestration.
```

---

## Common TDD Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Writing test after code | Can't verify test catches bugs | Delete code, write test first |
| Not watching test fail | Don't know if test works | Run test before implementation |
| Making multiple tests pass at once | Can't isolate failures | One test at a time |
| Refactoring while red | Changes behavior | Get green first |
| Testing implementation details | Brittle tests | Test behavior, not code |
