---
name: podcast-performance-monitor
description: Track and report on podcast guest appearance performance including downloads, referral traffic, and lead attribution
category: Podcast
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - podcast-episode-analytics
  - posthog-dashboards
  - posthog-custom-events
  - attio-reporting
  - n8n-scheduling
---

# Podcast Performance Monitor

This drill creates an ongoing measurement system that tracks the ROI of every podcast guest appearance. It attributes traffic, leads, and pipeline to individual episodes and identifies which podcast characteristics (audience size, topic, format) produce the best results.

## Input

- At least 3 podcast appearances completed with tracking links deployed
- PostHog tracking configured for podcast UTM parameters
- Attio list of all podcast appearances with metadata

## Steps

### 1. Build the PostHog podcast dashboard

Use `posthog-dashboards` to create a dashboard called "Podcast Guest ROI" with these insights:

**Insight 1 — Traffic by podcast**
- Event: `$pageview`
- Filter: `utm_source = podcast AND utm_medium = guest`
- Breakdown by: `utm_campaign` (one line per podcast)
- Date range: Last 90 days
- Chart: Line graph

**Insight 2 — Podcast lead funnel**
- Funnel steps:
  1. `$pageview` (where `utm_source = podcast`)
  2. `lead_created` (where `utm_source = podcast`)
  3. `meeting_booked` (where `utm_source = podcast`)
- Breakdown by: `utm_campaign`
- Shows conversion rate from visit to lead to meeting per podcast

**Insight 3 — Episode performance over time**
- Event: `$pageview` (where `utm_source = podcast`)
- Filter by specific `utm_campaign` + `utm_content` (episode date)
- Date range: 30 days from episode air date
- Chart: Line graph showing traffic decay curve per episode

**Insight 4 — Aggregate podcast KPIs**
- Total podcast referral visits (last 30 days, last 90 days)
- Total podcast-attributed leads
- Total podcast-attributed meetings
- Cost per lead (divide total podcast spend by leads)

### 2. Set up automated reporting

Use `n8n-scheduling` to create a weekly workflow that:

1. Queries PostHog for podcast metrics from the past 7 days
2. Compares to previous 7-day period (week-over-week change)
3. Identifies which episodes are still driving traffic (long-tail value)
4. Identifies episodes with traffic but no conversions (CTA or landing page problem)
5. Generates a summary and sends it to Slack or email

### 3. Update Attio with performance data

For each podcast appearance in Attio, maintain these fields:
- `total_clicks_7d`: UTM clicks in first 7 days
- `total_clicks_30d`: UTM clicks in first 30 days
- `total_clicks_lifetime`: All-time UTM clicks
- `leads_attributed`: Leads with `utm_source=podcast` and matching campaign
- `meetings_attributed`: Meetings from podcast traffic
- `host_reported_downloads`: Downloads if the host shared data
- `episode_roi_score`: (leads_attributed * estimated_deal_value) / time_invested

Use `attio-reporting` to build a view that ranks all podcast appearances by ROI score.

### 4. Identify patterns

After 5+ appearances, analyze which factors correlate with best results:
- **Audience size**: Do bigger podcasts always perform better, or do niche shows convert higher?
- **Topic angle**: Which pitch angles drove the most traffic/leads?
- **Host style**: Interview formats vs conversational — which converts better?
- **Day of week aired**: Does air day affect traffic?
- **CTA type**: Which offers (free trial, resource, consultation) drive more clicks?

Document findings in Attio notes. Feed insights back into `podcast-prospect-research` to refine targeting.

### 5. Calculate long-tail value

Podcast episodes keep generating traffic for months or years. Track:
- % of total podcast traffic from episodes older than 30 days
- Cumulative lifetime traffic per episode
- Point at which traffic drops below 1 visit/week (episode is "spent")

This data informs whether to prioritize new appearances (more episodes) or repurposing existing episodes (more distribution of fewer, higher-performing appearances).

## Output

- PostHog dashboard with real-time podcast ROI visibility
- Weekly automated performance report
- Attio records enriched with per-episode performance data
- Pattern analysis identifying highest-ROI podcast characteristics

## Triggers

- Dashboard: built once, reviewed weekly
- Automated report: runs every Monday via n8n
- Attio update: runs 7 days and 30 days after each episode airs, then monthly thereafter
