---
name: pricing-experiment-scalable
description: >
  Pricing Tests — Scalable Automation. Run concurrent pricing experiments across
  multiple plans and segments with automated experiment orchestration and segment-specific
  pricing optimization.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 3 months"
outcome: ">=8% NRR improvement sustained across 500+ users with 2+ experiments completed per month"
kpis: ["Net revenue retention (NRR)", "ARPU by plan and segment", "Experiment velocity (completed experiments/month)", "Churn rate by pricing cohort", "Expansion revenue from pricing-driven upgrades"]
slug: "pricing-experiment"
install: "npx gtm-skills add product/upsell/pricing-experiment"
drills:
  - ab-test-orchestrator
  - pricing-experiment-runner
  - dashboard-builder
---

# Pricing Tests — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Pricing experimentation is now a systematic, continuous process — not a one-off project. You are running 2+ experiments per month across different plans, segments, and pricing dimensions (base price, tier boundaries, overage rates, annual discount, add-on bundling). Each experiment uses the same rigorous framework from Baseline but the orchestration is automated: experiments queue, launch, monitor, and evaluate with minimal human intervention.

## Leading Indicators

- Experiment queue has 3+ hypotheses ranked by expected impact
- First automated experiment launches without manual Stripe/PostHog configuration
- Pricing page conversion monitor detecting plan selection shifts in real-time
- Segment-specific pricing cohorts active in PostHog (usage band, tenure, plan)
- Experiment velocity reaching 2 completed experiments per month by end of month 2

## Instructions

### 1. Build the experiment pipeline

Run the `ab-test-orchestrator` drill to create a systematic experiment pipeline:

- Maintain an experiment backlog in Attio: each entry is a hypothesis with fields for `dimension` (base price, tier boundary, overage rate, annual discount, add-on bundle, feature gate), `target_segment` (plan, usage band, tenure cohort), `expected_impact`, `risk_level`, `status`
- Rank hypotheses by expected revenue impact divided by risk level
- Implement the sequential experiment scheduler: only 1 active pricing experiment per plan at a time (different plans can have concurrent experiments); when one experiment concludes, the next queued hypothesis for that plan auto-launches
- Calculate sample sizes per experiment using PostHog's experiment calculator
- Set up automated significance checking: the n8n workflow evaluates each experiment weekly and auto-advances to the decision phase when significance is reached or the maximum duration expires

For each experiment, the orchestrator:
1. Creates Stripe variant prices from the hypothesis specification
2. Creates the PostHog feature flag with proper targeting and exclusions
3. Builds the n8n migration workflow
4. Monitors guardrails weekly
5. Evaluates at significance and posts the decision recommendation to Slack

### 2. Expand to segment-specific pricing experiments

Run the `pricing-experiment-runner` drill for each active experiment, but now with segment-specific targeting:

**By usage band:**
- Low-usage segment (below P25): test lower base prices or usage-based pricing to reduce churn
- Mid-usage segment (P25-P75): test tier boundary adjustments and overage rate optimization
- High-usage segment (above P75): test volume discounts and enterprise tier introduction

**By tenure:**
- New customers (0-90 days): test introductory pricing, trial extensions, first-month discounts
- Established customers (90-365 days): test annual conversion incentives and loyalty pricing
- Long-tenure customers (365+ days): test grandfathering vs. price increase communication strategies

**By plan:**
- Each plan tier gets its own experiment queue with independent hypotheses

For each segment, define specific guardrails calibrated to that segment's baseline metrics (a high-churn segment needs tighter churn guardrails than a sticky segment).

### 3. Monitor the pricing page conversion funnel

Run the `dashboard-builder` drill to build always-on monitoring of the self-serve conversion path:

- Build the "Pricing Page Health" PostHog dashboard: visitors, conversion rate, plan selection distribution, checkout abandonment, ARPU of new subscribers
- Build the multi-step pricing funnel: pricing_page_viewed > plan_card_clicked > checkout_started > payment_method_entered > subscription_created
- Configure anomaly detection: conversion rate drops >20% vs. 14-day average = High; plan mix shifts >15pp in 7 days = Medium; checkout abandonment >70% for 3 days = High
- Build daily monitoring and weekly digest workflows
- Maintain dynamic cohorts: comparison shoppers (3+ pricing page views without converting), plan hesitators (clicked CTA but abandoned checkout), downgrade researchers (paying customers viewing pricing page repeatedly), annual-curious (toggled annual view but chose monthly)

These cohorts become targeting inputs for pricing experiments: e.g., "For annual-curious users, test showing a larger annual discount (30% vs. current 20%)."

### 4. Evaluate at scale

After 3 months, measure against the pass threshold:
- Is NRR improved >= 8% vs. pre-experiment baseline (measured across all adopted pricing changes)?
- Are 500+ users on optimized pricing?
- Is experiment velocity at 2+ completed per month?
- Are segment-specific pricing cohorts producing different optimal prices (validating that one-size-fits-all pricing is suboptimal)?

If PASS: the experiment infrastructure is proven. Proceed to Durable where the AI agent takes over hypothesis generation and experiment design. If FAIL: diagnose whether the issue is hypothesis quality (wrong pricing dimensions), execution quality (experiment leaks, contamination), or measurement quality (insufficient sample sizes). Fix the bottleneck and continue at Scalable.

## Time Estimate

- 8 hours: experiment pipeline setup (backlog, orchestrator, automated launch/evaluate)
- 8 hours: segment-specific experiment design and targeting configuration
- 8 hours: pricing page conversion monitor build (dashboard, funnels, anomalies, cohorts)
- 12 hours: ongoing management over 3 months (1 hour/week for experiment review and backlog grooming)
- 4 hours: quarterly evaluation, documentation, Durable prep

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, dashboards, cohorts, anomaly detection | Free up to 1M flag requests/mo; ~$0.0001/request beyond — [posthog.com/pricing](https://posthog.com/pricing) |
| Stripe | Variant prices per experiment, subscription migrations, billing events | 2.9% + $0.30/txn + 0.7% Billing fee — [stripe.com/pricing](https://stripe.com/pricing) |
| n8n | Experiment orchestration, daily/weekly monitoring, automated launch/evaluate | Standard stack (excluded) |
| Intercom | Pricing change communication, segment-specific in-app messages | $29-132/seat/mo; Proactive Support Plus $99/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Attio | Experiment backlog, hypothesis tracking, pricing project records | Standard stack (excluded) |

**Play-specific cost:** ~$99-200/mo (Intercom Proactive Support Plus for segment-specific messaging; PostHog usage-based charges at scale may apply depending on flag request volume)

## Drills Referenced

- `ab-test-orchestrator` — build and manage the systematic experiment pipeline with automated hypothesis queuing, launch, monitoring, and evaluation
- `pricing-experiment-runner` — execute individual pricing experiments with Stripe price creation, PostHog flag targeting, n8n migration, and guardrail enforcement
- `dashboard-builder` — monitor self-serve pricing page conversion funnel, detect anomalies, and maintain behavioral cohorts for experiment targeting
