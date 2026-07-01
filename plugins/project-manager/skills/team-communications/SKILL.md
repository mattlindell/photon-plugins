---
name: team-communications
description: >-
  Dispatch internal company communications. Use when the user asks to draft, edit, or format a message for an internal
  audience — 3P update, company newsletter, FAQ roundup, leadership update, status report, or any internal comms
  request. Trigger on: "3P", "weekly update", "newsletter", "FAQ", "internal comms", "status report", "company update",
  "team update", "incident report", "write my update", or "summarize what my team did".
---

# Internal Comms

Dispatch the right format, load its reference, then draft.

## Routing

Match the request to a communication type, then read the reference file before writing anything:

| Type           | Trigger phrases                                                               | Reference file                     |
| -------------- | ----------------------------------------------------------------------------- | ---------------------------------- |
| **3P Update**  | "3P", "progress plans problems", "weekly team update", "what did we ship"     | `references/3p-updates.md`         |
| **Newsletter** | "newsletter", "company update", "weekly/monthly roundup", "all-hands summary" | `references/company-newsletter.md` |
| **FAQ**        | "FAQ", "common questions", "what people are asking", "confusion around"       | `references/faq-answers.md`        |
| **General**    | anything internal that doesn't match above                                    | `references/general-comms.md`      |

If the type is ambiguous, ask one clarifying question — don't guess.

## Workflow

1. **Read the reference file** for the matched type. Follow its formatting exactly. Criterion: the format, length
   constraints, and required sections from the reference file are loaded and understood.
2. **Gather inputs.** Use available MCP tools (Slack, Gmail, Google Drive, Calendar) to pull real data. Tool-unavailable
   fallback is covered in each reference file. Criterion: every field the reference format requires has a value —
   sourced from tools, user-provided content, or explicitly marked as unknown.
3. **Clarify scope.** Confirm the inputs the reference file requires before drafting — team name (for 3Ps), time period,
   audience. Criterion: no required scope field is still open.
4. **Draft.** Follow the format, tone, and length constraints from the reference file precisely. Criterion: draft
   matches the reference format exactly, with no invented fields or fabricated data.

## Related Skills

| Skill                               | Relationship                                                 |
| ----------------------------------- | ------------------------------------------------------------ |
| `project-manager/senior-pm`         | Broader PM scope — status reports feed into PM reporting     |
| `project-manager/meeting-analyzer`  | Meeting insights can feed into 3P updates and status reports |
| `project-manager/confluence-expert` | Publish comms as Confluence pages for permanent record       |
