---
name: ab-testing-framework-baseline
description: >
  Product A/B Testing — Baseline Run. First always-on experimentation program with structured event
  tracking, rigorous test execution, and result analysis. Run 5+ experiments over 2 weeks with at
  least 2 statistically significant winners that are implemented in production.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=5 experiments completed, >=2 adopted winners"
kpis: ["Experiment velocity", "Win rate", "Cumulative metric lift", "Time to significance"]
slug: "ab-testing-framework"
install: "npx gtm-skills add product/retain/ab-testing-framework"
drills:
  - posthog-gtm-events
  - ab-test-orchestrator
---

# Product A/B Testing — Baseline Run

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Establish a repeatable experimentation practice. The agent sets up proper event tracking for the testing program, runs experiments with statistical rigor using the `ab-test-orchestrator` drill, and produces at least 2 winners that are adopted in production. This level proves the experimentation process works reliably and produces real product improvements -- not just data.

## Leading Indicators

- Event taxonomy configured: all experiment-related events follow a consistent naming scheme and fire correctly
- Funnels built for the primary product flows being tested (activation, conversion, retention)
- Each experiment has a pre-registered hypothesis, sample size calculation, and planned duration before launch
- Experiments reach planned sample sizes on schedule (no underpowered tests)
- At least 1 winning experiment is adopted and its metric improvement holds for 7 days post-implementation

## Instructions

### 1. Configure experiment event tracking

Run the `posthog-gtm-events` drill to establish a clean event taxonomy for the experimentation program. Set up the following events:

- `experiment_started` -- fires when a new experiment is launched (properties: experiment_id, hypothesis, product_area, target_metric)
- `experiment_variant_assigned` -- fires when a user is allocated to control or variant (properties: experiment_id, variant, user_id)
- `experiment_metric_recorded` -- fires when a user completes the target action (properties: experiment_id, variant, metric_name, metric_value)
- `experiment_completed` -- fires when an experiment reaches its sample size or end date (properties: experiment_id, result, confidence, decision)
- `experiment_winner_adopted` -- fires when a winning variant is rolled out to 100% (properties: experiment_id, adopted_variant, expected_lift)

Build PostHog funnels for each product area being tested:
- Activation funnel: signup -> onboarding_step_completed (x N) -> activation_reached
- Conversion funnel: feature_used -> upgrade_prompt_shown -> checkout_started -> payment_completed
- Retention indicators: weekly_active_event with 4-week trailing retention

### 2. Run experiments with statistical rigor

Run the `ab-test-orchestrator` drill for each experiment. The drill enforces:

1. **Hypothesis registration:** Every experiment starts with a structured hypothesis logged before the test begins. No post-hoc storytelling.
2. **Sample size pre-calculation:** Using baseline rate and minimum detectable effect, calculate required samples per variant. Do not launch experiments that cannot reach significance within 14 days given current traffic.
3. **Proper randomization:** User-level allocation via PostHog feature flags. Each user always sees the same variant for the duration of the experiment.
4. **No peeking:** Do not check results before the planned end date. The only exception is guardrail breaches (error rate spike, crash rate increase, unsubscribe spike > 2x baseline) which trigger immediate experiment halt.
5. **Decision protocol:** At experiment end, evaluate primary metric for statistical significance (95% confidence). Check secondary metrics for unintended harm. Decision: adopt (significant improvement, no secondary harm), revert (significant degradation or secondary harm), iterate (not significant, but directionally interesting -- generate a new hypothesis building on this result), or abandon (not significant, no signal).

Run at least 5 experiments over 2 weeks. This requires parallel experiments on non-overlapping product surfaces (e.g., one on onboarding, one on pricing page, one on feature discovery) or rapid sequential experiments on high-traffic surfaces.

### 3. Adopt winners and measure sustained impact

For each adopted experiment:
1. Roll out the winning variant to 100% of users via PostHog feature flag
2. Monitor the target metric for 7 days post-adoption to confirm the lift holds (no novelty effect)
3. If the metric reverts to baseline within 7 days, revert the change and log the experiment as "novelty-only"
4. Log the confirmed lift in Attio with the experiment record

### 4. Evaluate against threshold

Measure against: >=5 experiments completed AND >=2 adopted winners with sustained lift.

If PASS, document:
- Total experiments run and outcomes (adopted/reverted/iterated/abandoned)
- Cumulative metric lift from adopted changes
- Average time to significance
- Product areas with the most opportunity (based on experiment outcomes)

Proceed to Scalable.

If FAIL, diagnose:
- If <5 experiments completed: traffic too low (need higher-traffic surfaces or longer time window) or implementation bottleneck (need faster variant deployment)
- If 5+ experiments but <2 winners: hypotheses too weak (improve data input to hypothesis generation), effect sizes too small (test bolder changes), or wrong metrics being measured

## Time Estimate

- 3 hours: configure event tracking, build funnels, set up experiment naming conventions
- 8 hours: design, implement, and launch 5+ experiments (hypothesis, implementation, monitoring)
- 3 hours: collect results, adopt winners, verify sustained lift, document learnings
- 2 hours: evaluate threshold, diagnose failures if any, prepare for Scalable

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, funnels, cohorts | Free up to 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation and result interpretation | ~$1-5/mo at Baseline volume ($3/$15 per 1M input/output tokens) -- [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Estimated play-specific cost: Free-$5/mo** (PostHog free tier handles Baseline traffic; minimal API calls)

## Drills Referenced

- `posthog-gtm-events` -- establishes the event taxonomy and funnels that all experiments measure against
- `ab-test-orchestrator` -- enforces statistical rigor: hypothesis registration, sample size calculation, no-peeking, decision protocol
