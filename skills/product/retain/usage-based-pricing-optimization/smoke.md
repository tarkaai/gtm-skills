---
name: usage-based-pricing-optimization-smoke
description: >
  Pricing for Retention — Smoke Test. Analyze current usage data and billing patterns
  to identify the optimal value metric and model 2+ pricing structures that could reduce
  churn for usage-sensitive customer segments.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Test 2 pricing models"
kpis: ["Churn rate", "ARPU", "Net retention"]
slug: "usage-based-pricing-optimization"
install: "npx gtm-skills add product/retain/usage-based-pricing-optimization"
drills:
  - usage-pricing-model-analysis
  - threshold-engine
---

# Pricing for Retention — Smoke Test

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Produce a pricing analysis that identifies the value metric, maps the usage distribution, and models at least 2 alternative pricing structures. The analysis must include projected revenue and churn impact per model. Pass if the analysis is complete and at least one model projects lower churn without >10% revenue loss.

## Leading Indicators

- Usage distribution data extracted from PostHog (confirms data quality is sufficient)
- Churn-by-usage-band analysis shows at least one band where churn correlates with pricing mismatch (confirms the hypothesis that pricing drives churn)
- At least 2 pricing models produce positive retention projections

## Instructions

### 1. Extract and analyze usage patterns

Run the `usage-pricing-model-analysis` drill. This is the core work of the Smoke level. The drill will:

a. Query PostHog for all product usage events over the last 60+ days. You need at least 60 days of per-user event data. If you have less, extend the analysis window or use whatever is available and note the limitation.

b. Identify the value metric: the usage event that most strongly correlates with retention. Test candidates: API calls, feature usage count, records created, team members active, storage consumed. The metric where high-usage users retain at 2x+ the rate of low-usage users is the winner.

c. Map the usage distribution: extract P25, P50, P75, P80, P95 usage levels across all active customers. Look for natural cluster boundaries.

d. Analyze churn by usage band: create 5 usage-band cohorts in PostHog and calculate 30-day and 90-day churn rates for each. Identify the bands where churn is highest and determine whether price-per-unit-of-value is the cause.

e. Model at least 2 pricing alternatives:
   - **Model A — Per-unit or tiered pricing:** Calculate what each customer would pay at their current usage level. Compare to what they pay now.
   - **Model B — Hybrid (base + overage):** Set the base to cover median usage. Calculate overage charges for above-median users.

For each model, compute: total revenue change, per-customer revenue change, number of customers who pay more vs. less, projected churn reduction based on the churn-by-usage-band analysis.

**Human action required:** Review the pricing analysis before proceeding. Validate that the value metric makes business sense (not just statistical correlation). Confirm the churn-by-usage-band findings match qualitative feedback from churned customers.

### 2. Validate with billing data

Pull current Stripe subscription data: plan distribution, ARPU by plan, MRR, monthly churn rate. Cross-reference with the PostHog usage analysis. Confirm that the usage bands from Step 1 align with actual billing tiers. If your current pricing already aligns with usage (low-usage users pay less), the opportunity may be smaller than expected.

### 3. Evaluate against threshold

Run the `threshold-engine` drill to assess whether the Smoke test passed. The pass criteria is: "Test 2 pricing models." This means:

- At least 2 complete pricing models were analyzed with per-customer revenue and churn projections
- At least one model projects churn reduction in the highest-churn usage band
- The analysis is documented with specific numbers, not vague estimates

If PASS, proceed to Baseline where you will run a controlled pricing experiment. If FAIL, investigate: is the data insufficient (need more tracking), is pricing actually not the churn driver (look at product quality, support, competition), or are the models not differentiated enough?

## Time Estimate

- 2 hours: PostHog data extraction and usage distribution analysis
- 1.5 hours: Churn-by-usage-band analysis and correlation work
- 1 hour: Pricing model construction and revenue projections
- 0.5 hours: Documentation and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage analytics, cohort analysis, retention curves | Free up to 1M events/mo; usage-based after ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `usage-pricing-model-analysis` — extracts usage patterns and models pricing alternatives
- `threshold-engine` — evaluates whether the Smoke test passed its outcome criteria
