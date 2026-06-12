# nonprofit-toolkit

A Claude Code plugin providing practical skills for nonprofit organizations — grant writing, budgeting, donor stewardship, communications, and volunteer management.

**Version:** 1.0.0
**Author:** Matt Lindell <misterphoton@gmail.com>
**License:** MIT

---

## Plugin Structure

```text
plugins/nonprofit-toolkit/
  .claude-plugin/
    plugin.json
  skills/
    budget-creation/
      SKILL.md
    donor-thank-you/
      SKILL.md
    grant-writing-basics/
      SKILL.md
    organization-profile-builder/
      SKILL.md
    social-media-content/
      SKILL.md
    volunteer-scheduling/
      SKILL.md
    givebutter-integration/
      SKILL.md
```

---

## Skills

Skills provide concrete implementation patterns, templates, and best practices that Claude routes to when helping with nonprofit work.

Start with **organization-profile-builder** — it builds a reusable profile that makes every other skill produce on-brand, contextually relevant output.

| Skill                            | Description                                                                                          |
| -------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **organization-profile-builder** | Build a comprehensive organizational profile that personalizes all other skills                     |
| **grant-writing-basics**         | Draft compelling grant proposal components — needs statements, SMART objectives, narratives          |
| **budget-creation**              | Create clear, accurate budgets for grants, programs, events, or annual operations with narratives    |
| **donor-thank-you**              | Write warm, effective donor thank you and stewardship communications that strengthen relationships   |
| **social-media-content**         | Generate mission-aligned posts, content calendars, and campaigns across Facebook, Instagram, LinkedIn, and Twitter/X |
| **volunteer-scheduling**         | Create volunteer schedules, recruitment messages, role descriptions, shift reminders, and hour logs  |
| **givebutter-integration**       | Reference for the Givebutter MCP — when to ground skills in live fundraising data and why the server is a remote Cloudflare Worker (see [Givebutter MCP server](#givebutter-mcp-server-optional)) |

---

## Installation

This plugin is distributed through the Caffelli plugin marketplace. Add the marketplace, then install the plugin:

```bash
/plugin marketplace add caffelli/plugin-marketplace
/plugin install nonprofit-toolkit@plugin-marketplace
```

**For local development (point to the plugin directory):**

```bash
claude --plugin-dir /path/to/plugins/nonprofit-toolkit
```

---

## Givebutter MCP server (optional)

The plugin can connect to [Givebutter](https://givebutter.com), exposing campaigns, contacts, transactions, households, and financial data to the skills above (e.g. pulling live donor records into a thank-you draft). The integration is **optional** — every skill works without it.

### Connecting the plugin

The endpoint URL is **not** committed to this repo. When you enable the plugin, Claude Code prompts for two values (declared in `plugin.json` under `userConfig`):

| Prompt                        | Value                                                                                          |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| **Givebutter MCP server URL** | Your Worker's `/mcp` endpoint, e.g. `https://givebutter-mcp.<subdomain>.workers.dev/mcp`. Leave blank to skip the integration. |
| **Givebutter MCP access token** | The `MCP_AUTH_TOKEN` you set on the Worker. Stored in secure storage. Leave blank if the Worker has no token. |

Those values populate the plugin's `.mcp.json` at enable time:

```json
{
  "mcpServers": {
    "givebutter": {
      "type": "http",
      "url": "${user_config.givebutter_mcp_url}",
      "headers": {
        "Authorization": "Bearer ${user_config.givebutter_mcp_token}"
      }
    }
  }
}
```

If the URL is left blank, the `givebutter` server simply isn't connected and the rest of the plugin's skills continue to work.
