---
name: feature-discovery-tooltips-smoke
description: >
  Contextual Feature Tooltips — Smoke Test. Deploy a single in-app tooltip targeting one
  underused feature, measure click-through, and validate that contextual nudges drive
  feature discovery.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=30% tooltip CTR on >=50 impressions"
kpis: ["Tooltip CTR", "Feature first-use rate", "Dismissal rate"]
slug: "feature-discovery-tooltips"
install: "npx gtm-skills add product/retain/feature-discovery-tooltips"
drills:
  - onboarding-flow
  - threshold-engine
---

# Contextual Feature Tooltips — Smoke Test

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

One tooltip targeting one underused feature achieves >=30% CTR on at least 50 impressions. This proves that contextual in-app nudges can drive feature discovery for your product and user base.

## Leading Indicators

- Tooltip impressions accumulating (Intercom message shown events in PostHog)
- Click events firing within minutes of first deployment
- Dismissal rate below 50% (users are not annoyed)
- At least some users who click the tooltip go on to use the feature

## Instructions

### 1. Identify the target feature

Query PostHog for features with low adoption but high value. Run this PostHog insight:

```
Event: feature_used
Breakdown: feature_name
Date range: last 30 days
```

Rank features by: (total active users) minus (users who used this feature). Pick the feature with the largest gap where the feature is accessible from a page users already visit frequently. Do NOT pick a feature that requires setup or configuration -- pick one that works with a single click or interaction.

### 2. Build the tooltip

Run the `onboarding-flow` drill to configure a single Intercom in-app tooltip:

- **Target element**: CSS selector of the UI element for the chosen feature
- **Trigger**: Show when user visits the page where the feature lives AND has not used the feature in the last 30 days AND has been active for at least 7 days
- **Copy**: One sentence, benefit-first. Example: "Export this view as a spreadsheet in one click." NOT "Did you know about CSV export?"
- **CTA**: "Try it" -- the button should activate the feature or navigate directly to it
- **Frequency**: Show once per user. If dismissed, do not show again.
- **Audience**: All active users who have not used this feature (use Intercom user properties to filter)

### 3. Instrument tracking in PostHog

Log these events via PostHog SDK or Intercom-to-PostHog forwarding:

```javascript
posthog.capture('tooltip_shown', { feature: 'csv-export', tooltip_id: 'smoke-v1' });
posthog.capture('tooltip_cta_clicked', { feature: 'csv-export', tooltip_id: 'smoke-v1' });
posthog.capture('tooltip_dismissed', { feature: 'csv-export', tooltip_id: 'smoke-v1' });
```

Also track downstream feature usage:
```javascript
posthog.capture('feature_used', { feature: 'csv-export', source: 'tooltip' });
```

**Human action required:** Deploy the Intercom tooltip to production. Verify it renders correctly on the target page by testing with a user account that matches the audience criteria.

### 4. Run for 1 week and evaluate

Let the tooltip run for 7 days or until it accumulates 50+ impressions, whichever comes first.

Run the `threshold-engine` drill to evaluate:

- **Primary metric**: Tooltip CTR (clicks / impressions). Threshold: >=30%.
- **Secondary metric**: Feature first-use rate (users who used the feature within 24 hours of clicking / total clickers). No threshold for Smoke, but record this -- it becomes the Baseline target.
- **Guard metric**: Dismissal rate. If >70%, the tooltip is poorly targeted or poorly written.

If PASS (>=30% CTR): Proceed to Baseline. Record the feature first-use rate as the benchmark.
If FAIL (<30% CTR): Rewrite the copy (try a different benefit angle), change the trigger timing, or pick a different target feature. Re-run.

## Time Estimate

- 1 hour: Feature gap analysis in PostHog
- 1.5 hours: Tooltip configuration in Intercom + PostHog event setup
- 0.5 hours: Deploy and verify
- 2 hours: Monitor over the week + final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Track tooltip events and feature usage | Free up to 1M events/mo (https://posthog.com/pricing) |
| Intercom | Deliver in-app tooltips | From $39/seat/mo, tooltips require Engage add-on (https://www.intercom.com/pricing) |

## Drills Referenced

- `onboarding-flow` -- configure the Intercom tooltip and PostHog tracking
- `threshold-engine` -- evaluate CTR against the >=30% pass threshold
