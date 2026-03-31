---
name: usage-based-pricing-optimization-scalable
description: >
  Pricing for Retention — Scalable Automation. Roll the proven pricing model to the
  full customer base, automate tier migration, add upgrade/downgrade prompts, and
  run systematic A/B tests on pricing parameters to find the 10x retention lever.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=8% churn reduction at 500+ customers"
kpis: ["Churn rate", "ARPU", "Net retention", "Segment metrics"]
slug: "usage-based-pricing-optimization"
install: "npx gtm-skills add product/retain/usage-based-pricing-optimization"
drills:
  - pricing-experiment-runner
  - ab-test-orchestrator
  - upgrade-prompt
---

# Pricing for Retention — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Roll the validated pricing model to the full customer base (500+ customers). Automate all pricing operations: tier migration, upgrade prompts at usage thresholds, downgrade offers for at-risk accounts, and systematic A/B tests on pricing parameters. Achieve >=8% churn reduction across the full base while maintaining or growing ARPU.

## Leading Indicators

- Full-base migration completes within 30 days with <5% support ticket rate about pricing
- Automated upgrade prompts fire for 80%+ of customers approaching plan limits
- First pricing parameter A/B test launched within 3 weeks of full rollout
- Usage-to-revenue ratio stabilizes or improves across all segments

## Instructions

### 1. Roll the pricing model to the full base

Using the results from Baseline, migrate all remaining customers to the new pricing model:

a. Create a migration plan segmented by risk: start with customers most likely to benefit (those in high-churn usage bands from Smoke analysis), then move to medium-risk, then low-risk (power users who may see higher bills).

b. Build an n8n workflow that processes the migration in batches of 50 customers per day. For each customer:
   - Check their current usage against the new pricing tiers to calculate their expected bill change
   - Using Stripe subscription management, swap their price objects at the next billing cycle
   - Send a personalized Intercom message: "Your plan is changing. Based on your usage of {X} this month, your new bill will be approximately ${Y}."
   - Log `pricing_migration_completed` event in PostHog with: `customer_id`, `old_plan`, `new_plan`, `expected_bill_change_pct`

c. For customers whose bills would increase >25%, flag for manual review before migration.

**Human action required:** Approve the migration plan and the customer communication templates. Review the flagged accounts (expected bill increase >25%) and decide on retention offers (discounts, grandfathering, etc.).

### 2. Automate upgrade and downgrade prompts

Run the `upgrade-prompt` drill configured for the new pricing model:

a. Define upgrade triggers based on the usage tiers from your model:
   - Customer at 80%+ of their tier's included usage -> show in-app prompt: "You're approaching your {tier} limit. Upgrade to {next tier} for higher limits and a lower per-unit rate."
   - Customer usage doubled month-over-month -> email via Loops: "Your usage is growing. Here's how {next tier} can save you money at this volume."
   - Customer hit a feature gate that requires a higher tier -> show contextual upgrade modal

b. Define downgrade/retention triggers:
   - Customer usage dropped >50% for 2 consecutive weeks and they are on a higher tier -> show offer: "Based on your current usage, you might save money on our {lower tier}. Want to switch?"
   - Customer visited billing/cancellation page -> trigger Intercom message with a tailored retention offer

c. Build the automation in n8n: PostHog cohort membership triggers the appropriate Intercom message or Loops email. Each trigger fires maximum once per customer per 30-day period (prevent message fatigue).

### 3. Run systematic pricing parameter tests

Run the `ab-test-orchestrator` drill to test specific pricing parameters:

Run these experiments sequentially (one at a time, per the `pricing-experiment-runner` guardrails):

**Experiment 1 — Tier boundary optimization:** Test whether moving the tier boundary up or down by 20% improves retention without material revenue impact. Example: if the current threshold between Starter and Pro is 5,000 API calls, test 4,000 vs. 6,000.

**Experiment 2 — Overage rate sensitivity:** Test whether a lower overage rate reduces bill shock and improves retention. Example: test $0.005/call vs. $0.003/call for above-tier usage.

**Experiment 3 — Base price anchoring:** Test whether a slightly higher base with more included usage outperforms a lower base with less included usage. Example: $49/mo with 10,000 included vs. $39/mo with 5,000 included.

For each experiment:
a. Use the `pricing-experiment-runner` drill for setup, monitoring, and decision-making
b. Run for minimum 2 billing cycles (60 days for monthly plans)
c. Primary metric: 30-day churn rate. Secondary metrics: ARPU, NRR, support ticket volume.
d. After each experiment, implement the winner and document the learning before starting the next test.

### 4. Build segment-specific pricing intelligence

Not all customers respond to pricing the same way. Using PostHog cohorts, analyze churn rate and ARPU by:

- Company size (seat count or revenue proxy)
- Usage profile (API-heavy vs. UI-heavy vs. mixed)
- Tenure (new vs. established)
- Growth trajectory (expanding vs. stable vs. contracting)

If specific segments show persistent high churn despite the new model, they may need segment-specific pricing interventions (e.g., startup discount, enterprise commitment pricing). Document segment insights and feed them into the Durable-level optimization.

### 5. Evaluate at scale

After 2 months of full-base pricing:

a. Calculate overall churn reduction: compare the 60-day churn rate post-migration to the 60-day churn rate pre-migration, controlling for seasonality and other changes.

b. Verify the threshold: >=8% churn reduction across 500+ customers. Break down by segment to identify where the model works best and worst.

c. Calculate revenue impact: total MRR change, ARPU change, NRR. Revenue should be flat or growing. If revenue declined, assess whether the churn savings offset the per-customer revenue decline (LTV analysis).

d. If PASS, proceed to Durable. If FAIL:
   - If churn reduction is positive but <8%, the model is directionally right but needs parameter tuning. Run more experiments.
   - If churn increased, the migration may have caused disruption. Segment the data — the model may work for some segments and not others.
   - If revenue declined significantly with minimal churn improvement, the value metric may be wrong. Return to Smoke.

## Time Estimate

- 15 hours: Full-base migration (workflow build, batched rollout, monitoring)
- 10 hours: Upgrade/downgrade prompt automation
- 25 hours: 3 pricing parameter experiments (setup, monitoring, analysis each)
- 5 hours: Segment analysis and documentation
- 5 hours: Final evaluation and threshold assessment

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, feature flags, experiments, cohorts | Free up to 1M events/mo; ~$0.00005/event after ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Billing, subscription management, metered pricing | 2.9% + $0.30/txn; Billing $0.50/invoice ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Migration workflows, prompt automation, monitoring | Self-hosted free; Cloud from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app upgrade/downgrade prompts, retention messaging | From $29/seat/mo; Proactive Support Plus add-on $99/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle emails for upgrade nudges | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

## Drills Referenced

- `pricing-experiment-runner` — manages the controlled rollout and pricing parameter experiments
- `ab-test-orchestrator` — provides the statistical framework for each pricing test
- `upgrade-prompt` — automates contextual upgrade and downgrade prompts based on usage thresholds
