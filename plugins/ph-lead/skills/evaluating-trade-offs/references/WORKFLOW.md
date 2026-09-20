# Trade-off Playbook (Heuristics)

Topic-keyed heuristics and defaults for the branches in `../SKILL.md`. Adjust every default to your context.

## Rigor dial (match process to stakes)

- **Quick (30-60 min):** reversible, small-stakes decisions. Frame, the 2-3 criteria that differ, order-of-magnitude impact, and a review date. This is Branch A.
- **Standard (2-4 hours):** meaningful resource allocation or customer impact. Add all-in cost / opportunity cost and a minimal validation plan.
- **Deep (multi-day):** one-way-door, high-stakes decisions. Consider `running-decision-processes` for decision rights, stakeholder alignment, and a full decision log.

## All-in cost + opportunity cost

Evaluate each option on total cost, not the obvious line item, and always against the next-best use of the same resources.

- If an option needs engineering, include integration, migrations, QA, on-call, and long-term maintenance.
- If an option needs headcount, include recruiting time, ramp, management overhead, and coordination.
- State the opportunity cost as a sentence: "If we pick A, we stop or defer B."

## Order of magnitude over false precision

Use ranges and confidence; prefer 10x comparisons over 1-2% differences when uncertainty is high.

- Use best / expected / worst (or min / likely / max) ranges.
- Record the top 2-3 assumptions that drive the decision; don't spread effort evenly across minor details.
- If two options sit inside each other's error bars, the numbers aren't deciding - pick on a guardrail or reversibility instead.

## Thought experiments first (think more, build less)

Most experiments should start as thought experiments; only build when the result could change the decision.

- Run a pre-mortem: "This failed - what happened?"
- Design the cheapest test that could falsify your biggest assumption (data pull, five customer calls, a timeboxed spike).
- Don't ship an "obvious loser" experiment to prove a point you already believe.

## Worse-first is normal - plan the dip

Many good decisions have a short-term downside before the long-term upside. If you choose a worse-first path, plan the dip explicitly.

- Identify the likely short-term degradation (support load, velocity slowdown, revenue dip).
- Define leading indicators and mitigations so the team doesn't panic and reverse prematurely.
- Decide in advance what would make you genuinely pull back, so a normal dip isn't mistaken for failure.

## Sunk costs don't justify future spend

For continuation decisions, ignore sunk costs and ask: "Would we start this today with what we know now?"

- Compare remaining cost-to-finish against future ROI and strategic fit.
- Define stop/continue triggers and a review date.
- If stopping, decide what to salvage (code reuse, learnings, comms) and how to prevent the repeat failure mode.

## Communication (trade-offs don't land without narrative)

Include a short trade-off narrative in any pack:

- What we're optimizing for and why.
- What we are *not* optimizing for, and the cost of that choice.
- What changes tomorrow - who does what, what stops, what starts.
- When we'll review, and what would cause a change of course.

## Anti-patterns (catch yourself)

- **Deciding on the sticker price.** Comparing headline dollars while ignoring maintenance, coordination, and switching costs picks the option that looks cheap and isn't.
- **False precision.** Two decimal places on a number built from three guesses. Ranges and a confidence label are more honest and more useful.
- **Building to decide.** Spinning up a real experiment when a pre-mortem or a data pull would have answered it. Think first; build only when the result could flip the call.
- **Honoring sunk cost.** "We've already put six months in" is not a reason to continue. Only future ROI is.
- **Reversing on the dip.** Killing a good worse-first decision the moment it gets worse, before the planned upside had a chance to arrive.
- **Criteria inflation.** Scoring on ten criteria where the options tie on eight of them buries the two that actually decide.
