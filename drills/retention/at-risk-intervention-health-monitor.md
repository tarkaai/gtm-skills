---
name: at-risk-intervention-health-monitor
description: Monitor at-risk intervention effectiveness by channel, segment, and timing, and generate weekly retention health briefs
category: Retention
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# At-Risk Intervention Health Monitor

This drill builds an always-on monitoring system for the at-risk-intervention play. It tracks how effectively interventions prevent churn across different risk tiers, channels, and user segments, and produces a weekly health brief that tells the agent exactly where to focus optimization.

This drill complements the `autonomous-optimization` drill by providing the play-specific signal layer that the optimization loop acts on.

## Prerequisites

- PostHog tracking installed with intervention events (run `posthog-gtm-events` first with events from the `churn-prevention` drill)
- `churn-risk-scoring` drill running daily (provides risk tier data)
- At least 4 weeks of intervention data
- n8n instance with PostHog and Slack/email credentials configured
- Attio configured with a campaign record for the at-risk-intervention play

## Steps

### 1. Define the intervention metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks:

- **Intervention reach:** Percentage of at-risk users (medium, high, critical tiers) who received at least one intervention within 24 hours of scoring. Target: >90%.
- **Response rate by channel:** Percentage of users who engaged with the intervention, broken down by channel (in-app message, email, personal outreach). Engagement = opened email, clicked CTA, replied, or took the prompted action.
- **Save rate by tier:** Percentage of at-risk users who returned to low risk within 14 days of intervention, segmented by the tier they were in when intervention fired.
- **Time-to-response:** Median hours from intervention delivery to first user engagement. Shorter is better — indicates the intervention was relevant and timely.
- **Intervention-to-retention:** Of users saved by intervention, what percentage are still active 30 days later? (Prevents counting temporary re-engagement as a save.)
- **False alarm rate:** Percentage of intervened users who were never actually going to churn (they were active throughout despite the risk score). High rates mean the scoring model needs calibration.
- **Channel efficiency:** Save rate per dollar spent per channel. Compares the cost-effectiveness of in-app vs. email vs. personal outreach.

### 2. Build the intervention health dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "At-Risk Intervention Health" dashboard:

1. **Save rate funnel:** Funnel from `intervention_sent` -> `intervention_engaged` -> `risk_tier_improved` -> `retained_30d`. Shows the full conversion from intervention to lasting retention.
2. **Save rate by risk tier (trend):** Weekly save rate for medium, high, and critical tiers over the last 12 weeks. One line per tier.
3. **Channel performance comparison:** Side-by-side bar chart: response rate, save rate, and time-to-response for each intervention channel (in-app, email, personal).
4. **Intervention timing heatmap:** Save rate by day-of-week and hour-of-day when the intervention was delivered. Identifies optimal intervention timing.
5. **Segment breakdown:** Save rate by user segment (plan type, company size, usage pattern, signup cohort). Identifies which user types respond best to intervention.
6. **Scoring model health:** Precision, recall, and false positive rate from the latest `churn-risk-scoring` calibration. Trend over last 6 calibrations.

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 09:00 UTC, after the `churn-risk-scoring` workflow completes at 06:00):

1. Query PostHog for yesterday's intervention metrics:
   - New at-risk users identified (by tier)
   - Interventions sent (by channel and tier)
   - Interventions engaged (by channel and tier)
   - Users who improved tier (saved)
   - Users who churned despite intervention (lost)
2. Using `posthog-anomaly-detection`, compare yesterday's metrics against the 4-week rolling average:
   - **Normal:** Within +/- 10% of rolling average. Log to Attio using `attio-notes`, no action.
   - **Warning:** Save rate dropped 10-20% below average, OR intervention reach dropped below 80%. Log with warning flag.
   - **Critical:** Save rate dropped >20% below average, OR overall save rate below play threshold, OR a specific channel's save rate dropped to zero. Log, send alert, trigger investigation.
3. For critical alerts, include: which tier/channel saw the drop, whether it correlates with a scoring model change, whether intervention delivery failed (n8n workflow errors), and recommended action.

Alert format:
```
AT-RISK INTERVENTION ALERT: [metric] at [value] (expected [expected_value])
- Overall save rate: [X%] (threshold: [T%])
- Worst channel: [channel] at [rate%]
- At-risk population: [N users] ([change vs. last week])
- Possible cause: [scoring drift | delivery failure | channel fatigue | segment shift]
- Recommended action: [recalibrate scoring | check n8n workflows | rotate messaging | investigate segment]
```

### 4. Build the weekly intervention health brief

Using `n8n-scheduling`, create a weekly cron workflow (run Monday 10:00 UTC):

1. Aggregate the past week:
   - Total at-risk users identified, total interventions sent, total saves, total losses
   - Save rate by tier, channel, and segment with comparison to prior week and 4-week average
   - Best and worst performing channel-tier combinations
   - Users who received intervention but did not respond (queue for channel rotation)
   - Scoring model accuracy metrics from latest calibration
2. Using `n8n-workflow-basics`, generate the brief via Claude API:

```
# At-Risk Intervention Health Brief — Week of [date]

## Summary
[1-2 sentences: overall health, biggest change from last week]

## Key Metrics
| Metric | This Week | Last Week | 4-Week Avg | Status |
|--------|-----------|-----------|------------|--------|
| At-risk users identified | N | N | N | — |
| Intervention reach | X% | Y% | Z% | OK/WARN/CRIT |
| Overall save rate | X% | Y% | Z% | OK/WARN/CRIT |
| Medium tier save rate | X% | Y% | Z% | OK/WARN/CRIT |
| High tier save rate | X% | Y% | Z% | OK/WARN/CRIT |
| Critical tier save rate | X% | Y% | Z% | OK/WARN/CRIT |
| 30-day retention of saved users | X% | Y% | Z% | OK/WARN/CRIT |

## Channel Performance
| Channel | Response Rate | Save Rate | Median Response Time | Cost/Save |
|---------|-------------|-----------|---------------------|-----------|
| In-app message | X% | Y% | Zh | $N |
| Email | X% | Y% | Zh | $N |
| Personal outreach | X% | Y% | Zh | $N |

## Biggest Opportunity
[The single tier + channel + segment combination where improving save rate would prevent the most churn. Include estimated revenue impact.]

## Experiments in Flight
[Any active A/B tests from autonomous-optimization, with current results]

## Recommendations
[2-3 specific next steps for the agent]
```

3. Post the brief to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Feed signals to the optimization loop

This monitor's output feeds into the `autonomous-optimization` drill's Phase 1:

- Daily anomaly classifications become triggers for hypothesis generation
- The weekly brief's "Biggest Opportunity" becomes the starting point for the next experiment
- Channel performance data tells the optimization loop which channel to experiment on
- Segment data helps the loop target experiments at the right users

Store all signals in Attio in a consistent format:
- Record type: Note on play campaign record
- Properties: `metric_name`, `metric_value`, `expected_value`, `classification`, `tier`, `channel`, `segment`, `date`

## Output

- A PostHog dashboard with 6 panels tracking intervention health
- A daily n8n workflow that checks intervention metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes an intervention health brief
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 09:00 UTC (after churn-risk-scoring completes at 06:00)
- Weekly brief: cron, Monday 10:00 UTC
- Critical alerts: real-time via daily check or PostHog actions
