# project-manager

A Claude Code plugin for project management and Atlassian work — Jira, Confluence, Atlassian administration and
templates, Scrum Master analytics, senior-PM portfolio management, meeting analysis, and internal team communications.

- **Version:** 1.0.1
- **Author:** Matt Lindell <misterphoton@gmail.com>
- **License:** MIT

---

## Plugin Structure

```text
plugins/project-manager/
  .claude-plugin/
    plugin.json
  .mcp.json                       # bundles the Atlassian Remote MCP server (key: atlassian)
  references/
    atlassian-mcp-tools.md        # canonical Atlassian MCP tool list (shared across skills)
  skills/
    atlassian-admin/
      SKILL.md
      references/                 # security-hardening guide, user-provisioning checklist
      assets/                     # permission_scheme_template.json
    atlassian-templates/
      SKILL.md
      references/                 # governance framework, template design patterns
    confluence-expert/
      SKILL.md
      references/                 # macro cheat sheet, space-architecture patterns, templates
    jira-expert/
      SKILL.md
      references/                 # workflows, automation, automation examples, JQL examples
    meeting-analyzer/
      SKILL.md
    scrum-master/
      SKILL.md
      references/                 # retro formats, team-dynamics framework, velocity forecasting
      scripts/                    # velocity_analyzer.py, sprint_health_scorer.py
      assets/                     # sample sprint data + report/health-check templates
    senior-pm/
      SKILL.md
      references/                 # portfolio KPIs, prioritization models, risk-management framework
      scripts/                    # project_health_dashboard.py, resource_capacity_planner.py, risk_matrix_analyzer.py
      assets/                     # sample project data + charter/RACI/executive-report templates
    team-communications/
      SKILL.md
      references/                 # 3P updates, newsletter, FAQ answers, general comms
```

---

## Skills

Skills provide concrete workflows, reference material, and templates that Claude routes to when helping with project
management and Atlassian work.

| Skill                   | Description                                                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **jira-expert**         | Configure Jira projects, write JQL and advanced searches, and build workflows, dashboards, custom fields, and automation           |
| **confluence-expert**   | Build and restructure Confluence spaces, page hierarchies, macros, templates, and documentation governance                         |
| **atlassian-admin**     | Administer Atlassian Cloud — users, groups, permissions, SSO, apps, and org-wide governance (via UI/REST; admin ops aren't on MCP) |
| **atlassian-templates** | Create and manage reusable Jira/Confluence templates, blueprints, and standardized content structures                              |
| **scrum-master**        | Data-driven sprint analysis — Monte Carlo velocity forecasting, multi-dimension team-health scoring, and retrospective analysis    |
| **senior-pm**           | Portfolio management, quantitative risk analysis (EMV, Monte Carlo, WSJF), resource planning, and executive reporting              |
| **meeting-analyzer**    | Analyze meeting transcripts for communication patterns, anti-patterns, and actionable coaching feedback                            |
| **team-communications** | Draft internal comms — 3P updates, newsletters, FAQ roundups, and status reports in your company's exact format                    |

---

## Installation

This plugin is distributed through the photon-plugins marketplace. Add the marketplace, then install the plugin:

```bash
/plugin marketplace add mattlindell/photon-plugins
/plugin install project-manager@photon-plugins
```

**For local development (point to the plugin directory):**

```bash
claude --plugin-dir /path/to/photon-plugins/plugins/project-manager
```

---

## Atlassian MCP server

The plugin bundles the [Atlassian Remote MCP server](https://www.atlassian.com/platform/remote-mcp-server) via
`.mcp.json` under the server key `atlassian`:

```json
{
  "mcpServers": {
    "atlassian": {
      "type": "http",
      "url": "https://mcp.atlassian.com/v1/mcp"
    }
  }
}
```

The Jira, Confluence, and template skills call these tools directly. In Claude Code each tool surfaces as
`mcp__atlassian__<toolName>` (camelCase) — the canonical, verified tool list lives in
[`references/atlassian-mcp-tools.md`](references/atlassian-mcp-tools.md), and the skills are instructed never to invent
tool names outside it.

First use triggers a browser-based OAuth flow to authorize your Atlassian Cloud site. **Admin operations** (user/group
provisioning, permission schemes, SSO, workflow/field configuration, space and project creation) are **not** available
through the MCP server — `atlassian-admin` routes those to `admin.atlassian.com` or the Atlassian REST API.
