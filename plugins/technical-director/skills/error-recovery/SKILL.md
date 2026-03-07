---
name: error-recovery
description: Use when tasks fail due to transient errors. Provides structured retry strategies and graceful degradation patterns. Invoke on network errors, rate limits, or intermittent failures.
---

# Error Recovery Skill

> **Core Principle**: Classify before retry.

## When to Invoke

- Network timeout or connection failure
- API rate limit exceeded
- Intermittent test failure
- External service unavailable
- Resource temporarily locked
- Any transient error condition

---

## Error Classification

First, classify the error type:

| Type | Description | Default Action |
|------|-------------|----------------|
| **Transient** | Temporary, likely to resolve | Retry with backoff |
| **Permanent** | Won't resolve on retry | Fail immediately |
| **Degradable** | Can proceed without | Graceful degradation |
| **Unknown** | Can't classify | Limited retry, then escalate |

### Transient Errors

```
- Network timeout
- Connection reset
- 429 Too Many Requests
- 503 Service Unavailable
- 504 Gateway Timeout
- Lock contention
- Temporary file access
```

### Permanent Errors

```
- 400 Bad Request (invalid input)
- 401 Unauthorized (wrong credentials)
- 403 Forbidden (permission denied)
- 404 Not Found (resource doesn't exist)
- Syntax error in code
- Invalid configuration
```

### Degradable Errors

```
- Optional dependency unavailable
- Non-critical API failure
- Caching service down
- Logging service failure
```

---

## Retry Strategies

### Strategy: Immediate Retry

For: Quick transient errors (network glitch)

```
Attempts: 1
Delay: 0
```

### Strategy: Linear Backoff

For: Rate limits with known cooldown

```
Attempts: 3
Delays: 1s, 2s, 3s
```

### Strategy: Exponential Backoff

For: Unknown transient errors

```
Attempts: 4
Delays: 1s, 2s, 4s, 8s
Max delay: 30s
```

### Strategy: Exponential with Jitter

For: Multiple concurrent requests

```
Attempts: 4
Delays: random(0.5x, 1.5x) * base
Base: 1s, 2s, 4s, 8s
```

---

## Recovery Protocol

### Step 1: Classify Error

```
1. Read full error message
2. Check error code/type
3. Classify as: transient | permanent | degradable | unknown
4. If permanent → fail immediately
5. If degradable → attempt graceful degradation
6. If transient/unknown → proceed to retry
```

### Step 2: Select Strategy

```
Rate limit (429) → Linear backoff
Network error → Exponential backoff
API error 5xx → Exponential with jitter
Unknown → Exponential with max 3 attempts
```

### Step 3: Execute Retry

```
for attempt in 1..max_attempts:
  try:
    execute_task()
    return success
  catch error:
    if is_permanent(error):
      return fail
    wait(delay_for_attempt)

return fail_with_all_attempts_exhausted
```

### Step 4: Handle Final Failure

```
After max attempts exhausted:
1. Log complete error history
2. Determine if degradable
3. If degradable → proceed without
4. If not → escalate to user
```

---

## Graceful Degradation

When non-critical components fail:

| Component | Degradation Strategy |
|-----------|---------------------|
| Caching | Proceed without cache |
| Logging | Log locally, continue |
| Analytics | Skip, don't block |
| Optional API | Use fallback/default |
| Non-critical validation | Warn, continue |

### Degradation Template

```yaml
degradation:
  failed_component: "[What failed]"
  impact: |
    [What functionality is affected]
  fallback_used: |
    [What alternative was used]
  warning_to_user: |
    [What user should know]
```

---

## Output Template

```yaml
error_recovery:
  timestamp: [ISO 8601]
  original_task: |
    [Task that failed]

  error:
    type: [transient | permanent | degradable | unknown]
    message: |
      [Error message]
    code: [error code if any]
    source: [where error occurred]

  classification_reasoning: |
    [Why you classified this way]

  strategy:
    name: [immediate | linear | exponential | exponential_jitter]
    max_attempts: [number]
    delays: [list of delays]

  attempts:
    - attempt: 1
      timestamp: [ISO 8601]
      result: fail
      error: "[error message]"
    - attempt: 2
      timestamp: [ISO 8601]
      result: success | fail
      error: "[error message if failed]"

  outcome: [recovered | degraded | failed | escalated]

  degradation:  # if applicable
    fallback_used: |
      [What fallback was used]
    functionality_lost: |
      [What's not available]

  next_action: |
    [What to do next]

  confidence: 0.0
  evidence:
    - "[Error logs examined]"
```

---

## Rules

> [!CRITICAL]
> ALWAYS classify before retry.
> NEVER retry permanent errors.
> ALWAYS cap retry attempts.

### Do
- Log all retry attempts
- Use appropriate backoff for error type
- Consider graceful degradation
- Escalate after max attempts

### Don't
- Retry indefinitely
- Retry permanent errors
- Ignore error messages
- Lose error context on retry

---

## User Escalation

When to escalate to user:

```
1. Max retry attempts exhausted
2. Permanent error encountered
3. Unknown error can't be classified
4. Degradation unacceptable for task
```

### Escalation Template

```
Error encountered: [type]

What happened:
[Description]

What I tried:
- Attempt 1: [result]
- Attempt 2: [result]

Options:
a) Retry with different approach
b) Skip this task, continue others
c) Abort entire operation
d) Provide alternative input
```

---

## Integration with Other Skills

| After Recovery | Invoke |
|----------------|--------|
| Root cause unclear | → `systematic-debugging` skill |
| Task recovered | → Continue with `orchestration` |
| Need to abort | → `finishing` skill |

### Chaining Rules

1. **IF** recovered **THEN** continue normal flow
2. **IF** 3+ tasks fail same error **THEN** invoke `systematic-debugging`
3. **IF** user chooses abort **THEN** invoke `finishing` skill
4. **ALWAYS** log recovery attempts in deviation log

---

## Deviation Logging

Log all recovery attempts:

```yaml
- id: [auto]
  timestamp: [now]
  expected: "Task completes successfully"
  actual: "Error: [type] - [message]"
  root_cause: transient_error | external_service | rate_limit | network
  recovery_attempted: true
  recovery_outcome: [recovered | degraded | failed]
  fix: |
    [If pattern emerges, note prevention strategy]
```

---

## Example

**Task fails with rate limit error:**

```yaml
error_recovery:
  timestamp: "2024-01-15T10:30:00Z"
  original_task: |
    Fetch user data from external API

  error:
    type: transient
    message: |
      HTTP 429: Too Many Requests
      Rate limit exceeded. Retry after 60 seconds.
    code: 429
    source: external_api.fetch_user()

  classification_reasoning: |
    429 is explicitly a rate limit error. The response includes
    a Retry-After header of 60 seconds. This is transient.

  strategy:
    name: linear
    max_attempts: 3
    delays: [60s, 60s, 60s]

  attempts:
    - attempt: 1
      timestamp: "2024-01-15T10:30:00Z"
      result: fail
      error: "429 Too Many Requests"
    - attempt: 2
      timestamp: "2024-01-15T10:31:00Z"
      result: success
      error: null

  outcome: recovered

  next_action: |
    Continue with original task flow

  confidence: 1.0
  evidence:
    - "HTTP response code 429"
    - "Retry-After: 60 header present"
    - "Second attempt succeeded after waiting"
```
