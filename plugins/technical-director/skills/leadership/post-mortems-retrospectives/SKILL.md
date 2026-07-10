---
name: "post-mortems-retrospectives"
description: "Run blameless post-mortems and retrospectives: incident reviews, project and OKR retros, pre-mortems with kill criteria, and the recurring learning ritual that turns insight into owned action."
disable-model-invocation: true
---

# Post-mortems & Retrospectives

## Learn from the system, not the person

Anchor every choice below to four ideas:

- **Blameless by construction.** You are here to fix systems, not judge people. Assume everyone acted reasonably given what they knew at the time; if a performance issue is real, handle it separately through the right channel.
- **Facts before stories.** Build a timestamped timeline with evidence before anyone theorizes about "why." Label every claim as fact or hypothesis.
- **A learning without an owned action is a wish.** Each insight must become a decision with an owner, a due date, and a success signal — or it will recur.
- **Institutionalize or lose it.** Learnings that stay in a doc die there. Socialize them and pre-commit to triggers so future work acts on them.

## When to use / not

Use to run an incident post-mortem or a project/OKR retrospective, prep and facilitate a review that's on the calendar, define kill criteria before a bet, or stand up a recurring learning ritual.

Do **not** use for: an incident that is **still active** — stabilize first, then schedule the review; **assigning blame** or evaluating an individual's performance — route to HR / your management process; deep technical debugging without the right experts in the room — this skill facilitates, it doesn't replace engineering investigation; or deciding *what problem to solve* — that's a discovery process.

## Pick the branch

| The user wants… | Branch |
|---|---|
| To post-mortem an incident or outage | **A — Incident post-mortem** |
| To retro a project or a missed OKR | **B — Project / OKR retro** |
| To prep and facilitate a review that's on the calendar | **C — Prep & facilitate** |
| To pre-commit to failure signals before/early in a bet | **D — Pre-mortem & kill criteria** |
| To stop learnings from dying in a doc | **E — Institutionalize learning** |

Gather missing context with [references/INTAKE.md](references/INTAKE.md) — ask ≤5 at a time, then proceed on labeled assumptions; never request secrets or personal data; anonymize.

## Branch A — Incident post-mortem

The blameless spine. Turn an outage into system learnings and owned actions.

1. **Frame it blameless and assign roles.** Name the review, set the "fix systems, not people" norm, and reframe as a "learning review" if *post-mortem* reads punitive in your culture. Confirm facilitator, scribe, and decision owner.
   **Done when:** the goal is learning + prevention (not blame) and the three roles are assigned.
2. **Assemble facts and a shared timeline.** Timestamped events, quantified impact, and "known facts" vs. "assumptions to verify" kept separate. Template: [references/TEMPLATES.md](references/TEMPLATES.md).
   **Done when:** the timeline has timestamps and evidence links, and hypotheses are labeled.
3. **Diagnose contributing factors (systems lens).** Cluster causes across People / Process / Product / Tech / Comms / Environment; ask "what made this outcome likely?"; run 5 Whys on the top one or two. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).
   **Done when:** causes are changeable system conditions, with no individual-blame language.
4. **Decide what changes, then own the follow-through.** Convert 3–7 crisp learnings into decisions (fix, guardrail, instrumentation, runbook, process, scope change) and build an action tracker with owner, due date, success signal, and follow-up date. Pass [references/CHECKLISTS.md](references/CHECKLISTS.md) / [references/RUBRIC.md](references/RUBRIC.md) and close with **Risks / Open questions / Next steps**.
   **Done when:** every top factor maps to an owned action and the checklist passes.

Deliverable: a post-mortem doc — brief + agenda, facts/timeline, contributing factors, learnings + decisions, action tracker, and a 1-page shareout.

## Branch B — Project / OKR retrospective

Same spine as Branch A (frame → facts → factors → decisions → actions), with three shifts in emphasis: compare **plan vs. actual** instead of an incident timeline, keep the numeric grade **secondary** to "what system produced this result?", and focus factors on **systemic blockers** (resourcing, dependencies, unclear requirements, decision latency, tech debt). Consider adding kill criteria (Branch D) for the next cycle.

**Done when:** learnings outweigh the grade, the top blockers map to owned decisions for the next cycle, and any next-cycle triggers are named.

## Branch C — Prep & facilitate a session

The workhorse. You have a review on the calendar and need to walk in ready to run it — not design a program.

1. **Pull the evidence.** Gather the timeline artifacts, metrics, tickets, and prior action items so the room debates facts, not memory.
2. **Draft the brief + agenda.** Purpose, roles, ground rules, pre-reads, and a timeboxed agenda. Prep sheet and agenda: [references/TEMPLATES.md](references/TEMPLATES.md).
3. **Plan the facilitation.** One opening line that sets the blameless norm, the order (facts before "why"), and how you'll keep it decision-oriented (owners + dates before anyone leaves).

**Done when:** a one-page brief + agenda exists, evidence is linked, ground rules are written, and the close captures owners and a follow-up date.

## Branch D — Pre-mortem & kill criteria

Forward-looking. Imagine the bet failed and work backward to the signals, or pre-commit to triggers early in a live initiative. Define 3–10 **observable** signals, each with a window, a threshold, a committed action (pause / pivot / kill / escalate / invest), and an owner who declares it. Template: [references/TEMPLATES.md](references/TEMPLATES.md).

**Done when:** each criterion is measurable and carries a pre-committed action and owner — never "we'll discuss it."

## Branch E — Institutionalize learning

Stand up a lightweight recurring **Impact & Learnings Review** (30 min, weekly/biweekly) that covers top learnings, what changed, and what's next — plus a single shared learning log with a consistent format. Heuristics: [references/WORKFLOW.md](references/WORKFLOW.md).

**Done when:** the ritual has a cadence, an owner, and inputs, and a leader can read a shareout and answer "what changed because of this?"

## Examples

- *"We had a 45-minute outage in our payments API yesterday — run a blameless post-mortem."* → **Branch A**: evidence-backed timeline, systems factors, owned actions, and a shareout.
- *"We hit 0.8 on our Q4 activation OKR — lead a retro on why and what we change next quarter."* → **Branch B**: learnings over grade, systemic blockers, decisions, and kill criteria for the next initiative.
- *"Write a post-mortem proving Person X caused the incident."* → out of scope: refuse the blame framing; redirect to a systems-based review and, if needed, a separate management process.
