---
name: product-qualified-lead-scoring-scalable
description: >
  PQL Scoring System — Scalable Automation. A/B test scoring thresholds and
  weights, auto-calibrate the model against actual outcomes, and scale PQL
  routing to handle 500+ users/month while maintaining ≥65% scoring accuracy.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 6 weeks"
outcome: "Scoring accuracy ≥65% at 500+ users/month with auto-calibrating weights and segmented routing"
kpis: ["Scoring accuracy at volume (≥65% of converters pre-identified)", "PQL-to-meeting conversion rate", "False positive rate (<20%)", "False negative rate (<10%)", "Model calibration frequency"]
slug: "product-qualified-lead-scoring"
install: "npx gtm-skills add product/onboard/product-qualified-lead-scoring"
drills:
  - ab-test-orchestrator
  - engagement-alert-routing
---

# PQL Scoring System — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

PQL scoring handles 500+ new users per month with no manual intervention. Scoring model self-calibrates monthly: dimension weights adjust based on actual churn and conversion outcomes. A/B tests on scoring thresholds and routing rules have been run and winners implemented. Segmented routing delivers different PQL experiences based on account value and user behavior patterns. Scoring accuracy remains >=65% (at least 65% of users who convert were pre-identified as Hot or Warm).

## Leading Indicators

- Monthly scoring volume exceeds 500 users with no pipeline errors or timeouts
- At least 2 A/B tests completed on scoring parameters (thresholds, weights, or routing rules)
- Weight tuning pipeline runs monthly and produces measurable accuracy changes
- Segmented routing delivers different interventions to high-value vs low-value PQLs
- False positive rate trends downward month over month

## Instructions

### 1. Run A/B tests on scoring thresholds

Run the `ab-test-orchestrator` drill to test whether adjusting PQL tier thresholds improves conversion identification. Design three experiments:

**Experiment 1 — Tier threshold test:**
- Control: Hot >= 70, Warm >= 40 (current thresholds from Baseline)
- Variant: Hot >= 60, Warm >= 35 (lower thresholds — captures more PQLs at the cost of precision)
- Success metric: PQL-to-meeting conversion rate. If variant produces more meetings without degrading conversion rate by >15%, adopt it.
- Use `posthog-experiments` to split new users 50/50. Run for 4 weeks or until 200+ users per variant.

**Experiment 2 — Intent signal weighting:**
- Control: All intent signals weighted equally (current model)
- Variant: Double the weight of `core_feature_used` and `invite_sent` signals, halve the weight of `pricing_page_viewed`
- Hypothesis: Feature usage and team invites are stronger buying signals than pricing page views for product-led companies.
- Success metric: Scoring accuracy (% of converters correctly pre-identified).

**Experiment 3 — Engagement score integration:**
- Control: Engagement score adds a flat +10/-10 bonus to intent score
- Variant: Engagement score replaces recency as a full scoring dimension at 20% weight
- Success metric: False negative rate (fewer missed converters).

For each experiment: set up the PostHog feature flag, implement the variant in the n8n scoring workflow (branch logic based on flag), run for statistical significance, evaluate with the `experiment-evaluation` fundamental, and implement the winner.

### 2. Auto-calibrate scoring weights monthly

Run the the engagement score weight tuning workflow (see instructions below) drill to build the monthly recalibration pipeline:

1. Build the outcome-labeled dataset: for every user scored 60+ days ago, label them as Churned, Expanded, Retained, or Declined based on current Attio status and PostHog activity.
2. Measure each scoring dimension's predictive power by computing separation scores (churn rate in bottom quartile minus top quartile).
3. Recompute optimal weights proportional to each dimension's separation score, constrained so no dimension exceeds 40% or falls below 10%.
4. Back-test the new weights against historical data. Only adopt if accuracy improves by >=5 percentage points.
5. Log every weight change in Attio with before/after weights, separation scores, and accuracy deltas.
6. When the model plateaus (no improvement for 2 consecutive months), use `hypothesis-generation` to diagnose: missing behavioral signals, product changes that invalidated existing signals, or user base composition shifts.

Schedule this pipeline via n8n cron on the 1st of each month.

### 3. Scale PQL routing with segmentation

Run the `engagement-alert-routing` drill to build tiered routing that matches intervention intensity to account value and behavior pattern:

**High-value PQLs (MRR potential >$500 based on company size and plan):**
- Hot tier: Create deal in Attio, immediate Slack alert to account exec, auto-draft a personalized outreach email referencing the user's top 3 product actions.
- Warm with rising engagement: Add to high-touch nurture sequence via Loops (bi-weekly product tips customized to their feature usage).

**Mid-value PQLs (MRR potential $100-$500):**
- Hot tier: Create deal in Attio, assign to SDR, send in-app Intercom message offering a quick call.
- Warm with rising engagement: Add to standard nurture sequence via Loops.

**Low-value PQLs (MRR potential <$100 or free-tier):**
- Hot tier: Send in-app Intercom message with self-serve upgrade prompt. No human routing.
- Warm: Automated email sequence only.

Build n8n routing logic that reads company size and plan from Attio, maps to value tier, and dispatches to the correct channel. Track routing effectiveness: conversion rate by value tier and intervention type.

### 4. Evaluate at scale

After 6 weeks with 500+ users scored:

- **Primary threshold:** >=65% of users who converted were scored Hot or Warm before conversion.
- **False positive rate:** <20% of Hot-tier users never engage with sales or upgrade.
- **False negative rate:** <10% of converters were scored Cold.
- **Pipeline health:** Zero scoring workflow errors in the last 7 days. All 4 n8n workflows executing on schedule.

If PASS: Model is calibrated, routing is segmented, volume is handled. Proceed to Durable.

If FAIL on accuracy: Review the monthly weight calibration output. If weights have not shifted meaningfully, the problem is likely missing intent signals — add new product events to the model.

If FAIL on false positives: Raise the Hot threshold or add a "confirmation signal" requirement (e.g., user must exhibit 2+ distinct intent signals, not just one high-value action).

## Time Estimate

- 12 hours: Design and run 3 A/B tests on scoring parameters
- 8 hours: Build monthly weight auto-calibration pipeline
- 10 hours: Implement segmented routing with value-tier logic
- 6 hours: Monitor pipeline health, evaluate accuracy, iterate
- 4 hours: Analyze test results and implement winners

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, event tracking | Free up to 1M events/month; paid ~$0.00005/event; Experiments from $0/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Scoring, routing, and calibration workflows | Self-hosted free; Cloud from EUR 24/month ([n8n.io/pricing](https://n8n.io/pricing)) |
| Clay | Ongoing firmographic enrichment at scale | Pro $149/month ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM: scoring, routing, deal management | Pro $29/seat/month ([attio.com/pricing](https://attio.com/pricing)) |
| Intercom | In-app PQL messages and upgrade prompts | Essential $39/seat/month ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Nurture email sequences by value tier | Starter $49/month ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic | Hypothesis generation for model plateau diagnosis | Pay-per-use ~$0.01-0.03/call ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on scoring thresholds and weights
- the engagement score weight tuning workflow (see instructions below) — monthly auto-calibration of scoring dimension weights against actual outcomes
- `engagement-alert-routing` — routes PQL alerts to the right intervention channel based on account value and risk tier
