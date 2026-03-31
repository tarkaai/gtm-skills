---
name: usage-based-pricing-smoke
description: >
  Consumption-Based Pricing — Smoke Test. Analyze product usage data to identify the optimal value
  metric and tier structure, then validate with a small cohort before committing to a pricing change.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Identified value metric with ≥2x retention correlation between high and low usage bands"
kpis: ["Value metric correlation to retention", "Usage distribution percentiles", "Churn rate by usage band"]
slug: "usage-based-pricing"
install: "npx gtm-skills add product/upsell/usage-based-pricing"
drills:
  - usage-pricing-model-analysis
  - posthog-gtm-events
---

# Consumption-Based Pricing — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

A validated value metric (the unit customers pay for) backed by data showing that high-usage users retain at 2x+ the rate of low-usage users. A documented usage distribution with percentile breakpoints that define where tier boundaries should sit. Three modeled pricing scenarios (per-unit, tiered, hybrid) with projected revenue and churn impact.

This is an analysis play — no pricing changes ship at Smoke. The agent runs the analysis, a human decides whether to proceed.

## Leading Indicators

- Usage event coverage: all candidate value metrics are instrumented in PostHog (API calls, seats, storage, messages, etc.)
- Retention curve divergence: at least one candidate metric shows a clear separation between high and low usage cohorts
- Usage distribution has identifiable cluster boundaries or natural breakpoints that map to tier thresholds

## Instructions

### 1. Instrument usage events in PostHog

Run the `posthog-gtm-events` drill to ensure every candidate value metric emits events. For each metered resource your product tracks (API calls, seats, projects, storage, messages, integrations), verify that PostHog receives `resource_consumed` events with properties: `account_id`, `resource_type`, `current_count`, `plan_tier`.

If any candidate metrics are missing, instrument them before proceeding. The analysis cannot run on incomplete data.

### 2. Run the usage pricing model analysis

Run the `usage-pricing-model-analysis` drill. This executes the full analysis pipeline:

1. **Identify the value metric:** Query PostHog for all candidate usage events over the past 90 days. Cross-reference with Stripe billing data to find which usage event has the strongest positive correlation with retention and expansion revenue. Build retention curves segmented by each candidate metric using PostHog retention analysis.

2. **Map the usage distribution:** Query the value metric distribution across all active customers. Identify P25, P50, P80, P95 percentiles. Look for natural cluster boundaries that suggest tier breakpoints.

3. **Analyze churn by usage band:** Create PostHog cohorts for each usage quartile plus a P95+ power user band. Compute 30-day and 90-day churn rates per band. Identify bands where churn is highest and assess whether price is the cause.

4. **Model three pricing scenarios:** Per-unit, tiered (graduated), and hybrid (base + overage). For each model, compute revenue at current usage levels, revenue change vs. current pricing, number of customers who would pay more vs. less, and projected churn impact.

5. **Validate willingness to pay:** Check PostHog for behavioral price sensitivity signals — pricing page visits by active customers, users hitting plan limits without upgrading, trial-to-paid drop-off at payment step.

6. **Document the recommendation:** Produce a pricing analysis report with the recommended value metric, pricing model, tier boundaries, expected revenue and churn impact, and implementation requirements.

**Human action required:** Review the pricing analysis report. Decide whether to proceed to Baseline with one of the three modeled scenarios. This decision changes what customers pay — it requires founder/pricing owner sign-off.

### 3. Evaluate against threshold

The Smoke test passes if:
- A single value metric was identified where high-usage users (P75+) retain at 2x+ the rate of low-usage users (P25 and below)
- The usage distribution has identifiable breakpoints suitable for tier boundaries
- At least one of the three pricing models projects revenue-neutral or positive impact without increasing churn in the highest-retention bands

If PASS, proceed to Baseline with the recommended pricing model. If FAIL, the product may not have a clear value metric that correlates with usage — consider whether usage-based pricing is the right model, or instrument additional candidate metrics and re-run in 2 weeks.

## Time Estimate

- 1 hour: PostHog event audit and gap instrumentation
- 2 hours: Running the `usage-pricing-model-analysis` drill (queries, cohort creation, scenario modeling)
- 1 hour: Report compilation and review
- 1 hour: Human review and go/no-go decision

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage event tracking, retention analysis, cohort creation | Free up to 1M events/mo; paid starts at $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Billing data for revenue correlation | 2.9% + $0.30/transaction; Billing at 0.5% of recurring revenue ([stripe.com/pricing](https://stripe.com/pricing)) |

**Estimated play-specific cost at this level:** Free (analysis only, no new tools required beyond standard stack)

## Drills Referenced

- `usage-pricing-model-analysis` — Runs the full value metric identification, usage distribution mapping, churn analysis, and pricing scenario modeling pipeline
- `posthog-gtm-events` — Ensures all candidate usage metrics are instrumented in PostHog with consistent event naming
