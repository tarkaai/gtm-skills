---
name: signup-funnel-health-monitor
description: Always-on monitoring of signup funnel health with anomaly detection, regression alerts, and weekly optimization briefs
category: Onboarding
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-custom-events
  - posthog-dashboards
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Signup Funnel Health Monitor

This drill creates an always-on monitoring system for the signup funnel. It detects conversion regressions within hours, identifies which segment or step degraded, and generates weekly optimization briefs that feed into the `autonomous-optimization` drill.

## Input

- PostHog signup funnel events flowing (from `signup-funnel-audit`)
- Baseline metrics established for at least 4 weeks
- n8n instance for scheduled monitoring
- Attio CRM for logging monitoring results

## Steps

### 1. Build the signup health dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Panel 1 — Overall Signup CVR Trend** (line chart, 90-day view)
- Metric: `signup_completed / signup_page_viewed` per day
- Include 7-day rolling average to smooth daily noise
- Add horizontal line at the pass threshold (target CVR)

**Panel 2 — Funnel Step Conversion Rates** (stacked bar chart, 30-day view)
- Each step's conversion rate as a separate series
- Shows where the funnel is tightening or loosening

**Panel 3 — Signup CVR by Segment** (table, 30-day view)
- Rows: traffic source, device type, signup method
- Columns: visitors, signups, CVR, change vs prior 30 days
- Sort by absolute signup volume descending

**Panel 4 — Form Error Rate** (line chart, 30-day view)
- `signup_form_field_error` events / `signup_form_focused` events per day
- Spike = form or validation regression

**Panel 5 — Time to Complete Signup** (histogram, 30-day view)
- Distribution of `time_to_complete_seconds` from `signup_completed` events
- Median and p95 annotated
- Increasing median = new friction introduced

**Panel 6 — Email Verification Rate** (line chart, 30-day view)
- `email_verification_completed / signup_completed` per day
- Drop = deliverability problem or verification UX regression

### 2. Build daily anomaly detection workflow

Using `n8n-scheduling`, create a workflow that runs at 9 AM daily:

1. Query PostHog API for signup funnel metrics over the last 7 days
2. Compare each metric against the 4-week rolling baseline
3. Classify each metric:
   - **Normal**: within +/- 15% of baseline
   - **Warning**: 15-25% below baseline for 2+ consecutive days
   - **Critical**: >25% below baseline for 1+ days OR signup_completed = 0 for any 12-hour window

4. For Warning/Critical alerts, include in the notification:
   - Which metric degraded
   - By how much (absolute and percentage)
   - Which segments are affected (break down by device, source)
   - Most recent `signup_form_error` or `signup_form_field_error` events (could be a bug)
   - Link to the PostHog dashboard

5. Route alerts: Critical → Slack #engineering + #product. Warning → Slack #product only.

### 3. Build regression detection for deployments

Using `n8n-workflow-basics`, create a webhook-triggered workflow that fires after each production deployment:

1. Record the deployment timestamp
2. Wait 4 hours
3. Compare signup CVR in the 4 hours post-deploy against the 4 hours pre-deploy
4. If CVR dropped >20%: send a Critical alert with the deployment timestamp and the metric delta
5. This catches bugs in signup flow code that automated tests may miss

### 4. Generate weekly optimization brief

Using `n8n-scheduling`, create a weekly workflow that runs Monday at 8 AM:

1. Pull 7-day signup funnel data from PostHog broken down by day, segment, and step
2. Calculate week-over-week changes for every metric
3. Generate a structured brief:

```
## Signup Funnel Weekly Brief — Week of [DATE]

### Overall
- Signup CVR: [X]% (prev: [Y]%, change: [+/-Z]pp)
- Total signups: [N] (prev: [M])
- Email verification rate: [X]%

### Top Finding
[The single most important insight: biggest improvement, biggest regression, or emerging trend]

### Step-by-Step Changes
| Step | This Week | Last Week | Change |
|------|-----------|-----------|--------|
| Page → Form Start | | | |
| Form Start → Submit | | | |
| Submit → Complete | | | |
| Complete → Verified | | | |

### Segment Highlights
- Best segment: [segment] at [CVR]%
- Worst segment: [segment] at [CVR]%
- Biggest change: [segment] [improved/declined] by [X]pp

### Active Experiments
[List any running A/B tests with current data]

### Recommended Actions
1. [Action based on data]
2. [Action based on data]
```

4. Post to Slack and store in Attio as a campaign note

### 5. Build experiment impact tracking

After any `autonomous-optimization` experiment concludes, this monitor:

1. Records the pre-experiment and post-experiment CVR
2. Calculates the net lift attributable to the change
3. Maintains a cumulative optimization log: every change, its lift, and the running total improvement since the play started
4. Includes the cumulative log in each weekly brief

## Output

- PostHog dashboard with 6 panels covering all aspects of signup funnel health
- Daily anomaly detection with tiered alerting (Warning, Critical)
- Deployment regression detection (webhook-triggered)
- Weekly optimization brief with data, insights, and recommended actions
- Cumulative experiment impact log

## Triggers

- Daily monitoring: 9 AM cron via n8n
- Deployment check: webhook after each production deploy
- Weekly brief: Monday 8 AM cron via n8n
