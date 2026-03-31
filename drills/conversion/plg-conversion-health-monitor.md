---
name: plg-conversion-health-monitor
description: Monitor the PLG-to-sales-assist conversion pipeline end to end, detect anomalies in routing quality and conversion rates, and generate weekly health reports
category: Conversion
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-cohorts
  - attio-reporting
  - attio-lists
  - n8n-scheduling
  - n8n-workflow-basics
---

# PLG Conversion Health Monitor

This drill builds the monitoring and reporting layer for a PLG + sales-assist model. It tracks the full pipeline from product usage signals through PQL identification, routing, and conversion outcome. The output is a weekly health report that identifies what is working, what is degrading, and where the agent should focus optimization effort.

## Input

- PostHog tracking from the `plg-sales-routing` drill (PQL signals, routing events, outcomes)
- PostHog funnels and dashboards configured for the PLG pipeline
- Attio CRM with expansion deals and account data
- n8n instance for scheduled monitoring workflows

## Steps

### 1. Build the PLG pipeline dashboard

Using `posthog-dashboards`, create a dashboard called "PLG + Sales-Assist Health" with these panels:

**Panel 1: PQL Funnel (weekly)**
Funnel: `product_active` -> `pql_signal_detected` -> `plg_upgrade_prompt_shown` -> `plg_route_outcome(outcome=upgraded)`
Break down by: route type (self_serve vs sales_assist)

**Panel 2: Self-Serve Conversion Rate (trailing 4 weeks)**
Line chart: weekly ratio of `plg_route_outcome(route=self_serve, outcome=upgraded)` / `plg_route_outcome(route=self_serve)`
Include: MRR added from self-serve upgrades per week

**Panel 3: Sales-Assist Pipeline (trailing 4 weeks)**
Line chart: weekly count of deals created, meetings booked, deals closed, ACV per closed deal
Source: Attio deal data synced to PostHog or queried directly

**Panel 4: Routing Quality**
Stacked bar: weekly count of correct routes vs mis-routes
Correct = self-serve that converted OR sales-assist that closed
Mis-route = self-serve that needed sales escalation OR sales-assist that self-served

**Panel 5: Time Metrics**
Line chart: median time from PQL signal to upgrade (self-serve) and PQL signal to deal close (sales-assist)
Goal: self-serve < 7 days, sales-assist < 30 days

**Panel 6: PQL Signal Distribution**
Bar chart: count of each PQL signal type (plan_limit_hit, feature_gate, team_growth, etc.) per week
Helps identify which signals are firing and which drive the most conversions

### 2. Set up anomaly detection

Using `posthog-anomaly-detection`, configure alerts for the following conditions:

| Metric | Anomaly Condition | Severity |
|--------|------------------|----------|
| Self-serve conversion rate | Drops below 10% for 2 consecutive weeks | Critical |
| Sales-assist meeting book rate | Drops below 30% for 2 consecutive weeks | Critical |
| PQL signal volume | Drops more than 40% week-over-week | Warning |
| Mis-route rate | Exceeds 25% for 2 consecutive weeks | Warning |
| Median time-to-upgrade (self-serve) | Exceeds 14 days | Warning |
| ACV (sales-assist) | Drops more than 30% vs 4-week average | Warning |

When an anomaly fires, the monitoring workflow triggers the `autonomous-optimization` drill to diagnose and generate hypotheses.

### 3. Build the weekly health check workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 08:00 UTC:

1. **Pull metrics from PostHog:** Query the PLG pipeline dashboard for the last 7 days and trailing 4-week comparison
2. **Pull deal data from Attio:** Using `attio-reporting`, query expansion deals created, advanced, closed-won, and closed-lost in the last 7 days
3. **Compute health scores:**
   - Self-serve health: conversion rate vs 4-week average, MRR trend, prompt engagement
   - Sales-assist health: pipeline velocity, close rate vs average, ACV trend
   - Routing health: mis-route rate, signal accuracy, threshold calibration
   - Overall PLG health: composite of all three on a green/yellow/red scale
4. **Generate the weekly brief:** Using Claude, synthesize the metrics into a 1-page report:
   - Top-line: overall PLG health status (green/yellow/red)
   - Wins: what improved this week and likely causes
   - Concerns: what degraded and hypothesized root causes
   - Recommendation: one specific action for the coming week
   - Metrics table: this week vs last week vs 4-week average
5. **Distribute:** Post the brief to Slack and store as an Attio note on the PLG campaign record

### 4. Track cohort conversion curves

Using `posthog-cohorts` and `posthog-funnels`, build cohort conversion curves:

- For each weekly signup cohort, track what percentage become PQLs within 14 days, 30 days, 60 days
- Compare cohort curves over time: are newer cohorts converting faster or slower than older ones?
- Break down by acquisition source: do users from different channels have different PLG conversion rates?
- Flag cohorts that are significantly underperforming the baseline curve

This reveals whether changes to the product, onboarding, or market are affecting the upstream pipeline before it shows up in conversion rates.

### 5. Monitor sales-assist deal health

Using `attio-lists` and `attio-reporting`, maintain three active lists:

- **"PLG Deals -- Stalled"**: Expansion deals that have not advanced stages in 14+ days. The monitoring workflow checks weekly and flags these for AE follow-up or deal re-qualification.
- **"PLG Deals -- At Risk"**: Deals where the account's engagement score has dropped below 40 since deal creation. The prospect may be losing interest.
- **"PLG Deals -- Won This Month"**: Closed-won expansion deals for the current month. Used for MRR reporting and win pattern analysis.

### 6. Build the convergence detector

Track the rate of improvement from optimization experiments. Using `posthog-dashboards`, create a panel that shows the net conversion rate change from each experiment in the last 90 days. If the last 3 experiments each produced less than 2% improvement, the play has reached its local maximum. At convergence:

1. Flag the play as "optimized" in Attio
2. Reduce monitoring frequency from weekly to biweekly
3. Generate a convergence report: current performance ceiling, what was tried, what worked, diminishing returns evidence

## Output

- PostHog dashboard with 6 panels covering the full PLG pipeline
- Anomaly detection alerts for 6 critical and warning conditions
- Weekly automated health report delivered to Slack and stored in Attio
- Cohort conversion curves revealing upstream pipeline health
- Three Attio lists tracking deal health (stalled, at-risk, won)
- Convergence detection for knowing when the play has reached its local maximum

## Triggers

- Weekly health check: n8n cron, Mondays at 08:00 UTC
- Anomaly alerts: real-time via PostHog anomaly detection
- Cohort analysis: generated as part of the weekly health check
- Convergence check: evaluated monthly as part of the health report
