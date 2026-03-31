---
name: mvt-results-analysis
description: Analyze multivariate experiment results including interaction effects, combination ranking, and winner implementation
category: Experimentation
tools:
  - PostHog
  - Anthropic
  - n8n
fundamentals:
  - posthog-experiments
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - experiment-evaluation
  - n8n-workflow-basics
---

# MVT Results Analysis

This drill extracts actionable insights from a completed multivariate experiment. Unlike A/B test analysis (which answers "is A or B better?"), MVT analysis answers three questions: which individual variable levels perform best, which combinations produce interaction effects (synergies or conflicts), and which single combination is the overall winner.

## Prerequisites

- A completed MVT experiment (reached planned sample size in all cells)
- PostHog experiment with per-cell event tracking configured
- The `mvt_cell_assigned` events with per-variable level properties (from `mvt-experiment-design`)

## Steps

### 1. Extract per-cell conversion data

Query PostHog for the primary metric broken down by cell:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      properties.variable_1_level AS var1,
      properties.variable_2_level AS var2,
      count(DISTINCT person_id) AS users,
      countIf(event = '{conversion_event}') AS conversions,
      conversions / users AS conversion_rate
    FROM events
    WHERE event IN ('mvt_cell_assigned', '{conversion_event}')
      AND properties.experiment_slug = '{slug}'
      AND timestamp BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY var1, var2
    ORDER BY conversion_rate DESC"
  }
}
```

Build a results table showing each cell's conversion rate, sample size, and confidence interval.

### 2. Compute main effects per variable

For each variable, compute its main effect by averaging across all levels of other variables:

- Variable 1 Level A effect = average conversion of all cells where var1 = A
- Variable 1 Level B effect = average conversion of all cells where var1 = B
- Main effect of Variable 1 = |Level A effect - Level B effect|

Rank variables by main effect size. The variable with the largest main effect is the most impactful lever. If a variable has a main effect close to zero, it does not matter for this metric -- document this finding and exclude it from future tests.

### 3. Detect interaction effects

An interaction effect occurs when the combination of two variables produces a result that differs from what their individual main effects would predict. Compute:

```
interaction = actual_cell_rate - (grand_mean + var1_main_effect + var2_main_effect)
```

If the interaction term is large relative to the main effects (>25% of the largest main effect), this is a meaningful interaction. Document it:

- **Synergy**: Combination performs better than main effects predict. Example: short copy + top placement converts 15%, but main effects predict only 11%. The combination has a synergistic interaction.
- **Conflict**: Combination performs worse than predicted. Example: urgent copy + delayed timing converts 5%, but main effects predict 9%. These variables interfere.

Use the `experiment-evaluation` fundamental to assess statistical significance of interaction terms. Only act on interactions that reach 90%+ confidence.

### 4. Rank all combinations

Sort all cells by conversion rate. The winning combination is the cell with the highest conversion rate AND statistical significance vs. the control (or vs. the baseline). If the top cell is not statistically significant, extend the test or declare no winner.

For each of the top 3 combinations, document:
- The exact variable levels
- Conversion rate and confidence interval
- Lift over baseline
- Whether the result is driven by main effects, interaction effects, or both

### 5. Generate the insight summary

Using the `experiment-evaluation` fundamental, produce a structured summary:

```json
{
  "experiment_slug": "{slug}",
  "status": "completed",
  "winner": {
    "cell": "var1=B, var2=top",
    "conversion_rate": 0.142,
    "lift_vs_baseline": "+3.2pp",
    "confidence": 0.97
  },
  "main_effects": [
    {"variable": "cta_copy", "best_level": "B", "effect_size": "+2.1pp"},
    {"variable": "placement", "best_level": "top", "effect_size": "+1.4pp"}
  ],
  "interactions": [
    {"variables": ["cta_copy", "placement"], "type": "synergy", "magnitude": "+0.8pp"}
  ],
  "recommendation": "Implement var1=B + var2=top. Run next MVT on timing and content length."
}
```

### 6. Implement the winner

Roll out the winning combination to 100% of users:

1. Update each feature flag to serve only the winning level using PostHog API
2. Track the `mvt_winner_deployed` event with the experiment slug and winning cell
3. Monitor the primary metric for 7 days post-deployment to confirm the lift holds in production (no novelty effect)
4. If the metric holds, clean up experiment flags and make the changes permanent in the codebase
5. If the metric decays >50% of the measured lift within 7 days, revert to the pre-experiment state and flag for investigation

### 7. Feed learnings into the next experiment

Using `n8n-workflow-basics`, store experiment results in a structured format:

- Append to a results log (Attio note or database record): slug, variables tested, winner, main effects, interactions, and next hypothesis
- Variables with large main effects are candidates for further optimization (test more levels)
- Variables with interaction effects should always be tested together in future MVTs
- Variables with no effect can be excluded from future tests on this metric

## Output

- Per-cell results table with conversion rates and confidence intervals
- Main effect rankings per variable
- Interaction effects identified and classified (synergy/conflict)
- Winning combination with implementation instructions
- Structured results log for institutional memory
