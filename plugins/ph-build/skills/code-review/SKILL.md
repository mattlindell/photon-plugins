---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

Each axis ends in a **verdict**, and `PASS` with no findings is a normal outcome. A review answers "is this done?" A reviewer that always finds one more thing never lets the answer be yes. See _Verdicts and the blocking bar_.

The issue tracker should have been provided to you, usually as a tracker doc at `docs/agents/issue-tracker.md`. If not, ask which tracker this repo uses rather than guessing, and tell the user to run `/ph-plan:setup-ph-plan` where it is installed.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch via the workflow in the tracker doc.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgment call.** Each smell is a labeled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.
- **Report it only when it costs something.** Name the concrete cost in this diff: a bug it invites, a change it will make harder, or a reader it will mislead. If you can't name one, the smell doesn't go in the report. A smell never blocks.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls, in the foreground, and aggregate the reports they return. Use the `general-purpose` subagent for both.

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full — the sub-agent has no other access to it.
- The brief: "Start with a verdict: `PASS`, `PASS WITH NOTES`, or `CHANGES REQUIRED`. Then list findings, each marked **blocking** or **note**. Blocking means the diff breaches a documented repo standard: cite the file and the rule, and quote the hunk. Note means a baseline smell, or a documented guideline the repo marks as optional. Name it, quote the hunk, and state its concrete cost in this diff. Drop any smell whose cost you can't name. A documented repo standard overrides the baseline. Skip anything tooling enforces. Any blocking finding makes the verdict `CHANGES REQUIRED`. Notes alone make it `PASS WITH NOTES`. If nothing qualifies, return `PASS` with no findings and stop. That is a correct, expected result, so don't search for something to add. Report what the diff warrants and nothing more."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Start with a verdict: `PASS`, `PASS WITH NOTES`, or `CHANGES REQUIRED`. Then give a requirement checklist: each requirement in the spec, quoted, marked **implemented**, **partial**, **missing**, or **wrong** (looks implemented, but the implementation doesn't do what the line asks). Partial, missing, and wrong are **blocking**. After the checklist, list behavior in the diff that the spec didn't ask for (scope creep). Scope creep is blocking when it changes user-facing behavior, public API, or data. Otherwise it's a **note**. Any blocking item makes the verdict `CHANGES REQUIRED`. Notes alone make it `PASS WITH NOTES`. If every requirement is implemented and nothing extra was added, return `PASS` with the checklist and stop. That is a correct, expected result, so don't search for something to add. Report what the diff warrants and nothing more."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned, each led by its verdict. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_). Don't add findings of your own while aggregating, and don't reopen a `PASS`.

End with a one-line summary: the verdict per axis, then the blocking count and the worst blocking issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent. When both axes pass, the summary says so and nothing else.

The change is **done** when neither axis returns `CHANGES REQUIRED`. Notes go to whoever owns the change, and they're free to leave them.

## Verdicts and the blocking bar

| Verdict | Meaning | Action |
| --- | --- | --- |
| `PASS` | Nothing reaches the reporting bar | None |
| `PASS WITH NOTES` | Only non-blocking notes | Optional; the change is done |
| `CHANGES REQUIRED` | At least one blocking finding | Fix the blocking findings |

What blocks:

- **Standards:** a breach of a documented repo standard.
- **Spec:** a requirement that is partial, missing, or wrong, or scope creep that changes user-facing behavior, public API, or data.

Smells, style preferences, and "could also" suggestions never block. A note has to name a concrete cost in this diff. Without one, leave it out of the report.

The bar is fixed so that "done" can be measured. If any observation could block, or an empty report looked like a failed review, every review would end in more work and nothing would ever finish. Not reporting below the bar is the reviewer doing its job.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
