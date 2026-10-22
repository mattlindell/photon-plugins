# Enterprise patterns

Each pattern here pays for itself only under a specific pressure. Name the
pressure before you adopt the pattern; without one, the default is a modular
monolith on one database.

## Multi-tenancy

| Model | Choose when | Cost |
| --- | --- | --- |
| One database, `tenant_id` column with a global scope | Many small tenants on a shared schema | One missed scope leaks data across tenants. Enforce with the scope plus tests that query as a second tenant; Postgres row-level security adds a database-level guard. |
| One database per tenant | Contractual isolation, per-tenant backup and restore, or noisy tenants | Migrations run once per tenant, connections switch per request, and cross-tenant reporting needs its own store |

`stancl/tenancy` supports both models; `spatie/laravel-multitenancy` is lighter.

Resolve the tenant once, in middleware, from the domain, subdomain, path, or API
token, and hold it in a scoped singleton. Queued jobs must carry the tenant ID
and restore the tenant context before running.

## CQRS

Separate command and query models when read shapes diverge from the write model
or reads need to scale on their own. Start light: commands as action classes,
queries as query classes or database views. Add a separate read store with
projections only when that is not enough, and design the UI for the eventual
consistency it brings.

## Domain-driven design

Use it when the domain has many rules and invariants, not for CRUD.

- Give each bounded context its own top-level namespace and its own models.
- Cross contexts through events or explicit service interfaces, never through
  Eloquent relations between contexts.
- Load and save an aggregate through its root only; change its children through
  the root.

## Microservices

Start as a modular monolith. Extract a service when a module has a different
scaling profile, release cadence, or owning team, and its boundary has been
stable for a while.

- Each service owns its data; services never share a database.
- Propagate changes with asynchronous events. Use synchronous HTTP only for
  queries that need fresh data, with timeouts and a circuit breaker.
- Put external auth and routing in an API gateway.

## Multiple databases

Set `$connection` per model. Relations across connections load lazily or
eagerly, but cannot join. Transactions do not span connections; use an outbox or
a saga with compensating actions.

## Read/write splitting

Configure `read` and `write` hosts with `sticky` on. Sticky covers only the
request that wrote. Reads that must see a write from an earlier request (the
page after a POST redirect) use `onWriteConnection()`.

## Sharding

Shard last, after indexes, caching, read replicas, archiving, and vertical
scaling. The shard key is usually the tenant. Serve cross-shard queries from an
analytics store, not by fanning out at request time.

## Event sourcing

Adopt it when a full history of state changes is a requirement, when you need
state as of a past time, or when many projections read one stream.

- **Costs:** event schemas are versioned forever (upcasters), projections take
  time to rebuild, and reads are eventually consistent.
- **Snapshots** once aggregates pass a few hundred events.
- **Rebuild** a projection by replaying into a new table and swapping it in.

`spatie/laravel-event-sourcing` is the usual package.
