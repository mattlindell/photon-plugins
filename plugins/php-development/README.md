# php-development

A Claude Code plugin for PHP development covering WordPress, Laravel, Sage/Roots, WooCommerce, and CodeIgniter 3 legacy maintenance. It provides three specialized agents for architecture decisions, twelve skills for implementation patterns, and four commands for scaffolding new projects.

**Version:** 1.0.0
**Author:** Matt Lindell
**License:** MIT

---

## Plugin Structure

```text
plugins/php-development/
  .claude-plugin/
    plugin.json
  agents/
    wordpress-master.md
    laravel-specialist.md
    php-pro.md
  skills/
    composer-dependency-management/SKILL.md
    database-patterns/SKILL.md
    laravel-api-patterns/SKILL.md
    laravel-patterns/SKILL.md
    legacy-ci3-maintenance/SKILL.md
    php-security-hardening/SKILL.md
    php-testing-patterns/SKILL.md
    sage-patterns/SKILL.md
    woocommerce-patterns/SKILL.md
    wordpress-plugin-patterns/SKILL.md
    wordpress-theme-patterns/SKILL.md
    wp-rest-api-patterns/SKILL.md
  commands/
    laravel-new.md
    sage-theme.md
    wp-plugin.md
    wp-theme.md
```

---

## Agents

Agents make architecture decisions, diagnose problems, design scaling strategies, and route to the appropriate skills when implementation details are needed.

| Agent                  | Description                                                                                                                                                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **wordpress-master**   | WordPress architecture, performance optimization, and troubleshooting expert. Handles site architecture, multisite design, WooCommerce scaling, migration strategy, headless WordPress, DevOps, and debugging.                                                  |
| **laravel-specialist** | Laravel and Sage/Roots architecture expert. Handles Eloquent modeling, queue/event system design, enterprise patterns, and the full Roots ecosystem (Sage, Acorn, Bud, Bedrock). Covers both standalone Laravel and Laravel-in-WordPress.                       |
| **php-pro**            | Modern PHP 8.3+ expert for cross-framework concerns. Handles type system mastery, PSR standards, design patterns, async programming, performance tuning, and CodeIgniter 3 legacy maintenance. First responder when a task is not clearly WordPress or Laravel. |

---

## Skills

Skills provide concrete implementation patterns, code examples, and best practices that agents route to during development work.

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

## How Agents, Skills, and Commands Relate

The plugin is organized into three layers that work together:

- **Agents** operate at the architecture level. They evaluate requirements, make design decisions, diagnose problems, and plan strategies. When implementation details are needed, agents route to the appropriate skill. Agents also hand off to each other when a question crosses framework boundaries (for example, wordpress-master hands Sage questions to laravel-specialist).

- **Skills** operate at the implementation level. They contain concrete code patterns, best practices, and framework-specific recipes. Skills are invoked by agents (or directly) when you need working code rather than architectural guidance.

- **Commands** operate at the project creation level. They are interactive scaffolding workflows that generate complete, production-ready project structures from scratch. Commands combine knowledge from multiple skills to produce properly organized codebases with all boilerplate in place.

---

## Installation

**From a plugin marketplace:**

```bash
claude plugin install php-development
```

**For local development (point to the plugin directory):**

```bash
claude --plugin-dir /path/to/plugins/php-development
```

---

## Acknowledgments

Plugin structure and approach inspired by [wshobson/agents](https://github.com/wshobson/agents), particularly the [python-development](https://github.com/wshobson/agents/tree/main/plugins/python-development) plugin. Their work on organizing Claude Code plugins into agents, skills, and commands provided the blueprint for this PHP-focused adaptation.
