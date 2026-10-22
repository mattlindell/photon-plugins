# ph-php

A Claude Code plugin for PHP development covering WordPress, Laravel, Sage/Roots, WooCommerce, and CodeIgniter 3 legacy maintenance. It provides sixteen skills (four for architecture decisions and troubleshooting, twelve for implementation patterns) and four commands for scaffolding new projects.

**Version:** 3.0.0
**Author:** Matt Lindell
**License:** MIT

---

## Plugin Structure

```text
plugins/ph-php/
  .claude-plugin/
    plugin.json
  skills/
    composer-dependency-management/SKILL.md
    database-patterns/SKILL.md
    laravel-api-patterns/SKILL.md
    laravel-architecture/
      SKILL.md
      references/{queues-and-events,enterprise,sage-roots}.md
    laravel-patterns/SKILL.md
    legacy-ci3-maintenance/SKILL.md
    php-architecture/SKILL.md
    php-security-hardening/SKILL.md
    php-testing-patterns/SKILL.md
    sage-patterns/SKILL.md
    woocommerce-patterns/SKILL.md
    wordpress-architecture/
      SKILL.md
      references/{performance,multisite,woocommerce,headless,devops,migration,scaling}.md
    wordpress-plugin-patterns/SKILL.md
    wordpress-theme-patterns/SKILL.md
    wordpress-troubleshooting/SKILL.md
    wp-rest-api-patterns/SKILL.md
  commands/
    laravel-new.md
    sage-theme.md
    wp-plugin.md
    wp-theme.md
```

---

## Skills

Every skill is model-invoked: Claude reaches for it when a task matches its description. The four decision skills each have an `agents/openai.yaml` portability sidecar.

### Decision skills

These skills choose an approach and state its tradeoffs. They hold almost no code; they point at the pattern skills for it.

| Skill | Description |
| --- | --- |
| **wordpress-architecture** | WordPress architecture decisions: caching and Core Web Vitals, multisite, WooCommerce architecture and scaling, headless, hosting and deployment, migration and upgrades, and infrastructure scaling. |
| **wordpress-troubleshooting** | Diagnostic procedure for a broken WordPress site: debug setup, white screens and 500s, 403/404s, database connection errors, memory exhaustion, plugin conflicts, cron, and AJAX. |
| **laravel-architecture** | Laravel and Sage/Roots architecture decisions: application structure, Eloquent model design, queues and events, design and enterprise patterns, performance strategy, and Sage, Acorn, Bud, and Bedrock. |
| **php-architecture** | Framework-agnostic PHP decisions: type and static-analysis policy, architecture patterns, runtime performance, async and long-running PHP, and the quality gate. |

### Pattern skills

These skills provide concrete implementation patterns and code examples.

| Skill                              | Description                                                                                                                                                                                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **composer-dependency-management** | Composer dependency management -- version constraints, autoloading, private packages, WPackagist for WordPress, Bedrock-style WordPress, and retrofitting Composer onto legacy CI3 projects.              |
| **database-patterns**              | Database query and optimization patterns for Eloquent (Laravel/Sage), WordPress ($wpdb, WP_Query, meta queries), and CodeIgniter 3 Query Builder. Covers migrations, N+1 optimization, and custom tables. |
| **laravel-api-patterns**           | Laravel API development -- API Resources, Sanctum token authentication, rate limiting, route groups, exception handling, webhook receivers, and cursor pagination.                                        |
| **laravel-patterns**               | Laravel implementation patterns -- service providers, middleware, Form Requests, API Resources, Eloquent models, jobs with retry logic, events and listeners, and action classes.                         |
| **legacy-ci3-maintenance**         | Safe maintenance patterns for CodeIgniter 3 legacy applications -- MVC conventions, avoiding regressions, incremental improvements, and security patching.                                                |
| **php-security-hardening**         | PHP security patterns organized by framework -- universal PHP, WordPress (nonces, capabilities, escaping), Laravel (Form Requests, guards, Sanctum), and CI3 legacy hardening.                            |
| **php-testing-patterns**           | PHP testing with PHPUnit, Pest, WordPress test framework (WP_UnitTestCase), Laravel test helpers, Sage testing, and CI3 legacy testing.                                                                   |
| **sage-patterns**                  | Sage/Roots theme patterns -- Acorn service providers, Bud asset configuration, Blade components in WordPress, view composers, and common Sage gotchas.                                                    |
| **woocommerce-patterns**           | WooCommerce development -- checkout field customization, cart/order hooks, custom product types, payment gateway skeleton, and HPOS compatibility.                                                        |
| **wordpress-plugin-patterns**      | WordPress plugin development -- OOP architecture with PSR-4, hook registration, activation/deactivation lifecycle, Gutenberg blocks, AJAX handlers, WP-CLI commands, and custom post types.               |
| **wordpress-theme-patterns**       | WordPress theme development for classic themes (template hierarchy, functions.php, child themes), block/FSE themes (theme.json, block templates), and hybrid approaches.                                  |
| **wp-rest-api-patterns**           | WordPress REST API -- registering custom endpoints, permission callbacks, schema validation, response formatting, extending existing endpoints, and webhook handling.                                     |

---

## Commands

Commands are interactive scaffolding workflows that generate production-ready project structures.

| Command         | Description                                                                                                                                     |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **laravel-new** | Scaffolds a new Laravel application with clean architecture, including optional API, queue, and testing configurations.                         |
| **sage-theme**  | Guides setup of a new Sage 10+ theme with CSS framework configuration, view composers, Blade components, and partials.                          |
| **wp-plugin**   | Generates a production-ready OOP WordPress plugin with PSR-4 autoloading, namespaced classes, lifecycle hooks, and Coding Standards compliance. |
| **wp-theme**    | Scaffolds a classic WordPress theme with all essential template files, Composer autoloading, and optional WooCommerce or hybrid FSE support.    |

---

## How Skills and Commands Relate

- **Decision skills** answer *what* and *why*: which caching layer, whether to go headless, how to design a queue topology, or how to diagnose a broken site.
- **Pattern skills** answer *how*, with working code for one framework area.
- **Commands** generate a complete project structure from scratch, combining knowledge from several pattern skills.

---

## Installation

**From a plugin marketplace:**

```bash
claude plugin install ph-php
```

**For local development (point to the plugin directory):**

```bash
claude --plugin-dir /path/to/plugins/ph-php
```

---

## Acknowledgments

Plugin structure and approach inspired by [wshobson/agents](https://github.com/wshobson/agents), particularly the [python-development](https://github.com/wshobson/agents/tree/main/plugins/python-development) plugin. Their work on organizing Claude Code plugins into agents, skills, and commands provided the blueprint for this PHP-focused adaptation.
