---
name: partner-performance-reporting
description: Monitor per-partner ROI, surface optimization levers, and generate weekly partnership performance briefs
category: Partnerships
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Partner Performance Reporting

This drill builds the monitoring and reporting layer specific to the co-marketing shoutouts play. It tracks per-partner performance, surfaces which partners and blurb variants drive the most value, and generates weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- Active partner placements with PostHog tracking in place (UTM parameters firing)
- Attio partner records with placement history
- At least 4 weeks of placement data (minimum for meaningful trends)

## Steps

### 1. Build the partnership dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Co-Marketing Shoutouts — Partner Performance" with these panels:

- **Clicks by partner** (bar chart): `pageview` events grouped by `utm_source` where `utm_campaign = co-marketing-shoutouts`, last 30 days
- **Leads by partner** (bar chart): `co_marketing_click` events grouped by `utm_source`, last 30 days
- **Click-to-lead conversion rate by partner** (table): leads / clicks per partner, sorted descending
- **Clicks over time** (trend line): weekly `pageview` events with `utm_campaign = co-marketing-shoutouts`, last 90 days
- **Blurb variant performance** (table): clicks and leads grouped by `utm_content` (variant ID), to compare which copy angles work best
- **Landing page conversion funnel**: `pageview` → `co_marketing_click` → downstream conversion (if tracked), filtered to co-marketing traffic

### 2. Create partner performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:
- **High-value partners**: Partners whose leads converted to meetings or signups at >10% rate
- **Volume partners**: Partners driving >50 clicks/month but low conversion
- **Declining partners**: Partners whose clicks dropped >30% month-over-month
- **New partners**: Partners with first placement in the last 30 days (need more data before judging)

These cohorts feed the `autonomous-optimization` drill's anomaly detection.

### 3. Build the weekly partnership brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of co-marketing data from PostHog (clicks, leads, conversion rates per partner)
2. Pull partner pipeline data from Attio (new partners contacted, partnerships activated, placements scheduled)
3. Compare this week's metrics to the 4-week rolling average
4. Use the `hypothesis-generation` fundamental to generate insights:
   - Which partners over/underperformed this week and why?
   - Which blurb variants outperformed?
   - What should change next week?
5. Compile into a structured brief and post to Slack

Brief format:
```
## Co-Marketing Weekly Brief — {date}

**This week**: {total_clicks} clicks, {total_leads} leads ({conversion_rate}% CVR)
**vs 4-week avg**: {change_pct}% {up/down}

### Top partners this week
1. {partner_1}: {clicks} clicks, {leads} leads
2. {partner_2}: {clicks} clicks, {leads} leads

### Underperformers
- {partner}: {clicks} clicks (down {pct}% from last week) — {hypothesis}

### Blurb insights
- Best variant: {variant} ({ctr}% CTR)
- Worst variant: {variant} ({ctr}% CTR)

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Build the per-partner ROI tracker

In Attio, maintain these fields on each partner record (updated weekly by n8n):
- **Total placements**: Count of newsletter issues featuring your blurb
- **Total clicks**: Cumulative clicks from this partner
- **Total leads**: Cumulative leads from this partner
- **Cost per lead**: Total cost (partner fees, if any) / total leads
- **Best blurb variant**: The variant ID that performed best with this partner
- **Last placement date**: When the most recent blurb ran
- **Next placement date**: Scheduled upcoming placement
- **Partner health score**: Composite of recency, frequency, and performance (calculated by n8n)

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:
- Any partner's weekly clicks drop >50% vs prior week → flag in Slack, investigate
- A new partner's first placement exceeds 50 clicks → celebrate in Slack, fast-track for repeat
- Total co-marketing leads drop below Scalable baseline for 2 consecutive weeks → trigger `autonomous-optimization` investigation
- A blurb variant achieves >5% CTR → flag as "proven template" for reuse across partners

## Output

- PostHog dashboard with per-partner and per-variant performance
- Weekly automated partnership brief with insights and recommendations
- Per-partner ROI tracking in Attio
- Alert system for performance anomalies
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts once at the start of Durable level. The weekly brief runs every Friday. Partner ROI fields update weekly via n8n.
