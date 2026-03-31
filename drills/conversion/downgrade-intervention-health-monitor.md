---
name: downgrade-intervention-health-monitor
description: Monitor downgrade prevention effectiveness across intent tiers, intervention channels, and offer types, generating weekly retention health briefs
category: Conversion
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Downgrade Intervention Health Monitor

This drill builds an always-on monitoring system for the downgrade-prevention play. It tracks how effectively interventions prevent downgrades across intent tiers, channels, offer types, and user segments, and produces a weekly health brief that tells the agent exactly where to focus optimization.

This drill complements the `autonomous-optimization` drill by providing the play-specific signal layer that the optimization loop acts on.

## Prerequisites

- PostHog tracking installed with downgrade intervention events (from `downgrade-intercept-flow` drill)
- `downgrade-intent-detection` drill running daily (provides intent tier data)
- At least 4 weeks of intervention data (sufficient for baseline metrics)
- n8n instance with PostHog and Slack/email credentials configured
- Attio configured with a campaign record for the downgrade-prevention play

## Steps

### 1. Define the downgrade prevention metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks:

- **Detection coverage:** Percentage of actual downgraders who were scored moderate+ before downgrading. Target: >80%. Low coverage means the detection model is missing signals.
- **Intervention reach:** Percentage of moderate+ intent users who received at least one intervention within 24 hours. Target: >90%.
- **Prevention rate by tier:** Percentage of users at each intent tier (moderate, high, imminent) who were prevented from downgrading (remained on current plan 30+ days post-intervention).
- **Intercept page effectiveness:** Of users who saw the downgrade page intercept, what percentage chose "keep plan" or "request discount" vs. "continue downgrade."
- **Offer acceptance rate:** Percentage of retention offers presented that were accepted, broken down by offer type (discount, pause, coaching).
- **Offer-to-retention:** Of users who accepted an offer, what percentage remained on their current plan 60 days after the offer expired? (Measures whether offers create lasting retention, not just delay.)
- **MRR saved:** Monthly recurring revenue retained by preventing downgrades. Calculated as: (users prevented * their plan delta per month).
- **Cost per save:** Total intervention cost (discounts given + agent time + tool costs) divided by number of saves.
- **Channel efficiency:** Prevention rate per channel (in-app message, email, personal outreach, intercept page) normalized by cost.

### 2. Build the downgrade prevention health dashboard

Using the `posthog-dashboards` fundamental, create a "Downgrade Prevention Health" dashboard:

1. **Prevention funnel:** Funnel from `downgrade_intent_scored` (tier >= moderate) -> `downgrade_intervention_sent` -> `downgrade_intervention_engaged` -> `downgrade_prevented`. Shows the full conversion from detection to lasting retention.
2. **Prevention rate by intent tier (trend):** Weekly prevention rate for moderate, high, and imminent tiers over the last 12 weeks. One line per tier.
3. **Intercept page conversion:** Funnel from `downgrade_intercept_shown` -> each action option (keep_plan, request_discount, continue_downgrade). Shows real-time intercept effectiveness.
4. **Offer performance:** Grouped bar chart: acceptance rate and 60-day retention rate for each offer type (discount, pause, coaching, feature education).
5. **MRR impact:** Stacked area chart: MRR saved by intervention type over the last 12 weeks, with MRR lost to downgrades overlaid.
6. **Channel comparison:** Side-by-side: prevention rate, engagement rate, and cost per save for each channel.
7. **Detection model health:** Precision, recall, and false positive rate from the latest `downgrade-intent-detection` calibration. Trend over last 6 calibrations.

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 09:00 UTC, after the `downgrade-intent-detection` workflow completes at 07:00):

1. Query PostHog for yesterday's downgrade prevention metrics:
   - New moderate+ intent users identified (by tier)
   - Interventions sent (by channel and tier)
   - Interventions engaged
   - Users who were prevented (remained on plan)
   - Users who downgraded despite intervention (lost)
   - Intercept page views and actions taken
   - Retention offers presented, accepted, fulfilled
2. Using `posthog-anomaly-detection`, compare yesterday's metrics against the 4-week rolling average:
   - **Normal:** Within +/- 10% of rolling average. Log to Attio, no action.
   - **Warning:** Prevention rate dropped 10-20% below average, OR intercept page bypass rate increased >15%, OR offer acceptance dropped >20%. Log with warning flag.
   - **Critical:** Prevention rate dropped >20% below average, OR overall prevention rate below play threshold, OR detection coverage dropped below 60%, OR MRR loss spike >50% above average. Log, send alert, trigger investigation.
3. For critical alerts, include:

```
DOWNGRADE PREVENTION ALERT: [metric] at [value] (expected [expected_value])
- Overall prevention rate: [X%] (threshold: [T%])
- MRR saved yesterday: $[N] (avg: $[M])
- MRR lost to downgrades: $[N] (avg: $[M])
- Worst performing tier: [tier] at [rate%]
- Worst performing channel: [channel] at [rate%]
- Possible cause: [detection drift | offer fatigue | channel saturation | product issue | competitor action]
- Recommended action: [recalibrate detection | rotate offers | test new channel | investigate product | check competitive landscape]
```

### 4. Build the weekly prevention health brief

Using `n8n-scheduling`, create a weekly cron workflow (Monday 10:00 UTC):

1. Aggregate the past week:
   - Total moderate+ intent users, total interventions, total saves, total losses
   - Prevention rate by tier, channel, and offer type with week-over-week and 4-week average comparison
   - MRR saved vs. MRR lost breakdown
   - Best and worst performing channel-tier-offer combinations
   - Intercept page stats: views, keep rate, discount request rate, bypass rate
   - Offer economics: total discount value given, MRR retained per dollar of discount
   - Detection model accuracy from latest calibration

2. Using `n8n-workflow-basics`, generate the brief via Claude API:

```
# Downgrade Prevention Health Brief -- Week of [date]

## Summary
[1-2 sentences: overall health, biggest change from last week]

## Key Metrics
| Metric | This Week | Last Week | 4-Week Avg | Status |
|--------|-----------|-----------|------------|--------|
| Moderate+ intent users detected | N | N | N | -- |
| Overall prevention rate | X% | Y% | Z% | OK/WARN/CRIT |
| Moderate tier prevention rate | X% | Y% | Z% | OK/WARN/CRIT |
| High tier prevention rate | X% | Y% | Z% | OK/WARN/CRIT |
| Imminent tier prevention rate | X% | Y% | Z% | OK/WARN/CRIT |
| Intercept page keep rate | X% | Y% | Z% | OK/WARN/CRIT |
| Offer acceptance rate | X% | Y% | Z% | OK/WARN/CRIT |
| MRR saved | $N | $N | $N | OK/WARN/CRIT |
| Cost per save | $N | $N | $N | OK/WARN/CRIT |

## Offer Economics
| Offer Type | Shown | Accepted | Accept Rate | 60-Day Retention | ROI |
|-----------|-------|----------|-------------|------------------|-----|
| 20% discount (3mo) | N | N | X% | Y% | Z:1 |
| Plan pause (30d) | N | N | X% | Y% | Z:1 |
| Free coaching session | N | N | X% | Y% | Z:1 |
| Feature education | N | N | X% | Y% | Z:1 |

## Biggest Opportunity
[The single tier + channel + offer combination where improving prevention rate would save the most MRR. Include estimated monthly revenue impact.]

## Experiments in Flight
[Any active A/B tests from autonomous-optimization, with current results]

## Recommendations
[2-3 specific next steps for the agent]
```

3. Post the brief to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Feed signals to the optimization loop

This monitor's output feeds into the `autonomous-optimization` drill's Phase 1:

- Daily anomaly classifications become triggers for hypothesis generation
- The weekly brief's "Biggest Opportunity" informs the next experiment target
- Offer economics data tells the optimization loop which offers to test variations of
- Channel performance tells the loop which delivery method to experiment on
- Tier-level data identifies where the detection model or intervention flow needs tuning

Store all signals in Attio in a consistent format:
- Record type: Note on play campaign record
- Properties: `metric_name`, `metric_value`, `expected_value`, `classification`, `tier`, `channel`, `offer_type`, `date`

## Output

- A PostHog dashboard with 7 panels tracking downgrade prevention health
- A daily n8n workflow that checks prevention metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes a prevention health brief
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 09:00 UTC (after downgrade-intent-detection completes at 07:00)
- Weekly brief: cron, Monday 10:00 UTC
- Critical alerts: real-time via daily check
