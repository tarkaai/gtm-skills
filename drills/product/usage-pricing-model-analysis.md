---
name: usage-pricing-model-analysis
description: Analyze product usage data to identify optimal pricing tiers, thresholds, and value metrics for usage-based pricing
category: Product
tools:
  - PostHog
  - Stripe
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-retention-analysis
  - stripe-usage-records
  - stripe-subscription-management
  - attio-custom-attributes
---

# Usage Pricing Model Analysis

This drill extracts usage patterns from PostHog and billing data from Stripe to identify the optimal pricing structure. It answers: what is the right value metric, where should tier boundaries sit, and which pricing model (per-unit, tiered, volume) minimizes churn while maximizing ARPU.

## Input

- PostHog with at least 60 days of product usage events per user
- Stripe with active subscriptions and billing history
- A hypothesis about what the value metric should be (API calls, seats, storage, messages, etc.)

## Steps

### 1. Identify the value metric

The value metric is the unit customers pay for. It must correlate with the value they receive. Query PostHog to find which usage events best predict retention and expansion:

```sql
SELECT
  person_id,
  countIf(event = 'api_call' AND timestamp > now() - interval 30 day) AS api_calls_30d,
  countIf(event = 'report_generated' AND timestamp > now() - interval 30 day) AS reports_30d,
  countIf(event = 'team_member_invited' AND timestamp > now() - interval 30 day) AS invites_30d,
  countIf(event = 'integration_connected' AND timestamp > now() - interval 30 day) AS integrations_30d
FROM events
WHERE timestamp > now() - interval 90 day
GROUP BY person_id
```

Cross-reference with Stripe data: for each user, pull their current MRR and whether they expanded, contracted, or churned. The usage event with the strongest positive correlation to retention and expansion is your candidate value metric.

Using `posthog-retention-analysis`, build retention curves segmented by each candidate metric. The metric where high-usage users retain at 2x+ the rate of low-usage users is the winner.

### 2. Map the usage distribution

Query the usage distribution for the value metric across all active customers:

```sql
SELECT
  person_id,
  count() AS usage_count_30d
FROM events
WHERE event = '{value_metric_event}'
  AND timestamp > now() - interval 30 day
GROUP BY person_id
ORDER BY usage_count_30d
```

Plot the distribution. Usage-based products typically show a long-tail distribution. Identify:

- **Median usage**: Where most customers sit. This is where your free tier or base plan should be comfortable.
- **80th percentile**: Where the first paid tier threshold should sit. 80% of users should be below this.
- **95th percentile**: Where the premium/enterprise tier starts.
- **Cluster boundaries**: If the distribution has natural gaps, use those as tier boundaries.

### 3. Analyze churn by usage band

Using `posthog-cohorts`, create usage-band cohorts:

- Band A: 0 to P25 (bottom quartile usage)
- Band B: P25 to P50
- Band C: P50 to P75
- Band D: P75 to P95
- Band E: P95+ (power users)

For each band, calculate 30-day churn rate, 90-day churn rate, and ARPU. The goal: find the bands where churn is highest and investigate whether price is the cause. If Band A churns at 15% monthly and they are on a flat-rate plan, usage-based pricing would let them pay less and potentially retain.

### 4. Model pricing scenarios

Build 3 pricing models using the data:

**Model 1 — Per-unit pricing:** Flat rate per unit of the value metric (e.g., $0.01/API call). Simple to understand. Calculate: at median usage, what would the customer pay? At P80? At P95?

**Model 2 — Tiered pricing (graduated):** Different rates per tier (e.g., first 1,000 calls at $0.01, next 9,000 at $0.008, above 10,000 at $0.005). Rewards growth. Calculate same breakpoints.

**Model 3 — Hybrid (base + overage):** Flat base fee includes X units, overage charged per unit above that (e.g., $49/mo includes 5,000 calls, $0.008/call after). Provides revenue predictability. Calculate breakpoints.

For each model, compute:
- Revenue at current usage levels across all customers
- Revenue change vs. current pricing (total and per-customer)
- Number of customers who would pay more vs. less
- Projected churn impact: customers paying more than current who are in high-churn bands

### 5. Validate willingness to pay

Using `posthog-custom-events`, check behavioral signals of price sensitivity:

- How many users visit the pricing page per month?
- How many users hit plan limits and do NOT upgrade?
- How many trial users convert vs. drop off at the payment step?
- Support ticket volume mentioning pricing or cost

Store insights in Attio using `attio-custom-attributes`: add `pricing_sensitivity_score` and `optimal_plan_recommendation` per company record.

### 6. Document the recommendation

Produce a pricing analysis report containing:

- Recommended value metric and justification
- Recommended pricing model (of the 3) with tier boundaries
- Expected revenue impact (increase/decrease/neutral)
- Expected churn impact per usage band
- Risks and mitigations
- Implementation requirements (Stripe meter setup, price objects, migration plan)

Store the report as an Attio note on the company-level record for the pricing project.

## Output

- Usage distribution analysis with percentile breakpoints
- Churn-by-usage-band analysis showing where pricing causes churn
- 3 modeled pricing scenarios with revenue/churn projections
- A recommendation document with implementation plan
- Attio records updated with per-customer pricing sensitivity data

## Triggers

Run once during Smoke, then re-run quarterly at Durable level to check if usage patterns have shifted enough to warrant tier boundary adjustments.
