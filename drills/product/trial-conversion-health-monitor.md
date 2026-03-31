---
name: trial-conversion-health-monitor
description: Continuous monitoring of trial-to-paid conversion funnel with cohort analysis, churn-point detection, and automated weekly reports
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Trial Conversion Health Monitor

This drill creates a continuous monitoring system for free-trial-to-paid conversion. It detects when conversion rates drift by cohort, signup source, or plan tier, identifies the funnel step where users abandon, and generates actionable alerts. This drill feeds anomaly data into the `autonomous-optimization` drill for automated experimentation.

## Prerequisites

- Free trial optimization running at Scalable level with 500+ trial starts per month
- At least 8 weeks of trial conversion data in PostHog
- n8n instance for scheduled monitoring workflows
- Attio configured for logging health observations

## Steps

### 1. Build the trial conversion health dashboard

Using the `posthog-dashboards` fundamental, create a dashboard titled "Trial Conversion Health" with these panels:

- **Trial-to-paid conversion rate (weekly trend)**: Line chart, 12-week window, with target threshold line. Break out by signup source (organic, paid, referral, direct).
- **Time-to-conversion distribution**: Histogram showing days from trial start to paid conversion. A shift right means users are taking longer to decide — friction or weak value demonstration.
- **Trial activation rate**: Percentage of trial users who reach the activation milestone within 72 hours. This is the leading indicator of eventual conversion.
- **Upgrade prompt performance**: Impressions, clicks, and conversions for each upgrade trigger type (limit proximity, feature gate, time-based). A drop here means prompts are fatiguing or misaligned.
- **Churn-point funnel**: Multi-step funnel from trial_started -> activation_reached -> feature_explored -> upgrade_prompt_shown -> upgrade_started -> payment_completed. Identify the step with highest absolute drop-off.
- **Cohort retention heatmap**: Weekly cohorts showing trial user engagement over their trial period (Day 1, 3, 7, 14). Fading engagement predicts non-conversion.

### 2. Define anomaly thresholds

For each metric, define what constitutes an anomaly:

| Metric | Normal range | Warning | Critical |
|--------|-------------|---------|----------|
| Trial-to-paid conversion rate | Within 10% of 4-week rolling average | 10-20% below average for 1 week | >20% below average OR below play threshold for 2 weeks |
| Trial activation rate (72h) | Within 15% of average | 15-25% below for 1 week | >25% below OR below 50% absolute |
| Time-to-conversion median | Within 20% of historical median | 20-35% above median | >35% above median |
| Upgrade prompt CTR | Within 20% of average | 20-40% below for 1 week | >40% below OR below 2% absolute |
| Day-7 trial engagement | Within 15% of average | 15-30% below for 1 week | >30% below OR below 30% absolute |

### 3. Build the daily monitoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs daily at 08:00 UTC:

1. Query PostHog for trial conversion metrics from the last 7 days
2. Compare each metric against its 4-week rolling average (from `posthog-anomaly-detection`)
3. Classify each metric: normal, warning, or critical
4. If any metric is critical: send immediate alert with the metric name, current value, expected value, and suggested investigation steps
5. If any metric is warning: log to Attio using `attio-notes` as an observation on the play record
6. If all metrics normal: log a "healthy" status to Attio

The alert message format:
```
TRIAL CONVERSION ALERT: [metric_name] at [X%] (expected [Y%])
- Trial starts this week: [N]
- Activation rate (72h): [Z%] (change: [delta])
- Upgrade prompt CTR: [W%] (change: [delta])
- Suggested cause: [funnel step N has highest new dropoff | upgrade prompt fatigue detected | activation milestone unreachable for segment X]
- Recommended action: [investigate funnel step N | refresh prompt copy | review activation milestone definition]
```

### 4. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

1. Pull 7-day trial metrics from PostHog
2. Pull 4-week trend data for comparison
3. Generate a structured report:

```
# Trial Conversion Health Report — Week of [date]

## Summary
- Trial starts: [N] (prev week: [M])
- Conversion rate: [X%] (prev week: [Y%])
- Activation rate (72h): [Z%]
- Median time to conversion: [D] days

## Funnel Performance
| Step | Volume | Conversion | Week-over-Week |
|------|--------|-----------|----------------|
| Trial started | ... | 100% | ... |
| Activation reached | ... | ...% | ↑/↓/→ |
| Feature explored | ... | ...% | ↑/↓/→ |
| Upgrade prompt shown | ... | ...% | ↑/↓/→ |
| Upgrade started | ... | ...% | ↑/↓/→ |
| Payment completed | ... | ...% | ↑/↓/→ |

## Upgrade Prompt Performance
| Trigger Type | Impressions | CTR | Conversions |
|-------------|------------|-----|-------------|
| Limit proximity | ... | ...% | ... |
| Feature gate | ... | ...% | ... |
| Time-based | ... | ...% | ... |

## Anomalies Detected
- [List of warning/critical anomalies with dates]

## Experiments in Flight
- [List any active A/B tests from autonomous-optimization]

## Recommended Actions
- [Prioritized list based on anomaly data]
```

4. Post the report to Slack and store in Attio as a note

### 5. Build signup-source drift detection

Using `posthog-cohorts`, create a weekly cohort comparison workflow:

1. Compare this week's trial signups against the 4-week historical average on: signup source distribution, company size distribution, plan interest distribution
2. If the profile of new trial users shifts significantly (e.g., paid traffic drops 50% while organic rises), flag it as a cohort drift
3. Cohort drift matters because trial experiences optimized for one user type may not work for another — a shift in who starts trials requires updating onboarding, not fixing it

Log cohort drift observations in Attio. These feed into the `autonomous-optimization` drill's diagnosis phase.

### 6. Connect to autonomous optimization

This drill's output feeds directly into the `autonomous-optimization` drill:

- **Anomaly detected** triggers the Diagnose phase of autonomous optimization
- **Anomaly type** determines hypothesis space: activation problem leads to test onboarding variations, prompt problem leads to test prompt copy/timing, engagement problem leads to test re-engagement interventions
- **Weekly health report** provides the context data that hypothesis generation needs
- **Cohort drift** triggers a strategic review rather than tactical optimization

## Output

- Daily health check running automatically
- Critical anomaly alerts delivered within hours of detection
- Weekly structured health report with full funnel breakdown
- Signup-source drift detection flagging changes in trial user mix
- Integration with autonomous-optimization for automated response to anomalies

## Triggers

Runs continuously once configured. Daily monitoring workflow fires at 08:00 UTC. Weekly report fires Mondays at 09:00 UTC.
