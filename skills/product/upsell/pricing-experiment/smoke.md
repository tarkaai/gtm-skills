---
name: pricing-experiment-smoke
description: >
  Pricing Tests — Smoke Test. Run one controlled pricing experiment on a single plan
  to prove that pricing changes move revenue per user without spiking churn.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "1 pricing variant tested with directional revenue-per-user signal (positive or negative) from 50+ users"
kpis: ["Revenue per user (treatment vs. control)", "30-day churn rate (treatment vs. control)", "Checkout conversion rate"]
slug: "pricing-experiment"
install: "npx gtm-skills add product/upsell/pricing-experiment"
drills:
  - usage-pricing-model-analysis
  - pricing-experiment-runner
  - threshold-engine
---

# Pricing Tests — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

One pricing variant has been tested against the current pricing on a small cohort (50+ users). You have directional data showing whether the variant moved revenue per user up, down, or neutral, and whether churn spiked. This is proof of signal, not proof of scale.

## Leading Indicators

- Stripe price objects created for the variant without errors
- PostHog feature flag live and assigning users to control/treatment
- First billing cycle completed for treatment users (invoices generated at the new price)
- No surge in support tickets mentioning billing or pricing within the first 7 days

## Instructions

### 1. Analyze current pricing and define the experiment hypothesis

Run the `usage-pricing-model-analysis` drill to:
- Identify the value metric that best correlates with retention (API calls, seats, storage, etc.)
- Map the usage distribution across all active customers (P25, P50, P75, P95)
- Compute churn rate by usage band to find where pricing causes churn
- Model 3 pricing scenarios (per-unit, tiered, hybrid) and pick the most promising one

Produce a structured hypothesis: "If we change from [current pricing] to [variant pricing], then revenue per user will [increase/maintain] by [estimated %] because [reasoning], and churn rate will not increase by more than [limit]."

**Human action required:** Review the hypothesis. Approve or revise before proceeding. Pricing experiments directly affect customer trust and revenue.

### 2. Set up and launch the experiment

Run the `pricing-experiment-runner` drill to:
- Create variant price objects in Stripe (tagged with `metadata[experiment]=pricing_smoke_v1`)
- Create a PostHog feature flag `pricing-experiment-smoke` with 50/50 split, targeting only the plan being tested, excluding enterprise/custom-priced accounts and accounts less than 30 days old
- Build the n8n workflow that migrates treatment users to the variant price at their next billing cycle (proration_behavior=none)
- Send an Intercom in-app message to treatment users explaining the pricing change
- Define guardrail metrics: auto-revert if treatment churn exceeds control by >50% at any weekly check, or if gross revenue drops >15% vs. control, or if >10 support tickets about pricing in 7 days

**Human action required:** Review and approve the Intercom message copy before launch. Pricing communication must be clear and honest.

### 3. Monitor for 2 billing cycles and evaluate

Wait for the experiment to run through at least 1 full billing cycle (minimum 14 days for this smoke test). The `pricing-experiment-runner` drill's weekly monitoring workflow checks guardrails automatically.

After the evaluation period, run the `threshold-engine` drill to measure against the pass threshold:
- Did 50+ users complete a billing cycle under the variant?
- Is there a directional signal on revenue per user (even if not statistically significant)?
- Did churn rate in the treatment group stay within the guardrail?

If PASS: document the hypothesis result, the directional signal, and proceed to Baseline where you run the experiment at scale with statistical rigor. If FAIL: diagnose whether the hypothesis was wrong (pricing model), the execution was wrong (targeting, communication), or the sample was too small. Iterate and re-run.

## Time Estimate

- 3 hours: usage analysis, hypothesis formulation, hypothesis review
- 2 hours: Stripe price creation, PostHog flag setup, n8n workflow build, Intercom message
- 1 hour: launch verification and first-week monitoring
- 2 hours: evaluation, documentation, decision

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, event tracking | Free up to 1M feature flag requests/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Stripe | Variant price objects, subscription management | 2.9% + $0.30/transaction + 0.7% Billing fee — [stripe.com/pricing](https://stripe.com/pricing) |
| n8n | Subscription migration workflow, weekly monitoring | Standard stack (excluded from play budget) |
| Intercom | In-app pricing change notification | Proactive Support Plus $99/mo for advanced in-app messages — [intercom.com/pricing](https://www.intercom.com/pricing) |

**Play-specific cost:** Free (PostHog free tier covers smoke-scale flag requests; Stripe fees are transaction-based on existing revenue; Intercom base plan includes basic in-app messaging)

## Drills Referenced

- `usage-pricing-model-analysis` — analyze usage data to identify the optimal pricing variant to test
- `pricing-experiment-runner` — create Stripe prices, PostHog flags, n8n migration workflow, and guardrail monitoring
- `threshold-engine` — evaluate experiment results against pass/fail criteria
