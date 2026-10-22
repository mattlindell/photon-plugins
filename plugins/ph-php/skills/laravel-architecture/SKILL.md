---
name: laravel-architecture
description: Laravel and Sage/Roots architecture decisions with tradeoffs. Use when planning a Laravel application's structure, designing Eloquent models and relationships, designing queues, jobs, events, or broadcasting, choosing a design or enterprise pattern such as repositories, CQRS, multi-tenancy, or event sourcing, setting a Laravel performance strategy, or deciding how Sage, Acorn, Bud, or Bedrock fit a WordPress project.
---

# Laravel Architecture

This skill decides structure and strategy, and ends at a decision with its
tradeoff. Code lives in `laravel-patterns`, `laravel-api-patterns`,
`sage-patterns`, and `database-patterns`.

## Establish the context

1. **Standalone Laravel, or Laravel inside WordPress through Sage and Acorn?** In
   Sage, WordPress owns routing, the `wp_` schema, auth, and the request
   lifecycle; Laravel contributes the container, Blade, and config. Most of this
   file assumes standalone Laravel. For Sage, read
   [references/sage-roots.md](references/sage-roots.md).
2. **Versions.** Read the Laravel and PHP constraints in `composer.json`, and
   recommend nothing they rule out.
3. **Existing conventions.** Follow the project's current structure unless
   changing it is the decision being made.
4. **The forces.** Data volume, read-to-write ratio, background work, real-time
   needs, and team size. Each decision below cites the force that drove it.

## Plan the application

Make the decisions in this order; each depends on the one before it.

1. **Structure.** Keep Laravel's default layout until the domain has several
   distinct areas with their own vocabulary or owners. Then group by domain
   (`app/Domain/Billing/...`) and keep framework glue (`Http`, `Console`) at the
   top level. Split into packages only after the boundaries stop moving.
2. **Schema and relationship graph.** See [Eloquent model design](#eloquent-model-design).
3. **API surface.** Version with a prefix (`/api/v1`) from the start when
   external consumers exist; an API used only by the app's own SPA can skip it.
4. **Background work.** Decide what leaves the request. See
   [references/queues-and-events.md](references/queues-and-events.md).
5. **Cache layers and invalidation.** See [Performance strategy](#performance-strategy).
6. **Deployment.** Zero-downtime deploys need migrations that the running
   release tolerates (expand, deploy, then contract). Restart queue workers after
   every deploy (`queue:restart`, or `horizon:terminate`); they keep the old code
   in memory.
7. **Record the decisions** as ADRs when the repo keeps them.

## Eloquent model design

| Decision | Rule |
| --- | --- |
| Polymorphic or dedicated relation | Use a dedicated foreign key when the parent types are few and fixed; it gives FK constraints and plain joins. Use `morphTo` when many unrelated parents share a child (comments, attachments, tags), and accept the lost FK integrity. Call `Relation::enforceMorphMap()` so the database stores aliases, not class names that a refactor breaks. |
| Mass assignment | Use `$fillable` on models that request input reaches. Use `$guarded = []` only when every write goes through `validated()` data. Turn on `Model::shouldBeStrict(! app()->isProduction())` either way. |
| Casts or accessors | Write a custom cast for a value object reused across models (money, address). Use an `Attribute` accessor for a one-off derived value. Cast status columns to enums. |
| Model events, observers, or domain events | Use model events or observers for invariants of that model's own persistence (slug, UUID). Dispatch domain events from the action for side effects that cross boundaries (mail, other aggregates). Query-builder `update()` and `delete()` skip model events, so an invariant enforced only there can be bypassed. |
| Soft or hard delete | Soft-delete when users need restore or an audit trail, or children must outlive the parent. It costs a `deleted_at` filter on every query, unique indexes that include `deleted_at`, and a separate real-delete path for data-erasure requests. Otherwise hard-delete and archive. |
| One table or several for subtypes | Laravel has no native single-table inheritance. Use one table with a `type` column and scoped subclasses when subtypes share most columns; use separate tables when their columns diverge. |
| One model or separate read models | Add read models (query classes, database views, projection tables) when read shapes differ sharply from the write model or reads dominate the load. Full CQRS is in [references/enterprise.md](references/enterprise.md). |

Query-level patterns (eager loading, scopes, chunking) are in `database-patterns`.

## Choose a design pattern

The default is an action class per write operation, called from controllers,
jobs, and commands alike. Add the others when their pressure is present.

| Pattern | Use when | Skip when |
| --- | --- | --- |
| Repository | Several data sources, a swappable store, or a domain layer that must not know Eloquent | It would wrap Eloquent one-to-one "for testability"; `RefreshDatabase` already makes Eloquent testable |
| Service class | Logic coordinates several models or external services and has more than one entry point | One action covers it |
| Pipeline | Ordered steps over one payload that get added or reordered (checkout, import normalization) | The steps are fixed; call them in sequence |
| Strategy | Behavior chosen at runtime from config or input (payment providers, exporters); bind with contextual binding or a manager class | There is one implementation |
| View composer | A partial needs the same data in many views | The data belongs to one page; pass it from the controller |
| Macro | A small, stateless helper on a framework class (`Collection`, `Str`, `Builder`) used app-wide | The logic has dependencies or state; static analysis cannot see macros without IDE helpers |

## Performance strategy

- **Indexes** come from the hot-path queries: every `WHERE` and `ORDER BY`
  column. In a composite index, put equality columns before range columns.
- **N+1 queries.** `Model::preventLazyLoading()` outside production turns them
  into exceptions.
- **Caching.** Cache tags work only on the Redis and Memcached drivers. Cache
  whole responses for anonymous GET pages; cache query results with
  `Cache::remember`; invalidate from model events or with a short TTL.
- **Build-time caches.** Run `php artisan optimize` during deploy. After
  `config:cache`, `env()` returns `null` outside config files, so read settings
  through `config()` only.
- **Octane.** Adopt it when bootstrap time dominates request latency and the app
  is safe for a long-running process: no request state in singletons, static
  properties, or package globals. Never under Sage or Acorn.
- **Read/write split.** Configure `read` and `write` hosts with
  `'sticky' => true`, so a request reads its own writes.
- **Connection pooling.** Past a few hundred PHP-FPM workers, put ProxySQL or
  PgBouncer (transaction mode) in front of the database.
- **Assets.** Ship Vite's hashed build output through a CDN with immutable
  caching.

## Deeper decisions

- [references/queues-and-events.md](references/queues-and-events.md) — job
  design, drivers, batching, Horizon, failure handling, events, and broadcasting.
- [references/enterprise.md](references/enterprise.md) — multi-tenancy, CQRS,
  DDD, microservices, multiple databases, sharding, and event sourcing.
- [references/sage-roots.md](references/sage-roots.md) — Sage, Acorn, Bud, and
  Bedrock.
