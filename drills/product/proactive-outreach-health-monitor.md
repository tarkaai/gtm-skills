---
name: proactive-outreach-health-monitor
description: Monitor proactive support outreach effectiveness — detection accuracy, outreach engagement, resolution rates, and retention impact — and generate weekly health briefs
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Proactive Outreach Health Monitor

This drill builds an always-on monitoring system for the proactive-support-outreach play. It tracks the full pipeline — from struggle detection accuracy through outreach delivery to resolution and retention outcomes — and produces weekly health briefs that feed into the `autonomous-optimization` drill.

This drill is play-specific. It complements `autonomous-optimization` by providing the signal layer that tells the optimization loop WHAT to experiment on.

## Prerequisites

- `struggle-signal-detection` drill running every 6 hours with PostHog events
- `proactive-outreach-pipeline` drill active with outreach events being tracked
- At least 4 weeks of detection + outreach data
- n8n instance connected to PostHog, Attio, and Slack/email
- Attio configured with a campaign record for the proactive-support-outreach play

## Steps

### 1. Define the metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks across the full pipeline:

**Detection metrics:**
- **Struggle detection volume:** Number of users flagged per day by tier (moderate, severe, critical). Trend over time.
- **Detection precision:** Of users flagged moderate+, what percentage actually had a genuine struggle (filed a ticket, churned, or had their struggle confirmed by session recording review)? Target: >60%.
- **Detection recall:** Of users who filed support tickets about confusion/errors, what percentage were flagged by struggle detection BEFORE the ticket? Target: >50%.
- **False positive rate:** Users flagged who resolved immediately on their own with no indication of real struggle. Target: <30%.

**Outreach metrics:**
- **Outreach reach:** Percentage of moderate+ users who received outreach within 6 hours of detection. Target: >90%.
- **Outreach engagement rate:** Percentage who interacted with outreach (clicked, replied, watched video, booked call). Break down by channel (in-app, email, human) and by tier.
- **Time to engagement:** Median hours from outreach delivery to first interaction. Target: <24 hours.
- **Cooldown suppression rate:** Percentage of re-detections suppressed by the 14-day cooldown. If >40%, the underlying struggles are not being resolved.

**Resolution metrics:**
- **Resolution rate:** Percentage of outreached users whose struggle score dropped below 10 within 7 days. Target: >40%.
- **Self-serve resolution rate:** Of resolved users, percentage who resolved via help link/article without human support.
- **Time to resolution:** Median days from first outreach to struggle score clearing.
- **Workflow-specific resolution rate:** Resolution rate broken down by `primary_stuck_workflow`. Identifies which workflows have effective help resources and which do not.

**Retention metrics:**
- **30-day retention after outreach:** Of users who received proactive outreach, percentage still active 30 days later.
- **Retention lift vs. control:** Compare 30-day retention of outreached users vs. similar-struggle-score users who were NOT outreached (from before the play launched, or from cooldown-suppressed users). This is the play's core value metric.
- **Support ticket deflection:** Reduction in support tickets from users who received proactive outreach vs. baseline ticket rate for similar struggle profiles.

### 2. Build the proactive outreach health dashboard

Using the `posthog-dashboards` fundamental, create a dedicated dashboard:

1. **Detection-to-resolution funnel:** `struggle_detected` -> `proactive_outreach_sent` -> `proactive_outreach_engaged` -> `proactive_outreach_resolved` -> `retained_30d`. Shows the full pipeline conversion.
2. **Struggle detection volume trend:** Daily count of users flagged by tier over last 12 weeks. Watch for spikes (product issue) or drops (detection drift).
3. **Outreach engagement by channel and tier:** Side-by-side bar chart. Engagement rate for in-app vs. email vs. human, segmented by struggle tier.
4. **Resolution rate by stuck workflow:** Bar chart showing resolution rate for each `primary_stuck_workflow` value. The lowest-resolution workflows need better help resources.
5. **Retention lift:** Line chart comparing 30-day retention of outreached cohort vs. non-outreached baseline. The gap between the lines is the play's value.
6. **Ticket deflection:** Weekly support ticket volume trend with overlay showing proactive outreach volume. As outreach increases, tickets should decrease.

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 10:00 UTC):

1. Query PostHog for the previous day's metrics across the full pipeline
2. Using `posthog-anomaly-detection`, compare against the 4-week rolling average. Classify each metric:
   - **Normal:** Within +/- 15% of rolling average. Log to Attio, no action.
   - **Warning:** Detection volume spiked >30% (possible product issue), OR engagement rate dropped 15-25%, OR resolution rate dropped 15-25%. Log with warning flag.
   - **Critical:** Engagement rate dropped >25% (outreach content is stale or irrelevant), OR resolution rate dropped >25% (help resources are broken or wrong), OR a specific workflow's resolution rate dropped to zero. Log, alert, trigger investigation.
3. For critical alerts, include diagnosis context:
   - Did a product deploy happen yesterday? (spike in new struggle patterns)
   - Did help article content change? (drop in resolution)
   - Is a specific workflow suddenly generating more struggles? (product regression)
   - Is the outreach being delivered? (check n8n workflow execution logs)

Alert format:
```
PROACTIVE OUTREACH ALERT: [metric] at [value] (expected [expected_value])
- Detection: [N] users flagged ([change vs. avg])
- Outreach reach: [X%] (target: >90%)
- Engagement: [X%] by [channel] (expected: [Y%])
- Resolution: [X%] (expected: [Y%])
- Worst workflow: [workflow_name] at [rate%] resolution
- Possible cause: [product regression | content drift | delivery failure | new struggle pattern]
- Recommended action: [update help content | investigate product change | check n8n | map new workflow]
```

### 4. Build the weekly health brief

Using `n8n-scheduling`, create a weekly cron workflow (run Monday 09:00 UTC):

1. Aggregate the past week's data across the full pipeline
2. Using `n8n-workflow-basics`, generate the brief:

```
# Proactive Support Outreach Health Brief — Week of [date]

## Summary
[1-2 sentences: overall health, biggest change from last week, whether play is on track]

## Pipeline Metrics
| Stage | This Week | Last Week | 4-Week Avg | Status |
|-------|-----------|-----------|------------|--------|
| Users flagged (moderate+) | N | N | N | — |
| Outreach reach | X% | Y% | Z% | OK/WARN/CRIT |
| Engagement rate (in-app) | X% | Y% | Z% | OK/WARN/CRIT |
| Engagement rate (email) | X% | Y% | Z% | OK/WARN/CRIT |
| Engagement rate (human) | X% | Y% | Z% | OK/WARN/CRIT |
| Resolution rate | X% | Y% | Z% | OK/WARN/CRIT |
| Self-serve resolution | X% | Y% | Z% | OK/WARN/CRIT |
| 30-day retention (outreached) | X% | Y% | Z% | OK/WARN/CRIT |
| Retention lift vs. baseline | +Xpp | +Ypp | +Zpp | OK/WARN/CRIT |
| Tickets deflected (est.) | N | N | N | — |

## Workflow Resolution Breakdown
| Stuck Workflow | Users | Outreached | Resolved | Resolution Rate |
|----------------|-------|-----------|----------|-----------------|
| [workflow_1] | N | N | N | X% |
| [workflow_2] | N | N | N | X% |
| ... | | | | |

## Biggest Opportunity
[The single workflow + channel combination where improving resolution rate would save the most users. Include estimated retention impact.]

## Experiments in Flight
[Any active A/B tests from autonomous-optimization, with current results]

## Recommendations
[2-3 specific next steps: update help content for workflow X, test new outreach timing, investigate detection false positives for workflow Y]
```

3. Post to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Feed signals to the optimization loop

This monitor's output feeds into the `autonomous-optimization` drill:

- **Daily anomaly classifications** become triggers for hypothesis generation (e.g., "email engagement dropped 20% — hypothesize: subject lines are stale, test new subject variants")
- **Weekly brief's "Biggest Opportunity"** becomes the starting experiment for the next optimization cycle
- **Workflow resolution data** tells the optimization loop which help resources to A/B test
- **Channel engagement data** tells the loop which delivery channel to experiment with for each tier

Store all signals in Attio in a consistent format on the play's campaign record:
- Properties: `metric_name`, `metric_value`, `expected_value`, `classification`, `struggle_tier`, `channel`, `workflow`, `date`

## Output

- A PostHog dashboard with 6 panels tracking the full detection-to-retention pipeline
- A daily n8n workflow that checks metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes a health brief
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 10:00 UTC (after struggle-signal-detection has run twice that day)
- Weekly brief: cron, Monday 09:00 UTC
- Critical alerts: real-time via daily check workflow
