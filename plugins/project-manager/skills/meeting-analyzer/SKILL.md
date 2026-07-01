---
name: meeting-analyzer
description: >
  Signal — use when the user uploads or points to meeting transcripts (.txt, .md, .vtt, .srt, .docx), asks how they
  come across in meetings, wants speaking ratio or filler-word analysis, or mentions Granola, Otter, Fireflies, or Zoom
  transcripts. Also trigger when the user asks about communication habits, conflict avoidance, or wants coaching
  feedback compared across time periods.
---

# Meeting Analyzer

Surface the signal in meeting transcripts: behavioral patterns, communication anti-patterns, and evidence-backed
coaching feedback.

Load [`REFERENCE.md`](REFERENCE.md) at the start of Step 3 — it contains the analysis module definitions, edge-case
rules, anti-patterns, and transcript source tips needed to run the analysis.

## Steps

### 1. Ingest & Inventory

Scan the target directory for transcript files (`.txt`, `.md`, `.vtt`, `.srt`, `.docx`, `.json`).

For each file:

- Extract meeting date from filename or content (expect `YYYY-MM-DD` prefix or embedded timestamps)
- Identify speaker labels — look for patterns like `Speaker 1:`, `[John]:`, `John Smith  00:14:32`, VTT/SRT cue
  formatting
- Detect the user's identity: ask if ambiguous, otherwise infer from the most frequent speaker or filename hints
- Log: filename, date, duration (from timestamps), participant count, word count

**Completion criterion:** A printed inventory table listing every discovered file, its date, duration, participant
count, and word count — user has confirmed the scope before analysis proceeds.

### 2. Normalize Transcripts

Normalize every file into a common internal structure before analysis:

```text
{ speaker: string, timestamp_sec: number | null, text: string }[]
```

Handling per format:

- **VTT/SRT**: Parse cue timestamps + text. Speaker labels may be inline (`<v Speaker>`) or prefixed.
- **Plain text**: Look for `Name:` or `[Name]` prefixes per line. If no speaker labels exist, warn the user that
  per-speaker analysis is limited.
- **Markdown**: Strip formatting, then treat as plain text.
- **DOCX**: Extract text content, then treat as plain text.
- **JSON**: Expect an array of objects with `speaker`/`text` fields (common Otter/Fireflies export).

If timestamps are missing, skip timing-dependent metrics (speaking pace, pause analysis) and run text-based analysis
only.

**Completion criterion:** Every file from the inventory has a normalized record array; files missing speaker labels are
flagged; files without timestamps are noted with skipped metrics listed.

### 3. Analyze

Load [`REFERENCE.md`](REFERENCE.md) — the module definitions, edge-case rules, and anti-pattern guide are there.

Run every applicable analysis module from REFERENCE.md. Skip any module that doesn't apply (e.g., skip Speaking Dynamics
if there are no speaker labels; skip Facilitation if the user is not the organizer).

**Completion criterion:** Every applicable module has been run and its findings recorded; each skipped module is listed
with the reason it was skipped.

### 4. Output the Report

Produce a single cohesive report using this structure — omit any section where data was insufficient:

```markdown
# Meeting Insights Report

**Period**: [earliest date] – [latest date]
**Meetings analyzed**: [count]
**Total transcript words**: [count]
**Your speaking share (avg)**: [X%]

---

## Top 3 Findings

[Rank by impact. Each finding gets 2-3 sentences + one concrete example with a direct quote and timestamp.]

## Detailed Analysis

### Speaking Dynamics
[Stats table + narrative interpretation + flagged red flags]

### Directness & Conflict Patterns
[Flagged instances grouped by pattern type, with quotes and rewrites]

### Verbal Habits
[Filler word stats, contextual spikes, only if rate > 3/100 words]

### Listening & Questions
[Question type breakdown, listening indicators, specific examples]

### Facilitation
[Only if applicable — agenda, decisions, action items]

### Energy & Sentiment
[Arc summary, flagged drops]

## Strengths

[3 specific things the user does well, with evidence]

## Growth Opportunities

[3 ranked by impact, each with: what to change, why it matters, a concrete "try this next time" action]

## Comparison to Previous Period

[Only if prior analysis exists — delta on key metrics]
```

**Completion criterion:** Report is complete and follows the template; every section with sufficient data is populated;
every omitted section is omitted (not left as a placeholder); Top 3 Findings each include a direct quote and timestamp.

### 5. Follow-Up Options

After delivering the report, offer:

- Deep dive into any specific meeting or pattern
- A 1-page "communication cheat sheet" with the user's top 3 habits to change
- Tracking setup — save current metrics as a baseline for future comparison
- Export as markdown or structured JSON for use in performance reviews

**Completion criterion:** The four follow-up options are offered to the user; any option the user selects is completed
before the skill ends.
