---
name: "organizational-transformation"
description: "Lead an organizational transformation toward a modern product operating model: diagnose the current system, design a context-fit target model, and sequence adoption through nudge-first pilots rather than wholesale framework adoption."
disable-model-invocation: true
---

# Organizational Transformation

## Transform outcomes, not frameworks

Anchor every choice below to four ideas:

- **Outcomes, not framework adoption.** The goal is changed behaviors and better outcomes, never "we implemented SAFe/Spotify." Frameworks are a toolbox to borrow from, not the destination.
- **Change the reinforcing loops, not the slides.** Feature teams persist because incentives, cadences, and approvals hold them in place. Announcing "empowered teams" without moving decision rights and incentives changes nothing.
- **Nudge, don't mandate.** Sequence change as safe-to-try pilots with defaults, rituals, and coaching so it's adopted, not rejected. Everything-at-once produces backlash.
- **Make the new model observable.** Specify decision rights, cadences, and required artifacts so a leader can answer "who decides what" and "what good looks like" on Day 1.

## When to use / not

Use to stand up transformation pilots, build a full transformation plan, design a target product operating model, or plan the change/comms that reduce rejection.

Do **not** use for: strategy or vision first (use `defining-product-vision` or `working-backwards`); an org chart or team-topology change alone (use `organizational-design`); project-managing a known plan (use `managing-timelines`); or HR/legal guidance on comp, layoffs, or labor law - involve HR/legal.

## Pick the branch

| The user wants... | Branch |
|---|---|
| To stand up a safe-to-try pilot now | **A - Design a pilot** |
| A full transformation plan to fund and sequence | **B - Full plan** |
| To specify the target operating model concretely | **C - Target operating model** |
| To reduce rejection of a change already in motion | **D - Change + comms** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) - ask <=5 at a time, then proceed on labeled assumptions; never request secrets.

## Branch A - Design a pilot

The workhorse. Stand up one or a few safe-to-try 90-day pilots that create proof without waiting for org-wide alignment. Produce a pilot plan, not a full program. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Pick for leverage, not politics.** Choose 2-4 areas with willing leadership, manageable dependencies, and quick, reversible proof (2-6 weeks). Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
2. **Write each as a hypothesis.** "If we do X, then Y improves because Z." Timebox it and keep it reversible.
3. **Enable with nudges.** Templates, rituals, coaching, and default paths - not mandates.
4. **Close the loop.** Set leading indicators and a learning loop that feeds each pilot's insights back into the model and roadmap.

**Done when:** each pilot is safe-to-try, timeboxed, measurable, and can start without org-wide alignment.

## Branch B - Full plan

For designing a transformation a sponsor can fund and sequence. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Align on outcomes.** Charter: why now, goals/non-goals, 3-5 principles, and success metrics with leading indicators.
   **Done when:** sponsors state success as outcomes and behaviors, not "we implemented X."
2. **Diagnose the operating model as a system.** Map idea -> shipped; name bottleneck mechanisms and the loops that reinforce feature teams (annual planning, output metrics, centralized approvals).
   **Done when:** the diagnostic explains the symptoms with concrete mechanisms, not vibes.
3. **Pick a thesis + framework hygiene.** The smallest set of changes that creates leverage, plus a borrow/don't-borrow list to prevent cargo-culting.
   **Done when:** the plan is tailored to context and avoids copying a model wholesale.
4. **Design the target operating model.** Specify it concretely, or run Branch C and return.
   **Done when:** a leader can answer who decides what and what good looks like on Day 1.
5. **Create the pilot plan.** Design nudge-first pilots, or run Branch A and return.
   **Done when:** pilots are safe-to-try, measurable, and don't need perfect org-wide alignment.
6. **Build the 6-12 month roadmap.** Sequence the big rocks (capability building and decision rights often precede structural change), with decision points, dependencies, and rollback triggers; reserve capacity for the work.
   **Done when:** the roadmap protects business continuity and in-flight commitments.
7. **Plan change + comms.** Reduce rejection, or run Branch D and return.
   **Done when:** the plan includes reinforcement mechanisms, not just announcements.
8. **Gate and finalize.** Run [references/CHECKLISTS.md](references/CHECKLISTS.md), score with [references/RUBRIC.md](references/RUBRIC.md), and include Risks / Open questions / Next steps.
   **Done when:** the pack passes; if the score is low, do one more intake round (<=5 questions) and revise.

## Branch C - Target operating model

For specifying the target model concretely. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Define the team model.** Team types (product / platform / enabling) and the ownership model (by area, journey, segment, platform).
2. **Write the decision rights.** A Day 1 table (DRI, consulted, guardrails) plus role expectations - including leadership behaviors, not just team behavior.
3. **Set cadences and artifacts.** Planning cadences and the required artifacts (problem briefs, discovery notes, decision logs) that make the model observable.

**Done when:** a leader can answer "who decides what" and "what good looks like" on Day 1.

## Branch D - Change + comms

For reducing rejection of a change already in motion. Templates: [references/TEMPLATES.md](references/TEMPLATES.md).

1. **Map the stakeholders.** Stance, concerns, and what each group needs to believe.
2. **Draft the narrative and messages.** Stakeholder-specific: what changes, what isn't changing yet, and what happens next.
3. **Build reinforcement.** Rituals, metrics, leadership behaviors, and incentives, plus a system that harvests objections into real mitigations.

**Done when:** the plan reinforces the change through rituals, metrics, and leader behavior - not a one-time announcement.

## Examples

- *"Teams ship features but outcomes don't improve - move us toward empowered product teams."* -> **Branch B**: system diagnostic, target operating model, 90-day pilots, 6-12 month roadmap, governance metrics.
- *"We tried SAFe/Spotify-style changes and got backlash - reduce the rejection."* -> **Branch A** for small proof pilots plus **Branch D** for stakeholder messaging and reinforcement.
- *"Write a plan to implement the Spotify model verbatim."* -> out of scope as stated: frameworks are tools, not the goal; instead produce a context-fit model and specify what, if anything, to borrow and how to validate it via pilots.
