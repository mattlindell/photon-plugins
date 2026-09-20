---
name: tdd
description: Test-driven development. Use when building a feature or fixing a bug, when the user mentions "red-green-refactor" or wants integration tests, or whenever code is about to be written without a test in front of it.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## Test-first is the default

Features and bug fixes are built test-first. That is the standing expectation, not something the user has to ask for.

Read the work's `verification` dimension before you start:

| `verification` | What to do |
| --- | --- |
| **settled** | A shared methodology was decided for this whole work set — follow it exactly. Do not invent your own; the point is that every ticket in the set is verified the same way. |
| **open** | No methodology was stated. Fall back to this skill's defaults. Open never means "skip the tests." |

## The escape hatch

Do not force a test that does not earn its place. Skip writing a new test when the only available one would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, or large unrelated fixture churn — or when the reproduction itself is still vague.

This is a judgment about **cost of the test path**, made in the moment. It is not licence to skip testing because the work felt small, and it is unrelated to the `verification` dimension.

When you take the hatch: say so explicitly, name which of the conditions above applied, and use the closest useful verification instead — an existing adjacent test, a runtime check against the real artifact, a manual reproduction you actually ran. Never report the hatch as though the work were tested.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at named seams.** Before writing any test, write down the seams under test and the reasoning that picked them, then proceed. No test is written at an unnamed seam. You can't test everything — naming the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case. The written list is what a reviewer checks the result against.

Naming is not asking. Nobody is watching this run (**principle-never-block-on-the-human**), so the list is a record, not a request. Revising a seam later is fine; record the revision and the reason alongside the original.

Answer in writing: what is the public interface, and which seams are under test?

When the shape of that interface is itself in question — how deep the module is, where the seam belongs, what the interface should expose — use the `ph-lib:codebase-design` skill for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
