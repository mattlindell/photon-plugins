# House standard

This page is for the person who sets up how a team tracks work. After it, you
can write one tracker standard that every repo and every person on the team
shares, and set up each repo from it.

Each repo gets its own `docs/agents/issue-tracker.md` when someone runs
`/ph-plan:setup-ph-plan` in it. `ph-plan` and `ph-build` read that file to find
tickets, specs, maps, and research. If two people answer the setup questions
differently, their repos put the same kind of artifact in different places.
Then a person or an agent who moves between the repos looks in the wrong place.
A house standard prevents this. It's one template for `issue-tracker.md`, plus
the rules for filling it in. Every repo's file comes from the template, and
repos differ only in the values the template leaves open.

This page shows how to build a standard. It doesn't give you a complete
template. You start from the built-in template for your tracker and change it.
Read [Setup](setup.md) first. This page assumes you have set up one repo.

Northwind Studio has two repos now: `storefront` and a new one, `wholesale`.
Northwind's team lead writes the standard. Where this page shows Northwind's
choices, make your own.

## Step 1. Decide where each artifact lives

`ph-plan` writes four kinds of artifact. Decide where each one lives, once, for
the whole team.

On this page, "the tracker" means the system that holds your tickets. Your
[issue tracker](../../CONTEXT.md#issue-tracker) is that system plus wherever
specs, maps, and research live, so this step decides what your issue tracker
is.

| Artifact | What it is | The decision |
| --- | --- | --- |
| Ticket | One piece of work, or one [decision ticket](../../CONTEXT.md#decision-ticket). | Always in the tracker. Decide which project or team holds each repo's tickets. |
| Spec | The plan for an effort, with its `settled:` block. | In the tracker beside the tickets, or in a wiki. |
| Map | A [scout map](../../CONTEXT.md#scout-map) for an effort too big for one session. | Put it wherever specs go. |
| Research | A finding that answers one research ticket, with its sources. | Put it wherever specs go. |

`CONTEXT.md` and the ADRs aren't part of this decision. They stay in the repo,
because the skills read them from there.

Keep specs, maps, and research in one place. A reader who finds the spec then
finds the map and the research beside it. Wherever they live, they never carry
triage labels. Those go on tickets only.

To choose between the tracker and a wiki for specs, ask these questions:

- Who reads the specs? If people outside the engineering team review them, put
  them where those people already read.
- Can Claude Code reach the wiki? Every person who runs `ph-plan` or `ph-build`
  needs access to it, the same as to the tracker. If they don't have it, keep
  specs in the tracker.
- Does your team publish a spec only after a person reviews it? A wiki that
  keeps pages as drafts until someone publishes them supports this.

Northwind keeps tickets in its tracker and specs, maps, and research in its
wiki, because the shop owner reads specs and doesn't use the tracker.

## Step 2. Decide what an effort is on your tracker

An [effort](../../CONTEXT.md#effort) is a body of work planned together, such as
Northwind's "Checkout redesign". It's a role, not a feature of any tracker. Your
standard says which part of your tracker fills it. Whatever you pick must do
three things:

- Hold the effort's tickets, so that you can list all of them.
- Hold the effort's specs, maps, and research, or link to them.
- Act as an index. One place says what the effort is for and links each spec,
  map, and research artifact.

Some common forms:

- **A parent ticket with wiki pages.** The effort is a ticket one level above
  ordinary tickets, and every ticket for the effort is its child. The wiki has
  one page for the effort, and the spec, map, and research pages are children of
  that page. The parent ticket's description links the effort page.
- **A parent ticket with artifact tickets.** The same parent ticket, but specs,
  maps, and research are also tickets under it. Their title prefix tells them
  apart from work tickets (see step 3).
- **A milestone that links project documents.** The effort is a milestone in a
  project, and the effort's tickets belong to the milestone. The specs, maps,
  and research are documents attached to the project. The milestone's
  description is the index, with a link to each document.
- **A folder.** When tickets are files in the repo, the effort is a folder
  under the repo that holds its map and its ticket files.

Some built-in templates already have an Efforts section that names one of
these forms. Others don't. If yours doesn't, add an Efforts section to your
template that names the form you picked.

Your standard also answers two smaller questions:

- **How does a ticket or spec name its effort?** For example, by the parent
  ticket's key or by the milestone's name. Give the exact phrase, such as
  `Effort: <name>`, so that every spec and ticket writes it the same way. A
  skill uses it to put new work in the right place.
- **What happens when new work has no effort yet?** The built-in templates that
  have an Efforts section say to create the effort first, before the first spec
  or ticket. Keep that rule.

Northwind uses a parent ticket with wiki pages. "Checkout redesign" is one
parent ticket, and its wiki page holds `Spec: Checkout redesign` and
`Map: Checkout redesign`.

## Step 3. Set title conventions

Title each artifact by its kind, with a fixed prefix:

| Artifact | Title |
| --- | --- |
| Spec | `Spec: <name>` |
| Map | `Map: <effort>` |
| Research | `Research: <topic>` |

Work tickets and decision tickets get no prefix. Their title is the work or the
question, such as "Payment entry points for guest shoppers".

The prefixes let people and agents find artifacts by name. A search for
`Map: Checkout redesign` finds one result. Where specs sit beside tickets, the
prefix tells them apart from work tickets. Where specs live in a wiki or as
documents, which carry no labels, the prefix is how a reader finds the map.

Write the prefixes exactly like this in your standard: a capital letter, a
colon, and a space. Not every built-in template has them. The templates for
trackers that can keep specs in a wiki or as documents use the same three. The
others find a map by a label or by a file path, with no title prefix. If your
base template has no prefixes, add them wherever it creates a spec, a map, or a
research finding.

## Step 4. Separate house-wide values from per-repo values

Your template holds two kinds of value:

- **House-wide values** are the same in every repo. Write them in the template
  as literal text.
- **Per-repo values** change from repo to repo. Leave each one as a placeholder
  in angle brackets, such as `<PROJECT_KEY>`. The built-in templates use the
  same style.

To sort a value, ask whether two repos would ever give different answers. If
they would, it's a placeholder.

These are usually house-wide:

- Which tracker you use, and where specs, maps, and research live (step 1).
- What an effort is (step 2), and the title prefixes (step 3).
- The issue types for tickets and for efforts.
- The triage label names. Keep the defaults unless your tracker already uses
  other names. Then put your `triage-labels.md` beside the template, so that it
  is part of the standard too.
- The tracker's site or workspace address, and the wiki space, when the whole
  team uses one.

These are usually per-repo:

- The project, or the team and project, that holds the repo's tickets.
- The ticket-key prefix, such as `SF` in `SF-37`.
- The wiki page that holds the repo's effort pages, when each repo has its own.

Northwind's site and wiki space are house-wide, so they're literal text in its
template. The project key is per-repo: `SF` for `storefront`, `WH` for
`wholesale`.

A value can be house-wide and still not belong in a committed file. Step 6
covers that.

## Step 5. Write the template and keep it in one place

Start from the built-in template for your tracker. The templates are in the
`setup-ph-plan` skill, in
[`plugins/ph-plan/skills/setup-ph-plan/references/`](../../plugins/ph-plan/skills/setup-ph-plan/references/).
The tracker templates are the files named `issue-tracker-<tracker>.md`. Copy
yours and make these changes:

1. Replace each house-wide placeholder with its value.
2. Leave each per-repo placeholder as it is.
3. Delete what doesn't apply. Some templates offer two versions of a section,
   for example one for specs in a wiki and one for specs in the tracker. Keep
   the one you chose in step 1.
4. Add what step 2 needs, such as an Efforts section, if the template doesn't
   have it.
5. Add one line at the top that says the file follows the house standard and
   where the standard lives. Someone who wants to change the file then knows to
   change the standard instead.

Don't add a connection method, such as a CLI or an MCP server, to the template.
Most built-in templates leave it out on purpose. A template whose commands all
use one CLI, because that CLI is the only way in, keeps it. Don't add a second
one. Claude Code uses whatever access
to the tracker each person already has, and each person records their own
preference in a local file (step 6).

Keep the template in one place that every lead can open and that keeps a
history of changes. A small repo for team conventions works well, because a
change to the standard then goes through a pull request like any other change.
A wiki page also works. Don't keep the master copy in one of your product repos.
A reader would take it for that repo's own setup.

Beside the template, write down how to fill each placeholder: what it means and
where to find its value. A person who sets up a new repo needs nothing else.

## Step 6. Keep private values in a local file

Some values must not go into a committed file:

- Workspace IDs, team keys, and project names, when the repo is public.
- Raw IDs, such as the UUIDs some trackers use for statuses and labels.
- Each person's connection preference: which CLI or MCP server their machine
  tries first, and what it falls back to.

Put these in a file in `docs/agents/` whose name ends in `.local.md`, and make
sure the repo's `.gitignore` ignores it. The line `*.local.*` covers every such
file. The committed `issue-tracker.md` keeps placeholders for these values and
says where to find them.

One built-in route does this for you. It asks whether to keep the values out of
the committed file, then writes the local file and the pointer to it. See
[Tracker routes](setup.md#tracker-routes) for which route that is. For any other
tracker, add the same two things to your template yourself:

- A paragraph in the committed template. It names the local file, says to read
  it first and substitute its values for the placeholders, and says to ask
  before writing anything to the tracker when the file is missing. The
  Coordinates section of the template that offers the split has a paragraph you
  can copy.
- The layout of the local file, as part of the standard. Give it three
  sections. "Placeholder resolution" is a table with each placeholder and its
  value. "Connection preference" says which CLI or MCP server this machine tries
  first. "Raw IDs" holds any IDs worth recording.

The setup skill adds `*.local.*` to `.gitignore` only on the route that offers
the split. On any other route, add the line yourself.

The standard fixes the local file's name and layout, not its values. Each person
writes their own copy, because the connection preference belongs to their
machine. Give new people the values the same way you share other settings that
aren't public.

## Step 7. Set up each repo from the standard

`/ph-plan:setup-ph-plan` can't read your template from where you keep it. You
give it the template in one of two ways.

**A built-in route as the base.** Use this when your template started from a
built-in template, which is the usual case.

1. Run `/ph-plan:setup-ph-plan` in the repo and pick the route for your tracker.
2. If the route asks follow-up questions, answer them with the house-wide
   values and this repo's values.
3. The skill shows you its drafts and lets you edit them before it writes
   anything. Compare the `docs/agents/issue-tracker.md` draft with your
   template. Where they differ, tell the skill to replace the draft with your
   template, with this repo's values filled in. Check the new draft, then tell
   the skill to write it.

The route still does its other work, such as creating triage labels on routes
that create them and, on the route that offers it, writing the local file. See
[Tracker routes](setup.md#tracker-routes) for which routes create labels.

**"Other".** Use this when no built-in route fits your tracker.

1. Run `/ph-plan:setup-ph-plan` and pick **Other**.
2. When the skill asks you to describe your workflow, paste your template with
   this repo's values filled in. Ask the skill to write it as
   `docs/agents/issue-tracker.md` without changes.
3. The skill writes this route's file from your description, so it can reword
   it. Check the draft against your template, and ask for changes until they
   match.

"Other" writes only the files. Create any triage labels and any local file
yourself.

Either way, answer the triage-label question the way the standard says. If your
standard has its own `triage-labels.md`, check the skill's draft against it the
same way. Keep the "Claim roles" section that the skill fills in. It maps each
[claim role](../../CONTEXT.md#claim-role) to the label or field that records
it. Then commit the files.

Northwind set up `wholesale` from the built-in route. Its `issue-tracker.md`
matches the one in `storefront` except for the project key.

For a repo that you set up before the standard existed, compare its
`issue-tracker.md` with the template. Edit the file to match, or run the setup
skill again.

## Changing the standard

Change the template first, then every repo's `issue-tracker.md`. If you change
only one repo, that repo no longer matches the others, and the standard no
longer describes your team. The line at the top of each file (step 5) shows
which repos follow the standard, so you know which files to update.

## Checklist

- [ ] Every artifact has one place to live: tickets, specs, maps, and research.
- [ ] The template says what an effort is and how work names its effort.
- [ ] The template uses `Spec:`, `Map:`, and `Research:` titles.
- [ ] House-wide values are literal text, and per-repo values are placeholders.
- [ ] The template adds no connection method that its base template left out.
- [ ] The template lives in one place, with notes on how to fill each
      placeholder.
- [ ] Private values and connection preferences go in a gitignored
      `*.local.md` file.
- [ ] Every repo's `issue-tracker.md` came from the template.
