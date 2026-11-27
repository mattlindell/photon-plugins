# Guide

This guide teaches a team to plan work with `ph-plan` and build it with
`ph-build`. It's written for people who haven't used the plugins before. Most of
this repo is written for its author; the guide is the one part written for
everyone else (see [Marketplace](../../CONTEXT.md#marketplace)).

Every page uses the same example. Northwind Studio, a small web agency, keeps
its online shop in a repo called `storefront`. The team is planning an
[effort](../../CONTEXT.md#effort) called "Checkout redesign".

The pages don't name a tracker. Your [issue tracker](../../CONTEXT.md#issue-tracker)
can be GitHub, GitLab, Jira, Linear, or local markdown. Where a page says a spec
or ticket goes "where your `issue-tracker.md` says", it means the file
`docs/agents/issue-tracker.md` that setup writes in your repo.

Terms link to [CONTEXT.md](../../CONTEXT.md), the repo's one glossary.

## Reading order

Read the pages in this order. Pages without a link aren't written yet.

1. [Setup](setup.md). Install the three plugins and set up one repo.
2. [Reading the plan](reading-the-plan.md). Read a spec's `settled:` block and predict what `ph-build` does with it.
3. [Writing the plan](writing-the-plan.md). Go from `/ph-plan:intake` to a spec or a set of tickets.
4. [House standard](house-standard.md). Agree on one way to track work across every repo and person on the team.
5. Quick reference. The short version of every other page.
