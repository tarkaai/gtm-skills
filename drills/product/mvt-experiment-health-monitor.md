---
name: mvt-experiment-health-monitor
description: Monitor running multivariate experiments for traffic balance, early harm signals, and projected completion
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# MVT Experiment Health Monitor

This drill provides continuous monitoring of running multivariate experiments. It detects problems early -- traffic imbalances, cell-level harm, and sample-starved cells -- so experiments either finish cleanly or get stopped before causing damage.

## Prerequisites

- A running MVT experiment configured via the `mvt-experiment-design` drill
- `mvt_cell_assigned` events flowing in PostHog with per-variable-level properties
- n8n instance for scheduling automated checks
- Attio for logging experiment status and alerts

## Steps

### 1. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs daily at a fixed time. The workflow performs these checks in sequence:

**Traffic balance check:**

Query PostHog for per-cell user counts:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      properties.variable_1_level AS var1,
      properties.variable_2_level AS var2,
      count(DISTINCT person_id) AS users
    FROM events
    WHERE event = 'mvt_cell_assigned'
      AND properties.experiment_slug = '{slug}'
      AND timestamp > '{experiment_start}'
    GROUP BY var1, var2"
  }
}
```

Calculate the expected users per cell (total / number of cells). Flag any cell with <80% or >120% of expected. If imbalanced for 2+ consecutive days, alert -- there is likely a feature flag misconfiguration.

**Guardrail metric check:**

For each cell, query the guardrail metrics (support ticket rate, error rate, unsubscribe rate). Using `posthog-anomaly-detection`, compare each cell's guardrail metric to the pre-experiment baseline. If any cell's guardrail metric exceeds 2x the baseline, trigger an immediate alert and recommend pausing that cell.

**Sample size projection:**

Based on current daily traffic rate per cell, project when the experiment will reach the planned sample size. If the projected end date exceeds the planned end date by more than 2 weeks, alert with options: extend the timeline, reduce the matrix (drop a variable), or increase traffic (e.g., expand the audience).

### 2. Build the harm detection trigger

Using `n8n-triggers`, create a real-time trigger that fires when a guardrail event exceeds the threshold. This is separate from the daily check -- it catches acute problems within hours:

1. Monitor the guardrail events in PostHog (errors, complaints, unsubscribes)
2. If the hourly rate of any guardrail event exceeds 3x the historical hourly average, trigger immediately
3. The trigger should:
   - Identify which experiment cell(s) are affected
   - Pause the affected cell by setting its feature flag rollout to 0% via PostHog API
   - Log the incident in Attio with: experiment slug, affected cell, guardrail metric, magnitude, timestamp
   - Alert the team via Slack or email with a summary and recommended action

### 3. Generate the weekly experiment status report

Using `n8n-scheduling`, create a weekly workflow that produces a status report for all running MVTs:

For each active experiment:
- **Traffic status**: total users enrolled, users per cell, days remaining to target sample size
- **Interim results** (marked as preliminary -- do not act on these): per-cell conversion rates with wide confidence intervals
- **Health flags**: any traffic imbalance alerts, guardrail triggers, or timeline slippage
- **Recommendation**: continue as planned, extend timeline, pause for investigation, or stop early (harm detected)

Post the report to Slack and store in Attio as a note on the experiment record.

### 4. Handle experiment completion

When all cells reach their target sample size, the health monitor triggers the completion workflow:

1. Set all experiment feature flags to "paused" (stop enrolling new users but keep existing assignments stable)
2. Wait 48 hours for lagging conversion events to arrive (users assigned on the last day may convert the next day)
3. Log the `mvt_experiment_completed` event in PostHog with: slug, total users, duration, cells
4. Alert the team that the experiment is ready for analysis
5. Hand off to the `mvt-results-analysis` drill

### 5. Log all monitoring data

Using `attio-notes`, maintain a running log for each experiment:

- Daily traffic counts per cell
- Any guardrail alerts with timestamps and resolution
- Weekly status snapshots
- Final completion timestamp and handoff to analysis

This log provides an audit trail and feeds into the `autonomous-optimization` drill at Durable level, which uses historical experiment performance to improve future experiment design.

## Output

- Daily automated health checks for all running MVT experiments
- Real-time harm detection with automatic cell-level pausing
- Weekly status reports with interim results and recommendations
- Automated completion detection and handoff to analysis
- Full audit trail in Attio
