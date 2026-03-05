---
name: wordpress-plugin-patterns
description: WordPress plugin development patterns — OOP architecture with PSR-4 autoloading, hook registration, activation/deactivation lifecycle, Gutenberg blocks, AJAX handlers, WP-CLI commands, custom post types, WP_Query, and transients. Use when building WordPress plugins or working with core WordPress APIs.
---

# WordPress Plugin Development Patterns

## Introduction

Production-ready patterns for WordPress plugin development. Every example is complete, PHP 8.0+ compatible, and follows WordPress Coding Standards with proper escaping, sanitization, and nonce verification.

## When to Use This Skill

- Creating WordPress plugins with modern OOP architecture
- Registering custom Gutenberg blocks with PHP render callbacks
- Writing `WP_Query` calls with meta or taxonomy queries
- Caching expensive operations with the Transients API
- Registering custom post types and taxonomies
- Handling AJAX requests through `admin-ajax.php`
- Building WP-CLI commands for maintenance or data operations

## Core Concepts

**Hook System**: Actions (do something at a point) and filters (modify a value and return it). All extensibility flows through `add_action()` and `add_filter()`.

**Escape Late, Sanitize Early**: Sanitize all input on entry. Escape all output at render time. Never trust user input, database values, or API responses.

**WordPress Coding Standards**: Tabs for indentation, `snake_case` for functions/variables, Yoda conditions, braces on same line.

---

## 1. OOP Plugin Bootstrap with PSR-4 Autoloading

**Directory structure:**

```
acme-plugin/
  acme-plugin.php
  composer.json
  uninstall.php
  src/
    Plugin.php
    Admin/Settings.php
    Core/Activator.php
    Core/Deactivator.php
    Core/PostTypes.php
    Public/Assets.php
```

**composer.json:**

```json
{
    "name": "acme/acme-plugin",
    "type": "wordpress-plugin",
    "license": "GPL-2.0-or-later",
    "require": { "php": ">=8.0" },
    "autoload": {
        "psr-4": { "Acme\\AcmePlugin\\": "src/" }
    },
    "config": { "optimize-autoloader": true }
}
```

**acme-plugin.php:**

```php
<?php
/**
 * Plugin Name: Acme Plugin
 * Version:     1.0.0
 * Requires PHP: 8.0
 * Text Domain: acme-plugin
 */

declare(strict_types=1);

namespace Acme\AcmePlugin;

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'ACME_PLUGIN_VERSION', '1.0.0' );
define( 'ACME_PLUGIN_FILE', __FILE__ );
define( 'ACME_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'ACME_PLUGIN_URL', plugin_dir_url( __FILE__ ) );
define( 'ACME_PLUGIN_BASENAME', plugin_basename( __FILE__ ) );

if ( file_exists( ACME_PLUGIN_DIR . 'vendor/autoload.php' ) ) {
    require_once ACME_PLUGIN_DIR . 'vendor/autoload.php';
}

register_activation_hook( __FILE__, [ Core\Activator::class, 'activate' ] );
register_deactivation_hook( __FILE__, [ Core\Deactivator::class, 'deactivate' ] );

add_action( 'plugins_loaded', function (): void {
    Plugin::get_instance()->init();
}, 10 );
```

**src/Plugin.php:**

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin;

final class Plugin {

    private static ?self $instance = null;

    public static function get_instance(): self {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __clone() {}
    private function __construct() {}

    public function init(): void {
        load_plugin_textdomain( 'acme-plugin', false, dirname( ACME_PLUGIN_BASENAME ) . '/languages' );
        $this->register_hooks();
    }

    private function register_hooks(): void {
        $post_types = new Core\PostTypes();
        add_action( 'init', [ $post_types, 'register' ] );

        if ( is_admin() ) {
            $settings = new Admin\Settings();
            add_action( 'admin_menu', [ $settings, 'add_menu_page' ] );
            add_action( 'admin_init', [ $settings, 'register_settings' ] );
        }

        $assets = new Public\Assets();
        add_action( 'wp_enqueue_scripts', [ $assets, 'enqueue_styles' ] );
        add_action( 'wp_enqueue_scripts', [ $assets, 'enqueue_scripts' ] );
    }
}
```

---

## 2. Hook Registration Patterns

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class HookExamples {

    public function register(): void {
        add_action( 'init', [ $this, 'register_post_types' ] );          // default priority 10
        add_action( 'init', [ $this, 'register_taxonomies' ], 5 );       // early
        add_action( 'init', [ $this, 'late_init' ], 99 );                // late
        add_filter( 'the_content', [ $this, 'append_cta' ], 10, 2 );     // 2 args
        add_filter( 'wp_insert_post_data', [ $this, 'auto_excerpt' ], 10, 4 );
        add_action( 'wp_footer', [ $this, 'render_footer' ], 20 );       // named for removal
    }

    public function append_cta( string $content, mixed $post = null ): string {
        if ( ! is_singular( 'post' ) || ! is_main_query() ) {
            return $content;
        }
        $cta = sprintf(
            '<div class="acme-cta"><a href="%s">%s</a></div>',
            esc_url( home_url( '/newsletter/' ) ),
            esc_html__( 'Subscribe to our newsletter', 'acme-plugin' )
        );
        return $content . $cta;
    }

    public function auto_excerpt( array $data, array $postarr, array $unsanitized, bool $update ): array {
        if ( 'acme_project' === $data['post_type'] && empty( $data['post_excerpt'] ) ) {
            $data['post_excerpt'] = wp_trim_words( $data['post_content'], 30, '...' );
        }
        return $data;
    }
}
```

**Conventions**: Prefix custom hooks with your plugin slug (`acme_plugin_before_render`). Use `do_action()` for extensibility points. Use `apply_filters()` to allow value modification.

---

## 3. Activation, Deactivation, and Uninstall Lifecycle

**src/Core/Activator.php:**

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class Activator {

    public static function activate(): void {
        if ( version_compare( PHP_VERSION, '8.0', '<' ) ) {
            deactivate_plugins( ACME_PLUGIN_BASENAME );
            wp_die( esc_html__( 'Requires PHP 8.0+.', 'acme-plugin' ), '', [ 'back_link' => true ] );
        }

        self::create_tables();

        $defaults = [
            'acme_plugin_enable_cta'     => true,
            'acme_plugin_items_per_page' => 10,
        ];
        foreach ( $defaults as $key => $val ) {
            if ( false === get_option( $key ) ) {
                add_option( $key, $val );
            }
        }

        ( new PostTypes() )->register();
        flush_rewrite_rules();
        update_option( 'acme_plugin_version', ACME_PLUGIN_VERSION );
    }

    private static function create_tables(): void {
        global $wpdb;
        $table   = $wpdb->prefix . 'acme_logs';
        $charset = $wpdb->get_charset_collate();

        $sql = "CREATE TABLE {$table} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL DEFAULT 0,
            action varchar(100) NOT NULL DEFAULT '',
            message text NOT NULL,
            created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY  (id),
            KEY user_id (user_id),
            KEY action (action)
        ) {$charset};";

        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta( $sql );
    }
}
```

**src/Core/Deactivator.php:**

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class Deactivator {

    /** Do NOT delete data here -- deactivation must be reversible. */
    public static function deactivate(): void {
        $ts = wp_next_scheduled( 'acme_plugin_daily_cleanup' );
        if ( false !== $ts ) {
            wp_unschedule_event( $ts, 'acme_plugin_daily_cleanup' );
        }
        flush_rewrite_rules();
        delete_transient( 'acme_plugin_activated' );
    }
}
```

**uninstall.php** (plugin root):

```php
<?php
declare(strict_types=1);

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

foreach ( [ 'acme_plugin_version', 'acme_plugin_enable_cta', 'acme_plugin_items_per_page' ] as $opt ) {
    delete_option( $opt );
}

$wpdb->query(
    $wpdb->prepare( "DELETE FROM {$wpdb->postmeta} WHERE meta_key LIKE %s", $wpdb->esc_like( '_acme_plugin_' ) . '%' )
);

$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}acme_logs" );

$wpdb->query(
    $wpdb->prepare(
        "DELETE FROM {$wpdb->options} WHERE option_name LIKE %s OR option_name LIKE %s",
        $wpdb->esc_like( '_transient_acme_plugin_' ) . '%',
        $wpdb->esc_like( '_transient_timeout_acme_plugin_' ) . '%'
    )
);

wp_clear_scheduled_hook( 'acme_plugin_daily_cleanup' );
```

---

## 4. Gutenberg Block Registration

Demonstrates both a static render block and a dynamic query block. Both use `block.json` with `render` pointing to a PHP file.

**blocks/team-member/block.json:**

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "acme/team-member",
    "title": "Team Member",
    "category": "widgets",
    "icon": "admin-users",
    "textdomain": "acme-plugin",
    "attributes": {
        "name": { "type": "string", "default": "" },
        "role": { "type": "string", "default": "" },
        "bio": { "type": "string", "default": "" },
        "imageId": { "type": "number", "default": 0 }
    },
    "supports": {
        "html": false,
        "align": [ "wide", "full" ],
        "color": { "background": true, "text": true },
        "spacing": { "margin": true, "padding": true }
    },
    "style": "file:./style.css",
    "render": "file:./render.php"
}
```

**blocks/team-member/render.php:**

```php
<?php
declare(strict_types=1);

$name     = $attributes['name'] ?? '';
$role     = $attributes['role'] ?? '';
$bio      = $attributes['bio'] ?? '';
$image_id = (int) ( $attributes['imageId'] ?? 0 );

if ( empty( $name ) ) {
    return;
}

$wrapper = get_block_wrapper_attributes( [ 'class' => 'acme-team-member' ] );
$img     = $image_id > 0 ? wp_get_attachment_image( $image_id, 'medium', false, [ 'loading' => 'lazy' ] ) : '';
?>
<div <?php echo $wrapper; ?>>
    <?php if ( $img ) : ?>
        <div class="acme-team-member__image"><?php echo $img; ?></div>
    <?php endif; ?>
    <div class="acme-team-member__info">
        <h3><?php echo esc_html( $name ); ?></h3>
        <?php if ( $role ) : ?><p class="acme-team-member__role"><?php echo esc_html( $role ); ?></p><?php endif; ?>
        <?php if ( $bio ) : ?><p><?php echo esc_html( $bio ); ?></p><?php endif; ?>
    </div>
</div>
```

**blocks/recent-projects/block.json** (dynamic block):

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "acme/recent-projects",
    "title": "Recent Projects",
    "category": "widgets",
    "textdomain": "acme-plugin",
    "attributes": {
        "count": { "type": "number", "default": 3 },
        "showExcerpt": { "type": "boolean", "default": true },
        "projectType": { "type": "string", "default": "" }
    },
    "supports": { "html": false, "align": [ "wide", "full" ] },
    "render": "file:./render.php"
}
```

**blocks/recent-projects/render.php:**

```php
<?php
declare(strict_types=1);

$count        = (int) ( $attributes['count'] ?? 3 );
$show_excerpt = (bool) ( $attributes['showExcerpt'] ?? true );
$type_slug    = $attributes['projectType'] ?? '';

$args = [
    'post_type' => 'acme_project', 'posts_per_page' => $count,
    'post_status' => 'publish', 'no_found_rows' => true,
];

if ( $type_slug ) {
    $args['tax_query'] = [ [ 'taxonomy' => 'project_type', 'field' => 'slug', 'terms' => sanitize_text_field( $type_slug ) ] ];
}

$q = new \WP_Query( $args );
if ( ! $q->have_posts() ) { return; }

$wrapper = get_block_wrapper_attributes( [ 'class' => 'acme-recent-projects' ] );
?>
<div <?php echo $wrapper; ?>>
    <?php while ( $q->have_posts() ) : $q->the_post(); ?>
        <article>
            <?php if ( has_post_thumbnail() ) : ?>
                <a href="<?php echo esc_url( get_the_permalink() ); ?>"><?php the_post_thumbnail( 'medium', [ 'loading' => 'lazy' ] ); ?></a>
            <?php endif; ?>
            <h3><a href="<?php echo esc_url( get_the_permalink() ); ?>"><?php echo esc_html( get_the_title() ); ?></a></h3>
            <?php if ( $show_excerpt && has_excerpt() ) : ?><p><?php echo esc_html( get_the_excerpt() ); ?></p><?php endif; ?>
        </article>
    <?php endwhile; ?>
</div>
<?php wp_reset_postdata(); ?>
```

**Register blocks in plugin:**

```php
add_action( 'init', function (): void {
    register_block_type( ACME_PLUGIN_DIR . 'blocks/team-member' );
    register_block_type( ACME_PLUGIN_DIR . 'blocks/recent-projects' );
} );
```

---

## 5. WP_Query with meta_query and tax_query

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class QueryExamples {

    /**
     * Compound query: taxonomy filter + nested meta_query + meta ordering.
     *
     * Finds featured "web-design" projects that are either high-budget (>=50k)
     * OR recently completed, ordered by budget descending.
     */
    public function get_featured_web_projects(): array {
        $query = new \WP_Query( [
            'post_type'      => 'acme_project',
            'post_status'    => 'publish',
            'posts_per_page' => 12,
            'no_found_rows'  => true,
            'tax_query'      => [
                [
                    'taxonomy' => 'project_type',
                    'field'    => 'slug',
                    'terms'    => 'web-design',
                ],
            ],
            'meta_query'     => [
                'relation' => 'AND',
                [
                    'key'     => '_acme_project_featured',
                    'value'   => '1',
                    'compare' => '=',
                ],
                [
                    'relation' => 'OR',
                    [
                        'key'     => '_acme_project_budget',
                        'value'   => 50000,
                        'compare' => '>=',
                        'type'    => 'NUMERIC',
                    ],
                    [
                        'key'     => '_acme_project_completed_date',
                        'value'   => gmdate( 'Y-m-d', strtotime( '-6 months' ) ),
                        'compare' => '>=',
                        'type'    => 'DATE',
                    ],
                ],
            ],
            'orderby'  => 'meta_value_num',
            'meta_key' => '_acme_project_budget',
            'order'    => 'DESC',
        ] );

        return $query->posts;
    }
}
```

**Key options**: `no_found_rows => true` skips pagination overhead. Omit it when you need `$query->max_num_pages`. Use `'operator' => 'IN'` for multi-term matching. Use `'type' => 'NUMERIC'` or `'DATE'` for proper comparison casting.

---

## 6. Transients API for Caching

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class CacheExamples {

    /**
     * Cache an expensive WP_Query result.
     */
    public function get_featured_projects(): array {
        $key    = 'acme_featured_projects';
        $cached = get_transient( $key );

        if ( false !== $cached && is_array( $cached ) ) {
            return $cached;
        }

        $query = new \WP_Query( [
            'post_type'      => 'acme_project',
            'post_status'    => 'publish',
            'posts_per_page' => 6,
            'meta_query'     => [ [ 'key' => '_acme_project_featured', 'value' => '1' ] ],
        ] );

        $result = [ 'posts' => $query->posts, 'total' => $query->found_posts ];
        set_transient( $key, $result, HOUR_IN_SECONDS );

        return $result;
    }

    /**
     * Invalidate caches when a project is saved/deleted.
     */
    public function invalidate( int $post_id ): void {
        if ( 'acme_project' !== get_post_type( $post_id ) ) {
            return;
        }
        delete_transient( 'acme_featured_projects' );
        delete_transient( 'acme_project_stats' );
        do_action( 'acme_plugin_project_cache_invalidated', $post_id );
    }

    public function register_hooks(): void {
        add_action( 'save_post_acme_project', [ $this, 'invalidate' ] );
        add_action( 'delete_post', [ $this, 'invalidate' ] );
        add_action( 'trashed_post', [ $this, 'invalidate' ] );
    }
}
```

---

## 7. Custom Post Type and Taxonomy Registration

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class PostTypes {

    public function register(): void {
        $this->register_project_post_type();
        $this->register_project_type_taxonomy();
        $this->register_project_tag_taxonomy();
        $this->register_meta_fields();
    }

    private function register_project_post_type(): void {
        register_post_type( 'acme_project', [
            'labels' => [
                'name'               => esc_html_x( 'Projects', 'Post type general name', 'acme-plugin' ),
                'singular_name'      => esc_html_x( 'Project', 'Post type singular name', 'acme-plugin' ),
                'add_new_item'       => esc_html__( 'Add New Project', 'acme-plugin' ),
                'edit_item'          => esc_html__( 'Edit Project', 'acme-plugin' ),
                'view_item'          => esc_html__( 'View Project', 'acme-plugin' ),
                'all_items'          => esc_html__( 'All Projects', 'acme-plugin' ),
                'search_items'       => esc_html__( 'Search Projects', 'acme-plugin' ),
                'not_found'          => esc_html__( 'No projects found.', 'acme-plugin' ),
                'not_found_in_trash' => esc_html__( 'No projects found in Trash.', 'acme-plugin' ),
            ],
            'public'             => true,
            'show_in_rest'       => true,
            'rest_base'          => 'projects',
            'menu_position'      => 20,
            'menu_icon'          => 'dashicons-portfolio',
            'capability_type'    => 'post',
            'has_archive'        => true,
            'supports'           => [ 'title', 'editor', 'thumbnail', 'excerpt', 'custom-fields', 'revisions' ],
            'rewrite'            => [ 'slug' => 'projects', 'with_front' => false ],
            'template'           => [
                [ 'core/paragraph', [ 'placeholder' => 'Describe this project...' ] ],
                [ 'core/image' ],
            ],
        ] );
    }

    /** Hierarchical taxonomy (like categories). */
    private function register_project_type_taxonomy(): void {
        register_taxonomy( 'project_type', [ 'acme_project' ], [
            'labels' => [
                'name'          => esc_html_x( 'Project Types', 'taxonomy general name', 'acme-plugin' ),
                'singular_name' => esc_html_x( 'Project Type', 'taxonomy singular name', 'acme-plugin' ),
                'add_new_item'  => esc_html__( 'Add New Project Type', 'acme-plugin' ),
                'edit_item'     => esc_html__( 'Edit Project Type', 'acme-plugin' ),
                'search_items'  => esc_html__( 'Search Project Types', 'acme-plugin' ),
                'menu_name'     => esc_html__( 'Project Types', 'acme-plugin' ),
            ],
            'hierarchical'      => true,
            'public'            => true,
            'show_in_rest'      => true,
            'show_admin_column' => true,
            'rewrite'           => [ 'slug' => 'project-type', 'with_front' => false, 'hierarchical' => true ],
        ] );
    }

    /** Flat taxonomy (like tags). */
    private function register_project_tag_taxonomy(): void {
        register_taxonomy( 'project_tag', [ 'acme_project' ], [
            'labels' => [
                'name'                       => esc_html_x( 'Project Tags', 'taxonomy general name', 'acme-plugin' ),
                'singular_name'              => esc_html_x( 'Project Tag', 'taxonomy singular name', 'acme-plugin' ),
                'add_new_item'               => esc_html__( 'Add New Project Tag', 'acme-plugin' ),
                'separate_items_with_commas' => esc_html__( 'Separate tags with commas', 'acme-plugin' ),
                'menu_name'                  => esc_html__( 'Project Tags', 'acme-plugin' ),
            ],
            'hierarchical'      => false,
            'public'            => true,
            'show_in_rest'      => true,
            'show_admin_column' => true,
            'rewrite'           => [ 'slug' => 'project-tag', 'with_front' => false ],
        ] );
    }

    /** Expose meta fields to the REST API. */
    private function register_meta_fields(): void {
        register_post_meta( 'acme_project', '_acme_project_budget', [
            'type'              => 'integer',
            'single'            => true,
            'show_in_rest'      => true,
            'sanitize_callback' => 'absint',
            'auth_callback'     => fn(): bool => current_user_can( 'edit_posts' ),
        ] );

        register_post_meta( 'acme_project', '_acme_project_featured', [
            'type'              => 'boolean',
            'single'            => true,
            'show_in_rest'      => true,
            'default'           => false,
            'sanitize_callback' => 'rest_sanitize_boolean',
            'auth_callback'     => fn(): bool => current_user_can( 'edit_posts' ),
        ] );

        register_post_meta( 'acme_project', '_acme_project_status', [
            'type'              => 'string',
            'single'            => true,
            'show_in_rest'      => true,
            'default'           => 'planning',
            'sanitize_callback' => function ( string $value ): string {
                $allowed = [ 'planning', 'in-progress', 'completed' ];
                return in_array( $value, $allowed, true ) ? $value : 'planning';
            },
            'auth_callback'     => fn(): bool => current_user_can( 'edit_posts' ),
        ] );
    }
}
```

---

## 8. AJAX Handler

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\Core;

class AjaxHandlers {

    public function register(): void {
        add_action( 'wp_ajax_acme_load_more', [ $this, 'load_more' ] );
        add_action( 'wp_ajax_nopriv_acme_load_more', [ $this, 'load_more' ] );
    }

    public function enqueue_scripts(): void {
        if ( ! is_post_type_archive( 'acme_project' ) ) {
            return;
        }

        wp_enqueue_script( 'acme-ajax', ACME_PLUGIN_URL . 'assets/js/ajax-loader.js', [], ACME_PLUGIN_VERSION, [ 'in_footer' => true, 'strategy' => 'defer' ] );
        wp_localize_script( 'acme-ajax', 'acmeAjax', [
            'url'   => admin_url( 'admin-ajax.php' ),
            'nonce' => wp_create_nonce( 'acme_load_more_nonce' ),
        ] );
    }

    public function load_more(): void {
        if ( ! check_ajax_referer( 'acme_load_more_nonce', 'nonce', false ) ) {
            wp_send_json_error( [ 'message' => 'Security check failed.' ], 403 );
        }

        $page = isset( $_POST['page'] ) ? absint( $_POST['page'] ) : 1;

        $query = new \WP_Query( [
            'post_type' => 'acme_project', 'post_status' => 'publish',
            'posts_per_page' => 6, 'paged' => $page,
        ] );

        if ( ! $query->have_posts() ) {
            wp_send_json_success( [ 'html' => '', 'has_more' => false ] );
        }

        ob_start();
        while ( $query->have_posts() ) {
            $query->the_post();
            ?>
            <article class="acme-project-card">
                <?php if ( has_post_thumbnail() ) : ?>
                    <div class="acme-project-card__image"><?php the_post_thumbnail( 'medium', [ 'loading' => 'lazy' ] ); ?></div>
                <?php endif; ?>
                <h3><a href="<?php echo esc_url( get_the_permalink() ); ?>"><?php echo esc_html( get_the_title() ); ?></a></h3>
            </article>
            <?php
        }
        $html = ob_get_clean();
        wp_reset_postdata();

        wp_send_json_success( [ 'html' => $html, 'has_more' => $page < $query->max_num_pages ] );
    }
}
```

**Companion JavaScript** (`assets/js/ajax-loader.js`):

```js
( function () {
    'use strict';

    const btn = document.querySelector( '.acme-load-more-btn' );
    const grid = document.querySelector( '.acme-projects-grid' );
    if ( ! btn || ! grid ) return;

    let page = 1;

    btn.addEventListener( 'click', function () {
        page++;
        btn.disabled = true;
        btn.textContent = 'Loading...';

        const fd = new FormData();
        fd.append( 'action', 'acme_load_more' );
        fd.append( 'nonce', acmeAjax.nonce );
        fd.append( 'page', page.toString() );

        fetch( acmeAjax.url, { method: 'POST', credentials: 'same-origin', body: fd } )
            .then( r => r.json() )
            .then( ( { success, data } ) => {
                if ( success && data.html ) grid.insertAdjacentHTML( 'beforeend', data.html );
                if ( ! data.has_more ) btn.remove();
                else { btn.disabled = false; btn.textContent = 'Load More'; }
            } )
            .catch( () => { btn.disabled = false; btn.textContent = 'Load More'; } );
    } );
} )();
```

---

## 9. WP-CLI Command Registration

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\CLI;

use WP_CLI;
use WP_CLI\Utils;

class ProjectCommand {

    /**
     * List projects with optional filters.
     *
     * ## OPTIONS
     *
     * [--status=<status>]
     * : Filter by status (planning, in-progress, completed).
     *
     * [--format=<format>]
     * : Output format (table, csv, json). Default: table.
     *
     * [--featured]
     * : Show only featured projects.
     *
     * ## EXAMPLES
     *
     *     wp acme project list --status=completed --format=json
     */
    public function list_command( array $args, array $assoc_args ): void {
        $query_args = [
            'post_type' => 'acme_project', 'post_status' => 'publish',
            'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC',
        ];

        $meta_query = [];

        $status = Utils\get_flag_value( $assoc_args, 'status', '' );
        if ( $status ) {
            $allowed = [ 'planning', 'in-progress', 'completed' ];
            if ( ! in_array( $status, $allowed, true ) ) {
                WP_CLI::error( sprintf( 'Invalid status. Allowed: %s', implode( ', ', $allowed ) ) );
            }
            $meta_query[] = [ 'key' => '_acme_project_status', 'value' => $status ];
        }

        if ( Utils\get_flag_value( $assoc_args, 'featured', false ) ) {
            $meta_query[] = [ 'key' => '_acme_project_featured', 'value' => '1' ];
        }

        if ( $meta_query ) {
            $meta_query['relation']    = 'AND';
            $query_args['meta_query'] = $meta_query;
        }

        $query = new \WP_Query( $query_args );
        if ( ! $query->have_posts() ) {
            WP_CLI::warning( 'No projects found.' );
            return;
        }

        $items = array_map( fn( $p ) => [
            'ID'       => $p->ID,
            'Title'    => $p->post_title,
            'Status'   => get_post_meta( $p->ID, '_acme_project_status', true ) ?: 'planning',
            'Budget'   => get_post_meta( $p->ID, '_acme_project_budget', true ) ?: '0',
            'Featured' => get_post_meta( $p->ID, '_acme_project_featured', true ) ? 'Yes' : 'No',
        ], $query->posts );

        Utils\format_items(
            Utils\get_flag_value( $assoc_args, 'format', 'table' ),
            $items,
            [ 'ID', 'Title', 'Status', 'Budget', 'Featured' ]
        );
    }

    /**
     * Clear project caches.
     *
     * ## EXAMPLES
     *
     *     wp acme project clear-cache
     */
    public function clear_cache( array $args, array $assoc_args ): void {
        delete_transient( 'acme_featured_projects' );
        delete_transient( 'acme_project_stats' );
        WP_CLI::success( 'Project caches cleared.' );
    }
}
```

**Register the command:**

```php
if ( defined( 'WP_CLI' ) && WP_CLI ) {
    \WP_CLI::add_command( 'acme project', CLI\ProjectCommand::class, [
        'shortdesc'     => 'Manage Acme Plugin projects.',
        'before_invoke' => function (): void {
            if ( ! post_type_exists( 'acme_project' ) ) {
                ( new Core\PostTypes() )->register();
            }
        },
    ] );
}
```

---

## Best Practices Summary

**Escaping and Sanitization**: `esc_html()` for text, `esc_attr()` for attributes, `esc_url()` for URLs, `wp_kses_post()` for rich HTML. Sanitize input with `sanitize_text_field()`, `absint()`, `sanitize_email()`. Always `wp_unslash()` before sanitizing `$_POST`/`$_GET`.

**Hook Discipline**: Always specify priority when ordering matters. Always specify accepted arg count when callback takes >1 param. Prefix custom hooks with plugin slug. Register post types on `init`, never `plugins_loaded`.

**Performance**: `no_found_rows => true` when pagination is not needed. Cache with transients + invalidate on `save_post`/`delete_post`. Use `update_post_meta_cache => false` and `update_post_term_cache => false` when meta/terms are not needed. Never query in loops.

**Architecture**: PSR-4 via Composer. Namespaced classes under `src/` with Admin/Public/Core separation. Activation/deactivation hooks in main file only. Never delete data on deactivation -- use `uninstall.php`. Guard every PHP file with `if ( ! defined( 'ABSPATH' ) ) { exit; }`.

**Blocks**: Always use `block.json`. Prefer `render` file over `render_callback`. Use `get_block_wrapper_attributes()` for automatic style application. Set `html: false` in supports for dynamic blocks.

**Security**: Verify nonces on every form/AJAX request. Check capabilities before privileged operations. Use `$wpdb->prepare()` for all raw queries. Type-cast IDs with `absint()`.
