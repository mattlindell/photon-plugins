---
name: database-patterns
description: Database query and optimization patterns for Eloquent (Laravel/Sage), WordPress ($wpdb, WP_Query, meta queries), and CodeIgniter 3 Query Builder. Use when writing database queries, optimizing N+1 problems, creating migrations, or deciding between post meta and custom tables.
---

# Database Patterns

Query and optimization patterns for Eloquent ORM (Laravel/Sage), WordPress database APIs (`WP_Query`, `$wpdb`, meta/tax queries), and CodeIgniter 3 Query Builder.

## When to Use This Skill

- Writing any database query (SELECT, INSERT, UPDATE, DELETE) in any framework
- Diagnosing or fixing N+1 query problems in Eloquent
- Choosing between `WP_Query`, `get_posts()`, and direct `$wpdb` calls
- Creating database migrations (Laravel) or custom tables (WordPress)
- Deciding whether to use post meta or a custom table in WordPress
- Wrapping expensive queries with object caching
- Processing large datasets without exhausting memory
- Handling transactions that must succeed or fail atomically
- Modifying the WordPress main query safely with `pre_get_posts`
- Working with CI3 Active Record / Query Builder in legacy code

## Core Concepts

**Prepared statements everywhere.** Never concatenate user input into SQL strings.

**Eager load relationships.** Eliminate N+1 queries by loading related data upfront.

**Transaction boundaries.** Group related writes so they succeed or fail as a unit.

**Cache expensive reads.** Queries on every page load that rarely change should be cached.

---

## Quick Start

**Eloquent -- fix N+1:**
```php
// Before: N+1 queries (100 posts = 101 queries)
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name;
}

// After: 2 queries total
$posts = Post::with('author')->get();
foreach ($posts as $post) {
    echo $post->author->name;
}
```

**WordPress -- safe raw query:**
```php
global $wpdb;

// NEVER: $wpdb->get_results("SELECT * FROM {$wpdb->posts} WHERE post_author = $user_id");
// ALWAYS:
$wpdb->get_results(
    $wpdb->prepare("SELECT * FROM {$wpdb->posts} WHERE post_author = %d", $user_id)
);
```

**CI3 -- safe query:**
```php
// NEVER: $this->db->query("SELECT * FROM users WHERE id = $id");
// ALWAYS:
$this->db->get_where('users', ['id' => $id]);
```

---

## Eloquent Patterns (Laravel / Sage)

### 1. N+1 Problem and Eager Loading

Eloquent lazy-loads relationships by default -- one additional query per iteration.

**BAD -- N+1 queries:**
```php
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->title . ' by ' . $post->author->name; // query per iteration
}
```

**GOOD -- eager loading (2 queries total):**
```php
$posts = Post::with('author')->get();
foreach ($posts as $post) {
    echo $post->title . ' by ' . $post->author->name;
}
```

**Nested eager loading:**
```php
$posts = Post::with(['author.profile', 'comments.user'])->get();
```

**Constrained eager loading:**
```php
$posts = Post::with([
    'comments' => function ($query) {
        $query->where('approved', true)->orderBy('created_at', 'desc')->limit(5);
    },
])->get();
```

Enable `preventLazyLoading()` in development to catch N+1 early:
```php
// app/Providers/AppServiceProvider.php
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

---

### 2. Query Scopes

Scopes encapsulate reusable query constraints.

**Local scope:**
```php
class Post extends Model
{
    public function scopePublished(Builder $query): Builder
    {
        return $query->where('status', 'published')
                     ->whereNotNull('published_at')
                     ->where('published_at', '<=', now());
    }

    public function scopeByAuthor(Builder $query, int $authorId): Builder
    {
        return $query->where('author_id', $authorId);
    }
}

// Usage: scopes are chainable
$posts = Post::published()->byAuthor(42)->paginate(15);
```

**Global scope:**
```php
class ActiveScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('is_active', true);
    }
}

#[ScopedBy(ActiveScope::class)]
class Subscription extends Model
{
    // Every query includes WHERE is_active = 1 automatically.
    // Bypass: Subscription::withoutGlobalScope(ActiveScope::class)->get();
}
```

---

### 3. Chunking and Lazy Collections

For processing thousands of rows without exhausting memory, use `lazy()`:

```php
Order::where('created_at', '>=', now()->subMonth())
    ->lazy(1000)
    ->each(function (Order $order) {
        ExportService::writeRow($order);
    });
```

| Method | Memory | Use When |
|---|---|---|
| `chunk()` | Fixed (batch size) | Processing in batches, sending notifications |
| `chunkById()` | Fixed (batch size) | Updating/deleting rows during iteration |
| `lazy()` | Minimal (one row) | Streaming, exports, pipelines |

---

### 4. Transactions

Wrap related writes so they either all succeed or all roll back.

```php
use Illuminate\Support\Facades\DB;

$order = DB::transaction(function () use ($cart, $user) {
    $order = Order::create([
        'user_id' => $user->id,
        'total'   => $cart->total(),
        'status'  => 'pending',
    ]);

    foreach ($cart->items() as $item) {
        OrderItem::create([
            'order_id'   => $order->id,
            'product_id' => $item->product_id,
            'quantity'   => $item->quantity,
            'price'      => $item->price,
        ]);

        $product = Product::findOrFail($item->product_id);
        if ($product->stock < $item->quantity) {
            throw new InsufficientStockException($product);
        }
        $product->decrement('stock', $item->quantity);
    }

    return $order;
});
// If any exception is thrown, all writes are rolled back.
// Pass a retry count as second arg for deadlock retries: DB::transaction(fn() => ..., 3);
```

---

### 5. Relationship Optimization

Query relationships efficiently without loading full related models.

```php
// withCount: adds comments_count attribute via subselect
$posts = Post::withCount('comments')->get();

// has: filter by relationship existence
$popularPosts = Post::has('comments', '>=', 5)->get();

// whereHas: filter by relationship conditions
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->whereHas('user', fn (Builder $q) => $q->whereNotNull('email_verified_at'));
})->get();

// withWhereHas: eager load only matching related models (Laravel 10+)
$posts = Post::withWhereHas('comments', function (Builder $query) {
    $query->where('approved', true);
})->get();
```

---

### 6. Migrations

Write reversible migrations with indexes for columns used in WHERE, JOIN, and ORDER BY.

```php
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('product_id')->constrained()->cascadeOnDelete();
            $table->string('status', 20)->default('pending');
            $table->decimal('total', 10, 2);
            $table->text('notes')->nullable();
            $table->timestamp('shipped_at')->nullable();
            $table->timestamps();
            $table->softDeletes();
            $table->index(['user_id', 'status']);
            $table->index('shipped_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('orders');
    }
};
```

Migration best practices:
- Always implement `down()`. If truly irreversible, throw an exception.
- One logical change per migration.
- Add indexes at creation time. Every `foreignId` gets an index from `constrained()`.
- For zero-downtime: add nullable columns first, deploy, backfill, then add constraints.

---

## WordPress Database Patterns

### 7. WP_Query with Meta and Tax Queries

`WP_Query` is the primary post query API. Combine `meta_query` and `tax_query` for compound filtering.

```php
$args = [
    'post_type'      => 'product',
    'post_status'    => 'publish',
    'posts_per_page' => 20,
    'tax_query'      => [
        [
            'taxonomy' => 'product_cat',
            'field'    => 'slug',
            'terms'    => 'electronics',
        ],
    ],
    'meta_query'     => [
        'relation' => 'AND',
        'stock_clause' => [
            'key'     => '_stock_status',
            'value'   => 'instock',
            'compare' => '=',
        ],
        'price_clause' => [
            'key'     => '_price',
            'value'   => [10, 500],
            'type'    => 'NUMERIC',
            'compare' => 'BETWEEN',
        ],
    ],
    'orderby' => 'price_clause',
    'order'   => 'ASC',
];

$query = new WP_Query($args);

if ($query->have_posts()) {
    while ($query->have_posts()) {
        $query->the_post();
        echo get_the_title() . ': $' . get_post_meta(get_the_ID(), '_price', true);
    }
    wp_reset_postdata();
}
```

Nested meta queries (OR inside AND) are supported:
```php
'meta_query' => [
    'relation' => 'AND',
    ['key' => 'is_featured', 'value' => '1'],
    [
        'relation' => 'OR',
        ['key' => 'is_free', 'value' => '1'],
        ['key' => 'ticket_price', 'value' => 50, 'type' => 'NUMERIC', 'compare' => '<='],
    ],
],
```

**Performance note:** Meta queries on large datasets are slow (EAV schema). For frequent queries on 10k+ posts, add a custom index or move data to a custom table (see section 11).

---

### 9. Safe Raw Queries with `$wpdb->prepare()`

Use `$wpdb` with `prepare()` for custom tables, complex JOINs, and aggregates.

**SELECT:**
```php
global $wpdb;

$user_meta = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->usermeta} WHERE user_id = %d AND meta_key = %s",
        $user_id,
        'billing_address'
    )
);

$count = $wpdb->get_var(
    $wpdb->prepare(
        "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = %s AND post_status = %s",
        'product',
        'publish'
    )
);
```

**INSERT:**
```php
global $wpdb;

$wpdb->insert(
    "{$wpdb->prefix}custom_logs",
    [
        'user_id'    => $user_id,
        'action'     => 'login',
        'ip_address' => $_SERVER['REMOTE_ADDR'],
        'created_at' => current_time('mysql', true),
    ],
    ['%d', '%s', '%s', '%s']
);

$new_id = $wpdb->insert_id;
```

**Format placeholders:**

| Placeholder | Type | Example |
|---|---|---|
| `%d` | Integer | `42` |
| `%f` | Float | `3.14` |
| `%s` | String | `'hello'` (auto-escaped and quoted) |
| `%i` | Identifier | Table/column names (WP 6.2+) |

---

### 10. Custom Table Creation with `dbDelta()`

`dbDelta()` creates or updates tables by diffing your SQL against the existing schema. It is extremely particular about formatting.

**CRITICAL formatting requirements:**

1. Each field must be on its own line.
2. TWO spaces between the column name and the column definition.
3. Use `KEY` (not `INDEX`) for indexes.
4. `PRIMARY KEY` on its own line with TWO spaces before the column name in parentheses.
5. Use `{$charset_collate}` from `$wpdb->get_charset_collate()`.
6. No trailing comma after the last column/index definition.
7. Use `CREATE TABLE` (not `CREATE TABLE IF NOT EXISTS`).

```php
function myplugin_create_tables(): void {
    global $wpdb;

    $table_name      = $wpdb->prefix . 'myplugin_events';
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE {$table_name} (
        id  bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        user_id  bigint(20) unsigned NOT NULL DEFAULT 0,
        event_type  varchar(50) NOT NULL DEFAULT '',
        event_data  longtext NOT NULL,
        ip_address  varchar(45) NOT NULL DEFAULT '',
        created_at  datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        PRIMARY KEY  (id),
        KEY user_id  (user_id),
        KEY event_type  (event_type),
        KEY created_at  (created_at)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta($sql);
}
```

**Version tracking for schema updates:**
```php
function myplugin_maybe_update_db(): void {
    $installed_version = get_option('myplugin_db_version', '0');
    $current_version   = '1.2.0';

    if (version_compare($installed_version, $current_version, '<')) {
        myplugin_create_tables();
        update_option('myplugin_db_version', $current_version);
    }
}
add_action('plugins_loaded', 'myplugin_maybe_update_db');
```

---

### 11. Post Meta vs Custom Tables: Decision Framework

| Criteria | Post Meta | Custom Table |
|---|---|---|
| Setup effort | Zero | Must create table, manage schema |
| Query simplicity | `get_post_meta()`, `meta_query` | Custom `$wpdb` queries |
| Plugin compatibility | Full (ACF, CMB2, REST API) | Must build integrations |
| Performance at scale | Degrades with row count | Scales with proper indexes |
| Complex queries | Slow (EAV joins) | Fast (native SQL) |
| Data integrity | No constraints | Foreign keys, unique, NOT NULL |
| Aggregation | Very slow | Native SQL performance |
| Best for | <10k posts, display-only, plugin compat | High volume, frequent queries, relational data |

**Hybrid approach:** Store the most-queried value as post meta for `WP_Query` compatibility, and store detailed data in a custom table with the post ID as a foreign key.

---

### 12. Object Caching

Wrap expensive queries with the WordPress Object Cache API.

```php
function myplugin_get_featured_products(int $limit = 10): array {
    $cache_key = "featured_products_{$limit}";
    $products  = wp_cache_get($cache_key, 'myplugin');

    if (false === $products) {
        $query = new WP_Query([
            'post_type'      => 'product',
            'post_status'    => 'publish',
            'posts_per_page' => $limit,
            'meta_query'     => [['key' => '_featured', 'value' => 'yes']],
        ]);
        $products = $query->posts;
        wp_cache_set($cache_key, $products, 'myplugin', 3600);
    }

    return $products;
}

// Invalidate when data changes
function myplugin_clear_featured_cache(int $post_id, WP_Post $post): void {
    if ($post->post_type !== 'product') return;
    wp_cache_delete('featured_products_10', 'myplugin');
    wp_cache_delete('featured_products_20', 'myplugin');
}
add_action('save_post', 'myplugin_clear_featured_cache', 10, 2);
```

---

### 13. Modifying the Main Query with `pre_get_posts`

Always check `is_main_query()` and `! is_admin()` to avoid affecting admin screens and secondary queries.

```php
function myplugin_modify_main_query(WP_Query $query): void {
    if (is_admin() || ! $query->is_main_query()) {
        return;
    }

    if ($query->is_search()) {
        $query->set('post_type', ['post', 'page', 'product', 'event']);
    }

    if ($query->is_home()) {
        $query->set('posts_per_page', 12);
    }

    if ($query->is_post_type_archive('event')) {
        $query->set('meta_key', 'event_date');
        $query->set('orderby', 'meta_value');
        $query->set('order', 'ASC');
        $query->set('meta_query', [
            ['key' => 'event_date', 'value' => current_time('Y-m-d'), 'compare' => '>=', 'type' => 'DATE'],
        ]);
    }
}
add_action('pre_get_posts', 'myplugin_modify_main_query');
```

---

## CodeIgniter 3 Query Builder Patterns

CI3 is legacy software. These patterns are for maintaining existing CI3 applications safely.

### 14. Query Builder

```php
class User_model extends CI_Model
{
    public function get_active_users(int $limit = 20, int $offset = 0): array
    {
        return $this->db
            ->select('users.id, users.name, users.email, roles.name AS role_name')
            ->from('users')
            ->join('roles', 'roles.id = users.role_id', 'left')
            ->where('users.is_active', 1)
            ->where('users.deleted_at IS NULL', null, false)
            ->order_by('users.name', 'ASC')
            ->limit($limit, $offset)
            ->get()
            ->result();
    }

    public function search_users(string $term): array
    {
        return $this->db
            ->select('id, name, email')
            ->from('users')
            ->group_start()
                ->like('name', $term)
                ->or_like('email', $term)
            ->group_end()
            ->where('is_active', 1)
            ->limit(50)
            ->get()
            ->result();
    }
}
```

For raw SQL, always use query bindings:
```php
// NEVER: $this->db->query("SELECT * FROM users WHERE email = '$email'");
// ALWAYS:
$this->db->query("SELECT * FROM users WHERE email = ?", [$email]);
```

---

### 15. Transaction Handling

Use `trans_start()` / `trans_complete()` for automatic rollback on failure.

```php
class Order_model extends CI_Model
{
    public function create_order(array $order_data, array $items)
    {
        $this->db->trans_start();

        $this->db->insert('orders', [
            'user_id'    => $order_data['user_id'],
            'total'      => $order_data['total'],
            'status'     => 'pending',
            'created_at' => date('Y-m-d H:i:s'),
        ]);
        $order_id = $this->db->insert_id();

        foreach ($items as $item) {
            $this->db->insert('order_items', [
                'order_id'   => $order_id,
                'product_id' => $item['product_id'],
                'quantity'   => $item['quantity'],
                'price'      => $item['price'],
            ]);
            $this->db->where('id', $item['product_id']);
            $this->db->set('stock', 'stock - ' . (int) $item['quantity'], false);
            $this->db->update('products');
        }

        $this->db->trans_complete();

        if ($this->db->trans_status() === false) {
            log_message('error', 'Order creation failed for user: ' . $order_data['user_id']);
            return false;
        }

        return $order_id;
    }
}
```

---

## Best Practices Summary

1. **Never concatenate user input into SQL.** Use prepared statements (`$wpdb->prepare()`, Eloquent parameterized queries, CI3 query bindings) for every query.
2. **Index columns used in WHERE, JOIN, and ORDER BY.** Missing indexes are the most common cause of slow queries.
3. **Use transactions for multi-step writes.** Partial data from failed operations corrupts your database.
4. **Limit result sets.** Always include `LIMIT` / `posts_per_page` / `->limit()` unless you genuinely need every row.
5. **Enable `preventLazyLoading()` in development** to catch N+1 problems before production.
6. **Always call `wp_reset_postdata()`** after a custom `WP_Query` loop.
7. **Follow `dbDelta()` formatting rules exactly.** Two spaces between column name and definition, `KEY` not `INDEX`, `PRIMARY KEY` on its own line.
8. **Check `is_main_query()` and `! is_admin()`** in every `pre_get_posts` callback.
