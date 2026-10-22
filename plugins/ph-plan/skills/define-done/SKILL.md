---
name: define-done
description: Close the verification dimension by deciding one shared way a body of work will be proven done, and attach it to whatever carries the work — a live planning session, a spec, or a ticket set. Use when grilling has settled problem, shape, and approach, when a spec or tickets still have verification open, or when the user asks how the work will be proven done or what counts as done.
---

# Define done

Close the `verification` dimension for a body of work by deciding **one** way
it will be proven done — then attach it to whatever carries the work.

The point is consistency, not permission. Without this, every agent that picks
up a ticket invents its own idea of proof, and a work set ends up verified five
different ways with no one able to say whether it is finished. `verification:
settled` means "there is a stated methodology here and it applies to all of
this."

It does not mean testing is optional anywhere. `verification: open` means "no
shared methodology was stated, fall back to the standard test-first default" —
never "skip the tests."

## Find the carrier

Run against whatever holds the work when you are reached. Do not wait for a
spec or tickets to exist.

| Carrier | Read the dimensions from | Attach the methodology to |
| --- | --- | --- |
| A live session — `grilling` mid-flight, nothing written yet | the session's own running `settled:` block | the session, stated in full, so `to-spec` or `to-tickets` writes it down with the block |
| A spec | the spec's `settled:` block | the spec's Testing Decisions section |
| A ticket set | each ticket's `settled:` block | every ticket in the set, not just one |

The live session is the usual case. `grilling` reaches this skill once the
other three dimensions are settled, which is before anything is written.

## Run it last

Read the other three dimensions first. You cannot say how to prove something
works until you know what it is (`problem`), what shape it takes (`shape`), and
how it gets built (`approach`).

This is a **soft** precondition. If one of the three is still open, you can
still run — but say which one is open and how that limits the methodology you
are proposing, because a verification plan built on an unsettled approach will
usually need redoing.

## Process

1. **Read the carrier's settled dimensions.** What is the actual claim that
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
5. **Attach it to the carrier**, per the table above. On a ticket set, that is
   every ticket: an agent picks up one ticket, not the whole plan. In a live
   session, state the methodology as a decision the user can confirm, the same
   way `grilling` puts every other decision to them.
6. **Mark the dimension settled** in the carrier's block.

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
