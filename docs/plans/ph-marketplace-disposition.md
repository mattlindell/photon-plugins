# ph-marketplace: per-skill disposition

Every skill in `technical-director` (52), `pstack` (54), and `developer-workflow`
(3) — 109 in total — with its destination, action, and invocation flag.

Review this before any file moves.

**Actions:** `move` (relocate unchanged) · `edit` (relocate with changes) ·
`rename` · `merge` · `drop` · `new`

**Invocation:** `model` (model-invocable) · `user` (`disable-model-invocation: true`) ·
`leaf` (`user-invocable: false` — model reads it, never appears in the slash menu)

---

## technical-director → engineering (18)

| Skill | Destination | Action | Invocation | Notes |
|---|---|---|---|---|
| ask-matt | — | drop | — | Replaced by `ph-plan:intake`. A binary branch beats a 24-item menu |
| code-review | ph-build | move | model | |
| codebase-design | **ph-lib** | move | model | Primitive: referenced by `tdd` (ph-build) and `improve-codebase-architecture` (ph-plan) |
| diagnosing-bugs | ph-build | edit | model | Soften hat-to-hat handoff: use `improve-codebase-architecture` if available, else hard stop and flag for a human |
| domain-modeling | ph-plan | move | model | |
| grill-with-docs | — | drop | — | Collapsed into `grilling`, which now always writes docs |
| implement | ph-build | move | user | |
| improve-codebase-architecture | ph-plan | move | user | Output is tickets, so it plans even though it reads code |
| prototype | ph-plan | edit | model | Closes `approach` |
| research | ph-plan | edit | model | Closes `approach` |
| resolve-merge-conflicts | — | drop | — | `pstack:fix-merge-conflicts` wins per the execution-rigor rule |
| setup-matt-pocock-skills | ph-plan | rename | user | → `setup-ph-plan`. Also drops upstream nomenclature |
| tdd | ph-build | merge | model | Absorbs `pstack:tdd`. td philosophy (test-first default) + pstack escape hatch (genuinely expensive test path) |
| to-spec | ph-plan | edit | user | Closes `problem`; emits the `settled:` block; embeds `define-done` methodology when present |
| to-tickets | ph-plan | edit | user | Closes `problem`; emits a `settled:` block per ticket |
| triage | ph-plan | move | user | Closes `problem`. Stays user-invoked — this is what keeps it from competing with `intake` |
| wayfinder | ph-plan | rename | user | → `scout`. Drops its research/prototype/grilling ticket taxonomy for `closes: <dimension>` |
| wizard | ph-build | move | model | |

## technical-director → leadership (24)

All 24 move to **ph-lead** unchanged, invocation flags preserved.

`building-team-culture`, `coaching-pms`, `cross-functional-collaboration`,
`delegating-work`, `energy-management`, `engineering-culture`,
`evaluating-trade-offs`, `having-difficult-conversations`, `leadership`,
`managing-timelines`, `managing-up`, `organizational-design`,
`organizational-transformation`, `planning-under-uncertainty`,
`post-mortems-retrospectives`, `running-decision-processes`,
`running-design-reviews`, `running-effective-1-1s`, `running-effective-meetings`,
`running-offsites`, `setting-okrs-goals`, `stakeholder-alignment`,
`systems-thinking`, `team-rituals`

Two edits required in this set:

- `leadership` (the router) — its example invocation says
  `/technical-director:delegating-work`; update to `ph-lead:`.
- **Nine dangling references** across the set point at skills that exist nowhere:
  `problem-definition`, `prioritizing-roadmap`, `scoping-cutting`,
  `defining-product-vision`, `working-backwards`, `writing-prds`,
  `writing-specs-designs`, `conducting-user-interviews`, `designing-surveys`.
  `working-backwards` and `designing-surveys` have zero coverage anywhere in the
  marketplace. Delete the pointers in this pass; revisit if the `product-team`
  cleanup ever supplies real targets.

## technical-director → misc (2)

| Skill | Destination | Action | Invocation |
|---|---|---|---|
| git-guardrails-claude-code | ph-build | move | model |
| setup-pre-commit | ph-build | move | model |

## technical-director → productivity (8)

| Skill | Destination | Action | Invocation | Notes |
|---|---|---|---|---|
| caveman | ph-lib | move | user | Operator tool |
| grill-me | — | drop | — | 7-line trampoline; collapsed into `grilling` |
| grilling | ph-plan | edit | model | Collapse target. Always maintains domain docs, always emits a `settled:` block. Can close any dimension |
| handoff | ph-lib | move | user | Operator tool |
| teach | ph-lib | move | user | Operator tool. Keeps the name; the pstack skill renames instead |
| to-questionnaire | ph-plan | move | user | |
| wait-what | ph-lib | move | user | Operator tool |
| writing-for-agents | ph-lib | move | model | Primitive |

## developer-workflow (3)

| Skill | Destination | Action | Invocation | Notes |
|---|---|---|---|---|
| claude-md | ph-build | move | model | Dual-published to the internal Caffelli marketplace — mirror or consciously diverge |
| commit | ph-build | move | model | Same |
| worktree | ph-build | move | model | Same |

## pstack → public skills (31)

| Skill | Destination | Action | Invocation | Notes |
|---|---|---|---|---|
| architect | ph-build | edit | **user** | Cap fan-out. Phase C currently defaults to no human checkpoint |
| arena | ph-build | edit | **user** | Hard cap on N. Was uncapped upward |
| automate-me | ph-lib | move | user | Operator tool |
| babysit | ph-build | move | model | Not a `ph-lib` operator tool — it drives a PR to green, which is product work |
| blast-radius | ph-build | move | model | |
| bro | ph-lib | move | user | Operator tool |
| create-verification-skill | ph-build | move | model | |
| deslop | ph-build | move | model | |
| figure-it-out | ph-build | edit | model | Strip references to the dropped orchestration playbooks |
| fix-ci | ph-build | move | model | cursor-team-kit origin |
| fix-merge-conflicts | ph-build | move | model | cursor-team-kit origin. Supersedes td `resolve-merge-conflicts` |
| get-pr-comments | ph-build | move | model | cursor-team-kit origin |
| how | ph-build | move | model | |
| interrogate | ph-build | edit | **user** | Cap reviewer count |
| maintain-verification-skill | ph-build | edit | model | Uncapped: one subagent per feature file. Needs a cap |
| make-pr-easy-to-review | ph-build | move | model | cursor-team-kit origin |
| no-comments | ph-build | move | model | Brings the `comment-sicko` agent |
| poteto-mode | — | drop | — | Rewritten as the `ph-build` router. Its autonomy stance is correct for an unattended harness; its unconditional fan-out triggers are not |
| recall | ph-lib | move | user | Operator tool |
| reflect | ph-lib | edit | user | Operator tool. Hard-codes 3 reviewers + 1 synthesizer — the only fixed N in pstack |
| setup-pstack | ph-build | rename | user | → `setup-ph-build`. Rewritten for the tier ladder and harness detection; proposes a mapping and asks for confirmation |
| show-me-your-work | ph-build | edit | model | Spawns a cross-model reviewer every run — make that conditional |
| swarm | ph-build | edit | **user** | No default N and no cap today. Needs both |
| tdd | — | merge | — | Merged into `ph-build:tdd` |
| teach | ph-build | rename | model | → `explain`. Sits next to `how`/`why`, which it calls — no cross-plugin edge |
| technical-writing | ph-lib | move | model | Primitive |
| thermo-nuclear-code-quality-review | ph-build | edit | user | Fans out via `swarm`; inherits the new cap |
| typescript-best-practices | ph-build | move | model | Keeps its `paths:` frontmatter |
| unslop | ph-lib | move | model | Primitive. "Must always apply" — referenced by both routers |
| what-did-i-get-done | ph-lib | move | user | Operator tool. cursor-team-kit origin |
| why | ph-build | edit | model | Up to 7 investigators + synthesizer. Cap it |

## pstack → principles (23)

All 23 move to **ph-build** as `leaf` (`user-invocable: false`), lightly edited.

`attack-the-premise`, `boundary-discipline`, `build-the-lever`,
`encode-lessons-in-structure`, `exhaust-the-design-space`, `experience-first`,
`fix-root-causes`, `foundational-thinking`, `guard-the-context-window`,
`laziness-protocol`, `make-operations-idempotent`,
`migrate-callers-then-delete-legacy-apis`, `minimize-reader-load`,
`model-the-domain`, `never-block-on-the-human`, `outcome-oriented-execution`,
`prove-it-works`, `redesign-from-first-principles`,
`separate-before-serializing-shared-state`, `sequence-verifiable-units`,
`subtract-before-you-add`, `test-behavior-not-implementation`,
`type-system-discipline`

The six that push toward acting without a checkpoint — `never-block-on-the-human`,
`exhaust-the-design-space`, `build-the-lever`, `guard-the-context-window`,
`redesign-from-first-principles`, `outcome-oriented-execution` — stay as written.
They are correct for an unattended harness. Their inverses live in the `ph-plan`
principle set.

`guard-the-context-window` needs one edit: it currently makes fan-out the default
response to any large read, with no cost ceiling.

## New skills (8)

| Skill | Plugin | Invocation | Purpose |
|---|---|---|---|
| intake | ph-plan | model | Router. Binary branch: `scout`-style frontier mapping, or straight to `grilling`. Short description, short body |
| define-done | ph-plan | user | Closes `verification`. Soft precondition on the other three. Produces one methodology shared by every ticket in the set |
| principle-block-on-the-human | ph-plan | leaf | Explicit inverse of the ph-build rule |
| principle-walk-the-tree | ph-plan | leaf | Ask the whole frontier; never guess at an answer that unblocks an unasked question |
| principle-close-or-block-the-dimension | ph-plan | leaf | Every dimension ends settled or as a named decision ticket |
| principle-write-it-down | ph-plan | leaf | An unrecorded decision did not happen |
| principle-name-the-destination | ph-plan | leaf | Know what done looks like before decomposing |
| principle-one-way-doors-first | ph-plan | leaf | Sequence irreversible decisions early. Shared concept with the ph-build cost gate |

## pstack playbooks (23 → 19)

Dropped: `orchestrate` ("dozens to hundreds of subagents"), `autopilot-full`,
`autopilot-stack`, `multi-phase-plan` (13 swarm lanes per PR head, and it
duplicates `scout`).

Kept, with `opening-a-pr` edited: it currently appends `interrogate` + `/deslop` +
`/no-comments` to the tail of **every** playbook — a flat +4 agents on every run.
Make it conditional on the one-way-door gate.

Remaining 19: `authoring-a-skill`, `autonomous-run`, `babysit`, `bug-fix`, `eval`,
`feature`, `hillclimb`, `investigation`, `opening-a-pr`, `pause-safely`,
`perf-issue`, `prototype`, `refactoring`, `runtime-forensics`, `session-pickup`,
`shipping`, `trace-forensics`, `visual-parity`, `worktree-cleanup`

`feature` also needs its step 4 relaxed — delegation is currently "Mandatory: no
skip-with-reason escape."

## Agents (4 → 3)

| Agent | From | Destination | Notes |
|---|---|---|---|
| implement | technical-director | ph-build | Update declared skills to `ph-build:` |
| code-review | technical-director | ph-build | Same |
| comment-sicko | pstack | ph-build | Invoked by `no-comments` |
| poteto-agent | pstack | — | Dropped with `poteto-mode` |

## Accounting

| | Count |
|---|---|
| ph-build | 32 skills + 23 principles + 19 playbooks + 3 agents |
| ph-plan | 11 moved + 2 new + 6 new principles |
| ph-lib | 4 primitives + 9 operator tools |
| ph-lead | 24 |
| Dropped | 5 (`ask-matt`, `grill-with-docs`, `grill-me`, `resolve-merge-conflicts`, `poteto-mode`) |
| Merged away | 1 (`pstack:tdd`) |
| **Total accounted** | **109** |

Unchanged and outside this table: `ph-pm` (8), `ph-php` (12 + 4 commands + 3
agents), `ph-npo` (7), `product-team` (17, deferred).

## Open items carried into implementation

- `nonprofit-toolkit`: the marketplace says 6 skills, disk has 7
  (`givebutter-integration`). Fix during its rename.
- The three `developer-workflow` skills are dual-published to the internal
  Caffelli marketplace with different author metadata. Folding them into
  `ph-build` means deciding what happens to that copy.
- Every capped skill needs its cap chosen, not merely marked. Defaults proposed
  at implementation time.
