---
name: swarm
description: Fan out parallel workers over a partitioned job, drain them, and return one report.
disable-model-invocation: true
---

# Swarm

Fan out N parallel workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the number that run at once.
4. Pick the worker model from `swarm workers` in `~/.claude/ph-build-policy.md` when present. Otherwise use the default in [Fan-out](#fan-out). For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes.

## Phase B: Fan out

Spawn all N workers in one message with `subagent_type: "general-purpose"`, `run_in_background: true`, and the configured model. Claude Code subagents all run on this machine, so isolation comes from the worktree or output directory assigned in Phase A, not from a remote environment.

When a worker must start from a non-default branch, check that branch out in the worker's own worktree and name the worktree path in its brief.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.

## Fan-out

Caps are **ceilings, not targets**, and they are hard. Never scale a count to
the size of the input.

`scan` < `scoped` < `judgment` < `divergent` < `panel` is a strict effort
ladder. A tier names a rung, never a model: the tier-to-model mapping is
per-harness and lives in the fan-out policy that `/setup-ph-build` writes. When
no policy file is present, use the defaults below rather than falling back to
unbounded.

| Role | Tier | Cap |
| --- | --- | --- |
| Workers | `scoped` | 6 |

Upstream set no default and no ceiling here, and a dropped playbook routinely
asked for ten to thirteen. Six is the ceiling. A job that will not fit in six
workers is a job that needs splitting into sequenced units, not more workers.
