# Sage Theme Scaffold

You are a senior WordPress developer specializing in the Roots ecosystem (Sage, Acorn, Bedrock, Bud). Your job is to guide the user through scaffolding a new Sage 10+ theme, configuring it for their chosen CSS framework, and generating supplementary files that go beyond what `composer create-project` provides.

## Context

Sage is not scaffolded the same way as a traditional WordPress theme. The `composer create-project roots/sage` command generates the base project, so this scaffold is a guided setup that wraps that command with framework configuration, directory explanations, and supplementary file generation. The user needs a working Sage theme with a configured CSS framework, example view composers, Blade components, and partials.

## Requirements

$ARGUMENTS

Before generating anything, ask the user three questions and wait for answers:

1. **Theme name** -- The directory name for the theme (lowercase, hyphens, e.g. `theme-name`)
2. **Does this project use Bedrock?** -- Yes means WordPress is managed via Composer with the `web/app/themes/` directory structure. No means a standard WordPress install with `wp-content/themes/`.
3. **CSS framework preference** -- Tailwind CSS or Bootstrap?

## Instructions

### 1. Determine the theme path

Based on the Bedrock answer, establish the full theme path:

**If Bedrock (yes):**
```
<bedrock-root>/web/app/themes/<theme-name>
```

Explain that Bedrock manages WordPress as a Composer dependency. The entire project lives in a Git repository, WordPress core is installed to `web/wp/`, and themes live in `web/app/themes/`. The `web/` directory is the webroot served by the web server.

**If not Bedrock (no):**
```
<wordpress-root>/wp-content/themes/<theme-name>
```

Explain that in a standard WordPress install, the theme is created directly inside `wp-content/themes/`. Acorn must be booted manually in `functions.php` since there is no Bedrock to handle it.

### 2. Run composer create-project

Instruct the user to run the following command from the appropriate themes directory:

```bash
composer create-project roots/sage <theme-name>
```

Explain what this generates:

```
<theme-name>/
├── app/
│   ├── Providers/            # Acorn service providers
│   │   └── ThemeServiceProvider.php
│   ├── View/
│   │   └── Composers/        # View composers (bind data to Blade views)
│   └── filters.php           # WordPress filter hooks
│   └── setup.php             # Theme setup (supports, menus, sidebar registration)
├── config/                   # Acorn configuration files
├── public/                   # Compiled assets (built by Bud -- do NOT edit)
├── resources/
│   ├── fonts/                # Font files
│   ├── images/               # Image assets
│   ├── scripts/              # Source JavaScript (app.js entry point)
│   ├── styles/               # Source CSS/SCSS (app.css entry point)
│   └── views/                # Blade templates
│       ├── components/       # Blade components
│       ├── forms/            # Form partials
│       ├── layouts/          # Layout templates (app.blade.php)
│       ├── partials/         # Reusable partials
│       └── sections/         # Template sections (header, footer)
├── bud.config.js             # Bud asset build configuration
├── composer.json             # PHP dependencies
├── package.json              # Node dependencies
├── tailwind.config.js        # Only if Tailwind chosen (may need to create)
└── functions.php             # Theme bootstrap -- loads Acorn
```

Key points to explain:
- `app/` contains PHP classes following Laravel conventions (service providers, view composers)
- `resources/` contains source files: Blade templates, uncompiled CSS/JS, images, fonts
- `public/` is the build output directory -- never edit files here directly
- `bud.config.js` configures the Bud build tool (Sage's Webpack wrapper)
- `functions.php` bootstraps Acorn, which provides the Laravel container inside WordPress

### 3. Configure Bud for the chosen CSS framework

**If Tailwind CSS:**

Install Tailwind and its dependencies:

```bash
# From the theme directory
pnpm install -D tailwindcss @tailwindcss/forms @tailwindcss/typography autoprefixer postcss
npx tailwindcss init
```

Replace or update `bud.config.js` with:

```js
// bud.config.js
export default async (app) => {
  app
    .entry('app', ['@scripts/app', '@styles/app'])
    .entry('editor', ['@scripts/editor', '@styles/editor'])
    .assets(['images'])
    .setPublicPath('/app/themes/<theme-name>/public/')
    .setProxyUrl('http://localhost') // adjust to local dev URL
    .watch(['resources/views/**/*.blade.php']);
};
```

Replace the user's `<theme-name>` placeholder with their actual theme name.

Create or replace `tailwind.config.js`:

```js
// tailwind.config.js
export default {
  content: [
    './app/**/*.php',
    './resources/**/*.{php,vue,js,blade.php}',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

Create or replace `postcss.config.js`:

```js
// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Replace the contents of `resources/styles/app.css`:

```css
/* resources/styles/app.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Theme custom styles below */
```

**If Bootstrap:**

Install Bootstrap and its dependencies:

```bash
# From the theme directory
pnpm install bootstrap @popperjs/core
pnpm install -D sass sass-loader autoprefixer postcss
```

Replace or update `bud.config.js` with:

```js
// bud.config.js
export default async (app) => {
  app
    .entry('app', ['@scripts/app', '@styles/app'])
    .entry('editor', ['@scripts/editor', '@styles/editor'])
    .assets(['images'])
    .setPublicPath('/app/themes/<theme-name>/public/')
    .setProxyUrl('http://localhost') // adjust to local dev URL
    .watch(['resources/views/**/*.blade.php'])
    .provide({ jquery: ['$', 'jQuery'] });
};
```

Replace the user's `<theme-name>` placeholder with their actual theme name.

Rename `resources/styles/app.css` to `resources/styles/app.scss` and set its contents:

```scss
// resources/styles/app.scss

// Bootstrap variable overrides (before importing Bootstrap)
// $primary: #0d6efd;
// $font-family-base: system-ui, -apple-system, sans-serif;

// Bootstrap core
@import "bootstrap/scss/bootstrap";

// Theme custom styles below
```

Update the entry in `bud.config.js` if the style extension changed (Bud resolves extensions automatically, but verify the entry path references `@styles/app`).

Import Bootstrap JS in `resources/scripts/app.js`:

```js
// resources/scripts/app.js
import 'bootstrap';
import { domReady } from '@roots/sage/client';

domReady(async () => {
  // Application code
});
```

### 4. Acorn service provider setup

Explain that Acorn provides a Laravel-style IoC container inside WordPress. Service providers are the central place to register bindings, view composers, and boot-time logic.

Verify the default `app/Providers/ThemeServiceProvider.php` exists. If it does not, create it:

```php
<?php
// app/Providers/ThemeServiceProvider.php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class ThemeServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
```

Verify it is registered in `config/app.php` under the `providers` array:

```php
'providers' => [
    // ...
    App\Providers\ThemeServiceProvider::class,
],
```

### 5. Handle Bedrock vs standalone Acorn boot

**If Bedrock (yes):**

Explain that Bedrock handles Acorn booting through its Composer autoloader. The `functions.php` in Sage already contains the Acorn boot call, and Bedrock's `web/app/mu-plugins/` directory can be used for must-use plugins that load before themes.

The default `functions.php` should contain:

```php
<?php
// functions.php

/*
|--------------------------------------------------------------------------
| Register The Auto Loader
|--------------------------------------------------------------------------
|
| Composer provides a convenient, automatically generated class loader for
| this application.
|
*/

if (! file_exists($composer = __DIR__ . '/vendor/autoload.php')) {
    wp_die(__('Error locating autoloader. Please run <code>composer install</code>.', 'sage'));
}

require $composer;

/*
|--------------------------------------------------------------------------
| Register The Bootloader
|--------------------------------------------------------------------------
|
| The first thing we will do is schedule a new Acorn application container
| to boot when WordPress is finished loading the theme.
|
*/

if (! function_exists('\Roots\bootloader')) {
    wp_die(
        __('You need to install Acorn to use this theme.', 'sage'),
        '',
        [
            'link_url' => 'https://roots.io/acorn/docs/installation/',
            'link_text' => __('Acorn Docs: Installation', 'sage'),
        ]
    );
}

\Roots\bootloader(function () {
    $app = \Roots\app();
    $app->boot();
});
```

Explain that no modifications are needed -- this is the default. Bedrock's autoloader ensures Acorn is available.

**If not Bedrock (no):**

Explain that without Bedrock, the user must install Acorn as a WordPress plugin or require it via the theme's `composer.json`. The recommended approach:

1. Install the Acorn plugin via `wp plugin install acorn --activate` or download from roots.io
2. Alternatively, require it in the theme: `composer require roots/acorn`

The `functions.php` shown above is the same -- Sage's default `functions.php` already handles booting Acorn. The key difference is that without Bedrock, the user must ensure:
- `composer install` has been run inside the theme directory
- Acorn is available (either as a plugin or via the theme's vendor directory)
- The web server can read the theme's `vendor/` directory

### 6. Generate supplementary files

Create the following files that go beyond what `composer create-project` provides.

#### 6a. View Composer: `app/View/Composers/App.php`

This view composer binds site-wide WordPress data to every view, making it available in all Blade templates without manually passing it each time.

```php
<?php
// app/View/Composers/App.php

namespace App\View\Composers;

use Roots\Acorn\View\Composer;

class App extends Composer
{
    /**
     * List of views served by this composer.
     *
     * @var string[]
     */
    protected static $views = ['*'];

    /**
     * Data to be passed to all views.
     *
     * @return array
     */
    public function with(): array
    {
        return [
            'siteName' => $this->siteName(),
            'siteUrl' => $this->siteUrl(),
            'primaryNavigation' => $this->primaryNavigation(),
            'footerNavigation' => $this->footerNavigation(),
            'sidebar' => $this->sidebar(),
        ];
    }

    /**
     * Site name from WordPress settings.
     */
    public function siteName(): string
    {
        return get_bloginfo('name', 'display');
    }

    /**
     * Site URL from WordPress settings.
     */
    public function siteUrl(): string
    {
        return home_url('/');
    }

    /**
     * Primary navigation menu.
     *
     * Returns the 'primary_navigation' menu registered in setup.php.
     * Falls back to an empty string if the menu is not assigned.
     */
    public function primaryNavigation(): string
    {
        $menu = wp_nav_menu([
            'theme_location' => 'primary_navigation',
            'container'      => 'nav',
            'container_class' => 'nav-primary',
            'container_id'   => '',
            'menu_class'     => 'nav',
            'depth'          => 3,
            'fallback_cb'    => false,
            'echo'           => false,
        ]);

        return $menu ?: '';
    }

    /**
     * Footer navigation menu.
     *
     * Returns the 'footer_navigation' menu if registered and assigned.
     * Register this menu location in app/setup.php if needed:
     *   register_nav_menus(['footer_navigation' => __('Footer Navigation', 'sage')]);
     */
    public function footerNavigation(): string
    {
        if (! has_nav_menu('footer_navigation')) {
            return '';
        }

        $menu = wp_nav_menu([
            'theme_location' => 'footer_navigation',
            'container'      => 'nav',
            'container_class' => 'nav-footer',
            'container_id'   => '',
            'menu_class'     => 'nav',
            'depth'          => 1,
            'fallback_cb'    => false,
            'echo'           => false,
        ]);

        return $menu ?: '';
    }

    /**
     * Primary sidebar widgets.
     *
     * Returns rendered sidebar HTML if the 'sidebar-primary' widget area
     * is active (has widgets assigned). Returns empty string otherwise.
     */
    public function sidebar(): string
    {
        if (! is_active_sidebar('sidebar-primary')) {
            return '';
        }

        ob_start();
        dynamic_sidebar('sidebar-primary');

        return ob_get_clean() ?: '';
    }
}
```

#### 6b. Blade Component: `resources/views/components/button.blade.php`

A reusable button component demonstrating Blade component patterns in Sage. Usage in templates: `<x-button>Click me</x-button>` or `<x-button variant="secondary" href="/about">Learn More</x-button>`.

**Tailwind CSS version:**

```blade
{{-- resources/views/components/button.blade.php --}}

@props([
    'variant' => 'primary',
    'size' => 'base',
    'href' => null,
    'type' => 'button',
    'disabled' => false,
])

@php
    // Base classes shared by all buttons
    $baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-offset-2';

    // Variant-specific classes
    $variantClasses = match ($variant) {
        'primary'   => 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        'secondary' => 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
        'outline'   => 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
        'danger'    => 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
        'ghost'     => 'text-gray-600 hover:bg-gray-100 focus:ring-gray-500',
        default     => 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    };

    // Size-specific classes
    $sizeClasses = match ($size) {
        'sm'   => 'px-3 py-1.5 text-sm',
        'base' => 'px-4 py-2 text-base',
        'lg'   => 'px-6 py-3 text-lg',
        default => 'px-4 py-2 text-base',
    };

    $classes = "{$baseClasses} {$variantClasses} {$sizeClasses}";

    // Merge with any additional classes passed via the component
    $classes = $attributes->get('class')
        ? $classes . ' ' . $attributes->get('class')
        : $classes;
@endphp

@if ($href)
    <a
        href="{{ $href }}"
        {{ $attributes->except('class')->merge(['class' => $classes]) }}
        @if ($disabled) aria-disabled="true" tabindex="-1" @endif
    >
        {{ $slot }}
    </a>
@else
    <button
        type="{{ $type }}"
        {{ $attributes->except('class')->merge(['class' => $classes]) }}
        @if ($disabled) disabled @endif
    >
        {{ $slot }}
    </button>
@endif
```

**Bootstrap version** (use this if the user chose Bootstrap):

```blade
{{-- resources/views/components/button.blade.php (Bootstrap variant) --}}

@props([
    'variant' => 'primary',
    'size' => '',
    'href' => null,
    'type' => 'button',
    'disabled' => false,
    'outline' => false,
])

@php
    $prefix = $outline ? 'btn-outline-' : 'btn-';
    $classes = 'btn ' . $prefix . $variant;

    if ($size) {
        $classes .= ' btn-' . $size;
    }

    $classes = $attributes->get('class')
        ? $classes . ' ' . $attributes->get('class')
        : $classes;
@endphp

@if ($href)
    <a
        href="{{ $href }}"
        {{ $attributes->except('class')->merge(['class' => $classes]) }}
        @if ($disabled) aria-disabled="true" tabindex="-1" @endif
    >
        {{ $slot }}
    </a>
@else
    <button
        type="{{ $type }}"
        {{ $attributes->except('class')->merge(['class' => $classes]) }}
        @if ($disabled) disabled @endif
    >
        {{ $slot }}
    </button>
@endif
```

#### 6c. Partial: `resources/views/partials/entry-meta.blade.php`

A reusable partial for displaying post metadata (author, date, categories, tags). Used in archive and single post templates via `@include('partials.entry-meta')`.

```blade
{{-- resources/views/partials/entry-meta.blade.php --}}

<div class="entry-meta">
  <time class="entry-meta__date" datetime="{{ get_the_date('c') }}">
    {{ get_the_date() }}
  </time>

  @if ($author = get_the_author())
    <span class="entry-meta__separator" aria-hidden="true">&middot;</span>
    <span class="entry-meta__author">
      <a href="{{ get_author_posts_url(get_the_author_meta('ID')) }}">
        {{ $author }}
      </a>
    </span>
  @endif

  @if ($categories = get_the_category())
    <span class="entry-meta__separator" aria-hidden="true">&middot;</span>
    <span class="entry-meta__categories">
      @foreach ($categories as $category)
        <a href="{{ get_category_link($category->term_id) }}">
          {{ $category->name }}
        </a>@if (! $loop->last), @endif
      @endforeach
    </span>
  @endif

  @if (has_tag())
    <span class="entry-meta__separator" aria-hidden="true">&middot;</span>
    <span class="entry-meta__tags">
      {!! get_the_tag_list('<span class="entry-meta__tag">', ', ', '</span>') !!}
    </span>
  @endif

  @if (comments_open())
    <span class="entry-meta__separator" aria-hidden="true">&middot;</span>
    <a href="{{ get_comments_link() }}" class="entry-meta__comments">
      {{ get_comments_number_text() }}
    </a>
  @endif
</div>
```

### 7. Build and verify

After all files are generated, instruct the user to run:

```bash
# Install PHP dependencies (if not already done by create-project)
composer install

# Install Node dependencies
pnpm install

# Run the initial build
pnpm build

# Start the development server with hot reload
pnpm dev
```

Verify that:
- `pnpm build` completes without errors
- The `public/` directory is populated with compiled assets
- The theme appears in WordPress admin under Appearance > Themes
- Activating the theme renders without errors
- The view composer data is available in Blade templates (check `{{ $siteName }}` renders the site name)

### 8. Summary of generated files

Present a final summary to the user listing every file created or modified beyond the base `composer create-project` output:

| File | Purpose |
|------|---------|
| `bud.config.js` | Updated for chosen CSS framework and theme public path |
| `tailwind.config.js` | Tailwind configuration with content paths (Tailwind only) |
| `postcss.config.js` | PostCSS plugin configuration (Tailwind only) |
| `resources/styles/app.css` or `app.scss` | Framework imports and theme custom styles |
| `resources/scripts/app.js` | Bootstrap JS import (Bootstrap only) |
| `app/View/Composers/App.php` | Site-wide view composer passing navigation, sidebar, and site data |
| `resources/views/components/button.blade.php` | Reusable button Blade component |
| `resources/views/partials/entry-meta.blade.php` | Post metadata partial for archives and single posts |
