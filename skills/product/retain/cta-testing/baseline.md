---
name: cta-testing-baseline
description: >
  CTA Optimization -- Baseline Run. Run the first always-on A/B test on the weakest CTA surface.
  Deploy a single variant behind a PostHog feature flag, measure for statistical significance,
  and ship the winner. Proves that systematic CTA testing produces measurable lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=15% CTR lift on the target CTA surface with 95% statistical significance"
kpis: ["CTA CTR lift (variant vs control)", "Statistical significance", "Conversion rate impact", "Time to significance"]
slug: "cta-testing"
install: "npx gtm-skills add product/retain/cta-testing"
drills:
  - cta-variant-pipeline
  - cta-conversion-monitor
  - threshold-engine
---

# CTA Optimization -- Baseline Run

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

One CTA surface has been optimized through a rigorous A/B test. The winning variant is shipped to 100% of users. You have a documented, repeatable process for CTA experimentation and a measured CTR lift of >= 15% on the target surface.

## Leading Indicators

- PostHog experiment shows diverging CTR curves between control and variant within the first 5 days
- Variant accumulates 200+ impressions in the first week (sufficient traffic for the test to converge)
- No negative impact on secondary metrics (conversion rate, page bounce rate) from the variant

## Instructions

### 1. Generate and deploy the first CTA variant

Run the `cta-variant-pipeline` drill targeting the weakest CTA surface identified in Smoke. The drill will:

1. Audit the target surface's current performance (CTR, conversion rate, device breakdown)
2. Generate 3-5 variant hypotheses ranked by expected impact / risk
3. Deploy the top variant behind a PostHog feature flag (50/50 split)
4. Configure the PostHog experiment with `cta_clicked` as the primary metric

Select a single-variable change for the first test. Recommended first tests by impact potential:
- **Copy change:** replace vague CTA text with outcome-specific text (highest expected lift, lowest risk)
- **Commitment reduction:** lower the perceived effort (e.g., "Book a demo" -> "Watch 90-second video")
- **Social proof addition:** add a user count or logo bar near the CTA

**Human action required:** Review the variant hypothesis and approve before the experiment goes live. Deploy the feature flag code that renders the variant based on the PostHog flag value.

### 2. Monitor the experiment

Run the `cta-conversion-monitor` drill to track the experiment in real time. The monitor will:

1. Track per-variant CTR and conversion rate daily
2. Alert if the variant performs > 30% worse than control after 3 days with 100+ samples (auto-revert signal)
3. Track secondary metrics: conversion rate (clicks that become completions) and page bounce rate

Do not stop the experiment early based on initial results. Let it run for the planned duration (minimum 7 days or until PostHog reports 95% significance, whichever is longer). Early stopping inflates false positive rates.

### 3. Decide and ship

When the experiment reaches significance or the 2-week window closes:

- **Significant winner:** Roll the winning variant to 100% via the PostHog feature flag API. Remove the experiment code path. Log the result: hypothesis, variant, sample size, CTR lift, confidence level.
- **No significant difference:** The variants perform equivalently. Keep the control (simpler). Queue a bigger change -- the first variant was too subtle.
- **Variant lost:** Revert to control. Document why the hypothesis was wrong. This learning is valuable.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against: >= 15% CTR lift on the target surface with 95% statistical significance.

If PASS: document the winning variant, the measured lift, and proceed to Scalable. You have proven that CTA testing produces real gains.

If FAIL (test completed but lift < 15% or not significant): diagnose. Common causes:
- Variant change was too subtle (test a bigger change)
- Insufficient traffic (the surface needs more impressions -- pick a higher-traffic surface)
- Wrong variable (copy was fine; the problem is placement or timing)

Re-run Baseline with a different variant or different target surface.

## Time Estimate

- 3 hours: audit target surface, generate hypotheses, select variant, deploy feature flag
- 1 hour: configure PostHog experiment and verify tracking
- 0 hours: 2-week experiment run (passive monitoring)
- 2 hours: monitor experiment health, check for guardrail breaches
- 3 hours: analyze results, make decision, ship or revert, document learnings
- 3 hours: buffer for variant implementation in product code

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, event tracking, funnels | Free tier: 1M events/mo, 1M flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `cta-variant-pipeline` -- generates variant hypotheses, deploys them behind feature flags, and provides the decision framework for shipping or reverting
- `cta-conversion-monitor` -- monitors the experiment in real time with daily per-variant tracking and guardrail alerts
- `threshold-engine` -- evaluates whether the >= 15% CTR lift threshold is met and recommends next action
