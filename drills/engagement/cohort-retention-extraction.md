---
name: cohort-retention-extraction
description: Extract structured retention data by signup cohort from PostHog, compute survival curves, and identify divergent cohorts
category: Retention
tools:
  - PostHog
  - Anthropic
fundamentals:
  - posthog-retention-analysis
  - posthog-cohorts
  - posthog-custom-events
---

# Cohort Retention Extraction

This drill pulls retention data from PostHog, structures it into cohort survival tables, and flags cohorts that diverge significantly from the population average. It produces the raw dataset that downstream drills (`cohort-insight-generation`, `autonomous-optimization`) consume.

## Input

- PostHog project with at least 8 weeks of user event data
- A defined "retained" event (the action that counts as a returning user — e.g., `$pageview`, `feature_used`, `session_started`)
- A cohort definition dimension: signup week (default), acquisition channel, plan type, or any PostHog person property

## Steps

### 1. Define the retention event and cohort dimension

Before querying, determine:

- **Retention event:** The event that signals a user came back. Use the most meaningful action for your product. `$pageview` works as a floor; a core feature event is better.
- **Cohort dimension:** How to group users. Default is `dateTrunc('week', person.created_at)` for signup-week cohorts. Alternatives: `properties.utm_source` for acquisition channel, `person.properties.plan` for plan type.
- **Time window:** 12 weeks of cohort data minimum for trend detection. Use 24 weeks if available.
- **Retention intervals:** Week 1 through Week 8 post-signup (8 retention checkpoints per cohort).

### 2. Run the cohort retention query

Use the `posthog-retention-analysis` fundamental to query cohort survival data. The query groups users by their cohort dimension and counts unique active users at each weekly interval after signup.

Output columns:
- `cohort_label` — the cohort identifier (e.g., "2026-W10", "organic", "pro_plan")
- `cohort_size` — number of users in the cohort at Week 0
- `week_1` through `week_8` — count of unique users who performed the retention event during each interval
- `week_1_pct` through `week_8_pct` — retention rate as percentage of cohort_size

### 3. Compute population baseline

Calculate the overall retention curve by averaging across all cohorts, weighted by cohort size:

For each week interval:
```
population_avg_week_N = SUM(week_N across all cohorts) / SUM(cohort_size across all cohorts)
```

This baseline is the "expected" retention for any given cohort. Deviations from this baseline are what generate insights.

### 4. Flag divergent cohorts

For each cohort, compare its retention curve to the population baseline. Flag a cohort as divergent when:

- **Outperformer:** Retention at week 4+ is 20% or more above the population average (e.g., population avg week 4 = 30%, cohort week 4 = 36%+)
- **Underperformer:** Retention at week 4+ is 20% or more below the population average
- **Early dropper:** Week 1 retention is 30%+ below population average (these users never activate)
- **Late churner:** Week 1-2 retention is normal but week 4+ drops 25%+ below population average (these users activate but do not stick)

Tag each divergent cohort with its divergence type and magnitude.

### 5. Structure the output

Produce a JSON document with this schema:

```json
{
  "extraction_date": "2026-03-30",
  "retention_event": "feature_used",
  "cohort_dimension": "signup_week",
  "time_window_weeks": 12,
  "population_baseline": {
    "week_1_pct": 45.2,
    "week_2_pct": 32.1,
    "week_4_pct": 22.8,
    "week_8_pct": 15.3
  },
  "cohorts": [
    {
      "cohort_label": "2026-W04",
      "cohort_size": 120,
      "retention": { "week_1_pct": 52.5, "week_2_pct": 38.3, "week_4_pct": 28.3, "week_8_pct": 19.2 },
      "divergence": { "type": "outperformer", "magnitude": 0.24, "first_detected_at": "week_4" }
    }
  ],
  "divergent_cohorts": ["2026-W04", "2026-W08"],
  "total_cohorts_analyzed": 12
}
```

Log the extraction as a PostHog event using `posthog-custom-events`:
- Event: `cohort_retention_extracted`
- Properties: `cohort_dimension`, `total_cohorts`, `divergent_count`, `extraction_date`

## Output

- Structured JSON with cohort survival data, population baseline, and divergent cohort flags
- PostHog event logging the extraction run
- Ready-to-consume input for `cohort-insight-generation` and `autonomous-optimization`

## Triggers

At Smoke level: run manually once. At Baseline: run weekly via n8n cron. At Scalable+: run weekly across multiple cohort dimensions in parallel.
