---
name: feature-discovery-tooltips-baseline
description: >
  Contextual Feature Tooltips — Baseline Run. Deploy always-on tooltips for 3-5 underused
  features with event tracking, automated delivery via Intercom, and funnel analysis
  proving tooltips drive sustained feature adoption.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=40% CTR AND >=12% sustained adoption (3+ uses in 7 days post-click)"
kpis: ["Tooltip CTR", "Feature first-use rate", "Sustained adoption rate", "Dismissal rate"]
slug: "feature-discovery-tooltips"
install: "npx gtm-skills add product/retain/feature-discovery-tooltips"
drills:
  - posthog-gtm-events
  - feature-announcement
  - tooltip-performance-monitor
---

# Contextual Feature Tooltips — Baseline Run

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

3-5 feature tooltips running always-on via Intercom. Tooltip CTR >=40% and sustained adoption rate >=12% (users who click the tooltip and then use the feature 3+ times in the following 7 days). This proves tooltips drive lasting behavior change, not just curiosity clicks.

## Leading Indicators

- Tooltip impressions growing daily as new users enter eligibility cohorts
- Click-to-first-use conversion rate above 60% (most clickers actually try the feature)
- Dismissal rate stable or declining (not trending toward fatigue)
- At least 1 tooltip achieving sustained adoption rate above 15%

## Instructions

### 1. Expand event tracking

Run the `posthog-gtm-events` drill to set up comprehensive tooltip event tracking. Configure these events:

```javascript
// Tooltip lifecycle events
posthog.capture('tooltip_shown', {
  feature: '{feature_name}',
  tooltip_id: '{tooltip_id}',
  user_segment: '{new|established|power}',
  page_context: '{page_path}'
});

posthog.capture('tooltip_cta_clicked', {
  feature: '{feature_name}',
  tooltip_id: '{tooltip_id}',
  time_to_click_ms: '{milliseconds from shown to click}'
});

posthog.capture('tooltip_dismissed', {
  feature: '{feature_name}',
  tooltip_id: '{tooltip_id}',
  reason: '{x_button|click_away|timeout}'
});

// Downstream feature events
posthog.capture('feature_first_used', {
  feature: '{feature_name}',
  source: 'tooltip',
  tooltip_id: '{tooltip_id}'
});

posthog.capture('feature_repeat_used', {
  feature: '{feature_name}',
  usage_count_7d: '{count}',
  source_was_tooltip: true
});
```

Build a PostHog funnel: `tooltip_shown -> tooltip_cta_clicked -> feature_first_used -> feature_repeat_used (count >= 3)`.

### 2. Deploy tooltips for 3-5 features

Using the feature gap analysis from Smoke, identify 3-5 features with the best tooltip potential. For each feature, run the `feature-announcement` drill to create an Intercom in-app tooltip:

For each tooltip, configure in Intercom:
- **Audience**: Users active in last 7 days AND have not used this feature in last 30 days AND have not been shown a tooltip in last 48 hours
- **Trigger**: User visits a page where the feature is accessible
- **Copy**: Benefit-first, under 15 words. End with a verb: "Export this view as a spreadsheet" / "Filter results by date range" / "Share this dashboard with your team"
- **CTA**: Single button that activates or navigates to the feature
- **Frequency**: Once per user per feature. Never show the same tooltip twice.
- **Priority**: If a user qualifies for multiple tooltips, show the one for the feature with the highest predicted value (most used by similar users who adopted it)

### 3. Build the performance monitoring layer

Run the `tooltip-performance-monitor` drill to create:

- Per-tooltip conversion funnel (impression -> click -> trial -> adoption)
- Tooltip performance dashboard with CTR, adoption rate, dismissal rate, and adoption lift panels
- Weekly health report comparing each tooltip's performance
- Automated alerts for tooltips with CTR < 10% or dismissal rate > 60%

### 4. Evaluate against threshold

After 2 weeks of always-on delivery:

- **Primary metric**: Aggregate tooltip CTR across all tooltips. Threshold: >=40%.
- **Primary metric**: Sustained adoption rate (users who click and then use the feature 3+ times in 7 days / total clickers). Threshold: >=12%.
- **Guard metric**: Dismissal rate below 50% on every tooltip.
- **Diagnostic**: Rank tooltips by adoption rate. Identify the top performer and the bottom performer. Understand why they differ (copy quality, feature value, targeting accuracy, page context).

If PASS (>=40% CTR AND >=12% adoption): Proceed to Scalable. Carry forward the top-performing tooltip patterns.
If FAIL: Rewrite underperforming tooltip copy, adjust targeting criteria, or replace low-value features with higher-value targets. Re-run for another 2-week cycle.

## Time Estimate

- 3 hours: Event tracking expansion with PostHog
- 5 hours: Configure 3-5 tooltips in Intercom with audience rules
- 4 hours: Build performance monitoring dashboard and alerts
- 4 hours: 2-week monitoring + evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, dashboards | Free up to 1M events/mo (https://posthog.com/pricing) |
| Intercom | In-app tooltip delivery and targeting | From $39/seat/mo with Engage add-on (https://www.intercom.com/pricing) |
| n8n | Scheduled performance reporting | Free self-hosted or from $24/mo cloud (https://n8n.io/pricing) |

## Drills Referenced

- `posthog-gtm-events` -- expand tooltip and feature usage event tracking
- `feature-announcement` -- configure each Intercom tooltip with targeting rules
- `tooltip-performance-monitor` -- build the measurement dashboard and weekly health reports
