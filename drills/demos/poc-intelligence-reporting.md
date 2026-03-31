---
name: poc-intelligence-reporting
description: Generate weekly POC intelligence reports correlating usage patterns with deal outcomes, tracking prediction accuracy, and surfacing optimization opportunities
category: Demos
tools:
  - PostHog
  - Attio
  - Anthropic
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-retention-analysis
  - posthog-anomaly-detection
  - attio-deals
  - attio-reporting
  - attio-notes
  - anthropic-api-patterns
  - n8n-scheduling
  - n8n-workflow-basics
---

# POC Intelligence Reporting

This drill produces weekly intelligence reports that synthesize POC usage data into actionable insights: which usage patterns predict closes, which POC structures work best, where the POC process itself needs improvement, and how prediction accuracy is trending. It runs alongside `autonomous-optimization` at the Durable level, feeding POC-specific context into the optimization loop.

## Input

- At least 12 weeks of POC outcome data in PostHog (won/lost/stalled)
- Deal outcomes tracked in Attio for completed POCs
- Active POC engagement scores updated by the `poc-health-monitoring` drill
- Predictive model from `poc-health-monitoring` with logged predictions

## Steps

### 1. Extract weekly POC metrics

Build an n8n workflow using `n8n-scheduling` that runs every Monday at 8 AM:

1. Query PostHog for the past 7 days:
   - POCs initiated (count)
   - POCs completed (count and pass/fail breakdown)
   - Criteria met across all active POCs (total and per-POC average)
   - Milestone completion rate (on-time vs. late)
   - Interventions triggered and effectiveness rate
   - Average risk score trend (this week vs. last 4 weeks)
   - Engagement score distribution (Green/Yellow/Red)

2. Query Attio using `attio-deals` and `attio-reporting` for the past 7 days:
   - Deals with POC that advanced to proposal
   - Deals with POC that went cold or lost
   - Average deal velocity: POC deals vs. non-POC deals
   - Win rate: POC deals vs. non-POC deals
   - Average deal size: POC deals vs. non-POC deals

### 2. Analyze POC structure effectiveness

Using `posthog-cohorts`, compare POC configurations to identify what works:

1. **Duration analysis**: Compare outcomes for 7-day vs. 14-day vs. 21-day POCs. Which duration produces the highest win rate per deal segment?
2. **Criteria analysis**: Which specific success criteria correlate most with won deals? Which criteria are being met but do not predict closes (noise)?
3. **Milestone analysis**: Are POCs with more milestones more successful? What is the optimal milestone count?
4. **Support model analysis**: Which check-in cadence (daily/bi-weekly/weekly) produces best outcomes? Do deals with more check-in calls close at higher rates?
5. **Engagement pattern analysis**: What is the engagement trajectory shape of won vs. lost POCs? (e.g., won POCs have rising engagement in week 2; lost POCs plateau after day 3)

Store the structural analysis as a PostHog insight and an Attio note.

### 3. Score prediction accuracy

For each POC that completed in the past 7 days:

1. Pull the risk score prediction that was active when the POC was at its midpoint.
2. Compare the prediction to the actual outcome.
3. Log accuracy: `poc_prediction_result` PostHog event with `deal_id`, `predicted_outcome`, `actual_outcome`, `confidence`, `accurate` (boolean).

Calculate rolling prediction accuracy:
- Last 4 weeks accuracy rate
- Accuracy by deal segment (size, industry, POC duration)
- Which predictive signals are most and least accurate

If accuracy drops below 65% for 2 consecutive weeks, flag the predictive model for retraining and include this in the weekly report.

### 4. Generate the weekly intelligence report

Send all data to Claude via `anthropic-api-patterns`:

```
Generate a weekly POC intelligence report from this data.

Weekly metrics:
{weekly_metrics_json}

POC structure analysis:
{structure_analysis_json}

Prediction accuracy:
{prediction_accuracy_json}

Completed POC outcomes this week:
{completed_pocs_json}

Active POC pipeline:
{active_pocs_json}

Report structure:
1. Executive Summary (3 sentences: POC program trend, highlight, concern)
2. Key Metrics vs. Prior Week (table with trend arrows)
3. POC Program Effectiveness:
   - Win rate for POC deals vs. non-POC deals
   - Average criteria achievement rate
   - Best-performing POC configuration (duration, criteria, support model)
4. Structural Recommendations:
   - Which POC configurations to use more or less of
   - Which criteria to add, modify, or retire
   - Optimal duration by deal segment
5. Pipeline Risk Report:
   - Active POCs needing attention with specific actions
   - Close-ready POCs with recommended next steps
6. Prediction Model Health:
   - Accuracy rate and trend
   - Signals performing well vs. poorly
   - Retrain recommendation if applicable

Keep under 600 words. Every recommendation must reference specific data.
```

### 5. Distribute and track

1. Post the report to the sales team Slack channel.
2. Store in Attio as a note on the POC program record.
3. For each at-risk active POC, send a direct Slack message to the deal owner with the specific recommended action from the report.
4. Log the report generation as a PostHog event: `poc_intelligence_report_generated` with `week`, `active_pocs`, `prediction_accuracy`, `poc_win_rate`.

### 6. Feed into the autonomous optimization loop

Extract the "Structural Recommendations" section and format it as optimization hypotheses compatible with the `autonomous-optimization` drill:

```json
{
  "source": "poc-intelligence-reporting",
  "hypotheses": [
    {
      "variable": "poc_duration",
      "current_value": "14 days",
      "proposed_value": "10 days",
      "rationale": "14-day POCs have same win rate as 10-day POCs but 40% longer sales cycle",
      "expected_impact": "Reduce average sales cycle by 4 days",
      "risk": "low"
    }
  ]
}
```

Store the hypotheses in Attio and pass them to the autonomous optimization loop for experiment design and execution.

## Output

- Weekly POC intelligence report with executive summary, effectiveness analysis, and structural recommendations
- Prediction accuracy tracking with retrain alerts
- Per-deal-owner alerts for at-risk POCs
- Optimization hypotheses formatted for the autonomous optimization loop

## Triggers

Runs weekly via n8n cron (Monday 8 AM). Prediction accuracy checks run on each POC completion.
