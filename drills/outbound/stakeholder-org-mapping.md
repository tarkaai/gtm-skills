---
name: stakeholder-org-mapping
description: Scale org chart mapping across all active deals with auto-population and relationship tracking
category: Prospecting
tools:
  - Clay
  - Attio
  - n8n
  - Apollo
fundamentals:
  - org-chart-research
  - clay-people-search
  - clay-claygent
  - clay-enrichment-waterfall
  - attio-lists
  - attio-custom-attributes
  - n8n-workflow-basics
  - n8n-scheduling
---

# Stakeholder Org Mapping at Scale

This drill scales stakeholder identification to all active deals simultaneously. Instead of researching one account at a time, it maintains a continuously updated Clay table of target companies and their people, with automated refreshes that catch new hires, departures, and role changes.

## Input

- All active deals in Attio at Connected stage or later
- Clay account with sufficient credits (budget ~15 credits per company per refresh)
- n8n scheduling configured
- Apollo account for supplementary contact data

## Steps

### 1. Build the master company table in Clay

Using `clay-people-search` and `clay-enrichment-waterfall`, create a persistent Clay table called "Stakeholder Mapping — Active Accounts". Pull all companies with active deals from Attio via the Clay-Attio integration. Columns: company name, domain, deal stage, deal value, current stakeholder count, last enrichment date.

### 2. Configure automated people discovery

For each company in the table, set up a recurring "Find People at Company" enrichment:
- **Filters**: Director+ seniority, relevant departments
- **Schedule**: Weekly refresh via `n8n-scheduling` (Mondays at 6 AM)
- **Delta detection**: Compare new results against existing contacts in Attio. Flag new people (recent hires) and missing people (possible departures)

### 3. Track relationship dynamics

Using `clay-claygent`, add inference columns:
- "Who does {Name} report to?" — Maps reporting lines
- "Has {Name} changed roles at {Company} in the last 90 days?" — Catches internal promotions
- "Does {Name} have any public connection to {Your Company Name}?" — Identifies warm intro paths

### 4. Auto-populate new stakeholders

Build an n8n workflow using `n8n-workflow-basics` that:
1. Reads the delta from Clay (new people found this week)
2. Runs role classification on new contacts
3. Creates Person records in Attio with role tags
4. Links new people to the existing deal
5. Alerts the deal owner via Slack: "3 new stakeholders discovered at {Company}: {Name/Title list}"

### 5. Build stakeholder coverage views in Attio

Using `attio-lists`, create filtered views:
- **Under-mapped deals**: Deals with fewer than 3 classified stakeholders
- **Missing Economic Buyer**: Deals where no contact is tagged as Economic Buyer
- **Single-threaded**: Deals with only 1-2 contacts at engagement level Active or Warm
- **Stale maps**: Deals where `stakeholder_map_date` is older than 30 days

These views drive the weekly deal review — which accounts need attention.

### 6. Predict stakeholder roles from title patterns

Analyze historical data across all deals to build title-to-role mapping rules. Using `attio-custom-attributes`, store the model:
- Titles containing "Procurement" → Blocker (92% accuracy across 50 deals)
- Titles containing "VP Engineering" → Influencer (85% accuracy)
- Titles containing "CEO" at companies < 50 employees → Economic Buyer (95% accuracy)

Apply these rules as a first pass before running AI classification, saving API costs.

### 7. Generate weekly stakeholder coverage report

Schedule a weekly n8n workflow that:
1. Counts total stakeholders mapped per deal
2. Calculates multi-threading rate (% of deals with 3+ engaged stakeholders)
3. Lists deals with new risks (Champion left, Blocker appeared)
4. Sends the report to the team channel

## Output

- Continuously updated stakeholder maps across all active deals
- Automated detection of org changes (new hires, departures, promotions)
- Coverage views that highlight which deals need more multi-threading
- Weekly stakeholder health report

## Triggers

- Weekly automated refresh of all active account org charts
- On-demand refresh when a deal enters a new stage
- Alert-triggered refresh when a key stakeholder's LinkedIn profile changes
