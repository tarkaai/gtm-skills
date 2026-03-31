---
name: mvt-experiment-design
description: Design multivariate experiments by selecting variables, mapping combinations, computing required traffic, and creating the test matrix in PostHog
category: Product
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-experiments
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-funnels
  - n8n-workflow-basics
---

# MVT Experiment Design

This drill builds a multivariate experiment from scratch: selecting variables to test, mapping all combinations into a test matrix, computing traffic requirements, and configuring PostHog to run the experiment with statistical rigor.

A multivariate test (MVT) differs from an A/B test in one critical way: an A/B test changes one variable at a time, while an MVT tests multiple variables simultaneously and measures interaction effects between them. An MVT with 2 variables and 2 levels each produces 4 cells (2x2). With 3 variables at 2 levels each: 8 cells. Traffic requirements grow with the number of cells.

## Prerequisites

- PostHog project with feature flags and experiments enabled
- Sufficient user traffic to power the test matrix (see traffic calculation below)
- At least 4 weeks of baseline event data for the metric you want to improve
- A clear retention or engagement metric to optimize

## Steps

### 1. Select variables to test

Identify 2-4 variables that plausibly affect the target metric. Each variable must be independently controllable. Good variables for retention MVTs:

- **In-app messaging**: copy variant, timing (immediate vs. delayed), placement (banner vs. modal vs. tooltip)
- **Email sequences**: subject line, send timing, CTA text, content length
- **Feature surfaces**: default view, onboarding checklist order, empty-state content
- **Pricing/upgrade prompts**: trigger threshold, copy framing (loss vs. gain), discount level

Bad variables: anything that cannot be independently toggled per user (infrastructure changes, third-party API behavior).

For each variable, define exactly 2-3 levels (variants). Keep the matrix small. A 2x2x2 test (3 variables, 2 levels each) has 8 cells. A 3x3x3 test has 27 cells and almost certainly needs more traffic than you have.

### 2. Build the combination matrix

Map every combination. For a 2x2 test of CTA copy (A, B) and CTA placement (top, bottom):

| Cell | CTA Copy | CTA Placement |
|------|----------|---------------|
| 1    | A        | top           |
| 2    | A        | bottom        |
| 3    | B        | top           |
| 4    | B        | bottom        |

For each cell, document the exact experience the user will see. Be precise enough that an agent can implement every cell programmatically using feature flags.

### 3. Calculate required traffic

For each cell in the matrix, you need a minimum sample size for statistical significance. The formula:

- Minimum per cell = `(16 * p * (1-p)) / MDE^2` where `p` = baseline conversion rate, `MDE` = minimum detectable effect as a proportion
- Example: baseline 10% conversion, MDE of 2 percentage points (0.02): `(16 * 0.10 * 0.90) / 0.02^2 = 3,600 per cell`
- For a 4-cell matrix: 14,400 total users needed
- Divide by your weekly user volume to estimate duration

If the required duration exceeds 6 weeks, reduce the matrix: drop a variable or merge levels. An MVT that runs too long produces stale results because user behavior shifts during the test.

### 4. Configure PostHog feature flags for each variable

Using the `posthog-feature-flags` fundamental, create one feature flag per variable:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "mvt-{experiment-slug}-{variable-name}",
  "name": "MVT: {variable-name}",
  "filters": {
    "multivariate": {
      "variants": [
        {"key": "level-a", "rollout_percentage": 50},
        {"key": "level-b", "rollout_percentage": 50}
      ]
    }
  },
  "active": true
}
```

PostHog assigns each user a consistent variant per flag. Because flags are independent, the cross-product of all flags produces the full combination matrix. Verify orthogonality: check that each cell receives approximately equal traffic after 48 hours.

### 5. Create the PostHog experiment

Using the `posthog-experiments` fundamental, create an experiment that references all the feature flags:

- Primary metric: the retention or engagement event you are optimizing
- Secondary metrics: guardrail metrics (e.g., support ticket rate, session errors) to ensure no combination causes harm
- Set the experiment duration based on step 3 calculations
- Enable Bayesian analysis for per-cell significance

Track a custom event `mvt_cell_assigned` using `posthog-custom-events` with properties: `experiment_slug`, `variable_1_level`, `variable_2_level`, etc. This event enables per-cell funnel analysis.

### 6. Build an n8n traffic health check

Using `n8n-workflow-basics`, create a daily workflow that:

1. Queries PostHog for per-cell user counts
2. Checks that no cell has <80% or >120% of expected traffic (indicates a flag configuration error)
3. Estimates completion date based on current traffic rate
4. Alerts (Slack or email) if traffic imbalance detected or if estimated completion date exceeds 6 weeks

## Output

- A documented test matrix with all variable/level combinations
- PostHog feature flags configured for each variable
- A PostHog experiment tracking the primary and secondary metrics
- An n8n health check monitoring traffic balance
- Estimated duration and minimum sample size per cell
