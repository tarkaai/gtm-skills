---
name: onboarding-health-monitor
description: Continuous per-persona onboarding health monitoring with anomaly alerts, cohort drift detection, and weekly automated reports
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Onboarding Health Monitor

This drill creates a continuous monitoring system for persona-based onboarding. It detects when any persona's activation rate drifts, identifies the root cause (tour abandonment, email disengagement, classification error), and generates actionable alerts. This drill feeds anomaly data into the `autonomous-optimization` drill for automated experimentation.

## Prerequisites

- Persona-based onboarding running at Scalable level with 5+ personas
- At least 8 weeks of per-persona activation data in PostHog
- n8n instance for scheduled monitoring workflows
- Attio configured for logging health observations

## Steps

### 1. Build the per-persona health dashboard

Using the `posthog-dashboards` fundamental, create a dashboard titled "Onboarding Health by Persona" with these panels:

- **Activation rate by persona (weekly trend)**: Line chart, one line per persona, 12-week window. Target line at the play's threshold.
- **Time to activation by persona (distribution)**: Histogram showing days from signup to activation per persona. Shift right = getting slower = problem.
- **Tour completion rate by persona**: Bar chart, weekly. A drop here causes downstream activation drops.
- **Email sequence engagement by persona**: Open rate and click rate per persona, weekly. Declining engagement signals content fatigue.
- **Persona classification distribution**: Pie chart of new signups by persona. A sudden shift means your user mix changed or classification rules broke.
- **Drop-off heatmap**: Table showing which tour step or email has the highest abandonment rate per persona. Updated weekly.

### 2. Define anomaly thresholds

For each metric, define what constitutes an anomaly:

| Metric | Normal range | Warning | Critical |
|--------|-------------|---------|----------|
| Activation rate per persona | Within 10% of 4-week rolling average | 10-20% below average for 1 week | >20% below average OR below play threshold for 2 weeks |
| Tour completion rate | Within 15% of average | 15-25% below for 1 week | >25% below OR below 40% absolute |
| Email open rate | Within 20% of average | 20-35% below for 1 week | >35% below OR below 15% absolute |
| Time to activation | Within 20% of median | 20-40% above median | >40% above median |
| Persona distribution | Within 15% of historical ratio | Any persona drops >50% of its usual share | Classification returning >30% "default" |

### 3. Build the daily monitoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs daily at 08:00 UTC:

1. Query PostHog for each persona's metrics from the last 7 days
2. Compare each metric against its 4-week rolling average (from `posthog-anomaly-detection`)
3. Classify each metric: normal, warning, or critical
4. If any metric is critical: send immediate alert (Slack or email) with the persona name, metric, current value, expected value, and suggested investigation steps
5. If any metric is warning: log to Attio using `attio-notes` as an observation on the play record
6. If all metrics normal: log a "healthy" status to Attio

The alert message format:
```
ONBOARDING ALERT: [persona_type] activation rate dropped to [X%] (expected [Y%])
- Tour completion: [Z%] (change: [delta])
- Email engagement: [open_rate%] open, [click_rate%] click
- Suggested cause: [tour step N has highest new dropoff | email M open rate collapsed | classification shifted]
- Recommended action: [investigate tour step N | refresh email M copy | check classification rules]
```

### 4. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

1. Pull 7-day metrics for each persona from PostHog
2. Pull 4-week trend data for comparison
3. Generate a structured report:

```
# Onboarding Health Report — Week of [date]

## Summary
- Total new signups: [N]
- Overall activation rate: [X%] (prev week: [Y%])
- Best persona: [persona] at [rate%]
- Worst persona: [persona] at [rate%]

## Per-Persona Breakdown
| Persona | Signups | Activation | Trend | Tour Complete | Email CTR |
|---------|---------|-----------|-------|---------------|-----------|
| ...     | ...     | ...       | ↑/↓/→ | ...           | ...       |

## Anomalies Detected
- [List of warning/critical anomalies with dates]

## Experiments in Flight
- [List any active A/B tests from autonomous-optimization]

## Recommended Actions
- [Prioritized list based on anomaly data]
```

4. Post the report to Slack and store in Attio as a note

### 5. Build cohort drift detection

Using `posthog-cohorts`, create a weekly cohort comparison workflow:

1. Compare this week's signup cohort against the 4-week historical average on: persona distribution, signup source distribution, company size distribution
2. If the profile of new signups shifts significantly (e.g., suddenly 40% of signups are a persona that was previously 15%), flag it as a cohort drift
3. Cohort drift is important because a tour optimized for one persona will not work for another — a shift in who signs up requires updating onboarding paths, not fixing them

Log cohort drift observations in Attio. These feed into the `autonomous-optimization` drill's diagnosis phase.

### 6. Connect to autonomous optimization

This drill's output feeds directly into the `autonomous-optimization` drill:

- **Anomaly detected** triggers the Diagnose phase of autonomous optimization
- **Anomaly type** determines hypothesis space: tour problem leads to test tour variations, email problem leads to test email copy, classification problem leads to fix classification rules
- **Weekly health report** provides the context data that hypothesis generation needs
- **Cohort drift** triggers a strategic review rather than tactical optimization

## Output

- Daily health check running automatically
- Critical anomaly alerts delivered within hours of detection
- Weekly structured health report with per-persona breakdown
- Cohort drift detection flagging changes in user mix
- Integration with autonomous-optimization for automated response to anomalies
