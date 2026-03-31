---
name: cta-testing-smoke
description: >
  CTA Optimization -- Smoke Test. Instrument 5 in-product CTAs with PostHog event tracking,
  measure baseline click-through and conversion rates, and identify the weakest CTA surface
  for optimization. Proves you can measure CTA performance before investing in testing.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "5 CTAs instrumented with baseline CTR measured for each"
kpis: ["CTA CTR per surface", "CTA-to-conversion rate", "Impressions per surface"]
slug: "cta-testing"
install: "npx gtm-skills add product/retain/cta-testing"
drills:
  - posthog-gtm-events
  - lead-capture-surface-setup
  - threshold-engine
---

# CTA Optimization -- Smoke Test

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

5 in-product CTAs are instrumented with PostHog event tracking. You have baseline CTR and conversion rates for each surface. You know which CTA is the weakest performer and have enough data to form a testing hypothesis.

## Leading Indicators

- PostHog receives `cta_impression` and `cta_clicked` events within 1 hour of deploying tracking code
- At least 3 of 5 CTAs accumulate 50+ impressions within the first 3 days
- You can query per-surface CTR in PostHog and see meaningful variance between surfaces

## Instructions

### 1. Define the CTA event taxonomy

Run the `posthog-gtm-events` drill to establish a standard event schema for CTA interactions. Define these events:

| Event | Trigger | Required Properties |
|-------|---------|-------------------|
| `cta_impression` | CTA element enters the viewport | `page`, `surface_id`, `cta_text`, `surface_type`, `device_type` |
| `cta_clicked` | User clicks the CTA | `page`, `surface_id`, `cta_text`, `surface_type`, `device_type` |
| `cta_converted` | User completes the action the CTA leads to | `page`, `surface_id`, `cta_text`, `surface_type`, `conversion_type` |

The `surface_id` property is critical -- it uniquely identifies each CTA location (e.g., `pricing-page-hero`, `dashboard-upgrade-banner`, `settings-plan-cta`). This is how you will compare surfaces against each other.

### 2. Instrument 5 CTA surfaces

Run the `lead-capture-surface-setup` drill for each of 5 CTA surfaces in your product. For each surface:

1. Add an Intersection Observer that fires `cta_impression` when the CTA enters the viewport (fire once per page load, not on every scroll)
2. Add a click handler that fires `cta_clicked` with all properties
3. Track the downstream conversion event as `cta_converted` (form submission, upgrade initiation, feature activation, etc.)

Choose 5 CTAs that span different user journeys:
- **Activation CTA:** appears during onboarding or first-run experience
- **Upgrade CTA:** prompts plan upgrade (pricing page, usage limit banner, feature gate)
- **Engagement CTA:** drives deeper product usage (try a feature, complete a workflow)
- **Retention CTA:** appears to at-risk or dormant users (re-engagement prompt, value reminder)
- **Expansion CTA:** drives seat addition, team invite, or add-on purchase

**Human action required:** Deploy the tracking code to your product. Verify each of the 5 surfaces fires events correctly by checking PostHog Live Events.

### 3. Collect baseline data for 7 days

Let all 5 CTAs run for a full 7 days without changes. Do not modify CTA copy, placement, or visibility during this period. You need clean baseline data.

After 7 days, query PostHog for each surface:
- Total impressions
- Total clicks
- CTR = clicks / impressions
- Total conversions
- Conversion rate = conversions / impressions
- Device split (desktop vs mobile CTR)

### 4. Evaluate against threshold

Run the `threshold-engine` drill to verify: all 5 CTAs are instrumented and producing data. If any surface has < 10 impressions in 7 days, it is either broken (tracking issue) or too low-traffic to optimize (replace it with a higher-traffic surface).

Rank all 5 surfaces by CTR. The lowest-performing surface with sufficient traffic (50+ weekly impressions) is your first optimization target for Baseline.

Document:
- Baseline CTR and conversion rate per surface
- The optimization target surface and its current metrics
- 2-3 hypotheses for why the target surface underperforms (copy too vague, placement below the fold, wrong audience, etc.)

If PASS (5 CTAs measured with baseline data), proceed to Baseline. If FAIL (tracking broken or insufficient traffic), fix instrumentation and re-run.

## Time Estimate

- 2 hours: define event taxonomy and implement tracking code for 5 surfaces
- 0.5 hours: verify events in PostHog Live Events
- 0 hours: 7-day data collection (passive)
- 1.5 hours: query results, compute baselines, rank surfaces, document findings
- 1 hour: buffer for debugging tracking issues

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, baseline measurement | Free tier: 1M events/mo, 1M feature flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `posthog-gtm-events` -- establishes the event taxonomy so all CTA events follow a consistent naming scheme
- `lead-capture-surface-setup` -- provides the implementation pattern for deploying tracking on each CTA surface
- `threshold-engine` -- evaluates whether the 5-CTA instrumentation threshold is met and recommends next action
