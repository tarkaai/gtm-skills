---
name: personalization-health-monitor
description: Continuously monitor personalization system health, detect degradation, and report on per-segment and per-surface performance
category: Experimentation
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - attio-lists
  - attio-custom-attributes
  - n8n-scheduling
  - n8n-workflow-basics
---

# Personalization Health Monitor

This drill builds the always-on monitoring system that watches the health of the personalization system and alerts when performance degrades. Unlike the `autonomous-optimization` drill (which runs experiments to improve), this drill focuses on detection and reporting — catching problems before they compound.

## Input

- Personalization system running at scale with event instrumentation (from `personalization-rule-engine` and `personalization-scaling-pipeline`)
- PostHog tracking personalization events (`personalization_surface_shown`, `personalization_surface_engaged`, etc.)
- At least 4 weeks of personalization performance data
- n8n instance for scheduled monitoring

## Steps

### 1. Define health metrics and thresholds

Establish baselines from 4 weeks of data. For each metric, set amber (warning) and red (critical) thresholds:

| Metric | Healthy | Amber | Red |
|--------|---------|-------|-----|
| Overall personalization engagement rate | >= 40% | 30-39% | < 30% |
| Per-segment engagement rate | Within 10pp of segment baseline | 10-20pp below | > 20pp below |
| Per-surface engagement rate | Within 15pp of surface baseline | 15-25pp below | > 25pp below |
| Fallback rate (unsegmented users) | < 10% | 10-20% | > 20% |
| Segment stability (weekly churn between segments) | < 15% | 15-25% | > 25% |
| Dynamic variant selection coverage | > 80% of sessions | 60-80% | < 60% |
| Email personalization delivery rate | > 95% | 90-95% | < 90% |
| LLM generation failure rate | < 2% | 2-5% | > 5% |

### 2. Build the daily health check pipeline

Using `n8n-scheduling`, create a workflow that runs daily at 08:00 UTC (after segmentation and scoring pipelines):

**Step 1 — Query aggregate health:**

Using `posthog-custom-events`:

```sql
SELECT
  toDate(timestamp) AS date,
  countIf(event = 'personalization_surface_shown') AS impressions,
  countIf(event = 'personalization_surface_engaged') AS engagements,
  engagements / greatest(impressions, 1) AS engagement_rate,
  countIf(event = 'personalization_fallback_used') AS fallbacks,
  fallbacks / greatest(impressions + fallbacks, 1) AS fallback_rate
FROM events
WHERE timestamp > now() - interval 7 day
GROUP BY date
ORDER BY date
```

**Step 2 — Query per-segment health:**

```sql
SELECT
  properties.segment AS segment,
  countIf(event = 'personalization_surface_shown') AS impressions,
  countIf(event = 'personalization_surface_engaged') AS engagements,
  engagements / greatest(impressions, 1) AS engagement_rate
FROM events
WHERE event IN ('personalization_surface_shown', 'personalization_surface_engaged')
  AND timestamp > now() - interval 7 day
GROUP BY segment
```

**Step 3 — Query per-surface health:**

```sql
SELECT
  properties.surface AS surface,
  properties.segment AS segment,
  countIf(event = 'personalization_surface_shown') AS impressions,
  countIf(event = 'personalization_surface_engaged') AS engagements,
  engagements / greatest(impressions, 1) AS engagement_rate
FROM events
WHERE event IN ('personalization_surface_shown', 'personalization_surface_engaged')
  AND timestamp > now() - interval 7 day
GROUP BY surface, segment
```

**Step 4 — Compare against thresholds:**

For each metric, classify as healthy / amber / red based on the thresholds from Step 1.

**Step 5 — Alert on degradation:**

- **Red alert:** Post to Slack immediately. Include: which metric, current value, threshold, affected segment/surface, link to PostHog dashboard.
- **Amber alert:** Log to Attio. Include in the weekly report. No immediate Slack notification unless 3+ amber alerts trigger on the same day.
- **Healthy:** Log to Attio. No alert.

### 3. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

1. **Aggregate 7-day metrics:** Pull all health metrics for the past week
2. **Compare to previous week:** Calculate week-over-week change for each metric
3. **Identify trends:** Flag metrics that have declined for 2+ consecutive weeks
4. **Per-segment deep dive:** For any segment with amber or red status, include:
   - Which surfaces are underperforming
   - User volume in the segment
   - Engagement trend (improving / stable / declining)
   - Recommendation (investigate, test new variant, re-segment)
5. **Generate the report:** Structure as:

```
## Personalization Health — Week of {date}

### Overall Status: {GREEN/AMBER/RED}
- Engagement rate: {rate}% ({change} vs last week)
- Fallback rate: {rate}%
- Active personalized users: {count}

### Segment Performance
| Segment | Users | Engagement | Trend | Status |
|---------|-------|------------|-------|--------|

### Surface Performance
| Surface | Impressions | Engagement | Trend | Status |
|---------|------------|------------|-------|--------|

### Alerts This Week
- {list of amber/red alerts with dates}

### Recommendations
- {actionable items based on data}
```

6. **Post to Slack** and store in Attio as a note on the personalization campaign record

### 4. Build retention correlation tracking

Using `posthog-cohorts`, create cohorts that track the relationship between personalization engagement and retention:

- `personalization-engaged-retained` — users who engaged with personalization AND are still active at 30 days
- `personalization-engaged-churned` — users who engaged but churned
- `personalization-not-engaged-retained` — users who did not engage but stayed
- `personalization-not-engaged-churned` — users who did not engage and churned

Compute weekly: personalization-engaged retention rate vs not-engaged retention rate. This is the core proof that personalization drives retention. If the gap narrows below 5pp, the personalization is not delivering enough differentiated value.

### 5. Monitor pipeline health

In addition to outcome metrics, monitor the infrastructure:

Using `posthog-anomaly-detection`:
- **Segmentation pipeline:** Did the `behavior_segment_assigned` event fire for the expected number of users today? If count drops >20% vs 7-day average, the pipeline may have failed.
- **Dynamic variant selection:** Did `personalization_dynamic_variant_selected` events fire at the expected volume? Compare to session count.
- **Email generation:** Did the LLM batch complete? Check for `personalization_email_dynamic_sent` event count vs expected.

Flag pipeline failures as red alerts immediately — a broken pipeline means users are getting fallback experiences.

## Output

- Daily automated health checks with threshold-based alerting
- Weekly health reports posted to Slack and stored in Attio
- Retention correlation tracking proving personalization impact
- Pipeline health monitoring detecting infrastructure failures
- Trend detection flagging multi-week declines before they become critical

## Triggers

- Daily health check: n8n cron, 08:00 UTC
- Weekly report: n8n cron, Monday 09:00 UTC
- Pipeline failure alerts: real-time via PostHog anomaly detection + n8n webhook
