---
name: personal-usage-analytics-smoke
description: >
  Personal Usage Analytics — Smoke Test. Build a minimal user-facing analytics surface showing
  personal usage stats to a test group. Validate that users view their stats and return to the product.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: "≥50% analytics view rate among test group (10-50 users) within 7 days"
kpis: ["Analytics view rate", "Time on analytics surface", "Return visit within 48 hours"]
slug: "personal-usage-analytics"
install: "npx gtm-skills add product/retain/personal-usage-analytics"
drills:
  - posthog-gtm-events
  - threshold-engine
---

# Personal Usage Analytics — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Pass threshold: at least 50% of a 10-50 user test group views the analytics surface within 7 days of it going live, and at least 30% of viewers return to the product within 48 hours of viewing their stats.

This proves that users will actually look at their own usage data when you put it in front of them, and that seeing it creates a return signal.

## Leading Indicators

- Users click the Intercom discovery prompt (prompt-to-view conversion rate)
- Users spend more than 15 seconds on the analytics surface (not a bounce)
- Users click at least one metric card (engagement depth)
- Users who view analytics have a higher 48-hour return rate than non-viewers

## Instructions

### 1. Set up event tracking for the analytics surface

Run the `posthog-gtm-events` drill to instrument the following events:

- `usage_analytics_page_viewed` — user opened the analytics surface
- `usage_analytics_metric_clicked` — user clicked a specific metric card (property: `metric_name`)
- `usage_analytics_cta_clicked` — user clicked the call-to-action (property: `cta_type`)
- `usage_analytics_time_spent` — duration on the analytics surface in seconds

Also verify that the core product usage events you plan to surface (e.g., projects created, automations run, queries executed) are already tracked in PostHog. If not, instrument them first.

### 2. Build the minimal analytics surface

Run the the usage analytics surface build workflow (see instructions below) drill. For the Smoke Test, simplify to the minimum viable version:

- Select 3 metrics that grow with usage and imply value (e.g., total projects created, actions completed this week, time saved)
- Build a simplified n8n aggregation workflow that runs daily for the test group only
- Design the analytics surface with: a headline stat, 3 metric cards with sparklines, and one CTA

**Human action required:** A developer must implement the frontend component. Provide them the data schema, layout spec, and PostHog event names from the drill output. Scope this to a feature-flagged page accessible only to the test group.

### 3. Launch to a test group of 10-50 users

Use PostHog feature flags to enable the analytics surface for 10-50 active users. Select users who have been active for at least 14 days (enough data for meaningful stats). Set up one Intercom in-app message to notify the test group: "See how you use [Product] — your personal stats are now available."

### 4. Measure against threshold

Run the `threshold-engine` drill after 7 days. Query PostHog for:

- **View rate**: unique users who fired `usage_analytics_page_viewed` / test group size. Pass: ≥50%.
- **Engagement depth**: users who fired `usage_analytics_metric_clicked` / users who viewed. Target: ≥30%.
- **Return signal**: users who had a product session within 48 hours of viewing analytics / users who viewed. Target: ≥30%.

If PASS: the analytics surface drives views and return visits. Proceed to Baseline.

If FAIL: diagnose via PostHog. If view rate is low, the discovery prompt is the problem — test different copy, placement, or timing. If engagement depth is low, the metrics displayed are not interesting — survey 5 test users to learn what stats they actually want to see. If return signal is low, the CTA is not motivating — test different CTA types.

## Time Estimate

- 2 hours: event tracking setup and verification
- 3 hours: analytics surface build (drill execution + developer handoff)
- 1 hour: test group selection and Intercom prompt setup
- 2 hours: threshold evaluation and diagnosis after 7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, funnels | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | Discovery prompt in-app messages | From $39/mo — https://www.intercom.com/pricing |
| n8n | Daily aggregation workflow | Free self-hosted or from $24/mo cloud — https://n8n.io/pricing |

**Estimated play-specific cost:** $0 (covered by standard stack)

## Drills Referenced

- the usage analytics surface build workflow (see instructions below) — builds the user-facing analytics surface with metrics, aggregation pipeline, and discovery prompts
- `posthog-gtm-events` — instruments the event taxonomy for tracking analytics surface interactions
- `threshold-engine` — evaluates pass/fail against the 50% view rate threshold
