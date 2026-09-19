# Context

Names for the concepts this repo's design discussions keep reaching for. If a
discussion needs a concept that isn't here, add it.

This file is a glossary. It holds no implementation decisions — those live in
`docs/adr/`.

## Marketplace

This repo. A registry of plugins, owned by and built primarily for one person,
published so it can be pointed at rather than because it is a product. Coherence
is judged by whether it makes sense to its author, not to a stranger.

## Plugin

The unit of install and the unit of versioning. A user turns on a whole plugin,
never part of one, and everything inside it ships together. Two things belong in
the same plugin when they are one install decision.

## Hat

The role a person is wearing when they reach for a plugin. The chosen seam for
splitting the marketplace: one plugin per hat. A hat is a *who*, not a *when* —
splitting the same person's work into sequential phases produces two plugins that
are always installed together, which fails the definition of Plugin.

## Skill cluster

A set of skills that point at each other — preconditions, hand-offs, shared
vocabulary. A cluster is evidence about where a seam could go, but a cluster is
not automatically a plugin; clusters may span plugins.

## Upstream

`pstack-claude`, which is itself a port of Lauren Tan's Cursor `pstack` plus seven
skills from Cursor's `cursor-team-kit`. Both MIT. Anything taken from it carries
two copyright lineages that must travel with it.

## Fan-out

A skill spending more than one agent or model on a single task — parallel
candidates, multi-model panels, worker swarms. Fan-out is how Upstream buys
confidence. It is also the dominant cost in a session.

## Proportional rigor

The property that effort spent executing a task tracks the uncertainty remaining
in that task. Work that arrived already specified, argued over, and written down
should cost less to execute than work that arrived vague. Its absence is the
defect being designed against: a fully-specified task consuming a full five-hour
token allotment because the executing skills could not tell that the thinking had
already happened.

## Planning front-end

The skills that run before anything is built — deciding whether a task is the
right task, sharpening it, and writing it down where an agent can pick it up.
Upstream has no equivalent; it begins at "here is a task, now be rigorous."

## Playbook

An Upstream unit larger than a skill: a named end-to-end procedure for a kind of
work (a feature, a bug fix, a migration) that sequences skills and decides how
much fan-out each step gets. Playbooks are where cost is actually committed.

## Non-negotiable

An Upstream trigger that fires unconditionally — a rule stated without an escape
hatch. The cost problem lives here rather than in any single skill: a rule with no
way to say "this step was already done" cannot be satisfied cheaply.

## Escape hatch

A stated condition under which a step may be skipped. Upstream's existing hatches
key on *triviality* — how small the task is. The missing hatch keys on
*specification* — how much of the thinking already happened. See Proportional
rigor.

## Rigor signal

The written marker that tells an executing skill how much uncertainty a task still
carries, so fan-out can scale to it. Produced by the Planning front-end, which is
the only part of the system that knows how much uncertainty it removed. Its
absence is why model tuning alone could not control cost.

## Harness

Where an agent runs and whether a human is present. **Interactive** — a person is
in the loop, able to answer, and their judgment is the cheapest way to resolve
ambiguity. **Unattended** — nobody is there, so blocking to ask is a stall with no
payoff. The chosen seam between the two development plugins: planning is
interactive work, implementation is unattended work. Rules that look contradictory
across the two plugins are usually the same rule, correctly inverted for its
harness.

## Middle-up planning

Planning that starts from ideas and works toward a gestalt — deciding what the
thing should be. Also covers planning for anything not software. This is the
product hat.

## Middle-down planning

Planning that starts from an agreed thing and works toward its specifics —
defining the details of something that will be coded. This is the development
planning hat. The boundary against Middle-up planning is direction of travel and
whether the subject is software, not altitude or formality.

## Library plugin

The one deliberate exception to "one plugin per hat": a plugin that is not a hat
at all, but shared material other plugins reference and require. It has no
audience of its own — nobody installs it because of the work they are doing, they
install it because something else needs it.

Being an exception is the point. A second library plugin, or a hat that starts
behaving like a library, means the seam has eroded rather than been extended.

## Primitive

Material in the Library plugin that another plugin's router actually references.
Primitives are the reason the dependency is hard.

## Operator tool

A skill the human invokes directly, belonging to no hat's workflow — it acts on
the conversation or on the agent system rather than on any work product. Shares
the Library plugin with Primitives but is not a dependency of anything.

## Dimension

One of the four axes of uncertainty a task can carry: **problem** (what and why),
**shape** (structure and types), **approach** (implementation path), and
**verification** (how anyone knows it is done). A dimension is either *settled* or
*open*; there is no partial state. The set of settled dimensions is the Rigor
signal.

## Tier

A rung on the single effort ladder every model choice resolves to: **scan** <
**scoped** < **judgment** < **divergent** < **panel**, strictly ordered, no ties.
Skills name tiers, never models — the mapping from tier to an actual model is
per-Harness and written by a setup skill. All four dimensions settled means
`scoped`.

## Decision ticket

A ticket whose purpose is to close a Dimension for other tickets rather than to
ship anything. Whoever closes it — human or agent — updates the blocked tickets'
Rigor signal on close, recording which dimension was decided and with what.

## Verification methodology

What `verification: settled` actually carries: one stated way of proving the work
is done, shared by every ticket in a work set. Its purpose is consistency, not
permission — an agent picking up any ticket in the set verifies the same way as an
agent picking up any other, instead of each inventing a method.

`verification: open` therefore means "no shared methodology was stated, use the
standard test-first default," not "testing is optional." Skipping tests remains a
separate in-the-moment judgment about an expensive test path, unrelated to this
Dimension.
