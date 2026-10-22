# Queues and events

Job and listener code is in `laravel-patterns` (Patterns 6 and 7). Faking queues
and events in tests is in `php-testing-patterns` (Pattern 15).

## Queues

**Job design:**

- **Idempotent.** Running a job twice leaves the same result. Check state before
  acting and use unique keys. `ShouldBeUnique` deduplicates at dispatch;
  `WithoutOverlapping` middleware prevents concurrent runs.
- **Atomic.** One unit of work per job. Fan large work out as a batch instead of
  one long job.
- **Small payload.** Pass IDs or models (`SerializesModels` refetches them), not
  large arrays. The refetched model reflects the database at run time, not at
  dispatch.
- **After commit.** Set `after_commit` on the connection, or call
  `->afterCommit()`, so a job never runs before its transaction commits and finds
  rows missing.

**Driver:**

| Driver | Choose when |
| --- | --- |
| Redis | Production default; Horizon requires it |
| Database | Low volume, no extra infrastructure |
| SQS | Serverless (Vapor) or managed durability. Payloads cap at 256 KB and delays at 15 minutes. |
| Sync | Local and tests only |

**Batches and chains.** Use `Bus::batch` for independent jobs that run in
parallel and need progress and `then`/`catch`/`finally` callbacks. Use
`Bus::chain` when each job depends on the previous one; one failure stops the
chain.

**Rate limits.** Wrap calls to external APIs in `RateLimited` middleware with a
named limiter, and use `ThrottlesExceptions` for flaky upstreams. Release the
job with a backoff instead of failing it.

**Horizon:**

- Run separate supervisors per workload class (default, notifications,
  long-running imports), so slow jobs cannot starve fast ones.
- The connection's `retry_after` must exceed the longest job `timeout`, or a
  still-running job is released and runs twice.
- Use `balance => auto` and set `waits` thresholds per queue.

**Failure handling.** Set `$tries` and an exponential `$backoff` array, or
`retryUntil()` for time-bound work. Put compensation and alerting in `failed()`.
The `failed_jobs` table is the dead-letter queue: alert on its growth and prune
it with `queue:prune-failed`.

**Monitoring.** Track throughput, runtime per job class, and wait time per queue.
Alert on wait time as well as failures; a queue can be healthy and hours behind.

## Events and broadcasting

**Event or job.** Dispatch a job when there is one known piece of work. Fire an
event when the producer should not know its consumers: several listeners, or
listeners in other modules. An event with one listener is indirection.

**Listeners:**

- Run a listener synchronously when it must succeed or fail with the request,
  inside the same transaction.
- Queue it (`ShouldQueue`) for side effects: mail, webhooks, external sync. Add
  `ShouldHandleEventsAfterCommit` when the event fires inside a transaction.
- Listener order is not a contract. When order matters, use a pipeline or a job
  chain.

**Channels.** Public channels for non-sensitive data. Private channels for
per-user or per-resource data, authorized in `routes/channels.php`. Presence
channels when the UI shows who is online. Name channels by resource
(`orders.{id}`).

**WebSocket server.** Reverb (first-party, self-hosted, Laravel 11+) is the
default for new apps. Choose Pusher or Ably for a managed service with no
operations. `beyondcode/laravel-websockets` is unmaintained; migrate off it.

**Real-time features.** Send notifications through both the `broadcast` and
`database` channels so offline users see them later. Broadcast minimal payloads
(IDs) and let the client refetch; full payloads leak data to the channel and
arrive out of order.

**Event sourcing** is in [enterprise.md](enterprise.md#event-sourcing).

**Testing.** Fake only the events under test (`Event::fake([OrderShipped::class])`)
so other listeners still run, and test listeners by calling `handle()` directly.
