---
name: marketplace-performance-monitor
description: Track template marketplace KPIs, download trends, conversion rates, and competitive positioning with automated weekly reporting
category: Marketplaces
tools:
  - PostHog
  - n8n
  - Clay
  - Attio
fundamentals:
  - marketplace-analytics-scraping
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-workflow-basics
  - clay-claygent
  - attio-reporting
---

# Marketplace Performance Monitor

This drill builds the monitoring and reporting system for the template-tool-marketplaces play at Durable level. It tracks downloads, conversion rates, competitive positioning, and marketplace ecosystem changes across all template marketplaces -- then surfaces anomalies and optimization opportunities in a weekly report.

## Input

- Active template portfolio across multiple marketplaces (output from `marketplace-portfolio-scaling` drill)
- PostHog tracking configured for marketplace-sourced traffic (via UTM parameters)
- n8n instance for scheduled data collection
- At least 4 weeks of template performance data (Scalable baseline established)

## Steps

### 1. Configure comprehensive tracking events

Using `posthog-custom-events`, ensure the full template-to-revenue funnel is captured:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `marketplace_weekly_metrics` | n8n weekly data collection | `marketplace`, `template_slug`, `downloads`, `views`, `reviews`, `avg_rating` |
| `marketplace_visit` | UTM-tagged site visit from marketplace | `marketplace`, `template_slug`, `utm_campaign` |
| `marketplace_cta_click` | CTA click from marketplace-sourced session | `marketplace`, `template_slug`, `cta_location` |
| `marketplace_lead_captured` | Lead capture from marketplace-sourced session | `marketplace`, `template_slug`, `lead_type`, `email` |
| `marketplace_cross_promo_click` | Click on cross-promotion link inside a template | `source_template`, `target_template`, `marketplace` |

### 2. Build the data collection workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow that runs weekly (Monday 7am):

**Step 1 -- Pull marketplace analytics:**
For each marketplace, use `marketplace-analytics-scraping` to fetch:
- Downloads per template (last 7 days)
- Views per template (last 7 days, if available)
- New reviews/ratings (last 7 days)
- Current average rating
- Current marketplace ranking/position in category

**Step 2 -- Pull PostHog data:**
Query PostHog API for the same period:
- `marketplace_visit` count by marketplace and template
- `marketplace_lead_captured` count by marketplace and template
- Conversion rate: leads / visits per marketplace and template

**Step 3 -- Pull competitive data:**
Use Clay-based scraping (via `clay-claygent`) to monitor top 5 competing templates per marketplace:
- Their download count change
- Their rating change
- Any new competing templates published this week
- Their description/title changes (possible optimization signals)

**Claygent prompt:**
```
For the {marketplace_name} marketplace, category {category}:
1. Find the top 5 templates by downloads/popularity
2. For each: extract title, download count, rating, date last updated
3. Flag any template published in the last 7 days
4. Compare to last week's snapshot and note changes
Return as JSON array.
```

**Step 4 -- Store in PostHog:**
Send aggregated weekly metrics as `marketplace_weekly_metrics` events (one per template per marketplace).

**Step 5 -- Store in Attio:**
Update each template's campaign record with latest metrics using `attio-reporting`.

### 3. Build the PostHog dashboard

Using `posthog-dashboards`, create a "Template Marketplace Performance" dashboard:

**Panel 1 -- Portfolio Overview:**
- Trend: total downloads per week (stacked by marketplace)
- Trend: total site visits from templates per week
- Number: total leads captured this month from templates
- Number: portfolio-wide download-to-lead conversion rate

**Panel 2 -- Per-Template Performance:**
- Table: template_name, marketplace, downloads_this_week, visits, leads, conversion_rate
- Sorted by leads descending
- Color-code: green (improving), yellow (stable), red (declining)

**Panel 3 -- Conversion Funnel:**
- Funnel: marketplace_visit -> marketplace_cta_click -> marketplace_lead_captured
- Break down by marketplace

**Panel 4 -- Cross-Promotion Network:**
- Table: source_template, target_template, cross_promo_clicks
- Identify which cross-promotion links drive the most traffic

**Panel 5 -- Competitive Landscape:**
- Table: competitor_template, marketplace, their_downloads, their_rating, rank_vs_ours
- Highlight rows where a competitor overtook our template in ranking

### 4. Set up anomaly detection and alerts

Using `posthog-anomaly-detection` and n8n:

**Anomaly thresholds:**
- **Download drop:** >30% decline week-over-week on any template
- **Conversion drop:** Lead conversion rate drops >25% on any marketplace
- **Rating drop:** Average rating falls below 4.0 on any listing
- **New competitor:** A new template in our category appears with >100 downloads in its first week
- **Cross-promo failure:** Cross-promotion click-through drops below 1%

Route alerts to Slack with: the specific template, the metric, the change, and a recommended investigation action.

### 5. Generate weekly performance report

The n8n workflow generates:

```
# Template Marketplace Report -- Week of {date}

## Portfolio Summary
- Total downloads: {downloads} ({change}% vs last week)
- Total site visits from templates: {visits} ({change}% vs last week)
- Leads captured: {leads} ({change}% vs last week)
- Portfolio conversion rate: {rate}% (downloads -> leads)
- Active templates: {count} across {marketplace_count} marketplaces

## Top Performers
1. {template_1}: {downloads_1} downloads, {leads_1} leads, {rate_1}% conversion
2. {template_2}: {downloads_2} downloads, {leads_2} leads, {rate_2}% conversion

## Underperformers
- {template_x}: only {downloads_x} downloads (below portfolio average of {avg})
  Recommendation: {specific action}

## Competitive Intelligence
- {notable changes in competing templates}

## Optimization Opportunities
- {data-driven recommendations for next experiments}
```

Post to Slack and store in Attio.

## Output

- Weekly automated data collection from all marketplaces and templates
- Real-time PostHog dashboard with portfolio-level and per-template KPIs
- Automated anomaly detection alerts
- Weekly performance report with competitive intelligence
- Historical trend data feeding the autonomous optimization loop

## Triggers

- Data collection: weekly via n8n cron (Monday 7am)
- Anomaly alerts: continuous (checked during weekly collection; real-time for PostHog-tracked metrics)
- Dashboard: always-on, refreshes with live data
- Competitive scans: weekly
