# Reading the plan

This page teaches you to read a plan that `ph-plan` wrote. After it, you can
open a spec, read its `settled:` block, and tell which decisions are already
made. You can predict how much work `ph-build` will spend on the spec, and you
can hand the spec to `ph-build` without reopening a decision.

The examples come from Northwind Studio's "Checkout redesign"
[effort](../../CONTEXT.md#effort). Its spec, its scout map, and one of its
decision tickets appear in full on this page, so you don't need access to
anyone's tracker. Northwind's ticket keys look like `SF-37`. Yours look like
whatever your [issue tracker](../../CONTEXT.md#issue-tracker) uses.

## The settled block

A spec or ticket that `ph-plan` writes starts with a short YAML block:

```yaml
settled: [problem, shape, approach]
open: [verification]
```

Each name in the block is a [dimension](../../CONTEXT.md#dimension). A
dimension under `settled` is a decision that someone made and wrote down. A
dimension under `open` is a decision that nobody has made yet. There is no
partial state. When all four dimensions are settled, the block can show
`open: []` or leave out the `open` line. Both mean that nothing is open.

Together, the settled dimensions are the
[rigor signal](../../CONTEXT.md#rigor-signal). Read the block first. It tells
you which questions you must not ask again and which ones are still yours.

## The four dimensions

Each dimension closes a different kind of question. The examples come from the
Checkout redesign spec in the next section.

| Dimension | The question it closes | Example from the Checkout redesign spec |
| --- | --- | --- |
| `problem` | What are we building, and why? | Shoppers leave the five-step checkout, and Northwind can't tell at which step. |
| `shape` | What is the structure, and what are the types? | One `Order` type for guest and signed-in checkouts. Guest orders carry `guestEmail` instead of `customerId`. |
| `approach` | How will we build it? | A queue worker sends each placed order to the warehouse system. |
| `verification` | How will anyone know it's done? | v1 is done when the acceptance run on staging passes. Every ticket uses the same test method. |

`verification: open` doesn't mean that tests are optional. It means that the
spec doesn't state one shared way to prove the work is done. The builder then
uses the standard default: write the test first.

## Reading a spec

This is the Checkout redesign spec. It's shorter than a real spec, but it has
the same sections that `/ph-plan:to-spec` writes. The ADRs it cites are
architecture decision records in Northwind's `storefront` repo. They're part of
the example, so you can't open them.

````markdown
# Spec: Checkout redesign

```yaml
settled: [problem, shape, approach, verification]
open: []
```

Written from Map: Checkout redesign. The decisions come from tickets SF-37
through SF-47 and from ADRs 0001 to 0004 in `storefront`.

## Problem Statement

Shoppers leave the five-step checkout, and Northwind Studio can't tell at
which step. Two more storefronts will use the same checkout next year, so a
one-off fix would be built three times.

## Solution

A one-page checkout that guest and signed-in shoppers share, with one
analytics event for each step.

## User Stories

1. As a guest shopper, I want to pay on one page, so that I can finish without
   making an account.
2. As the shop owner, I want to see at which step shoppers leave, so that I
   know what to fix next.

## Implementation Decisions

### Checkout page (SF-37, SF-43)

An embedded card form on the checkout page. There's no express wallet button
and no saved-card quick pay.

### Order record (ADR 0003, SF-41)

One `Order` type for guest and signed-in checkouts. `customerId` is optional.
A guest order carries `guestEmail` instead. Order state is an enum: `draft`,
`placed`, `paid`, `refunded`.

### Order sync (ADR 0002, SF-46)

A queue worker sends each placed order to the warehouse system. A failed send
retries three times, then marks the order for a person to check.

### Drop-off reporting (SF-44)

Each checkout step writes one `checkout_step` event with the step name and
the order ID.

## Testing Decisions

Every ticket built from this spec follows it. Each slice gets tests at its
API boundary, written first. v1 is done when the acceptance run on staging
passes (SF-47).

## Out of Scope

Express wallets and saved cards (see SF-49).

## Further Notes

Open build checks. These aren't spec questions. The builder checks each one
when it builds the slice:

- Does the payment provider's test environment support partial refunds on
  Northwind's account?
````

Read it from the top:

1. **The block.** All four dimensions are settled. Nothing in this spec is up
   for debate during the build.
2. **The line under the block.** It says where the decisions came from: a scout
   map, a range of tickets, and ADRs in the repo. To learn why a decision went
   the way it did, follow these sources. Don't work it out again yourself.
3. **Implementation Decisions.** Each heading names the ticket or ADR that made
   the decision. This section holds the `shape` and `approach` content.
4. **Testing Decisions.** It starts with "Every ticket built from this spec
   follows it." Settled verification looks like this: one method, shared by
   every ticket.
5. **Open build checks.** The question about partial refunds isn't an open
   dimension. Nobody plans anything to answer it. The builder runs the check
   when they build that slice.

## Scout maps

A [scout map](../../CONTEXT.md#scout-map) charts an effort that's too big for
one planning session. `/ph-plan:scout` writes it. The Checkout redesign spec
came from this map:

```markdown
# Map: Checkout redesign

## Destination

A buildable spec for the Checkout redesign, with all four dimensions settled.

## Notes

Domain terms are in CONTEXT.md in storefront. Ask the shop owner about any
change that shoppers can see.

## Decisions so far

- Payment entry points for guest shoppers (SF-37): guests can use an embedded
  card form. Express wallet buttons and saved-card quick pay need an account.
- One order type or two (SF-41): one Order type for guest and signed-in
  checkouts (ADR 0003).
- Where drop-off is measured (SF-44): one analytics event for each step.
- Order sync runtime (SF-46): a queue worker, not a scheduled job (ADR 0002).
- How v1 is proven done (SF-47): the acceptance run on staging.

## Not yet specified

Nothing.

## Out of scope

- Express wallet support (SF-49): closed. Guests can't use express wallets
  (SF-37). It comes back only as a new effort.
```

On a real tracker, each ticket name is a link to its ticket. Read the map like
this:

1. **Destination.** The map says what done looks like before it lists any work.
   A map usually ends in a spec, not in shipped code.
2. **Decisions so far.** Each line is a one-line summary of a closed
   [decision ticket](../../CONTEXT.md#decision-ticket), with a link to it. The
   map is an index. The details stay in the ticket.
3. **Not yet specified.** These are questions that the team knows are coming but
   can't state precisely yet. "Nothing" means that every question became a
   ticket and every ticket closed. The [frontier](../../CONTEXT.md#frontier) is
   empty. An empty frontier with nothing unspecified closes the map, and the
   next step is the spec.
4. **Out of scope.** These are decisions that the team placed outside this
   effort. Each line says why. A ticket listed here is closed, not waiting.

## Decision tickets

A decision ticket exists to make a decision, not to ship code. When it closes,
the tickets that waited for the decision get one more settled dimension. This is
SF-37 from the map:

````markdown
# Payment entry points for guest shoppers

Type: research
Blocks: SF-43, SF-46

## Question

On the checkout page, which payment entry points can a guest shopper use?

```yaml
closes: approach
```
````

The `Type:` and `Blocks:` lines show what the ticket records, not how it
records it. Most trackers keep the type as a label and blocking as a native
link between tickets. Your `docs/agents/issue-tracker.md` says how yours does.

The type says how the decision gets made. There are four types:

- **research.** An agent reads documentation and records what it says.
- **prototype.** A person reacts to a rough artifact, such as a sketch or a stub.
- **grilling.** A person answers questions in a session with an agent.
- **task.** Someone does a piece of work, such as getting access to a service,
  so that a decision can be made.

The `closes:` line names the dimension that the ticket closes for the tickets
it blocks. When SF-37 closed, its comment gave the answer: guests can use an
embedded card form, and express wallet buttons and saved-card quick pay need an
account. The comment linked a research page that cites the payment provider's
documentation for each claim. Then whoever closed SF-37 moved `approach` to
`settled` on SF-43 and SF-46.

Follow the decision forward and you find it three times. The map's Decisions
so far has a one-line summary. The spec's Checkout page section states the
result. The ticket and its research page hold the evidence. A builder who asks
"why no express wallet button?" can follow the spec back to SF-37. The answer
is already written down, so the build doesn't reopen it.

Read the comments on every ticket you pick up. Answers and later decisions
often live there, not in the ticket body.

## Handing a spec to ph-build

Hand any spec or ticket to `ph-build` with `/ph-build:dispatch`. Follow it with
the ticket key or a link to the spec, for example `/ph-build:dispatch SF-43`.
`dispatch` fetches the ticket with its comments, finds the settled block, and
decides how much work the build needs. The `implement` agent in `ph-build` isn't
a second way in. It runs `dispatch` too.

The settled block decides what `dispatch` does next:

| Settled block | What `ph-build` does |
| --- | --- |
| All four settled | Builds it at the `scoped` [tier](../../CONTEXT.md#tier). It runs no exploration phase and no panels of agents. |
| Some settled | Skips the phases that own the settled dimensions and works only on the open ones. If `shape` is open on a nontrivial change, it runs `ph-build:how`, which reads the code and explains how it works, before it designs. If `verification` is open, it writes tests first. |
| None settled, or no block | Runs one orientation pass with `ph-build:how`. It then writes its own provisional settled block and says that it inferred the block instead of reading it. It doesn't get a second pass. |
| No spec at all | Routes the work to `/ph-plan:intake`, because nobody planned it. If nobody is there to plan it and the work is easy to undo, it takes the orientation pass and continues. |

The Checkout redesign spec has all four dimensions settled, so `ph-build` builds
each ticket at the `scoped` tier. A ticket with only `problem` settled costs
more, because `ph-build` must work out the shape and the approach itself
before it builds. This
is the reason to settle what you can before you hand work off. See
[proportional rigor](../../CONTEXT.md#proportional-rigor).

`ph-build` also has direct entry points for narrow jobs. Use `ph-build:how` to
learn how code works, `ph-build:why` for the reasons behind it, `ph-build:tdd`
for a failure you can reproduce, and `ph-build:babysit` to get a pull request to
pass its checks. Use these when you already know which one you need. They
aren't how you hand over a spec.

## One-way doors

A [one-way door](../../CONTEXT.md#one-way-door) is a decision that's expensive
to undo:

- A schema change or a data migration
- A public API, or anything that outside consumers depend on
- Anything that deletes or permanently rewrites data
- Auth, billing, or security boundaries

Every other decision is a two-way door. `ph-build` builds two-way doors even
when the plan is vague, because a reviewer can correct them later for less than
a planning session costs.

At a one-way door, `ph-build` reads the settled block:

- **The block settles it.** The spec already made the decision, so `ph-build`
  builds it. The change still doesn't count as ready to merge until a reviewer
  that didn't write it passes it. The pull request description also
  recommends `/ph-build:interrogate` as your step before merge. Every
  one-way-door pull request carries that line. It doesn't mean anyone
  disputed the design.
- **The block leaves it open.** `ph-build` stops. It writes a decision ticket
  with `closes: shape`, or `closes: approach` when the open question needs an
  exploration of test coverage or race conditions. It hands the ticket back to
  you and names the skill that fits.

The skills it names are ones that only you can start:

| Skill | Use it for |
| --- | --- |
| `/ph-build:architect` | A shape that crosses a function boundary |
| `/ph-build:interrogate` | An adversarial review of a design or diff by several models |
| `/ph-build:swarm` | Coverage matrices, race conditions, or exploring a large space in parts |
| `/ph-build:arena` | Comparing competing designs or implementations |

These skills run several agents at once and cost the most. `ph-build` never
starts them by itself.

## When you think a settled decision is wrong

Sometimes new evidence shows that a settled decision is wrong. Say a builder on
the Order sync slice finds that the warehouse system rejects any order without a
`customerId`. The spec settled that guest orders don't carry one (ADR 0003).

Don't decide again yourself. Escalate:

1. Stop building the part that the decision touches. Work that doesn't depend on
   it can continue.
2. Comment on the spec or the ticket. Quote the decision, say what you found,
   and link the evidence.
3. Tag the person who settled it. For a spec, that's usually its author. For a
   ticket, it's whoever closed the decision ticket named in the ticket or in its
   comments.
4. Let them decide. If the decision stands, build on it. If it changes, they
   move the dimension from `settled` to `open` and settle it again, in a
   grilling session or with a new decision ticket. Then they update the settled
   block to match.

Don't edit a settled block yourself, and don't build around the decision while
you wait.

`ph-build` works the same way. If a ticket contradicts an ADR that's still in
force, it stops and names both the ADR and the line of the ticket. It doesn't
pick a side.

## Where specs and tickets live

Every effort keeps its parts together. Its tickets hang under one parent, and its
spec, scout map, and research sit beside them. Northwind titles each one by kind,
so people and agents can find it: `Spec: Checkout redesign`,
`Map: Checkout redesign`, `Research: Payment entry points for guest shoppers`.
`CONTEXT.md` and the ADRs stay in the repo.

Each repo records where these live in `docs/agents/issue-tracker.md`, and
`ph-plan` and `ph-build` read that file. `/ph-plan:setup-ph-plan` writes it from
the template for your tracker. See [Tracker routes](setup.md#tracker-routes) in
the setup page for what each template does.
