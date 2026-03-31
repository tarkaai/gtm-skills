---
name: usage-alert-health-monitor
description: Monitor usage threshold alert system performance — detection accuracy, conversion rates, revenue impact, and system health at Durable cadence
category: Retention
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-custom-events
  - posthog-cohorts
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Usage Alert Health Monitor

This drill builds the observability layer for the usage threshold alert system. It tracks whether detection is accurate, alerts are converting, and upgrades are sticking — then surfaces weekly health reports that feed into the `autonomous-optimization` loop at Durable level.

## Input

- Usage threshold detection and alert delivery systems running for at least 2 weeks (baseline data required)
- PostHog events: `usage_threshold_detected`, `usage_alert_shown`, `usage_alert_clicked`, `usage_alert_converted`
- Attio expansion deals tagged with usage-triggered source
- n8n instance for scheduled reporting

## Steps

### 1. Build the alert effectiveness funnel

Using the `posthog-funnels` fundamental, create the core conversion funnel:

```
usage_threshold_detected
  -> usage_alert_shown
    -> usage_alert_clicked
      -> usage_alert_converted (upgrade completed)
```

Break this funnel down by:
- Resource type (seats, API calls, storage, projects)
- Urgency tier (approaching, imminent, critical, exceeded)
- Channel (in_app, email, human)
- Plan tier (free, starter, pro)

Identify the largest drop-off point. If detection fires but alerts are not shown, the delivery system has a bug. If alerts show but nobody clicks, the copy or placement is wrong. If people click but do not upgrade, the pricing page or checkout flow has friction.

### 2. Build the alert system dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Alerts fired by resource (daily) | Stacked bar chart | Which resources are driving the most alerts |
| Alert-to-upgrade funnel | Funnel chart | Drop-off from detection to conversion |
| Upgrade rate by urgency tier | Bar chart | Which tier converts best |
| Upgrade rate by resource type | Bar chart | Which resources drive the most upgrades |
| Revenue from alert-driven upgrades (weekly) | Line chart | MRR impact trending over time |
| Median days from alert to upgrade | Line chart (trend) | Is the upgrade path getting smoother |
| Alert volume vs. user base growth | Dual-axis line | Are alerts scaling proportionally or spiking |
| False positive rate | Line chart | Are we alerting users who never hit limits |

Set alerts for:
- Alert-to-upgrade conversion drops below 15% for 3 consecutive days
- False positive rate exceeds 30% (users alerted who do not hit limit within 14 days)
- Alert volume spikes 200%+ week over week (may indicate a system misconfiguration or pricing change)
- Zero alerts fired in 48 hours (detection system may be broken)

### 3. Compute detection accuracy

Using `posthog-custom-events` and `posthog-cohorts`, measure how well the detection system predicts actual limit hits:

**True positive rate:** Of accounts flagged as critical (95%+), what percentage actually hit the limit within 7 days? Target: 70%+.

**False positive rate:** Of accounts flagged as imminent (85-94%), what percentage never hit the limit in their billing period? Target: below 30%.

**Miss rate:** Of accounts that hit a limit, what percentage were never flagged beforehand? Target: below 10%. A high miss rate means the detection thresholds are too high or the velocity calculation is miscalibrated.

Log accuracy metrics weekly:

```javascript
posthog.capture('usage_detection_accuracy', {
  week: '2026-W14',
  true_positive_rate: 0.73,
  false_positive_rate: 0.22,
  miss_rate: 0.08,
  total_accounts_flagged: 145,
  total_accounts_hit_limit: 89
});
```

### 4. Track upgrade retention

An upgrade driven by a usage alert is only valuable if the customer stays on the higher tier. Using `posthog-cohorts`, create a cohort of alert-driven upgraders and track:

- 30-day retention on new tier: target 85%+
- 90-day retention on new tier: target 75%+
- Downgrade rate within 60 days: target below 15%

If alert-driven upgrades have a high downgrade rate, the alerts may be creating pressure upgrades rather than genuine expansion. This is a signal to shift from urgency messaging to value messaging.

### 5. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 08:00 UTC:

```
# Usage Alert System — Weekly Health Report

## Detection
- Accounts monitored: [N]
- Alerts fired: [N] (approaching: [N], imminent: [N], critical: [N], exceeded: [N])
- True positive rate: [%]  |  False positive rate: [%]  |  Miss rate: [%]

## Conversion
- Alerts shown: [N]  →  Clicked: [N] ([%])  →  Upgraded: [N] ([%])
- Best converting resource: [resource] at [%] conversion
- Best converting tier: [tier] at [%] conversion
- Best converting channel: [channel] at [%] conversion

## Revenue Impact
- MRR from alert-driven upgrades this week: $[N]
- MRR from alert-driven upgrades trailing 30d: $[N]
- Alert-driven upgrades as % of total upgrades: [%]

## Retention
- 30-day retention of alert-driven upgraders: [%]
- Downgrade rate (60-day): [%]

## System Health
- Detection pipeline: [running/error] — last run [timestamp]
- Alert delivery: [running/error] — last run [timestamp]
- Average detection-to-alert latency: [N] hours

## Anomalies
- [List any metric that deviated >20% from 4-week average]

## Recommendations
- [Agent-generated suggestions based on this week's data]
```

Post to Slack and store in Attio. At Durable level, this report feeds into the `autonomous-optimization` loop as input for anomaly detection.

### 6. Feed optimization loop

Using `n8n-workflow-basics`, create a webhook that the `autonomous-optimization` drill can call to retrieve current health metrics. Return a structured JSON payload:

```json
{
  "play": "usage-threshold-alerts",
  "period": "last_7_days",
  "metrics": {
    "alert_conversion_rate": 0.23,
    "revenue_impact_mrr": 4500,
    "detection_true_positive_rate": 0.73,
    "detection_false_positive_rate": 0.22,
    "upgrade_30d_retention": 0.87,
    "alerts_fired": 145,
    "top_resource": "api_calls",
    "top_channel": "in_app"
  }
}
```

The autonomous optimization loop uses these metrics to detect plateaus, generate improvement hypotheses, and design experiments.

## Output

- Alert effectiveness funnel in PostHog
- Alert system dashboard with 8 panels and threshold alerts
- Detection accuracy metrics computed weekly
- Upgrade retention cohort tracking
- Weekly health report posted to Slack and Attio
- Webhook endpoint for autonomous optimization integration

## Triggers

Dashboard and accuracy metrics: updated daily by PostHog. Weekly health report: cron, Monday 08:00 UTC. Accuracy recalibration: monthly review of detection thresholds based on true positive and miss rates.
