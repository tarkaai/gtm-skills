---
name: org-chart-research
description: Research and reconstruct a target company's org chart using Clay, LinkedIn, and Apollo
tool: Clay
product: Clay
difficulty: Config
---

# Org Chart Research

Research and reconstruct the reporting structure and key personnel at a target account. Produces a structured map of who reports to whom, team sizes, and role classifications relevant to your buying process.

## Prerequisites

- Clay account with credits (Claygent + People Search)
- Target company identified with domain or LinkedIn company URL
- Buyer personas defined (titles/roles you care about)
- Optional: LinkedIn Sales Navigator for deeper org browsing

## Steps

### 1. Seed the company in Clay

Create a Clay table row for the target company. Add columns for `company_name`, `domain`, `linkedin_company_url`, `employee_count`, and `industry`. Use `clay-company-search` if you need to find the company first.

### 2. Find people at the company

Add a "Find People at Company" enrichment column using `clay-people-search`. Configure filters:
- **Seniority**: Director, VP, C-Suite, Founder
- **Departments**: Engineering, Product, Operations, Finance, IT, Procurement
- **Limit**: 20-30 people per company (covers the buying committee without credit waste)

Expand rows so each person gets their own row.

### 3. Enrich each person

For each person found, add enrichment columns:
- **Title** (from LinkedIn or People Data Labs)
- **Department** (parsed from title)
- **Seniority level** (C-Suite, VP, Director, Manager, IC)
- **LinkedIn URL** (for manual verification)
- **Email** (via `clay-enrichment-waterfall`)
- **Tenure at company** (from LinkedIn start date)
- **Reports to** (use Claygent: "Who does {Name} at {Company} report to based on LinkedIn?")

### 4. Use Claygent to infer reporting lines

Add a Claygent column with prompt:
```
Based on LinkedIn profiles and public information, who does {Full Name}, {Title} at {Company Name} report to? Return the name and title of their likely manager. If you cannot determine this, return "Unknown".
```

Run on Director-level and below. VP and C-Suite reporting lines are usually obvious from titles.

### 5. Map the hierarchy

Export the enriched table. Structure the output as a nested hierarchy:
```
CEO
  |- CTO
  |    |- VP Engineering
  |    |    |- Director of Platform
  |    |    |- Director of Frontend
  |    |- VP Product
  |- CFO
  |    |- VP Finance
  |- CRO
       |- VP Sales
       |- VP Customer Success
```

### 6. Identify gaps

Flag departments or levels with missing data. Common gaps: middle management (Directors), cross-functional roles (Chief of Staff, Business Operations), and newly created roles. These gaps may hide stakeholders who influence buying decisions.

## Via Apollo

Apollo provides org chart data for some companies:
1. Search for the company in Apollo
2. Navigate to the company profile > People tab
3. Filter by department and seniority
4. Export contacts with titles and departments
5. Apollo does not provide reporting-line data — use Clay for that

## Via LinkedIn Sales Navigator

1. Search: `Current company: {Company} AND Seniority: Director+`
2. Browse results and note titles/departments
3. Use TeamLink to see if anyone in your network knows them
4. Save leads to a Sales Navigator list for later outreach

## Tool Alternatives

| Tool | Org Chart Capability | Notes |
|------|---------------------|-------|
| Clay | People Search + Claygent inference | Best for automated research at scale |
| Apollo | People tab on company profiles | Good contact data, no reporting lines |
| LinkedIn Sales Navigator | Advanced people search | Manual but deepest data |
| ZoomInfo | Org chart feature | Enterprise-grade, expensive |
| Cognism | People search | Strong in EU/UK markets |

## Error Handling

- **Claygent returning "Unknown" for most entries**: Company may be too small or private. Fall back to LinkedIn manual research.
- **Stale data**: People change roles frequently. Filter for people with tenure > 3 months to avoid recently departed contacts.
- **Credit burn**: Claygent uses 5-10 credits per query. Budget 10-15 credits per company for full org chart research. Run on high-priority accounts only.
- **Duplicate people across providers**: Deduplicate by LinkedIn URL (most reliable unique identifier).
