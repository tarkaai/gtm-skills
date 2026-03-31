---
name: intent-signal-health-monitor
description: Monitor the health and accuracy of the intent signal pipeline — signal volume, scoring accuracy, outreach conversion, and signal decay patterns
category: Measurement
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Intent Signal Health Monitor

This drill builds the monitoring layer specific to intent signal tracking. It tracks whether signals are arriving, whether scores are accurate, whether outreach timing is fast enough, and whether the entire pipeline is converting intent into meetings and revenue.

## Input

- Intent signal automation running for at least 4 weeks (from `intent-signal-automation` drill)
- PostHog events logging all signal and outreach actions
- Attio with deal outcomes linked to intent-sourced accounts

## Steps

### 1. Build the signal pipeline dashboard

Using `posthog-dashboards`, create a dashboard called "Intent Signal Health" with these panels:

**Panel 1 — Signal Volume (trend, last 30 days)**
Query: count of `intent_signal_received` events grouped by signal_source (website, g2, bombora, enrichment). Alert if total signals drop below 50% of 4-week average.

**Panel 2 — Score Distribution (bar chart)**
Query: count of accounts by intent_tier (Hot, Warm, Cool, Cold) at current snapshot. Healthy distribution: 5-15% Hot, 15-25% Warm, 30-40% Cool, 30-40% Cold. If Hot exceeds 25%, the model is too generous.

**Panel 3 — Signal-to-Outreach Time (trend)**
Query: time delta between `intent_signal_received` (where tier = Hot) and `intent_outreach_triggered`. Target: median under 30 minutes for Hot-tier. Alert if median exceeds 2 hours.

**Panel 4 — Outreach Funnel (funnel chart)**
Using `posthog-funnels`:
`intent_outreach_triggered` -> `email_opened` -> `email_replied` -> `meeting_booked` -> `deal_created`
Break down by intent_tier. Expect Hot-tier to convert 3x+ better than Warm-tier at every stage.

**Panel 5 — Scoring Accuracy (comparison chart)**
Query: conversion rate (replied OR meeting_booked) grouped by intent_tier over last 30 days. This is the key accuracy metric. If Hot and Cold accounts convert at similar rates, the scoring model is broken.

**Panel 6 — Score Decay Impact (trend)**
Query: count of `intent_score_decay_pause` events (accounts that lost score and were paused). Healthy: 10-20% of active accounts per month. If above 40%, signals are too fleeting. If below 5%, decay is too gentle.

### 2. Build the weekly health check workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 8am:

**Flow:**
1. **PostHog API query** — pull the last 7 days of key metrics:
   - Total signals received (by source)
   - Hot-tier accounts identified
   - Outreach emails sent
   - Reply rate by tier
   - Meetings booked from intent
   - Average signal-to-outreach time
2. **Anomaly detection** — using `posthog-anomaly-detection`, compare each metric to its 4-week rolling average. Flag any metric that deviates by more than 20%.
3. **Score accuracy check** — pull conversion rates by tier. Compute the Hot-to-Cold conversion ratio. If below 2x, flag the scoring model for recalibration.
4. **Signal source health** — check each signal source individually. If any source produced zero signals in the last 7 days, flag as "source down."
5. **Generate report** — compile findings into a structured brief:
   ```
   ## Intent Signal Weekly Health — Week of [date]

   ### Pipeline Status: [HEALTHY / WARNING / CRITICAL]

   | Metric | This Week | 4-Week Avg | Status |
   |--------|-----------|------------|--------|
   | Signals received | X | Y | OK/WARN |
   | Hot accounts | X | Y | OK/WARN |
   | Outreach sent | X | Y | OK/WARN |
   | Reply rate (Hot) | X% | Y% | OK/WARN |
   | Meetings booked | X | Y | OK/WARN |
   | Avg signal-to-outreach | Xm | Ym | OK/WARN |
   | Hot:Cold conversion ratio | X:1 | Y:1 | OK/WARN |

   ### Anomalies Detected
   - [description of any flagged metric]

   ### Signal Source Status
   - Website visitors: [OK/DOWN] (X signals)
   - G2 intent: [OK/DOWN] (X signals)
   - Enrichment refresh: [OK/DOWN] (X updates)

   ### Recommended Actions
   - [auto-generated based on anomalies]
   ```
6. **Distribute** — post to Slack and store in Attio as a note on the "Intent Signal Tracking" campaign record

### 3. Build the monthly scoring audit workflow

Using `n8n-scheduling`, create a workflow that runs on the 1st of each month:

**Flow:**
1. Pull all accounts that received outreach in the last 30 days with their intent_score at time of outreach
2. Pull outcomes: replied, meeting, deal created, deal won, deal lost
3. Build a confusion matrix:
   - True positives: Hot/Warm accounts that converted
   - False positives: Hot/Warm accounts that did not respond
   - True negatives: Cool/Cold accounts that were correctly deprioritized
   - False negatives: Cool/Cold accounts that actually would have converted (check by looking at any Cool/Cold accounts that later created deals through other channels)
4. Calculate precision (of Hot accounts contacted, what % converted?) and recall (of accounts that converted, what % were scored Hot?)
5. If precision drops below 15% or recall drops below 50%, flag the model for recalibration and output specific recommendations (which signals to increase/decrease in weight)

## Output

- PostHog dashboard with 6 real-time panels
- Weekly Slack health report with anomaly detection
- Monthly scoring audit with precision/recall metrics
- Automated alerts when signal sources go down or scoring accuracy degrades

## Triggers

- Dashboard: always-on, real-time
- Weekly health check: Monday 8am (cron)
- Monthly scoring audit: 1st of month (cron)
