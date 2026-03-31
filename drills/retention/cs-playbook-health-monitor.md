---
name: cs-playbook-health-monitor
description: Monitor CS playbook adoption, intervention success rates, and retention impact across all documented playbooks
category: Retention
tools:
  - PostHog
  - Attio
  - Intercom
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - attio-reporting
  - attio-notes
  - intercom-conversations-export
  - n8n-scheduling
  - n8n-workflow-basics
---

# CS Playbook Health Monitor

This drill builds an always-on monitoring system that tracks how well each CS intervention playbook performs: how often it is triggered, how often it succeeds, and how much churn it prevents. It produces a weekly brief that tells the agent which playbooks need improvement, retirement, or expansion.

This drill complements the `autonomous-optimization` drill by providing the play-specific signal layer. The optimization loop acts on the signals this monitor produces.

## Prerequisites

- PostHog tracking active with intervention events (`playbook_triggered`, `playbook_step_completed`, `playbook_outcome_logged`)
- At least 5 documented CS playbooks being executed
- `churn-risk-scoring` or `churn-signal-extraction` drill running daily
- Intervention outcomes tracked in Attio (from `churn-intervention-routing`)
- n8n instance with PostHog, Attio, and Slack credentials configured

## Steps

### 1. Define the playbook metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks per playbook:

- **Trigger rate:** How often each playbook is invoked per week. A playbook that never triggers may be irrelevant or too narrowly scoped.
- **Completion rate:** Percentage of triggered playbooks where all intervention steps were completed (not abandoned mid-playbook). Low completion signals the playbook is too complex or steps are failing.
- **Success rate:** Percentage of completed playbooks where the customer's churn risk score improved within 14 days. This is the core effectiveness metric.
- **Time-to-resolution:** Median hours from playbook trigger to risk score improvement. Faster playbooks are more efficient.
- **Retention impact:** Of customers saved by each playbook, what percentage are still active 60 days later? Prevents counting temporary re-engagement as a real save.
- **Cost per save:** Estimated cost (human time + tool cost) per successful intervention, per playbook.
- **Scenario coverage:** Percentage of at-risk customers whose churn signal matches an existing playbook. Gaps mean new playbooks are needed.

### 2. Build the playbook performance dashboard

Using the `posthog-dashboards` fundamental, create a "CS Playbook Health" dashboard:

1. **Playbook usage funnel:** `playbook_triggered` -> `playbook_step_completed` (all steps) -> `playbook_outcome_logged (success=true)` -> `customer_retained_60d`. One funnel per playbook.
2. **Success rate by playbook (trend):** Weekly success rate for each playbook over the last 12 weeks. Line chart, one line per playbook.
3. **Scenario coverage heatmap:** Matrix of churn signal types (activity_decay, feature_abandonment, support_escalation, billing_concern, team_shrinkage) vs. playbooks that address them. Gaps are visible.
4. **Top and bottom performers:** Table ranking playbooks by success rate, sorted descending. Highlights the bottom 2 playbooks (candidates for revision) and top 2 (candidates for scaling).
5. **Unmatched at-risk users:** Count of at-risk users (medium+ risk tier) whose primary churn signal does not match any existing playbook. Trend over time.
6. **Playbook step drop-off:** For each playbook, which step has the highest abandonment rate? This identifies where playbooks break.

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 10:00 UTC, after churn scoring at 06:00 and intervention routing at 08:00):

1. Query PostHog for yesterday's playbook metrics:
   - Playbooks triggered (by playbook name and churn signal)
   - Playbooks completed vs. abandoned
   - Intervention outcomes logged
   - At-risk users not matched to any playbook
2. Using `posthog-anomaly-detection`, compare yesterday's metrics against the 4-week rolling average:
   - **Normal:** Within +/- 10% of rolling average. Log to Attio, no action.
   - **Warning:** Any playbook's success rate dropped 15-25% below average, OR scenario coverage dropped below 70%. Log with warning flag.
   - **Critical:** Any playbook's success rate dropped >25% below average, OR overall playbook success rate below play threshold, OR unmatched at-risk users exceed 30% of total at-risk population. Log, send alert, trigger investigation.
3. For critical alerts, include: which playbook underperformed, whether the churn model's signal distribution shifted (new signal types the playbooks do not cover), and recommended action.

Alert format:
```
CS PLAYBOOK ALERT: [metric] at [value] (expected [expected_value])
- Overall playbook success rate: [X%] (threshold: [T%])
- Worst playbook: [name] at [rate%] success
- Unmatched at-risk users: [N] ([%] of total at-risk)
- Possible cause: [signal shift | playbook staleness | execution failure | model drift]
- Recommended action: [revise playbook | create new playbook | recalibrate scoring | check automation]
```

### 4. Build the weekly playbook health brief

Using `n8n-scheduling`, create a weekly cron workflow (run Monday 11:00 UTC):

1. Aggregate the past week per playbook:
   - Trigger count, completion rate, success rate, time-to-resolution
   - Comparison to prior week and 4-week average
   - Step-level drop-off analysis for any playbook with completion rate below 70%
   - Unmatched signal analysis: which churn signal types lack a playbook
2. Generate the brief via Claude API:

```
# CS Playbook Health Brief -- Week of [date]

## Summary
[1-2 sentences: overall health, biggest change from last week]

## Playbook Performance
| Playbook | Triggers | Completion | Success Rate | Δ vs Last Week | 60-Day Retention | Status |
|----------|----------|------------|-------------|----------------|------------------|--------|
| [name]   | N        | X%         | Y%          | +/-Z%          | W%               | OK/WARN/CRIT |

## Scenario Coverage
- Covered churn signals: [list]
- Uncovered churn signals: [list with frequency]
- Coverage rate: [X%] of at-risk users matched to a playbook

## Biggest Opportunity
[The single playbook or missing scenario where improvement would prevent the most churn. Include estimated revenue impact: N at-risk users x average MRR.]

## Experiments in Flight
[Any active A/B tests from autonomous-optimization, with current results]

## Recommendations
[2-3 specific next steps for the agent: revise a failing playbook, create a new playbook for an uncovered scenario, scale a high-performing playbook to a new segment]
```

3. Post to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Feed signals to the optimization loop

This monitor's output feeds into the `autonomous-optimization` drill's Phase 1:

- Daily anomaly classifications become triggers for hypothesis generation
- The weekly brief's "Biggest Opportunity" becomes the starting point for the next experiment
- Playbook success rate trends tell the optimization loop which playbook to experiment on
- Step drop-off data tells the loop which specific intervention step to A/B test

Store all signals in Attio in a consistent format:
- Record type: Note on play campaign record
- Properties: `playbook_name`, `metric_name`, `metric_value`, `expected_value`, `classification`, `date`

## Output

- A PostHog dashboard with 6 panels tracking playbook health
- A daily n8n workflow that checks playbook metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes a playbook health brief
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 10:00 UTC (after churn scoring + intervention routing)
- Weekly brief: cron, Monday 11:00 UTC
- Critical alerts: real-time via daily check
