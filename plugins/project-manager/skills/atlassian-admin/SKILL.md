---
name: "atlassian-admin"
description: >-
  Use when administering an Atlassian org (Jira, Confluence, Bitbucket, Trello) beyond what the Atlassian MCP can reach:
  provisioning or deprovisioning users, managing groups, designing permission schemes, configuring SSO or SCIM,
  installing marketplace apps, setting org security or authentication policies, running access or security reviews, or
  any org-wide governance task. Also use when another skill hits an admin action MCP cannot perform and hands it off.
---

# Atlassian Administrator

**Admin operations are NOT available via the Atlassian MCP.** The canonical tool list
(`project-manager/references/atlassian-mcp-tools.md`) has no tools for user/group management, permission schemes,
field/workflow configuration, SSO, app management, or org settings. Never invent tool names — every workflow here runs
through `admin.atlassian.com` or the REST APIs cited inline. MCP contributes only read-mostly support:
`mcp__atlassian__lookupJiraAccountId` (resolve a user to `accountId`), `mcp__atlassian__searchJiraIssuesUsingJql` (find
a leaver's open issues), `mcp__atlassian__getVisibleJiraProjects` / `mcp__atlassian__getConfluenceSpaces` (inventory for
reviews), `mcp__atlassian__atlassianUserInfo` (verify acting identity).

**Least privilege** governs every grant: assign through groups, not individuals; give the minimum access the role needs;
revoke completely on departure. Read it as the default answer whenever a step asks what to grant.

## User provisioning

For the full role-based access templates, group naming standards, and the onboarding checklist, load
`references/user-provisioning-checklist.md` before granting access — it is the source of truth for which products,
groups, and roles each role gets.

1. Create the account: `admin.atlassian.com > User management > Invite users`, or REST `POST /rest/api/3/user` with
   `{"emailAddress", "displayName", "products"}`. **Done when** the account exists and its email domain matches a
   verified org domain.
2. Assign product access and add to groups per the role template in the checklist:
   `admin.atlassian.com > Products > [product] > Access` and `User management > Groups > [group] > Add members`. **Done
   when** every product and group the role template lists is assigned — none extra.
3. **Done overall when** the user appears active at `admin.atlassian.com/o/{orgId}/users`, logs in via SSO, has 2FA
   enrolled, and the requesting team lead is notified.

## User deprovisioning

Load `references/user-provisioning-checklist.md` (Offboarding Procedure) for the day-of / 24-hour / 7-day breakdown and
data-retention rules.

1. Resolve the user to an `accountId` (`mcp__atlassian__lookupJiraAccountId`), then inventory everything they own: open
   Jira issues (`GET /rest/api/3/search?jql=assignee={accountId}`), owned Confluence spaces/pages, filters, dashboards,
   automation rules, and API tokens. **Done when** each owned item is listed with a reassignment target.
2. Reassign every listed item: Jira project/component leads (`Project settings > People`), Confluence space ownership
   (`Space settings > Overview`), open issues (`Jira > Issues > Bulk change`), filters and dashboards
   (`User management > [user] > Managed content`). Hand off to the Jira Expert for bulk issue reassignment. **Done
   when** nothing from step 1 still lists the departing user as owner.
3. Revoke all group memberships, all API tokens, and all OAuth authorizations. **Done when** the user is in zero groups
   and holds zero active tokens.
4. Deactivate: `admin.atlassian.com > User management > [user] > Deactivate` or REST
   `DELETE /rest/api/3/user?accountId={accountId}`. **Done when** `GET /rest/api/3/user?accountId={accountId}` returns
   `"active": false` and the offboarding is recorded in the audit log.

## Group management

1. Create the group (`admin.atlassian.com > User management > Groups > Create group` or REST `POST /rest/api/3/group`)
   using the naming convention in `references/user-provisioning-checklist.md` (`dept-`, `team-`, `role-`, `project-`
   prefixes). **Done when** the name follows the convention and its purpose is documented in Confluence.
2. Assign the group's default permissions (least privilege) and add members. **Done when**
   `GET /rest/api/3/group/member?groupName={name}` returns exactly the intended members. Hand documentation to the
   Confluence Expert.

## Permission scheme design

Start from `assets/permission_scheme_template.json` — copy it, customize role assignments, and grant through the four
roles (projectAdmin, developer, user, viewer) it defines rather than ad-hoc grants. Before finalizing, run the scheme
against the audit heuristics in `references/security-hardening-guide.md` (Permission Scheme Audit Heuristics) — that
file owns the sensitive-permission list and the critical/high/medium flag conditions.

**Done when** the scheme grants only through groups, every sensitive permission is justified, and the heuristics surface
no critical or high findings.

## SSO and SCIM configuration

`references/security-hardening-guide.md` (Identity & Authentication) owns the SAML checklist, attribute mapping, and 2FA
enforcement policy — load it before configuring.

1. Configure SAML at `admin.atlassian.com > Security > SAML single sign-on` (Entity ID, ACS URL, IdP X.509 cert). **Done
   when** an admin test login and a regular-user test login both succeed with password login still active as fallback.
2. Enforce SSO (`Security > Authentication policies > Enforce SSO`) and enable SCIM
   (`User provisioning > [IdP] > Enable SCIM`). **Done when** the audit log shows `saml.login.success` events and SCIM
   sync creates a test account.

## Marketplace app management

`references/security-hardening-guide.md` (Third-Party App Security) owns the app review criteria and governance cadence.

1. Vet the app against those criteria (Marketplace certification, permission scope, vendor security docs), then install
   from `admin.atlassian.com > Products > [product] > Apps`. **Done when** the app is on the approved list with a
   documented owner and business justification.
2. Configure and verify. **Done when** the app appears in `GET /rest/plugins/1.0/` and its health check passes.

## Org security and governance

`references/security-hardening-guide.md` is the source of truth for the full hardening program — authentication,
session, IP allowlisting, API token, audit-log, data-residency, and compliance controls, plus the recurring hardening
schedule. Load it for any security-hardening or compliance task.

Inline essentials:

- **Admins**: limit org admins to 2-3 people; require MFA (`Security > Authentication policies > Require 2FA`); audit
  admin actions monthly. **Done when** the admin roster is 3 or fewer and all have MFA enforced.
- **Access reviews** (quarterly): export users (`admin.atlassian.com > User management > Export users`), have managers
  confirm each user's access, remove departed and stale (90-day no-login) accounts. **Done when** every active account
  maps to a current employee and the review completion is documented for compliance.
- **Audit logs**: enable org audit logging; export via `GET /admin/v1/orgs/{orgId}/audit-log`; retain per policy. **Done
  when** logging is enabled and export to the SIEM is confirmed.

## Change management

- **Major changes** (workflows, schemes, SSO): announce 2 weeks ahead, test in sandbox, prepare a rollback plan, execute
  off-peak. **Done when** the change is verified in production and a post-implementation review is recorded.
- **Minor changes**: announce 48 hours ahead and log the change. **Done when** logged and monitored for regressions.

## Handoff

- **Escalate to Atlassian Support**: org-wide outage or performance degradation, data loss/corruption, license/billing
  issues, complex migrations.
- **To Jira Expert**: project-specific configuration, new global workflows, custom fields, permission schemes.
- **To Confluence Expert**: space-specific settings, global templates, blueprints, macros.
- **To Senior PM**: usage analytics, capacity planning, cost and compliance status.
- **To Scrum Master**: team access provisioned, board and automation options.
- **Involve Security Team**: security incidents, unusual access patterns, compliance-audit prep, new-integration review.
