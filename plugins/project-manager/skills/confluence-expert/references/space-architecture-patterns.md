# Confluence Space Architecture Patterns

## Overview

Well-organized Confluence spaces dramatically improve information discoverability and team productivity. This guide
covers proven space organization patterns, page hierarchy best practices, and governance strategies.

## Space Organization Patterns

### Pattern 1: By Team

Each team or department gets its own space.

**Structure:**

```text
Engineering Space (ENG)
Product Space (PROD)
Marketing Space (MKT)
Design Space (DES)
Support Space (SUP)
```

**Pros:**

- Clear ownership and permissions
- Teams control their own content
- Natural permission boundaries
- Easy to find team-specific content

**Cons:**

- Cross-team content duplication
- Silos between departments
- Hard to find project-spanning information
- Inconsistent practices across spaces

**Best for:** Organizations with stable teams and clear departmental boundaries

### Pattern 2: By Project

Each major project or product gets its own space.

**Structure:**

```text
Project Alpha Space (ALPHA)
Project Beta Space (BETA)
Platform Infrastructure Space (PLAT)
Internal Tools Space (TOOLS)
```

**Pros:**

- All project context in one place
- Easy onboarding for project members
- Clean archival when project completes
- Natural lifecycle management

**Cons:**

- Team knowledge scattered across spaces
- Permission management per project
- Space proliferation over time
- Ongoing vs project work separation unclear

**Best for:** Project-based organizations, agencies, consulting firms

### Pattern 3: By Domain (Hybrid)

Combine functional spaces with cross-cutting project spaces.

**Structure:**

```text
Company Wiki (WIKI) - Shared knowledge
Engineering Standards (ENG) - Team practices
Product Specs (PROD) - Requirements and roadmap
Project Alpha (ALPHA) - Cross-team project
Project Beta (BETA) - Cross-team project
Archive (ARCH) - Completed projects
```

**Pros:**

- Balances team and project needs
- Shared knowledge has a home
- Clear archival path
- Scales with organization growth

**Cons:**

- More complex to set up initially
- Requires governance to maintain
- Some ambiguity about where content belongs

**Best for:** Growing organizations, 50-500 people, multiple concurrent projects

## Page Hierarchy Best Practices

### Recommended Depth

- **Maximum 4 levels deep** - Deeper hierarchies become hard to navigate
- **3 levels ideal** for most content types
- Use flat structures with labels for categorization beyond 4 levels

### Standard Page Hierarchy

```text
Space Home (overview, quick links, recent updates)
├── Getting Started
│   ├── Onboarding Guide
│   ├── Tool Setup
│   └── Key Contacts
├── Projects
│   ├── Project Alpha
│   │   ├── Requirements
│   │   ├── Design
│   │   └── Meeting Notes
│   └── Project Beta
├── Processes
│   ├── Development Workflow
│   ├── Release Process
│   └── On-Call Runbook
├── References
│   ├── Architecture Decisions
│   ├── API Documentation
│   └── Glossary
└── Archive
    ├── 2025 Projects
    └── Deprecated Processes
```

### Page Naming Conventions

- Use clear, descriptive titles (not abbreviations)
- Include date for time-sensitive content: "2025-Q1 Planning"
- Prefix meeting notes with date: "2025-03-15 Sprint Review"
- Use consistent casing (Title Case or Sentence case, not both)
- Avoid special characters that break URLs

### Space Homepage Design

Every space homepage should include:

1. **Space purpose** - One paragraph describing what this space is for
2. **Quick links** - 5-7 most accessed pages
3. **Recent updates** - Recently Updated macro filtered to this space
4. **Getting started** - Link to onboarding content for new members
5. **Contact info** - Space owner, key contributors

## Labeling Taxonomy

### Label Categories

- **Content type:** `meeting-notes`, `decision`, `specification`, `runbook`, `retrospective`
- **Status:** `draft`, `in-review`, `approved`, `deprecated`, `archived`
- **Team:** `team-engineering`, `team-product`, `team-design`
- **Project:** `project-alpha`, `project-beta`
- **Priority:** `high-priority`, `p1`, `critical`

### Labeling Best Practices

- Use lowercase, hyphenated labels (no spaces or camelCase)
- Define a standard label vocabulary and document it
- Use labels for cross-space categorization
- Combine labels with CQL for powerful search and reporting
- Audit labels quarterly to remove unused or inconsistent labels
- Limit to 3-5 labels per page (over-labeling reduces value)

### CQL Examples for Label-Based Queries

```text
# All meeting notes in a space
type = page AND space = "ENG" AND label = "meeting-notes"

# All approved specifications
type = page AND label = "specification" AND label = "approved"

# Recent decisions across all spaces
type = page AND label = "decision" AND lastModified > now("-30d")
```

## Cross-Space Linking

### When to Link vs Duplicate

- **Link** when content has a single source of truth
- **Duplicate** (Include Page macro) when content must appear in multiple contexts
- **Excerpt Include** when only a portion of a page is needed elsewhere

### Linking Best Practices

- Use full page titles in links for clarity
- Add context around links ("See the [Architecture Decision Record] for rationale")
- Avoid orphan pages - every page should be reachable from space navigation
- Use the Recently Updated macro on hub pages for activity visibility
- Create "Related Pages" sections at the bottom of content pages

## Content Governance

### Review Cycles

- Critical docs: monthly
- Standard docs: quarterly
- Archive docs: annually

### Page Quality Standards

Every published page should have: a clear descriptive title; an identified owner/author; a visible last-updated date;
structure via headings; appropriate labels (3-5); functional links; consistent formatting; no exposed sensitive data.

## Archive Strategy

### When to Archive

- Project completed more than 90 days ago
- Process or document officially deprecated
- Content not updated in 12+ months
- Replaced by newer content

### Archive Process

1. Add `archived` label to the page
2. Move to Archive section within the space (or dedicated Archive space)
3. Add a note at the top: "This page is archived as of [date]. See [replacement] for current information."
4. Update any incoming links to point to current content
5. Do NOT delete - archived content has historical value

### Archive Space Pattern

- Create a dedicated `Archive` space for completed projects
- Move entire project page trees to Archive space on completion
- Set Archive space to read-only permissions
- Review Archive space annually for content that can be deleted

## Team-Type Section Conventions

When scaffolding a new space, start from a base section set and add the sections that match the team's type. Emit one
page per node; nest children under their parent's page id.

### Base sections (every space)

- **Home** — landing page with quick links and team overview (labels: `home`, `landing`)
- **Getting Started** — onboarding for new members (labels: `onboarding`, `getting-started`); children: Team Charter,
  Tools & Access, Communication Guidelines, Key Contacts
- **Meeting Notes** — recurring and ad-hoc meeting docs (label: `meetings`); children: Weekly Standups, Team Syncs,
  Ad-hoc Meetings
- **Templates** — reusable page templates (label: `templates`)
- **Archive** — archived and deprecated content (label: `archive`)

### Type-specific sections

- **Engineering** — Architecture (ADRs, System Design, API Docs, Tech Stack), Development (Coding Standards, Git
  Workflow, CI/CD, Environment Setup), Runbooks (Incident Response, Deployment, Troubleshooting)
- **Product** — Strategy (Vision, Roadmap, OKRs, Competitive Analysis), Research (Personas, Interview Notes, Surveys,
  Usability Testing), Requirements (Feature Specs, User Stories, Acceptance Criteria)
- **Marketing** — Strategy (Brand Guidelines, Marketing Plan, Target Audiences, Channels), Campaigns (Active, Results,
  Templates), Content (Calendar, Assets, Style Guide)
- **Project** — Project Overview (Charter, Scope & Deliverables, Stakeholder Map, Timeline & Milestones), Status &
  Reporting (Weekly Status, Risk Register, Decision Log), Resources (Technical Docs, Vendor Info, Budget & Financials)

If the team also lists named projects, add a **Projects** section with one child per project, each holding Overview /
Requirements / Status pages.

### Space key and sizing

- **Space key**: single-word name → first 10 characters uppercased; multi-word → the initials of the first five words.
- **≤ 3 people**: merge low-traffic sections to simplify the tree.
- **> 10 people**: consider restricted sections or sub-spaces per sub-team.
- **> 5 projects listed**: consider a separate space per project for isolation.

### Permission role tiers by team type

- **Engineering** — admins: team leads, eng managers; contributors: developers, QA; viewers: product, stakeholders.
  Restrict Runbooks to engineering; give product view-only on Architecture.
- **Product** — admins: PMs, product leads; contributors: designers, analysts; viewers: engineering, marketing,
  stakeholders. Restrict raw Research data to product; share Strategy with leadership.
- **Marketing** — admins: marketing managers/leads; contributors: content creators, designers; viewers: sales, product.
  Restrict campaign budgets to leadership; share brand guidelines broadly.
- **Project** — admins: PMs; contributors: project team; viewers: stakeholders, sponsors. Restrict Budget & Financials
  to PMs and sponsors; share status reports with all stakeholders.

## Content Health Audit

Score a space against these dimensions before any restructure or governance review. Export the page inventory via
`mcp__atlassian__getPagesInConfluenceSpace` / `mcp__atlassian__searchConfluenceUsingCql` (title, last modified, view
count, author, labels, word count), then judge every page against each dimension.

| Dimension        | Weight | Flag when                                                                 |
| ---------------- | ------ | ------------------------------------------------------------------------- |
| **Freshness**    | 30%    | stale: not updated in 90-180 days; outdated: not updated in > 180 days    |
| **Engagement**   | 25%    | fewer than 5 views                                                        |
| **Organization** | 20%    | orphaned: no labels applied                                               |
| **Size balance** | 15%    | oversized: > 5000 words (split); undersized: < 50 words (expand or merge) |
| **Completeness** | 10%    | missing any of title, last-modified date, author                          |

Ideal page length is 200-3000 words. Turn the flagged pages into two lists: an **archive list**
(stale/outdated/orphaned/low-engagement → label `archived` + move per the Archive Process) and an **update backlog**
(oversized to split, incomplete metadata to fill, undersized to expand) worked against the quality standards below.
Prioritize outdated pages first, then stale and orphaned, then size and completeness fixes.

## Permission Inheritance Patterns

### Pattern 1: Open by Default

- All spaces readable by all employees
- Edit restricted to space members
- Admin restricted to space owners
- **Best for:** Transparency-focused organizations

### Pattern 2: Restricted by Default

- Spaces accessible only to specific groups
- Request access via space admin
- **Best for:** Regulated industries, confidential projects

### Pattern 3: Tiered Access

- Public tier: Company wiki, shared processes
- Team tier: Team-specific spaces with team access
- Restricted tier: HR, finance, legal with limited access
- **Best for:** Most organizations (balanced approach)

### Permission Tips

- Use Confluence groups, not individual users, for permissions
- Align groups with LDAP/SSO groups where possible
- Audit permissions quarterly
- Document permission model on the space homepage
- Use page-level restrictions sparingly (breaks inheritance, hard to audit)

## Scaling Considerations

### < 50 People

- 3-5 spaces total
- Simple by-team pattern
- Light governance

### 50-200 People

- 10-20 spaces
- Hybrid pattern (team + project)
- Formal labeling taxonomy
- Quarterly content reviews

### 200+ People

- 20-50+ spaces
- Full domain pattern with governance
- Space owners and content stewards
- Automated archival policies
- Regular information architecture reviews
