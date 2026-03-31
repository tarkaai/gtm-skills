---
name: change-objection-intelligence-monitor
description: Continuous monitoring of change objection patterns, resolution effectiveness, readiness scoring accuracy, and change support asset performance across all deals
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - attio-deals
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# Change Objection Intelligence Monitor

This drill creates the play-specific monitoring layer for change management objection handling at Durable level. It tracks resistance patterns, resolution effectiveness, change readiness scoring accuracy, and support asset performance — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `change_resistance_extracted` and `change_objection_resolved` events
- Attio CRM with structured change resistance data on deal records
- n8n instance for scheduling
- This drill runs alongside `autonomous-optimization` — it provides the domain-specific metrics and hypotheses that the optimization loop acts on

## Steps

### 1. Build the change objection intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "Change Management Intelligence" with these panels:

**Panel 1 — Change objection resolution rate (weekly trend)**
- Query: `change_objection_resolved` events / total `change_resistance_extracted` events
- Chart: line graph, 12-week view
- Alert: if resolution rate drops below 55% for 2 consecutive weeks

**Panel 2 — Root cause distribution (stacked bar)**
- Query: `change_resistance_extracted` events grouped by `primary_root_cause`
- Chart: stacked bar, weekly buckets
- Shows which resistance types are increasing or decreasing over time

**Panel 3 — Resolution method effectiveness (heatmap)**
- Query: `change_objection_resolved` events, group by `root_cause` x `resolution_method`
- Chart: heatmap showing resolve rate per intervention per root cause
- Identifies which interventions work best for each resistance type

**Panel 4 — Time to resolution (histogram)**
- Query: `days_to_resolution` property on `change_objection_resolved` events
- Chart: histogram with 3-day buckets
- Target: 80th percentile under 14 days

**Panel 5 — Change readiness score accuracy (scatter)**
- Query: deals with `change_readiness_scored` event, plot predicted score vs actual outcome (resolved/lost/stalled)
- Shows whether the scoring model is correctly predicting change difficulty

**Panel 6 — Asset engagement rates (bar)**
- Query: `change_support_engaged` events grouped by `asset_type`
- Chart: bar chart showing engagement rate per asset type
- Identifies which assets prospects actually read vs ignore

**Panel 7 — Resolution funnel (funnel)**
- Funnel: `change_resistance_extracted` -> `change_support_delivered` -> `change_support_engaged` -> `change_objection_resolved` -> `deal_closed_won`
- Shows the full conversion path from resistance detection to deal close

**Panel 8 — Revenue impact (scorecard)**
- Query: total deal value of `deal_closed_won` events where the deal had `change_resistance_extracted` events
- Compare to: deal value of `deal_closed_lost` with change resistance (shows salvage rate)
- Shows: average deal size, close rate, and cycle length for change-resistant vs clean deals

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of change management metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Resolution rate: flag if drops >15% from 4-week rolling average
   - Root cause concentration: flag if any single root cause exceeds 50% of all resistance signals (suggests a systematic issue: maybe the product, market, or sales process changed)
   - Asset engagement: flag if engagement rate for any asset type drops below 20% (asset fatigue or quality degradation)
   - Readiness score drift: flag if the correlation between predicted readiness and actual outcomes drops below 0.5
   - Time to resolution: flag if 80th percentile exceeds 21 days (interventions are taking too long)
3. For each detected anomaly, log to Attio and fire a PostHog event:

```json
{
  "event": "change_objection_anomaly_detected",
  "properties": {
    "anomaly_type": "resolution_rate_drop|root_cause_concentration|asset_fatigue|scoring_drift|slow_resolution",
    "metric_name": "resolution_rate",
    "current_value": 0.48,
    "baseline_value": 0.65,
    "change_percentage": -26.2,
    "severity": "warning|critical"
  }
}
```

### 3. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with change-management-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current resolution method effectiveness rankings
- Root cause distribution trends
- Change readiness scoring accuracy
- Asset engagement data
- Recent deal context (are deals getting larger? new industries? new competitor?)

The hypothesis generator will produce 3 ranked hypotheses. Examples:

- "Resolution rate dropped because disruption_fear resistance increased 40%. The change support plan template hasn't been updated since initial build. Experiment: regenerate change support plans with updated implementation timelines and new case study data."
- "Asset engagement for migration_scope_document dropped from 65% to 30%. Experiment: replace PDF attachment with an interactive migration calculator that prospects can explore."
- "Change readiness scoring over-predicts risk for companies with recent funding rounds. Experiment: increase the negative weight for recent_funding from -5 to -10 and re-score."
- "past_failure root cause has the lowest resolution rate (38%). Current intervention leads with empathy email. Experiment: lead with a reference call offer instead (social proof before content)."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 4. Build weekly change intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all change management data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: best/worst metric this week",
    "resolution_rate": {"current": 0.62, "trend": "improving", "vs_target": "+2%"},
    "top_intervention": {"root_cause": "disruption_fear", "method": "phased_plan", "resolve_rate": 0.78, "sample_size": 9},
    "worst_intervention": {"root_cause": "political_dynamics", "method": "exec_one_pager", "resolve_rate": 0.25, "sample_size": 4},
    "root_cause_shift": "past_failure increased from 15% to 28% of resistance signals",
    "readiness_model_accuracy": {"correlation": 0.72, "trend": "stable"},
    "asset_engagement": {"best": "change_support_plan (78%)", "worst": "migration_scope_doc (22%)"},
    "deals_at_risk": [{"deal_name": "...", "risk_reason": "...", "readiness_score": 0}],
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": 4}]
  }
}
```

3. Post the report to Slack and store in Attio as a note on the "Change Management Objection" campaign record

### 5. Feed the optimization loop

The key output of this drill is structured metric data that the `autonomous-optimization` drill can act on:

- Anomaly alerts trigger the optimization loop's Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- The weekly report provides Phase 5 (Report) content
- Resolution method effectiveness data informs which variables to experiment on next
- Readiness scoring accuracy data drives model weight adjustments

Without this monitoring drill, `autonomous-optimization` would lack the change-management-specific context needed to generate useful hypotheses.

## Output

- PostHog dashboard with 8 panels tracking all change management metrics
- Daily anomaly detection with automated alerts
- Domain-specific hypothesis generation for the optimization loop
- Weekly change intelligence report
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Weekly report: Monday 9 AM cron via n8n
- Hypothesis generation: triggered by anomaly detection
