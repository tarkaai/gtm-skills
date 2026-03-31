---
name: experiment-portfolio-health-monitor
description: Monitor experiment program health including velocity, win rates, coverage gaps, and convergence signals
category: Measurement
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-reporting
---

# Experiment Portfolio Health Monitor

This drill provides always-on monitoring of your A/B testing program's health. It detects when the program is stalling, when experiments are producing diminishing returns, when product areas are under-tested, and when the program has converged (reached local maximum). It feeds anomaly signals to the `autonomous-optimization` drill at Durable level.

## Prerequisites

- Experiment pipeline running (via `experiment-pipeline-automation` or manual orchestration)
- At least 8 weeks of experiment history in Attio
- PostHog with experiment events tracked
- n8n for scheduled monitoring

## Input

- Attio experiment records spanning at least 2 months
- PostHog experiment completion events
- Target experiment velocity (experiments per month)

## Steps

### 1. Build the health check workflow (n8n)

Using `n8n-scheduling`, create a weekly cron workflow that runs every Monday at 08:00 UTC. The workflow queries Attio and PostHog for the following health indicators:

**Velocity health:**
- Experiments completed in the last 4 weeks
- Experiments currently running
- Experiments queued in backlog
- Days since last experiment completed
- Classification: healthy (on target), slowing (below 75% of target), stalled (no experiment completed in 14+ days)

**Win rate health:**
- Win rate over the last 8 weeks (rolling)
- Win rate trend: improving, stable, or declining
- Classification: healthy (25-50%), too conservative (>50%, testing easy wins), too speculative (<15%, hypotheses need better data)

**Coverage health:**
- Map of product areas tested in the last 90 days
- Identify product areas with no experiments in 90+ days
- Identify product areas where all recent experiments lost (potential misunderstanding of user behavior in that area)

**Convergence detection:**
- For each product area, track the lift of the last 3 winning experiments
- If lifts are declining (e.g., +3pp, +1.5pp, +0.4pp), the area is converging
- If 3 consecutive experiments in an area produce <2% lift, flag as converged

### 2. Configure anomaly alerts

Using `n8n-triggers`, set up alerts for health issues:

- **Stall alert:** No experiment completed in 14+ days → notify team, check for blockers (sample size issues, implementation delays, forgotten experiments)
- **Empty backlog alert:** Fewer than 2 hypotheses queued → run `experiment-hypothesis-design` drill to replenish
- **Win rate anomaly:** Win rate drops below 15% over 4-week window → review hypothesis quality, check if product changes invalidated assumptions
- **Coverage gap alert:** A product area with active users has not been tested in 90+ days → flag for hypothesis generation
- **Convergence alert:** A product area shows 3 consecutive experiments with <2% lift → recommend shifting experimentation resources to unconverged areas

### 3. Build the portfolio dashboard

Using `posthog-dashboards` and `posthog-custom-events`, create a dashboard showing:

- **Pipeline view:** queued → running → completed → adopted/reverted (counts per status)
- **Velocity trend:** experiments completed per week over the last 12 weeks
- **Win rate trend:** rolling 8-week win rate
- **Area coverage heatmap:** product areas × recency of last experiment (green = recent, yellow = stale, red = never tested)
- **Convergence tracker:** per-area chart showing diminishing returns trend
- **Cumulative impact:** total adopted lift across all metrics since program start

### 4. Generate the weekly health brief

Every Monday, the n8n workflow compiles a brief:

```
## Experiment Program Health — Week of [Date]

**Status:** [Healthy / Attention Needed / Critical]

**Velocity:** [X] experiments completed (target: [Y])
**Pipeline:** [A] running, [B] queued, [C] ready for evaluation
**Win rate (8-week):** [Z]%

**Alerts:**
- [Any active alerts from Step 2]

**Convergence:**
- [Area 1]: converging (last 3 lifts: +2.1%, +0.8%, +0.3%)
- [Area 2]: active optimization (last lift: +4.2%)

**Action items:**
- [Specific actions based on alerts and convergence signals]
```

Post to Slack and store in Attio.

### 5. Feed signals to autonomous optimization

At Durable level, this monitor's output feeds directly into the `autonomous-optimization` drill:
- Convergence signals tell the optimization loop to shift focus to unconverged areas
- Velocity stalls become anomalies that the optimization loop diagnoses
- Win rate trends inform hypothesis generation strategy adjustments

The integration point: the weekly health brief data is written to a PostHog custom event (`experiment_health_check`) that the autonomous optimization monitor reads during its daily scan.

## Output

- Weekly experiment program health brief with status classification
- Real-time alerts for stalls, empty backlogs, and convergence
- Portfolio dashboard showing pipeline, velocity, coverage, and impact
- Convergence detection per product area
- Anomaly feed for the autonomous optimization loop

## Triggers

- Weekly health check: Monday 08:00 UTC via n8n cron
- Real-time alerts: triggered by Attio status changes and PostHog events
- Convergence analysis: computed as part of the weekly health check
