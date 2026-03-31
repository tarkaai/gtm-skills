---
name: onboarding-call-performance-monitor
description: Continuous monitoring of onboarding call funnel metrics -- booking rate, completion rate, activation rate, call quality scores, and cohort analysis
category: Onboarding
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
  - attio-reporting
---

# Onboarding Call Performance Monitor

This drill builds an always-on monitoring system for the onboarding call program. It tracks the full funnel from invitation to activation, detects anomalies, compares call vs no-call cohorts, and generates weekly performance reports. This drill feeds data into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- Onboarding call program running for at least 4 weeks with PostHog events being captured: `onboarding_call_invitation_clicked`, `onboarding_call_booked`, `onboarding_call_completed`, `onboarding_call_activation_fast`, `onboarding_call_activation_failed`
- PostHog dashboards enabled
- n8n instance for scheduled monitoring
- Attio CRM with onboarding call attributes populated

## Steps

### 1. Build the call funnel dashboard

Using `posthog-dashboards`, create a dashboard titled "Onboarding Call Program" with these panels:

**Panel 1 -- Full funnel (weekly trend):**
Build a funnel using `posthog-funnels` with these steps:
1. `onboarding_call_eligible` (qualified for a call)
2. `onboarding_call_invitation_clicked` (clicked the booking CTA)
3. `onboarding_call_booked` (completed the booking)
4. `onboarding_call_completed` (attended the call)
5. `activation_reached` (hit the activation milestone)

Display as a weekly trend chart. Calculate conversion rate between each step.

**Panel 2 -- Call quality distribution (weekly):**
Bar chart of call scores (4-12 scale) from the `onboarding_call_completed` event's `call_score` property. Overlay the weekly average. A declining average signals call quality degradation.

**Panel 3 -- Activation rate: call vs no-call:**
Using `posthog-cohorts`, create two cohorts:
- "Took onboarding call" = users where `onboarding_call_completed` = true
- "Eligible but no call" = users matching call eligibility criteria but `onboarding_call_completed` is null

Compare 7-day and 30-day activation rates between these cohorts. This is the core metric proving the program's value. Display as a line chart (weekly trend) with both cohorts overlaid.

**Panel 4 -- Time to activation (distribution):**
Histogram of days from signup to activation for call vs no-call cohorts. The call cohort should have a shorter tail. If the distributions overlap, the calls are not accelerating activation.

**Panel 5 -- Booking source breakdown:**
Pie chart of `booking_source` property from `onboarding_call_booked` events: in-app message, email 1, email 2, email 3, direct link. Identify which channel drives the most bookings.

**Panel 6 -- No-show and cancellation rate (weekly):**
Line chart of `onboarding_call_no_show` and `onboarding_call_cancelled` events as a percentage of `onboarding_call_booked`. Threshold: no-show rate should stay below 20%.

### 2. Define anomaly thresholds

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Booking rate (invitation to booked) | >25% | 15-25% | <15% |
| Completion rate (booked to attended) | >80% | 65-80% | <65% |
| Post-call activation rate (7-day) | >70% | 50-70% | <50% |
| Call quality average score | >8 | 6-8 | <6 |
| Activation lift vs no-call | >15pp | 5-15pp | <5pp |
| No-show rate | <15% | 15-25% | >25% |

### 3. Build the daily monitoring workflow

Using `n8n-scheduling`, create a workflow that runs daily at 09:00 UTC:

1. Query PostHog for the last 7 days of onboarding call events
2. Calculate each metric from Step 2
3. Compare against thresholds
4. If any metric is critical: send an immediate alert with the metric name, current value, threshold, and suggested diagnosis:
   - Low booking rate: check if invitation messages are still displaying, review email delivery rates
   - Low completion rate: check no-show rate, review reminder emails, check Cal.com availability
   - Low activation rate: review call scores, check if the walkthrough is reaching the milestone
   - Low activation lift: the calls may not be adding value beyond self-serve onboarding
5. If warning: log to Attio using `attio-notes`
6. If normal: log healthy status

### 4. Build the weekly performance report

Using `n8n-scheduling`, create a workflow that runs every Monday at 10:00 UTC:

1. Pull 7-day and 4-week metrics from PostHog
2. Pull call quality scores and feedback from Attio
3. Generate a structured report:

```
# Onboarding Call Program -- Week of [date]

## Summary
- Calls completed: [N] (prev week: [M])
- Booking rate: [X%] (target: >25%)
- Completion rate: [X%] (target: >80%)
- Post-call activation (7-day): [X%] (target: >70%)
- Activation lift vs no-call: [X pp]
- Average call score: [X]/12

## Funnel
| Step | Count | Conversion |
|------|-------|-----------|
| Eligible | [N] | -- |
| Invitation clicked | [N] | [X%] |
| Booked | [N] | [X%] |
| Completed | [N] | [X%] |
| Activated (7-day) | [N] | [X%] |

## Booking Sources
- In-app: [N] ([X%])
- Email 1: [N] ([X%])
- Email 2: [N] ([X%])
- Email 3: [N] ([X%])
- Direct: [N] ([X%])

## Call Quality
- Score distribution: [histogram summary]
- Top blockers this week: [list from call follow-up data]
- Feature requests: [list]

## Trends
- [Positive or negative trends with context]

## Anomalies
- [Any warning or critical alerts from daily monitoring]

## Recommended Actions
- [Prioritized list based on data]
```

4. Post to Slack and store in Attio

### 5. Build the cohort comparison analysis

Run monthly using `posthog-cohorts`:

1. Compare activation rates, 30-day retention, and feature adoption between call and no-call cohorts, controlling for plan type and company size
2. Calculate the program's ROI: (incremental activations from calls * LTV) vs (time spent on calls * cost per hour)
3. Identify which user segments benefit most from calls (e.g., enterprise users may benefit more than individual users)
4. Output a recommendation: expand call eligibility, narrow it, or keep it the same

### 6. Connect to autonomous optimization

This drill feeds directly into the `autonomous-optimization` drill at the Durable level:

- **Anomaly detected** triggers the Diagnose phase of autonomous optimization
- **Anomaly type** determines the hypothesis space: booking rate problem leads to test invitation copy, completion rate problem leads to test reminder cadence, activation rate problem leads to test call structure
- **Weekly performance report** provides context for hypothesis generation
- **Cohort comparison** determines whether to expand or contract the program

## Output

- PostHog dashboard tracking the full onboarding call funnel
- Daily anomaly detection with immediate alerts
- Weekly structured performance report
- Monthly cohort comparison and ROI analysis
- Integration with autonomous optimization for automated experimentation
