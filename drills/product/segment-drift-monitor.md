---
name: segment-drift-monitor
description: Continuously monitor behavioral segment quality, detect segment drift, and trigger cluster refresh when segments degrade
category: Product
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-dashboards
  - posthog-anomaly-detection
  - attio-notes
  - n8n-workflow-basics
  - n8n-scheduling
  - hypothesis-generation
---

# Segment Drift Monitor

This drill watches for degradation in behavioral segment quality over time. As the product evolves and user behavior shifts, segments that were once distinct may merge, split, or lose predictive power. The drift monitor detects these changes early and triggers corrective action before personalization effectiveness erodes.

This drill is specific to the AI Behavior Segmentation play at the Durable level. It runs alongside `autonomous-optimization` (which handles the broader experiment-evaluate-implement loop) and focuses narrowly on whether the segment taxonomy itself remains valid.

## Input

- Behavioral segment assignments stored in PostHog (from `behavior-segmentation-pipeline`)
- At least 8 weeks of historical segment assignments for trend analysis
- PostHog dashboards tracking segment distribution and retention per segment
- n8n instance for scheduling monitoring workflows
- Anthropic API key for drift diagnosis

## Steps

### 1. Compute weekly segment health metrics

Using `posthog-custom-events`, compute these metrics every week for each segment:

**Segment stability:**
```sql
SELECT
  behavior_segment_id,
  count(DISTINCT person_id) AS current_members,
  countIf(behavior_segment_changed_this_week = true) AS members_who_moved,
  members_who_moved / greatest(current_members, 1) AS churn_rate_from_segment
FROM (
  SELECT
    person_id,
    properties.behavior_segment_id AS behavior_segment_id,
    properties.behavior_segment_id != properties.previous_segment_id AS behavior_segment_changed_this_week
  FROM events
  WHERE event = 'behavior_segment_assigned'
    AND timestamp > now() - interval 7 day
)
GROUP BY behavior_segment_id
```

Target: <25% of any segment's members should move to a different segment in a given week. Higher instability means the boundary between segments is fuzzy.

**Segment size balance:**
- Track the member count per segment as a percentage of total active users
- Flag if any segment grows above 40% (too broad to personalize meaningfully) or shrinks below 5% (too small to justify a distinct experience)

**Retention divergence:**
- Compute 14-day retention rate per segment
- Calculate the spread: max_retention - min_retention
- Flag if the spread drops below 10pp (segments are not capturing retention-relevant differences)

**Personalization engagement:**
- Pull `segment_message_clicked` and `segment_tour_completed` events per segment
- If click-through rate converges across segments (within 2pp of each other), the personalization is not differentiated enough

### 2. Define drift thresholds

Store these as configuration in the n8n workflow:

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Segment stability (weekly churn from segment) | <25% | 25-40% | >40% |
| Largest segment size | <40% | 40-55% | >55% |
| Smallest segment size | >5% | 3-5% | <3% |
| Retention spread across segments | >15pp | 10-15pp | <10pp |
| Personalization CTR spread | >5pp | 2-5pp | <2pp |
| Unclassified user rate | <10% | 10-20% | >20% |

### 3. Build the weekly monitoring workflow

Using `n8n-scheduling`, create a workflow triggered every Monday at 07:00 UTC:

1. Query PostHog for all segment health metrics (step 1)
2. Evaluate each metric against drift thresholds (step 2)
3. Classify overall segment health: **Healthy** (all normal), **Degrading** (any warning), **Drifted** (any critical)
4. If Healthy: log metrics, no action needed
5. If Degrading: generate a drift diagnosis (step 4) and log a warning
6. If Drifted: trigger cluster refresh and alert the team

### 4. Diagnose drift causes

When metrics hit Warning or Critical, use the `hypothesis-generation` fundamental to identify root causes:

```
Segment health is degrading. Here is the current state:
- Segment stability: {stability_data}
- Retention spread: {retention_data}
- Personalization engagement: {engagement_data}
- Recent product changes: {changelog_summary}
- User base growth rate: {growth_data}

Why are the segments losing distinctiveness? Generate 3 hypotheses:
1. What changed in user behavior or product that caused drift
2. How confident you are in this hypothesis
3. What corrective action to take
```

Common drift causes:
- **Product change:** A new feature shifted user workflows, making old segments irrelevant
- **User base composition change:** Growth from a new channel brought users with different behavior patterns
- **Seasonal shift:** Usage patterns change by quarter (common in B2B)
- **Segment convergence:** Two segments became more similar as users in both adopted the same features

### 5. Trigger corrective actions

Based on drift severity:

**Degrading (Warning):**
- Re-run cluster discovery with fresh 30-day behavior data
- Compare new clusters to existing clusters: if >80% overlap, the original taxonomy is still valid -- adjust boundaries only
- Update personalization content to better match evolved segment profiles
- Log the adjustment in Attio using `attio-notes`

**Drifted (Critical):**
- Pause personalized in-app messages to avoid irrelevant targeting
- Run full cluster discovery from scratch
- Assign all users to new segments
- Rebuild personalization matrix with new segment definitions
- Restart personalization routing with the new taxonomy
- Fire `segmentation_model_reset` event in PostHog

### 6. Build the segment health dashboard

Using `posthog-dashboards`, add panels:

- **Segment distribution over time:** Stacked area chart showing each segment's share of active users (should be stable)
- **Segment stability trend:** Line chart of weekly churn-from-segment rate per cluster
- **Retention by segment:** Line chart of 14-day retention per segment (lines should be separated, not converging)
- **Personalization CTR by segment:** Bar chart showing engagement with personalized touchpoints per segment
- **Drift status indicator:** Single value showing current drift classification (Healthy / Degrading / Drifted)
- **Unclassified user trend:** Line chart of unclassified percentage over time

### 7. Generate weekly segment health brief

Compile a weekly report:

```json
{
  "report_date": "2026-03-30",
  "drift_status": "healthy",
  "segments": [
    {
      "label": "Power Collaborator",
      "member_count": 234,
      "pct_of_users": 0.18,
      "stability": 0.88,
      "retention_14d": 0.72,
      "personalization_ctr": 0.15
    }
  ],
  "alerts": [],
  "recommended_actions": [],
  "model_age_weeks": 6,
  "next_scheduled_refresh": "2026-04-01"
}
```

Store the report as an Attio note on the segmentation campaign record. Post a summary to Slack if the team uses it.

## Output

- Weekly segment health metrics computed and stored in PostHog
- Drift detection with automatic classification (Healthy / Degrading / Drifted)
- AI-generated drift diagnosis when degradation is detected
- Automatic corrective actions: cluster refresh, personalization pause, or full model reset
- Segment health dashboard in PostHog
- Weekly health briefs stored in Attio

## Triggers

- Weekly health check: n8n cron, Monday 07:00 UTC
- On-demand health check: webhook trigger for manual runs
- Drift alert: fires immediately when any metric hits Critical threshold
