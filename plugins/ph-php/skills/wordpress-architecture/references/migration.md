# Migration

## Plan the transfer

Inventory both sides first: WordPress, PHP, and MySQL versions; plugins with
domain-locked license keys; URLs hardcoded in the theme; cron jobs; email
delivery; and server rules (`.htaccess` against Nginx config).

**Search-replace:**

- Use `wp search-replace 'https://old.example' 'https://new.example' --all-tables --precise --skip-columns=guid`.
  It handles serialized data. A raw SQL `REPLACE` or `sed` over a dump corrupts
  serialized string lengths.
- Run it with `--dry-run` first.
- Replace the JSON-escaped form too (`https:\/\/old.example`), which blocks and
  page builders store.
- Replace absolute filesystem paths when the server path changes.

**Media:** `rsync` the uploads directory. When moving uploads to object storage,
let the offload plugin rewrite attachment URLs.

## Zero-downtime host move

1. Lower the DNS TTL to 300 seconds at least one old-TTL period before cutover.
2. Copy files and database to the new host. Test it through a hosts-file
   override.
3. Provision the TLS certificate on the new host before cutover (DNS-01
   challenge, or the host's pre-provisioning), so HTTPS works at the switch.
4. Freeze content for the final sync. For a store, enable maintenance mode or
   carry over orders placed since the snapshot.
5. Run the final database sync and switch DNS.
6. Keep the old host running until the old TTL has expired and its traffic has
   drained. Watch the logs on both hosts.

**Large databases:** use `mysqldump --single-transaction --quick` (or
`wp db export`) for InnoDB without locking. Past a few gigabytes, use
`mydumper`/`myloader` for parallel dump and load.

## Platform changes

- **Into WordPress.** Map source content types to post types, taxonomies, and
  meta before writing the importer. Store each source ID in meta so redirects can
  look it up.
- **To headless.** Keep URL parity between the old theme and the new frontend;
  redirects move to the frontend or CDN. See [headless.md](headless.md).
- **Redirects.** Map one-to-one with 301s; a redirect of everything to the home
  page discards the old URLs' search equity. Serve bulk redirects (thousands) at
  the server or CDN rather than from a plugin's per-request database lookup.

## Version upgrades

- **PHP.** Scan themes and plugins with PHPCompatibilityWP (a PHP_CodeSniffer
  ruleset) for the target version. Check each plugin's tested-up-to PHP version.
  Run staging on the new version with `WP_DEBUG_LOG` on and read the
  deprecations.
- **WordPress major.** Upgrade a staging clone of production first. Check each
  plugin's tested-up-to version. Run `wp core update-db`, then test the editor,
  checkout, forms, and cron.
- **Rollback.** Snapshot the database and files immediately before. Core
  upgrades change the database, and downgrading the files does not undo that;
  roll back by restoring both together.
