---
name: ab-testing-framework-smoke
description: >
  Product A/B Testing — Smoke Test. Run 3 rigorous experiments on product features, UX, or messaging
  using PostHog experiments and feature flags. Validate that hypotheses can be generated from data,
  tests can reach statistical significance, and results produce actionable outcomes.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Run 3 experiments with statistically significant results"
kpis: ["Experiment velocity", "Win rate", "Statistical significance achieved"]
slug: "ab-testing-framework"
install: "npx gtm-skills add product/retain/ab-testing-framework"
drills:
  - experiment-hypothesis-design
  - threshold-engine
---

# Product A/B Testing — Smoke Test

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Prove the concept: can you extract product usage data from PostHog, generate testable hypotheses, run A/B experiments with proper statistical rigor, and get results that an agent can act on? No automation, no always-on. A single agent-assisted run that produces 3 experiments with measurable outcomes. The goal is to confirm that your product has enough traffic for experimentation and that the testing infrastructure works end to end.

## Leading Indicators

- PostHog has at least 30 days of product usage events with 3+ meaningful event types
- Hypothesis generation produces ranked, testable hypotheses with calculated sample sizes
- At least 2 of 3 experiments reach the required sample size within the 7-day window
- Experiment results show a clear separation between control and variant (whether the variant wins or loses)

## Instructions

### 1. Verify PostHog data readiness

Confirm your PostHog project has the minimum data for experimentation. Run this verification query via PostHog API:

```
SELECT event, count() FROM events WHERE timestamp > now() - interval 30 day GROUP BY event ORDER BY count() DESC LIMIT 20
```

Check that:
- At least 3 meaningful product event types exist (feature usage, page views, conversions)
- Weekly active users exceed 200 (minimum for experiments to reach significance in a reasonable timeframe)
- Feature flag requests are enabled (required for experiment variant allocation)

If fewer than 3 event types exist, instrument tracking first using the `posthog-custom-events` fundamental. If WAU is below 200, select the highest-traffic product surface for your experiments.

### 2. Generate experiment hypotheses

Run the `experiment-hypothesis-design` drill in manual mode. The drill:
1. Extracts opportunity signals from PostHog: funnel drop-offs, cohort divergence between retained and churned users, friction signals in session patterns
2. Passes the opportunity brief to Claude for hypothesis generation
3. Calculates sample sizes for each hypothesis and filters for feasibility (can reach significance within 7 days given your traffic)

Select the top 3 feasible hypotheses. Each must have:
- A structured hypothesis: "If we [change X], then [metric Y] will [increase/decrease] by [estimated amount], because [reasoning]"
- A calculated sample size and estimated days to significance
- A primary metric and at least one secondary/guardrail metric

**Human action required:** Review the 3 hypotheses before proceeding. Verify they are testing meaningful product changes, not trivial variations. Confirm the implementation is feasible within the time window.

### 3. Run 3 experiments sequentially

For each hypothesis, use PostHog's experiment and feature flag system:

1. Create a feature flag for variant allocation (50/50 split, user-level randomization)
2. Configure the experiment in PostHog: primary metric, secondary metrics, target sample size
3. Implement the variant change (copy, layout, flow, or feature behavior)
4. Launch the experiment and let it run until sample size is reached or 7 days elapse
5. Collect results: control vs variant for primary and secondary metrics, confidence interval, p-value

Run experiments sequentially (one at a time) to avoid interaction effects. If an experiment cannot reach sample size in 7 days, document it as underpowered and note the actual sample achieved.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: did you complete 3 experiments with statistically significant results (p < 0.05)?

Record for each experiment:
- Hypothesis tested
- Sample size achieved (control and variant)
- Primary metric: baseline, variant, lift, confidence
- Decision: adopt winner, revert, or inconclusive
- Key learning (what did you learn regardless of outcome)

If PASS (3 experiments completed with significant results), proceed to Baseline. If FAIL, diagnose: was traffic too low (need higher-traffic surfaces), were hypotheses too weak (need better data input), or was implementation flawed (need engineering support)?

## Time Estimate

- 1 hour: verify PostHog data readiness and feature flag infrastructure
- 1 hour: generate and review hypotheses, calculate sample sizes
- 2 hours: implement and launch 3 experiments (rapid sequential execution)
- 1 hour: collect results, evaluate threshold, document learnings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data, feature flags, experiments, funnels | Free up to 1M events/mo, 1M feature flag requests/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation from usage data | ~$0.01-0.05 per hypothesis batch ($3/$15 per 1M input/output tokens) -- [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Estimated cost for Smoke: Free** (PostHog free tier + <$1 in API calls for hypothesis generation)

## Drills Referenced

- `experiment-hypothesis-design` -- generates testable hypotheses from PostHog data, ranks by expected impact, calculates sample sizes
- `threshold-engine` -- evaluates whether the 3 experiments met the pass threshold
