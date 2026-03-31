---
name: partner-marketplace-monitor
description: Track partner marketplace KPIs, install trends, conversion rates, review velocity, and competitive positioning with automated weekly reporting
category: Partner Marketplaces
tools:
  - PostHog
  - n8n
  - Clay
  - Attio
fundamentals:
  - partner-marketplace-analytics-api
  - partner-marketplace-review-api
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-workflow-basics
  - clay-claygent
  - attio-reporting
---

# Partner Marketplace Monitor

This drill builds the monitoring and reporting system for partner marketplace listings at Durable level. It tracks installs, conversion rates, review velocity, competitive positioning, and marketplace ecosystem changes -- then surfaces anomalies and optimization opportunities in a weekly report. This data feeds the `autonomous-optimization` drill's detect-diagnose-experiment-evaluate loop.

## Input

- Active partner marketplace listings across 5+ marketplaces (output from `partner-marketplace-scaling` drill)
- PostHog tracking configured for marketplace-sourced traffic
- n8n instance for scheduled data collection
- At least 4 weeks of marketplace performance data (Scalable baseline established)

## Steps

### 1. Configure comprehensive tracking events

Using `posthog-custom-events`, ensure the full marketplace-to-revenue funnel is captured:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `partner_marketplace_weekly_metrics` | n8n weekly data collection | `marketplace`, `listing_slug`, `page_views`, `installs`, `uninstalls`, `active_installs`, `reviews_count`, `avg_rating`, `category_rank` |
| `partner_marketplace_visit` | UTM-tagged site visit from marketplace | `marketplace`, `listing_slug`, `utm_campaign`, `landing_page` |
| `partner_marketplace_signup` | Trial start from marketplace-sourced session | `marketplace`, `listing_slug`, `signup_type`, `plan` |
| `partner_marketplace_activation` | Integration connected from marketplace-sourced user | `marketplace`, `listing_slug`, `integration_type`, `time_to_connect` |
| `partner_marketplace_conversion` | Paid conversion from marketplace-sourced user | `marketplace`, `listing_slug`, `plan`, `mrr` |
| `partner_marketplace_review_posted` | New review detected via API | `marketplace`, `listing_slug`, `rating`, `word_count`, `is_solicited` |

### 2. Build the weekly data collection workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow that runs weekly (Monday 7am):

**Step 1 -- Pull marketplace analytics:**
For each marketplace, use `partner-marketplace-analytics-api` to fetch:
- Page views / search impressions (last 7 days)
- New installs (last 7 days)
- Uninstalls (last 7 days)
- Active install count (current)
- Review count and average rating (current)
- Category rank / position (current)

**Step 2 -- Pull PostHog data:**
Query PostHog API for the same period:
- `partner_marketplace_visit` count by marketplace
- `partner_marketplace_signup` count by marketplace
- `partner_marketplace_activation` count by marketplace
- `partner_marketplace_conversion` count by marketplace and MRR sum
- Conversion rates at each funnel stage

**Step 3 -- Pull competitive intelligence:**
Use Clay with `clay-claygent` to monitor the top 5 competing apps per marketplace:

**Claygent prompt:**
```
For the {marketplace_name} app marketplace, in our category:
1. List the top 5 apps by install count or ranking
2. For each: extract name, install count (or user count), rating, review count, last updated date
3. Flag any new app published in the last 7 days
4. Note any changes to top competitor listings (description updates, new screenshots, pricing changes)
Return as JSON array.
```

**Step 4 -- Store in PostHog:**
Send aggregated weekly metrics as `partner_marketplace_weekly_metrics` events (one per marketplace).

**Step 5 -- Store in Attio:**
Update each marketplace campaign record with latest metrics using `attio-reporting`.

### 3. Build the PostHog dashboard

Using `posthog-dashboards`, create a "Partner Marketplace Performance" dashboard:

**Panel 1 -- Portfolio Overview:**
- Trend: total installs per week (stacked by marketplace)
- Trend: total signups from marketplace sources per week
- Number: total MRR attributed to marketplace-sourced users this month
- Number: portfolio-wide install-to-paid conversion rate

**Panel 2 -- Per-Marketplace Performance:**
- Table: marketplace, installs_this_week, signups, activations, paid_conversions, conversion_rate, avg_rating, category_rank
- Sorted by paid conversions descending
- Color-code: green (improving), yellow (stable), red (declining)

**Panel 3 -- Full Conversion Funnel:**
- Funnel: partner_marketplace_visit -> partner_marketplace_signup -> partner_marketplace_activation -> partner_marketplace_conversion
- Break down by marketplace

**Panel 4 -- Review Health:**
- Trend: new reviews per week by marketplace
- Current average rating per marketplace
- Table: recent reviews with rating, marketplace, and response status

**Panel 5 -- Competitive Landscape:**
- Table: competitor_app, marketplace, their_installs, their_rating, their_review_count, rank_vs_ours
- Highlight rows where a competitor overtook our listing in ranking

### 4. Configure anomaly detection and alerts

Using `posthog-anomaly-detection` and n8n:

**Anomaly thresholds:**
- **Install drop:** >30% decline week-over-week on any marketplace
- **Conversion drop:** Signup-to-paid conversion rate drops >25% on any marketplace
- **Rating drop:** Average rating falls below 4.0 on any listing
- **Rank drop:** Category rank falls by 3+ positions on any marketplace
- **Uninstall spike:** Uninstalls exceed 20% of active installs in a week
- **New competitor:** A new app in our category appears with significant traction in its first week
- **Review drought:** No new reviews on any marketplace for 3+ weeks

Route alerts to Slack with: the specific marketplace, the metric, the change magnitude, and a recommended investigation action.

### 5. Generate weekly performance report

The n8n workflow generates a structured report:

```
# Partner Marketplace Report -- Week of {date}

## Portfolio Summary
- Total installs this week: {installs} ({change}% vs last week)
- Marketplace-sourced signups: {signups} ({change}% vs last week)
- Marketplace-sourced paid conversions: {conversions} ({change}% vs last week)
- MRR from marketplace channel: ${mrr} ({change}% vs last month)
- Active listings: {count} across {marketplace_count} marketplaces

## Per-Marketplace Breakdown
| Marketplace | Installs | Signups | Paid | Conv. Rate | Rating | Rank |
|------------|----------|---------|------|-----------|--------|------|
{table rows}

## Top Performers
1. {marketplace_1}: {installs_1} installs, {conversions_1} paid conversions, {rate_1}% conversion
2. {marketplace_2}: ...

## Needs Attention
- {marketplace_x}: {specific issue and data}
  Recommendation: {specific action}

## Review Health
- New reviews this week: {count} (target: {target})
- Pending responses: {count}
- Lowest-rated marketplace: {marketplace} at {rating}

## Competitive Intelligence
- {notable changes in competing apps}

## Optimization Opportunities
- {data-driven recommendations feeding the autonomous optimization loop}
```

Post to Slack and store in Attio.

## Output

- Weekly automated data collection from all partner marketplace listings
- Real-time PostHog dashboard with portfolio and per-marketplace KPIs
- Automated anomaly detection alerts
- Weekly performance report with competitive intelligence
- Historical trend data feeding the `autonomous-optimization` drill

## Triggers

- Data collection: weekly via n8n cron (Monday 7am)
- Anomaly alerts: checked during weekly collection + real-time for PostHog-tracked events
- Dashboard: always-on, refreshes with live data
- Competitive scans: weekly
