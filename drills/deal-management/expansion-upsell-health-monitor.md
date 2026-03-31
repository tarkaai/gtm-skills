---
name: expansion-upsell-health-monitor
description: Monitor the usage-limit sales upsell funnel — signal detection, qualification, outreach, and close rates — and surface weekly health reports for autonomous optimization
category: Deal Management
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Expansion Upsell Health Monitor

This drill builds the monitoring and reporting layer for the usage-limit sales upsell play. It tracks the full pipeline from usage signal detection through sales qualification, outreach, meeting booking, and deal close. It generates weekly health reports and feeds metrics to the `autonomous-optimization` loop at Durable level.

## Input

- PostHog events from usage detection, scoring, and outreach tracking
- Attio expansion deals with stage progression data
- At least 2 weeks of pipeline data
- n8n instance for scheduled monitoring

## Steps

### 1. Build the expansion pipeline dashboard

Using the `posthog-dashboards` fundamental, create a dashboard called "Usage Expansion Sales Health" with these panels:

**Panel 1: Full Pipeline Funnel (Funnel insight)**
Using `posthog-funnels`:
1. `expansion_score_computed` (accounts scored as Tier 1)
2. `expansion_deal_created` (expansion deal opened in Attio)
3. `expansion_outreach_sent` (first touch delivered)
4. `expansion_meeting_booked` (Cal.com booking confirmed)
5. `expansion_deal_closed` (upgrade completed)

Break down by: resource type, expansion tier, account MRR band, outreach channel.

**Panel 2: Pipeline Velocity (Trend insight)**
Track median days between each funnel stage over time. Healthy: signal-to-deal < 1 day, deal-to-first-touch < 1 day, first-touch-to-meeting < 7 days, meeting-to-close < 14 days. If any stage exceeds 2x the target, flag for investigation.

**Panel 3: Outreach Sequence Performance (Table insight)**
Per touch: delivery count, open rate, reply rate, meeting booking rate. Sort by reply rate descending. Compare Touch 1 vs Touch 2 vs Touch 3 vs Touch 4 performance to identify the highest-converting touch point.

**Panel 4: Expansion Revenue (Trend insight)**
Weekly expansion ARR from usage-triggered sales deals. Cumulative total for the play's duration. Overlay with total company expansion ARR to show what percentage is driven by this play.

**Panel 5: Scoring Model Accuracy (Bar chart)**
Tier 1 conversion rate (deals closed / Tier 1 accounts), Tier 2 conversion rate, Self-serve conversion rate. The scoring model is working if Tier 1 conversion rate is significantly higher than Tier 2.

**Panel 6: Resource-Level Performance (Table insight)**
Per resource type: signals detected, deals created, deals closed, conversion rate, average deal value. Identifies which usage limits are the most productive expansion triggers.

### 2. Configure anomaly alerts

Using `posthog-anomaly-detection`, set up alerts:

- **Pipeline stall:** If zero new expansion deals are created for 5 consecutive days while Tier 1 signals are being detected → alert (scoring or deal creation may be broken)
- **Outreach degradation:** If Touch 1 open rate drops below 30% for 7 consecutive days → alert (deliverability issue or subject line fatigue)
- **Conversion collapse:** If meeting-to-close conversion drops below 20% for 2 consecutive weeks → alert (pricing objections or product fit issue)
- **Score inflation:** If Tier 1 account volume increases 50%+ week over week without corresponding close rate increase → alert (scoring thresholds may need tightening)
- **Revenue decline:** If weekly expansion ARR drops 30%+ compared to 4-week rolling average → alert

Route alerts to team Slack and log in Attio.

### 3. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 08:00 UTC:

```
# Usage Expansion Sales — Weekly Health Report

## Pipeline
- Tier 1 accounts identified: [N] ([delta] vs last week)
- Expansion deals created: [N]
- Outreach sequences started: [N]
- Meetings booked: [N] (booking rate: [%])
- Deals closed: [N] (close rate: [%])

## Outreach Performance
- Touch 1: [N] sent, [%] open, [%] reply
- Touch 2: [N] sent, [%] reply
- Touch 3: [N] sent, [%] reply
- Touch 4: [N] sent, [%] reply
- Self-serve conversions during outreach: [N]

## Revenue Impact
- Expansion ARR this week: $[N]
- Expansion ARR trailing 30d: $[N]
- Average deal size: $[N]
- Expansion as % of total revenue growth: [%]

## Scoring Accuracy
- Tier 1 close rate: [%] (target: 35%+)
- Tier 2 close rate: [%]
- Top-performing resource signal: [resource] at [%] close rate

## Pipeline Velocity
- Signal to deal: [N] days (target: <1)
- Deal to first touch: [N] days (target: <1)
- First touch to meeting: [N] days (target: <7)
- Meeting to close: [N] days (target: <14)

## Anomalies
- [List any metric that deviated >20% from 4-week average]

## Recommendations
- [Agent-generated suggestions based on this week's data]
```

Post to Slack and store in Attio. At Durable level, this report feeds into the `autonomous-optimization` loop.

### 4. Create the optimization webhook

Using `n8n-workflow-basics`, create a webhook endpoint that the `autonomous-optimization` drill can call to retrieve current health metrics:

```json
{
  "play": "usage-limit-sales-upsell",
  "period": "last_7_days",
  "metrics": {
    "tier_1_accounts": 23,
    "deals_created": 18,
    "meetings_booked": 9,
    "deals_closed": 5,
    "close_rate": 0.28,
    "expansion_arr_week": 4200,
    "expansion_arr_30d": 15800,
    "touch_1_open_rate": 0.62,
    "touch_1_reply_rate": 0.18,
    "meeting_booking_rate": 0.50,
    "scoring_tier_1_close_rate": 0.28,
    "scoring_tier_2_close_rate": 0.08,
    "avg_days_signal_to_close": 12,
    "top_resource": "api_calls",
    "top_resource_close_rate": 0.38
  }
}
```

The autonomous optimization loop uses these metrics to detect plateaus, generate improvement hypotheses (e.g., "scoring weights need recalibration" or "Touch 2 subject line has decayed"), and design experiments.

## Output

- PostHog dashboard "Usage Expansion Sales Health" with 6 panels
- Anomaly alerts for pipeline stalls, outreach degradation, conversion collapse, and revenue decline
- Weekly automated health report posted to Slack and stored in Attio
- Webhook endpoint for autonomous optimization integration

## Triggers

Dashboard is always-on. Anomaly alerts run continuously. Weekly report runs every Monday at 08:00 UTC via n8n cron. Webhook responds on demand.
