---
name: integration-health-monitor
description: Continuous monitoring of integration setup rates, failure patterns, and per-integration health with anomaly alerts and weekly reports
category: Onboarding
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

# Integration Health Monitor

This drill creates a continuous monitoring system for integration setup performance. It tracks setup rates, failure rates, and time-to-connect per integration, detects anomalies, and generates actionable alerts. This drill feeds anomaly data into the `autonomous-optimization` drill for automated experimentation at the Durable level.

## Prerequisites

- Integration wizard running with PostHog events flowing (from `integration-wizard-build` drill)
- At least 4 weeks of integration setup data in PostHog
- n8n instance for scheduled monitoring workflows
- Attio configured for logging health observations

## Steps

### 1. Build the integration health dashboard

Using the `posthog-dashboards` fundamental, create a dashboard titled "Integration Setup Health" with these panels:

- **Overall wizard completion rate (weekly trend)**: Line chart, 12-week window. Target line at the play's threshold (e.g., 55% for Smoke, 65% for Baseline).
- **Per-integration success rate**: Bar chart showing setup success rate per integration, weekly. Identifies which integrations have the highest failure rates.
- **Time to connect by integration**: Box plot or histogram showing seconds from `integration_step_started` to `integration_setup_succeeded` per integration. Increasing time = growing friction.
- **Failure rate by error type**: Stacked bar chart showing failure distribution per integration (auth_expired, permissions_insufficient, rate_limited, unknown). Tracks whether error patterns are shifting.
- **Rescue workflow effectiveness**: Line chart showing: stalled users detected, rescue messages sent, users who resumed, users who completed after rescue. Measures recovery pipeline health.
- **Wizard abandonment funnel**: Funnel from `integration_wizard_started` to `integration_wizard_completed` with per-step drop-off.

### 2. Define anomaly thresholds

For each metric, define what constitutes an anomaly:

| Metric | Normal range | Warning | Critical |
|--------|-------------|---------|----------|
| Wizard completion rate | Within 10% of 4-week rolling average | 10-20% below average for 1 week | >20% below average OR below play threshold for 2 consecutive weeks |
| Per-integration success rate | Within 15% of average | 15-25% below for 1 week | >25% below OR below 50% absolute |
| Time to connect | Within 20% of median | 20-40% above median for 1 week | >40% above median (friction increasing) |
| Failure rate for any error type | Within 20% of average | Any error type spikes 2x its average | Any error type spikes 3x OR `unknown` errors exceed 20% of all failures |
| Rescue recovery rate | Within 15% of average | 15-30% below average | >30% below average for 2 weeks |

### 3. Build the daily monitoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs daily at 08:00 UTC:

1. Query PostHog for the last 7 days of integration setup events
2. Calculate: wizard completion rate, per-integration success rate, failure distribution, rescue effectiveness
3. Compare each metric against its 4-week rolling average using `posthog-anomaly-detection`
4. Classify each metric: normal, warning, or critical
5. If any metric is critical: send immediate alert (Slack or email):

```
INTEGRATION ALERT: [metric_name] at [current_value] (expected [expected_value])
- Integration: [integration_name] (if per-integration)
- Error breakdown: auth_expired=[N], permissions=[N], rate_limited=[N], unknown=[N]
- Trend: [improving | stable | declining] over 4 weeks
- Suggested cause: [top error type spiked | third-party API changed | new user cohort has different tool stack]
- Recommended action: [update auth flow | add permission guidance | contact integration partner | investigate unknown errors]
```

6. If any metric is warning: log observation to Attio using `attio-notes`
7. If all metrics normal: log "healthy" status to Attio

### 4. Build the weekly integration health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

1. Pull 7-day and 4-week metrics from PostHog
2. Generate a structured report:

```
# Integration Setup Health Report -- Week of [date]

## Summary
- Total wizard starts: [N]
- Overall completion rate: [X%] (prev week: [Y%], threshold: [Z%])
- Integrations connected: [total_count]
- Median time to first integration: [seconds]

## Per-Integration Breakdown
| Integration | Attempts | Success Rate | Avg Time | Top Error |
|-------------|----------|-------------|----------|-----------|
| [int_1]     | [N]      | [X%]        | [Ns]     | [error]   |
| [int_2]     | [N]      | [X%]        | [Ns]     | [error]   |
| [int_3]     | [N]      | [X%]        | [Ns]     | [error]   |

## Failure Analysis
- Total failures: [N] ([X%] of attempts)
- auth_expired: [N] ([X%]) -- trend: [up/down/stable]
- permissions_insufficient: [N] ([X%]) -- trend: [up/down/stable]
- rate_limited: [N] ([X%]) -- trend: [up/down/stable]
- unknown: [N] ([X%]) -- trend: [up/down/stable]

## Rescue Pipeline
- Users stalled: [N]
- Rescue messages sent: [N]
- Users resumed: [N] ([X%] recovery rate)
- Users completed after rescue: [N]

## Anomalies Detected
- [List of warning/critical anomalies with dates]

## Experiments in Flight
- [List any active A/B tests from autonomous-optimization]

## Recommended Actions
- [Prioritized list based on anomaly data]
```

3. Post the report to Slack and store in Attio as a note on the play record

### 5. Build integration-specific failure tracking

Using `posthog-cohorts`, create cohorts for each failure pattern:

- "Failed [Integration 1] -- Auth": Users where `integration_setup_failed` with `integration_name = [int_1]` AND `error_type = auth_expired` in last 14 days AND `integration_1_connected != true`
- "Failed [Integration 2] -- Permissions": Same pattern for permissions errors
- "Chronic Failures": Users with 3+ `integration_setup_failed` events across any integrations in last 14 days

These cohorts feed into the rescue workflow (for targeted messaging) and the `autonomous-optimization` drill (for hypothesis generation about what to fix).

### 6. Detect third-party integration changes

Using `n8n-scheduling`, create a workflow that runs daily and checks for sudden spikes in specific error types for individual integrations:

1. If `auth_expired` errors for one integration spike >3x in 24 hours, it likely means the third-party changed their OAuth flow or revoked tokens
2. If `permissions_insufficient` errors spike, the third-party likely added new required scopes
3. If `rate_limited` errors spike, the third-party changed their rate limits

For each detected spike:
- Log to Attio with the integration name and suspected cause
- Alert the engineering team to investigate and update the integration
- Temporarily update the Intercom bot for that integration to acknowledge the issue: "We're aware of a connection issue with [Integration] and working on a fix. We'll notify you when it's resolved."

### 7. Connect to autonomous optimization

This drill's output feeds directly into the `autonomous-optimization` drill:

- **Anomaly detected** triggers the Diagnose phase of autonomous optimization
- **Anomaly type** determines hypothesis space: high failure rate leads to test setup flow changes, slow time-to-connect leads to test UI simplification, low rescue recovery leads to test rescue message copy
- **Weekly health report** provides the context data that hypothesis generation needs
- **Third-party integration changes** trigger immediate triage rather than experimentation

## Output

- PostHog dashboard: "Integration Setup Health" with 6 panels
- Daily automated health check with critical anomaly alerts
- Weekly structured health report with per-integration breakdown
- Per-integration failure cohorts for targeted intervention
- Third-party change detection with automatic acknowledgment messages
- Integration with autonomous-optimization for automated response to anomalies

## Triggers

Runs continuously once activated. Daily monitoring workflow fires at 08:00 UTC. Weekly report fires Mondays at 09:00 UTC.
