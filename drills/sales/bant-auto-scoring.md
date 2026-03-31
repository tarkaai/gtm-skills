---
name: bant-auto-scoring
description: Automated pre-qualification scoring pipeline that enriches and BANT-scores new leads before human contact
category: Sales
tools:
  - Clay
  - Attio
  - n8n
  - PostHog
fundamentals:
  - clay-bant-enrichment
  - clay-scoring
  - clay-table-setup
  - attio-custom-attributes
  - attio-deals
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# BANT Auto-Scoring Pipeline

This drill builds an automated pipeline that takes raw leads and produces BANT pre-qualification scores without any human involvement. New leads enter via CRM webhook, get enriched in Clay, scored across all four BANT dimensions, and routed back to CRM with scores and a qualification tier.

## Input

- New lead enters Attio (via form submission, import, or outbound list)
- Clay table configured with BANT enrichment columns (from `clay-bant-enrichment` fundamental)
- n8n instance for orchestration

## Steps

### 1. Set up the trigger workflow in n8n

Using the `n8n-triggers` fundamental, create a workflow triggered by new deal creation in Attio:

- **Trigger:** Attio webhook — fires when a new deal record is created
- **Filter:** Only process deals where `bant_composite_score` is empty (avoids re-processing already-scored deals)

### 2. Push the lead to Clay for enrichment

When a new deal triggers the workflow:

1. Extract the company name, contact email, and LinkedIn URL from the Attio record
2. Use the `clay-table-setup` fundamental to add the row to your BANT enrichment table in Clay
3. Trigger Clay's enrichment columns (they run automatically on new rows)
4. Wait for enrichment to complete (poll Clay API every 30 seconds for up to 5 minutes)

### 3. Compute BANT pre-scores in Clay

After enrichment completes, Clay's formula columns calculate per-dimension scores:

- **Budget signal score (0-100):** Based on funding, revenue, tech spend, and headcount growth signals
- **Authority signal score (0-100):** Based on title seniority, department match, org chart depth, and LinkedIn activity
- **Need signal score (0-100):** Based on job postings, tech stack gaps, competitor reviews, and news mentions
- **Timeline signal score (0-100):** Based on funding recency, leadership changes, fiscal year timing, and contract renewal windows

Composite: `(budget * 0.25) + (authority * 0.25) + (need * 0.30) + (timeline * 0.20)`

See `clay-bant-enrichment` fundamental for the detailed formula logic.

### 4. Push scores back to Attio

Using the `attio-deals` fundamental, update the deal record with:
- `bant_budget_score`, `bant_authority_score`, `bant_need_score`, `bant_timeline_score`
- `bant_composite_score`
- `bant_verdict` — Qualified / Needs Work / Disqualified based on thresholds
- `bant_assessment_source` = "Pre-call Enrichment"
- `bant_last_assessed` = today's date

### 5. Route the deal based on pre-score

In the same n8n workflow, add routing logic:

- **Composite >= 70 (Qualified):** Move deal to "BANT Pre-Scored" stage. Trigger a Slack notification to the founder: "New qualified lead: {company} — BANT score {score}. Book discovery call."
- **Composite 40-69 (Needs Work):** Move to "BANT Pre-Scored" stage. Add a note listing which dimensions are weak and what to probe in discovery.
- **Composite < 40 (Disqualified):** Move to "BANT Disqualified." Add to a nurture sequence. No outbound sales effort.

### 6. Log to PostHog

Using `posthog-custom-events`, fire a `bant_auto_score_completed` event with properties:
- `deal_id`, `company_name`, `composite_score`, `verdict`
- `budget_score`, `authority_score`, `need_score`, `timeline_score`
- `enrichment_hit_rate` (% of enrichment columns that returned data)

This feeds your qualification funnel analytics.

### 7. Handle enrichment failures

If Clay enrichment fails or returns sparse data (< 50% of columns populated):
- Set `bant_verdict` = "Needs Work" regardless of score (insufficient data to judge)
- Add an Attio note: "Auto-scoring incomplete — enrichment coverage {X}%. Manual research recommended."
- Flag in Slack for manual review

## Output

- Every new deal in Attio gets automatic BANT pre-scores within minutes
- Deals are routed to the correct pipeline stage without manual intervention
- Founder receives Slack alerts for high-scoring leads
- PostHog tracks the full auto-scoring funnel for analysis

## Triggers

Runs automatically on every new deal creation via n8n webhook. No manual intervention needed. Monitor n8n execution logs weekly for errors.
