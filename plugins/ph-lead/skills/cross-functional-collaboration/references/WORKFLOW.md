# Cross-functional Playbook (Heuristics)

Topic-keyed heuristics, defaults, and anti-patterns for the branches in `../SKILL.md`. Adjust every default to your context.

## Anti-patterns (catch yourself)

- **Meeting your way out of ambiguity.** Adding a sync rarely fixes unstated goals or decision rights. Write the thing down first; meet to confirm.
- **RACI theater.** Roles exist on paper but decision rights are still ambiguous - "ownership" is assigned without authority or the time to exercise it.
- **Org-chart mapping.** Listing stakeholders by reporting line misses the team that actually blocks you. Map by execution dependency instead.
- **Missing a seat.** Forgetting Legal/Support/Ops/Data until late produces rework and a surprise veto. Invite required experts into the mission, not the final review.
- **Doc sprawl.** Multiple sources of truth drift; requirements get negotiated verbally and never captured. Name one artifact of record.
- **Re-litigating settled decisions.** If a decision was never logged with its rationale, it will be reopened. Log the "why," not just the "what."
- **Treating recurring conflict as a personality problem.** Chronic friction is usually a missing decision right, a metric clash, or a misaligned incentive.
- **Credit hoarding.** One function owns the narrative to leadership and the others go quiet. Recognition has to be designed, not left to whoever speaks up.
- **A Pack no one adopts.** A beautiful charter with no kickoff and no owner changes nothing. Ship with an owner and a health-check date.

## Mission and mode

- If you cannot name the outcome and the time horizon, you are coordinating vibes, not work.
- Name the mode explicitly: a **project team** (finite) and an **ongoing interface** need different cadences and artifacts.
- Watch for a mission that is really a task list (no outcome), and for competing success metrics across functions (e.g., "quality" vs "speed") that stay implicit until they collide.

## Mapping the system (stakeholders + incentives)

- List stakeholders by **execution dependency**, not org chart.
- Capture incentives as two columns: what each function is **optimizing for** and what it **fears**.
- In content or regulated domains, put subject matter experts (legal, compliance, editorial, security) into the mission up front, not as last-minute reviewers.

## Expectations and decision rights

- Run the "expectations of each other" exercise: each function writes what it expects of the others (PM of Eng/Design/Data, Eng of PM/Design, and so on), then reconcile.
- Turn every recurring disagreement into an explicit decision right and an escalation trigger: "who decides when we disagree, and at what threshold do we escalate?"
- Revisit the contract every 4-8 weeks or at each phase change - it is a living agreement, not a launch artifact.

## Shared artifacts

- Prefer artifacts that push ambiguity to the surface: a working slice, prototype, or concrete example ends more debates than abstract discussion.
- Define the **artifact of record** - where the latest truth lives (charter, spec, metric definitions) - so people stop arguing from stale copies.

## Operating cadence and decision logging

- Default async update format: **progress vs outcome**, **decisions made/needed**, **risks + mitigations**, **asks/blockers**.
- Keep meetings small and expand visibility with async notes rather than bigger invite lists.
- Every meaningful decision gets an owner, a due date, and a recorded rationale; re-litigate only with new information or changed constraints.

## Defusing a live conflict (Branch B)

- Open on the goals, not the people: "we seem to be optimizing X vs Y" lowers the temperature faster than assigning fault.
- Validate both goals before proposing a tradeoff ("Yes, speed matters because…, and quality matters because…") - people concede once they feel heard.
- Diagnose before deciding: if the same conflict keeps returning, it is a missing decision right, an unclear metric, or a misaligned incentive - not a clash of temperaments.
- End with a decision or a clean escalation (question + recommendation to the named decider), and log it so the conflict does not reopen next week.

## Unblocking a dependency (Branch C)

- Quantify the cost of delay in dates and scope before you ask for anything - it turns a favor into a shared business problem.
- Classify the cause honestly: **capacity**, **priorities/incentives**, an **undecided decision**, or **unclear ownership**. Each has a different fix (more people vs re-prioritization vs a decision vs an owner).
- Make one specific, dated ask with a named owner; a vague "can you help sooner?" gets a vague answer.
- Pre-agree the escalation path and date so escalation reads as a process, not an attack.

## Credit and recognition

- Credit sharing is a system: define who presents, who gets named, and how recognition is shared before the demo, not after.
- Rotate presenters so Eng/Design/Data get airtime, and name contributors explicitly in written updates.
- Celebrate behind-the-scenes work (reliability, quality, craft), which is the work most likely to go unseen.

## Launch and health checks

- Use the rubric as a go/no-go: if the score is low, do one more intake round (max 5 questions) rather than shipping a shaky Pack.
- Run a 2-week health check: what decisions are stuck, what rework happened, which norms were ignored - then update roles and cadence to match reality.
