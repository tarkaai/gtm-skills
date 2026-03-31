---
name: ttv-health-monitor
description: Monitor time-to-value cohort trends, detect activation regressions, and generate weekly activation health briefs
category: Onboarding
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# TTV Health Monitor

This drill builds an always-on monitoring system for time-to-value metrics. It tracks how quickly each signup cohort reaches activation, detects regressions before they compound, and produces a weekly health brief that tells the agent (or human) exactly where to focus optimization effort.

This drill is play-specific to `time-to-value-optimization` and complements the `autonomous-optimization` drill by providing the monitoring signal layer that the optimization loop acts on.

## Prerequisites

- PostHog tracking installed with activation funnel events (run `posthog-gtm-events` first)
- At least 4 weeks of cohort data (signups through activation)
- n8n instance with PostHog and Slack/email credentials configured
- Attio configured with a campaign record for the time-to-value play

## Steps

### 1. Define the TTV metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks:

- **Median time-to-value (TTV):** Median minutes from `signup_completed` to `activation_reached` per weekly cohort. This is the primary metric.
- **Activation rate:** Percentage of signups that reach `activation_reached` within 14 days.
- **Step conversion rates:** Conversion between each onboarding milestone (signup -> milestone_2 -> milestone_3 -> ... -> activation).
- **TTV by segment:** Break TTV down by signup source, plan type, and user role. Different segments have different baseline TTVs.
- **Drop-off concentration:** Which funnel step has the highest absolute drop-off for this week's cohort.

### 2. Build the cohort dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "TTV Health" dashboard with these panels:

1. **TTV trend line:** Weekly median TTV for the last 12 weeks. Add a horizontal line at the target threshold (e.g., 8 minutes).
2. **Activation rate trend:** Weekly activation rate for the last 12 weeks. Add a horizontal line at the target threshold (e.g., 60%).
3. **Funnel waterfall:** Current week's onboarding funnel showing step-by-step conversion and absolute drop-off.
4. **Segment heatmap:** TTV by segment (rows = signup sources, columns = weeks). Color-code: green if below target, yellow if within 20% of target, red if above target.
5. **Cohort retention curve:** Overlay the last 4 weekly cohorts to spot whether newer cohorts are activating faster or slower than older ones.

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 08:00 UTC):

1. Query PostHog for yesterday's activation metrics:
   - New signups
   - Activations (users who reached `activation_reached`)
   - Median TTV for users who activated yesterday
   - Funnel step conversion rates for yesterday's signups
2. Using `posthog-anomaly-detection`, compare yesterday's metrics against the 4-week rolling average:
   - **Normal:** Within +/- 10% of rolling average. Log to Attio, no action.
   - **Warning:** TTV increased 10-25% or activation rate dropped 10-25%. Log to Attio with a warning flag.
   - **Alert:** TTV increased >25% or activation rate dropped >25%. Log to Attio, send Slack alert, trigger investigation.
3. For alerts, include context: which funnel step saw the biggest change, which segment was most affected, and any correlated product events (deploy, feature flag change, traffic spike).

### 4. Build the weekly health brief

Using `n8n-scheduling`, create a weekly cron workflow (run Monday 09:00 UTC):

1. Aggregate the past week's data:
   - Total signups, total activations, overall activation rate
   - Median TTV with comparison to prior week and 4-week average
   - Best and worst performing segments
   - Funnel step with the biggest drop-off
   - Number of anomalies detected during the week
2. Using `n8n-workflow-basics`, generate the brief via Claude API:
   - Input: This week's metrics, last week's metrics, 4-week averages, any anomalies, any experiments running
   - Output: A structured brief with sections: Summary (1-2 sentences), Key Metrics (table), Biggest Opportunity (the single highest-impact change to make), Segment Spotlight (one segment that improved or degraded notably), Recommendations (2-3 specific actions)
3. Post the brief to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Set up regression alerts

Beyond daily checks, configure trip-wire alerts for critical regressions:

- **Activation rate < 40%** for 3 consecutive days: Immediate Slack alert. Something is broken.
- **Median TTV > 2x baseline** for 2 consecutive days: Immediate alert. Likely a product bug or UX change.
- **Any funnel step drops below 50% conversion** when it was previously above 70%: Immediate alert. Specific step regression.

These alerts bypass the daily summary and go directly to the team. Include a link to the relevant PostHog dashboard panel and the last 3 days of session recordings for the affected step.

### 6. Feed signals to the optimization loop

This monitor's output feeds directly into the `autonomous-optimization` drill's Phase 1 (Monitor):

- Daily anomaly classifications (normal, warning, alert) become the trigger for hypothesis generation
- The weekly health brief's "Biggest Opportunity" becomes the starting point for the next experiment
- Segment-level TTV data helps the optimization loop decide which segment to experiment on first

Store all signals in a consistent format in Attio so the optimization loop can query them programmatically.

## Output

- A PostHog dashboard with 5 panels tracking TTV health
- A daily n8n workflow that checks metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes a health brief
- Trip-wire alerts for critical regressions
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 08:00 UTC
- Weekly brief: cron, Monday 09:00 UTC
- Regression alerts: real-time via PostHog actions or daily check
