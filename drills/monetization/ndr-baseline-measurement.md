---
name: ndr-baseline-measurement
description: Compute net dollar retention from billing and usage data, establish per-cohort baselines, and decompose NDR into churn, contraction, and expansion components
category: Revenue Ops
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-retention-analysis
  - attio-custom-attributes
  - n8n-workflow-basics
---

# NDR Baseline Measurement

This drill computes net dollar retention (NDR) from your billing and usage data, decomposes it into its three components (churn, contraction, expansion), and establishes per-cohort baselines so you can measure the impact of retention and expansion interventions.

NDR = (Starting MRR - Churned MRR - Contraction MRR + Expansion MRR) / Starting MRR * 100

An NDR of 100% means you keep every dollar. Above 100% means expansion outpaces churn. Below 100% means you are leaking revenue.

## Prerequisites

- PostHog tracking active with billing-related events: `subscription_created`, `subscription_cancelled`, `subscription_upgraded`, `subscription_downgraded`, `subscription_renewed`
- If billing events are not in PostHog, you need an n8n workflow that syncs billing data from Stripe/Paddle/your billing system into PostHog as custom events
- Attio with company records that have an MRR field
- At least 3 months of billing history to establish a meaningful baseline

## Steps

### 1. Instrument billing events in PostHog

Using the `posthog-custom-events` fundamental, ensure these events fire with the correct properties:

```javascript
// Subscription lifecycle events
posthog.capture('subscription_created', {
  company_id: 'comp_123',
  plan: 'pro',
  mrr: 99,
  billing_cycle: 'monthly',
  source: 'self-serve'
});

posthog.capture('subscription_cancelled', {
  company_id: 'comp_123',
  plan: 'pro',
  mrr_lost: 99,
  cancellation_reason: 'too_expensive',
  months_active: 4
});

posthog.capture('subscription_upgraded', {
  company_id: 'comp_123',
  old_plan: 'starter',
  new_plan: 'pro',
  old_mrr: 29,
  new_mrr: 99,
  expansion_mrr: 70
});

posthog.capture('subscription_downgraded', {
  company_id: 'comp_123',
  old_plan: 'pro',
  new_plan: 'starter',
  old_mrr: 99,
  new_mrr: 29,
  contraction_mrr: 70
});

posthog.capture('seat_added', {
  company_id: 'comp_123',
  new_seat_count: 6,
  mrr_increase: 15
});

posthog.capture('seat_removed', {
  company_id: 'comp_123',
  new_seat_count: 4,
  mrr_decrease: 15
});
```

If billing events come from Stripe webhooks, use an n8n workflow (see step 2) to relay them into PostHog.

### 2. Build the billing sync workflow (if needed)

Using the `n8n-workflow-basics` fundamental, create a workflow that listens for Stripe/Paddle webhooks and translates them into PostHog events:

1. **Trigger:** Webhook node receiving billing provider events
2. **Transform:** Map billing provider event types to PostHog event names (e.g., `customer.subscription.updated` -> `subscription_upgraded` or `subscription_downgraded` depending on MRR change direction)
3. **Emit:** POST to PostHog capture API with the normalized event and properties
4. **Log:** Write the raw billing event to Attio as a note on the company record for audit trail

### 3. Compute monthly NDR

Run a HogQL query that computes NDR for each month:

```sql
SELECT
  dateTrunc('month', timestamp) AS month,
  sumIf(properties.mrr, event = 'subscription_created' AND timestamp = dateTrunc('month', timestamp)) AS starting_mrr,
  sumIf(properties.mrr_lost, event = 'subscription_cancelled') AS churned_mrr,
  sumIf(properties.contraction_mrr, event = 'subscription_downgraded')
    + sumIf(properties.mrr_decrease, event = 'seat_removed') AS contraction_mrr,
  sumIf(properties.expansion_mrr, event = 'subscription_upgraded')
    + sumIf(properties.mrr_increase, event = 'seat_added') AS expansion_mrr
FROM events
WHERE event IN ('subscription_created', 'subscription_cancelled', 'subscription_upgraded', 'subscription_downgraded', 'seat_added', 'seat_removed')
  AND timestamp > now() - interval 6 month
GROUP BY month
ORDER BY month
```

Then compute NDR per month:

```
NDR = (starting_mrr - churned_mrr - contraction_mrr + expansion_mrr) / starting_mrr * 100
```

### 4. Decompose NDR by cohort

Using the `posthog-cohorts` fundamental, create signup-month cohorts. Compute NDR for each cohort independently to identify which cohorts retain best. This reveals whether recent product changes improved retention or whether older cohorts are propping up your number.

Query pattern:
```sql
SELECT
  dateTrunc('month', person.created_at) AS signup_month,
  -- same NDR computation as step 3, filtered by signup cohort
```

### 5. Establish the baseline

Using the `posthog-retention-analysis` fundamental, compute:

- **Trailing 3-month NDR:** Your current performance baseline
- **Gross retention rate (GRR):** NDR without expansion (measures how well you prevent revenue loss)
- **Expansion rate:** Expansion MRR / Starting MRR (measures how well you grow existing accounts)
- **Logo churn rate:** Accounts cancelled / Total active accounts (count-based, not dollar-based)
- **Revenue churn rate:** Churned MRR / Starting MRR (dollar-based)

Store these baselines in Attio using `attio-custom-attributes` as company-level metrics that update monthly.

### 6. Log the baseline as a PostHog event

Using `posthog-custom-events`, emit a monthly tracking event:

```javascript
posthog.capture('ndr_computed', {
  month: '2026-03',
  ndr: 107.2,
  grr: 94.1,
  expansion_rate: 13.1,
  churned_mrr: 4200,
  contraction_mrr: 1700,
  expansion_mrr: 8900,
  starting_mrr: 67800,
  logo_churn_rate: 3.2,
  revenue_churn_rate: 5.9,
  active_accounts: 312
});
```

This creates a time series for tracking NDR improvement as retention and expansion interventions take effect.

## Output

- PostHog billing events instrumented with consistent properties
- Monthly NDR computation with full decomposition (churn, contraction, expansion)
- Per-cohort NDR breakdown revealing which signup cohorts retain best
- Baseline metrics stored in Attio and PostHog for trend tracking
- n8n billing sync workflow (if billing data originates outside PostHog)

## Triggers

- Monthly NDR computation: cron, 1st of each month at 06:00 UTC
- Billing event sync: real-time via webhook (if using Stripe/Paddle relay)
