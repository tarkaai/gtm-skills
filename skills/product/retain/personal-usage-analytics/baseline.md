---
name: personal-usage-analytics-baseline
description: >
  Personal Usage Analytics — Baseline Run. Roll out the analytics surface to all users with
  engagement monitoring. First always-on deployment measuring view rate and retention lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥40% weekly analytics view rate across all active users AND ≥8pp 30-day retention lift for viewers vs. non-viewers"
kpis: ["Weekly analytics view rate", "Engagement depth (metric click rate)", "30-day retention lift (viewers vs. non-viewers)", "CTA conversion rate"]
slug: "personal-usage-analytics"
install: "npx gtm-skills add product/retain/personal-usage-analytics"
drills:
  - usage-analytics-engagement-monitor
  - feature-adoption-monitor
  - posthog-gtm-events
---

# Personal Usage Analytics — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Pass threshold: ≥40% of all active users view the analytics surface at least once per week, AND viewers show ≥8 percentage point higher 30-day retention than non-viewers.

This proves the analytics surface works at full user base scale and that looking at personal stats correlates with better retention.

## Leading Indicators

- View rate ramp: week 1 view rate (novelty) vs. week 3 view rate (sustainable interest)
- Engagement depth holds above 30% (users are not just glancing and leaving)
- Discovery prompt click-through rate stays above 10%
- Weekly email digest open rate (if enabled) stays above 25%
- CTA clicks translate into downstream product actions within 24 hours

## Instructions

### 1. Expand event tracking to full user base

Run the `posthog-gtm-events` drill to verify all analytics surface events are firing correctly at full scale. Ensure the daily n8n aggregation workflow (from `usage-analytics-surface-build` at Smoke level) handles the full user base without timeouts. If the workflow exceeds 5 minutes, partition by user cohort and run in parallel batches.

### 2. Roll out the analytics surface to all users

Remove the feature flag restricting the analytics surface to the test group. Enable it for all active users. Configure the discovery prompts from the `usage-analytics-surface-build` drill for the full audience:

- **First visit prompt**: Trigger for all users who have never viewed the analytics page and have 7+ days of activity
- **Weekly digest prompt**: Every Monday for users active in the last 7 days
- **Milestone prompt**: When n8n detects a user hit a new personal milestone

### 3. Build the engagement monitoring system

Run the `usage-analytics-engagement-monitor` drill. This creates:

- The analytics engagement funnel in PostHog (viewed -> clicked metric -> clicked CTA -> product action)
- Viewer vs. non-viewer retention comparison cohorts
- The 7-panel engagement dashboard with threshold alerts
- The weekly health report workflow in n8n

Pay special attention to the retention lift measurement. Compare viewer cohort 30-day retention against non-viewer cohort. This is the primary Baseline metric.

### 4. Track feature adoption from analytics CTAs

Run the `feature-adoption-monitor` drill configured for the features promoted by the analytics surface CTAs. Track whether the "have you tried [feature]" CTAs actually drive feature adoption. Measure: CTA shown -> feature first used within 7 days. If adoption rate from CTAs is below 5%, the CTA recommendations are too generic — personalize based on the user's actual usage patterns.

### 5. Evaluate against threshold after 3 weeks

Query PostHog at the end of week 3:

- **Weekly view rate**: unique users who fired `usage_analytics_page_viewed` in the last 7 days / total active users in the last 7 days. Pass: ≥40%.
- **Retention lift**: 30-day retention rate for the "analytics viewers" cohort minus the "non-viewers" cohort. Pass: ≥8 percentage points.

If PASS: the analytics surface drives engagement at scale. Proceed to Scalable to establish causal impact via A/B testing.

If FAIL on view rate: review discovery prompt performance. Which prompt type drives the most views? Test 2-3 new prompt variations (different copy, different trigger timing). Consider adding the weekly email digest if not yet enabled.

If FAIL on retention lift: the analytics surface is viewed but not impactful. Review engagement depth — if users bounce quickly, the stats shown are not valuable enough. Survey 10 active users to understand what usage data they would actually find motivating. Rebuild the metric selection.

## Time Estimate

- 3 hours: full-scale rollout and aggregation pipeline scaling
- 6 hours: engagement monitoring setup (drill execution + dashboard configuration)
- 4 hours: feature adoption tracking from CTAs
- 3 hours: weekly health report reviews (1 hour x 3 weeks)
- 4 hours: threshold evaluation, cohort analysis, and diagnosis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohort retention analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app discovery prompts, milestone notifications | From $39/mo — https://www.intercom.com/pricing |
| n8n | Daily aggregation workflow, weekly health report | Free self-hosted or from $24/mo cloud — https://n8n.io/pricing |
| Attio | Play health logging, optimization notes | From $29/seat/mo — https://attio.com/pricing |

**Estimated play-specific cost:** ~$50-100/mo (primarily n8n compute for daily aggregation at full user base)

## Drills Referenced

- `usage-analytics-engagement-monitor` — monitors view rates, engagement depth, retention lift, and generates weekly health reports
- `feature-adoption-monitor` — tracks whether analytics CTAs drive feature discovery and adoption
- `posthog-gtm-events` — verifies and maintains the event taxonomy at full scale
