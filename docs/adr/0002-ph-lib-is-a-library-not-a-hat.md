# ph-lib is a library, not a hat

Every other plugin in this marketplace is one hat — the role someone is wearing
when they install it. `ph-lib` is deliberately not. It holds material other
plugins reference and require, plus operator tools that belong to no workflow, and
nobody installs it because of the work they are doing. It is a hard dependency of
both `ph-plan` and `ph-build`.

The alternative was keeping every plugin self-contained by duplicating shared
skills — `unslop`, `codebase-design`, `writing-for-agents` — or by shipping
abridged copies alongside the authoritative ones. Both were rejected: two copies
drift, and an abridged copy is a worse version of the skill sitting next to the
real one.

## Consequences

- **The seam has one exception, and only one.** A second library plugin, or a hat
  that starts behaving like a library, means the seam has eroded rather than been
  extended.
- **Cross-plugin references follow a two-tier rule.** A leaf skill may reference
  `ph-lib` freely, because `ph-lib` is guaranteed present. A leaf skill may never
  reference another *hat* plugin unless the reference is optional with a defined
  fallback — `diagnosing-bugs` reaching `improve-codebase-architecture` is the
  worked example, and its fallback is a hard stop flagged for a human, because an
  unattended agent facing an architectural rebuild is at a one-way door.
- **Claude Code cannot enforce this.** There is no `dependencies` field in
  `plugin.json`; the official manifest reference offers only advisory prose. The
  requirement is enforced at runtime by the `ph-build` `SessionStart` hook, which
  degrades loudly when `ph-lib` is missing, and documented in both plugin
  descriptions.
- **`ph-lib` holds two kinds of thing and states both tests.** A *primitive* is
  referenced by another plugin's router, which is what makes the dependency hard.
  An *operator tool* is invoked directly by the human and touches no work product.
  Anything satisfying neither test does not go in — that rule is what keeps this
  from becoming the `misc/` directory it replaces.
- **`ph-lib` needs no setup skill.** A useful smell test that it really is a
  library.
