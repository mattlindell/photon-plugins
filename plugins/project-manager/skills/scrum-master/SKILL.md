---
name: "scrum-master"
description:
  "Coach a scrum team through its sprint cadence with data-driven analysis. Use when the user asks about sprint planning,
  velocity or capacity forecasting, sprint health, retrospectives, standup facilitation, blocker resolution, story
  points, burndown, team maturity, or agile team health. Runs Python scripts over a sprint JSON export
  (velocity_analyzer.py for Monte Carlo capacity forecasts, sprint_health_scorer.py for weighted 0-100 health grades)
  and falls back to documented formulas when the tooling is unavailable."
---

# Scrum Master

Coach a scrum team through its **cadence** — the recurring loop of plan, standup, review, and retrospective — using
velocity analytics, probabilistic forecasting, and team-development framing. Two Python scripts do the heavy statistics;
the references hold the formulas behind them so the work never depends on the tooling being present.

## Data foundation

Both scripts read one JSON file whose schema is defined by `assets/sample_sprint_data.json` (a complete 6-sprint
example; `assets/expected_output.json` shows the corresponding results — velocity avg 20.2 pts, CV 12.7%, health score
78.3/100). Marshal any Jira or board export into that schema before running a script — MCP cannot read boards or sprints
directly (see `../../references/atlassian-mcp-tools.md`), so pull the raw issues you can and shape them into the
`sprints[]` / `retrospectives[]` arrays yourself.

Run scripts with `uv`, not `python3`:

```bash
uv run scripts/velocity_analyzer.py <data.json> --format text
uv run scripts/sprint_health_scorer.py <data.json> --format text
```

Both accept `--format json` for downstream processing. If `uv` is unavailable, every metric each script produces can be
computed by hand from the formulas in `references/velocity-forecasting-guide.md` (forecasting, CV) and the dimension
thresholds below.

## Sprint planning

1. Forecast capacity: marshal the sprint history into the data schema, then run
   `uv run scripts/velocity_analyzer.py <data.json> --format text`. Fallback: compute the Monte Carlo forecast manually
   using the formulas in `references/velocity-forecasting-guide.md`. **Done when** you hold a 6-sprint forecast with
   50/70/85/95% confidence intervals and a stated CV. If fewer than 3 sprints exist, stop and request more data — no
   forecast is defensible below that.
2. Set the commitment ceiling at the 70% confidence interval, adjusted down for known capacity loss (leave,
   dependencies). **Done when** the proposed backlog total sits at or below that adjusted ceiling and every capacity
   assumption is written down for next-sprint comparison.
3. If CV exceeds 20%, present the range to stakeholders rather than a single number. **Done when** the forecast has been
   communicated as a range wherever volatility is high.

## Daily standup

1. Log every blocker with its open date the moment it surfaces; escalate any blocker still open after 2 days. **Done
   when** each active blocker has an open date recorded and none older than 2 days is un-escalated.
2. Capture ceremony attendance and engagement into the sprint's `ceremonies` object for end-of-sprint scoring. **Done
   when** the sprint record carries attendance and engagement for each ceremony held.

## Sprint review

1. Present the velocity trend and latest health score alongside the demo so stakeholders read delivery in context.
   **Done when** both figures accompany the demo.
2. Record every scope-change request raised as an `added_points`/`removed_points` event in the sprint data. **Done
   when** all in-review scope changes are captured for the next scoring cycle.

## Sprint retrospective

1. Score sprint health before the session: `uv run scripts/sprint_health_scorer.py <data.json> --format text`. The
   scorer weights six dimensions into a 0-100 grade:

   | Dimension                     | Weight | Target                 |
   | ----------------------------- | ------ | ---------------------- |
   | Commitment reliability        | 25%    | >85% of planned points |
   | Scope stability               | 20%    | <15% mid-sprint change |
   | Blocker resolution            | 15%    | <3 days average        |
   | Ceremony engagement           | 15%    | >90% participation     |
   | Story completion distribution | 15%    | High ratio fully done  |
   | Velocity predictability       | 10%    | CV <20%                |

   Fallback: score each dimension by hand against these targets. **Done when** you have an overall grade plus the two
   lowest-scoring dimensions identified, and any dimension the data can't support is reported as a gap rather than
   scored. The scorer needs 2+ sprints with ceremony and story data.

2. Choose a retrospective format fit to the team's mood and open on the health score and its weakest dimensions. Format
   menu and facilitation practices are in `references/retro-formats.md`. **Done when** a format is selected and the
   session is framed around the flagged dimensions.
3. Gauge how many action items the team can absorb from its recent completion rate — the thresholds and manual scoring
   live in the "Retrospective Analysis" section of `references/retro-formats.md`. **Done when** the new-action-item
   count respects that ceiling (cap at 2-3 if completion is below 60%).
4. Give every action item an owner and a measurable success criterion, and record it in the data for next cycle. **Done
   when** no action item lacks an owner, a criterion, or a place in the sprint data.

## Team development

Run the health scorer across several sprints and read the trend, then place the team on a Tuckman stage and match
facilitation to it. The per-stage metric ranges (CV, psychological-safety index, ceremony participation), stage-specific
interventions, the Edmondson 7-point safety scale, and crisis-intervention triggers are all in
`references/team-dynamics-framework.md` — reach it whenever you need to classify a stage or pick an intervention.

- **Assess** — map velocity CV and survey scores to a stage; supplement with an anonymous psychological-safety pulse
  (target >4.0/5.0) and 1:1 observation. If the team reads as forming or storming, prioritize safety and conflict
  facilitation before process optimization. **Done when** the team is placed on one stage with corroborating
  quantitative and qualitative evidence.
- **Measure progress** — target overall health improvement of ≥5 points per quarter and a rising safety index. If scores
  plateau or regress for 2 consecutive sprints, escalate per the crisis-intervention triggers in the framework. **Done
  when** the trend is compared against these targets and any 2-sprint regression has triggered escalation.

## Limitations

- Fewer than 6 sprints weakens Monte Carlo confidence — always state intervals, never point estimates.
- Missing ceremony or story fields suppress the affected health dimensions — report the gap, don't infer.
- Scores demand qualitative interpretation: organizational context, cross-team dependencies, and team factors outside
  the JSON are not modeled. Techniques assume 5-9 member teams.

## Related skills

- **Senior PM** (`../senior-pm/`) — portfolio health context informs sprint priorities.

## References and assets

- `references/velocity-forecasting-guide.md` — Monte Carlo formulas, CV, confidence intervals (the forecasting
  fallback).
- `references/team-dynamics-framework.md` — Tuckman stages with metric ranges, psychological safety, interventions.
- `references/retro-formats.md` — retrospective format menu, facilitation practices, and manual retrospective analysis.
- `assets/sprint_report_template.md`, `assets/team_health_check_template.md` — report templates.
