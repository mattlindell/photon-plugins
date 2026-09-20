# `agents/` are connector wrappers, not method holders

A file in a plugin's `agents/` directory exists so a third-party ACP connector
can trigger a skill automatically. That is its whole purpose. It names the entry
condition — what kind of handoff should wake it — and points at the skill or
playbook that does the work. It carries no method of its own.

`ph-build/agents/code-review.md` is the reference shape. It states the entry
condition, says the method lives in `/ph-build:code-review`, and covers only what
a bare PR handoff leaves the skill missing: the fixed point and the spec.

The alternative was letting an agent file hold its own process, which is what
`ph-build/agents/implement.md` did. It grew a full seven-step implementation
procedure, a definition of done, a report format, and edge cases, in parallel
with `dispatch` and contradicting it on six axes — human reachability, seam
confirmation, rigor sizing, the one-way-door gate, PR authority, and principles.
The same ticket produced different work depending on whether it arrived through
the `SessionStart` hook or through an `Agent` call. Two documents describing one
job will diverge; the only question is how long before someone notices.

## Consequences

- **The drift is detectable.** An agent file that describes *how* rather than
  *when* has drifted. Length is the cheap proxy: a wrapper is tens of lines, not
  hundreds.
- **Every agent declares the skill it wraps.** The `skills:` frontmatter names
  the target, so the pointer is machine-readable rather than buried in prose.
- **A wrapper with no skill behind it is a missing skill.** The fix is to write
  the skill and point at it, not to let the wrapper keep the method.
- **`ph-php`'s three agents violate this.** They run 144, 198, and 279 lines and
  declare no `skills:`. They are method-holders and are tracked for cleanup
  separately — a different plugin and a different hat.
- **`comment-sicko` is the edge case.** It is a persona rather than a procedure,
  invoked only by `no-comments`, and at 32 lines it holds no process worth
  extracting. A persona that stays short is within the rule.
