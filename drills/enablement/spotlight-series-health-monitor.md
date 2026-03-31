---
name: spotlight-series-health-monitor
description: Monitor per-feature spotlight performance, detect series fatigue, and report on cumulative discovery impact
category: Enablement
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
  - attio-lists
---

# Spotlight Series Health Monitor

This drill builds the measurement layer for an ongoing feature spotlight series. It tracks per-spotlight performance, cumulative series impact, audience fatigue signals, and feature discovery velocity. Without this drill, you are sending spotlights blind — you do not know which ones worked, which features are still undiscovered, or when your audience is tired of hearing from you.

## Input

- Feature spotlight series running for at least 4 weeks (minimum 4 spotlights delivered)
- PostHog events flowing: `spotlight_delivered`, `spotlight_opened`, `spotlight_clicked`, `spotlight_feature_tried`, `spotlight_feature_adopted`
- Spotlight Calendar maintained in Attio (feature name, date, target segment, reach)
- n8n instance for scheduled monitoring

## Steps

### 1. Build the per-spotlight performance funnel

Using `posthog-funnels`, create a funnel template that measures each spotlight's conversion path:

```
spotlight_delivered (feature={X})
  -> spotlight_opened (feature={X})
    -> spotlight_clicked (feature={X})
      -> spotlight_feature_tried (feature={X})
        -> spotlight_feature_adopted (feature={X})
```

Break down by channel (`email` vs `in-app`) to understand which delivery mechanism drives more actual feature adoption, not just clicks. Calculate per-spotlight:

| Metric | Formula | Target |
|--------|---------|--------|
| Open rate | opened / delivered | >40% in-app, >25% email |
| Click-through rate | clicked / opened | >15% |
| Trial rate | tried / clicked | >30% |
| Adoption rate | adopted / tried | >20% |
| End-to-end rate | adopted / delivered | >3% |

### 2. Build the series-level dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Spotlight funnel by feature | Stacked bar chart | Compare conversion across all spotlights |
| Feature discovery coverage | Progress bar | Percentage of product features that have been spotlighted |
| Cumulative adoption lift | Line chart (trend) | Total users who adopted a feature because of a spotlight, cumulative over time |
| Series engagement trend | Line chart | Open rate and CTR per spotlight over time — declining trend signals fatigue |
| Per-feature adoption delta | Bar chart | Each feature's adoption rate before vs. after spotlight |
| Audience saturation | Pie chart | Users who received 0, 1-3, 4-6, 7+ spotlights |
| Channel effectiveness | Grouped bar | Email vs. in-app conversion rates per spotlight |

### 3. Configure fatigue detection

Using `posthog-anomaly-detection` and `n8n-scheduling`, build a weekly fatigue detection check:

**Engagement fatigue signals:**
- Open rate declining for 3+ consecutive spotlights
- Unsubscribe rate on spotlight emails exceeding 0.5%
- In-app dismiss rate increasing for 3+ consecutive spotlights
- Click-through rate dropping below 8% for 2+ consecutive spotlights

**Audience saturation signals:**
- >30% of active users have received 6+ spotlights (they have seen many; stop sending unless they engage)
- Target cohort size shrinking below 50 users for most features (the addressable audience is depleted)

When fatigue is detected:
1. Log the signal in Attio using `attio-notes`
2. If engagement fatigue: change the spotlight format (try video, try interactive demo, try different subject line structure)
3. If audience saturation: implement tiered frequency — highly engaged users get weekly spotlights, low-engagement users drop to biweekly or monthly
4. If both: pause the series for 2 weeks and re-launch with a refreshed format

### 4. Track cumulative discovery impact

Using `posthog-custom-events` and `posthog-cohorts`, measure the series' aggregate impact on product health:

- **Feature coverage**: How many of the product's features have been spotlighted? Track progress toward 100%.
- **Discovery velocity**: Average time from feature launch to first spotlight. Target: within 4 weeks of launch.
- **Adoption lift**: For each spotlighted feature, compare the 30-day adoption rate before the spotlight vs. the 30-day adoption rate after. Aggregate across all spotlights for the series-level lift.
- **Retention correlation**: Using `posthog-cohorts`, compare 90-day retention for users who engaged with at least 1 spotlight vs. users who received spotlights but never engaged. If spotlight engagers retain better, the series is driving real value.
- **Stickiness**: Of users who adopted a feature via a spotlight, what percentage are still using it 30 days later? If stickiness is below 40%, the spotlights may be driving trial without lasting adoption.

### 5. Generate the weekly series report

Using `n8n-scheduling`, automate a Monday report:

Structure:
```
SPOTLIGHT SERIES — WEEK OF {date}

LAST SPOTLIGHT: {feature name}
  Delivered: {N} | Opened: {N} ({%}) | Clicked: {N} ({%})
  Tried: {N} ({%}) | Adopted: {N} ({%})
  Channel winner: {email|in-app}
  vs. series average: {above|below|inline}

SERIES HEALTH:
  Spotlights shipped: {N} total
  Features covered: {N}/{total} ({%})
  Cumulative adoption lift: {N} users adopted features via spotlights
  Engagement trend: {stable|declining|improving}
  Fatigue signals: {none|list of active signals}

NEXT SPOTLIGHT: {recommended feature}
  Target audience: {N} users
  Rationale: {why this feature, why this audience}
```

Post to Slack and store in Attio using `attio-notes`.

### 6. Maintain the spotlight backlog

Using `attio-lists`, keep a running backlog of features to spotlight:

For each feature:
- Last spotlighted date (or "never")
- Current adoption rate
- Estimated value (retention correlation score)
- Target audience size
- Priority score = (value x audience size) / recency penalty

Re-score the backlog weekly as part of the Monday report. Features that were spotlighted but had low adoption get a lower priority for re-spotlighting (the audience already said no). Features with growing adoption after a spotlight do not need re-spotlighting (it worked).

## Output

- Per-spotlight conversion funnel in PostHog
- Series-level health dashboard with 7 panels
- Automated fatigue detection with response playbook
- Cumulative discovery impact tracking
- Weekly series report (automated)
- Scored spotlight backlog in Attio

## Triggers

The fatigue detection and weekly report run every Monday via n8n cron. The dashboard is reviewed weekly. Re-run the full setup when changing the spotlight format, adding new features, or adjusting the cadence.
