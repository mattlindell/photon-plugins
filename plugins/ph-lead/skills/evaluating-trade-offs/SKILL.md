---
name: "evaluating-trade-offs"
description: "Evaluate a leadership or product trade-off: compare options on all-in cost and opportunity cost, estimate impact as ranges, and reach a decision-ready recommendation with stop/continue triggers."
disable-model-invocation: true
---

# Evaluating Trade-offs

## Turn the debate into a decision

Anchor every choice below to four ideas:

- **All-in cost, not the sticker price.** Compare options on total cost - cash, people-time, maintenance, coordination, switching - plus what you give up elsewhere (opportunity cost), never the obvious line item alone.
- **Order of magnitude beats false precision.** Estimate impact as ranges with a confidence label. A 10x difference decides; a 2% difference is noise inside your error bars, so don't let it drive the call.
- **Think more, build less.** Most "experiments" should start as thought experiments - a pre-mortem and the cheapest test that could falsify your biggest assumption - before anyone writes code.
- **Sunk costs are gone; worse-first is normal.** Continuation turns on future ROI and strategic fit, never on what's already spent. If the right path dips before it climbs, plan the dip instead of reversing it.

## When to use / not

Use to evaluate a specific trade-off, compare 2-4 options, decide whether to stop or continue an existing effort, or manage a speed-vs-quality call.

Do **not** use for: clarifying what problem you're solving (use `problem-definition`); a full cross-functional decision process with decision rights and a decision log (use `running-decision-processes`); prioritizing across many initiatives (use `prioritizing-roadmap`); cutting scope to hit a date (use `scoping-cutting`); or a personal, legal, HR, or financial decision - route to a qualified human.

## Pick the branch

| The user wants... | Branch |
|---|---|
| To make a specific call now (reversible / time-boxed) | **A - Quick trade-off call** |
| A rigorous evaluation of a high-stakes or one-way-door decision | **B - Full evaluation** |
| To decide whether to keep investing or stop (sunk cost) | **C - Stop or continue** |
| To weigh shipping now vs polishing (speed vs quality) | **D - Speed vs quality** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) - ask <=5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A - Quick trade-off call

The workhorse. Produce a one-page call, not a pack.

1. **Frame it in one sentence.** "We are choosing X vs Y by DATE to achieve GOAL." Name the owner and who lives with the outcome.
2. **Score only what differs.** Pick the 2-3 criteria on which the options actually diverge (include one guardrail); skip everything they tie on.
3. **Size it order-of-magnitude.** Is one option plausibly 10x better, or are they within the error bars? Name the one assumption that would flip the answer. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
4. **Make the call.** State the pick, the opportunity cost you're accepting, and a review date.

**Done when:** the decision, the accepted trade-off, and a review date fit on one page, and a reader can act without reopening the debate.

## Branch B - Full evaluation

For high-stakes or one-way-door decisions. Produce a written evaluation a stakeholder can decide from async. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Frame the trade-off.** One-sentence decision, why now, owner, constraints, non-negotiables, and time horizon.
   **Done when:** you can answer what you're deciding, by when, and for what outcome.
2. **Define what you're optimizing.** Pick 4-8 criteria including at least one guardrail (trust, reliability, cost, support load); name what you're explicitly *not* optimizing for.
   **Done when:** criteria reflect real trade-offs and the horizon is explicit.
3. **Build the all-in cost view.** Estimate total cost per option (cash, people-time, engineering, maintenance, coordination) and the opportunity cost - what gets displaced.
   **Done when:** hidden costs (on-call, tooling, cross-team coordination, switching) are included and comparable across options.
4. **Estimate impact as ranges.** Give upside/downside ranges with confidence; name the 2-3 assumptions that drive the model.
   **Done when:** no fake decimals, and a few named drivers explain the decision.
5. **Run the thought experiments.** Pre-mortem the top 1-2 options; design the cheapest test that could falsify the biggest assumption, and decide whether a build is even warranted.
   **Done when:** any proposed test is the smallest that could change your mind.
6. **Plan worse-first + triggers.** Name any short-term dip and its mitigations/leading indicators; set stop/continue triggers and a review date.
   **Done when:** the dip is anticipated and continuation logic ignores sunk costs.
7. **Recommend and gate.** Write the recommendation with rationale and explicit trade-offs (what you'll stop doing), plus Risks / Open questions / Next steps with owners. Gate with [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md).
   **Done when:** a stakeholder can decide async without re-litigating the debate.

## Branch C - Stop or continue

For continuation decisions on an existing effort. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Reset on sunk cost.** Ask: "If we weren't already doing this, would we start today with what we know now?"
2. **Compare forward, not backward.** Estimate the remaining all-in cost to finish against future ROI and strategic fit; ignore what's already spent.
3. **Set the rule.** Define stop/continue triggers and a review date. If stopping, decide what to salvage (reusable work, learnings, comms) and how to avoid the repeat failure mode.

**Done when:** there's a clear stop/continue verdict with kill criteria and a review date, and the logic never cites sunk cost as a reason to continue.

## Branch D - Speed vs quality

For ship-now-vs-polish calls. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Separate the guardrails from the trade.** Name what quality protects (trust, reliability, support load) and which of those you can safely trade now.
2. **Size the worse-first dip.** Estimate the short-term degradation if you ship now and why the long-term upside beats it.
3. **Instrument the dip.** Set leading indicators and mitigations so the team doesn't reverse prematurely, and define what would make you pull back.

**Done when:** the ship decision is explicit, the guardrail line is drawn, and a dip-mitigation plan with leading indicators is in place.

## Examples

- *"Should we invest in SEO or paid acquisition for the next two quarters?"* -> **Branch B**: all-in cost per channel, order-of-magnitude impact ranges, recommendation with a review date.
- *"Ship v1 next week rough, or delay three weeks to ship it polished?"* -> **Branch D**: guardrails that quality protects, an expected dip plan, and pull-back triggers if support load spikes.
- *"Should I leave my job?"* -> out of scope: this skill is for organizational and product leadership trade-offs; suggest a personal decision framework or a coach instead.
