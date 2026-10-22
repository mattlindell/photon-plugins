# Performance and caching

## Profile before optimizing

Record a baseline before changing anything: uncached and cached TTFB, query
count, and peak memory for the slow pages. Set a measurable target. Use Query
Monitor on staging and an APM (New Relic, Blackfire, Tideways) in production.

Work the layers in impact order: **database queries → object cache → page cache
→ CDN → frontend**. A fix lower in that list cannot rescue a slow layer above
it. A page cache hides slow queries from anonymous visitors only; logged-in,
cart, and checkout requests still pay for them.

Classify the slowness before fixing it:

| Signal | Likely cause |
| --- | --- |
| Slow on every page, even with a default theme and plugins off | Hosting: CPU, PHP workers, disk, or database server |
| Slow only while one plugin is active | That plugin |
| Fast uncached at low load, slow under load | Capacity: PHP-FPM workers or database connections |
| Hundreds of queries per page, or single queries over 100 ms | Architecture: data model, meta queries, no persistent object cache |

## Choose the caching layer

| Need | Layer |
| --- | --- |
| Whole page for anonymous visitors | Page cache: Nginx FastCGI cache, Varnish, host-level, or a plugin |
| Expensive computed value reused across requests | Object cache (`wp_cache_*`) on a persistent backend |
| Value that must expire on schedule and survive without a persistent object cache | Transient |
| One dynamic region in an otherwise cacheable page | Fragment cache in the object cache, or ESI at the edge |

Without a persistent object cache, transients live in `wp_options`, and a
transient set without an expiration is autoloaded on every request. Give every
transient an expiration.

Object cache code is in `database-patterns` (§12).

**Redis or Memcached.** Choose Redis by default: it supports persistence, more
data types, and has the broader plugin support (Redis Object Cache, Object Cache
Pro). Choose Memcached when the host provides it and nothing needs persistence.
Run one Redis node with a replica until the cache outgrows one node's memory or
throughput; move to a cluster or a managed service past that. Set
`maxmemory-policy allkeys-lru` on a cache-only Redis.

**Page-cache bypass rules.** Bypass for the `wordpress_logged_in_*` cookie, the
WooCommerce cookies (`woocommerce_items_in_cart`, `wp_woocommerce_session_*`),
the cart, checkout, and account pages, and every POST. Strip tracking parameters
(`utm_*`, `gclid`, `fbclid`) from the cache key instead of bypassing on them.

## Plan invalidation

- **Event-based purge** for content that must be fresh: purge on `save_post`, on
  stock changes, and on comment approval.
- **Time-based TTL** for derived or aggregate data where some staleness is
  acceptable.
- Purge the narrowest set: the post URL, its archives, the home page, and its
  feeds. A full purge on every save turns a cache into a cold start.

**Cache-Control by content type:**

| Content | Header |
| --- | --- |
| Anonymous HTML | Short `s-maxage` at the edge, with purge-on-publish |
| Fingerprinted CSS and JS | `max-age=31536000, immutable` |
| Uploads | Long `max-age` |
| Logged-in or personalized responses | `private, no-store` |

CDN topology is in [scaling.md](scaling.md#cdn).

## Core Web Vitals

Judge against field data (CrUX) at the 75th percentile, not a single Lighthouse
run. The "good" thresholds are LCP ≤ 2.5 s, INP ≤ 200 ms, and CLS ≤ 0.1.

- **LCP.** Find the LCP element first; it is usually the hero image or the
  heading. Exclude it from lazy loading, give it `fetchpriority="high"`, and
  preload it when it is a CSS background. TTFB is part of LCP, so the page cache
  comes before frontend work.
- **CLS.** Set `width` and `height` on images and embeds. Reserve space for ad
  slots, banners, and cookie notices. Use `font-display` with a size-adjusted
  fallback font.
- **INP.** Look for long tasks from plugin and third-party JavaScript. Defer or
  delay third-party scripts until interaction.

Each plugin's frontend assets cost Core Web Vitals on every page that loads
them. Require a plugin to load its assets only on the pages that use it; dequeue
them elsewhere, or replace the plugin.
