---
name: poc-health-monitoring
description: Real-time POC health monitoring with predictive risk scoring, automated interventions, and portfolio-level visibility across all active POCs
category: Sales
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
  - Intercom
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-error-handling
  - attio-deals
  - attio-notes
  - attio-reporting
  - anthropic-api-patterns
  - intercom-in-app-messages
  - sandbox-usage-tracking
---

# POC Health Monitoring

This drill builds the real-time monitoring system that watches all active POCs simultaneously, scores each POC's health, predicts outcomes based on usage patterns, and triggers targeted interventions when a POC is at risk. It enables a single rep to manage 15-25+ concurrent POCs without losing visibility into any of them.

## Input

- Multiple active POCs with PostHog tracking configured (from `poc-governance-automation`)
- Sandbox usage events flowing (from `sandbox-usage-tracking` fundamental)
- POC success criteria stored in Attio for each deal
- n8n instance with PostHog, Attio, and Intercom integrations
- At least 8 weeks of historical POC outcome data (won/lost) for predictive modeling

## Steps

### 1. Build the POC portfolio dashboard

Using `posthog-dashboards`, create a single dashboard showing all active POCs:

**Panel 1 — POC Pipeline Overview:**
- Active POCs by health status (on-track / at-risk / stalled) as a stacked bar
- POCs starting this week vs. completing this week
- Average POC duration (actual vs. planned)

**Panel 2 — Criteria Progress Matrix:**
- Heatmap: each row is an active POC, each column is a criterion, cells are met/not-met/in-progress
- Sort by: days remaining (most urgent at top)

**Panel 3 — Engagement Trends:**
- Line chart: daily session count across all active POCs
- Scatter: engagement score vs. days into POC (identify outliers)

**Panel 4 — Conversion Funnel:**
- `poc_scoped` -> `poc_kickoff_completed` -> `poc_milestone_achieved` (3+) -> `poc_completed` (pass) -> `deal_won`
- Break down by POC duration, deal size, and industry

**Panel 5 — Intervention Effectiveness:**
- Track which interventions (email, in-app, call) improved POC health
- Measure: intervention triggered -> engagement increased within 48 hours

### 2. Build the predictive risk model

Create an n8n workflow that runs daily using `n8n-scheduling`:

1. Pull all historical POC data from PostHog using `posthog-cohorts`:
   - Cohort A: POCs where deal was won
   - Cohort B: POCs where deal was lost or stalled
2. Compare behavior patterns between cohorts:
   - Time to first login (won vs. lost)
   - Sessions in first 3 days (won vs. lost)
   - Criterion completion velocity (criteria met per day)
   - Own data uploaded (yes/no rate in won vs. lost)
   - Champion engagement pattern (increasing vs. flat vs. declining sessions)
3. Send the comparison data to Claude via `anthropic-api-patterns`:

```
Analyze these two POC cohorts and identify the top 5 behavioral signals that predict POC success vs. failure.

Won POC patterns: {won_data}
Lost POC patterns: {lost_data}

For each signal, provide:
- Signal name
- Won cohort average
- Lost cohort average
- Predictive weight (0-1, how strongly this signal predicts outcome)
- Detection threshold (at what point does this signal indicate risk?)

Return JSON array of signal objects.
```

4. Store the predictive model as an Attio note on the POC program record. Update monthly.

### 3. Apply risk scores to active POCs

For each active POC, run the predictive model:

1. Pull current usage data from PostHog.
2. Score against each predictive signal.
3. Calculate a composite risk score (0-100, where 100 = highest risk of failure).
4. Classify: Green (0-30), Yellow (31-60), Red (61-100).
5. Update the Attio deal with: `poc_risk_score`, `poc_risk_classification`, `poc_risk_signals` (list of triggered risk signals).

Fire PostHog event: `poc_risk_scored` with `deal_id`, `risk_score`, `classification`, `top_risk_signal`.

### 4. Configure automated interventions

Build n8n workflows using `n8n-triggers` that fire on specific risk signals:

**Signal: No login within 24 hours of kickoff**
- Action: Send Intercom in-app message (if the prospect is in product) via `intercom-in-app-messages`: "Your POC environment is ready. Here's what to try first: {milestone_1}."
- Action: Send email via Loops with walkthrough video and Cal.com quick-help link.

**Signal: Engagement declining (3+ consecutive sessions shorter than previous)**
- Action: Alert deal owner via Slack with specific data: "Sessions getting shorter at {company}. Last 3 sessions: {durations}. Recommend check-in call."
- Action: Show Intercom message: "Want a quick walkthrough of {feature_they_haven't_used}?"

**Signal: Milestone behind schedule by 3+ days**
- Action: Send targeted email: "I noticed you haven't had a chance to {milestone_name} yet. Here's a 2-minute guide: {link}. Or grab 15 minutes with me: {cal_link}."
- Action: Update Attio deal with blocker note.

**Signal: Risk score crosses from Green to Yellow**
- Action: Alert deal owner: "POC at {company} moved to Yellow. Risk signal: {signal}. Recommended action: {action}."
- Action: Auto-schedule a check-in call if none exists in the next 3 days.

**Signal: Risk score crosses from Yellow to Red**
- Action: Escalate to deal owner AND manager: "POC at {company} is Red. {days_remaining} days left, {criteria_met}/{total_criteria} criteria met. Immediate intervention recommended."
- Action: Auto-draft a direct message from the deal owner to the champion referencing specific stalled criteria.

### 5. Build the intervention tracking system

For every automated intervention:

1. Fire a PostHog event: `poc_intervention_triggered` with `deal_id`, `intervention_type`, `risk_signal`, `channel`.
2. Track whether the intervention produced a response within 48 hours (session activity increased, email replied, call booked).
3. Store intervention outcomes: `poc_intervention_effective` (boolean), `response_time_hours`, `engagement_delta`.

This data feeds back into the predictive model and intervention selection.

### 6. Generate the weekly POC portfolio brief

Using `n8n-scheduling`, run weekly on Monday mornings:

1. Aggregate all active POC metrics: count by health status, criteria completion rates, average risk score, interventions triggered and their effectiveness.
2. Identify the 3 POCs most at risk and the 3 most likely to close.
3. Send to Claude via `anthropic-api-patterns`:

```
Generate a weekly POC portfolio brief.

Active POCs: {count}
Health distribution: {green}/{yellow}/{red}
Criteria completion rate this week: {rate}
Interventions triggered: {count}, effective: {effective_count}

Top 3 at-risk POCs:
{risk_details}

Top 3 likely-to-close POCs:
{close_details}

Format:
1. Executive summary (3 sentences)
2. Portfolio health table
3. Action items for at-risk POCs (specific per deal)
4. Close-ready POCs with recommended next steps
Keep under 400 words.
```

Post to Slack and store in Attio.

## Output

- Real-time POC portfolio dashboard in PostHog
- Predictive risk scoring for every active POC
- Automated risk-based interventions (in-app, email, Slack alerts)
- Intervention effectiveness tracking
- Weekly POC portfolio brief

## Triggers

- Risk scoring: Runs daily via n8n cron
- Interventions: Fire in real-time based on PostHog events and risk score changes
- Portfolio brief: Runs weekly via n8n cron
