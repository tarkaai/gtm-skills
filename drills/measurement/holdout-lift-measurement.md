---
name: holdout-lift-measurement
description: Measure cumulative lift between holdout and treatment populations across all experiments over time
category: Measurement
tools:
  - PostHog
  - Anthropic
  - Attio
fundamentals:
  - posthog-holdout-group
  - posthog-retention-analysis
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - hypothesis-generation
  - attio-notes
---

# Holdout Lift Measurement

This drill measures the cumulative impact of all your experiments by comparing the treatment population (users who received optimizations) against the holdout group (users on the original unoptimized experience). Unlike individual A/B test results that show the effect of one change, holdout lift shows the compounded effect of every change you have shipped.

## Input

- A provisioned holdout group (output of `holdout-group-setup`)
- At least 2 weeks of data since holdout creation (4+ weeks preferred)
- Primary metrics: retention rate, engagement frequency, revenue per user, or conversion rate
- PostHog project with both cohorts tracked

## Steps

### 1. Pull cohort-level metrics from PostHog

Using `posthog-holdout-group`, run the holdout vs treatment comparison query for each primary metric. Query at minimum:

**Retention comparison:**
```sql
SELECT
  if(JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout', 'holdout', 'treatment') AS grp,
  dateTrunc('week', timestamp) AS week,
  uniqExact(distinct_id) AS active_users
FROM events
WHERE event IN ('{retention_event}')
  AND timestamp > now() - interval {window} week
GROUP BY grp, week
ORDER BY week, grp
```

**Revenue/conversion comparison:**
```sql
SELECT
  if(JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout', 'holdout', 'treatment') AS grp,
  count(DISTINCT distinct_id) AS users,
  countIf(event = '{conversion_event}') AS conversions,
  countIf(event = '{conversion_event}') / count(DISTINCT distinct_id) AS conversion_rate
FROM events
WHERE timestamp > now() - interval {window} week
GROUP BY grp
```

Run these queries using `posthog-cohorts` for the pre-built holdout and treatment cohorts.

### 2. Compute cumulative lift

For each metric, calculate lift as:

```
lift_pct = ((treatment_value - holdout_value) / holdout_value) * 100
```

Track lift over time by computing it weekly. The lift trend is as important as the current number:

- **Increasing lift:** Your experiments are compounding value. Each optimization builds on the last.
- **Flat lift:** Recent experiments are not adding incremental value. You may be near the local maximum.
- **Declining lift:** The holdout group is naturally improving (or the treatment group is degrading). Investigate.

### 3. Assess statistical significance

For each metric comparison, compute significance:

- Use a two-proportion z-test for conversion rates
- Use a two-sample t-test for continuous metrics (revenue, engagement frequency)
- Require p < 0.05 (95% confidence) before reporting lift as "confirmed"

If the holdout group is small (< 200 users), use Bayesian estimation instead of frequentist tests. Flag results with p between 0.05 and 0.10 as "directional but not confirmed."

Log significance assessment using `posthog-custom-events`:
- Event: `holdout_lift_measured`
- Properties: `metric_name`, `holdout_value`, `treatment_value`, `lift_pct`, `p_value`, `significant` (boolean), `measurement_window_weeks`

### 4. Build the holdout dashboard

Using `posthog-dashboards`, create a dedicated holdout measurement dashboard with these panels:

- **Cumulative lift trend:** Line chart showing lift_pct per week for each primary metric
- **Holdout vs treatment retention curves:** Overlaid retention curves for both groups
- **Experiment log:** Table of all experiments shipped since holdout creation, with their individual A/B test results and dates
- **Group health:** Holdout group size over time (should be stable), plus demographic parity check

### 5. Generate lift insights

Using the `hypothesis-generation` fundamental, pass the lift data to Claude:

```
Analyze the cumulative holdout lift data for this product.

Holdout group (no experiments): [holdout_metrics]
Treatment group (all experiments): [treatment_metrics]
Weekly lift trend: [lift_trend_json]
Experiments shipped: [experiment_log]

Questions to answer:
1. What is the total cumulative lift across all metrics?
2. Which experiments contributed most to the lift? (correlate experiment ship dates with lift changes)
3. Are there metrics where the holdout group is outperforming treatment? If so, why?
4. Is the lift trend accelerating, flat, or decelerating?
5. Recommendation: should we continue the current optimization strategy, pivot, or dissolve the holdout?
```

### 6. Store results and report

Store the lift measurement in Attio using `attio-notes`:
- Measurement date
- Lift values per metric with significance flags
- Trend classification (accelerating/flat/decelerating)
- Cumulative experiment count
- Recommendation

Log to PostHog for longitudinal tracking:
- Event: `holdout_lift_report`
- Properties: all metric lifts, trend classification, recommendation

## Output

- Weekly lift measurements with statistical significance for each primary metric
- PostHog dashboard showing holdout vs treatment performance over time
- Trend analysis showing whether optimizations are compounding
- Ranked attribution of which experiments drove the most cumulative lift
- Stored results in Attio with actionable recommendations

## When to Dissolve the Holdout

Consider dissolving the holdout group (letting all users receive optimizations) when:

- Cumulative lift is confirmed at 95% confidence across all primary metrics
- The lift trend has been stable or increasing for 8+ consecutive weeks
- You have shipped 10+ experiments, giving the holdout sufficient measurement value
- The opportunity cost of excluding holdout users from improvements exceeds the measurement value

To dissolve: disable the `global-holdout` feature flag, archive the cohorts, and document the final cumulative lift as the play's definitive outcome.

## Triggers

At Smoke: run once manually after 2+ weeks. At Baseline: run weekly via n8n cron. At Scalable+: run weekly with multi-metric analysis and automated dashboards.
