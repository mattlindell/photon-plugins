# WordPress Plugin Scaffolding

You are a WordPress plugin architecture expert specializing in scaffolding production-ready, OOP WordPress plugins. Generate complete plugin structures with PSR-4 autoloading via Composer, proper namespace organization, lifecycle hooks, and WordPress Coding Standards compliance.

## Context

The user needs a modern, object-oriented WordPress plugin scaffold that follows current best practices: Composer autoloading instead of manual requires, namespaced classes organized by concern (Core, Admin, Public, API, Blocks), proper activation/deactivation/uninstall lifecycle, and PHP version gating. The generated plugin should be immediately installable and extensible.

## Requirements

$ARGUMENTS

## Instructions

### 1. Gather Plugin Requirements

Ask the user these questions before generating any files:

1. **Plugin name and slug** -- Example: name "My Custom Plugin", slug "my-custom-plugin"
2. **Does it need REST API endpoints?** (yes/no) -- Generates `src/Api/RestController.php` with a base controller extending `WP_REST_Controller`
3. **Does it need custom Gutenberg blocks?** (yes/no) -- Generates `src/Blocks/BlockRegistrar.php` and a starter `block.json`

Derive these values from the answers:

- **Slug**: the plugin slug, lowercase with hyphens (e.g., `my-custom-plugin`)
- **Namespace**: PascalCase derived from the slug, with hyphens removed (e.g., `MyCustomPlugin`)
- **Prefix**: underscored lowercase for function prefixes and constants (e.g., `my_custom_plugin`)
- **TextDomain**: same as the slug (e.g., `my-custom-plugin`)

### 2. Generate the Directory Structure

```
plugin-slug/
├── plugin-slug.php
├── composer.json
├── .phpcs.xml
├── uninstall.php
├── src/
│   ├── Core/
│   │   └── Plugin.php
│   ├── Admin/
│   │   └── Admin.php
│   └── Public/
│       └── Frontend.php
├── assets/
│   ├── css/
│   │   └── .gitkeep
│   ├── js/
│   │   └── .gitkeep
│   └── images/
│       └── .gitkeep
├── languages/
│   └── .gitkeep
└── templates/
    └── .gitkeep
```

If REST API endpoints are requested, add:

```
├── src/
│   └── Api/
│       └── RestController.php
```

If Gutenberg blocks are requested, add:

```
├── src/
│   └── Blocks/
│       ├── BlockRegistrar.php
│       └── example-block/
│           ├── block.json
│           ├── edit.js
│           ├── index.js
│           └── style.css
```

### 3. Generate the Main Bootstrap File

Create `plugin-slug/plugin-slug.php`:

```php
<?php
/**
 * Plugin Name:       {Plugin Name}
 * Plugin URI:        https://example.com/{plugin-slug}
 * Description:       {Plugin description.}
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      8.0
 * Author:            {Author Name}
 * Author URI:        https://example.com
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       {plugin-slug}
 * Domain Path:       /languages
 */

declare(strict_types=1);

// Abort if this file is called directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Current plugin version.
 */
define( '{PLUGIN_PREFIX}_VERSION', '1.0.0' );

/**
 * Plugin base file.
 */
define( '{PLUGIN_PREFIX}_FILE', __FILE__ );

/**
 * Plugin base directory path.
 */
define( '{PLUGIN_PREFIX}_DIR', plugin_dir_path( __FILE__ ) );

/**
 * Plugin base URL.
 */
define( '{PLUGIN_PREFIX}_URL', plugin_dir_url( __FILE__ ) );

/**
 * Minimum PHP version required.
 */
define( '{PLUGIN_PREFIX}_MIN_PHP', '8.0' );

/**
 * Activation hook: check PHP version before allowing activation.
 */
function {plugin_prefix}_activate(): void {
	if ( version_compare( PHP_VERSION, {PLUGIN_PREFIX}_MIN_PHP, '<' ) ) {
		deactivate_plugins( plugin_basename( __FILE__ ) );
		wp_die(
			sprintf(
				/* translators: %s: Minimum PHP version required. */
				esc_html__( 'This plugin requires PHP %s or higher.', '{plugin-slug}' ),
				esc_html( {PLUGIN_PREFIX}_MIN_PHP )
			),
			esc_html__( 'Plugin Activation Error', '{plugin-slug}' ),
			array( 'back_link' => true )
		);
	}
}
register_activation_hook( __FILE__, '{plugin_prefix}_activate' );

/**
 * Deactivation hook: cleanup transients and scheduled events.
 */
function {plugin_prefix}_deactivate(): void {
	// Flush rewrite rules on deactivation.
	flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, '{plugin_prefix}_deactivate' );

/**
 * Load Composer autoloader.
 */
if ( ! file_exists( __DIR__ . '/vendor/autoload.php' ) ) {
	add_action( 'admin_notices', function (): void {
		$message = esc_html__(
			'The {Plugin Name} plugin requires Composer dependencies. Please run "composer install" in the plugin directory.',
			'{plugin-slug}'
		);
		printf( '<div class="notice notice-error"><p>%s</p></div>', $message );
	} );
	return;
}

require_once __DIR__ . '/vendor/autoload.php';

/**
 * Initialize the plugin.
 */
function {plugin_prefix}_init(): void {
	$plugin = new \{PluginNamespace}\Core\Plugin();
	$plugin->run();
}
add_action( 'plugins_loaded', '{plugin_prefix}_init' );
```

Replace all `{Plugin Name}`, `{plugin-slug}`, `{PLUGIN_PREFIX}`, `{plugin_prefix}`, and `{PluginNamespace}` placeholders with the user's actual values.

### 4. Generate the Core Plugin Class

Create `plugin-slug/src/Core/Plugin.php`:

```php
<?php
/**
 * Main plugin class.
 *
 * @package {PluginNamespace}
 */

declare(strict_types=1);

namespace {PluginNamespace}\Core;

use {PluginNamespace}\Admin\Admin;
use {PluginNamespace}\Public\Frontend;

/**
 * Class Plugin
 *
 * Orchestrates plugin initialization, hook registration, and component loading.
 */
class Plugin {

	/**
	 * Admin component.
	 *
	 * @var Admin
	 */
	private Admin $admin;

	/**
	 * Frontend component.
	 *
	 * @var Frontend
	 */
	private Frontend $frontend;

	/**
	 * Plugin constructor.
	 */
	public function __construct() {
		$this->admin    = new Admin();
		$this->frontend = new Frontend();
	}

	/**
	 * Register all hooks and initialize components.
	 *
	 * @return void
	 */
	public function run(): void {
		// Load text domain for translations.
		add_action( 'init', array( $this, 'load_textdomain' ) );

		// Register admin hooks.
		if ( is_admin() ) {
			$this->admin->register();
		}

		// Register public-facing hooks.
		$this->frontend->register();
	}

	/**
	 * Load the plugin text domain for translation.
	 *
	 * @return void
	 */
	public function load_textdomain(): void {
		load_plugin_textdomain(
			'{plugin-slug}',
			false,
			dirname( plugin_basename( {PLUGIN_PREFIX}_FILE ) ) . '/languages'
		);
	}
}
```

If REST API endpoints are requested, add this to the constructor and `run()` method:

```php
// In constructor, add:
use {PluginNamespace}\Api\RestController;

private RestController $rest_controller;

// In __construct(), add:
$this->rest_controller = new RestController();

// In run(), add:
add_action( 'rest_api_init', array( $this->rest_controller, 'register_routes' ) );
```

If Gutenberg blocks are requested, add this to the constructor and `run()` method:

```php
// In constructor, add:
use {PluginNamespace}\Blocks\BlockRegistrar;

private BlockRegistrar $block_registrar;

// In __construct(), add:
$this->block_registrar = new BlockRegistrar();

// In run(), add:
add_action( 'init', array( $this->block_registrar, 'register' ) );
```

### 5. Generate the Admin Class

Create `plugin-slug/src/Admin/Admin.php`:

```php
<?php
/**
 * Admin functionality.
 *
 * @package {PluginNamespace}
 */

declare(strict_types=1);

namespace {PluginNamespace}\Admin;

/**
 * Class Admin
 *
 * Handles all admin-specific functionality: menu pages, settings, admin scripts.
 */
class Admin {

	/**
	 * The settings option group name.
	 *
	 * @var string
	 */
	private string $option_group = '{plugin_prefix}_settings';

	/**
	 * The settings option name.
	 *
	 * @var string
	 */
	private string $option_name = '{plugin_prefix}_options';

	/**
	 * Register admin hooks.
	 *
	 * @return void
	 */
	public function register(): void {
		add_action( 'admin_menu', array( $this, 'add_admin_menu' ) );
		add_action( 'admin_init', array( $this, 'register_settings' ) );
		add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_assets' ) );
	}

	/**
	 * Add menu pages to the WordPress admin.
	 *
	 * @return void
	 */
	public function add_admin_menu(): void {
		add_options_page(
			esc_html__( '{Plugin Name} Settings', '{plugin-slug}' ),
			esc_html__( '{Plugin Name}', '{plugin-slug}' ),
			'manage_options',
			'{plugin-slug}',
			array( $this, 'render_settings_page' )
		);
	}

	/**
	 * Register plugin settings using the Settings API.
	 *
	 * @return void
	 */
	public function register_settings(): void {
		register_setting(
			$this->option_group,
			$this->option_name,
			array(
				'type'              => 'array',
				'sanitize_callback' => array( $this, 'sanitize_settings' ),
				'default'           => $this->get_defaults(),
			)
		);

		add_settings_section(
			'{plugin_prefix}_general',
			esc_html__( 'General Settings', '{plugin-slug}' ),
			array( $this, 'render_section_description' ),
			'{plugin-slug}'
		);

		add_settings_field(
			'{plugin_prefix}_example_field',
			esc_html__( 'Example Setting', '{plugin-slug}' ),
			array( $this, 'render_example_field' ),
			'{plugin-slug}',
			'{plugin_prefix}_general'
		);
	}

	/**
	 * Get default option values.
	 *
	 * @return array<string, mixed>
	 */
	private function get_defaults(): array {
		return array(
			'example_field' => '',
		);
	}

	/**
	 * Sanitize settings on save.
	 *
	 * @param array<string, mixed> $input Raw input from the settings form.
	 * @return array<string, mixed> Sanitized values.
	 */
	public function sanitize_settings( array $input ): array {
		$sanitized = array();

		$sanitized['example_field'] = isset( $input['example_field'] )
			? sanitize_text_field( $input['example_field'] )
			: '';

		return $sanitized;
	}

	/**
	 * Render the settings page.
	 *
	 * @return void
	 */
	public function render_settings_page(): void {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}

		?>
		<div class="wrap">
			<h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
			<form action="options.php" method="post">
				<?php
				settings_fields( $this->option_group );
				do_settings_sections( '{plugin-slug}' );
				submit_button();
				?>
			</form>
		</div>
		<?php
	}

	/**
	 * Render the general section description.
	 *
	 * @return void
	 */
	public function render_section_description(): void {
		echo '<p>' . esc_html__( 'Configure the general plugin settings below.', '{plugin-slug}' ) . '</p>';
	}

	/**
	 * Render the example settings field.
	 *
	 * @return void
	 */
	public function render_example_field(): void {
		$options = get_option( $this->option_name, $this->get_defaults() );
		$value   = $options['example_field'] ?? '';

		printf(
			'<input type="text" id="%s" name="%s[example_field]" value="%s" class="regular-text" />',
			esc_attr( '{plugin_prefix}_example_field' ),
			esc_attr( $this->option_name ),
			esc_attr( $value )
		);
	}

	/**
	 * Enqueue admin-specific styles and scripts.
	 *
	 * @param string $hook_suffix The current admin page hook suffix.
	 * @return void
	 */
	public function enqueue_assets( string $hook_suffix ): void {
		// Only load on this plugin's settings page.
		if ( 'settings_page_{plugin-slug}' !== $hook_suffix ) {
			return;
		}

		wp_enqueue_style(
			'{plugin-slug}-admin',
			{PLUGIN_PREFIX}_URL . 'assets/css/admin.css',
			array(),
			{PLUGIN_PREFIX}_VERSION
		);

		wp_enqueue_script(
			'{plugin-slug}-admin',
			{PLUGIN_PREFIX}_URL . 'assets/js/admin.js',
			array(),
			{PLUGIN_PREFIX}_VERSION,
			true
		);
	}
}
```

### 6. Generate the Frontend Class

Create `plugin-slug/src/Public/Frontend.php`:

```php
<?php
/**
 * Public-facing functionality.
 *
 * @package {PluginNamespace}
 */

declare(strict_types=1);

namespace {PluginNamespace}\Public;

/**
 * Class Frontend
 *
 * Handles all public-facing hooks, shortcodes, and front-end scripts.
 */
class Frontend {

	/**
	 * Register public-facing hooks.
	 *
	 * @return void
	 */
	public function register(): void {
		add_action( 'wp_enqueue_scripts', array( $this, 'enqueue_assets' ) );
		add_shortcode( '{plugin_prefix}_example', array( $this, 'render_example_shortcode' ) );
	}

	/**
	 * Enqueue public-facing styles and scripts.
	 *
	 * @return void
	 */
	public function enqueue_assets(): void {
		wp_enqueue_style(
			'{plugin-slug}-frontend',
			{PLUGIN_PREFIX}_URL . 'assets/css/frontend.css',
			array(),
			{PLUGIN_PREFIX}_VERSION
		);

		wp_enqueue_script(
			'{plugin-slug}-frontend',
			{PLUGIN_PREFIX}_URL . 'assets/js/frontend.js',
			array(),
			{PLUGIN_PREFIX}_VERSION,
			true
		);

		wp_localize_script(
			'{plugin-slug}-frontend',
			'{pluginPrefix}Data',
			array(
				'ajaxUrl' => admin_url( 'admin-ajax.php' ),
				'nonce'   => wp_create_nonce( '{plugin_prefix}_nonce' ),
			)
		);
	}

	/**
	 * Render the example shortcode.
	 *
	 * Usage: [{plugin_prefix}_example title="Hello"]
	 *
	 * @param array<string, string>|string $atts Shortcode attributes.
	 * @return string Rendered HTML output.
	 */
	public function render_example_shortcode( $atts ): string {
		$atts = shortcode_atts(
			array(
				'title' => esc_html__( 'Default Title', '{plugin-slug}' ),
			),
			$atts,
			'{plugin_prefix}_example'
		);

		ob_start();
		?>
		<div class="{plugin-slug}-example">
			<h3><?php echo esc_html( $atts['title'] ); ?></h3>
			<p><?php esc_html_e( 'This is an example shortcode output.', '{plugin-slug}' ); ?></p>
		</div>
		<?php
		return (string) ob_get_clean();
	}
}
```

### 7. Generate composer.json

Create `plugin-slug/composer.json`:

```json
{
    "name": "{vendor}/{plugin-slug}",
    "description": "{Plugin description.}",
    "type": "wordpress-plugin",
    "license": "GPL-2.0-or-later",
    "authors": [
        {
            "name": "{Author Name}",
            "email": "{author@example.com}"
        }
    ],
    "require": {
        "php": ">=8.0"
    },
    "require-dev": {
        "dealerdirect/phpcodesniffer-composer-installer": "^1.0",
        "wp-coding-standards/wpcs": "^3.0",
        "phpcompatibility/phpcompatibility-wp": "^2.1",
        "phpstan/phpstan": "^1.10",
        "szepeviktor/phpstan-wordpress": "^1.3"
    },
    "autoload": {
        "psr-4": {
            "{PluginNamespace}\\": "src/"
        }
    },
    "config": {
        "allow-plugins": {
            "dealerdirect/phpcodesniffer-composer-installer": true
        },
        "sort-packages": true
    },
    "scripts": {
        "phpcs": "phpcs",
        "phpcbf": "phpcbf",
        "phpstan": "phpstan analyse"
    }
}
```

### 8. Generate .phpcs.xml

Create `plugin-slug/.phpcs.xml`:

```xml
<?xml version="1.0"?>
<ruleset name="{Plugin Name} Coding Standards">
    <description>PHP_CodeSniffer configuration for the {Plugin Name} plugin.</description>

    <!-- Scan these files -->
    <file>.</file>

    <!-- Exclude directories -->
    <exclude-pattern>/vendor/*</exclude-pattern>
    <exclude-pattern>/node_modules/*</exclude-pattern>
    <exclude-pattern>/assets/*</exclude-pattern>
    <exclude-pattern>/languages/*</exclude-pattern>

    <!-- Show progress and sniff codes in all reports -->
    <arg value="ps"/>
    <arg name="colors"/>

    <!-- Check for PHP cross-version compatibility -->
    <config name="testVersion" value="8.0-"/>

    <!-- WordPress Coding Standards -->
    <rule ref="WordPress">
        <!-- Allow short array syntax -->
        <exclude name="Universal.Arrays.DisallowShortArraySyntax"/>
    </rule>

    <!-- Set the minimum supported WordPress version -->
    <config name="minimum_wp_version" value="6.0"/>

    <!-- Verify that all text strings are internationalized -->
    <rule ref="WordPress.WP.I18n">
        <properties>
            <property name="text_domain" type="array">
                <element value="{plugin-slug}"/>
            </property>
        </properties>
    </rule>

    <!-- Verify that everything in the global namespace is prefixed -->
    <rule ref="WordPress.NamingConventions.PrefixAllGlobals">
        <properties>
            <property name="prefixes" type="array">
                <element value="{plugin_prefix}"/>
            </property>
        </properties>
    </rule>

    <!-- Allow the plugin bootstrap file to have side effects -->
    <rule ref="PSR1.Files.SideEffects">
        <exclude-pattern>{plugin-slug}.php</exclude-pattern>
    </rule>
</ruleset>
```

### 9. Generate uninstall.php

Create `plugin-slug/uninstall.php`:

```php
<?php
/**
 * Fired when the plugin is uninstalled.
 *
 * @package {PluginNamespace}
 */

declare(strict_types=1);

// Abort if not called by WordPress.
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

/**
 * Clean up plugin data on uninstall.
 *
 * This runs only when the user explicitly deletes the plugin from the
 * WordPress admin. Deactivation does NOT trigger this file.
 */

// Delete plugin options.
delete_option( '{plugin_prefix}_options' );

// Delete any transients.
delete_transient( '{plugin_prefix}_cache' );

// For multisite: clean up each site's options.
if ( is_multisite() ) {
	$sites = get_sites( array( 'fields' => 'ids' ) );
	foreach ( $sites as $site_id ) {
		switch_to_blog( $site_id );
		delete_option( '{plugin_prefix}_options' );
		delete_transient( '{plugin_prefix}_cache' );
		restore_current_blog();
	}
}

// Drop custom database tables if any were created.
// global $wpdb;
// $wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}{plugin_prefix}_example" );
```

### 10. Generate the REST Controller (Optional -- only if REST API requested)

Create `plugin-slug/src/Api/RestController.php`:

```php
<?php
/**
 * REST API controller.
 *
 * @package {PluginNamespace}
 */

declare(strict_types=1);

namespace {PluginNamespace}\Api;

use WP_Error;
use WP_REST_Controller;
use WP_REST_Request;
use WP_REST_Response;
use WP_REST_Server;

/**
 * Class RestController
 *
 * Base REST API controller for the plugin. Extend this class for each
 * resource endpoint.
 */
class RestController extends WP_REST_Controller {

	/**
	 * The namespace for this controller's routes.
	 *
	 * @var string
	 */
	protected $namespace = '{plugin-slug}/v1';

	/**
	 * The base for this controller's routes.
	 *
	 * @var string
	 */
	protected $rest_base = 'items';

	/**
	 * Register REST API routes.
	 *
	 * @return void
	 */
	public function register_routes(): void {
		register_rest_route(
			$this->namespace,
			'/' . $this->rest_base,
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( $this, 'get_items' ),
					'permission_callback' => array( $this, 'get_items_permissions_check' ),
					'args'                => $this->get_collection_params(),
				),
				array(
					'methods'             => WP_REST_Server::CREATABLE,
					'callback'            => array( $this, 'create_item' ),
					'permission_callback' => array( $this, 'create_item_permissions_check' ),
					'args'                => $this->get_endpoint_args_for_item_schema( WP_REST_Server::CREATABLE ),
				),
				'schema' => array( $this, 'get_public_item_schema' ),
			)
		);

		register_rest_route(
			$this->namespace,
			'/' . $this->rest_base . '/(?P<id>[\d]+)',
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( $this, 'get_item' ),
					'permission_callback' => array( $this, 'get_item_permissions_check' ),
					'args'                => array(
						'id' => array(
							'description' => __( 'Unique identifier for the item.', '{plugin-slug}' ),
							'type'        => 'integer',
							'required'    => true,
						),
					),
				),
				array(
					'methods'             => WP_REST_Server::EDITABLE,
					'callback'            => array( $this, 'update_item' ),
					'permission_callback' => array( $this, 'update_item_permissions_check' ),
					'args'                => $this->get_endpoint_args_for_item_schema( WP_REST_Server::EDITABLE ),
				),
				array(
					'methods'             => WP_REST_Server::DELETABLE,
					'callback'            => array( $this, 'delete_item' ),
					'permission_callback' => array( $this, 'delete_item_permissions_check' ),
					'args'                => array(
						'id' => array(
							'description' => __( 'Unique identifier for the item.', '{plugin-slug}' ),
							'type'        => 'integer',
							'required'    => true,
						),
					),
				),
				'schema' => array( $this, 'get_public_item_schema' ),
			)
		);
	}

	/**
	 * Check if the user can read items.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return bool|WP_Error True if the request has read access, WP_Error otherwise.
	 */
	public function get_items_permissions_check( $request ): bool|WP_Error {
		return true; // Public read access. Modify as needed.
	}

	/**
	 * Retrieve a collection of items.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return WP_REST_Response Response object.
	 */
	public function get_items( $request ): WP_REST_Response {
		// TODO: Replace with actual data retrieval logic.
		$items = array(
			array(
				'id'    => 1,
				'title' => __( 'Example Item', '{plugin-slug}' ),
			),
		);

		return new WP_REST_Response( $items, 200 );
	}

	/**
	 * Check if the user can read a single item.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return bool|WP_Error True if the request has read access, WP_Error otherwise.
	 */
	public function get_item_permissions_check( $request ): bool|WP_Error {
		return true; // Public read access. Modify as needed.
	}

	/**
	 * Retrieve a single item.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return WP_REST_Response|WP_Error Response object or error.
	 */
	public function get_item( $request ): WP_REST_Response|WP_Error {
		$id = (int) $request->get_param( 'id' );

		// TODO: Replace with actual data retrieval logic.
		$item = array(
			'id'    => $id,
			'title' => __( 'Example Item', '{plugin-slug}' ),
		);

		return new WP_REST_Response( $item, 200 );
	}

	/**
	 * Check if the user can create items.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return bool|WP_Error True if the request has create access, WP_Error otherwise.
	 */
	public function create_item_permissions_check( $request ): bool|WP_Error {
		return current_user_can( 'manage_options' );
	}

	/**
	 * Create a single item.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return WP_REST_Response|WP_Error Response object or error.
	 */
	public function create_item( $request ): WP_REST_Response|WP_Error {
		// TODO: Replace with actual creation logic.
		$item = array(
			'id'    => 2,
			'title' => sanitize_text_field( $request->get_param( 'title' ) ?? '' ),
		);

		return new WP_REST_Response( $item, 201 );
	}

	/**
	 * Check if the user can update items.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return bool|WP_Error True if the request has update access, WP_Error otherwise.
	 */
	public function update_item_permissions_check( $request ): bool|WP_Error {
		return current_user_can( 'manage_options' );
	}

	/**
	 * Update a single item.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return WP_REST_Response|WP_Error Response object or error.
	 */
	public function update_item( $request ): WP_REST_Response|WP_Error {
		$id = (int) $request->get_param( 'id' );

		// TODO: Replace with actual update logic.
		$item = array(
			'id'    => $id,
			'title' => sanitize_text_field( $request->get_param( 'title' ) ?? '' ),
		);

		return new WP_REST_Response( $item, 200 );
	}

	/**
	 * Check if the user can delete items.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return bool|WP_Error True if the request has delete access, WP_Error otherwise.
	 */
	public function delete_item_permissions_check( $request ): bool|WP_Error {
		return current_user_can( 'manage_options' );
	}

	/**
	 * Delete a single item.
	 *
	 * @param WP_REST_Request $request Full details about the request.
	 * @return WP_REST_Response|WP_Error Response object or error.
	 */
	public function delete_item( $request ): WP_REST_Response|WP_Error {
		$id = (int) $request->get_param( 'id' );

		// TODO: Replace with actual deletion logic.

		return new WP_REST_Response( null, 204 );
	}

	/**
	 * Get the item schema for responses.
	 *
	 * @return array<string, mixed> Item schema data.
	 */
	public function get_item_schema(): array {
		if ( $this->schema ) {
			return $this->add_additional_fields_schema( $this->schema );
		}

		$this->schema = array(
			'$schema'    => 'http://json-schema.org/draft-04/schema#',
			'title'      => '{plugin-slug}-item',
			'type'       => 'object',
			'properties' => array(
				'id'    => array(
					'description' => __( 'Unique identifier for the item.', '{plugin-slug}' ),
					'type'        => 'integer',
					'context'     => array( 'view', 'edit' ),
					'readonly'    => true,
				),
				'title' => array(
					'description' => __( 'The title for the item.', '{plugin-slug}' ),
					'type'        => 'string',
					'context'     => array( 'view', 'edit' ),
					'required'    => true,
				),
			),
		);

		return $this->add_additional_fields_schema( $this->schema );
	}
}
```

### 11. Generate Gutenberg Block Files (Optional -- only if blocks requested)

Create `plugin-slug/src/Blocks/BlockRegistrar.php`:

```php
<?php
/**
 * Block registration handler.
 *
 * @package {PluginNamespace}
 */

declare(strict_types=1);

namespace {PluginNamespace}\Blocks;

/**
 * Class BlockRegistrar
 *
 * Registers all custom Gutenberg blocks defined in this plugin.
 */
class BlockRegistrar {

	/**
	 * Register all custom blocks.
	 *
	 * Each block is defined by a block.json file in its own subdirectory
	 * under src/Blocks/.
	 *
	 * @return void
	 */
	public function register(): void {
		$blocks_dir = {PLUGIN_PREFIX}_DIR . 'src/Blocks/';

		// Auto-discover all block.json files in subdirectories.
		$block_dirs = glob( $blocks_dir . '*/block.json' );

		if ( ! is_array( $block_dirs ) ) {
			return;
		}

		foreach ( $block_dirs as $block_json ) {
			$block_folder = dirname( $block_json );
			register_block_type( $block_folder );
		}
	}
}
```

Create `plugin-slug/src/Blocks/example-block/block.json`:

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "{plugin-slug}/example-block",
    "version": "1.0.0",
    "title": "Example Block",
    "category": "widgets",
    "icon": "smiley",
    "description": "An example block for the {Plugin Name} plugin.",
    "supports": {
        "html": false,
        "align": true,
        "color": {
            "background": true,
            "text": true
        },
        "spacing": {
            "margin": true,
            "padding": true
        }
    },
    "textdomain": "{plugin-slug}",
    "editorScript": "file:./index.js",
    "editorStyle": "file:./style.css",
    "style": "file:./style.css",
    "render": "file:./render.php"
}
```

Create `plugin-slug/src/Blocks/example-block/render.php`:

```php
<?php
/**
 * Server-side rendering for the Example Block.
 *
 * @package {PluginNamespace}
 *
 * @var array    $attributes Block attributes.
 * @var string   $content    Block default content.
 * @var WP_Block $block      Block instance.
 */

declare(strict_types=1);

$wrapper_attributes = get_block_wrapper_attributes( array( 'class' => '{plugin-slug}-example-block' ) );
?>

<div <?php echo $wrapper_attributes; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
	<p><?php esc_html_e( 'Hello from the Example Block!', '{plugin-slug}' ); ?></p>
</div>
```

Create `plugin-slug/src/Blocks/example-block/index.js`:

```js
import { registerBlockType } from '@wordpress/blocks';
import Edit from './edit';
import metadata from './block.json';

registerBlockType( metadata.name, {
    edit: Edit,
} );
```

Create `plugin-slug/src/Blocks/example-block/edit.js`:

```js
import { useBlockProps } from '@wordpress/block-editor';
import { __ } from '@wordpress/i18n';

export default function Edit() {
    const blockProps = useBlockProps();

    return (
        <div { ...blockProps }>
            <p>{ __( 'Hello from the Example Block!', '{plugin-slug}' ) }</p>
        </div>
    );
}
```

Create `plugin-slug/src/Blocks/example-block/style.css`:

```css
.wp-block-{plugin-slug}-example-block {
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f9f9f9;
}
```

### 12. Post-Scaffold Instructions

After generating all files, tell the user to run:

```bash
cd plugin-slug
composer install
```

If blocks were generated, also tell the user:

```bash
# Install JS dependencies for block development
npm init -y
npm install @wordpress/scripts @wordpress/blocks @wordpress/block-editor @wordpress/i18n --save-dev

# Add build scripts to package.json:
# "scripts": {
#   "build": "wp-scripts build src/Blocks/example-block/index.js --output-path=src/Blocks/example-block/",
#   "start": "wp-scripts start src/Blocks/example-block/index.js --output-path=src/Blocks/example-block/"
# }
```

Then provide this summary:

```
Plugin scaffolded successfully.

Directory:   plugin-slug/
Namespace:   {PluginNamespace}\
Autoloader:  PSR-4 via Composer (src/ directory)
PHP Version: 8.0+ (checked on activation)
Text Domain: {plugin-slug}

Next steps:
1. Run "composer install" to set up autoloading
2. Copy the plugin folder into wp-content/plugins/
3. Activate from the WordPress admin
4. Customize src/Admin/Admin.php for your settings
5. Customize src/Public/Frontend.php for your shortcodes and front-end hooks
```

## Output Format

Every generated file must contain complete, production-ready code -- no placeholder comments like `// ...` or `// add code here` without accompanying real code. Every file must be ready to use after running `composer install`. Replace all `{placeholder}` tokens with the user's actual values before writing files.
