# Headless WordPress

## Headless or traditional

Choose **headless** when the frontend team works in a JavaScript framework, when
content feeds several channels (web and app), or when the goals need static
output with no PHP on the request path.

Stay **traditional** when editors rely on plugins that render frontend output
(forms, page builders, SEO output, WooCommerce checkout), when preview must be
instant and exact, when the team works only in PHP, or when the budget does not
cover two applications.

Headless costs two deployments, preview plumbing, and rebuilding everything
plugins used to render for free. Price those before recommending it.

## REST or GraphQL

| Choose | When |
| --- | --- |
| REST | Endpoints map one-to-one to pages, the content model is small, or many simple consumers need CDN-cacheable GET URLs |
| WPGraphQL | Pages compose many related types in one request and the frontend wants a typed schema |

WPGraphQL needs an extension per plugin it exposes (ACF, WooCommerce). Its POST
queries do not cache at a CDN; use persisted queries over GET.

## Frontend framework

Pick by the team's skills first. Then: Next.js for React teams that need
incremental or on-demand revalidation; Astro for content-heavy, mostly static
sites with little JavaScript; Nuxt for Vue teams.

## Rendering and revalidation

| Strategy | Choose when |
| --- | --- |
| Full static build | A few thousand pages or fewer, and build time is acceptable |
| Time-based revalidation (ISR) | Content may be stale for a known number of seconds |
| On-demand revalidation | Editorial sites; the default |

For on-demand revalidation, hook `transition_post_status` to call the frontend's
revalidate endpoint with a shared secret.

## Preview

Drafts are not public, so preview needs an authenticated fetch. Use the
framework's draft mode with a token that WordPress mints, and point WordPress's
preview link at the frontend with the `preview_post_link` filter.

## Authentication

| Method | Use for |
| --- | --- |
| Application passwords (core since 5.6) | Server-to-server: builds and preview fetches. Per-user and revocable, HTTPS only. |
| JWT plugin | End users logging in through the frontend |
| OAuth | Third parties acting on behalf of users |

Keep credentials on the server side of the frontend; nothing in the browser
bundle should authenticate to WordPress.

## API surface

- Restrict CORS to the frontend origins.
- Limit `/wp/v2/users` on a public API, which otherwise enumerates authors.
- Version custom namespaces (`myapp/v1`) and add `v2` instead of changing `v1`.
  Endpoint code is in `wp-rest-api-patterns`.

## Hybrid

- **Partial headless.** Keep the WordPress theme for routes that depend on
  plugins (checkout, account) and serve the rest from the frontend; route by
  path at the CDN or reverse proxy.
- **Content federation.** Aggregate several WordPress installs at the frontend's
  build layer instead of syncing content between them.
