---
name: joint-content-performance-monitor
description: Track per-asset and per-partner ROI for joint content campaigns, surface optimization levers, and generate weekly performance briefs
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
  - attio-notes
  - n8n-scheduling
  - hypothesis-generation
---

# Joint Content Performance Monitor

This drill builds the monitoring and reporting layer specific to the joint-content-campaigns play. It tracks per-asset and per-partner performance, surfaces which partners, topics, and formats generate the most leads, and produces weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- Active joint content assets with PostHog tracking (UTM parameters firing on landing pages and email links)
- Attio partner and deal records with asset metadata
- At least 4 weeks of asset performance data (minimum for meaningful trends)

## Steps

### 1. Build the joint content dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Joint Content Campaigns -- Performance" with these panels:

- **Downloads by asset** (bar chart): `content_download` events grouped by `asset_slug`, last 30 days
- **Downloads by partner** (bar chart): `content_download` events grouped by `partner_slug`, last 30 days
- **Downloads by channel** (bar chart): `content_download` events grouped by `utm_source` (your-email, partner-email, organic, social), last 30 days
- **Download-to-lead conversion by asset** (table): `content_download` to `lead_qualified` events per `asset_slug`, sorted descending
- **Asset performance over time** (trend line): weekly `content_download` events, last 90 days, grouped by `asset_slug`
- **Partner contribution funnel**: `content_download` → `lead_qualified` → `meeting_booked` → `deal_created`, filtered to `source = joint-content`
- **Topic performance** (table): downloads and leads grouped by `content_topic` to identify which problem areas resonate most

### 2. Create performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:
- **High-converting assets**: Assets where download-to-qualified-lead rate exceeds 15%
- **High-volume partners**: Partners whose co-content generates >50 downloads/month
- **Declining assets**: Assets whose monthly downloads dropped >30% month-over-month
- **Fast-converting leads**: Leads from joint content who book a meeting within 14 days of download

These cohorts feed the `autonomous-optimization` drill's anomaly detection at Durable level.

### 3. Build the weekly joint content brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of joint content data from PostHog (downloads, leads, conversion rates per asset and per partner)
2. Pull partner pipeline data from Attio (assets in production, assets published this week, leads attributed)
3. Compare this week's metrics to the 4-week rolling average
4. Use the `hypothesis-generation` fundamental to generate insights:
   - Which assets and partners over/underperformed and why?
   - Which topics and formats are trending up or down?
   - What should change next week (new asset topic, partner emphasis, distribution channel)?
5. Compile into a structured brief and post to Slack

Brief format:
```
## Joint Content Weekly Brief -- {date}

**This week**: {total_downloads} downloads, {total_leads} qualified leads ({conversion_rate}% CVR)
**vs 4-week avg**: {change_pct}% {up/down}

### Top assets this week
1. {asset_1} with {partner_1}: {downloads} downloads, {leads} leads
2. {asset_2} with {partner_2}: {downloads} downloads, {leads} leads

### Top partners this week
1. {partner}: {downloads} total downloads across {asset_count} assets

### Underperformers
- {asset}: {downloads} downloads (down {pct}% from last week) -- {hypothesis}

### Topic insights
- Best topic: {topic} ({downloads} downloads, {cvr}% CVR)
- Declining topic: {topic} ({change}% week-over-week)

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Maintain per-asset ROI tracking in Attio

Using the `attio-reporting` fundamental, maintain these fields on each asset deal record (updated weekly by n8n):
- **Total downloads**: Cumulative downloads across all channels
- **Your-list downloads**: Downloads from your email/social distribution
- **Partner-list downloads**: Downloads from partner distribution
- **Organic downloads**: Downloads from SEO/direct traffic
- **Qualified leads**: Leads that passed qualification from this asset
- **Meetings booked**: Meetings attributed to this asset
- **Cost per lead**: Total production cost / qualified leads
- **Asset format**: Ebook, guide, report, checklist, etc.
- **Content topic**: Primary topic/pain point addressed
- **Partner name**: Which partner co-created this asset
- **Publication date**: When the asset went live
- **Asset health score**: Composite of recency, download velocity, and conversion rate

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:
- Any asset's weekly downloads drop >50% vs prior week -> flag in Slack for investigation
- A new asset exceeds 100 downloads in its first week -> celebrate in Slack, flag for repeat topic
- Total joint content leads drop below Scalable baseline for 2 consecutive weeks -> trigger `autonomous-optimization` investigation
- An asset achieves >20% download-to-lead conversion -> flag as "proven format" for reuse with other partners
- A partner's overall contribution drops >40% month-over-month -> investigate whether the partner relationship needs attention

## Output

- PostHog dashboard with per-asset, per-partner, and per-topic performance
- Weekly automated joint content brief with insights and recommendations
- Per-asset ROI tracking in Attio
- Alert system for performance anomalies
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts once at the start of Durable level. The weekly brief runs every Friday. Asset ROI fields update weekly via n8n.
