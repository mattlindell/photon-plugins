# Meeting Analyzer — Reference

Analysis module definitions, edge-case rules, anti-patterns, and transcript source tips for the `meeting-analyzer`
skill.

---

## Analysis Modules

### Module: Speaking Dynamics

Calculate per-speaker:

- **Word count & percentage** of total meeting words
- **Turn count** — how many times each person spoke
- **Average turn length** — words per uninterrupted speaking turn
- **Longest monologue** — flag turns exceeding 60 seconds or 200 words
- **Interruption detection** — a turn that starts within 2 seconds of the previous speaker's last timestamp, or
  mid-sentence breaks

Produce a per-meeting summary and a cross-meeting average if multiple transcripts exist.

Red flags to surface:

- User speaks > 60% in a 1:many meeting (dominating)
- User speaks < 15% in a meeting they're facilitating (disengaged or over-delegating)
- One participant never speaks (excluded voice)
- Interruption ratio > 2:1 (user interrupts others twice as often as they're interrupted)

---

### Module: Conflict & Directness

Scan the user's speech for hedging and avoidance markers.

**Hedging language** (score per-instance, aggregate per meeting):

- Qualifiers: "maybe", "kind of", "sort of", "I guess", "potentially", "arguably"
- Permission-seeking: "if that's okay", "would it be alright if", "I don't know if this is right but"
- Deflection: "whatever you think", "up to you", "I'm flexible"
- Softeners before disagreement: "I don't want to push back but", "this might be a dumb question"

**Conflict avoidance patterns** (requires more context, flag with confidence level):

- Topic changes after tension (speaker A raises problem → user pivots to logistics)
- Agreement-without-commitment: "yeah totally" followed by no action or follow-up
- Reframing others' concerns as smaller than stated: "it's probably not that big a deal"
- Absent feedback in 1:1s where performance topics would be expected

For each flagged instance, extract:

- The full quote (with surrounding context — 2 turns before and after)
- A severity tag: `low` (single hedge word), `medium` (pattern of hedging in one exchange), `high` (clearly avoided a
  necessary conversation)
- A rewrite suggestion: what a more direct version would sound like

---

### Module: Filler Words & Verbal Habits

Count occurrences of: "um", "uh", "like" (non-comparative), "you know", "actually", "basically", "literally", "right?"
(tag question), "so yeah", "I mean"

Report:

- Total count per meeting
- Rate per 100 words spoken (normalizes across meeting lengths)
- Breakdown by filler type
- Contextual spikes — do fillers increase in specific situations? (e.g., when responding to a senior stakeholder, when
  giving negative feedback, when asked a question cold)

Only flag this as an issue if the rate exceeds ~3 per 100 words. Below that, it's normal speech.

---

### Module: Question Quality & Listening

Classify the user's questions:

- **Closed** (yes/no): "Did you finish the report?"
- **Leading** (answer embedded): "Don't you think we should ship sooner?"
- **Open genuine**: "What's blocking you on this?"
- **Clarifying** (references prior speaker): "When you said X, did you mean Y?"
- **Building** (extends another's idea): "That's interesting — what if we also Z?"

Good listening indicators:

- Clarifying and building questions (shows active processing)
- Paraphrasing: "So what I'm hearing is..."
- Referencing a point someone made earlier in the meeting
- Asking quieter participants for input

Poor listening indicators:

- Asking a question that was already answered
- Restating own point without acknowledging the response
- Responding to a question with an unrelated topic

Report the ratio of open/clarifying/building vs. closed/leading questions.

---

### Module: Facilitation & Decision-Making

Only apply when the user is the meeting organizer or facilitator.

Evaluate:

- **Agenda adherence**: Did the meeting follow a structure or drift?
- **Time management**: How long did each topic take vs. expected?
- **Inclusion**: Did the facilitator actively draw in quiet participants?
- **Decision clarity**: Were decisions explicitly stated? ("So we're going with option B — Sarah owns the follow-up by
  Friday.")
- **Action items**: Were they assigned with owners and deadlines, or left vague?
- **Parking lot discipline**: Were off-topic items acknowledged and deferred, or did they derail?

---

### Module: Sentiment & Energy

Track the emotional arc of the user's language across the meeting:

- **Positive markers**: enthusiastic agreement, encouragement, humor, praise
- **Negative markers**: frustration, dismissiveness, sarcasm, curt responses
- **Neutral/flat**: low-energy responses, monosyllabic answers

Flag energy drops — moments where the user's engagement visibly decreases (shorter turns, less substantive responses).
These often correlate with discomfort, boredom, or avoidance.

---

## Edge Cases

- **No speaker labels**: Warn the user upfront. Run text-level analysis (filler words, question types on the full
  transcript) but skip per-speaker metrics. Suggest re-exporting with speaker diarization enabled.
- **Very short meetings** (< 5 minutes or < 500 words): Analyze but caveat that patterns from short meetings may not be
  representative.
- **Non-English transcripts**: The filler word and hedging dictionaries are English-centric. For other languages, note
  the limitation and focus on structural analysis (speaking ratios, turn-taking, question counts).
- **Single meeting vs. corpus**: If only one transcript, skip trend/comparison language. Focus findings on that meeting
  alone.
- **User not identified**: If you can't determine which speaker is the user after scanning, ask before proceeding. Don't
  guess.

---

## Anti-Patterns

| Anti-Pattern                                | Why It Fails                                                          | Better Approach                                                                       |
| ------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Analyzing without speaker labels            | Per-person metrics impossible — results are generic word clouds       | Ask user to re-export with speaker identification enabled                             |
| Running all modules on a 5-minute standup   | Overkill — filler word and conflict analysis need 20+ min meetings    | Auto-detect meeting length and skip irrelevant modules                                |
| Presenting raw metrics without context      | "You said 'um' 47 times" is demoralizing without benchmarks           | Always compare to norms and show trajectory over time                                 |
| Analyzing a single meeting in isolation     | One meeting is a snapshot, not a pattern — conclusions are unreliable | Require 3+ meetings minimum for trend-based coaching                                  |
| Treating speaking time equality as the goal | A facilitator SHOULD talk less; a presenter SHOULD talk more          | Weight speaking ratios by meeting type and role                                       |
| Flagging every hedge word as negative       | "I think" and "maybe" are appropriate in brainstorming                | Distinguish between decision meetings (hedges are bad) and ideation (hedges are fine) |

---

## Transcript Source Tips

Include this section in output only if the user seems unsure about how to get transcripts:

- **Zoom**: Settings → Recording → enable "Audio transcript". Download `.vtt` from cloud recordings.
- **Google Meet**: Auto-transcription saves to Google Docs in the calendar event's Drive folder.
- **Granola**: Exports to markdown. Best speaker label quality of consumer tools.
- **Otter.ai**: Export as `.txt` or `.json` from the web dashboard.
- **Fireflies.ai**: Export as `.docx` or `.json` — both work.
- **Microsoft Teams**: Transcripts appear in the meeting chat. Download as `.vtt`.

Recommend `YYYY-MM-DD - Meeting Name.ext` naming convention for easy chronological analysis.

---

## Related Skills

| Skill                               | Relationship                                                     |
| ----------------------------------- | ---------------------------------------------------------------- |
| `project-manager/senior-pm`         | Broader PM scope — use for project planning, risk, stakeholders  |
| `project-manager/scrum-master`      | Agile ceremonies — pairs with meeting-analyzer for retro quality |
| `project-manager/confluence-expert` | Store meeting analysis outputs as Confluence pages               |
| `c-level-advisor/executive-mentor`  | Executive communication coaching — complementary perspective     |
