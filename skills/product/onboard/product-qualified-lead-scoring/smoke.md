---
name: product-qualified-lead-scoring-smoke
description: >
  PQL Scoring System — Smoke Test. Define a product-qualified lead scoring model
  based on in-product usage signals, instrument tracking, manually score 20+ users,
  and verify the top 20% of scores correlate with actual conversion behavior.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "PQL model defined, 20+ users scored, top-20% scored users convert at ≥2x the rate of bottom-50%"
kpis: ["PQL identification rate", "Score-to-conversion correlation", "False positive rate"]
slug: "product-qualified-lead-scoring"
install: "npx gtm-skills add product/onboard/product-qualified-lead-scoring"
drills:
  - lead-score-model-setup
  - posthog-gtm-events
  - threshold-engine
---

# PQL Scoring System — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

A documented PQL scoring model with specific product-usage criteria and point values. 20+ active users scored and tiered in Attio. The top-20% scored users (Hot tier) convert to paid or book a sales call at >=2x the rate of bottom-50% scored users. You have PostHog events logging every score computation for later analysis.

## Leading Indicators

- All product-usage events referenced in the scoring model fire correctly in PostHog (verify via Live Events)
- 20+ users have `lead_scored` events in PostHog with non-null fit and intent scores
- Score distribution shows meaningful spread: not all users clustered in one tier
- At least 3 different intent signals contribute non-zero points across the scored population

## Instructions

### 1. Instrument product usage events in PostHog

Run the `posthog-gtm-events` drill to define and implement the event taxonomy for PQL-relevant product actions. At minimum, instrument these events:

- `signup_completed` — user finishes account creation
- `onboarding_step_completed` — user completes each onboarding milestone (attach `step_name`, `step_number` properties)
- `core_feature_used` — user performs the product's primary value action (attach `feature_name` property)
- `pricing_page_viewed` — user visits the pricing or upgrade page
- `invite_sent` — user invites a teammate
- `integration_connected` — user connects an external tool
- `export_performed` — user exports data (signals production use)
- `session_started` — standard session tracking with `session_number` property

Verify all events fire by creating a test account and walking through each action. Check PostHog Live Events to confirm.

### 2. Design the PQL scoring model

Run the `lead-score-model-setup` drill, adapting it for product-usage signals instead of marketing signals. Define two scoring dimensions:

**Fit Score (0-50 points) — who the user is:**

| Fit Criterion | Condition | Points |
|---------------|-----------|--------|
| Company size | 10-1000 employees (ICP sweet spot) | +15 |
| Buyer role | Decision-maker or technical lead title | +15 |
| Industry | Target industry match | +10 |
| Work email | Uses company domain (not gmail/hotmail) | +10 |

Enrich users via Clay to populate firmographic data. Use the `clay-enrichment-waterfall` fundamental referenced by `lead-score-model-setup`.

**Intent Score (0-50 points) — what the user does in-product:**

| Intent Signal | Condition | Points |
|---------------|-----------|--------|
| Activation depth | Completed 3+ onboarding steps | +15 |
| Core feature usage | Used primary feature 3+ times in 7 days | +15 |
| Pricing page visit | Viewed pricing page at least once | +10 |
| Team signal | Invited at least 1 teammate | +5 |
| Integration signal | Connected at least 1 integration | +5 |

**Composite PQL Score:** `fit_score + intent_score` (0-100)
**Tiers:** Hot (>=70), Warm (>=40), Cold (<40)

**Human action required:** Review the scoring criteria with your product and sales teams. Confirm that the intent signals genuinely predict buying behavior based on historical closed deals. Adjust point values if your product has different high-value actions.

### 3. Score 20+ users manually

For each of the 20+ most recent active users:

1. Pull firmographic data from Clay enrichment. Compute fit score.
2. Query PostHog for their product-usage events over the last 14 days. Compute intent score.
3. Calculate composite PQL score and assign tier.
4. Write scores to Attio using the `attio-lead-scoring` fundamental (fit_score, intent_score, lead_score, lead_tier, last_scored).
5. Fire a `lead_scored` event in PostHog with all score components, tier, and `scoring_method: "manual"`.

### 4. Validate score-to-conversion correlation

Run the `threshold-engine` drill to evaluate. Pull the scored users and check their actual conversion behavior (upgraded to paid, booked a sales call, or entered a deal in Attio). Measure:

- **Primary threshold:** Top-20% scored users (Hot tier) convert at >=2x the rate of bottom-50% (Cold tier).
- **Score distribution:** 15-30% Hot, 25-45% Warm, 30-50% Cold. If distribution is skewed, adjust tier thresholds.
- **False positive check:** <25% of Hot-tier users show zero engagement after scoring (they should be your most active users).

If PASS: The model distinguishes high-intent users. Proceed to Baseline.

If FAIL on correlation: The scoring criteria do not predict conversion. Re-examine which product actions actually correlate with purchases by querying PostHog for events of users who converted in the last 90 days vs. those who did not. Rebuild the intent criteria based on observed differences.

If FAIL on distribution: Thresholds are miscalibrated. Adjust tier boundaries until the distribution matches the target ranges.

## Time Estimate

- 1 hour: Instrument product events in PostHog and verify
- 1.5 hours: Design scoring model (fit + intent criteria, point values)
- 1.5 hours: Score 20+ users manually, write to Attio and PostHog
- 1 hour: Validate score distribution and conversion correlation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Product event tracking, user behavior queries | Free up to 1M events/month; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Clay | User firmographic enrichment for fit scoring | Free 100 credits/month; Pro $149/month ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Store PQL scores and tiers on contact records | Free for small teams; Pro $29/seat/month ([attio.com/pricing](https://attio.com/pricing)) |

## Drills Referenced

- `lead-score-model-setup` — designs the fit + intent scoring model, assigns point values, and manually scores an initial batch
- `posthog-gtm-events` — defines the event taxonomy and instruments product-usage tracking in PostHog
- `threshold-engine` — evaluates pass/fail against the 2x conversion correlation threshold
