---
name: ai-personalization-smoke
description: >
  AI Product Personalization — Smoke Test. Classify users by behavior and deliver one
  personalized in-app experience to prove engagement lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=40% of test group engages with the personalized surface"
kpis: ["Personalization surface engagement rate", "Personalized vs control retention at 7 days", "Surface dismissal rate"]
slug: "ai-personalization"
install: "npx gtm-skills add product/retain/ai-personalization"
drills:
  - user-behavior-segmentation
  - personalization-rule-engine
  - threshold-engine
---

# AI Product Personalization — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

At least 40% of users in the test group interact with the personalized surface (click, complete, or expand) within 7 days. This proves that segment-aware content outperforms the generic default enough to justify always-on automation.

## Leading Indicators

- Personalized surface impression count reaches expected volume (test group size x avg sessions)
- Surface engagement rate exceeds 25% within the first 3 days
- Dismissal rate stays below 40% (users are not annoyed by the personalization)
- At least 2 of the defined segments receive personalized surfaces (routing logic works)

## Instructions

### 1. Build behavioral segments from existing data

Run the `user-behavior-segmentation` drill. Focus on the minimum viable version:

1. Query PostHog for 21 days of per-user event data
2. Compute the three behavioral dimensions: primary workflow, session pattern, collaboration level
3. Classify users into 3-4 segments (keep it simple for smoke — expand later)
4. Store segment assignments as PostHog person properties
5. Validate: confirm each segment contains at least 10% of active users and no segment exceeds 50%

Do NOT build the full n8n daily pipeline yet. Run the segmentation as a one-time batch using the PostHog HogQL editor or a local script.

### 2. Configure one personalized surface per segment

Run the `personalization-rule-engine` drill. For the smoke test, pick ONE surface to personalize — the highest-traffic surface in your product (typically the dashboard or home screen). For each segment:

1. Create a PostHog feature flag `personalization-smoke-dashboard` with multivariate variants matching your segments
2. Design a variant per segment: different hero content, CTA, or highlighted feature
3. Set the flag to distribute based on the `behavior_segment` person property
4. Add a control variant that shows the current generic experience
5. Split: 70% personalized (routed to segment variant), 30% control (generic)

For the smoke test, limit in-app messaging to ONE Intercom message per segment. Keep email sequences out of scope.

**Human action required:** Review each variant's copy and design before launching. Verify the feature flag routing by testing with 2-3 internal users across different segments.

### 3. Instrument personalization events

Using PostHog custom events, track:
- `personalization_surface_shown` with properties `{surface: "dashboard", segment, variant, is_control}`
- `personalization_surface_engaged` when user clicks or interacts
- `personalization_surface_dismissed` when user closes or ignores

Verify events are firing correctly in PostHog Live Events before exposing to real users.

### 4. Launch to a small test group

Enable the feature flag for a test group of 50-200 users. Use a PostHog cohort to target users who have been active in the last 14 days and have a `behavior_segment` assigned. Let the test run for 7 days.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- Primary: engagement rate >= 40% in the personalized group
- Compare: personalized group engagement rate vs control group engagement rate
- Guard: dismissal rate < 40%

If PASS (>= 40% engagement AND personalized > control by >= 5pp), proceed to Baseline.
If FAIL, diagnose: which segments engaged vs which did not? Was the surface choice wrong? Was the variant content too subtle? Iterate on the weakest segment variant and re-run.

## Time Estimate

- 2 hours: behavioral segmentation batch run and validation
- 2 hours: feature flag setup, variant design, Intercom message creation, event instrumentation
- 1 hour: test group launch and monitoring setup
- 1 hour: 7-day evaluation and threshold analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | User analytics, feature flags, cohorts, custom events | Free tier: 1M events + 1M flag requests/mo. Paid: $0.00005/event. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages for segment-specific nudges | Essential: $29/seat/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated play-specific cost at Smoke:** $0 (within PostHog and Intercom free tiers for small test group)

## Drills Referenced

- `user-behavior-segmentation` — classify users into behavioral segments from PostHog data
- `personalization-rule-engine` — configure personalized surfaces and messages per segment
- `threshold-engine` — evaluate engagement rate against pass/fail threshold
