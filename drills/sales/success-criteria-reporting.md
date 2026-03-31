---
name: success-criteria-reporting
description: Build dashboards and automated reports tracking success criteria definition rates, achievement rates, and correlation with deal outcomes
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - attio-deals
  - n8n-workflow-basics
  - n8n-scheduling
---

# Success Criteria Reporting

This drill builds the reporting layer for the success criteria program. It creates dashboards, automated reports, and data feeds that track how well success criteria are being defined, whether they predict deal outcomes, and how the program evolves over time. At Durable level, this reporting layer feeds the autonomous optimization loop.

## Input

- PostHog events from the success criteria program (`success_criteria_defined`, `mutual_success_plan_created`, `criteria_recommendation_generated`, etc.)
- Attio deal records with success criteria custom attributes
- n8n instance for scheduled report generation

## Steps

### 1. Build the PostHog Success Criteria Dashboard

Using `posthog-dashboards`, create a dashboard named "Success Criteria Program" with 6 panels:

**Panel 1 — Definition Rate (line chart, weekly)**
- Query: count of `success_criteria_defined` events per week / count of deals entering Connected stage per week
- Target line: the current level's threshold (e.g., 80% at Baseline)

**Panel 2 — Criteria Quality Distribution (bar chart)**
- Query: distribution of `avg_achievability_score` across all deals with defined criteria
- Buckets: 0-30 (risky), 31-60 (moderate), 61-80 (good), 81-100 (strong)

**Panel 3 — Close Rate Comparison (bar chart)**
- Query: close rate for deals WITH defined success criteria vs deals WITHOUT
- Break down by: criteria count (1-2, 3-4, 5+)

**Panel 4 — Achievement Rate (line chart, monthly)**
- Query: % of criteria that were achieved post-sale, tracked monthly
- Break down by category (efficiency, revenue, cost_savings, quality, time_to_value, adoption)

**Panel 5 — Deal Velocity Comparison (bar chart)**
- Query: average days from Connected to Won for deals WITH criteria vs WITHOUT
- Shows whether success criteria definition accelerates or slows the sales cycle

**Panel 6 — Stakeholder Alignment (pie chart)**
- Query: distribution of `mutual_success_plan_created` events by stakeholder count
- Shows how many stakeholders are involved in success criteria definition

### 2. Build Attio Saved Views

Create 3 saved views in Attio using `attio-reporting`:

**View 1 — "Deals Missing Success Criteria"**
- Filter: deal stage = Connected or Qualified, `success_criteria_status` is empty or null
- Sort: deal value descending
- Purpose: identify high-value deals that need criteria defined

**View 2 — "At-Risk Criteria"**
- Filter: `success_criteria_status` = "defined", any criterion with `achievability_score < 50`
- Sort: achievability score ascending
- Purpose: flag deals where overpromising may cause post-sale disappointment

**View 3 — "Success Criteria Funnel"**
- Filter: all deals from the last 90 days
- Group by: `success_criteria_status` (none, draft, defined, achieved, missed)
- Purpose: track the full lifecycle of success criteria from definition through achievement

### 3. Set Up Automated Weekly Digest

Using `n8n-scheduling`, create a weekly workflow that runs every Monday at 9 AM:

1. Query PostHog for last week's metrics: definition rate, average achievability score, criteria count
2. Query Attio for: deals missing criteria, new mutual success plans created, criteria outcomes recorded
3. Generate a digest:
   ```
   ## Success Criteria Weekly Digest — Week of {date}

   **Definition Rate:** {X}% ({Y} deals defined / {Z} deals at Connected+)
   **Average Achievability Score:** {score}/100
   **New Mutual Plans Created:** {count}

   ### Attention Required
   - {count} deals at Connected+ without criteria defined (top 3 by value: ...)
   - {count} criteria with achievability < 50 (deals: ...)

   ### Outcomes Tracked This Week
   - {count} criteria marked as achieved
   - {count} criteria marked as missed
   - Current achievement rate: {X}%
   ```
4. Post the digest to Slack
5. Store in Attio as a note tagged `weekly-criteria-digest`

### 4. Set Up Monthly ROI Report

Using `n8n-scheduling`, create a monthly workflow:

1. Calculate the close rate delta: deals with defined criteria vs without (last 90 days)
2. Calculate the retention delta: customers where criteria were achieved vs not (if data available)
3. Calculate deal velocity impact: average days to close with criteria vs without
4. Estimate revenue impact: `(close_rate_delta * average_deal_value * deal_volume)`
5. Store as Attio note tagged `monthly-criteria-roi`

### 5. Feed the Optimization Loop (Durable Only)

At Durable level, configure the reporting outputs to feed the `autonomous-optimization` drill:

- Export the weekly metrics as a PostHog API endpoint the optimization loop queries
- Set anomaly thresholds: definition rate drops >20% from 4-week average, achievability calibration drifts >15%, achievement rate drops below 60%
- When anomaly thresholds are breached, the reporting layer fires a PostHog event `criteria_anomaly_detected` which triggers the optimization loop's Phase 2 (Diagnose)

## Output

- PostHog dashboard with 6 panels tracking the success criteria program
- 3 Attio saved views for daily CRM workflow
- Weekly digest posted to Slack
- Monthly ROI report stored in Attio
- Data feed for the autonomous optimization loop (Durable level)

## Triggers

- **Weekly (Monday 9 AM):** Weekly digest
- **Monthly (1st of month):** ROI report
- **Continuous:** Dashboard auto-refreshes in PostHog
- **On anomaly:** Fires event to trigger optimization loop
