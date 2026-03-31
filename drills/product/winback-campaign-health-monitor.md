---
name: winback-campaign-health-monitor
description: Always-on monitoring for winback campaign metrics with anomaly detection, segment performance tracking, and weekly health briefs
category: Product
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
  - hypothesis-generation
---

# Winback Campaign Health Monitor

This drill builds the always-on monitoring layer for the winback-campaign play. It tracks reactivation rates, segment performance, offer effectiveness, and retention of reactivated users — surfacing anomalies and opportunities for the autonomous optimization loop.

## Input

- PostHog with winback event tracking configured (`winback_email_sent`, `winback_engaged`, `winback_reactivated`, `winback_retained_30d`, `winback_rechurned`)
- n8n instance for scheduled monitoring workflows
- Attio with winback campaign records
- Anthropic API key for health brief generation
- At least 2 weeks of winback campaign data at Scalable level

## Steps

### 1. Build daily anomaly detection

Using `n8n-scheduling`, create a daily workflow that runs at 07:00 UTC:

1. Use `posthog-anomaly-detection` to check these metrics against their 4-week rolling average:
   - Overall reactivation rate (winback_reactivated / winback_email_sent)
   - Email open rate per segment
   - Email click-through rate per segment
   - Reactivation rate per churn reason segment
   - 30-day retention of reactivated users (winback_retained_30d / winback_reactivated)
   - Rechurn rate (winback_rechurned / winback_reactivated)

2. Classify each metric:
   - **Normal:** Within +/-10% of rolling average
   - **Plateau:** Within +/-2% for 3+ consecutive weeks
   - **Drop:** >20% decline from rolling average
   - **Spike:** >50% increase (unusual for winback — investigate whether data is accurate)

3. If any metric classified as Drop or Plateau, store the anomaly in Attio as a note on the winback campaign record with: metric name, current value, rolling average, classification, and affected segments.

4. If anomaly detected, trigger a notification to the autonomous optimization loop.

### 2. Build weekly segment performance report

Using `n8n-scheduling`, create a weekly workflow that runs Monday at 08:00 UTC:

1. Pull from PostHog using `posthog-dashboards`:
   - Reactivation rate by churn reason segment (price, feature, competitor, experience, inactive)
   - Reactivation rate by recency sub-segment (fresh, mid, stale, cold)
   - Reactivation rate by value sub-segment (high, standard, low)
   - Email sequence performance: open rate, click rate, and reply rate per email step per segment
   - In-app welcome-back message performance: impression rate, click rate, reactivation rate
   - Offer redemption rate by offer type (discount, free trial, feature access)

2. Identify the best-performing and worst-performing segments. Flag any segment with reactivation rate below 5% as "candidate for retirement" — stop spending resources on segments that consistently fail.

3. Calculate cost per reactivation by segment: (Loops email cost + Intercom message cost + personal outreach time cost) / reactivations in that segment.

### 3. Track reactivated user retention

The real measure of winback success is not just reactivation — it is whether reactivated users stick. Build a cohort analysis using `posthog-cohorts`:

- Create a dynamic cohort: "Reactivated users" = users with `winback_reactivated` event
- Track their weekly retention at 7, 14, 30, 60, and 90 days post-reactivation
- Compare retention of reactivated users vs. retention of never-churned users
- Flag if reactivated user retention drops below 50% of never-churned retention — this means winback is producing low-quality reactivations

Track rechurn specifically: users who reactivate and then churn again within 90 days. If rechurn rate exceeds 40%, the winback offers are attracting deal-seekers, not genuinely re-engaged users.

### 4. Generate weekly health brief

Using `hypothesis-generation`, produce a weekly brief:

```
# Winback Campaign Health Brief — Week of [date]

## Key Metrics
- Reactivation rate: [X%] (target: [Y%], trend: [up/down/flat])
- Total reactivations this week: [N]
- Reactivated user 30-day retention: [X%]
- Rechurn rate: [X%]
- Cost per reactivation: $[X]
- Revenue recovered: $[X] MRR

## Segment Performance
| Segment | Reactivation Rate | Trend | Volume | Status |
|---------|-------------------|-------|--------|--------|
| Price   | [X%]              | [up/down/flat] | [N] | [active/watch/retire] |
| Feature | [X%]              | ... | ... | ... |
| Competitor | [X%]           | ... | ... | ... |
| Experience | [X%]           | ... | ... | ... |
| Inactive | [X%]             | ... | ... | ... |

## Anomalies
- [List any metrics classified as Drop or Plateau]

## Optimization Opportunities
- [Top opportunity identified from segment analysis]
- [Second opportunity]

## Active Experiments
- [Experiment name, hypothesis, days running, interim direction]
```

Store the brief in Attio and post to the configured notification channel.

### 5. Configure critical alerts

Set up immediate alerts (not weekly) for:
- Overall reactivation rate drops >30% below 4-week average
- Email delivery failure rate exceeds 5% (domain reputation issue)
- Rechurn rate exceeds 50% in any week (offers are attracting wrong users)
- Any segment's reactivation rate drops to 0% for 7+ days (likely a broken automation)

Route critical alerts to the team immediately. These cannot wait for the weekly brief.

## Output

- Daily anomaly detection feeding the autonomous optimization loop
- Weekly health briefs with segment-level performance data
- Reactivated user retention cohort tracking
- Critical alerts for system failures or metric collapses
- All monitoring data stored in Attio for historical analysis

## Triggers

- Daily: Anomaly detection at 07:00 UTC
- Weekly: Health brief generation Monday 08:00 UTC
- Continuous: Critical alerts fire immediately when thresholds are breached
