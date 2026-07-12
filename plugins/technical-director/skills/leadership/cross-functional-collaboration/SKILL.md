---
name: "cross-functional-collaboration"
description: "Align teams that work across functions - stand up or repair how they work together, defuse a live cross-team conflict, unblock a stalled dependency, or fix slow and re-litigated decisions. Use when the user mentions cross-functional friction, working with Engineering/Design/Product/Data, teams thrashing or misaligned, unclear ownership or decision rights, a partner team that keeps blocking or slipping, or turf and credit tensions between teams."
---

# Cross-functional Collaboration

## Make the implicit explicit

Anchor every choice below to four ideas:

- **Make the implicit explicit.** Cross-team friction is almost always unstated goals, decision rights, or expectations - the fix is to write them down, not to hold another meeting.
- **Map by decision, not org chart.** Name who decides what and who must execute or sign off. Ambiguous ownership is the root cause of most thrash.
- **Trust is a system you install.** Conflict norms and shared credit are mechanisms you design before you need them, not personality traits you hope for.
- **Attack the cause, not the moment.** Repeated conflict or a chronic blocker is usually a missing decision right, a metric clash, or a misaligned incentive. Fix that, not the flare-up.

## When to use / not

Use to stand up or repair how cross-functional teams work together, to defuse a live conflict between functions, to unblock a stalled dependency, or to fix slow and re-litigated decisions.

Do **not** use for: defining the underlying product problem (use **problem-definition**); running a full process for a single high-stakes decision (use **running-decision-processes**); a performance or accountability problem with one individual (use **having-difficult-conversations**); or a pure timeline/milestone plan (use **managing-timelines**). If the real need is a one-way persuasion narrative to get another team to do what you want, that is out of scope - clarify the decision and use **running-decision-processes** or **managing-up**.

## Pick the branch

| The user wants… | Branch |
|---|---|
| To stand up or repair how two+ teams work together | **A - Collaboration operating system** |
| To defuse a live conflict or turf/credit clash right now | **B - Defuse a conflict now** |
| To unblock a stalled cross-team dependency right now | **C - Unblock a dependency now** |
| To fix slow or re-litigated decisions | **D - Decision rights and log** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) - ask ≤5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A - Collaboration operating system

The one-time design (or repair) flow. Produce a system, not a single conversation.

1. **Define the mission and mode.** Clarify the outcome, success metric(s), and timeframe; name the mode - project team (finite) vs ongoing interface - and why it matters now.
   **Done when:** a cross-functional partner can restate the mission, metric(s), and constraints without you in the room.
2. **Map the system by dependency.** Identify DRI, approvers, contributors, and informed stakeholders; capture what each optimizes for and fears; flag missing seats (Legal/Support/Ops). Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** every team that must execute or sign off is represented - no surprise vetoes.
3. **Write the expectations contract.** Run the "expectations of each other" exercise, then convert it to a responsibility map, decision rights, and escalation triggers. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** each function can state what it owns, what it expects of others, and which decisions it can make alone.
4. **Pick shared artifacts.** Choose the minimum set (charter, spec, prototype/working slice, metric definitions) and name the artifact of record.
   **Done when:** at least one artifact concretely removes an interpretation dispute.
5. **Design the cadence and decision log.** Set the cadence, async update format, and doc hub; install a decision log and a lightweight protocol for who decides and how disagreements resolve.
   **Done when:** updates center outcomes/decisions/risks and every meaningful decision lands in the log with an owner.
6. **Set conflict and credit norms.** Define the conflict protocol ("Yes, and" on competing goals) and credit mechanics - who presents, who gets named.
   **Done when:** the norms are specific enough to follow in a real disagreement and in an exec/customer update.
7. **Gate and launch.** Score with [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md), book a 2-week health check, and close with **Risks / Open questions / Next steps**.
   **Done when:** the Pack has an owner, a kickoff, and a health-check date.

Deliverable: a **Collaboration Pack** - charter, stakeholder/incentives map, roles and decision-rights contract, operating cadence, decision log, and conflict + credit norms.

## Branch B - Defuse a conflict now

The tactical workhorse: two functions are stuck, re-litigating, or the tension has turned personal, and you need to run the conversation soon. Prep sheet, not a system. Working sheet and conflict protocol: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Name the clash neutrally.** State it as competing goals, not people: "we seem to be optimizing X vs Y."
   **Done when:** both sides recognize the framing without feeling blamed.
2. **Validate both goals ("Yes, and").** Say why each goal is legitimate before proposing any tradeoff.
   **Done when:** each function's core concern has been stated back accurately.
3. **Surface constraints and the real cause.** Separate non-negotiables from what can flex, and check whether this is actually a missing decision right, a metric clash, or an incentive gap.
   **Done when:** the underlying cause is named, not just the surface disagreement.
4. **Put options on the table, then decide or escalate.** Offer 2-3 options with tradeoffs; decide, or escalate via a defined trigger with a clear question and recommendation.
   **Done when:** a decision is made (or escalated with a recommendation) and logged so it will not be re-litigated.

## Branch C - Unblock a dependency now

Tactical: your work is blocked by a partner team, or a partner keeps slipping a commitment. Produce a targeted unblock plan, not a full system. Working sheet: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Pin the blocker.** State exactly what is blocked, since when, and what the delay costs (dates/scope).
   **Done when:** the blocked outcome and the cost of delay are concrete.
2. **Diagnose the cause.** Classify it: capacity, priorities/incentives, an undecided decision, or unclear ownership - not "they're just slow."
   **Done when:** the cause is classified rather than assumed.
3. **Make one specific ask.** A single clear request with an owner and a date, framed against shared goals rather than blame.
   **Done when:** the partner has an unambiguous ask and can commit or counter.
4. **Set the escalation path.** If there is no movement by the date, escalate with the question and your recommendation to the named decider.
   **Done when:** a dated fallback exists and the resolution (or escalation) is logged.

## Branch D - Decision rights and log

When decisions keep stalling or getting re-opened but the rest of the operating model is fine - install decision-making without rebuilding everything.

1. **List the contested decisions.** Write the 3-5 decisions that keep stalling or reopening as decisions, not topics.
   **Done when:** each item is phrased as a decision with a needed-by date.
2. **Assign decision rights.** Pick a lightweight model (DACI/RAPID/RACI-lite) and name who decides vs advises for each. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** every listed decision has one decider and clear input roles.
3. **Set re-litigation rules and seed the log.** Record owner, criteria, and rationale; agree what new information reopens a decision.
   **Done when:** decisions live in a log and are reopened only on changed constraints or genuinely new information.

## Examples

- *"PM, Eng, and Design keep thrashing on our onboarding revamp - set up a better way to work together."* → **Branch A**: charter, stakeholder map, decision-rights contract, cadence, decision log, and norms.
- *"Design and Eng are stuck re-litigating scope and it's getting personal - I have to run the conversation tomorrow."* → **Branch B**: neutral framing, "Yes, and" on both goals, options with tradeoffs, a logged decision.
- *"Help me convince the platform team to just do what I want."* → out of scope: this skill aligns on shared goals and decision rights; for a one-way persuasion or exec escalation, clarify the decision and use **running-decision-processes** or **managing-up**.
