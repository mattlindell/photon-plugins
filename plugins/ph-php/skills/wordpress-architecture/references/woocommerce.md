# WooCommerce architecture and scaling

Code for checkout fields, product types, gateways, and HPOS-compatible meta
access is in `woocommerce-patterns`.

## Product data model

The meta-versus-custom-table framework is in `database-patterns` (§11). On top
of it, for stores:

- Use **global attributes** (`pa_*` taxonomies) for anything shoppers filter on.
  Custom per-product attributes live in meta and filter slowly.
- **Variations** are posts. Each one adds rows, and past
  `woocommerce_ajax_variation_threshold` (30 by default) the frontend switches to
  AJAX lookups. When a combination does not need its own SKU, stock, or price,
  use product add-ons instead of variations.

## HPOS migration

1. Audit every active plugin for an HPOS compatibility declaration. The features
   screen (WooCommerce → Settings → Advanced → Features) lists incompatible ones.
   Do not migrate while any order-touching plugin is incompatible.
2. Turn on compatibility mode, which syncs the posts tables and the orders
   tables. On large stores, sync in bulk with WooCommerce's WP-CLI HPOS commands
   (`wp wc hpos --help`) instead of waiting for Action Scheduler batches.
3. Verify the synced data, then switch authoritative storage to HPOS with sync
   still on, so you can roll back.
4. Turn sync off after a stable period.

## Cart, session, and checkout

- Sessions live in `wp_woocommerce_sessions`. Any page that varies by the cart
  cookie must bypass the page cache or render the cart region at the edge.
- Since WooCommerce 7.8, the cart-fragments script loads only with the legacy
  Mini-Cart widget. A theme or plugin that enqueues it again puts an uncached
  AJAX request on every page view.
- **Block or classic checkout.** Block checkout is the default for new stores
  since 8.3. Extensions that add fields through `woocommerce_checkout_fields` do
  nothing in block checkout; they need the Additional Checkout Fields API or a
  Store API extension. Audit every checkout customization before switching.

## Scaling the catalog and orders

- **100k+ products.** Move search and layered filtering off meta queries: turn on
  the product attributes lookup table, and move search to Elasticsearch or
  OpenSearch (ElasticPress).
- **Order volume.** Keep post-order work (ERP sync, fulfillment, CRM) off the
  checkout request; queue it in Action Scheduler. Run the queue from WP-CLI on a
  system cron rather than WP-Cron. Lower the retention of completed actions
  (30 days by default) on high-volume stores.
- **Inventory.** Real-time stock holds (the hold-stock setting) prevent overselling
  but contend under flash-sale load. Eventual consistency is acceptable when
  backorders are allowed. With an external inventory system, make it the single
  source of truth and sync by webhook; never let two systems write stock.
- **Payment gateways.** Choose by supported payment methods, payout schedule, and
  dispute tooling. Offer a second gateway as a customer-visible alternative.
  Automatic retry across gateways risks double charges.

## Extend or build custom

Extend WooCommerce when the store fits its product, cart, and order model and a
maintained extension covers most of the need. Build custom, or choose another
platform, when the core model fights you (marketplace payouts, non-cart purchase
flows).

- **Subscriptions.** Use WooCommerce Subscriptions for standard recurring
  billing. When billing logic outgrows it, make the gateway's billing product
  (Stripe Billing) the system of record rather than writing a scheduler.
- **B2B.** Role-based pricing and quote or approval flows come from extensions;
  check that they work with the checkout type you run.
- **Multi-currency.** Decide between display-only conversion and real
  per-currency prices with per-currency settlement; the second affects
  accounting and gateways.
- **Multi-language.** WPML duplicates each product per language, which
  multiplies catalog rows; factor that into the catalog scaling above.
