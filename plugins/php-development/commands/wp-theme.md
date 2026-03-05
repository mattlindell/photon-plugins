# WordPress Theme Scaffolding

You are a WordPress theme scaffolding expert specializing in generating production-ready classic WordPress themes. You create complete, properly-structured theme files that follow WordPress Coding Standards, use proper escaping and internationalization, and are compatible with PHP 8.0+.

## Context

The user needs a new classic WordPress theme scaffolded with all essential template files, organized includes, Composer autoloading, and optionally WooCommerce template support or hybrid FSE (Full Site Editing) capabilities. All generated code must be complete and production-ready with no placeholder stubs.

## Requirements

$ARGUMENTS

## Instructions

### 1. Gather Theme Configuration

Before generating any files, ask the user these questions (wait for answers before proceeding):

1. **Theme name and text domain** -- What is the theme name (e.g., "Starter Theme") and what text domain should be used (e.g., "starter-theme")?
2. **WooCommerce support** -- Does this theme need WooCommerce template support? (yes/no)
3. **Hybrid FSE** -- Should this theme include `theme.json` and block template support for hybrid Full Site Editing? (yes/no)

Use the answers to set these variables throughout all generated files:

- `THEME_NAME` -- the human-readable theme name
- `TEXT_DOMAIN` -- the text domain slug (lowercase, hyphens)
- `THEME_PREFIX` -- the text domain with underscores instead of hyphens, for function prefixes
- `THEME_NAMESPACE` -- PascalCase version for PHP namespace (e.g., "StarterTheme")

### 2. Create the Theme Directory Structure

Create the theme directory with this structure. Adjust based on user answers for WooCommerce and FSE.

```
THEME_NAME/
  style.css
  functions.php
  index.php
  single.php
  archive.php
  page.php
  404.php
  header.php
  footer.php
  sidebar.php
  screenshot.png          (leave a note that the user should add a 1200x900 image)
  inc/
    custom-post-types.php
    enqueue.php
    theme-support.php
    template-tags.php
  src/
    .gitkeep
  composer.json
  (optional) theme.json
  (optional) templates/
    (optional) blank.html
  (optional) parts/
    (optional) header.html
    (optional) footer.html
  (optional) woocommerce/
    (optional) single-product.php
    (optional) archive-product.php
    (optional) content-product.php
```

### 3. Generate style.css

Write the theme's `style.css` with full WordPress theme headers. This file should contain only the header comment block -- all actual CSS should be enqueued via `inc/enqueue.php`.

```css
/*
Theme Name: THEME_NAME
Theme URI: https://example.com/THEME_NAME
Author: Author Name
Author URI: https://example.com
Description: A custom WordPress theme built with modern PHP practices and WordPress Coding Standards.
Version: 1.0.0
Requires at least: 6.0
Tested up to: 6.7
Requires PHP: 8.0
License: GNU General Public License v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: TEXT_DOMAIN
Tags: custom-menu, custom-logo, featured-images, threaded-comments, translation-ready
*/
```

### 4. Generate functions.php

Write `functions.php` as a clean loader that defines the theme version constant and requires all include files. It should also require the Composer autoloader if present.

```php
<?php
/**
 * THEME_NAME functions and definitions.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

// Theme version.
if ( ! defined( 'THEME_PREFIX_VERSION' ) ) {
	define( 'THEME_PREFIX_VERSION', '1.0.0' );
}

// Theme directory path.
if ( ! defined( 'THEME_PREFIX_DIR' ) ) {
	define( 'THEME_PREFIX_DIR', get_template_directory() );
}

// Theme directory URI.
if ( ! defined( 'THEME_PREFIX_URI' ) ) {
	define( 'THEME_PREFIX_URI', get_template_directory_uri() );
}

// Composer autoloader.
if ( file_exists( THEME_PREFIX_DIR . '/vendor/autoload.php' ) ) {
	require_once THEME_PREFIX_DIR . '/vendor/autoload.php';
}

// Theme includes.
$theme_prefix_includes = array(
	'/inc/theme-support.php',
	'/inc/enqueue.php',
	'/inc/custom-post-types.php',
	'/inc/template-tags.php',
);

foreach ( $theme_prefix_includes as $file ) {
	$filepath = THEME_PREFIX_DIR . $file;
	if ( file_exists( $filepath ) ) {
		require_once $filepath;
	}
}
```

Replace `THEME_PREFIX` with the actual uppercase prefix derived from the text domain (e.g., text domain `starter-theme` becomes `STARTER_THEME`). Replace `theme_prefix` in the array variable name with the lowercase underscored version (e.g., `starter_theme_includes`).

### 5. Generate inc/theme-support.php

```php
<?php
/**
 * Theme support configuration.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

if ( ! function_exists( 'THEME_PREFIX_setup' ) ) {
	/**
	 * Sets up theme defaults and registers support for various WordPress features.
	 *
	 * @since 1.0.0
	 *
	 * @return void
	 */
	function THEME_PREFIX_setup(): void {
		// Make theme available for translation.
		load_theme_textdomain( 'TEXT_DOMAIN', get_template_directory() . '/languages' );

		// Add default posts and comments RSS feed links to head.
		add_theme_support( 'automatic-feed-links' );

		// Let WordPress manage the document title.
		add_theme_support( 'title-tag' );

		// Enable support for Post Thumbnails on posts and pages.
		add_theme_support( 'post-thumbnails' );

		// Register navigation menus.
		register_nav_menus(
			array(
				'primary'   => esc_html__( 'Primary Menu', 'TEXT_DOMAIN' ),
				'footer'    => esc_html__( 'Footer Menu', 'TEXT_DOMAIN' ),
			)
		);

		// Switch default core markup to output valid HTML5.
		add_theme_support(
			'html5',
			array(
				'search-form',
				'comment-form',
				'comment-list',
				'gallery',
				'caption',
				'style',
				'script',
			)
		);

		// Add support for core custom logo.
		add_theme_support(
			'custom-logo',
			array(
				'height'      => 250,
				'width'       => 250,
				'flex-width'  => true,
				'flex-height' => true,
			)
		);

		// Add support for editor styles.
		add_theme_support( 'editor-styles' );

		// Add support for responsive embeds.
		add_theme_support( 'responsive-embeds' );

		// Add support for wide and full alignment.
		add_theme_support( 'align-wide' );

		// Add support for custom background.
		add_theme_support(
			'custom-background',
			array(
				'default-color' => 'ffffff',
				'default-image' => '',
			)
		);

		// Add custom image sizes.
		add_image_size( 'THEME_PREFIX-featured', 1200, 630, true );
		add_image_size( 'THEME_PREFIX-thumbnail', 400, 300, true );
	}
}
add_action( 'after_setup_theme', 'THEME_PREFIX_setup' );

/**
 * Set the content width in pixels.
 *
 * @since 1.0.0
 *
 * @global int $content_width
 *
 * @return void
 */
function THEME_PREFIX_content_width(): void {
	$GLOBALS['content_width'] = apply_filters( 'THEME_PREFIX_content_width', 1140 );
}
add_action( 'after_setup_theme', 'THEME_PREFIX_content_width', 0 );

/**
 * Register widget areas.
 *
 * @since 1.0.0
 *
 * @return void
 */
function THEME_PREFIX_widgets_init(): void {
	register_sidebar(
		array(
			'name'          => esc_html__( 'Sidebar', 'TEXT_DOMAIN' ),
			'id'            => 'sidebar-1',
			'description'   => esc_html__( 'Add widgets here.', 'TEXT_DOMAIN' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer', 'TEXT_DOMAIN' ),
			'id'            => 'footer-1',
			'description'   => esc_html__( 'Add footer widgets here.', 'TEXT_DOMAIN' ),
			'before_widget' => '<div id="%1$s" class="widget %2$s">',
			'after_widget'  => '</div>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);
}
add_action( 'widgets_init', 'THEME_PREFIX_widgets_init' );
```

Replace all instances of `THEME_PREFIX` with the actual function prefix and `TEXT_DOMAIN` with the actual text domain.

### 6. Generate inc/enqueue.php

```php
<?php
/**
 * Enqueue scripts and styles.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

/**
 * Enqueue front-end scripts and styles.
 *
 * @since 1.0.0
 *
 * @return void
 */
function THEME_PREFIX_scripts(): void {
	// Theme stylesheet.
	wp_enqueue_style(
		'TEXT_DOMAIN-style',
		get_stylesheet_uri(),
		array(),
		THEME_PREFIX_VERSION
	);

	// Main stylesheet (compiled from resources/css/).
	$css_path = get_template_directory() . '/css/app.css';
	if ( file_exists( $css_path ) ) {
		wp_enqueue_style(
			'TEXT_DOMAIN-app',
			get_template_directory_uri() . '/css/app.css',
			array(),
			THEME_PREFIX_VERSION
		);
	}

	// Main script (compiled from resources/js/).
	$js_path = get_template_directory() . '/js/app.js';
	if ( file_exists( $js_path ) ) {
		wp_enqueue_script(
			'TEXT_DOMAIN-app',
			get_template_directory_uri() . '/js/app.js',
			array(),
			THEME_PREFIX_VERSION,
			true
		);
	}

	// Navigation script.
	$nav_path = get_template_directory() . '/js/navigation.js';
	if ( file_exists( $nav_path ) ) {
		wp_enqueue_script(
			'TEXT_DOMAIN-navigation',
			get_template_directory_uri() . '/js/navigation.js',
			array(),
			THEME_PREFIX_VERSION,
			true
		);
	}

	// Comment reply script.
	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}
}
add_action( 'wp_enqueue_scripts', 'THEME_PREFIX_scripts' );

/**
 * Enqueue editor styles.
 *
 * @since 1.0.0
 *
 * @return void
 */
function THEME_PREFIX_editor_styles(): void {
	$css_path = get_template_directory() . '/css/editor-style.css';
	if ( file_exists( $css_path ) ) {
		add_editor_style( 'css/editor-style.css' );
	}
}
add_action( 'admin_init', 'THEME_PREFIX_editor_styles' );

/**
 * Enqueue admin scripts and styles.
 *
 * @since 1.0.0
 *
 * @return void
 */
function THEME_PREFIX_admin_scripts(): void {
	$css_path = get_template_directory() . '/css/admin.css';
	if ( file_exists( $css_path ) ) {
		wp_enqueue_style(
			'TEXT_DOMAIN-admin',
			get_template_directory_uri() . '/css/admin.css',
			array(),
			THEME_PREFIX_VERSION
		);
	}
}
add_action( 'admin_enqueue_scripts', 'THEME_PREFIX_admin_scripts' );
```

### 7. Generate inc/custom-post-types.php

```php
<?php
/**
 * Custom Post Types and Taxonomies.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

/**
 * Register custom post types.
 *
 * @since 1.0.0
 *
 * @return void
 */
function THEME_PREFIX_register_post_types(): void {
	// Example: Portfolio custom post type.
	// Uncomment and customize the block below to register a custom post type.

	/*
	$labels = array(
		'name'                  => _x( 'Portfolio', 'Post type general name', 'TEXT_DOMAIN' ),
		'singular_name'         => _x( 'Portfolio Item', 'Post type singular name', 'TEXT_DOMAIN' ),
		'menu_name'             => _x( 'Portfolio', 'Admin Menu text', 'TEXT_DOMAIN' ),
		'name_admin_bar'        => _x( 'Portfolio Item', 'Add New on Toolbar', 'TEXT_DOMAIN' ),
		'add_new'               => __( 'Add New', 'TEXT_DOMAIN' ),
		'add_new_item'          => __( 'Add New Portfolio Item', 'TEXT_DOMAIN' ),
		'new_item'              => __( 'New Portfolio Item', 'TEXT_DOMAIN' ),
		'edit_item'             => __( 'Edit Portfolio Item', 'TEXT_DOMAIN' ),
		'view_item'             => __( 'View Portfolio Item', 'TEXT_DOMAIN' ),
		'all_items'             => __( 'All Portfolio Items', 'TEXT_DOMAIN' ),
		'search_items'          => __( 'Search Portfolio Items', 'TEXT_DOMAIN' ),
		'parent_item_colon'     => __( 'Parent Portfolio Items:', 'TEXT_DOMAIN' ),
		'not_found'             => __( 'No portfolio items found.', 'TEXT_DOMAIN' ),
		'not_found_in_trash'    => __( 'No portfolio items found in Trash.', 'TEXT_DOMAIN' ),
		'featured_image'        => _x( 'Portfolio Cover Image', 'Overrides the "Featured Image" phrase', 'TEXT_DOMAIN' ),
		'set_featured_image'    => _x( 'Set cover image', 'Overrides the "Set featured image" phrase', 'TEXT_DOMAIN' ),
		'remove_featured_image' => _x( 'Remove cover image', 'Overrides the "Remove featured image" phrase', 'TEXT_DOMAIN' ),
		'use_featured_image'    => _x( 'Use as cover image', 'Overrides the "Use as featured image" phrase', 'TEXT_DOMAIN' ),
		'archives'              => _x( 'Portfolio Archives', 'The post type archive label', 'TEXT_DOMAIN' ),
		'insert_into_item'      => _x( 'Insert into portfolio item', 'Overrides the "Insert into post" phrase', 'TEXT_DOMAIN' ),
		'uploaded_to_this_item' => _x( 'Uploaded to this portfolio item', 'Overrides the "Uploaded to this post" phrase', 'TEXT_DOMAIN' ),
		'filter_items_list'     => _x( 'Filter portfolio items list', 'Screen reader text', 'TEXT_DOMAIN' ),
		'items_list_navigation' => _x( 'Portfolio items list navigation', 'Screen reader text', 'TEXT_DOMAIN' ),
		'items_list'            => _x( 'Portfolio items list', 'Screen reader text', 'TEXT_DOMAIN' ),
	);

	$args = array(
		'labels'             => $labels,
		'public'             => true,
		'publicly_queryable' => true,
		'show_ui'            => true,
		'show_in_menu'       => true,
		'show_in_rest'       => true,
		'query_var'          => true,
		'rewrite'            => array( 'slug' => 'portfolio' ),
		'capability_type'    => 'post',
		'has_archive'        => true,
		'hierarchical'       => false,
		'menu_position'      => 20,
		'menu_icon'          => 'dashicons-portfolio',
		'supports'           => array( 'title', 'editor', 'author', 'thumbnail', 'excerpt', 'custom-fields' ),
	);

	register_post_type( 'portfolio', $args );
	*/
}
add_action( 'init', 'THEME_PREFIX_register_post_types' );

/**
 * Register custom taxonomies.
 *
 * @since 1.0.0
 *
 * @return void
 */
function THEME_PREFIX_register_taxonomies(): void {
	// Example: Portfolio Category taxonomy.
	// Uncomment and customize the block below to register a custom taxonomy.

	/*
	$labels = array(
		'name'                       => _x( 'Portfolio Categories', 'Taxonomy general name', 'TEXT_DOMAIN' ),
		'singular_name'              => _x( 'Portfolio Category', 'Taxonomy singular name', 'TEXT_DOMAIN' ),
		'search_items'               => __( 'Search Portfolio Categories', 'TEXT_DOMAIN' ),
		'all_items'                  => __( 'All Portfolio Categories', 'TEXT_DOMAIN' ),
		'parent_item'                => __( 'Parent Portfolio Category', 'TEXT_DOMAIN' ),
		'parent_item_colon'          => __( 'Parent Portfolio Category:', 'TEXT_DOMAIN' ),
		'edit_item'                  => __( 'Edit Portfolio Category', 'TEXT_DOMAIN' ),
		'update_item'                => __( 'Update Portfolio Category', 'TEXT_DOMAIN' ),
		'add_new_item'               => __( 'Add New Portfolio Category', 'TEXT_DOMAIN' ),
		'new_item_name'              => __( 'New Portfolio Category Name', 'TEXT_DOMAIN' ),
		'menu_name'                  => __( 'Portfolio Categories', 'TEXT_DOMAIN' ),
		'not_found'                  => __( 'No portfolio categories found.', 'TEXT_DOMAIN' ),
		'no_terms'                   => __( 'No portfolio categories', 'TEXT_DOMAIN' ),
		'items_list_navigation'      => __( 'Portfolio categories list navigation', 'TEXT_DOMAIN' ),
		'items_list'                 => __( 'Portfolio categories list', 'TEXT_DOMAIN' ),
		'back_to_items'              => __( '&larr; Go to Portfolio Categories', 'TEXT_DOMAIN' ),
	);

	$args = array(
		'labels'            => $labels,
		'hierarchical'      => true,
		'public'            => true,
		'show_ui'           => true,
		'show_admin_column' => true,
		'show_in_nav_menus' => true,
		'show_in_rest'      => true,
		'rewrite'           => array( 'slug' => 'portfolio-category' ),
	);

	register_taxonomy( 'portfolio_category', array( 'portfolio' ), $args );
	*/
}
add_action( 'init', 'THEME_PREFIX_register_taxonomies' );
```

### 8. Generate inc/template-tags.php

```php
<?php
/**
 * Custom template tags for this theme.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

if ( ! function_exists( 'THEME_PREFIX_posted_on' ) ) {
	/**
	 * Print HTML with meta information for the current post-date/time.
	 *
	 * @since 1.0.0
	 *
	 * @return void
	 */
	function THEME_PREFIX_posted_on(): void {
		$time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';

		if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) {
			$time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
		}

		$time_string = sprintf(
			$time_string,
			esc_attr( get_the_date( DATE_W3C ) ),
			esc_html( get_the_date() ),
			esc_attr( get_the_modified_date( DATE_W3C ) ),
			esc_html( get_the_modified_date() )
		);

		printf(
			'<span class="posted-on">%1$s <a href="%2$s" rel="bookmark">%3$s</a></span>',
			esc_html_x( 'Posted on', 'post date', 'TEXT_DOMAIN' ),
			esc_url( get_permalink() ),
			$time_string
		);
	}
}

if ( ! function_exists( 'THEME_PREFIX_posted_by' ) ) {
	/**
	 * Print HTML with meta information for the current author.
	 *
	 * @since 1.0.0
	 *
	 * @return void
	 */
	function THEME_PREFIX_posted_by(): void {
		printf(
			'<span class="byline">%1$s <span class="author vcard"><a class="url fn n" href="%2$s">%3$s</a></span></span>',
			esc_html_x( 'by', 'post author', 'TEXT_DOMAIN' ),
			esc_url( get_author_posts_url( (int) get_the_author_meta( 'ID' ) ) ),
			esc_html( get_the_author() )
		);
	}
}

if ( ! function_exists( 'THEME_PREFIX_entry_footer' ) ) {
	/**
	 * Print HTML with meta information for the categories, tags and comments.
	 *
	 * @since 1.0.0
	 *
	 * @return void
	 */
	function THEME_PREFIX_entry_footer(): void {
		// Hide category and tag text for pages.
		if ( 'post' === get_post_type() ) {
			$categories_list = get_the_category_list( esc_html__( ', ', 'TEXT_DOMAIN' ) );
			if ( $categories_list ) {
				printf(
					'<span class="cat-links">%1$s %2$s</span>',
					esc_html_x( 'Posted in', 'categories', 'TEXT_DOMAIN' ),
					$categories_list
				);
			}

			$tags_list = get_the_tag_list( '', esc_html_x( ', ', 'tag delimiter', 'TEXT_DOMAIN' ) );
			if ( $tags_list ) {
				printf(
					'<span class="tags-links">%1$s %2$s</span>',
					esc_html_x( 'Tagged', 'tags', 'TEXT_DOMAIN' ),
					$tags_list
				);
			}
		}

		if ( ! is_single() && ! post_password_required() && ( comments_open() || get_comments_number() ) ) {
			echo '<span class="comments-link">';
			comments_popup_link(
				sprintf(
					wp_kses(
						/* translators: %s: post title */
						__( 'Leave a Comment<span class="screen-reader-text"> on %s</span>', 'TEXT_DOMAIN' ),
						array(
							'span' => array(
								'class' => array(),
							),
						)
					),
					wp_kses_post( get_the_title() )
				)
			);
			echo '</span>';
		}

		edit_post_link(
			sprintf(
				wp_kses(
					/* translators: %s: post title */
					__( 'Edit <span class="screen-reader-text">%s</span>', 'TEXT_DOMAIN' ),
					array(
						'span' => array(
							'class' => array(),
						),
					)
				),
				wp_kses_post( get_the_title() )
			),
			'<span class="edit-link">',
			'</span>'
		);
	}
}

if ( ! function_exists( 'THEME_PREFIX_post_thumbnail' ) ) {
	/**
	 * Display an optional post thumbnail.
	 *
	 * @since 1.0.0
	 *
	 * @return void
	 */
	function THEME_PREFIX_post_thumbnail(): void {
		if ( post_password_required() || is_attachment() || ! has_post_thumbnail() ) {
			return;
		}

		if ( is_singular() ) {
			?>
			<div class="post-thumbnail">
				<?php the_post_thumbnail( 'full' ); ?>
			</div>
			<?php
		} else {
			?>
			<a class="post-thumbnail" href="<?php the_permalink(); ?>" aria-hidden="true" tabindex="-1">
				<?php
				the_post_thumbnail(
					'post-thumbnail',
					array(
						'alt' => the_title_attribute(
							array(
								'echo' => false,
							)
						),
					)
				);
				?>
			</a>
			<?php
		}
	}
}

if ( ! function_exists( 'THEME_PREFIX_pagination' ) ) {
	/**
	 * Display pagination for archive pages.
	 *
	 * @since 1.0.0
	 *
	 * @return void
	 */
	function THEME_PREFIX_pagination(): void {
		the_posts_pagination(
			array(
				'mid_size'  => 2,
				'prev_text' => sprintf(
					'<span class="screen-reader-text">%s</span><span aria-hidden="true">&laquo;</span>',
					esc_html__( 'Previous page', 'TEXT_DOMAIN' )
				),
				'next_text' => sprintf(
					'<span class="screen-reader-text">%s</span><span aria-hidden="true">&raquo;</span>',
					esc_html__( 'Next page', 'TEXT_DOMAIN' )
				),
			)
		);
	}
}

if ( ! function_exists( 'THEME_PREFIX_excerpt_more' ) ) {
	/**
	 * Customize the excerpt "read more" string.
	 *
	 * @since 1.0.0
	 *
	 * @param string $more The default "more" text.
	 * @return string Modified "more" text.
	 */
	function THEME_PREFIX_excerpt_more( string $more ): string {
		if ( is_admin() ) {
			return $more;
		}

		return sprintf(
			'&hellip; <a href="%1$s" class="more-link">%2$s</a>',
			esc_url( get_permalink( get_the_ID() ) ),
			esc_html__( 'Continue reading', 'TEXT_DOMAIN' )
		);
	}
}
add_filter( 'excerpt_more', 'THEME_PREFIX_excerpt_more' );
```

### 9. Generate header.php

```php
<?php
/**
 * The header for the theme.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">

	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
	<a class="skip-link screen-reader-text" href="#primary">
		<?php esc_html_e( 'Skip to content', 'TEXT_DOMAIN' ); ?>
	</a>

	<header id="masthead" class="site-header">
		<div class="site-branding">
			<?php if ( has_custom_logo() ) : ?>
				<div class="site-logo">
					<?php the_custom_logo(); ?>
				</div>
			<?php endif; ?>

			<?php if ( is_front_page() && is_home() ) : ?>
				<h1 class="site-title">
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
						<?php bloginfo( 'name' ); ?>
					</a>
				</h1>
			<?php else : ?>
				<p class="site-title">
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
						<?php bloginfo( 'name' ); ?>
					</a>
				</p>
			<?php endif; ?>

			<?php
			$THEME_PREFIX_description = get_bloginfo( 'description', 'display' );
			if ( $THEME_PREFIX_description || is_customize_preview() ) :
				?>
				<p class="site-description">
					<?php echo esc_html( $THEME_PREFIX_description ); ?>
				</p>
			<?php endif; ?>
		</div><!-- .site-branding -->

		<nav id="site-navigation" class="main-navigation" aria-label="<?php esc_attr_e( 'Primary Menu', 'TEXT_DOMAIN' ); ?>">
			<button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
				<?php esc_html_e( 'Menu', 'TEXT_DOMAIN' ); ?>
			</button>
			<?php
			wp_nav_menu(
				array(
					'theme_location' => 'primary',
					'menu_id'        => 'primary-menu',
					'container_class' => 'primary-menu-container',
					'fallback_cb'    => false,
				)
			);
			?>
		</nav><!-- #site-navigation -->
	</header><!-- #masthead -->
```

Replace the variable `$THEME_PREFIX_description` with the actual prefix (e.g., `$starter_theme_description`).

### 10. Generate footer.php

```php
<?php
/**
 * The footer for the theme.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

?>
	<footer id="colophon" class="site-footer">
		<div class="site-footer-inner">
			<?php if ( is_active_sidebar( 'footer-1' ) ) : ?>
				<div class="footer-widgets">
					<?php dynamic_sidebar( 'footer-1' ); ?>
				</div><!-- .footer-widgets -->
			<?php endif; ?>

			<?php if ( has_nav_menu( 'footer' ) ) : ?>
				<nav class="footer-navigation" aria-label="<?php esc_attr_e( 'Footer Menu', 'TEXT_DOMAIN' ); ?>">
					<?php
					wp_nav_menu(
						array(
							'theme_location' => 'footer',
							'menu_class'     => 'footer-menu',
							'depth'          => 1,
							'fallback_cb'    => false,
						)
					);
					?>
				</nav><!-- .footer-navigation -->
			<?php endif; ?>

			<div class="site-info">
				<a href="<?php echo esc_url( home_url( '/' ) ); ?>">
					<?php bloginfo( 'name' ); ?>
				</a>
				<span class="sep"> | </span>
				<?php
				printf(
					/* translators: %s: current year and site name */
					esc_html__( '&copy; %1$s %2$s. All rights reserved.', 'TEXT_DOMAIN' ),
					esc_html( (string) gmdate( 'Y' ) ),
					esc_html( get_bloginfo( 'name' ) )
				);
				?>
			</div><!-- .site-info -->
		</div><!-- .site-footer-inner -->
	</footer><!-- #colophon -->
</div><!-- #page -->

<?php wp_footer(); ?>

</body>
</html>
```

### 11. Generate sidebar.php

```php
<?php
/**
 * The sidebar containing the main widget area.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

if ( ! is_active_sidebar( 'sidebar-1' ) ) {
	return;
}
?>

<aside id="secondary" class="widget-area" aria-label="<?php esc_attr_e( 'Sidebar', 'TEXT_DOMAIN' ); ?>">
	<?php dynamic_sidebar( 'sidebar-1' ); ?>
</aside><!-- #secondary -->
```

### 12. Generate index.php

```php
<?php
/**
 * The main template file.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

get_header();
?>

<main id="primary" class="site-main">
	<?php
	if ( have_posts() ) :

		if ( is_home() && ! is_front_page() ) :
			?>
			<header class="page-header">
				<h1 class="page-title screen-reader-text">
					<?php single_post_title(); ?>
				</h1>
			</header><!-- .page-header -->
			<?php
		endif;

		while ( have_posts() ) :
			the_post();
			?>
			<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
				<header class="entry-header">
					<?php
					if ( is_singular() ) :
						the_title( '<h1 class="entry-title">', '</h1>' );
					else :
						the_title(
							'<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">',
							'</a></h2>'
						);
					endif;

					if ( 'post' === get_post_type() ) :
						?>
						<div class="entry-meta">
							<?php
							THEME_PREFIX_posted_on();
							THEME_PREFIX_posted_by();
							?>
						</div><!-- .entry-meta -->
					<?php endif; ?>
				</header><!-- .entry-header -->

				<?php THEME_PREFIX_post_thumbnail(); ?>

				<div class="entry-content">
					<?php
					if ( is_singular() ) :
						the_content(
							sprintf(
								wp_kses(
									/* translators: %s: post title */
									__( 'Continue reading<span class="screen-reader-text"> "%s"</span>', 'TEXT_DOMAIN' ),
									array(
										'span' => array(
											'class' => array(),
										),
									)
								),
								wp_kses_post( get_the_title() )
							)
						);

						wp_link_pages(
							array(
								'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'TEXT_DOMAIN' ),
								'after'  => '</div>',
							)
						);
					else :
						the_excerpt();
					endif;
					?>
				</div><!-- .entry-content -->

				<footer class="entry-footer">
					<?php THEME_PREFIX_entry_footer(); ?>
				</footer><!-- .entry-footer -->
			</article><!-- #post-<?php the_ID(); ?> -->
			<?php
		endwhile;

		THEME_PREFIX_pagination();

	else :
		?>
		<section class="no-results not-found">
			<header class="page-header">
				<h1 class="page-title">
					<?php esc_html_e( 'Nothing Found', 'TEXT_DOMAIN' ); ?>
				</h1>
			</header><!-- .page-header -->

			<div class="page-content">
				<?php if ( is_search() ) : ?>
					<p><?php esc_html_e( 'Sorry, but nothing matched your search terms. Please try again with some different keywords.', 'TEXT_DOMAIN' ); ?></p>
					<?php get_search_form(); ?>
				<?php else : ?>
					<p><?php esc_html_e( 'It seems we can&rsquo;t find what you&rsquo;re looking for. Perhaps searching can help.', 'TEXT_DOMAIN' ); ?></p>
					<?php get_search_form(); ?>
				<?php endif; ?>
			</div><!-- .page-content -->
		</section><!-- .no-results -->
	<?php endif; ?>
</main><!-- #primary -->

<?php
get_sidebar();
get_footer();
```

### 13. Generate single.php

```php
<?php
/**
 * The template for displaying single posts.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

get_header();
?>

<main id="primary" class="site-main">
	<?php
	while ( have_posts() ) :
		the_post();
		?>
		<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
			<header class="entry-header">
				<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>

				<div class="entry-meta">
					<?php
					THEME_PREFIX_posted_on();
					THEME_PREFIX_posted_by();
					?>
				</div><!-- .entry-meta -->
			</header><!-- .entry-header -->

			<?php THEME_PREFIX_post_thumbnail(); ?>

			<div class="entry-content">
				<?php
				the_content();

				wp_link_pages(
					array(
						'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'TEXT_DOMAIN' ),
						'after'  => '</div>',
					)
				);
				?>
			</div><!-- .entry-content -->

			<footer class="entry-footer">
				<?php THEME_PREFIX_entry_footer(); ?>
			</footer><!-- .entry-footer -->
		</article><!-- #post-<?php the_ID(); ?> -->

		<?php
		// Post navigation.
		the_post_navigation(
			array(
				'prev_text' => '<span class="nav-subtitle">' . esc_html__( 'Previous:', 'TEXT_DOMAIN' ) . '</span> <span class="nav-title">%title</span>',
				'next_text' => '<span class="nav-subtitle">' . esc_html__( 'Next:', 'TEXT_DOMAIN' ) . '</span> <span class="nav-title">%title</span>',
			)
		);

		// If comments are open or there is at least one comment, load the comments template.
		if ( comments_open() || get_comments_number() ) :
			comments_template();
		endif;

	endwhile;
	?>
</main><!-- #primary -->

<?php
get_sidebar();
get_footer();
```

### 14. Generate archive.php

```php
<?php
/**
 * The template for displaying archive pages.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

get_header();
?>

<main id="primary" class="site-main">
	<?php if ( have_posts() ) : ?>

		<header class="page-header">
			<?php
			the_archive_title( '<h1 class="page-title">', '</h1>' );
			the_archive_description( '<div class="archive-description">', '</div>' );
			?>
		</header><!-- .page-header -->

		<?php
		while ( have_posts() ) :
			the_post();
			?>
			<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
				<header class="entry-header">
					<?php
					the_title(
						'<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">',
						'</a></h2>'
					);

					if ( 'post' === get_post_type() ) :
						?>
						<div class="entry-meta">
							<?php
							THEME_PREFIX_posted_on();
							THEME_PREFIX_posted_by();
							?>
						</div><!-- .entry-meta -->
					<?php endif; ?>
				</header><!-- .entry-header -->

				<?php THEME_PREFIX_post_thumbnail(); ?>

				<div class="entry-summary">
					<?php the_excerpt(); ?>
				</div><!-- .entry-summary -->

				<footer class="entry-footer">
					<?php THEME_PREFIX_entry_footer(); ?>
				</footer><!-- .entry-footer -->
			</article><!-- #post-<?php the_ID(); ?> -->
			<?php
		endwhile;

		THEME_PREFIX_pagination();

	else :
		?>
		<section class="no-results not-found">
			<header class="page-header">
				<h1 class="page-title">
					<?php esc_html_e( 'Nothing Found', 'TEXT_DOMAIN' ); ?>
				</h1>
			</header><!-- .page-header -->

			<div class="page-content">
				<p><?php esc_html_e( 'It seems we can&rsquo;t find what you&rsquo;re looking for. Perhaps searching can help.', 'TEXT_DOMAIN' ); ?></p>
				<?php get_search_form(); ?>
			</div><!-- .page-content -->
		</section><!-- .no-results -->
	<?php endif; ?>
</main><!-- #primary -->

<?php
get_sidebar();
get_footer();
```

### 15. Generate page.php

```php
<?php
/**
 * The template for displaying pages.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

get_header();
?>

<main id="primary" class="site-main">
	<?php
	while ( have_posts() ) :
		the_post();
		?>
		<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
			<header class="entry-header">
				<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
			</header><!-- .entry-header -->

			<?php THEME_PREFIX_post_thumbnail(); ?>

			<div class="entry-content">
				<?php
				the_content();

				wp_link_pages(
					array(
						'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'TEXT_DOMAIN' ),
						'after'  => '</div>',
					)
				);
				?>
			</div><!-- .entry-content -->

			<?php if ( get_edit_post_link() ) : ?>
				<footer class="entry-footer">
					<?php
					edit_post_link(
						sprintf(
							wp_kses(
								/* translators: %s: page title */
								__( 'Edit <span class="screen-reader-text">%s</span>', 'TEXT_DOMAIN' ),
								array(
									'span' => array(
										'class' => array(),
									),
								)
							),
							wp_kses_post( get_the_title() )
						),
						'<span class="edit-link">',
						'</span>'
					);
					?>
				</footer><!-- .entry-footer -->
			<?php endif; ?>
		</article><!-- #post-<?php the_ID(); ?> -->

		<?php
		// If comments are open or there is at least one comment, load the comments template.
		if ( comments_open() || get_comments_number() ) :
			comments_template();
		endif;

	endwhile;
	?>
</main><!-- #primary -->

<?php
get_sidebar();
get_footer();
```

### 16. Generate 404.php

```php
<?php
/**
 * The template for displaying 404 pages (not found).
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

get_header();
?>

<main id="primary" class="site-main">
	<section class="error-404 not-found">
		<header class="page-header">
			<h1 class="page-title">
				<?php esc_html_e( 'Oops! That page can&rsquo;t be found.', 'TEXT_DOMAIN' ); ?>
			</h1>
		</header><!-- .page-header -->

		<div class="page-content">
			<p>
				<?php esc_html_e( 'It looks like nothing was found at this location. Maybe try one of the links below or a search?', 'TEXT_DOMAIN' ); ?>
			</p>

			<?php get_search_form(); ?>

			<div class="widget-area">
				<?php
				the_widget(
					'WP_Widget_Recent_Posts',
					array(
						'title'  => esc_html__( 'Recent Posts', 'TEXT_DOMAIN' ),
						'number' => 5,
					),
					array(
						'before_widget' => '<section class="widget">',
						'after_widget'  => '</section>',
						'before_title'  => '<h2 class="widget-title">',
						'after_title'   => '</h2>',
					)
				);
				?>

				<section class="widget widget_categories">
					<h2 class="widget-title">
						<?php esc_html_e( 'Most Used Categories', 'TEXT_DOMAIN' ); ?>
					</h2>
					<ul>
						<?php
						wp_list_categories(
							array(
								'orderby'    => 'count',
								'order'      => 'DESC',
								'show_count' => true,
								'title_li'   => '',
								'number'     => 10,
							)
						);
						?>
					</ul>
				</section><!-- .widget_categories -->

				<?php
				/* translators: %1$s: smiley face */
				$THEME_PREFIX_archive_content = '<p>' . sprintf(
					esc_html__( 'Try looking in the monthly archives. %1$s', 'TEXT_DOMAIN' ),
					convert_smilies( ':)' )
				) . '</p>';

				the_widget(
					'WP_Widget_Archives',
					array(
						'title'    => esc_html__( 'Archives', 'TEXT_DOMAIN' ),
						'count'    => true,
						'dropdown' => true,
					),
					array(
						'before_widget' => '<section class="widget">',
						'after_widget'  => '</section>' . $THEME_PREFIX_archive_content,
						'before_title'  => '<h2 class="widget-title">',
						'after_title'   => '</h2>',
					)
				);

				the_widget(
					'WP_Widget_Tag_Cloud',
					array(
						'title' => esc_html__( 'Tags', 'TEXT_DOMAIN' ),
					),
					array(
						'before_widget' => '<section class="widget">',
						'after_widget'  => '</section>',
						'before_title'  => '<h2 class="widget-title">',
						'after_title'   => '</h2>',
					)
				);
				?>
			</div><!-- .widget-area -->
		</div><!-- .page-content -->
	</section><!-- .error-404 -->
</main><!-- #primary -->

<?php
get_footer();
```

Replace `$THEME_PREFIX_archive_content` with the actual prefixed variable name.

### 17. Generate composer.json

```json
{
    "name": "theme-vendor/TEXT_DOMAIN",
    "description": "THEME_NAME WordPress theme",
    "type": "wordpress-theme",
    "license": "GPL-2.0-or-later",
    "authors": [
        {
            "name": "Author Name",
            "email": "author@example.com"
        }
    ],
    "require": {
        "php": ">=8.0"
    },
    "require-dev": {
        "squizlabs/php_codesniffer": "^3.7",
        "wp-coding-standards/wpcs": "^3.0",
        "phpcompatibility/phpcompatibility-wp": "^2.1",
        "dealerdirect/phpcodesniffer-composer-installer": "^1.0"
    },
    "autoload": {
        "psr-4": {
            "THEME_NAMESPACE\\": "src/"
        }
    },
    "config": {
        "allow-plugins": {
            "dealerdirect/phpcodesniffer-composer-installer": true
        }
    },
    "scripts": {
        "phpcs": "phpcs --standard=WordPress --extensions=php .",
        "phpcbf": "phpcbf --standard=WordPress --extensions=php ."
    }
}
```

Replace `THEME_NAMESPACE` with the actual PascalCase namespace (e.g., `StarterTheme\\`) and `TEXT_DOMAIN` with the actual text domain slug.

### 18. Generate theme.json (Hybrid FSE Only)

Only generate this file if the user chose hybrid FSE support. This enables block editor features while keeping the classic PHP template hierarchy.

```json
{
    "$schema": "https://schemas.wp.org/wp/6.7/theme.json",
    "version": 3,
    "settings": {
        "appearanceTools": true,
        "color": {
            "palette": [
                {
                    "slug": "primary",
                    "color": "#0073aa",
                    "name": "Primary"
                },
                {
                    "slug": "secondary",
                    "color": "#23282d",
                    "name": "Secondary"
                },
                {
                    "slug": "accent",
                    "color": "#00a0d2",
                    "name": "Accent"
                },
                {
                    "slug": "white",
                    "color": "#ffffff",
                    "name": "White"
                },
                {
                    "slug": "light-gray",
                    "color": "#f1f1f1",
                    "name": "Light Gray"
                },
                {
                    "slug": "dark-gray",
                    "color": "#32373c",
                    "name": "Dark Gray"
                },
                {
                    "slug": "black",
                    "color": "#000000",
                    "name": "Black"
                }
            ],
            "gradients": [],
            "defaultPalette": false,
            "defaultGradients": false
        },
        "typography": {
            "fluid": true,
            "fontSizes": [
                {
                    "slug": "small",
                    "size": "0.875rem",
                    "name": "Small",
                    "fluid": {
                        "min": "0.8125rem",
                        "max": "0.875rem"
                    }
                },
                {
                    "slug": "medium",
                    "size": "1rem",
                    "name": "Medium",
                    "fluid": {
                        "min": "0.9375rem",
                        "max": "1rem"
                    }
                },
                {
                    "slug": "large",
                    "size": "1.5rem",
                    "name": "Large",
                    "fluid": {
                        "min": "1.25rem",
                        "max": "1.5rem"
                    }
                },
                {
                    "slug": "x-large",
                    "size": "2.25rem",
                    "name": "Extra Large",
                    "fluid": {
                        "min": "1.75rem",
                        "max": "2.25rem"
                    }
                }
            ],
            "fontFamilies": [
                {
                    "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif",
                    "slug": "system",
                    "name": "System"
                },
                {
                    "fontFamily": "'Georgia', 'Times New Roman', serif",
                    "slug": "serif",
                    "name": "Serif"
                }
            ]
        },
        "spacing": {
            "units": ["px", "em", "rem", "vh", "vw", "%"],
            "spacingSizes": [
                {
                    "slug": "10",
                    "size": "0.625rem",
                    "name": "1"
                },
                {
                    "slug": "20",
                    "size": "1.25rem",
                    "name": "2"
                },
                {
                    "slug": "30",
                    "size": "2rem",
                    "name": "3"
                },
                {
                    "slug": "40",
                    "size": "3rem",
                    "name": "4"
                },
                {
                    "slug": "50",
                    "size": "4.5rem",
                    "name": "5"
                }
            ]
        },
        "layout": {
            "contentSize": "800px",
            "wideSize": "1140px"
        },
        "useRootPaddingAwareAlignments": true
    },
    "styles": {
        "spacing": {
            "padding": {
                "top": "0",
                "right": "var(--wp--preset--spacing--30)",
                "bottom": "0",
                "left": "var(--wp--preset--spacing--30)"
            },
            "blockGap": "var(--wp--preset--spacing--20)"
        },
        "typography": {
            "fontFamily": "var(--wp--preset--font-family--system)",
            "fontSize": "var(--wp--preset--font-size--medium)",
            "lineHeight": "1.6"
        },
        "color": {
            "background": "var(--wp--preset--color--white)",
            "text": "var(--wp--preset--color--dark-gray)"
        },
        "elements": {
            "link": {
                "color": {
                    "text": "var(--wp--preset--color--primary)"
                },
                ":hover": {
                    "color": {
                        "text": "var(--wp--preset--color--secondary)"
                    }
                }
            },
            "h1": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--x-large)"
                }
            },
            "h2": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--large)"
                }
            }
        }
    },
    "templateParts": [
        {
            "name": "header",
            "title": "Header",
            "area": "header"
        },
        {
            "name": "footer",
            "title": "Footer",
            "area": "footer"
        }
    ],
    "customTemplates": [
        {
            "name": "blank",
            "title": "Blank",
            "postTypes": ["page", "post"]
        }
    ]
}
```

Also generate the following block template files when hybrid FSE is selected.

**templates/blank.html:**

```html
<!-- wp:template-part {"slug":"header","area":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","area":"footer"} /-->
```

**parts/header.html:**

```html
<!-- wp:group {"tagName":"header","className":"site-header","layout":{"type":"constrained"}} -->
<header class="wp-block-group site-header">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:site-title /-->
        <!-- wp:navigation {"layout":{"type":"flex","justifyContent":"right"}} /-->
    </div>
    <!-- /wp:group -->
</header>
<!-- /wp:group -->
```

**parts/footer.html:**

```html
<!-- wp:group {"tagName":"footer","className":"site-footer","layout":{"type":"constrained"}} -->
<footer class="wp-block-group site-footer">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"center"}} -->
    <div class="wp-block-group">
        <!-- wp:paragraph {"fontSize":"small"} -->
        <p class="has-small-font-size">&copy; <!-- wp:shortcode -->[year]<!-- /wp:shortcode --> <!-- wp:site-title /--></p>
        <!-- /wp:paragraph -->
    </div>
    <!-- /wp:group -->
</footer>
<!-- /wp:group -->
```

### 19. Generate WooCommerce Template Overrides (WooCommerce Only)

Only generate these files if the user chose WooCommerce support. These are minimal template overrides that developers customize for their design.

**woocommerce/single-product.php:**

```php
<?php
/**
 * The template for displaying single product pages.
 *
 * This template can be overridden by copying it to TEXT_DOMAIN/woocommerce/single-product.php.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

defined( 'ABSPATH' ) || exit;

get_header();
?>

<main id="primary" class="site-main woocommerce-single-product">
	<?php
	while ( have_posts() ) :
		the_post();

		wc_get_template_part( 'content', 'single-product' );

	endwhile;
	?>
</main><!-- #primary -->

<?php
get_sidebar();
get_footer();
```

**woocommerce/archive-product.php:**

```php
<?php
/**
 * The template for displaying product archive pages.
 *
 * This template can be overridden by copying it to TEXT_DOMAIN/woocommerce/archive-product.php.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

defined( 'ABSPATH' ) || exit;

get_header();
?>

<main id="primary" class="site-main woocommerce-archive">
	<?php if ( apply_filters( 'woocommerce_show_page_title', true ) ) : ?>
		<header class="woocommerce-products-header">
			<h1 class="woocommerce-products-header__title page-title">
				<?php woocommerce_page_title(); ?>
			</h1>
		</header>
	<?php endif; ?>

	<?php
	/**
	 * Hook: woocommerce_archive_description.
	 *
	 * @hooked woocommerce_taxonomy_archive_description - 10
	 * @hooked woocommerce_product_archive_description - 10
	 */
	do_action( 'woocommerce_archive_description' );
	?>

	<?php if ( woocommerce_product_loop() ) : ?>

		<?php
		/**
		 * Hook: woocommerce_before_shop_loop.
		 *
		 * @hooked woocommerce_output_all_notices - 10
		 * @hooked woocommerce_result_count - 20
		 * @hooked woocommerce_catalog_ordering - 30
		 */
		do_action( 'woocommerce_before_shop_loop' );
		?>

		<?php woocommerce_product_loop_start(); ?>

		<?php
		if ( wc_get_loop_prop( 'total' ) ) :
			while ( have_posts() ) :
				the_post();

				/**
				 * Hook: woocommerce_shop_loop.
				 */
				do_action( 'woocommerce_shop_loop' );

				wc_get_template_part( 'content', 'product' );
			endwhile;
		endif;
		?>

		<?php woocommerce_product_loop_end(); ?>

		<?php
		/**
		 * Hook: woocommerce_after_shop_loop.
		 *
		 * @hooked woocommerce_pagination - 10
		 */
		do_action( 'woocommerce_after_shop_loop' );
		?>

	<?php else : ?>

		<?php
		/**
		 * Hook: woocommerce_no_products_found.
		 *
		 * @hooked wc_no_products_found - 10
		 */
		do_action( 'woocommerce_no_products_found' );
		?>

	<?php endif; ?>
</main><!-- #primary -->

<?php
get_sidebar();
get_footer();
```

**woocommerce/content-product.php:**

```php
<?php
/**
 * The template for displaying product content within loops.
 *
 * This template can be overridden by copying it to TEXT_DOMAIN/woocommerce/content-product.php.
 *
 * @package THEME_NAMESPACE
 * @since   1.0.0
 */

declare(strict_types=1);

defined( 'ABSPATH' ) || exit;

global $product;

// Ensure visibility.
if ( empty( $product ) || ! $product->is_visible() ) {
	return;
}
?>

<li <?php wc_product_class( '', $product ); ?>>
	<?php
	/**
	 * Hook: woocommerce_before_shop_loop_item.
	 *
	 * @hooked woocommerce_template_loop_product_link_open - 10
	 */
	do_action( 'woocommerce_before_shop_loop_item' );

	/**
	 * Hook: woocommerce_before_shop_loop_item_title.
	 *
	 * @hooked woocommerce_show_product_loop_sale_flash - 10
	 * @hooked woocommerce_template_loop_product_thumbnail - 10
	 */
	do_action( 'woocommerce_before_shop_loop_item_title' );

	/**
	 * Hook: woocommerce_shop_loop_item_title.
	 *
	 * @hooked woocommerce_template_loop_product_title - 10
	 */
	do_action( 'woocommerce_shop_loop_item_title' );

	/**
	 * Hook: woocommerce_after_shop_loop_item_title.
	 *
	 * @hooked woocommerce_template_loop_rating - 5
	 * @hooked woocommerce_template_loop_price - 10
	 */
	do_action( 'woocommerce_after_shop_loop_item_title' );

	/**
	 * Hook: woocommerce_after_shop_loop_item.
	 *
	 * @hooked woocommerce_template_loop_product_link_close - 5
	 * @hooked woocommerce_template_loop_add_to_cart - 10
	 */
	do_action( 'woocommerce_after_shop_loop_item' );
	?>
</li>
```

Also add WooCommerce theme support in `inc/theme-support.php` by appending this inside the `THEME_PREFIX_setup()` function:

```php
		// WooCommerce support.
		add_theme_support( 'woocommerce' );
		add_theme_support( 'wc-product-gallery-zoom' );
		add_theme_support( 'wc-product-gallery-lightbox' );
		add_theme_support( 'wc-product-gallery-slider' );
```

### 20. Generate the src/.gitkeep File

Create an empty `src/.gitkeep` file to preserve the PSR-4 autoloading directory in version control. Leave a comment in `composer.json` or the project README noting that custom PHP classes should be placed in `src/` using the theme namespace.

### 21. Post-Generation Steps

After generating all files, provide the user with these next steps:

1. **Install dependencies:** Run `composer install` in the theme directory.
2. **Add screenshot:** Replace `screenshot.png` with a 1200x900 pixel theme preview image.
3. **Customize style.css:** Update Author, Author URI, Theme URI, and Description.
4. **Register custom post types:** Uncomment and customize the example in `inc/custom-post-types.php`.
5. **Build assets:** Set up your CSS/JS build pipeline and output compiled files to `css/` and `js/` directories.
6. **Activate:** Move the theme directory to `wp-content/themes/` and activate in the WordPress admin.

## Output Format

1. All generated files with complete, production-ready code (no stubs or placeholders)
2. Proper variable substitution throughout (THEME_NAME, TEXT_DOMAIN, THEME_PREFIX, THEME_NAMESPACE)
3. Conditional files based on user choices (WooCommerce templates, theme.json)
4. Summary of the generated file tree
5. Post-generation instructions for the developer
