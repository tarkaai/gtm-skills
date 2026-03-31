---
name: feature-discovery-tooltips-scalable
description: >
  Contextual Feature Tooltips — Scalable Automation. Automated tooltip targeting across
  all user segments with usage-based personalization, A/B-tested copy, and segment-specific
  delivery rules serving 500+ users without manual intervention.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=35% CTR across 500+ unique users AND >=15% sustained adoption"
kpis: ["Tooltip CTR at scale", "Sustained adoption rate", "Segment-specific adoption", "Tooltip fatigue index", "Feature coverage ratio"]
slug: "feature-discovery-tooltips"
install: "npx gtm-skills add product/retain/feature-discovery-tooltips"
drills:
  - tooltip-targeting-automation
  - ab-test-orchestrator
  - feature-adoption-monitor
---

# Contextual Feature Tooltips — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Automated tooltip delivery across all user segments -- new, established, and power users -- each receiving personalized tooltips based on their individual feature gap. System serves 500+ unique users per month with >=35% CTR and >=15% sustained adoption rate. No manual tooltip selection or targeting required.

## Leading Indicators

- Daily tooltip impressions growing as new users enter eligibility automatically
- Per-segment CTR within 10% of aggregate CTR (no single segment dragging average down)
- A/B test velocity: at least 2 tooltip copy experiments completed per month
- Feature coverage ratio increasing (percentage of features with active tooltips)
- Tooltip fatigue index stable (sequential dismissal rate below 30%)

## Instructions

### 1. Deploy automated tooltip targeting

Run the `tooltip-targeting-automation` drill to build the personalized delivery system:

1. **Feature usage matrix**: Query PostHog for every user's feature usage pattern. For each user, compute the feature gap -- features used by similar users but not by this user.

2. **Eligibility cohorts**: Create PostHog cohorts for each feature tooltip with these rules:
   - Has NOT used the feature in 30 days
   - HAS used at least 2 prerequisite features
   - Active in last 7 days
   - Not shown a tooltip in last 48 hours
   - Has not dismissed this tooltip before

3. **Daily targeting pipeline**: Build an n8n workflow (daily cron) that:
   - Queries PostHog for eligible users per tooltip
   - Ranks features by predicted impact per user (collaborative filtering: features adopted by similar users)
   - Selects the single highest-priority tooltip per user
   - Updates Intercom user properties: `next_tooltip_feature`, `tooltip_priority_score`

4. **Segment-specific strategies**:
   - New users (0-14 days active): Prioritize core features that correlate with activation
   - Established users (14-60 days): Prioritize intermediate features that correlate with retention
   - Power users (60+ days): Prioritize advanced features that correlate with expansion

### 2. A/B test tooltip copy and timing

Run the `ab-test-orchestrator` drill to systematically test tooltip variations:

**Test 1 -- Copy style**: For each tooltip, test two copy variants:
- Variant A: Benefit statement ("Export this view as a spreadsheet in one click")
- Variant B: Social proof ("Teams export 500+ reports/week with this")
- Use PostHog feature flags to split users 50/50 per tooltip

**Test 2 -- Trigger timing**: Test when to show the tooltip:
- Variant A: Immediately when user visits the page
- Variant B: After 10 seconds on the page
- Variant C: After user completes a related action on the page

**Test 3 -- CTA design**: Test the call-to-action:
- Variant A: "Try it" button
- Variant B: "Show me" button that highlights the feature with an animation
- Variant C: No button -- clicking anywhere on the tooltip activates the feature

Run each test for statistical significance (minimum 200 impressions per variant). Log all experiment results in PostHog.

### 3. Build the feature adoption monitoring layer

Run the `feature-adoption-monitor` drill to track how tooltip-driven discovery translates to sustained usage:

- Build adoption funnels per feature: tooltip shown -> clicked -> first use -> 3 uses in 7 days -> 10 uses in 30 days
- Create tier transition velocity metrics: how quickly do users move from "never used" to "regular user" for each feature
- Configure stalled-user detection: users who clicked a tooltip but never adopted the feature get a follow-up Intercom message after 7 days with a different angle or a help article link
- Build the feature adoption dashboard showing tooltip-driven vs organic adoption rates side by side

### 4. Evaluate against threshold

After 2 months of automated delivery:

- **Primary**: Aggregate CTR across 500+ unique users. Threshold: >=35%.
- **Primary**: Sustained adoption rate (3+ uses in 7 days post-click). Threshold: >=15%.
- **Secondary**: Per-segment CTR variance. No segment should be more than 15 percentage points below the aggregate.
- **Secondary**: Feature coverage ratio -- percentage of discoverable features with active tooltips. Target: >=60%.
- **Guard**: Tooltip fatigue index (sequential dismissal rate). Must remain below 30%.

If PASS: Proceed to Durable. The system is delivering personalized tooltips at scale.
If FAIL: Diagnose by segment. If one segment underperforms, adjust that segment's targeting rules or copy. If fatigue is high, reduce frequency or raise the priority threshold. Re-run for another month.

## Time Estimate

- 15 hours: Tooltip targeting automation setup (n8n pipeline, PostHog cohorts, Intercom properties)
- 15 hours: A/B test design, implementation, and analysis (3 test cycles)
- 15 hours: Feature adoption monitoring layer
- 15 hours: 2-month monitoring, optimization, and evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, cohorts, experiments, dashboards | Free up to 1M events/mo; paid from $0.00031/event (https://posthog.com/pricing) |
| Intercom | In-app tooltip delivery, targeting, user properties | From $39/seat/mo with Engage add-on (https://www.intercom.com/pricing) |
| n8n | Daily targeting pipeline and reporting automation | Free self-hosted or from $24/mo cloud (https://n8n.io/pricing) |

## Drills Referenced

- `tooltip-targeting-automation` -- build the automated per-user tooltip selection and delivery pipeline
- `ab-test-orchestrator` -- run A/B tests on tooltip copy, timing, and CTA design
- `feature-adoption-monitor` -- track tooltip-driven feature adoption and detect stalled users
