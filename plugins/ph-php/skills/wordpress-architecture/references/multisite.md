# Multisite

## Multisite or separate installs

Choose **multisite** when the sites share a codebase, a plugin and theme set, a
user base, and an admin team, and they update in lockstep.

Choose **separate installs** when any of these holds:

- Sites need different plugins or PHP versions.
- Sites have different owners or clients.
- Sites release on independent schedules.
- Failure or security isolation matters. One bad plugin update or one
  compromised plugin reaches every site in a network.
- A site may be sold or split off later.

Check the host and the critical plugins for multisite support before you commit;
some do not support it.

## Network type

| Type | Choose when | Requirements |
| --- | --- | --- |
| Subdirectory | Sites belong under one brand and domain | One certificate. WordPress refuses subdirectory mode on an install older than a month, because existing permalinks can collide. |
| Subdomain | Sites need their own hostnames under one domain | Wildcard DNS and a wildcard certificate |
| Domain-mapped | Sites need unrelated domains | Native since WordPress 4.5: set the site URL to the domain. Each domain needs DNS and a certificate. Leave `COOKIE_DOMAIN` undefined; a fixed value breaks login on mapped domains. |

## Plugins and themes

- Network-activate only what every site needs.
- Put policy that site admins must not disable (security, cache configuration)
  in must-use plugins.
- Let site admins activate plugins from the installed set; keep installation
  with super admins.

## Users and roles

Users are network-wide (one `wp_users` table); roles are per site. Grant super
admin sparingly, because it reaches every site. Login cookies are per domain, so
single sign-on across mapped domains needs a cross-domain auth solution.

## Scaling a network

- Each site adds its own set of about ten tables. At thousands of sites, the
  table count strains MySQL (`table_open_cache`, backup time). Shard by blog ID
  across database servers with LudicrousDB.
- Use a persistent object cache. WordPress keys cache entries per blog, except
  for global groups.
- `switch_to_blog()` swaps cache groups and globals on every call. Use it for a
  handful of sites; for bulk content syndication, push through the REST API or a
  distributor plugin (Distributor) instead of looping over the network.

## Split or merge

- **Split a site out:** export its `wp_N_*` tables and its users' rows from
  `wp_users` and `wp_usermeta`, rename the table prefix, move
  `uploads/sites/N` to `uploads`, and run a serialized-safe search-replace on the
  URLs (see [migration.md](migration.md)).
- **Merge sites in:** import at the database level with a prefix rewrite. A WXR
  export and import drops data that plugins keep outside posts.
