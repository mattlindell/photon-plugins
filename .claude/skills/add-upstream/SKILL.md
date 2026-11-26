---
name: add-upstream
description: Register a new upstream, with its license, upstreams.json seed entry, NOTICE lineage, and glossary entry, so its first import lands correctly.
disable-model-invocation: true
argument-hint: <name> <repo-url>
---

# Add upstream

Register `$ARGUMENTS`: the first word is the upstream's name, the second its
repository URL. The name is kebab-case and permanent. It becomes the record's
`name`, the `LICENSE-<name>` suffix, and the heading of every NOTICE lineage
table, and the lint matches those strings exactly.

The record is defined in
[ADR-0006](../../../docs/adr/0006-upstream-record.md), lineage states in
[ADR-0004](../../../docs/adr/0004-lineage-states-for-upstream-derived-skills.md).
Later reviews are `sync-upstream`'s job, not this skill's.

Before step 1, settle these with the maintainer:

- **Import SHA.** The full 40-character upstream commit being imported.
- **Import map.** Each upstream path, the plugin path it lands at, and whether
  it starts `tracked` or `derived`.

Do all of it in one PR.

## 1. License gate

Read the license file at the import SHA, not at the default branch. Check for
a `LICENSE` inside any imported subdirectory too, since it overrides the root
license for paths under it.

Proceed only on MIT, BSD-2-Clause, BSD-3-Clause, ISC, or Apache-2.0. For
Apache-2.0, carry the upstream's own `NOTICE` file text into the receiving
NOTICE.

On anything else, **stop and ask the maintainer. Do not import.** That covers a
missing license, a `NOASSERTION` or custom license, copyleft (GPL, LGPL, AGPL,
MPL), and non-commercial or no-derivatives terms. Write nothing to the repo
until the maintainer clears it.

## 2. License file

Write the upstream's license text, verbatim and byte-for-byte, to
`LICENSE-<name>` at the repository root. Fetch the raw file at the import SHA.
Never retype it.

## 3. Import

Copy the mapped paths at the import SHA into their plugins. This has to happen
before step 4, because the lint fails on an outcome path that does not exist.
Registering the imported skills in their plugins (skills arrays, READMEs,
versions) follows CLAUDE.md's Plugin Registry rules.

## 4. Record entry

Append one upstream to `upstreams.json`. The fork point and the Pin are both
the import SHA. The log is seeded with one entry from `null` to that SHA:

```json
{
  "name": "<name>",
  "repository": "<repo-url>",
  "fork_point": { "sha": "<import sha>", "version": "<label>" },
  "pin": {
    "sha": "<import sha>",
    "version": "<label>",
    "committed": "<YYYY-MM-DD the import SHA was committed>",
    "reviewed": "<YYYY-MM-DD today>"
  },
  "log": [
    {
      "date": "<YYYY-MM-DD today>",
      "from": null,
      "to": "<import sha>",
      "pr": "<this PR's URL>",
      "note": "Initial import.",
      "outcomes": {
        "plugins/<plugin>/skills/<skill>/": "ported"
      },
      "candidates": []
    }
  ]
}
```

- **Every SHA is full.** The schema rejects a short one.
- **Version label.** Use the tag if the SHA is tagged. Otherwise use
  `<nearest tag>+<commits since>`, as in `v1.3.1+47`. Use the short SHA if the
  upstream has no tags.
- **Outcomes.** Mark every imported path `ported`, derived ones included. Each
  key is the plugin directory joined to the first cell of its NOTICE row,
  directories with a trailing slash. A key that differs from its row by even
  a slash fails the "newest entry names every tracked row" rule.
- **Seed entry shape.** Omit `backfilled`, because this entry is a real record.
  `candidates` stays `[]`, since an initial import has no untracked additions
  to decide on.
- **`pr`.** The schema accepts any string, so the lint cannot catch a
  placeholder. Fill in the real URL once the PR exists, before it merges.

## 5. NOTICE lineage

In each receiving plugin's `NOTICE.md` (modeled on `plugins/ph-plan/NOTICE.md`
if the plugin has none), add:

- **A copyright section.** The upstream copyright line as it appears in its
  license, the license name, and a link to `../../LICENSE-<name>`. Name every
  copyright holder whose work travels with the import.
- **A lineage table** under `## Upstream sources`, headed `### <name>`, where
  the heading text is exactly the record's `name`. The first cell is the
  backticked path relative to the plugin directory, and the last column is
  `State`:

  ```markdown
  | Skill | Upstream | State |
  | --- | --- | --- |
  | `skills/<skill>/` | `<upstream path>/` | tracked |
  | `skills/<other>/` | `<upstream path>/` | **derived**, forked from `<7-char sha>` |
  ```

A row is `derived` when the import is edited so heavily that upstream changes
cannot be applied to it. Add a sentence under the table explaining why, as the
existing NOTICEs do. A NOTICE never holds a full SHA or the words "reviewed
through".

Update any skill count in the NOTICE's opening paragraph.

## 6. Glossary

In `CONTEXT.md`, under `## Upstream`, add `### <name> upstream` after the
existing upstream subsections. Say who maintains it, what it is, which plugins
and skills it feeds, and which copyright lineages must travel with anything
taken from it. Update the count in the section's opening sentence.

These hand-written views also count upstreams, so update them too:

- `UPSTREAMS.md`: the intro sentence, the "What it is / Feeds" table, and the
  list of NOTICE links.
- `README.md`: the Acknowledgments list.

## 7. Regenerate and check

```bash
python scripts/lint-upstreams.py --apply
```

This regenerates the Pin table in `UPSTREAMS.md`, then checks the record
against every NOTICE. After that, run every check in CLAUDE.md's Checks section.
Fix what fails at its source. Never hand-edit the generated block.
