# ph-lead

**Engineering leadership and people management.** Twenty-four skills with a
router.

This is the hat you wear when the work is people, teams, and decisions rather
than code. It shares no vocabulary and no workflow with the development plugins,
which is exactly why it is its own install.

Standalone — depends on no other plugin.

## Start here

**`leadership`** is the router. Describe the situation and it points at the
right skill. Most skills here are user-invoked, so the router tells you what to
type.

## Skills

**People** — `running-effective-1-1s`, `having-difficult-conversations`,
`delegating-work`, `coaching-pms`

**Teams** — `building-team-culture`, `engineering-culture`, `team-rituals`,
`running-offsites`, `post-mortems-retrospectives`

**Org** — `organizational-design`, `organizational-transformation`,
`systems-thinking`

**Decisions** — `running-decision-processes`, `evaluating-trade-offs`,
`planning-under-uncertainty`, `running-design-reviews`

**Delivery** — `managing-timelines`, `setting-okrs-goals`

**Across and upward** — `managing-up`, `stakeholder-alignment`,
`cross-functional-collaboration`

**Yourself** — `energy-management`

**Router** — `leadership`

Every skill except the router carries a `references/` set: `INTAKE.md`,
`WORKFLOW.md`, `TEMPLATES.md`, `CHECKLISTS.md`, `RUBRIC.md`.

## Known gaps

Nine cross-references in this set point at skills that do not exist anywhere in
the marketplace — `problem-definition`, `prioritizing-roadmap`,
`scoping-cutting`, `defining-product-vision`, `working-backwards`,
`writing-prds`, `writing-specs-designs`, `conducting-user-interviews`,
`designing-surveys`. They appear as "do not use this for X, use Y instead"
pointers, so the guidance still reads correctly; the target just is not there.

These are deliberately left alone in the reorganization and tracked as separate
improvement work on this plugin.

## Structure

```text
ph-lead/
  .claude-plugin/plugin.json
  skills/
    leadership/              — the router
    <23 skills>/
      references/            — INTAKE, WORKFLOW, TEMPLATES, CHECKLISTS, RUBRIC
```

## Attribution

Adapted from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills)
(MIT), distilled from Lenny's Podcast, and since substantially rewritten.
