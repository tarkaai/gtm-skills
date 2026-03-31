---
name: experiment-hypothesis-design
description: Generate testable hypotheses from product data, rank by expected impact, and calculate required sample sizes
category: Measurement
tools:
  - PostHog
  - Anthropic
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - hypothesis-generation
  - attio-notes
---

# Experiment Hypothesis Design

This drill turns product data into testable experiment hypotheses. It prevents the common failure mode of A/B testing programs: running random tests with no theory of change. Every experiment starts with data, produces a structured hypothesis, and has a pre-calculated sample size so you know whether the test is feasible before you build anything.

## Prerequisites

- PostHog with at least 30 days of product usage events
- At least 100 weekly active users (below this, most experiments cannot reach statistical significance within a reasonable timeframe)
- Anthropic API key for Claude (hypothesis generation)
- Attio configured for experiment logging

## Input

- A product area or metric the team wants to improve (e.g., "activation rate", "feature X adoption", "trial-to-paid conversion")
- Current baseline value for that metric
- Minimum detectable effect (the smallest improvement worth investing in)

## Steps

### 1. Extract opportunity signals from PostHog

Query PostHog for data that reveals improvement opportunities:

**Funnel drop-offs:** Using `posthog-funnels`, build the funnel for the target metric. Identify the step with the largest absolute drop-off. A step where 40% of users abandon is a bigger opportunity than one where 5% abandon, regardless of how "broken" the latter feels.

**Cohort divergence:** Using `posthog-cohorts`, compare high-performing user cohorts (retained 60+ days) against churned cohorts. What features or actions differentiate them? The gap between these cohorts reveals what to test.

**Session patterns:** Query event sequences for users who completed the target action vs. those who did not. Look for friction signals: repeated attempts at the same step, navigation loops, or long pauses between steps.

Compile the raw data into a structured opportunity brief:
```json
{
  "target_metric": "trial_to_paid_conversion",
  "current_baseline": "8.2%",
  "funnel_drop_offs": [
    {"step": "pricing_page_viewed -> checkout_started", "drop_off_rate": "62%"},
    {"step": "checkout_started -> payment_completed", "drop_off_rate": "18%"}
  ],
  "cohort_differences": [
    "Converted users viewed pricing page 2.4x more often before converting",
    "Converted users used feature X within first 3 days (72% vs 31%)"
  ],
  "friction_signals": [
    "38% of users who view pricing leave within 5 seconds",
    "Users toggle between plan comparison 4+ times before selecting"
  ]
}
```

### 2. Generate ranked hypotheses

Pass the opportunity brief to the `hypothesis-generation` fundamental. Request 5 hypotheses, each structured as:

```json
{
  "hypothesis": "If we add a plan recommendation quiz to the pricing page, then trial-to-paid conversion will increase by 2 percentage points",
  "reasoning": "62% drop-off at pricing->checkout and users toggling between plans 4+ times suggests confusion, not price resistance. A quiz reduces decision effort.",
  "target_metric": "trial_to_paid_conversion",
  "expected_lift": "2pp (8.2% -> 10.2%)",
  "risk_level": "low",
  "implementation_effort": "medium",
  "dependencies": ["pricing page can render dynamic content via feature flag"],
  "estimated_impact_score": 8.5
}
```

Rank hypotheses by: (expected_lift * confidence) / implementation_effort. The top-ranked hypothesis should have the best ratio of potential impact to effort.

### 3. Calculate sample size for each hypothesis

For each hypothesis, compute the required sample size:

- **Inputs:** baseline rate, minimum detectable effect (from the hypothesis), significance level (0.05), power (0.80)
- **Formula:** Use PostHog's built-in experiment calculator or compute manually: `n = (Z_alpha + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p1 - p2)^2`
- **Feasibility check:** Given your current traffic, how many days will this experiment take? If longer than 28 days, either increase the expected effect size (test a bolder change) or pick a higher-traffic surface to test on.

Mark each hypothesis as feasible (can run within 28 days) or infeasible (requires more traffic than available). Drop infeasible hypotheses.

### 4. Log the experiment backlog

Using the `attio-notes` fundamental, create an experiment record in Attio for each feasible hypothesis:
- Hypothesis statement
- Expected lift and confidence
- Required sample size and estimated duration
- Implementation dependencies
- Status: "queued"

This creates the experiment backlog that the `ab-test-orchestrator` drill pulls from.

### 5. Prioritize and schedule

From the feasible backlog, select the top hypothesis for the next experiment. Criteria:
- Highest impact score among feasible hypotheses
- No dependency conflicts with currently running experiments
- Implementation can start within the current sprint

Log the selected hypothesis as "next" in Attio. Archive hypotheses that become stale (older than 90 days without being tested).

## Output

- Ranked list of 3-5 testable hypotheses with sample sizes and feasibility assessments
- Top hypothesis selected and logged in Attio as the next experiment to run
- Opportunity brief documented for future reference

## Triggers

Run this drill:
- At the start of each experiment cycle (before running `ab-test-orchestrator`)
- When a previous experiment completes (to select the next one)
- When the team identifies a new metric to improve
