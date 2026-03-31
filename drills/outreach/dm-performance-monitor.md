---
name: dm-performance-monitor
description: Track and report on DM outreach performance across LinkedIn and Twitter/X channels
category: Outreach
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
---

# DM Performance Monitor

This drill builds an always-on monitoring and reporting system for cold DM plays across LinkedIn and X. It tracks funnel metrics, detects performance changes, and generates weekly performance briefs. Used at Durable level alongside `autonomous-optimization`.

## Input

- PostHog with DM play events tracked (from `posthog-gtm-events` drill)
- Attio with deal records sourced from DM outreach
- n8n for scheduling automated reports
- At least 4 weeks of DM outreach data for meaningful trend analysis

## Steps

### 1. Define the DM funnel events

Ensure these events are flowing into PostHog (via `posthog-custom-events`):

| Event | Description | Properties |
|-------|-------------|------------|
| `dm_engagement_started` | First like/comment on prospect's content | channel (linkedin/x), prospect_id |
| `dm_sent` | DM message delivered | channel, prospect_id, message_variant, day_of_week, time_of_day |
| `dm_opened` | DM read by recipient (where trackable) | channel, prospect_id |
| `dm_replied` | Prospect responded to DM | channel, prospect_id, sentiment (positive/neutral/negative) |
| `dm_meeting_booked` | Meeting scheduled from DM conversation | channel, prospect_id, deal_value |
| `dm_meeting_held` | Meeting actually occurred (no-show tracking) | channel, prospect_id |
| `dm_deal_created` | Deal entered pipeline from DM-sourced meeting | channel, prospect_id, deal_value |

### 2. Build the DM performance dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

- **Funnel**: dm_sent > dm_replied > dm_meeting_booked > dm_deal_created (breakdown by channel: LinkedIn vs X)
- **Reply rate trend**: Weekly reply rate for each channel over the last 12 weeks
- **Best performing message variants**: Reply rate by message_variant property
- **Day/time heatmap**: Reply rate by day_of_week and time_of_day
- **Channel comparison**: Side-by-side metrics for LinkedIn and X
- **Cost per meeting**: (tool costs + time cost) / meetings booked, per channel
- **Pipeline value**: Total deal value attributed to DM outreach, per channel

### 3. Set up threshold alerts

Using `posthog-custom-events` and n8n:

- **Reply rate drop**: Alert if 7-day rolling reply rate drops below 10% on either channel.
- **Volume drop**: Alert if daily DM send volume drops below 50% of the 4-week average (indicates automation failure or list exhaustion).
- **Negative sentiment spike**: Alert if negative replies exceed 15% of total replies in a 7-day window.
- **Meeting no-show rate**: Alert if no-show rate exceeds 30% over 2 weeks (indicates qualification problem).

Route alerts to Slack and log them in Attio.

### 4. Build the weekly performance brief

Using `n8n-scheduling`, create a weekly cron workflow (runs Monday 8am):

1. Query PostHog for the last 7 days of DM metrics.
2. Compare to the prior 7-day period and the 4-week rolling average.
3. Pull Attio pipeline data for DM-sourced deals.
4. Generate a brief with:
   - DMs sent (LinkedIn + X)
   - Reply rate by channel (vs prior week)
   - Meetings booked (vs prior week)
   - Pipeline value added
   - Top performing message variant
   - Anomalies or alerts triggered this week
   - Recommended actions (e.g., "Reply rate on X dropped 8pp -- investigate message fatigue")
5. Post to Slack and store in Attio.

### 5. Build the monthly channel health report

In addition to weekly briefs, generate a monthly deep-dive report:

- LinkedIn vs X channel comparison (which produces more meetings per hour of effort?)
- Message variant lifecycle: which variants are decaying and should be retired?
- ICP segment performance: which segments respond best on each channel?
- Cost analysis: all-in cost per meeting by channel (tool costs + estimated time)
- Recommendation: increase/decrease investment in each channel based on data

### 6. Feed data to autonomous-optimization

Expose key metrics via PostHog API so the `autonomous-optimization` drill can:
- Detect when reply rates plateau or drop
- Identify which variables to experiment on (message copy, send timing, engagement duration, ICP segment)
- Evaluate experiment results against the DM funnel

## Output

- Real-time PostHog dashboard for DM outreach performance
- Automated threshold alerts for metric anomalies
- Weekly performance briefs posted to Slack
- Monthly channel health reports
- Data pipeline feeding `autonomous-optimization` for Durable-level experimentation

## Triggers

- Dashboard: always-on, updated in real-time as events flow
- Threshold alerts: checked continuously via PostHog webhooks
- Weekly brief: Monday 8am via n8n cron
- Monthly report: first Monday of each month via n8n cron
