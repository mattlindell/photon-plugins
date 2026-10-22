# DevOps and deployment

## Local environments

Use one tool per team, with its config committed to the repo.

| Tool | Choose when |
| --- | --- |
| wp-env | Plugin or block development; matches the WordPress core test setup |
| DDEV | A team standard across projects, including Bedrock and Sage; matches production PHP and Nginx config |
| Lando | The team already uses it, or the host has a Lando recipe (Pantheon, Platform.sh) |
| Local | Designers and non-developers who need a GUI |

## Environments and data

Code moves up (local → staging → production). Data moves down (production →
staging → local). Pushing a database up overwrites production content.

When pulling production data down, scrub personal data (user emails, orders)
after the search-replace. Staging matches production in PHP version, object
cache, and page cache, or it does not test what production runs.

## Deployment

- **Deploy a build artifact from Git.** CI runs `composer install --no-dev` and
  the asset build, then ships the result. Not FTP, and not `git pull` with
  Composer on the production server.
- **Version control holds** themes, custom plugins, mu-plugins, and
  `composer.json` with third-party plugins as dependencies (WPackagist or
  Bedrock). Uploads and the database are not code.
- **Set `DISALLOW_FILE_MODS`** in production once deployments manage plugins,
  or admin-side updates drift from Git.
- **Make deploys atomic.** Build each release in its own directory, switch a
  symlink, and keep several previous releases for instant rollback. Share
  `uploads` and `.env` across releases.
- **Schema changes.** WordPress has no migration framework. Ship schema changes
  as versioned upgrade routines that compare a stored `db_version` option and
  run `dbDelta()` (code in `database-patterns` §10). Make them idempotent and
  backward compatible with the previous release (expand, deploy, then contract)
  so rollback stays safe.
- **Blue-green and canary** fit only containerized or load-balanced setups. Both
  colors share one database, so the same backward-compatibility rule applies.
- **After deploy:** purge the page cache and CDN, run `wp core update-db` after a
  core update, and flush the object cache only when cached structures changed.

## Hosting

| Option | Choose when | Gives up |
| --- | --- | --- |
| Managed WordPress (WP Engine, Kinsta, Pantheon, WordPress VIP) | The default for agency sites; caching, backups, staging, and patching are handled | Root access, some plugins, and PHP worker headroom |
| VPS | The site needs custom services (search, workers), or cost matters at scale, and the team can run patching and backups | Managed operations |
| Containers or Kubernetes | The organization already runs Kubernetes, or needs autoscaling or many instances | Simplicity; WordPress must be stateless first (see [scaling.md](scaling.md#horizontal-scaling)) |

## Load balancing and monitoring

- Point the load balancer health check at a lightweight script that checks
  database connectivity, not at the home page, which is cached or heavy.
- Monitor external uptime, APM response times, PHP error rate, the database
  slow-query log, and overdue cron events.
- Alert on error rate and p95 TTFB as well as uptime; a site can be up and
  failing.
