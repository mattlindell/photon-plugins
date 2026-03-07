---
description: Process ideas from the inbox - triage, evaluate, integrate or archive
---

# Process Inbox

You have been invoked with: `/process-inbox`

## Protocol

Process all pending ideas in the inbox following the self-maintenance protocol from CLAUDE.md.

---

### Phase 1: Load Inbox

1. Read `docs/inbox/ideas.md`
2. Identify all ideas with `**Status**: pending`
3. If no pending ideas, report "Inbox empty - no ideas to process" and exit

---

### Phase 2: Triage Each Idea

For each pending idea, determine:

| Question | YES | NO |
|----------|-----|-----|
| Is this idea actionable? | → Proceed to Evaluate | → Archive with reason |
| Is this a duplicate of existing knowledge? | → Archive as duplicate | → Proceed |

**Archive format** (add to `docs/archive/dismissed-ideas.md`):
```
| [date] | [idea title] | [reason: not actionable / duplicate / out of scope] |
```

---

### Phase 3: Evaluate Actionable Ideas

For each actionable idea:

1. **Category fit**: Which existing framework category does this belong to?
   - If fits existing: Note target document
   - If new pattern: Propose new knowledge doc name

2. **Confidence**: How validated is this idea?
   - HIGH: Multiple sources, tested in practice
   - MEDIUM: Single source, reasonable logic
   - LOW: Speculative, needs validation

3. **Integration recommendation**:
   - Add to `docs/frameworks/quality-categories.md` section?
   - Add to existing knowledge doc?
   - Create new `docs/knowledge/[topic].md`?
   - Needs user decision (ambiguous)?

---

### Phase 4: Present Recommendations

For each evaluated idea, present:

```
## Idea: [title]

**Source**: [from idea]
**Category Fit**: [assessment]
**Confidence**: HIGH | MEDIUM | LOW
**Recommendation**: [integrate to X | create new doc | needs user decision]
**Proposed Content**:
[Draft of how the idea would be integrated]
```

---

### Phase 5: Await User Decision

After presenting all recommendations:

```
┌─────────────────────────────────────────────┐
│ Inbox Processing Complete                   │
├─────────────────────────────────────────────┤
│ Processed: [N] ideas                        │
│ - Archived: [X]                             │
│ - Ready to integrate: [Y]                   │
│ - Need user decision: [Z]                   │
├─────────────────────────────────────────────┤
│ Actions:                                    │
│ [1] Integrate all recommendations           │
│ [2] Review each individually                │
│ [3] Defer processing                        │
└─────────────────────────────────────────────┘
```

---

### Phase 6: Execute Integration

If user approves:

1. **Update target documents** with new content
2. **Remove processed ideas** from `docs/inbox/ideas.md`
3. **Log changes** to `docs/changelog.md`:
   ```
   | [date] | integrated | [idea title] | [target doc] | [brief note] |
   ```
4. **Report completion** with summary of changes made

---

## Curation Rules (from CLAUDE.md)

- Max 5 "always read" documents
- Flag docs not referenced in 30 days
- Check for duplication before adding
- Each item must cite source/evidence

---

## Begin

Read `docs/inbox/ideas.md` and process all pending ideas.
