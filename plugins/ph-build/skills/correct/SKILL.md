---
name: correct
description: Find the mistakes agents keep repeating in this repo and make each one impossible, at the highest level that works, with every check proven to fail on a real past mistake.
disable-model-invocation: true
---

# Correct

The operator keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent can't make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

First, read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Read the session transcripts too, when the operator names one or the current session is the one that went wrong. Claude Code keeps them under `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/`; resolve that directory with `skills/operator-tools/reflect/scripts/claude-project-dir.mjs` under the installed `ph-lib` plugin rather than by hand.

Group the mistakes into classes. A class counts once it has happened twice. Every class names the commits, comments, or transcript turns it came from. Drop a class you can't trace to a specific moment, however plausible it sounds.

Before you design a check, read the repo's own check command (its `lint` or `check` scripts, its CI workflow). A check that already exists but is unwired or silently broken is the finding. Wire it rather than build a second one. A repo with no guardrail at all, meaning no pre-commit hook and no CI job that runs lint, typecheck, and tests, is a finding of its own.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** If bad code still compiles, add a lint or CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them. A judgment rule belongs where the reviewer reads it (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, or the repo's equivalent), not in `CLAUDE.md` or `AGENTS.md`, which load into every session whether the rule applies or not.

## Costs that are not code mistakes

Some classes are not wrong code. They are time the agent lost. Fix these too:

- **Navigation.** The agent took many calls to find a file or fact, or missed a hidden dependency between files. Add a navigation pointer from a file it already reads.
- **Tool economy.** A tool call cost far more than it returned, such as a CLI or MCP that dumps its whole payload. Streamline the call, or replace the tool.
- **Information access.** The agent needed something it could not reach. Widen its access: tee the dev server log to a file, or grant read-only access to the service.
- **No-ops.** A steering file carries lines that change no behavior. Delete them.

## Fix and prove

Then fix the most frequent classes now, one commit each. Prove each new check fails on a real past mistake. Run the same command locally and in CI. Exceptions go on the offending line with a reason, an expiry date, and a human's approval.

## Keep the rule table

Last, keep a table in the agent instruction file that pairs each rule with what enforces it. When the operator corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that's a repeat, so fix it at the highest level in the same change. Drop a rule once its mistake can't happen.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.
