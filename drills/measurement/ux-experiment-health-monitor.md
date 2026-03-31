---
name: ux-experiment-health-monitor
description: Track active UX experiments, alert on guardrail breaches, and report weekly experiment velocity and cumulative lift
category: Experimentation
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-experiments
  - posthog-dashboards
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# UX Experiment Health Monitor

This drill provides always-on monitoring of all active page layout and UX experiments. It detects guardrail breaches in real-time, tracks experiment velocity (how many tests run per month), and generates weekly reports showing cumulative lift from all implemented winners.

## Prerequisites

- PostHog experiments running for at least one active layout test
- n8n instance for scheduled monitoring
- Attio configured with a "UX Experiments" list or campaign record
- At least one completed experiment to establish baseline velocity

## Steps

### 1. Build the experiment registry

Create a PostHog dashboard using `posthog-dashboards` that tracks all active and completed UX experiments:

- **Panel 1 — Active experiments:** List of currently running experiments with: name, start date, days running, sample size per variant, current statistical significance
- **Panel 2 — Experiment velocity:** Rolling 30-day count of experiments started, completed, and implemented
- **Panel 3 — Cumulative lift:** Sum of primary metric improvement from all implemented winners over the last 90 days
- **Panel 4 — Win rate:** Percentage of completed experiments where the variant beat the control

Query active experiments via:
```
GET /api/projects/<id>/experiments/?status=running
```

### 2. Configure guardrail monitoring

Using `n8n-scheduling`, create a workflow that runs every 6 hours:

1. Fetch all active experiments from PostHog
2. For each experiment, check guardrail metrics:
   - **Bounce rate:** If variant bounce rate exceeds control by >15 percentage points, flag
   - **Error rate:** If any client-side errors spike >2x in the variant, flag
   - **Core metric regression:** If the variant's primary metric drops >25% below control after 48+ hours of data, flag
   - **Sample ratio mismatch:** If the variant/control split deviates from 50/50 by more than 5 percentage points, flag (indicates a bug)
3. If any guardrail is breached:
   - Send an alert via Slack or email with: experiment name, breached guardrail, current values, and recommended action
   - If the breach is a core metric regression >30%, auto-pause the experiment by disabling the feature flag via PostHog API

Using `posthog-anomaly-detection`, check for unexpected patterns: sudden traffic changes, time-of-day effects that could bias results, or geographic skew.

### 3. Generate the weekly experiment report

Using `n8n-scheduling`, create a weekly cron workflow (Monday 9am):

1. Fetch all experiments that were active during the past 7 days
2. For each experiment, compute:
   - Days running and estimated days remaining
   - Current sample size vs. required sample size
   - Current significance level
   - Trend direction (improving, stable, declining)
3. For experiments completed this week:
   - Final result: winner, loser, or inconclusive
   - Primary metric delta (variant vs. control)
   - Decision: implement, iterate, or revert
4. Aggregate metrics:
   - **Experiment velocity:** Tests started, completed, and implemented this week
   - **Cumulative lift:** Net improvement from all implemented winners
   - **Pipeline:** Number of experiments queued for next week
5. Generate a formatted report and post to Slack. Store in Attio using `attio-notes`.

### 4. Track experiment learning log

For every completed experiment, log in Attio:

- Hypothesis (what you predicted)
- Result (what actually happened)
- Learning (what you now know that you did not before)
- Next action (what this result suggests testing next)

Over time, this learning log reveals patterns: which types of layout changes tend to win, which page elements are most sensitive to changes, and where diminishing returns begin.

### 5. Detect convergence signals

Using `posthog-anomaly-detection`, monitor for convergence — the point where successive experiments produce diminishing returns:

- Track the magnitude of lift from each successive experiment
- If the last 3 implemented experiments each produced <2% lift, flag convergence
- At convergence, recommend: reduce experiment frequency, shift testing to a different page or element, or escalate to a product-level change

## Output

- Real-time guardrail monitoring with automated alerts and auto-pause
- Weekly experiment health report with velocity, cumulative lift, and pipeline
- Experiment learning log in Attio for institutional knowledge
- Convergence detection signaling when a page has reached its local maximum

## Triggers

- Guardrail monitoring: every 6 hours (automated via n8n)
- Weekly report: Monday 9am (automated via n8n)
- Convergence check: after every experiment completion
