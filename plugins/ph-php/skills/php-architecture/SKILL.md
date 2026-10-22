---
name: php-architecture
description: Framework-agnostic PHP architecture and quality decisions. Use when setting type or static-analysis policy, choosing an architecture or design pattern for plain PHP or Symfony code, tuning PHP runtime performance (OPcache, preloading, JIT), choosing an async or long-running runtime such as ReactPHP, Swoole, or Fibers, or defining the quality gate for a PHP codebase.
---

# PHP Architecture

This skill covers decisions that hold for any PHP codebase. WordPress decisions
go to `wordpress-architecture`, Laravel and Sage decisions to
`laravel-architecture`, and CodeIgniter 3 work to `legacy-ci3-maintenance`.

## Orient before advising

1. **Read `composer.json`.** The `require.php` constraint sets which language
   features exist; recommend nothing above it. Note the framework, the autoload
   map, and which tools are already installed (PHPStan or Psalm, PHP_CodeSniffer
   or PHP-CS-Fixer, Rector, PHPUnit or Pest).
2. **Read the static-analysis config and baseline.** The current level and the
   baseline size are the starting point for any type-policy change.
3. **Assess the codebase:**
   - Type coverage: the highest static-analysis level that passes.
   - Dependency health: `composer audit` and `composer outdated`.
   - Layout: PSR-4 namespaces and where the domain logic lives.
   - Debt: files with both high churn and high complexity.

## Type-system policy

- **`declare(strict_types=1)` in every new file.** In legacy code, adding it
  turns scalar coercion into a `TypeError` for calls made *from* that file. Add
  it one file at a time, with tests around each file, never by bulk replace.
- **Native types on every parameter, return, and property.** Use PHPDoc only for
  what native types cannot say: generics (`@template`), `list<T>`, array shapes
  (`array{id: int, name: string}`), `int<0, max>`, `non-empty-string`, and
  `class-string<T>`.
- **`mixed` only at boundaries** (decoded JSON, framework callbacks), narrowed
  right away by parsing into a typed object or asserting.
- **`never`** for functions that always throw or exit.
- **Variance.** Subclass return types may narrow and parameter types may widen.
  Give interface parameters the widest type the contract allows, so
  implementations are not forced to break it.
- **Static-analysis level.** Start new projects at PHPStan's maximum level (10
  in PHPStan 2, 9 in PHPStan 1) or Psalm level 1. On an existing codebase, pick
  the highest level whose error count you can work down, generate a baseline,
  fail CI when the baseline grows, and raise the level one step at a time. Add
  the framework extension: Larastan, `szepeviktor/phpstan-wordpress`, or
  `phpstan/phpstan-symfony`.

## Choose an architecture pattern

The default is plain service classes with constructor injection, under PSR-4
autoloading. Add a pattern when its pressure is present.

| Pattern | Pressure that justifies it | Cost |
| --- | --- | --- |
| Value objects | Any primitive that carries rules (email, money, identifiers) | Small; use them freely as `readonly` classes |
| Domain-driven design (aggregates, domain events) | Many business rules and invariants, and domain experts with their own vocabulary | More classes and a mapping layer |
| Repository interface | The domain must not depend on the persistence library, or there are several stores | An indirection on every data access |
| Service layer | Logic spans several entities and is called from several entry points (HTTP, CLI, queue) | An extra layer for simple CRUD |
| CQRS | Read and write shapes diverge, or reads need to scale separately | Two models to keep consistent |
| Event sourcing | Audit history or as-of-time state is a requirement | Event schemas versioned forever |
| Hexagonal (ports and adapters) | The domain must outlive the framework, or serve several delivery mechanisms | An adapter for every external dependency |

- **Dependency injection** is constructor injection through an autowiring
  container (Symfony DI, PHP-DI, League Container). Domain code never pulls
  from a service locator.
- **SOLID** is a review lens for classes that change often, not a reason to
  split a stable class.

## Build order

1. Domain models and value objects.
2. Service interfaces, only where a second implementation or a test seam exists;
   otherwise a concrete class.
3. Implementations.
4. Repositories behind their interfaces, when that pattern was chosen.
5. Validation at the boundaries (HTTP request, CLI input, queue payload) that
   parses input into typed objects. Code past the boundary trusts the types.
6. Event handlers for side effects.

## Runtime performance

Profile first (Xdebug profiler, Blackfire, Tideways, or SPX), and change one
setting at a time against the measurement.

- **OPcache** in production: `opcache.enable=1`; `memory_consumption` of 128–256
  MB; `max_accelerated_files` above the project's PHP file count, `vendor`
  included; `interned_strings_buffer` of 16–32. Set `validate_timestamps=0` and
  reload PHP-FPM on every deploy. Check `opcache_get_status()` for full memory and
  restarts.
- **Preloading** (`opcache.preload`) gains a few percent on framework-heavy apps.
  Preloaded code changes only on an FPM restart, and the script runs as
  `opcache.preload_user`. Adopt it only when measurement shows the gain; skip it
  on shared FPM pools.
- **JIT** helps CPU-bound code (math, image processing, parsers). Typical web
  requests are I/O-bound and gain little. Turn it on only when the profiler shows
  CPU-bound hot loops, and check the target PHP version's JIT defaults.
- **Autoloader** optimization is in `composer-dependency-management` (§11).
- **Caching.** APCu for hot data shared by the processes of one server; it is not
  shared across servers and clears on FPM restart. Redis for cache and locks
  shared across servers.
- **Memory.** Iterate large datasets with generators instead of building arrays.
  Defer expensive, rarely used services with lazy initialization (native lazy
  objects from PHP 8.4).

## Async and long-running PHP

Fibers are a primitive for libraries (Revolt, AMPHP 3, ReactPHP's async
package), not something to hand-roll in application code.

| Need | Choose |
| --- | --- |
| Concurrent HTTP calls inside one request or script | Guzzle pools or Symfony HttpClient's concurrent requests |
| A long-running event-loop service (WebSocket server, message consumer) | ReactPHP or AMPHP; pure PHP, no extension |
| A persistent app server in place of PHP-FPM | FrankenPHP worker mode or RoadRunner; Swoole or OpenSwoole when you want coroutines that hook PDO and curl. In Laravel, this is Octane. |
| Parallel CPU work | Separate processes (queue workers, `symfony/process`), or `ext-parallel` on a ZTS build |

Rules for long-running PHP:

- Keep no request state in static properties or singletons; reset state per
  request or message.
- Bound memory: restart workers after N jobs or M megabytes.
- Reconnect to the database on "server has gone away".
- A blocking call (PDO, `file_get_contents`) stalls the whole event loop unless
  the runtime hooks it, as Swoole does. Use async clients inside a loop.
- Serve WebSockets and long polling from an event-loop server or a managed
  service (Pusher, Ably, Mercure). Under PHP-FPM, each open connection holds a
  worker.
- Stream large files (`fopen`, `stream_copy_to_stream`, generators) instead of
  reading them whole.

## Quality gate

PHP work is done when every box holds:

- [ ] Static analysis passes at the project's level with no new baseline entries.
- [ ] The coding-standard check passes: PER Coding Style, which supersedes PSR-12,
      through PHP_CodeSniffer or PHP-CS-Fixer.
- [ ] Every new parameter, return, and property has a native type.
- [ ] `composer audit` is clean, or each advisory is triaged.
- [ ] Tests pass (`php-testing-patterns`).
- [ ] A changed hot path was profiled before and after.
