# Writing the plan

This page teaches you to plan your own work with `ph-plan`. After it, you can
start at `/ph-plan:intake`, answer a grilling session or chart a scout map, and
end with a spec or a set of tickets saved where your `issue-tracker.md` says.
You'll know which skill runs next, what it asks you, and what it writes down.

Read [Reading the plan](reading-the-plan.md) first. This page writes the specs
and tickets that page teaches you to read.

The examples come from Northwind Studio's `storefront` repo. The shop owner
wants shoppers to add a gift message to an order. Northwind's ticket keys look
like `SF-52`. Yours look like whatever your
[issue tracker](../../CONTEXT.md#issue-tracker) uses.

## Before you start

The repo needs `docs/agents/issue-tracker.md`. `ph-plan` reads it to decide
where specs, maps, and tickets go. If the repo doesn't have one, do
[Step 4 of the setup page](setup.md#step-4-set-up-a-repo).
[Tracker routes](setup.md#tracker-routes) says what each tracker's template
writes.

## The whole flow

1. `intake` decides which planning skill runs.
2. `grilling` interviews you until every decision is made. For work that's too
   big for that, `intake` routes to `scout` instead.
3. `define-done` decides how anyone will know the work is done.
4. `to-spec`, `to-tickets`, or both write the result where your
   `issue-tracker.md` says.
5. You hand the result to `ph-build`.

Every route ends in a written spec or ticket with a `settled:` block. No route
writes code. Building is `ph-build`'s job.

## Step 1. Start with intake

Start a Claude Code session in the repo, run `/ph-plan:intake`, and describe the
work in a few sentences:

```text
/ph-plan:intake Shoppers want to add a gift message to an order. It should print
on the packing slip.
```

`intake` makes one decision and hands off. It asks whether the
[frontier](../../CONTEXT.md#frontier) is mapped. In other words, can you list
the open questions, even if you can't answer them yet?

| If | `intake` routes to | What happens next |
| --- | --- | --- |
| You can name the unknowns, and the work fits in a session or two | `grilling` | An interview that settles the dimensions and ends in a spec or tickets. This is the usual case. |
| You can't see the end yet, the work needs many sessions, or nobody can list the questions yet | `scout` | A [scout map](../../CONTEXT.md#scout-map) of decision tickets, resolved one per session until the way is clear. |

Scale words such as "rewrite", "migrate", and "the whole X" send work to
`scout`. So does saying you can't see where it ends. Everything else goes to
`grilling`. `intake` asks you which one only when it can't tell.

The gift message fits in one session, and the questions are easy to list, so
`intake` routes it to `grilling`. The Checkout redesign in
[Reading the plan](reading-the-plan.md#scout-maps) went to `scout`. See
[If intake routes to scout](#if-intake-routes-to-scout) at the end of this page.

`intake` sends three kinds of work somewhere else:

- **Work that already exists as a ticket** goes to `/ph-plan:triage`. Triage
  checks the ticket and grills it into shape if it needs that. When a ticket
  reaches `ready-for-agent` through triage, its `problem` dimension is settled.
- **Work that already has a spec with a settled block** goes to `ph-build`
  through `/ph-build:dispatch`.
- **A question about existing code** goes to `ph-build:how`, or to
  `ph-build:why` for the reasons behind the code. `intake` is for work, not for
  learning how code works.

## Step 2. Answer the grilling rounds

Grilling is an interview. The agent asks and you decide. It keeps going until
every decision the work depends on is made.

### How a round works

The agent keeps a design tree. Each decision leads to the decisions that depend
on it. The frontier is every decision whose prerequisites are already settled.
Each round asks the whole frontier at once, as numbered questions, and then
waits for your answers.

Your answers settle decisions, and those unblock the questions that depended on
them. The agent works out the new frontier and asks the next round. A question
that depends on another question in the same round waits for a later round. The
agent doesn't guess at an answer you haven't given yet.

Every question comes with the agent's recommended answer, worded so that "yes"
accepts it. The first round for the gift message looks like this:

```text
❓ Q1 - Where the message lives: Should the gift message be a new optional
giftMessage field on Order, rather than a separate table?

➡️ Yes. One optional field on Order. Only one message per order is needed.

---

❓ Q2 - Length: Should the message be limited to 200 characters?

➡️ Yes. 200 characters fits on the packing slip.

---

❓ Q3 - Who sees it: Should only the packing slip show the message, and not the
order confirmation email?

➡️ Yes. The message is for the person who receives the gift.
```

Q1 comes first because it's a [one-way door](../../CONTEXT.md#one-way-door). A
new field on `Order` is a schema change. Grilling settles one-way doors early,
while changing your mind still costs only a conversation. Decisions that are
cheap to undo go fast, and you can reverse them later.

### How to answer

- **Answer every question in the round.** Number your answers to match:
  `Q1 yes. Q2 yes. Q3 no, the email shows it too.`
- **"Yes" is a full answer.** Use it when the recommendation is right.
- **Push back when the recommendation is wrong.** The recommendation is a
  starting point. The decision is yours.
- **Say "I don't know" when you don't know.** An honest "I don't know" becomes a
  decision ticket (see [Close or block each dimension](#close-or-block-each-dimension)).
  A guess becomes a settled decision that nobody checked.

Facts are the agent's job, not yours. When a question needs something the agent
can look up, such as how the code works today, it sends a subagent to find out.
It doesn't ask you. Questions that don't depend on that fact go ahead in the
meantime.

### Watch the settled block

The agent tracks the four [dimensions](../../CONTEXT.md#dimension) and says
which one each round works on. It keeps a running `settled:` block and shows it
again each time a dimension closes:

```yaml
settled: [problem, shape]
open: [approach, verification]
```

A dimension is settled or open. "Mostly agreed" is open. Grilling usually
closes `problem`, `shape`, and `approach`. `define-done` closes `verification`
in Step 3. If the block says a dimension is settled and you don't agree, say so
before the next round.

### Close or block each dimension

A dimension that can't close in the session doesn't stay open with nobody
responsible for it. It becomes a [decision ticket](../../CONTEXT.md#decision-ticket).
The ticket names the dimension it closes and blocks the work that waits for it.

| What's missing | Decision ticket | Who resolves it |
| --- | --- | --- |
| A design sketch or a module boundary | `closes: shape` | A design session that uses `ph-lib:codebase-design` |
| An answer that only an experiment can give | `closes: approach` | `/ph-plan:prototype` |
| Facts from outside the room | `closes: problem` or `closes: approach` | `/ph-plan:research` |

For the gift message, nobody in the session knows whether the warehouse system
accepts a message on the packing slip. That's a fact from outside the room, so
the agent proposes a decision ticket:

````markdown
# Does the warehouse system accept a packing-slip message?

```yaml
closes: approach
```
````

Whoever resolves the ticket also updates the tickets it blocks. They move
`approach` to `settled` on each one and record what was decided.

### Agree on the words

Grilling runs `domain-modeling` the whole time. When you and the agent agree on
what a term means, the agent writes it to the repo's `CONTEXT.md` then, not at
the end. Expect it to challenge a word you use that conflicts with the
glossary. When a decision is hard to reverse, surprising without context, and
the result of a real trade-off, the agent offers to record an ADR.

### When the session ends

The session ends when the frontier is empty. Every branch of the design tree is
visited, and nothing is left assumed without saying so. The agent then asks
whether you've reached a shared understanding. It doesn't write anything until
you say yes.

## Step 3. Decide how the work is proven done

When `problem`, `shape`, and `approach` are settled, grilling runs
`define-done`. It closes `verification` by choosing one way to prove that the
work is done. This is the [verification
methodology](../../CONTEXT.md#verification-methodology). It usually runs in the
same session, before anything is written. You can also run
`/ph-plan:define-done` later on a spec or a set of tickets that left
`verification` open.

It proposes four things and asks you to confirm them, the same way grilling puts
every other decision to you:

1. **The claim.** What has to be true at the end, read from the three settled
   dimensions.
2. **The cheapest proof that would convince a skeptic.** It doesn't propose the
   most thorough proof. A unit test that pins the real behavior beats an
   integration suite that nobody runs.
3. **Where the proof runs.** A unit test, an integration test, a test that drives
   the real app, or a check that a person does by hand. It's specific enough
   that two agents would build the same check.
4. **What doesn't need proving, and why.** This stops an agent from writing
   tests that the work doesn't need.

Without one stated method, every agent that picks up a ticket invents its own
idea of proof. Settled verification means one method applies to every ticket in
the set. It doesn't make tests optional. `verification: open` means the builder
uses the standard default and writes the test first.

Sometimes you can't know how to prove something until it exists. Exploratory
work, an unfamiliar integration, and a performance question with no baseline are
examples. Then `define-done` doesn't make up a method. It writes a decision
ticket with `closes: verification` and leaves the dimension open.

For an example of the result, read the Testing Decisions section of the spec in
[Reading the plan](reading-the-plan.md#reading-a-spec).

## Step 4. Write it down with to-spec or to-tickets

A session that ends in agreement but writes nothing saves nobody any effort.
Every session ends in a spec, tickets, or both. The agent offers the next skill.
You can also run `/ph-plan:to-spec` or `/ph-plan:to-tickets` yourself.

| | `to-spec` | `to-tickets` |
| --- | --- | --- |
| Use it when | The work needs one document that explains the whole plan. | The work should go straight to tickets that an agent can build, or a spec needs splitting into tickets. |
| What it writes | One spec: a settled block, then Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, and Further Notes. | A set of tracer-bullet tickets. Each is a narrow slice that works end to end and that you can verify on its own. Each names the tickets that block it. |
| What it asks you | No new questions about the plan. It writes up what the session decided. It asks only whether the places it plans to test the work are the ones you expect. | Whether the breakdown is right: too coarse or too fine, whether the blocking links are correct, and whether to merge or split any tickets. It asks again until you approve. |
| Settled block | One block at the top, listing only what the session closed. | One block on each ticket, because an agent picks up one ticket, not the whole plan. When `verification` is settled, the method goes on every ticket, below the acceptance criteria. |
| Where it goes | Where your `issue-tracker.md` says specs live. It's marked `ready-for-agent` unless that file says specs carry no labels. | Where your `issue-tracker.md` says tickets live, created blockers first and connected with your tracker's blocking links. Each ticket is marked `ready-for-agent`. |

Both skills read `docs/agents/issue-tracker.md` to find where things go and how
your tracker records them. Setup wrote that file from the template for your
tracker. See [Tracker routes](setup.md#tracker-routes).

Be honest about the settled block. It tells whoever builds the work how much
thinking is left. If you overstate it, they skip a question that nobody
answered. Every dimension left open should have a decision ticket that will
close it. On tickets, that decision ticket blocks the tickets that wait for it.

The gift message session ends in tickets. The schema change comes first, and
the packing-slip ticket waits for the warehouse decision ticket:

```yaml
settled: [problem, shape, verification]
open: [approach]
```

That block sits on the packing-slip ticket until the warehouse question closes.
Then whoever closes it moves `approach` to `settled`.

## Step 5. Hand it to ph-build

Hand the spec or a ticket to `/ph-build:dispatch`, for example
`/ph-build:dispatch SF-52`. It reads the settled block you wrote and sizes the
build to what's still open. [Handing a spec to
ph-build](reading-the-plan.md#handing-a-spec-to-ph-build) covers what it does
with each kind of block.

## If intake routes to scout

`/ph-plan:scout` charts an effort that's too big for one session. It works in
two modes.

**Chart the map.** This takes one session:

1. Scout grills you to name the destination, meaning what done looks like for
   the effort. Usually that's a spec.
2. It grills you again, wide instead of deep, across the whole effort. It looks
   for the open decisions and the first steps you can take now.
3. It writes the map where your `issue-tracker.md` says. The map has the
   Destination, Notes, Decisions so far, Not yet specified, and Out of scope
   sections.
4. It creates a decision ticket for each question it can already state
   precisely, and links the blocking edges between them. A question it can't
   state precisely yet goes under Not yet specified on the map.
5. It starts subagents on the research tickets that nothing blocks. Then it
   stops.

If step 2 finds no unknowns, the work is small enough for one session and
doesn't need a map. Scout stops and asks you how to continue.

**Work through the map.** Run `/ph-plan:scout` with the map. Each session takes
one ticket from the frontier, claims it by assigning it, and resolves it the way
its type says. Each ticket has one of four types: research, prototype, grilling,
or task. [Decision tickets](reading-the-plan.md#decision-tickets) explains what
each type does. Scout posts the answer on the ticket, closes it, and adds a
one-line summary to the map's Decisions so far. When an answer makes a question
in Not yet specified clear enough to state, scout turns it into a new ticket.

When the frontier is empty and nothing is left under Not yet specified, the way
to the destination is clear. The next step is usually a spec. Run
`/ph-plan:to-spec`, and the spec cites the tickets that made each decision.
[Scout maps](reading-the-plan.md#scout-maps) shows a map that reached that
point.
