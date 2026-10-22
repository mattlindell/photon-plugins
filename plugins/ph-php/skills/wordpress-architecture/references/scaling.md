# Scaling and infrastructure

## Vertical scaling

Scale vertically first, in this order: page cache → object cache → PHP-FPM
tuning → a larger server → the database on its own server. Go horizontal when one
server stays CPU-bound after caching, when the site needs high availability, or
when spikes exceed what one server absorbs.

**PHP-FPM:**

- `pm.max_children` = memory available to PHP ÷ average worker RSS. Measure RSS
  under load; WordPress workers commonly run 40–100 MB, WooCommerce more.
- `pm = static` on a dedicated server with steady traffic, `dynamic` for mixed
  load, `ondemand` for many low-traffic pools on one server.
- Set `pm.max_requests` (around 500) to recycle workers that leak memory.

**MySQL or MariaDB:**

- On a dedicated database server, size `innodb_buffer_pool_size` to hold the
  working set, typically 70–80% of RAM.
- The query cache is removed in MySQL 8 and deprecated in MariaDB; use the object
  cache instead.
- `max_connections` must exceed the sum of `pm.max_children` across all
  application servers, plus headroom.

**OPcache** settings are in `php-architecture`. For WordPress, set
`opcache.max_accelerated_files` above the file count of core plus all plugins,
which often passes 10,000.

## Horizontal scaling

WordPress must be stateless before you add application servers:

- **Uploads** in object storage (S3, GCS) through an offload plugin. NFS adds
  latency and a single point of failure.
- **Object cache** on a shared Redis.
- **Nothing written to local disk at runtime.** Move disk-based page caching to
  the load balancer, Varnish, or the CDN.
- **`DISALLOW_FILE_MODS`** set, so no node installs code.
- **Cron on one node**: `DISABLE_WP_CRON` everywhere, and one system cron running
  `wp cron event run --due-now`.

Avoid sticky sessions. They hide state that should have moved out and unbalance
load; use them only as a stopgap for a plugin that stores state locally.

## Database clustering

- **Read replicas** when the database CPU is the bottleneck and the load is
  read-heavy, which most WordPress traffic is. WordPress has no native read/write
  split; use LudicrousDB or ProxySQL.
- **Replication lag.** After a write, read from the primary for the rest of that
  request (LudicrousDB does this by default). Send admin, logged-in, and checkout
  traffic to the primary.
- **Galera multi-primary** only when writes must survive a node failure without
  a failover step. WordPress's hot rows (`wp_options`, counters) cause
  certification conflicts under Galera. Prefer primary-replica with automatic
  failover, such as a managed database (RDS or Aurora, Cloud SQL).

## CDN

| Topology | Choose when |
| --- | --- |
| Static assets only (`wp-content`, `wp-includes`) | Every site; near-zero risk |
| Full-site HTML at the edge (Cloudflare APO, Fastly, CloudFront) | Anonymous traffic dominates and the audience is global. Needs purge integration and the bypass rules in [performance.md](performance.md#choose-the-caching-layer). |
| Multi-CDN | Very large audiences or contractual uptime; doubles purge and configuration work |

- Add an **origin shield** when many points of presence would otherwise hit the
  origin.
- Use an **image CDN** with on-the-fly resizing and WebP or AVIF when the media
  library is large or the theme registers many image sizes.
- Serve **video** from a streaming host, not from WordPress uploads.

## Edge and static

- **Static generation** (WP2Static, Simply Static) for brochure sites with no
  forms, search, or comments that need PHP, or as a fallback copy. Forms and
  search then move to third-party services.
- **ESI** for cacheable pages with small dynamic regions (cart count, greeting).
  It needs Varnish, Fastly, or Akamai.
- **Edge workers** (Cloudflare Workers, Lambda@Edge) for geo or A/B routing,
  header rewrites, and cookie-based cache keys. Business logic stays at the
  origin.
