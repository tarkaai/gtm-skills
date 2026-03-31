---
name: churn-model-health-monitor
description: Monitor churn prediction accuracy, intervention save rates, and model calibration drift
category: Retention
tools:
  - PostHog
  - Anthropic
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Churn Model Health Monitor

This drill monitors the performance of the churn prediction model itself: is it predicting accurately, are interventions working, and is the model drifting out of calibration? This is distinct from the `autonomous-optimization` drill (which optimizes the play's overall KPIs) -- this drill specifically monitors the prediction machinery.

## Input

- Churn risk scores being generated daily by `churn-signal-extraction`
- Intervention outcomes being tracked by `churn-intervention-routing`
- At least 4 weeks of scoring + outcome data (for meaningful accuracy measurement)
- PostHog dashboards configured for churn metrics

## Steps

### 1. Build the churn model dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Prediction Accuracy (weekly)**
- True Positive Rate: users scored high-risk who actually churned
- False Positive Rate: users scored high-risk who did not churn
- True Negative Rate: users scored low-risk who retained
- False Negative Rate: users scored low-risk who actually churned (MOST DANGEROUS -- missed churners)

Query via HogQL: compare `churn_risk_scored` events from 30 days ago against actual churn events in the following 30 days.

**Intervention Effectiveness (weekly)**
- Save rate by risk tier: percentage of intervened users who re-engaged
- Save rate by intervention type: which intervention channels work best
- Save rate by primary signal: which churn signals respond best to intervention
- Cost per save: total intervention cost / number of saved users

**Model Calibration (monthly)**
- For each risk tier, what percentage actually churned?
  - Expected: critical (76-100) -> 70%+ churn rate, high (51-75) -> 40-60%, medium (26-50) -> 15-30%, low (0-25) -> <10%
- If actual churn rates diverge from expected by >15 percentage points, the model needs recalibration

**Population Distribution (daily)**
- How many users are in each risk tier?
- If critical+high exceeds 30% of active users, something systemic is wrong (product issue, not a prediction issue)

### 2. Set up automated health checks

Using `n8n-scheduling`, create a weekly workflow that:

1. Queries PostHog for the past week's prediction accuracy metrics
2. Compares against thresholds:
   - False negative rate must stay below 15% (missing too many churners)
   - Save rate must stay above 10% (interventions must be working)
   - Critical+high population must stay below 30% of active users
3. If any threshold is breached, generate an alert with the specific metric and its value
4. If all thresholds pass, log a health check pass

### 3. Detect calibration drift

Using `posthog-anomaly-detection`, monitor the churn model's accuracy metrics for trends. The model can drift when:

- **Product changes:** A new feature launch changes usage patterns, making old signals unreliable
- **Seasonal effects:** Usage naturally declines during holidays, inflating false positives
- **Audience shift:** Different user cohorts have different churn patterns

When drift is detected, use `hypothesis-generation` to diagnose the cause and recommend recalibration steps.

### 4. Generate the weekly churn intelligence brief

Using the Anthropic API, generate a weekly report summarizing:

- Total users scored this week, broken down by risk tier
- Prediction accuracy: true positive rate, false negative rate
- Intervention save rate: overall and by tier
- Notable changes: any new patterns in why users are churning
- Recommended actions: recalibrate model, adjust intervention templates, escalate product issues

Post to Slack and store in Attio.

## Output

- PostHog dashboard with 4 panel groups monitoring model health
- Weekly automated health check with threshold alerts
- Calibration drift detection with diagnosis
- Weekly churn intelligence brief

## Triggers

- Dashboard: real-time, always accessible
- Health check: weekly via n8n cron (Mondays)
- Calibration drift check: monthly via n8n cron
- Intelligence brief: weekly, generated after the health check
