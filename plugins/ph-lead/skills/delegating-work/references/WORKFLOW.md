# Delegation Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Principles (the checks behind the stance)

1. **Delegate outcomes, not tasks.** Hand over the "what," the "why," and the guardrails; leave the "how" to the owner.
   *Check:* the owner can restate the problem, constraints, and definition of done in their own words — not just repeat a task list.
2. **Match authority to readiness.** Pick the level of delegation from the person's experience with this kind of work, not a blanket policy.
   *Check:* for each workstream you can name why the level is recommend vs. decide-with-guardrails vs. fully own.
3. **Delegate to grow, not just to offload.** Choose owners and work partly for their learning value.
   *Check:* you can say what this person will be able to own next as a result.
4. **Stay accountable without taking it back.** You own the outcome; you review through artifacts and criteria, not by dictating the path.
   *Check:* your feedback is framed as constraint/quality-bar/impact, and ownership doesn't snap back to you after delivery.

## Anti-patterns (catch yourself)

- **Dumping, not delegating.** Handing over a task with no outcome, context, or authority is abdication. Give the "why" and the definition of done, or don't hand it over.
- **Reverse-delegation (taking it back).** The owner brings you a problem and you leave the meeting owning it. Hand the monkey back: "what's your recommendation?"
- **Delegating, then micromanaging.** Assigning ownership and then dictating the sequence of tasks or rewriting the work. Review criteria, not keystrokes.
- **Level-mismatched authority.** "Fully own" on a high-risk, unfamiliar task sets the person up to fail; "recommend only" on routine work they've mastered insults them and clogs you.
- **Vibes-based escalation.** "Pull me in if it feels risky" gives no threshold. Escalation triggers must be specific and observable.
- **Fake autonomy.** Saying "you decide" and then overriding decisions that were inside the guardrails. New constraints or new evidence are the only valid reasons to overrule.
- **Ownership that snaps back.** Delivery happens, but maintenance and the next iteration quietly return to you. Assign durable ownership explicitly.

## Levels of delegation (delegation poker)

Make the level explicit — "you own it" means nothing without it. Pick one per workstream:

- **Recommend:** owner researches and recommends; you decide.
- **Decide with guardrails:** owner decides inside stated constraints and informs you.
- **Fully own:** owner decides and executes; you're informed at milestones.

Heuristics:

- Raise autonomy when the failure cost is low and the learning value is high.
- Lower autonomy when safety, compliance, reputation, or customer-trust risk is high — but still avoid prescribing the exact path; tighten the guardrails instead.
- Autonomy is per-workstream, not per-person: the same owner can be "fully own" on one slice and "recommend" on another.

## Match authority to readiness (task-relevant maturity)

Readiness is task-specific, not a global trait. Someone senior can be low-readiness on an unfamiliar problem, and a junior can be high-readiness on work they've done before.

- **Low readiness (new to this work):** more structure, tighter guardrails, shorter check-in loops, more shared context up front.
- **High readiness (proven on this work):** more autonomy, milestone-only check-ins, artifact reviews rather than step reviews.
- Recalibrate as you go — raise the level as the owner demonstrates judgment; drop it (with a reason) if a guardrail is breached.

## Ownership map (RACI / DRI)

For anything with more than one contributor, make ownership unambiguous:

- **DRI (single owner):** one directly responsible individual per outcome — the person accountable, not a committee.
- **RACI:** who is Responsible, Accountable (one name), Consulted, and Informed.
- Watch for the two failure shapes: **no owner** (everyone assumes someone else has it) and **too many owners** (diffused accountability, slow decisions).

## Context transfer — "context, not control"

Give the owner enough to reason independently:

- Background and why now.
- Prior decisions and "why we didn't do X."
- Stakeholders and their incentives.
- Known gotchas and pitfalls.
- Example outputs — what "good" looks like.

Then have the owner restate the problem and propose the first steps before you agree on cadence.

## Decision rights & escalation triggers

Guardrails should cover:

- **Quality bar:** what must be true in the output.
- **Non-negotiables:** policy, compliance, security, customer promises.
- **Escalation triggers:** specific thresholds that pull you in.
- **Review points:** when you'll look at artifacts — not daily task updates.

Examples of specific triggers:

- "Any change that impacts pricing or packaging."
- "Any external customer communication."
- "Any security-control change."
- "Any timeline slip greater than one week."

## Monitoring cadence

Create predictability without control:

- Short, frequent check-ins early; taper as the owner stabilizes.
- Default agenda: progress vs. outcome, decisions made/needed, risks, asks.
- "Refuse to rule" unless an escalation trigger fires or the work drifts from the outcome or guardrails.
- Good milestones are outcome-linked: "draft spec reviewed," not "met with team"; "experiment launched," not "built dashboard."

## Reviewing without micromanaging

Be accountable for quality while preserving ownership:

- Review artifacts against criteria (acceptance, risks, customer impact) — not the sequence of tasks.
- Frame feedback as **constraint → quality bar → impact**, not "do it my way."
- Separate style preference from non-negotiable requirement, and say which is which.

Signals you've crossed into micromanagement:

- You're dictating the order of tasks.
- You're rewriting the work instead of giving criteria-based feedback.
- The owner has stopped bringing options and only asks for instructions.

## Debrief & durable ownership

Make delegation compounding. After delivery, ask:

- Which assumptions were wrong?
- Which guardrails were missing?
- What should we template for next time?
- What should the owner own going forward — including maintenance and the next iteration?

Output: a short debrief note plus an updated "who owns what" statement so nothing quietly reverts to you.
