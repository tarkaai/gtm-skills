---
name: multivariate-testing-baseline
description: >
  Multivariate Experiments — Baseline Run. Establish always-on MVT infrastructure
  with automated event tracking, results analysis, and a continuous pipeline of
  experiments that reliably find winning combinations.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥3 MVTs completed, ≥1 statistically significant winner implemented"
kpis: ["MVT velocity", "Win rate", "Combination insights"]
slug: "multivariate-testing"
install: "npx gtm-skills add product/retain/multivariate-testing"
drills:
  - posthog-gtm-events
  - mvt-experiment-design
  - mvt-results-analysis
---

# Multivariate Experiments — Baseline Run

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Run at least 3 multivariate experiments over 2 weeks. At least 1 must produce a statistically significant winner (95% confidence) that gets implemented into the live product. Establish a standardized event taxonomy for MVT tracking, a repeatable experiment design workflow, and a structured results analysis process.

## Leading Indicators

- Standardized MVT event taxonomy deployed in PostHog within the first 2 days
- First experiment launched within 3 days
- Per-cell traffic balancing within 10% of expected within 48 hours of each launch
- At least 1 experiment reaches statistical significance within the first week
- Main effects and interaction effects computed for every completed experiment

## Instructions

### 1. Establish the MVT event taxonomy

Run the `posthog-gtm-events` drill to set up standardized tracking for all multivariate experiments. Define these events:

- `mvt_cell_assigned` — fired when a user enters an experiment cell. Properties: `experiment_slug`, `variable_1_name`, `variable_1_level`, `variable_2_name`, `variable_2_level`
- `mvt_impression` — fired when the user sees the tested surface. Properties: `experiment_slug`, `cell_id`
- `mvt_engaged` — fired when the user interacts with the tested element. Properties: `experiment_slug`, `cell_id`, `action_type`
- `mvt_converted` — fired when the user completes the target action. Properties: `experiment_slug`, `cell_id`, `conversion_value`
- `mvt_retained` — fired when the user returns within the retention window. Properties: `experiment_slug`, `cell_id`, `days_since_conversion`

Build PostHog funnels: `mvt_cell_assigned` -> `mvt_impression` -> `mvt_engaged` -> `mvt_converted` -> `mvt_retained`. Break down by `cell_id` to see per-combination conversion.

### 2. Design and launch 3 experiments

Run the `mvt-experiment-design` drill for each experiment. Target different retention surfaces to maximize learning:

**Experiment 1: Upgrade prompt optimization**
- Variable A: copy framing (2 levels: benefit-focused vs. loss-aversion)
- Variable B: trigger timing (2 levels: at usage threshold vs. at session start)
- Primary metric: `mvt_converted` (upgrade click-through)

**Experiment 2: Feature discovery optimization**
- Variable A: tooltip content (2 levels: text-only vs. animated demo)
- Variable B: tooltip trigger (2 levels: automatic on page load vs. on hover of feature area)
- Primary metric: `mvt_engaged` (feature first-use within 7 days)

**Experiment 3: Re-engagement message optimization**
- Variable A: message urgency (2 levels: informational vs. time-limited offer)
- Variable B: channel (2 levels: in-app banner vs. email)
- Primary metric: `mvt_retained` (return within 3 days of message)

Stagger launches so experiments do not compete for the same users. If user overlap is unavoidable, ensure experiments target different product surfaces.

### 3. Analyze results with interaction effect detection

Run the `mvt-results-analysis` drill for each completed experiment. For each experiment, produce:

- Per-cell conversion rates with confidence intervals
- Main effect per variable (which variable matters more)
- Interaction effects (which combinations synergize or conflict)
- A winning combination recommendation with statistical confidence

If an experiment does not reach statistical significance, document why (insufficient traffic, variables with no effect, noisy metric) and apply the learning to the next experiment design.

### 4. Implement winners

For each experiment with a statistically significant winner:

1. Roll out the winning combination to 100% of users via PostHog feature flags
2. Track the primary metric for 7 days post-implementation
3. Confirm the lift holds (within 50% of measured lift)
4. Make the change permanent in the codebase and clean up experiment flags

### 5. Evaluate against threshold

Measure against: at least 3 MVTs completed, at least 1 statistically significant winner implemented. If PASS, proceed to Scalable. If FAIL, diagnose: were experiments too small (increase traffic or reduce matrix), were variables poorly chosen (talk to product/support teams about what actually affects retention), or was analysis incomplete (ensure interaction effects are computed, not just per-cell rates).

## Time Estimate

- 3 hours: event taxonomy setup and PostHog funnel configuration
- 4 hours: designing 3 experiment matrices and configuring feature flags
- 2 hours: implementation verification and launch
- 4 hours: monitoring, analysis, and results documentation
- 3 hours: winner implementation and post-deployment monitoring

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, event tracking, funnels | Free tier: 1M flag requests/mo, 1M events/mo. Paid: $0.0001/flag request after free tier ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation for traffic health checks | Self-hosted free; Cloud Starter ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

## Drills Referenced

- `posthog-gtm-events` — establishes the standardized event taxonomy for all MVT tracking
- `mvt-experiment-design` — designs each experiment's matrix, configures feature flags, and computes sample sizes
- `mvt-results-analysis` — analyzes per-cell results, computes main effects and interaction effects, ranks combinations
