---
name: wordpress-architecture
description: WordPress architecture decisions with tradeoffs. Use when choosing a caching, CDN, or Core Web Vitals strategy, deciding on multisite, planning WooCommerce architecture or scaling, evaluating headless WordPress, choosing hosting or a deployment pipeline, planning a site migration or version upgrade, or scaling WordPress infrastructure.
---

# WordPress Architecture

This skill decides *what* to build and *why*. It ends at a recommendation, not
code; the pattern skills (`wordpress-plugin-patterns`, `woocommerce-patterns`,
`database-patterns`, and the rest) hold the implementation.

## Gather the six inputs

Pin down each input before recommending anything. When one is unknown, state the
assumption you made for it in the recommendation.

1. **Traffic and scale** — peak concurrent users, geographic spread, and the
   share of traffic that is logged in. The logged-in share matters most: page
   caching serves anonymous visitors only, so every logged-in or cart-holding
   visitor reaches PHP.
2. **Content model** — ratio of static to dynamic content, custom data
   structures, and expected row counts.
3. **Integrations** — e-commerce, membership, LMS, and third-party APIs.
4. **Team** — who maintains the site after launch, and what they can operate.
5. **Budget** — hosting, plugin licenses, and build time.
6. **Targets** — page-load and Core Web Vitals goals, and the uptime SLA.

## Recommend with tradeoffs

Each recommendation names the option chosen, the runner-up, and the input that
decided between them. "Use Redis" is incomplete; "Redis over Memcached, because
the host provides it and the store needs persistent cart sessions" is a
recommendation.

## Decision areas

Read the reference for the area in front of you.

| Question | Reference |
| --- | --- |
| Profiling, caching layers, cache invalidation, Core Web Vitals | [references/performance.md](references/performance.md) |
| Multisite or separate installs, network type, scaling a network | [references/multisite.md](references/multisite.md) |
| Store data model, HPOS migration, checkout, catalog and order scaling | [references/woocommerce.md](references/woocommerce.md) |
| Headless or traditional, REST or GraphQL, preview, rendering | [references/headless.md](references/headless.md) |
| Local environments, deployment, hosting choice, monitoring | [references/devops.md](references/devops.md) |
| Site transfers, host moves, platform changes, version upgrades | [references/migration.md](references/migration.md) |
| Vertical and horizontal scaling, database clustering, CDN, edge | [references/scaling.md](references/scaling.md) |

A site that is broken rather than being designed goes to
`wordpress-troubleshooting`.
