---
name: pricing-page-optimization-scalable
description: >
  Self-Serve Pricing Optimization — Scalable Automation. Segment the pricing page
  experience by visitor persona, automate experiment pipelines across plan structure
  and checkout UX, and scale to ≥8% sustained lift at 500+ monthly conversions.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥8% sustained lift at 500+ monthly pricing page conversions"
kpis: ["Pricing page conversion rate", "Plan selection mix", "ARPU (new subscribers)", "Segment-level conversion rates", "Experiment velocity"]
slug: "pricing-page-optimization"
install: "npx gtm-skills add product/upsell/pricing-page-optimization"
drills:
  - pricing-experiment-runner
  - upgrade-prompt
  - usage-pricing-model-analysis
---

# Self-Serve Pricing Optimization — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

The pricing page delivers ≥8% sustained conversion lift at 500+ monthly conversions. Visitor experiences are segmented by persona or source, with each segment receiving a tailored pricing page variant. Pricing structure itself is tested (not just layout/copy) using controlled Stripe experiments. An experiment pipeline runs continuously with minimal manual intervention.

## Leading Indicators

- At least 3 segment-specific pricing page variants live simultaneously
- Experiment pipeline completing one full test cycle every 2-3 weeks
- Segment-level conversion rates all trending above pre-Baseline levels
- ARPU increasing or stable across all segments (not sacrificing revenue for volume)
- Upgrade prompt conversion rate >5% for limit-approaching users

## Instructions

### 1. Analyze pricing model fitness

Run the `usage-pricing-model-analysis` drill to determine whether the current pricing tiers align with actual usage patterns:

1. Extract the usage distribution across all active customers (what value metric they consume and how much)
2. Map usage bands to churn rates — identify if low-usage users churn because the base price exceeds their perceived value
3. Model 3 pricing scenarios: current tiers with adjusted boundaries, graduated tiering, or hybrid (base + overage)
4. Compare projected revenue and churn impact for each scenario
5. Produce a recommendation document stored in Attio

This analysis informs what to test at Scalable — layout experiments from Baseline are not enough. You now test the actual pricing structure.

### 2. Run a pricing structure experiment

Run the `pricing-experiment-runner` drill to test the top recommendation from Step 1:

1. Create variant Price objects in Stripe (new tiers, adjusted thresholds, or a usage-based component). Tag all with `metadata[experiment]=pricing_structure_v1`.
2. Set up a PostHog feature flag `pricing-structure-experiment` with 50/50 split. Targeting: active paying customers on the plan being tested. Exclude: enterprise, custom pricing, accounts <30 days old.
3. Build the n8n subscription migration workflow: when a user is assigned to treatment, swap their Stripe subscription items to the variant prices at the next billing cycle (never mid-cycle).
4. Define guardrails: auto-revert if treatment churn rate exceeds control by >50% at any weekly check, or if gross revenue drops >15%.
5. Run for minimum 2 full billing cycles (60 days for monthly billing).
6. Evaluate: adopt, iterate, or revert based on net revenue retention and churn impact.

**Human action required:** Approve the experiment hypothesis and guardrail thresholds before the feature flag goes live. Pricing experiments directly affect revenue — no auto-launch.

### 3. Segment the pricing page by visitor persona

Using PostHog feature flags, create 3 pricing page variants based on visitor attributes:

**Segment A — New visitors from organic search:**
- Lead with a comparison table vs. competitors
- Emphasize free trial or free tier to reduce friction
- Show the most popular plan prominently

**Segment B — Existing free users visiting from in-product link:**
- Lead with their current usage data ("You've used X of Y this month")
- Highlight the specific features they would unlock by upgrading
- Show a personalized recommendation based on their usage band

**Segment C — Visitors from paid campaigns:**
- Match the pricing page headline to the ad copy they clicked
- Lead with the plan that matches the campaign's target persona
- Include the offer or incentive mentioned in the ad

Route visitors into segments using PostHog person properties (existing customer vs. new, traffic source, usage band). Track conversion rate per segment separately. Each segment gets its own funnel in the PostHog dashboard.

### 4. Set up expansion upgrade prompts

Run the `upgrade-prompt` drill to catch users who visit the pricing page but do not convert immediately:

1. Create a PostHog cohort: "pricing page visitors who did not convert within 48 hours"
2. Trigger an Intercom in-app message when they next log into the product: "Still deciding? Here's what [recommended plan] includes that your current plan doesn't: [top 3 differentiating features]."
3. For users who clicked a plan CTA but abandoned checkout, trigger a Loops transactional email 24 hours later: "You were looking at [plan name]. Complete your upgrade in one click: [direct checkout link with pre-filled plan]."
4. For high-usage users approaching plan limits, trigger a contextual upgrade prompt inside the product when they hit 80% of a limit.

Track the conversion rate of each prompt type. A/B test the prompt copy and timing.

### 5. Evaluate against threshold

After 2 months, measure:

- **Primary metric:** Pricing page to checkout conversion rate. Threshold: ≥8% sustained lift vs. pre-Smoke baseline at 500+ monthly conversions.
- **Segment metrics:** Each segment (A, B, C) conversion rate must be individually above the pre-Baseline level.
- **ARPU:** Must be stable or increasing. If conversion increased but ARPU dropped, the lift is not real revenue growth.
- **Experiment velocity:** At least 3 completed experiments during the 2-month window.
- **Guardrail:** No segment's churn rate can be more than 1.5x the pre-Smoke level.

If PASS: Document all segment configurations, experiment results, and the pricing model recommendation. Proceed to Durable.
If FAIL: Identify which segments are underperforming. Focus the next experiment cycle on the weakest segment. Re-run Scalable for another month.

## Time Estimate

- 12 hours: usage-pricing-model-analysis (data extraction, modeling, recommendation)
- 16 hours: pricing structure experiment (Stripe setup, feature flag, migration workflow, monitoring, evaluation)
- 16 hours: segment variant builds (3 variants, PostHog targeting, per-segment funnels)
- 8 hours: upgrade prompt setup and A/B testing
- 8 hours: ongoing monitoring, analysis, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, cohorts, session recordings | Free up to 1M events/mo, then $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Variant price objects, subscription migration, billing events | 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Subscription migration workflow, monitoring automations | From €24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Intercom | In-app upgrade prompts for pricing page abandoners | From $39/mo Starter ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Transactional email for checkout abandonment recovery | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

## Drills Referenced

- `pricing-experiment-runner` — run a controlled Stripe pricing structure experiment with guardrails and auto-revert
- `upgrade-prompt` — trigger contextual upgrade prompts for pricing page visitors who did not convert
- `usage-pricing-model-analysis` — analyze usage data to determine optimal pricing tiers and structure
