# Setup

This page installs `ph-plan` and `ph-build` in Claude Code, then sets up one repo
to use them. Do the steps in order. You don't need any experience with plugins.

You also install `ph-lib`. Some `ph-plan` and `ph-build` skills depend on
`ph-lib` skills, such as `ph-lib:unslop` for prose and `ph-lib:codebase-design`
for module design. Claude Code doesn't install `ph-lib` for you. Without it,
those skills can't reach the `ph-lib` skills they call, so they do that part of
their work worse or not at all. You don't need to learn `ph-lib` itself. It's a
[library plugin](../../CONTEXT.md#library-plugin), and
[ADR-0002](../adr/0002-ph-lib-is-a-library-not-a-hat.md) explains why it's
separate.

The examples set up Northwind Studio's `storefront` repo. Use your own repo
where the page says `storefront`.

## Before you start

- Claude Code is installed and you can sign in. In a terminal, this prints a
  version number:

  ```bash
  claude --version
  ```

- Git is installed. Claude Code uses it to download the plugins. This prints a
  version number:

  ```bash
  git --version
  ```

- You know which [issue tracker](../../CONTEXT.md#issue-tracker) your team uses
  for this repo: GitHub, GitLab, Jira, Linear, or local markdown. Claude Code
  must be able to reach it. For GitHub, that's the `gh` CLI, signed in. For
  GitLab, it's the `glab` CLI, signed in. For Jira or Linear, it's a CLI or an
  MCP server your team already uses. To check an MCP server, run `/mcp` in a
  Claude Code session and look for the server in the list, shown as connected.
  If you can't reach your tracker, ask your lead before you do step 4. Local
  markdown needs nothing.

Run steps 1 through 3 in a terminal (PowerShell, Git Bash, or the macOS
Terminal), not in a Claude Code session. Close any open Claude Code sessions
first. A session doesn't load plugins that you install after it starts.

## Step 1. Add the photon-plugins marketplace

A [marketplace](../../CONTEXT.md#marketplace) is a catalog of plugins. The
photon-plugins catalog is a public GitHub repo.

```bash
claude plugin marketplace add https://github.com/mattlindell/photon-plugins
```

The last line of output is `✔ Successfully added marketplace: photon-plugins`.

## Step 2. Install the three plugins

```bash
claude plugin install ph-lib@photon-plugins
claude plugin install ph-plan@photon-plugins
claude plugin install ph-build@photon-plugins
```

Each command prints `✔ Successfully installed plugin: <name>@photon-plugins (scope: user)`.
User scope means that the plugins load in every repo on your machine.

## Step 3. Check that the plugins loaded

First, in the terminal:

```bash
claude plugin list
```

The list includes all three plugins, and each one shows `Status: ✔ enabled`.
Your version numbers can be different from these:

```text
Installed plugins:

  ❯ ph-build@photon-plugins
    Version: 2.3.2
    Scope: user
    Status: ✔ enabled

  ❯ ph-lib@photon-plugins
    Version: 1.0.5
    Scope: user
    Status: ✔ enabled

  ❯ ph-plan@photon-plugins
    Version: 1.3.0
    Scope: user
    Status: ✔ enabled
```

Next, check that a session can see the skills. Start Claude Code:

```bash
claude
```

At the prompt, type each prefix below. Don't press Enter. Look at the menu that
opens.

| Type | The menu includes |
| --- | --- |
| `/ph-plan:` | `/ph-plan:intake` and `/ph-plan:setup-ph-plan` |
| `/ph-build:` | `/ph-build:dispatch` |
| `/ph-lib:` | `/ph-lib:unslop` |

If a prefix shows no skills, see [Troubleshooting](#troubleshooting). When
you're done, exit the session.

## Step 4. Set up a repo

Do this step once in each repo where your team plans work. The
`/ph-plan:setup-ph-plan` skill writes files under `docs/agents/`. These files
tell `ph-plan` and `ph-build` where the repo's tickets, specs, maps, and research
live.

1. In a terminal, go to the repo root and start Claude Code. Use your repo's
   path:

   ```bash
   cd path/to/storefront
   claude
   ```

2. Run the setup skill:

   ```text
   /ph-plan:setup-ph-plan
   ```

3. The skill looks at the repo, tells you what it found, and then asks about one
   section at a time. Each question starts with a recommended answer.

   - **Issue tracker.** Pick your tracker, then answer its follow-up questions.
     See [Tracker routes](#tracker-routes) below.
   - **Triage labels.** Answer **yes** to keep the default labels. Answer **no**
     only when your tracker already uses other label names for the same states.
   - **Domain docs.** The skill usually picks single-context and doesn't ask.
     It asks only in a monorepo.

4. The skill shows you drafts of the files before it writes them. Check the
   `docs/agents/issue-tracker.md` draft. It must name your tracker and contain
   the values you gave. Then tell the skill to write the files.

5. If the repo has neither `CLAUDE.md` nor `AGENTS.md`, the skill asks which one
   to create. Pick the one your team uses.

When the skill is done, the repo has these new files:

- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- An `## Agent skills` section in `CLAUDE.md` or `AGENTS.md` that points to the
  three files

Commit these files, so that everyone who works in the repo gets the same setup.
`triage-labels.md` also has a "Claim roles" section that the skill fills in
without asking. `/ph-build:foreman` reads it. Leave the defaults.

The Linear route can also write a local file that git ignores. See
[Tracker routes](#tracker-routes).

Other skills read `docs/agents/issue-tracker.md` to find where to put things.
When another guide page says "where your `issue-tracker.md` says", it means this
file.

### Tracker routes

The skill proposes GitHub when the repo's git remote is on GitHub, and GitLab
when it's on GitLab. You can pick a different tracker.

Each route writes the tracker's version of the same model. Tickets for one
[effort](../../CONTEXT.md#effort), such as Northwind's "Checkout redesign",
hang under one parent. The effort's specs, maps, and research sit beside them.

| Tracker | Where tickets go | What the skill asks next |
| --- | --- | --- |
| GitHub | GitHub Issues in the repo, through `gh` | Nothing. |
| GitLab | GitLab Issues in the repo, through `glab` | Nothing. |
| Jira | Issues in one Jira project | Where specs, maps, and research live, then your Jira coordinates. |
| Linear | Issues in one Linear project; each effort is a milestone | Your team key and project name, then whether to keep those two values out of the committed file. |
| Local markdown | Files under `.scratch/<feature>/` in the repo | Nothing. |
| Other | However you describe it | One paragraph that describes your workflow. |

**Jira.** The skill asks where specs, maps, and research live. Pick a wiki such
as Confluence when your team has one. Otherwise pick Jira issues. Then the skill
asks for the site, the project key, the issue type for tickets, and the issue
type for efforts. The effort type is the type one level above tickets in your
project's hierarchy, usually Epic. For a wiki, it also asks for the space key and the page that
holds effort pages. Use standard issue types only. The Jira route doesn't
support custom issue types or custom fields. Jira creates a label the first time
an issue uses it, so the skill doesn't create triage labels on Jira.

**Linear.** The skill asks for the team key and the project name. Then it asks
whether to keep those two values out of the committed file. Answer **yes** for a public
repo. The skill then writes the values to `docs/agents/linear-ids.local.md`,
which git ignores, and keeps placeholders in `issue-tracker.md`. Don't commit
the local file. Each person who works in the repo keeps their own copy, and can
record in it which CLI or MCP server their machine uses for Linear.
On Linear, the skill creates any triage label your workspace doesn't have yet.

**GitHub and GitLab.** The skill creates any triage label the repo doesn't have
yet.

**Local markdown.** There are no labels to create. This route suits solo
projects and repos without a remote.

Neither the Jira route nor the Linear route names a connection method. Claude
Code uses whatever access to the tracker it already has.

## Keep the plugins current

To get new versions, run these commands in a terminal, then restart Claude Code:

```bash
claude plugin marketplace update photon-plugins
claude plugin update ph-lib@photon-plugins
claude plugin update ph-plan@photon-plugins
claude plugin update ph-build@photon-plugins
```

## Troubleshooting

- **The terminal says that `claude` isn't a command.** Claude Code isn't
  installed, or the terminal opened before you installed it. Open a new terminal
  and try again.
- **Step 1 fails with a git error.** Run `git --version` to make sure that Git
  is installed. Then make sure that your machine can reach GitHub, for example
  by opening the marketplace URL from step 1 in a browser.
- **A prefix in step 3 shows no skills.** Run `claude plugin list`. If the
  plugin isn't in the list, run its install command from step 2 again. If the
  plugin shows as disabled, enable it, for example
  `claude plugin enable ph-lib@photon-plugins`. Then restart Claude Code.
- **The skill in step 4 can't reach your tracker.** Claude Code has no access to
  it yet. For GitHub or GitLab, sign in to `gh` or `glab`. For Jira or Linear,
  ask your lead which CLI or MCP server the team uses.
