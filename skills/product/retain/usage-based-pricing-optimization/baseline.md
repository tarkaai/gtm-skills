---
name: usage-based-pricing-optimization-baseline
description: >
  Pricing for Retention — Baseline Run. Deploy billing event streaming, run a controlled
  pricing experiment on a cohort of customers, and measure churn reduction against a
  control group over 2 billing cycles.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=10% churn reduction"
kpis: ["Churn rate", "ARPU", "Net retention"]
slug: "usage-based-pricing-optimization"
install: "npx gtm-skills add product/retain/usage-based-pricing-optimization"
drills:
  - posthog-gtm-events
  - pricing-experiment-runner
  - usage-drop-detection
---

# Pricing for Retention — Baseline Run

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Run a controlled pricing experiment where a treatment cohort receives the new usage-based pricing model and a control cohort stays on current pricing. Achieve >=10% churn reduction in the treatment group vs. control after 2 full billing cycles. Revenue per user in the treatment group must not decline by more than 15%.

## Leading Indicators

- Billing events flowing into PostHog within 24 hours of experiment launch (data pipeline working)
- Treatment group enrollment reaches target size within first week (feature flag targeting is correct)
- No guardrail breaches in the first 2 weekly checks (experiment is safe to continue)
- Usage patterns in the treatment group remain stable or increase (new pricing is not discouraging usage)

## Instructions

### 1. Set up billing event tracking

Run the `posthog-gtm-events` drill to configure the billing-to-analytics pipeline:

a. Set up the Stripe webhook to your n8n instance. Configure it to forward: `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed`.

b. Build the n8n workflow that receives Stripe webhooks, maps customer IDs to PostHog distinct IDs, and sends billing events to PostHog. Key events to track:
   - `billing_subscription_updated` with properties: `plan_name`, `plan_amount_usd`, `change_type` (upgrade/downgrade/new)
   - `billing_invoice_paid` with properties: `amount_usd`, `period_start`, `period_end`
   - `billing_payment_failed` with properties: `failure_reason`, `attempt_count`

c. Set PostHog person properties for each customer: `current_plan`, `mrr`, `billing_interval`, `subscription_status`. These enable segmentation in all downstream analysis.

d. Validate: send a test webhook from Stripe's dashboard and confirm the event appears in PostHog within 60 seconds.

### 2. Launch the pricing experiment

Run the `pricing-experiment-runner` drill with the winning pricing model from the Smoke analysis:

a. Create the variant prices in Stripe. Tag all experiment prices with `metadata[experiment]=pricing_v2_baseline`. Do not modify existing prices.

b. Create a PostHog feature flag `pricing-experiment-v2` with 50/50 split. Target only active paying customers who have been on their current plan for at least 30 days. Exclude enterprise contracts and accounts with custom pricing.

c. Build the n8n workflow that migrates treatment-group users to the new prices at their next billing cycle (not mid-cycle). Log every migration as a `pricing_experiment_enrolled` event in PostHog.

d. Configure the in-app notification via Intercom explaining the pricing change to treatment users. The message must clearly state: what changed, why, and that they can contact support with questions.

**Human action required:** Approve the experiment design before launch. Review: the target cohort definition, the variant prices, the in-app messaging copy, and the guardrail thresholds. Sign off that the experiment is safe to run.

### 3. Monitor for usage drops in the treatment group

Run the `usage-drop-detection` drill specifically on the treatment cohort:

a. Configure the detection query to compare treatment-group usage in the 2 weeks after enrollment vs. their 30-day pre-enrollment baseline.

b. Set alert thresholds: if >20% of treatment users show a >30% usage drop within 14 days of the pricing change, this is a signal that the new pricing is discouraging product use. Flag for review.

c. Compare treatment-group usage trends against control-group usage trends. If the control group is stable but the treatment group is declining, the pricing change is the cause.

### 4. Run weekly experiment checks

Every 7 days during the experiment:

a. Query PostHog for treatment vs. control metrics: churn rate, ARPU, usage volume, support tickets mentioning pricing.

b. Check guardrails: treatment churn must not exceed control churn by >50%. Treatment revenue must not drop >15% vs. control. If either guardrail is breached, trigger the auto-revert mechanism from the `pricing-experiment-runner` drill.

c. Check progress toward statistical significance. With 200 customers per group, expect 4-6 weeks to reach 95% confidence on a 10% churn difference.

### 5. Evaluate at the end of 2 billing cycles

After the experiment has run for at least 2 full billing cycles:

a. Pull final metrics from PostHog: churn rate (treatment vs. control), ARPU (treatment vs. control), NRR (treatment vs. control), usage volume change.

b. Calculate the churn reduction: `(control_churn - treatment_churn) / control_churn * 100`. Target: >=10%.

c. Verify the revenue guardrail: treatment ARPU must not have declined >15% vs. control.

d. If PASS (>=10% churn reduction + revenue guardrail held), document results and proceed to Scalable. If FAIL, diagnose:
   - If churn did not decrease: the pricing model may be wrong. Return to Smoke and test a different model.
   - If revenue dropped too much: the base price is too low or overage thresholds are too generous. Adjust and re-run.
   - If insufficient data: extend the experiment duration or increase the cohort size.

## Time Estimate

- 4 hours: Billing event pipeline setup and validation
- 4 hours: Experiment setup (Stripe prices, feature flag, migration workflow, Intercom messaging)
- 2 hours: Usage drop detection configuration
- 6 hours: Weekly monitoring checks (1.5 hours/week x 4 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, feature flags, experiments | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Billing, subscriptions, metered pricing | 2.9% + $0.30 per transaction; Billing at $0.50/invoice ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Webhook pipeline, scheduled monitoring | Self-hosted free; Cloud from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app messaging for pricing change notifications | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |

## Drills Referenced

- `posthog-gtm-events` — sets up the billing-to-PostHog event pipeline
- `pricing-experiment-runner` — manages the full pricing experiment lifecycle
- `usage-drop-detection` — monitors the treatment cohort for adverse usage changes
