---
name: net-retention-optimization-smoke
description: >
  Net Retention Optimization — Smoke Test. Instrument billing events, compute your first NDR
  number, decompose it into churn/contraction/expansion, and validate that the measurement
  is accurate enough to act on.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "NDR baseline computed with <5% variance from billing system"
kpis: ["Net dollar retention", "Gross retention rate", "Revenue churn rate", "Expansion rate", "Logo churn rate"]
slug: "net-retention-optimization"
install: "npx gtm-skills add product/retain/net-retention-optimization"
drills:
  - posthog-gtm-events
  - threshold-engine
---

# Net Retention Optimization — Smoke Test

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Prove the measurement: can you compute NDR accurately from PostHog billing events, decompose it into its three components (churn, contraction, expansion), and establish per-cohort baselines? No automation, no always-on. Just a single agent run that produces a validated NDR number and identifies where revenue is leaking.

A passing NDR baseline means the measurement matches your billing system within 5% variance. The number itself does not need to be above 100% — you need to trust the measurement before optimizing it.

## Leading Indicators

- Billing events (`subscription_created`, `subscription_cancelled`, `subscription_upgraded`, `subscription_downgraded`) are flowing into PostHog with correct MRR properties
- NDR computation produces a number within 5% of your billing system's reported revenue retention
- Decomposition reveals which component (churn, contraction, expansion) has the largest impact on NDR
- At least 3 months of historical data is available for baseline computation

## Instructions

### 1. Instrument billing events in PostHog

Run the `posthog-gtm-events` drill to establish your event taxonomy. Ensure the following billing-specific events are tracked:

- `subscription_created` with `company_id`, `plan`, `mrr`, `billing_cycle`
- `subscription_cancelled` with `company_id`, `plan`, `mrr_lost`, `cancellation_reason`, `months_active`
- `subscription_upgraded` with `company_id`, `old_plan`, `new_plan`, `old_mrr`, `new_mrr`, `expansion_mrr`
- `subscription_downgraded` with `company_id`, `old_plan`, `new_plan`, `old_mrr`, `new_mrr`, `contraction_mrr`
- `seat_added` and `seat_removed` with `company_id`, `new_seat_count`, `mrr_increase`/`mrr_decrease`

If your billing system is Stripe or Paddle, set up an n8n webhook workflow to relay billing events into PostHog. If your app already fires these events directly, verify the property values match your billing system records.

**Human action required:** Verify that at least 10 recent billing events have correct MRR values by cross-referencing PostHog events with your billing dashboard. Fix any discrepancies before proceeding.

### 2. Compute your NDR baseline

Run the the ndr baseline measurement workflow (see instructions below) drill in manual mode. This computes:

- Trailing 3-month NDR with full decomposition (churned MRR, contraction MRR, expansion MRR)
- Gross retention rate (GRR) — NDR without expansion, showing pure revenue retention
- Per-cohort NDR by signup month
- Revenue churn rate and logo churn rate

Review the output. Check:
- Does the computed NDR match what your billing system reports? (Target: <5% variance)
- Which NDR component is the largest drag? (Churn? Contraction? Weak expansion?)
- Are there specific signup cohorts with notably worse retention?

### 3. Identify the primary lever

From the NDR decomposition, determine your highest-impact opportunity:

- If **churned MRR** is the dominant loss component: the primary play lever is churn prevention. Users are leaving entirely.
- If **contraction MRR** is dominant: users are downgrading, removing seats, or reducing usage. The lever is engagement and value delivery.
- If **expansion MRR** is weak: users are staying but not growing. The lever is upgrade prompts and feature adoption.

Document which lever is primary. This determines which drills to prioritize at Baseline.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to validate: does the computed NDR match your billing system within 5% variance? This is a measurement accuracy threshold, not a performance threshold.

If PASS (variance <5%), the measurement is trustworthy. Record the NDR baseline number and proceed to Baseline.
If FAIL (variance >5%), diagnose the discrepancy. Common causes: missing billing events (check webhook reliability), incorrect MRR properties (check event payloads), or timing mismatches (check timezone handling). Fix and re-compute.

### 5. Document findings

Record:
- Current NDR (trailing 3 months)
- NDR decomposition: churn %, contraction %, expansion %
- GRR (retention without expansion)
- Primary lever identified (churn, contraction, or expansion)
- Top 3 worst-performing signup cohorts
- Top 3 most common cancellation reasons (from `cancellation_reason` property)
- Measurement accuracy (variance vs. billing system)

## Time Estimate

- 2 hours: instrument billing events and verify data accuracy
- 1.5 hours: run NDR baseline computation and review output
- 1 hour: decompose NDR and identify primary lever
- 1 hour: validate against billing system and fix discrepancies
- 0.5 hours: document findings and decide next steps

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Billing event tracking, NDR computation, cohort analysis | Free up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated cost for Smoke: Free** (PostHog free tier covers billing event volume for most early-stage companies)

## Drills Referenced

- the ndr baseline measurement workflow (see instructions below) — computes NDR from billing events, decomposes into churn/contraction/expansion, establishes per-cohort baselines
- `posthog-gtm-events` — establishes the standard event taxonomy in PostHog for billing and product events
- `threshold-engine` — validates that the NDR measurement matches the billing system within the 5% accuracy threshold
