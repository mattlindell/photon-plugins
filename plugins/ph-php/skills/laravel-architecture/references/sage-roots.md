# Sage and Roots decisions

Code and the known Sage gotchas are in `sage-patterns`.

## Which pieces to adopt

| Tool | Adopt when | Watch for |
| --- | --- | --- |
| Bedrock | Any WordPress site managed with Composer: plugins as dependencies, config in `.env`, and a `web/` document root separate from config | Hosts with a fixed directory layout may not allow the custom document root |
| Sage | A developer-built theme, for a team comfortable with Blade and a build step | Choose a block theme instead when the design should be editable in the Site Editor |
| Acorn | Theme or plugin code that benefits from service providers, config, and Blade; it works without Sage | Run one Acorn per site. Require it at the project level (Bedrock's `composer.json`); a distributable plugin that bundles its own Acorn conflicts with any other copy. |
| Bud | Sage 10 themes | Sage 11 replaced Bud with Vite. Keep Bud on existing Sage 10 themes, and start new themes on the current Sage. |

## Blade and the template hierarchy

The WordPress template hierarchy still picks the template; Sage maps each
template to a Blade view. Keep that hierarchy-based routing instead of adding a
router to the theme. Build reusable UI as Blade components, and supply data
through view composers rather than queries inside templates.

## The container inside WordPress

- Bind services in Acorn service providers. Register WordPress hooks in a
  provider's `boot()`.
- Resolve services in view composers, not in Blade templates.
- Read WordPress content through `WP_Query` and the WordPress APIs, which honor
  hooks (`pre_get_posts`) and the object cache. Eloquent over `wp_` tables
  bypasses both. Use Eloquent only for custom tables.
