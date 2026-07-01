---
name: "senior-pm"
description:
  Triage a multi-project portfolio and report to executives. Use when the user needs a portfolio health review, a
  project status or executive report, a quantitative risk assessment, resource capacity or allocation planning, roadmap
  prioritization across initiatives, or program-level milestone tracking — especially enterprise-scale portfolios with
  multiple workstreams, complex dependencies, or multi-million-dollar budgets.
---

# Senior Project Management Expert

Strategic portfolio management for enterprise software, SaaS, and digital transformation. The core move is **triage**:
run the analyzers, sort the portfolio into what is healthy and what breaches a threshold, and stop to escalate every
breach before advancing to synthesis. Each analyzer emits a checkable signal (RAG status, risk score, utilization band);
a project either clears its threshold or gets flagged. Never fold a breach silently into an executive summary.

## Scripts

Three analyzers do the quantitative triage. Run each with `uv` (which reads the PEP 723 header and needs no separate
install):

```bash
uv run scripts/project_health_dashboard.py <portfolio.json>
uv run scripts/risk_matrix_analyzer.py <portfolio.json>
uv run scripts/resource_capacity_planner.py <portfolio.json>
```

All three read one JSON file whose shape is defined by `assets/sample_project_data.json` — the required **input
schema**. Before running, marshal the portfolio into that schema: `projects[]` (id, status, priority, dates, budget,
timeline, quality_metrics), `resources[]` (id, role, hourly_rate, current_utilization, skills), and `risks[]` (id,
category, probability 1-5, impact 1-5, status, mitigation_actions). Missing fields fall back to defaults and silently
distort scores, so validate the marshaled data against the sample before running.

If `uv` is unavailable, compute the same signals by hand: health scoring from the dimension weights below, risk scores
and responses from `references/risk-management-framework.md`, prioritization from
`references/portfolio-prioritization-models.md`.

## Portfolio Health Review Workflow

Run the three analyzers in order. Each step's completion criterion is a triage gate: resolve the flagged breach before
advancing.

1. **Marshal and validate input.** Produce the portfolio JSON in the `assets/sample_project_data.json` schema.
   - Completion criterion: every project has non-null `budget`, `timeline`, `status`, and `priority`; every risk has
     `probability` and `impact` in 1-5; every resource has `current_utilization`. No field left to a silent default.

2. **Health dashboard.** `uv run scripts/project_health_dashboard.py <portfolio.json>`. The script weights Timeline 25%,
   Budget 25%, Scope 20%, Quality 20%, Risk 10% into a composite score, then assigns RAG (Green ≥80, Amber 60-79, Red
   <60).
   - ⚠️ If any active project is Red (composite <60), STOP: escalate to the project sponsor and record a recovery action
     before running the next analyzer.
   - Completion criterion: every active project has a RAG status, and every Red project has a named owner and recovery
     action logged.

3. **Risk matrix.** `uv run scripts/risk_matrix_analyzer.py <portfolio.json>`. Scores each risk
   `probability × impact × category_weight` and assigns a response (Avoid / Mitigate / Transfer / Accept) by the
   thresholds in `references/risk-management-framework.md`.
   - ⚠️ If any risk lands in the Avoid band (score >18), STOP and initiate sponsor escalation before proceeding.
   - Completion criterion: every active risk has a score and a response strategy; every Avoid/Mitigate risk has a named
     owner and a target resolution date.

4. **Resource capacity.** `uv run scripts/resource_capacity_planner.py <portfolio.json>`. Reports per-resource
   utilization against bands (under <60%, optimal 60-85%, over 85-95%, critical >95%) and flags capacity gaps.
   - ⚠️ If any resource is critical (>95%) or a project has an unfilled capacity gap, flag it for a reallocation
     decision before synthesis.
   - Completion criterion: every resource sits in a named utilization band, and every flagged over-allocation or gap has
     a reallocation recommendation attached.

5. **Executive synthesis.** Fold the three outputs into `assets/executive_report_template.md`. For the portfolio KPI
   definitions and target thresholds the report grades against (on-time delivery, budget variance, ROI, utilization),
   use `references/portfolio-kpis.md`.
   - Completion criterion: the report names every Red project, every Avoid-band risk, and every critical resource
     surfaced in steps 2-4 — none dropped — each with its escalation or recommendation. If the count of flagged items in
     the report is less than the count raised by the analyzers, the report is incomplete.

## Prioritization

When the task is ranking initiatives rather than reviewing health, select one model by context and apply it. Formulas,
scoring rubrics, worked examples, and the full selection decision tree live in
`references/portfolio-prioritization-models.md` — reach for it whenever you need the exact math or a model this summary
does not cover.

- **WSJF** — resource-constrained agile portfolios with quantifiable cost of delay.
- **RICE** — customer-facing initiatives where reach and impact are measurable.
- **ICE** — rapid ranking during ideation or when analysis time is short.
- **MoSCoW** — multiple stakeholder groups needing scope alignment.
- **MCDA** — complex trade-offs across incommensurable criteria.

Completion criterion: every candidate initiative carries a score from the chosen model and a rank; ties are broken and
recorded.

## Risk Management

For anything beyond the health-review risk gate — classification, EMV, Monte Carlo schedule modeling, portfolio risk
correlation, risk-appetite bands, or the response-score thresholds — use `references/risk-management-framework.md`. It
holds the category weights, the three-point estimation and correlation formulas, the EMV reference implementation, and
the escalation authority matrix. Reach for it when quantifying financial exposure or setting contingency reserves.

## Assets

- `assets/sample_project_data.json` — the input schema for all three scripts and a worked example portfolio.
- `assets/expected_output.json` — reference outputs showing how the three analyzers' results complement each other.
- `assets/project_charter_template.md` — 12-section charter (strategic alignment, success criteria, RACI, risk, budget,
  timeline).
- `assets/executive_report_template.md` — board-level report (RAG dashboard, financial performance, risk heat map,
  capacity, forward recommendations).
- `assets/raci_matrix_template.md` — phase-based responsibility assignment with escalation paths.

## Atlassian Integration

Pull live portfolio data and publish reports through the Atlassian MCP. Use only tools listed in
`references/atlassian-mcp-tools.md` — never invent tool names.

- Read cross-project metrics and risk registers from Jira with `searchJiraIssuesUsingJql`.
- Publish executive reports to Confluence with `createConfluencePage` (body must be storage-format XHTML or ADF, not
  wiki markup).

## Related Skills

- **Scrum Master** (`project-manager/scrum-master/`) — sprint velocity data feeds the health dashboard's Timeline and
  Quality dimensions.
