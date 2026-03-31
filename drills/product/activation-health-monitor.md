---
name: activation-health-monitor
description: Monitor activation milestone completion rates per cohort, detect regressions in milestone progression, and generate weekly activation health briefs
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Activation Health Monitor

This drill builds an always-on monitoring system for activation milestone metrics. It tracks how each signup cohort progresses through defined milestones, detects when any milestone's completion rate regresses, and produces a weekly health brief that tells the agent exactly where to focus optimization effort.

This drill is play-specific to `activation-milestone-tracking` and complements the `autonomous-optimization` drill by providing the monitoring signal layer that the optimization loop acts on.

## Prerequisites

- PostHog tracking installed with activation milestone events (run `posthog-gtm-events` first)
- At least 4 weeks of cohort data (signups through each milestone)
- n8n instance with PostHog and Slack/email credentials configured
- Attio configured with a campaign record for the activation-milestone-tracking play
- Activation milestones defined and instrumented (typically 4-6 events between signup and full activation)

## Steps

### 1. Define the milestone metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks:

- **Milestone completion rates:** Percentage of signups that reach each milestone within 14 days, per weekly cohort. Track each milestone independently: `milestone_1_completed`, `milestone_2_completed`, through `activation_reached`.
- **Milestone sequence conversion:** Step-by-step conversion between consecutive milestones. This reveals where users stall.
- **Time-to-milestone:** Median minutes from signup to each milestone per weekly cohort. Increasing time signals growing friction.
- **Milestone completion by segment:** Break rates down by signup source, plan type, user role, and device type. Different segments hit different walls.
- **Stall concentration:** Which milestone has the highest absolute drop-off for this week's cohort. This is where optimization effort belongs.

### 2. Build the activation milestone dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "Activation Milestone Health" dashboard with these panels:

1. **Milestone funnel waterfall:** Current week's milestone-by-milestone conversion showing step-by-step conversion and absolute drop-off count.
2. **Milestone completion rate trends:** Weekly completion rate for each milestone over the last 12 weeks. One line per milestone. Add horizontal threshold lines at the play's targets.
3. **Time-to-milestone distribution:** Histogram showing minutes from signup to each milestone for the current week's cohort. Right-shift means increasing friction.
4. **Segment heatmap:** Milestone completion rates by segment (rows = signup sources or plan types, columns = milestones). Color-code: green if above target, yellow if within 10% of target, red if below target.
5. **Cohort overlay:** Overlay the last 4 weekly cohorts' milestone progression curves to spot whether newer cohorts are activating faster or slower.
6. **Stall point concentration:** Bar chart showing which milestone has the most users stalled (reached milestone N but not N+1 after 48+ hours).

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 08:00 UTC):

1. Query PostHog for yesterday's milestone metrics:
   - New signups count
   - Users completing each milestone yesterday
   - Median time-to-milestone for users who completed each milestone yesterday
   - Step conversion rates between consecutive milestones
2. Using `posthog-anomaly-detection`, compare yesterday's metrics against the 4-week rolling average:
   - **Normal:** Within +/- 10% of rolling average. Log to Attio using `attio-notes`, no action.
   - **Warning:** Any milestone completion rate dropped 10-20% below average. Log to Attio with a warning flag.
   - **Critical:** Any milestone completion rate dropped >20% below average, OR overall activation rate dropped below the play's pass threshold. Log to Attio, send Slack alert, trigger investigation.
3. For critical alerts, include context: which milestone saw the biggest drop, which segment was most affected, whether time-to-milestone also increased (friction vs. abandonment), and any correlated product events (deploys, feature flag changes, traffic spikes).

Alert format:
```
ACTIVATION MILESTONE ALERT: [milestone_name] completion dropped to [X%] (expected [Y%])
- Overall activation rate: [Z%] (threshold: [T%])
- Worst segment: [segment] at [rate%]
- Time-to-milestone: [M min] (was [N min])
- Possible cause: [milestone N step has highest new dropoff | segment shift detected | time increase suggests friction]
- Recommended action: [investigate milestone N UX | check for product changes | review segment targeting]
```

### 4. Build the weekly activation health brief

Using `n8n-scheduling`, create a weekly cron workflow (run Monday 09:00 UTC):

1. Aggregate the past week's data:
   - Total signups, total users reaching each milestone, overall activation rate
   - Per-milestone completion rates with comparison to prior week and 4-week average
   - Best and worst performing milestones
   - Best and worst performing segments per milestone
   - Stall point with the highest absolute user count
   - Number of anomalies detected during the week
2. Using `n8n-workflow-basics`, generate the brief via Claude API:
   - Input: This week's metrics, last week's metrics, 4-week averages, anomalies, any active experiments
   - Output: A structured brief with sections:

```
# Activation Milestone Health Brief — Week of [date]

## Summary
[1-2 sentences: overall health, biggest change]

## Key Metrics
| Milestone | This Week | Last Week | 4-Week Avg | Status |
|-----------|-----------|-----------|------------|--------|
| Milestone 1 | X% | Y% | Z% | OK/WARN/CRIT |
| ...       | ...       | ...       | ...        | ...    |
| Activation | X% | Y% | Z% | OK/WARN/CRIT |

## Biggest Opportunity
[The single milestone + segment combination where improvement would yield the largest activation lift. Include estimated impact.]

## Stall Analysis
[Where users are getting stuck, how many, and for how long]

## Experiments in Flight
[Any active A/B tests from autonomous-optimization, with current results if available]

## Recommendations
[2-3 specific, actionable next steps for the agent to execute]
```

3. Post the brief to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Set up regression trip-wires

Beyond daily checks, configure immediate alerts for critical regressions:

- **Overall activation rate < play threshold** for 3 consecutive days: Immediate alert. The play is failing.
- **Any milestone completion rate drops below 50%** when it was previously above 70%: Immediate alert. Specific milestone regression.
- **Median time-to-activation > 2x baseline** for 2 consecutive days: Immediate alert. Likely a product bug or UX regression.
- **Stall count at any milestone exceeds 30% of active cohort**: Immediate alert. Users are hitting a wall.

These alerts bypass the daily summary and go directly to the team. Include a link to the relevant PostHog dashboard panel.

### 6. Feed signals to the optimization loop

This monitor's output feeds directly into the `autonomous-optimization` drill's Phase 1 (Monitor):

- Daily anomaly classifications (normal, warning, critical) become the trigger for hypothesis generation
- The weekly health brief's "Biggest Opportunity" becomes the starting point for the next experiment
- Stall analysis data tells the optimization loop which milestone to experiment on first
- Segment-level data helps the optimization loop decide which segment to target

Store all signals in a consistent format in Attio so the optimization loop can query them programmatically:
- Record type: Note on play campaign record
- Properties: `metric_name`, `metric_value`, `expected_value`, `classification`, `milestone`, `segment`, `date`

## Output

- A PostHog dashboard with 6 panels tracking activation milestone health
- A daily n8n workflow that checks milestone metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes an activation health brief
- Trip-wire alerts for critical milestone regressions
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 08:00 UTC
- Weekly brief: cron, Monday 09:00 UTC
- Regression alerts: real-time via PostHog actions or daily check
