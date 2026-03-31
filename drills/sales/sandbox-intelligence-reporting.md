---
name: sandbox-intelligence-reporting
description: Generate weekly sandbox intelligence reports correlating usage patterns with deal outcomes and surfacing optimization opportunities
category: Sales
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

# Sandbox Intelligence Reporting

This drill produces weekly intelligence reports that synthesize sandbox usage data into actionable insights for the sales team: which usage patterns predict closes, which prospects need intervention, and where the sandbox experience itself needs improvement. It runs alongside `autonomous-optimization` at the Durable level, feeding play-specific context into the optimization loop.

## Input

- At least 8 weeks of sandbox usage data in PostHog
- Deal outcomes (won/lost/stalled) tracked in Attio for closed sandboxes
- Active sandbox engagement scores updated by the `sandbox-usage-monitoring` drill

## Steps

### 1. Extract weekly sandbox metrics

Build an n8n workflow using `n8n-scheduling` that runs every Monday at 8 AM:

1. Query PostHog using `posthog-dashboards` for the past 7 days:
   - Sandboxes provisioned (count)
   - First logins (count and percentage of provisioned)
   - Active sandboxes (at least 1 session this week)
   - Milestones completed (total and per-sandbox average)
   - Features used (total unique features across all sandboxes)
   - Errors encountered (count by type)
   - Engagement score distribution (Cold/Warm/Hot/Champion)

2. Query Attio using `attio-deals` for the past 7 days:
   - Deals with sandbox that advanced stage
   - Deals with sandbox that went cold or lost
   - Average deal velocity for sandbox vs. non-sandbox deals

### 2. Build the predictive model

Using `posthog-cohorts` and `posthog-retention-analysis`, analyze historical sandbox data to identify the usage patterns that predict deal outcomes:

1. Create cohorts: "Sandbox deals that closed won" vs. "Sandbox deals that closed lost."
2. Compare the two cohorts across every sandbox metric:
   - Time to first login
   - Session count in first 7 days
   - Features used in first 3 sessions
   - Whether own data was uploaded
   - Milestone completion rate
   - Engagement score trajectory (rising vs. flat vs. declining)

3. Identify the top 3-5 predictive signals. Example findings:
   - "Prospects who upload their own data within 5 days close at 3.2x the rate of those who don't."
   - "3+ completed workflows in the first week predicts close with 78% accuracy."

Update the predictive model monthly as more outcome data accumulates.

### 3. Score current pipeline

For each active sandbox, apply the predictive model to generate a close probability:

1. Pull current usage data from PostHog for each active sandbox.
2. Score against the predictive signals identified in step 2.
3. Classify each sandbox deal: "Likely to close" (>60%), "Needs attention" (30-60%), "At risk" (<30%).
4. Update the classification in Attio on each deal using `attio-notes`.

### 4. Generate the weekly intelligence report

Send the weekly metrics and pipeline scores to Claude via `anthropic-api-patterns`:

```
Generate a weekly sandbox intelligence report from this data.

Metrics this week:
{weekly_metrics_json}

Pipeline scores:
{pipeline_scores_json}

Predictive model findings:
{predictive_signals}

Report structure:
1. Executive Summary (3 sentences: trend, highlight, concern)
2. Key Metrics vs. Prior Week (table with direction arrows)
3. Pipeline Risk Report (list deals needing attention with specific recommended actions)
4. Sandbox Experience Issues (any errors, friction points, or drop-off patterns detected)
5. Optimization Opportunities (what to test or change based on this week's data)
6. Close Predictions (which deals are most likely to close this week and why)

Keep it under 500 words. Focus on actions, not description.
```

### 5. Distribute the report

1. Post to the sales team Slack channel.
2. Store in Attio as a note on the "Sandbox Program" campaign record.
3. For each "Needs attention" deal, send a direct Slack message to the deal owner with the specific recommended action.

### 6. Track report accuracy

Log each weekly prediction as a PostHog event:

```json
{
  "event": "sandbox_intelligence_prediction",
  "properties": {
    "deal_id": "...",
    "predicted_outcome": "likely_close",
    "confidence": 0.72,
    "report_week": "2026-W14"
  }
}
```

After deals close, compare predictions to outcomes. Track prediction accuracy over time. If accuracy drops below 65%, flag the predictive model for retraining.

## Output

- Weekly sandbox intelligence report with executive summary, pipeline risk assessment, and optimization opportunities
- Per-deal close probability scores updated in Attio
- Direct deal-owner alerts for at-risk sandboxes
- Prediction accuracy tracking over time

## Triggers

Runs weekly via n8n cron (Monday 8 AM). The predictive model retrains monthly.
