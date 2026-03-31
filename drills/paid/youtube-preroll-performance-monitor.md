---
name: youtube-preroll-performance-monitor
description: Monitor YouTube pre-roll campaign health, detect creative fatigue, flag audience saturation, and generate weekly performance reports
category: Paid
tools:
  - Google Ads
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - google-ads-youtube-reporting
  - posthog-anomaly-detection
  - posthog-dashboards
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-notes
  - hypothesis-generation
---

# YouTube Pre-roll Performance Monitor

This drill creates an automated monitoring system for YouTube pre-roll campaigns. It detects creative fatigue, audience saturation, budget pacing issues, and lead quality degradation before they become costly. At Durable level, this drill feeds into `autonomous-optimization` for the full detect-diagnose-experiment-evaluate loop.

## Prerequisites

- Active YouTube pre-roll campaign(s) with at least 7 days of data
- Google Ads API access configured
- PostHog with YouTube campaign events tracked (from `youtube-preroll-lead-routing`)
- n8n instance for scheduling monitoring workflows

## Input

- Baseline performance metrics (from Baseline level): average VTR, average CPV, average cost per lead, average ICP match rate
- Alert thresholds (configurable, see defaults below)
- Reporting recipients (Slack channel or email list)

## Steps

### 1. Build the daily health check workflow

Create an n8n workflow on a daily cron schedule (9am):

**Pull campaign metrics:**
Using `google-ads-youtube-reporting`, query:
- Yesterday's metrics per campaign: impressions, views, VTR, CPV, clicks, CTR, conversions, cost per conversion, spend
- Last 7-day rolling metrics per campaign (same fields)
- Per-variant metrics: impressions, VTR, CTR, cost per conversion

**Pull lead quality metrics from PostHog:**
Using `posthog-dashboards`, query:
- Yesterday's `yt_preroll_form_submit` count
- Yesterday's `yt_preroll_lead_enriched` with average ICP score
- Yesterday's `yt_preroll_meeting_booked` count

**Compute derived metrics:**
- 7-day cost per qualified lead (CPqL): spend / leads with ICP score >= 50
- View-to-lead rate: conversions / views
- ICP match rate: leads with score >= 50 / total leads
- Budget pacing: actual spend vs. planned daily spend

### 2. Configure alert thresholds

Default thresholds (agent should store in a config and make adjustable):

| Metric | Warning | Critical |
|--------|---------|----------|
| CPV | >1.5x baseline for 3 days | >2x baseline for 3 days |
| VTR | <75% of baseline for 3 days | <50% of baseline for 3 days |
| Cost per lead | >1.5x baseline for 5 days | >2x baseline for 3 days |
| ICP match rate | <40% for 7 days | <25% for 3 days |
| Daily spend | >120% of planned | >150% of planned |
| Zero conversions | 3 consecutive days | 5 consecutive days |

### 3. Detect creative fatigue

Add a creative fatigue detection step to the daily workflow:

For each active video ad variant:
1. Pull last 7-day VTR and last 7-day CTR from Google Ads
2. Pull the variant's first-week VTR and CTR (stored from initial launch)
3. Calculate VTR decay: (first_week_VTR - last_7d_VTR) / first_week_VTR
4. Calculate CTR decay: same formula

Fatigue thresholds:
- **Warning:** VTR decay > 20% AND variant has been running 10+ days
- **Fatigued:** VTR decay > 30% AND variant has been running 14+ days
- **Action:** Pause fatigued variants via Google Ads API. Queue replacement from `youtube-preroll-creative-pipeline`.

### 4. Detect audience saturation

For each audience segment (placement campaign, custom intent campaign, topic campaign):

1. Pull last 7-day frequency (impressions / unique reach) from Google Ads
2. Pull cost per conversion trend over last 4 weeks

Saturation thresholds:
- **Warning:** Frequency > 3 AND cost per conversion rising for 2 consecutive weeks
- **Saturated:** Frequency > 5 OR cost per conversion > 2x baseline for same audience type
- **Action:** For saturated audiences, reduce budget by 30% and flag for audience refresh via `youtube-preroll-audience-builder`

### 5. Generate weekly performance report

Create an n8n workflow on a weekly cron (Monday 8am):

1. Pull last 7 days of campaign data from Google Ads
2. Pull last 7 days of lead and meeting data from PostHog
3. Pull pipeline data from Attio (deals sourced from YouTube preroll)
4. Use the Anthropic API to generate a structured report:

```
YOUTUBE PRE-ROLL WEEKLY REPORT — Week of [date]

HEADLINE
- Views this week: [X] (vs [Y] last week, [Z] baseline)
- Leads this week: [X] (vs [Y] last week, [Z] baseline)
- Cost per lead: $[X] (vs $[Y] last week, $[Z] target)
- Meetings booked: [X]
- Total spend: $[X] (vs $[Y] budget)
- ICP match rate: [X]%

CREATIVE HEALTH
- Active variants: [X] (of which [Y] are <2 weeks old)
- Top variant: "[name]" — VTR [X]%, CPL $[Y]
- Fatigued variants paused: [X] (list)
- New variants needed: [X]

AUDIENCE HEALTH
- Placement campaign: [X] conversions at $[Y] CPL
- Custom intent campaign: [X] conversions at $[Y] CPL
- Topic campaign: [X] conversions at $[Y] CPL
- Saturated audiences: [list or "none"]

PIPELINE IMPACT
- Leads in nurture: [X]
- Meetings booked this week: [X]
- Deals in pipeline from YouTube preroll (all time): [X] worth $[Y]

ALERTS
- [Any warning or critical alerts from the daily checks this week]

RECOMMENDATION
- [One specific recommendation based on this week's data]
```

5. Post to Slack and store in Attio as a note on the YouTube Preroll campaign record.

### 6. Integration with autonomous-optimization (Durable level)

At Durable, this monitor feeds directly into the `autonomous-optimization` drill:
- Daily health check data becomes the monitoring input for Phase 1 (Monitor)
- Anomaly detection triggers Phase 2 (Diagnose) of the optimization loop
- Creative fatigue triggers automatic hypothesis generation: "Replace fatigued variant with [new angle]"
- Audience saturation triggers automatic hypothesis generation: "Expand to [new placement set]"

The performance monitor becomes the eyes of the autonomous optimization agent.

## Output

- Daily automated health check with alerts on threshold breaches
- Creative fatigue detection with automatic pausing
- Audience saturation detection with budget reduction
- Weekly performance report posted to Slack
- All monitoring data logged in PostHog for trend analysis

## Triggers

- **Daily at 9am:** Health check and fatigue/saturation detection
- **Weekly Monday 8am:** Full performance report
- **On critical alert:** Immediate Slack notification
