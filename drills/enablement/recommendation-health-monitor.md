---
name: recommendation-health-monitor
description: Monitor AI recommendation quality, adoption trends, and model drift to maintain recommendation system health
category: Enablement
tools:
  - PostHog
  - Anthropic
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - hypothesis-generation
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# Recommendation Health Monitor

This drill provides the play-specific monitoring layer for AI-powered recommendations. While `autonomous-optimization` handles the generic detect-hypothesize-experiment-evaluate loop, this drill tracks recommendation-specific health signals: model quality degradation, feature catalog staleness, segment drift, and suggestion fatigue. It feeds anomalies into the autonomous optimization loop and generates recommendation-specific weekly briefs.

## Input

- AI recommendation pipeline running at Scalable level for 4+ weeks
- PostHog tracking the full recommendation lifecycle (shown, clicked, adopted, dismissed)
- Behavioral clusters computed and assigned
- n8n instance for scheduled monitoring
- Attio for logging recommendations system health

## Steps

### 1. Define recommendation health metrics

Using `posthog-custom-events`, ensure these derived metrics are calculable:

| Metric | Formula | Healthy Range | Alert Threshold |
|--------|---------|---------------|-----------------|
| Overall adoption rate | adopted / shown | 15-40% | <12% for 2 weeks |
| Per-segment adoption rate | adopted / shown per cluster | Varies by segment | >30% below segment average |
| Suggestion quality score | (adopted + clicked) / shown | 25-50% | <20% for 2 weeks |
| Dismissal velocity | dismissals in first 3 seconds / shown | <15% | >25% (users dismiss without reading) |
| Feature catalog coverage | features recommended / total features | >60% | <40% (model fixating on few features) |
| Recommendation diversity | unique features recommended per week / total features | >50% | <30% (same recommendations cycling) |
| Segment distribution | recommendations per segment / total | Proportional to segment sizes | Any segment >2x its user share |
| Time to adoption | median days from shown to adopted | 1-5 days | >10 days (suggestions not compelling) |
| Repeat adoption | users who adopted 2+ recommendations / users who adopted 1+ | >30% | <15% (one-time curiosity, not sustained value) |

### 2. Build the recommendation health dashboard

Using `posthog-dashboards`, create a dashboard:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Adoption rate trend (28-day) | Line chart | Spot overall system degradation |
| Adoption rate by segment | Grouped bar chart | Which segments get value, which do not |
| Suggestion quality by feature | Heatmap (feature x week) | Which features produce good recommendations |
| Dismissal velocity trend | Line chart | Early indicator of content fatigue |
| Feature catalog coverage | Gauge | Is the model recommending broadly |
| Recommendation diversity (weekly) | Line chart | Is the model getting repetitive |
| Time to adoption distribution | Histogram | How quickly users act on suggestions |
| Segment drift monitor | Stacked area chart | Are cluster proportions stable |

### 3. Build the model quality monitoring workflow

Using `n8n-scheduling`, create a daily workflow:

1. Pull the last 7 days of recommendation events from PostHog
2. Compute all health metrics from Step 1
3. Compare each metric against its alert threshold
4. Classify system state:
   - **Healthy**: all metrics in range. Log to Attio, no action.
   - **Degrading**: 1-2 metrics breaching thresholds. Log alert, flag for next autonomous optimization cycle.
   - **Unhealthy**: 3+ metrics breaching OR adoption rate below 10%. Pause low-performing segments, trigger immediate diagnosis.

### 4. Detect feature catalog staleness

Using `posthog-custom-events`, track which features from the catalog are actually being recommended and whether users have already discovered them organically:

- **Stale features**: features in the catalog that have not been recommended in 30+ days (may be irrelevant or too niche)
- **Saturated features**: features where >80% of the target segment already uses them (recommending these wastes a recommendation slot)
- **Missing features**: new product features shipped in the last 30 days that are not in the recommendation catalog

Run this check weekly. Output a catalog health report:
- Features to remove (stale or saturated)
- Features to add (new, high-potential)
- Features to re-weight (high adoption rate when recommended, should be recommended more)

Log the report in Attio using `attio-notes`.

**Human action required:** When new product features ship, add them to the feature catalog with metadata (description, trigger event, prerequisite, benefit, plan). This is the one manual input the system requires.

### 5. Detect segment drift

Using `posthog-cohorts`, monitor whether behavioral clusters are stable:

- Re-run cluster assignment weekly using `behavior-cluster-computation` (via the `recommendation-personalization-pipeline` drill)
- Compare this week's cluster distribution to the 4-week rolling average
- Flag if any cluster grows or shrinks by >20% (user behavior is shifting)
- Flag if >10% of users change clusters week over week (segments are unstable)

If segment drift is detected, the recommendation strategies may need updating. Feed this signal into the `autonomous-optimization` drill as a hypothesis input.

### 6. Generate weekly recommendation system brief

Using `n8n-scheduling`, produce a weekly brief aggregating:

- Overall system health status (healthy/degrading/unhealthy)
- Adoption rate trend with week-over-week change
- Top 3 performing recommendations this week (feature, segment, adoption rate)
- Bottom 3 performing recommendations (candidates for removal or rewording)
- Feature catalog health: stale, saturated, and missing features
- Segment drift summary
- Estimated retention impact: users who adopted recommendations vs. comparable users who did not (retention rate difference)
- Recommended actions for next week

Post the brief to Slack and store in Attio.

## Output

- Recommendation health dashboard in PostHog (8 panels)
- Daily model quality monitoring workflow in n8n
- Weekly feature catalog health report
- Weekly segment drift detection
- Weekly recommendation system brief
- Anomaly signals fed into autonomous optimization loop

## Triggers

- Model quality monitoring: daily via n8n cron
- Feature catalog staleness check: weekly via n8n cron
- Segment drift detection: weekly (aligned with cluster re-computation)
- Weekly brief: Monday 9am via n8n cron
- Re-run full setup when the recommendation delivery mechanism changes, the feature catalog is overhauled, or cluster definitions are significantly revised
