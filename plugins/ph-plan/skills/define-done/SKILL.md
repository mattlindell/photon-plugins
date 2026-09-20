---
name: define-done
description: Decide how a body of work will be proven done, and attach one shared verification methodology to every ticket in it.
disable-model-invocation: true
---

# Define done

Close the `verification` dimension for a spec or a set of tickets by deciding
**one** way the work will be proven done — then attach it to all of them.

The point is consistency, not permission. Without this, every agent that picks
up a ticket invents its own idea of proof, and a work set ends up verified five
different ways with no one able to say whether it is finished. `verification:
settled` means "there is a stated methodology here and it applies to all of
this."

It does not mean testing is optional anywhere. `verification: open` means "no
shared methodology was stated, fall back to the standard test-first default" —
never "skip the tests."

## Run it last

Read the other three dimensions first. You cannot say how to prove something
works until you know what it is (`problem`), what shape it takes (`shape`), and
how it gets built (`approach`).

This is a **soft** precondition. If one of the three is still open, you can
still run — but say which one is open and how that limits the methodology you
are proposing, because a verification plan built on an unsettled approach will
usually need redoing.

## Process

1. **Read the spec and the settled dimensions.** What is the actual claim that
   needs to be true at the end?
2. **Pick the cheapest proof that would actually convince a skeptic.** Not the
   most thorough — the cheapest sufficient one. A unit test that pins the real
   behavior beats an integration suite nobody runs.
3. **Name the surface.** Where the proof runs: unit, integration, a live driver
   against the real app, a manual check a human must do. Be specific enough that
   two different agents would build the same thing.
4. **State what does *not* need proving**, and why. This is as valuable as the
   rest — it is what stops an agent gold-plating coverage on work that did not
   warrant it.
5. **Write it onto every ticket in the set**, not just the spec. An agent picks
   up one ticket, not the whole plan.
6. **Mark the dimension settled.**

```yaml
settled: [problem, shape, approach, verification]
```

## When verification cannot be decided yet

Sometimes you genuinely cannot know how to prove something until something
exists — exploratory work, an unfamiliar integration, a performance question
with no baseline.

Do not invent a methodology to fill the slot. Emit a decision ticket declaring
`closes: verification`, blocking the work that depends on it, and leave the
dimension open. Whoever resolves it updates the blocked tickets on close.

An honestly open dimension costs one fallback to test-first defaults. A fabricated
one costs every agent in the set following a plan that does not fit the work.
