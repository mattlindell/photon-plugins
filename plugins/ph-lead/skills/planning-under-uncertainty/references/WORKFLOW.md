# Uncertainty Playbook (Heuristics)

Topic-keyed heuristics and defaults for the branches in `../SKILL.md`. Adjust every default to your context.

## Wartime vs peacetime

Set the mode before anything else - it changes tempo, evidence bar, and what you optimize for.

- **Wartime:** stabilize and stop the bleeding. Restrict changes, diagnose fast, and pre-agree rollback/patch rules. Tempo is daily or every 48 hours on the top hypotheses.
- **Peacetime:** explore and learn. Tolerate slower, higher-quality evidence building. Tempo is a weekly learning review plus a biweekly decision checkpoint.

## Diagnose before acting (humility first)

When the system behaves unexpectedly, diagnose before committing.

- Separate symptoms ("the metric dropped") from causes (why it dropped).
- Write a short situation report: what changed (release, traffic source, pricing, infra), what the data shows (trend, magnitude, segment), and what you don't know yet.
- Generate hypotheses across categories - product, marketing, pricing, reliability, ops, external - including uncomfortable ones, and state what would falsify each.
- Bias toward reversible actions until uncertainty is reduced.

## Uncertainty mapping

- Rate each assumption on confidence (H/M/L) and impact; prioritize high-impact, low-confidence items.
- Give every top unknown a validation method (customer calls, log analysis, A/B tests, usability tests, forced-choice surveys, market scans) with an owner and a time bound.

## Experiments are about learning, not "wins"

- Define the hypothesis up front; treat a "failed" result as valuable if it changes a decision.
- Every experiment must answer: "What will we do differently depending on the result?"
- Don't measure individuals on win rate - it breeds risk aversion.
- Write hypotheses falsifiably: "If <condition>, then <measurable change> because <mechanism>," each with a primary signal, guardrails, and a decision rule.

## Reproducible testing process (many shots at bat)

- Keep one place for hypotheses and experiments (a portfolio table) and a consistent review cadence.
- Give each test a clear owner and reviewer: who designs, runs, analyzes, decides.
- Mix fast/cheap tests with slower/high-confidence ones; ensure at least one fast test can run soon.
- Speed matters because uncertainty is unpredictable - process quality often dominates idea quality.

## Data is a compass, not a GPS

- Prefer directional decisions over false precision.
- Define "ridiculousness tests": signals that tell you quickly that you're wrong.
- Pair every metric with a guardrail so you don't optimize the wrong thing.

## Buffers, contingencies, and triggers keep plans alive

- Allocate explicit time/capacity/budget buffers, proportional to uncertainty (higher uncertainty, larger buffer).
- Keep contingency paths (Plan A/B/C) that can be activated quickly.
- Write triggers as "if <signal> crosses <threshold>, then rollback/pivot/escalate by <when>."
- Structure Plan v0 around learning gates: Phase 1 reduce uncertainty, Phase 2 commit to a direction, Phase 3 build and roll out.

## Anti-patterns (catch yourself)

- **Acting before diagnosing.** Jumping to a fix in a crisis based on the first plausible story, before any hypothesis is tested.
- **Confirmation bias.** Generating only hypotheses the team already believes; skip the uncomfortable ones and you'll miss the real cause.
- **Theater experiments.** Running a test with no decision attached - "winning" measured as a positive result rather than a decision that changed.
- **GPS thinking.** Treating a noisy metric as precise truth, or optimizing a number with no guardrail.
- **Certainty cosplay.** A plan with fixed dates and no buffers, contingencies, or triggers, presented as if uncertainty were already resolved.
- **Cadence drift.** Running experiments with no review ritual or decision log, so learning never turns into decisions.
