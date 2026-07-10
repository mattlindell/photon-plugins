---
name: "setting-okrs-goals"
description: "Set aligned, measurable OKRs and goals: turn strategy into a small set of objectives and robust, hard-to-game key results, backed by default-on systems and a review-and-grading loop."
disable-model-invocation: true
---

# Setting OKRs & Goals

## OKRs are for focus and learning

Anchor every choice below to four ideas:

- **Alignment, one step away.** Every team objective traces to the company goal in a single hop. If it takes a five-layer cascade chart to explain the link, it's too far.
- **Obsess over the system, not the goal.** Default-on habits produce progress; a target with no recurring mechanism behind it is a wish. Be obsessed with the system that gets you there.
- **Absolute over ratio.** Prefer counts. Every ratio invites gaming by shrinking the denominator, so pair it with an absolute numerator or a volume/quality guardrail.
- **Grade to learn, not to punish.** OKRs are for focus and learning. The moment they become individual performance scores, teams sandbag targets and the signal dies.

## When to use / not

Use to set a cycle's OKRs, sharpen a weak objective or key result, run a review or mid-cycle checkpoint, or grade a cycle and run the retro.

Do **not** use when: there's no agreed strategy or North Star to anchor to (do that first — `writing-north-star-metrics` or `defining-product-vision`); you need sprint planning or a delivery plan (tickets, estimates, timelines); or OKRs are being wired to individual performance evaluation — that corrupts them, so route compensation and rating to your HR process instead.

## Pick the branch

| The user wants… | Branch |
|---|---|
| To set the OKR set for a cycle | **A — Build the OKR set** |
| To fix or sharpen a specific objective or KR right now | **B — Sharpen an OKR** |
| To run a weekly check-in or mid-cycle checkpoint | **C — Review** |
| To score the cycle and run the retro | **D — Grade + retro** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) — ask ≤5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A — Build the OKR set

The full design flow. Produce a shareable OKR set for the cycle.

1. **Frame + snapshot.** Confirm horizon, scope, strategy anchor, baseline availability, constraints, and decider. State up front that OKRs are for focus and learning, not evaluation. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** a context snapshot exists and everyone agrees what these OKRs are (and aren't) for.
2. **Map alignment (one step away).** Write a one-sentence company goal for the cycle; trace each proposed objective back to it in a single hop.
   **Done when:** for every objective you can answer "how does this move the company goal within this horizon?"
3. **Draft 1–3 objectives (outcome-first).** Write objectives as outcomes and intent, not project lists. Keep the set small; prefer customer-value language over internal activity.
   **Done when:** each objective is understandable without reading its KRs and changes what the team prioritizes weekly.
4. **Generate robust KRs.** Draft 2–5 KRs per objective, each with definition, baseline, target, window, owner, and data source. Prefer absolute metrics; for any ratio, add its absolute numerator or a denominator/quality guardrail. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** two analysts would compute each KR the same way, and targets are ambitious but not fantasy.
5. **Add default-on systems + guardrails.** Specify a recurring mechanism per objective (cadence, routine, gate, customer touchpoint) with an owner. Name 1–2 gaming or harm failure modes per KR and how you'll detect them early.
   **Done when:** each objective has at least one default-on system, and each KR has a guardrail or a "hard to game because…" note.
6. **Set the review + grading loop.** Define the weekly format, the mid-cycle checkpoint rules (what can change), and end-of-cycle scoring plus retro prompts. Then run [references/CHECKLISTS.md](references/CHECKLISTS.md), score with [references/RUBRIC.md](references/RUBRIC.md), and close with **Risks / Open questions / Next steps**.
   **Done when:** the set is shareable as-is and the loop specifies who reviews, when, and what decisions can change mid-cycle.

## Branch B — Sharpen an OKR

The workhorse. Repair a specific objective or KR without redesigning the whole set.

1. **Diagnose the weakness.** Is it a project masquerading as an objective? A vanity or ambiguous metric? A ratio that can be gamed? An orphan with no system behind it?
2. **Rewrite to the failing property.** Objective → recast as an outcome. KR → add definition, baseline, target, window, owner, data source. Ratio → add absolute numerator or a volume/quality guardrail. Orphan → attach a default-on system with an owner and cadence. Question bank and anti-gaming notes: [references/WORKFLOW.md](references/WORKFLOW.md).

**Done when:** the objective reads as an outcome, or the KR is unambiguous with baseline/target/owner/source and a named gaming failure mode plus its guardrail.

## Branch C — Review

Run a weekly check-in or the mid-cycle checkpoint. Agenda and decision rules: [references/TEMPLATES.md](references/TEMPLATES.md).

Weekly: what moved, what changed in the world, decide what to stop/start/adjust, log risks and owners. Mid-cycle: allow dropping/replacing an unmeasurable KR, adjusting a target if the baseline was wrong (document why), or adding a guardrail if gaming appears.

**Done when:** each KR has an updated on-track/off-track status and the meeting produced a short decision log, not just a status readout.

## Branch D — Grade + retro

Score each KR at cycle end (0.0 no progress → 0.3 some → 0.7 meaningful → 1.0 achieved), then run the learning retro. Prompts and grading table: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** every KR has a score, and the retro captures what blocked progress, which systems helped or were missing, and what changes next cycle — framed as learning, not blame.

## Examples

- *"Set our Q2 OKRs for the Activation team."* → **Branch A**: one-step alignment map, 1–2 outcome objectives, absolute KRs with baselines/targets, a default-on funnel review, and a weekly-plus-grading loop.
- *"This KR is 'improve conversion rate to 55%' and I think it's gameable."* → **Branch B**: pair the ratio with an absolute-volume KR and a denominator/segment-parity guardrail, and note how shrinking the denominator would fake progress.
- *"Write OKRs, but we don't have a company goal or baselines."* → out of scope to finish: gather the minimum anchor and baselines; if unavailable, offer 2–3 draft options on labeled assumptions and recommend North Star/vision work first.
