---
name: cohort-retention-health-monitor
description: Monitor cohort retention trends, detect degradation across dimensions, and surface anomalies for the optimization loop
category: Retention
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-retention-analysis
  - posthog-cohorts
  - posthog-dashboards
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# Cohort Retention Health Monitor

This drill builds the always-on measurement layer that tracks whether cohort retention is improving, stable, or degrading. It detects when specific cohort dimensions show anomalies, generates the data the `autonomous-optimization` drill consumes, and maintains a retention health dashboard.

## Input

- PostHog project with `cohort_retention_extracted` and `cohort_insight_generated` events flowing (from upstream drills)
- At least 8 weeks of cohort retention data
- n8n instance for scheduled monitoring
- Attio for logging health reports

## Steps

### 1. Build the cohort retention dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Overall retention curve | Line chart (weekly trend) | Population-level Week 1, 2, 4, 8 retention rates over time — are they trending up or down? |
| Retention by acquisition channel | Grouped bar chart | Compare Week 4 retention across acquisition channels — which channels produce sticky users? |
| Retention by plan type | Grouped bar chart | Compare Week 4 retention across plan types — does plan level predict retention? |
| New cohort quality | Line chart (trend) | Week 1 retention of each new signup cohort over time — is user quality improving or degrading? |
| Divergent cohort count | Trend line | Number of cohorts flagged as divergent each week — increasing divergence means the product serves some users well and others poorly |
| Insight-to-action pipeline | Funnel chart | Insights generated -> actioned -> tested -> validated — is the team closing the loop? |
| Intervention impact | Bar chart | Retention lift from actioned insights vs. control — are the interventions working? |

### 2. Create the weekly health check workflow

Using `n8n-scheduling`, build a workflow triggered by weekly cron:

1. Run `cohort-retention-extraction` across 3 dimensions: signup week, acquisition channel, plan type
2. For each dimension, use `posthog-anomaly-detection` to compare the latest 2-week retention metrics against the 8-week rolling average
3. Classify each dimension as: **improving** (retention up 5%+), **stable** (within +/-5%), **degrading** (retention down 5%+), **alarm** (retention down 15%+)
4. Aggregate into a health score: number of dimensions improving minus number degrading

### 3. Configure alerting thresholds

Using `n8n-triggers`, set up alerts:

- **Alarm:** Any dimension shows 15%+ retention degradation for 2 consecutive weeks. Action: send immediate alert, pause any running experiments on that dimension, and flag for the autonomous optimization loop.
- **Degradation warning:** Any dimension shows 5-15% degradation for 3 consecutive weeks. Action: log to Attio, add to the next optimization cycle's priority queue.
- **New cohort quality drop:** The most recent signup cohort's Week 1 retention is 20%+ below the 8-week average. Action: alert the marketing/growth team — the acquisition channel mix may have shifted to lower-quality users.

### 4. Generate weekly health brief

After the health check completes, generate a structured health brief:

```json
{
  "report_date": "2026-03-30",
  "overall_health": "stable",
  "health_score": 2,
  "dimensions": {
    "signup_week": { "status": "improving", "week_4_retention_current": 24.1, "week_4_retention_8wk_avg": 22.8, "change_pct": 5.7 },
    "acquisition_channel": { "status": "stable", "best_channel": "organic", "worst_channel": "paid_social", "gap_pp": 12.3 },
    "plan_type": { "status": "degrading", "degrading_segment": "free_tier", "change_pct": -7.2 }
  },
  "alerts": ["Free tier Week 4 retention declining 3 consecutive weeks"],
  "insights_pipeline": { "pending": 3, "actioned": 2, "tested": 1, "validated": 1 },
  "recommended_focus": "Investigate free-tier retention drop — possible cause: recent onboarding flow change on 2026-W11"
}
```

Log the brief to Attio using `attio-notes`. Post to the team's notification channel via n8n.

### 5. Feed the autonomous optimization loop

At Durable level, this monitor's output directly feeds the `autonomous-optimization` drill:

- When the monitor detects a degrading dimension, it becomes an anomaly that triggers the optimization loop's Phase 2 (Diagnose)
- The health brief's `recommended_focus` seeds the hypothesis generation context
- The intervention impact panel provides the evaluation data for Phase 4 (Evaluate)

Ensure the health check events are logged to PostHog so the autonomous optimization drill can query them:
- `cohort_health_check_completed` — properties: `overall_health`, `health_score`, `alert_count`, `report_date`
- `cohort_health_alert_fired` — properties: `dimension`, `alert_type`, `magnitude`, `cohort_label`

## Output

- 7-panel cohort retention dashboard in PostHog
- Weekly automated health check with dimension-level status classification
- Alerting pipeline for degradation and alarm conditions
- Structured health briefs logged to Attio
- PostHog events for the autonomous optimization loop to consume

## Triggers

Weekly via n8n cron. Dashboard is live and always accessible. Alerts fire in real-time when thresholds are breached during the weekly check.
