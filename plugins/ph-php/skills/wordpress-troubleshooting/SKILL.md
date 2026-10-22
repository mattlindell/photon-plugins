---
name: wordpress-troubleshooting
description: Diagnostic procedure for a broken WordPress site. Use when a site shows a white screen, a 500, 403, or 404, or a database connection error, runs out of memory, breaks after a plugin or theme change, misses scheduled cron events, or has failing or slow admin-ajax requests.
---

# WordPress Troubleshooting

The work is done when you can name the root cause and show the evidence for it:
a log line, a reproduction, or a toggle that turns the symptom on and off. A
symptom that went away on its own is not a diagnosis.

## Diagnose a broken WordPress site

### 1. Capture the evidence

Reproduce the failure and record the exact URL, the user role, and the time.
Then turn on logging without showing errors to visitors:

```php
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', '/var/log/wordpress/debug.log' ); // a path outside the web root
define( 'WP_DEBUG_DISPLAY', false );
```

`WP_DEBUG_LOG` set to `true` writes `wp-content/debug.log`, which the web server
can serve to anyone. Give it a path outside the document root (supported since
WordPress 5.1).

Also read:

- **The PHP-FPM and web server error logs.** A fatal error that happens before
  WordPress loads never reaches `debug.log`.
- **The admin mailbox.** Since 5.2, a fatal error in a plugin or theme sends the
  admin a recovery-mode link that names the extension.
- **Query Monitor**, for queries, hooks, and HTTP API calls on the failing
  request. Set `SAVEQUERIES` on staging only; it holds every query in memory.

### 2. Branch on the symptom

#### White screen or 500

1. Read the fatal error in the log. Its file path names the plugin or theme, and
   most white screens end here.
2. No fatal error: look in the PHP-FPM log for `Allowed memory size exhausted`
   (go to [Memory exhaustion](#memory-exhaustion)) or `max_execution_time`.
3. Still nothing: deactivate everything from the CLI, which works when
   wp-admin does not:
   `wp plugin deactivate --all --skip-plugins --skip-themes`, then
   `wp theme activate twentytwentyfive --skip-themes`. If the site recovers,
   isolate the cause with [Plugin or theme conflict](#plugin-or-theme-conflict).
4. If the failure started with a PHP version change, check the code against the
   new version (see `wordpress-architecture` →
   [migration.md](../wordpress-architecture/references/migration.md#version-upgrades)).

#### 403 or 404

- **404 on every post while the home page works:** the rewrite rules. Run
  `wp rewrite flush`. On Apache, confirm `mod_rewrite` is on and `.htaccess` is
  writable and allowed (`AllowOverride`). On Nginx, confirm
  `try_files $uri $uri/ /index.php?$args;`.
- **404 on a custom post type only:** rewrite rules were not flushed after the
  type was registered. Flush on plugin activation, never on every `init`.
- **403 from the server:** check the WAF first (ModSecurity, Cloudflare, a
  security plugin) and its logs, then file permissions (directories 755, files
  644).
- **403 inside WordPress** ("Sorry, you are not allowed…"): a capability check.
  Compare the user's capabilities (`wp user list-caps <user>`) with the one the
  code checks.
- **403 `rest_cookie_invalid_nonce` from the REST API:** the request is missing
  the `X-WP-Nonce` header.

#### Database connection error

Check in this order:

1. The credentials and `DB_HOST` in `wp-config.php`, including a port or socket.
2. Whether the web server reaches the database: `wp db check`.
3. Whether MySQL is running.
4. Whether connections are exhausted: compare `SHOW STATUS LIKE 'Threads_connected'`
   with `max_connections`.
5. "One or more database tables are unavailable": run `wp db repair`.

#### Memory exhaustion

Three limits interact:

| Setting | Applies to | Default |
| --- | --- | --- |
| `WP_MEMORY_LIMIT` | Frontend requests | 40M (64M on multisite) |
| `WP_MAX_MEMORY_LIMIT` | Admin requests | 256M |
| `memory_limit` in `php.ini` | Everything | Host-defined |

WordPress raises the PHP limit to its own setting but never lowers it, and it
cannot raise it at all when the host disables `ini_set`.

Raising the limit is a stopgap. Find the consumer:

- The fatal error's file is where an allocation failed, not necessarily what
  used the memory. Compare peak memory in Query Monitor with plugins on and off.
- Look for unbounded queries: `posts_per_page => -1`, `get_posts()` without a
  limit, or loading every user.
- **Long-running processes** (WP-CLI, cron, imports) grow memory on every
  iteration through the runtime object cache and the query log. Process in
  batches, call `wp_cache_flush_runtime()` between batches, and keep
  `SAVEQUERIES` off.
- **A full persistent object cache**: with `maxmemory-policy noeviction`, Redis
  rejects writes once full. Use `allkeys-lru` for a cache-only Redis.

#### Plugin or theme conflict

1. **Bisect the plugins.** Deactivate half, test, keep the half that still
   reproduces, and repeat; n plugins take about log₂(n) rounds. On production,
   use the Health Check & Troubleshooting plugin, which disables plugins for your
   session only.
2. **Rule out the theme** by switching to a default theme.
3. With the conflicting pair found, identify the mechanism:
   - **Hook priority:** list the callbacks on the hook (Query Monitor's Hooks &
     Actions panel) and check which one runs last and overwrites the other.
   - **JavaScript:** read the browser console, and look for a library loaded
     twice in different versions or a missing script dependency.
   - **Database locks:** run `SHOW PROCESSLIST` while the slowdown happens and
     look for threads waiting on a lock.

#### Cron

WP-Cron runs on page loads. Low-traffic sites miss schedules, fully page-cached
sites may never trigger it, and busy sites trigger it too often. Switch to system
cron when any of those applies, or when tasks must run on time:

```php
define( 'DISABLE_WP_CRON', true );
```

Then run `wp cron event run --due-now` from system cron every one to five
minutes.

To diagnose:

- `wp cron event list` shows overdue events. `wp cron test` checks that
  WP-Cron can spawn.
- A failed loopback request stops WP-Cron. Site Health reports loopback
  failures; HTTP basic auth on staging is a common cause.
- **Duplicate events:** code that schedules on every page load without a
  `wp_next_scheduled()` guard fills the autoloaded `cron` option. Check its size.
- **Long tasks** run inside a web request's `max_execution_time`. Split them into
  batches with Action Scheduler.

#### AJAX

- **Volume:** `admin-ajax.php` boots the admin and is never page-cached. Find
  which `action` values dominate in the access log or the browser's network tab,
  and move frontend reads to cacheable REST endpoints.
- **Heartbeat:** it polls every 15 seconds in the post editor. Slow it or turn it
  off on the frontend with the `heartbeat_settings` filter; keep it in the editor,
  where autosave and post locking depend on it.
- **Response `0`:** no handler for that action. A logged-out request needs a
  `wp_ajax_nopriv_{action}` hook as well as `wp_ajax_{action}`.
- **Response `-1`:** the nonce check failed. A page cached longer than the nonce
  lifetime (12 to 24 hours) serves expired nonces.
- **Response `400`:** the request has no `action` parameter.

#### Slow site

Profile it instead of guessing: follow `wordpress-architecture` →
[performance.md](../wordpress-architecture/references/performance.md#profile-before-optimizing).

### 3. Fix and confirm

Fix the root cause, then run the original reproduction and confirm it passes.
Restore production settings afterward: logging back to its normal path, and
`SAVEQUERIES` off.
