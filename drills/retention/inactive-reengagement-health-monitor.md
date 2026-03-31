---
name: inactive-reengagement-health-monitor
description: Monitor reengagement sequence performance per inactivity cohort, detect delivery or conversion regressions, and generate weekly winback health briefs
category: Retention
tools:
  - PostHog
  - Loops
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-custom-events
  - loops-audience
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Inactive Reengagement Health Monitor

This drill builds an always-on monitoring system for email reengagement campaigns targeting inactive users. It tracks how each inactivity cohort responds to reengagement sequences, detects when open rates, click rates, or return rates regress, and produces a weekly health brief that tells the agent exactly where to focus optimization effort.

This drill is play-specific to `email-reengagement-inactive` and complements the `autonomous-optimization` drill by providing the monitoring signal layer that the optimization loop acts on.

## Prerequisites

- PostHog tracking installed with reengagement events (`reengagement_email_sent`, `reengagement_email_opened`, `reengagement_email_clicked`, `reengagement_user_returned`, `reengagement_user_reactivated`)
- Loops sequences active with at least 2 weeks of send data
- n8n instance with PostHog, Loops, and Slack/email credentials configured
- Attio configured with a campaign record for the email-reengagement-inactive play
- Inactivity cohorts defined in PostHog (7-14 day inactive, 14-30 day, 30-60 day, 60+ day)

## Steps

### 1. Define the reengagement metric suite

Using the `posthog-cohorts` fundamental, define the metrics this monitor tracks:

- **Sequence entry rate:** Percentage of newly inactive users who enter a reengagement sequence within 24 hours of qualifying. Drops here signal a sync issue between PostHog and Loops.
- **Email delivery rate per step:** Delivery rate for each email in each sequence variant. Track per inactivity cohort. Drops signal deliverability or list hygiene issues.
- **Open rate per step per cohort:** Open rate for each email step, broken down by inactivity duration cohort. Longer-inactive users typically open at lower rates. A drop in the 7-14 day cohort is more alarming than a drop in the 60+ day cohort.
- **Click-to-open rate per step:** Of users who opened, what percentage clicked the CTA. This measures content relevance independently of deliverability.
- **Return rate per cohort:** Percentage of users in each inactivity cohort who log back in within 7 days of sequence start. This is the primary outcome metric.
- **Reactivation rate per cohort:** Percentage of returned users who complete a meaningful product action (not just login) within 14 days. This separates curiosity from real reengagement.
- **Unsubscribe rate per step:** Unsubscribes triggered by each email step. Spikes here mean the content or frequency is wrong for that cohort.

### 2. Build the reengagement health dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "Reengagement Health" dashboard with these panels:

1. **Sequence funnel waterfall:** Current week's email_sent -> email_opened -> email_clicked -> user_returned -> user_reactivated funnel, showing step-by-step conversion and absolute drop-off.
2. **Return rate trend by cohort:** Weekly return rate for each inactivity cohort over the last 12 weeks. One line per cohort (7-14d, 14-30d, 30-60d, 60+d). Add horizontal threshold lines at the play's targets.
3. **Email performance heatmap:** Rows = sequence steps (Email 1, 2, 3...), columns = inactivity cohorts. Cell value = open rate. Color-code: green if above 25%, yellow if 15-25%, red if below 15%.
4. **Reactivation quality:** Of users who returned, what percentage completed a meaningful action within 14 days. Broken down by cohort and by the specific CTA they clicked.
5. **Unsubscribe rate trend:** Weekly unsubscribe rate per sequence step. Any step consistently above 0.5% needs content revision.
6. **Cohort volume tracker:** How many users entered each inactivity cohort this week, how many entered reengagement sequences, and the gap (if any users were missed).

### 3. Build the daily check workflow

Using `n8n-scheduling`, create a daily cron workflow (run at 09:00 UTC):

1. Query PostHog for yesterday's reengagement metrics:
   - Users entering each inactivity cohort
   - Users entering reengagement sequences (should match cohort entries)
   - Emails sent, delivered, opened, clicked per step per cohort
   - Users returned yesterday (any login from a user currently in a sequence)
   - Unsubscribes triggered yesterday
2. Using `posthog-anomaly-detection`, compare yesterday's metrics against the 4-week rolling average:
   - **Normal:** Within +/- 10% of rolling average. Log to Attio using `attio-notes`, no action.
   - **Warning:** Open rate or return rate dropped 10-20% below average for any cohort. Log with warning flag.
   - **Critical:** Return rate dropped >20% below average, OR overall reactivation rate dropped below the play's pass threshold, OR unsubscribe rate for any step exceeds 1%. Log, send Slack alert, trigger investigation.
3. For critical alerts, include context: which cohort and step saw the biggest change, whether the issue is deliverability (delivery rate down), relevance (opens down), or content (clicks down despite opens), and any correlated product events.

Alert format:
```
REENGAGEMENT ALERT: [metric_name] for [cohort] dropped to [X%] (expected [Y%])
- Overall return rate: [Z%] (threshold: [T%])
- Worst step: Email [N] at [rate%] open rate
- Sequence entry gap: [N] users missed (not entered into sequence)
- Possible cause: [deliverability issue | content staleness | product change | seasonal pattern]
- Recommended action: [check Loops delivery logs | refresh email copy | verify PostHog-Loops sync | review cohort definitions]
```

### 4. Build the weekly reengagement health brief

Using `n8n-scheduling`, create a weekly cron workflow (run Monday 09:00 UTC):

1. Aggregate the past week's data:
   - Total users entering inactivity cohorts, total entering sequences, overall return rate, overall reactivation rate
   - Per-cohort return rates with comparison to prior week and 4-week average
   - Best and worst performing cohort
   - Best and worst performing email step (by click-to-open rate)
   - Unsubscribe rate by step with trend
   - Number of anomalies detected during the week
2. Using `n8n-workflow-basics`, generate the brief via Claude API:
   - Input: This week's metrics, last week's metrics, 4-week averages, anomalies, any active experiments
   - Output: A structured brief:

```
# Reengagement Health Brief — Week of [date]

## Summary
[1-2 sentences: overall health, biggest change]

## Key Metrics
| Cohort | Return Rate | vs Last Week | vs 4-Week Avg | Status |
|--------|-------------|-------------|----------------|--------|
| 7-14d  | X%          | +/-Y%       | +/-Z%          | OK/WARN/CRIT |
| 14-30d | X%          | +/-Y%       | +/-Z%          | OK/WARN/CRIT |
| 30-60d | X%          | +/-Y%       | +/-Z%          | OK/WARN/CRIT |
| 60+d   | X%          | +/-Y%       | +/-Z%          | OK/WARN/CRIT |

## Email Step Performance
| Step | Open Rate | CTOR | Unsub Rate | Status |
|------|-----------|------|------------|--------|
| Email 1 | X% | Y% | Z% | OK/WARN/CRIT |
| ...     | ...| ... | ...| ...          |

## Biggest Opportunity
[The single cohort + email step combination where improvement would yield the largest return rate lift. Include estimated impact.]

## Sequence Gap Analysis
[How many users were missed — entered inactivity cohort but not sequence. Root cause if gap > 0.]

## Experiments in Flight
[Any active A/B tests from autonomous-optimization, with current results if available]

## Recommendations
[2-3 specific, actionable next steps for the agent to execute]
```

3. Post the brief to Slack and store in Attio using `attio-notes` on the play's campaign record.

### 5. Set up regression trip-wires

Beyond daily checks, configure immediate alerts for critical regressions:

- **Overall return rate < play threshold** for 3 consecutive days: Immediate alert. The play is failing.
- **Any cohort's open rate drops below 10%** when it was previously above 20%: Immediate alert. Likely a deliverability issue.
- **Unsubscribe rate for any single email step exceeds 1.5%**: Immediate alert. That email is actively harming the list.
- **Sequence entry gap exceeds 20%** of qualifying users for 2 consecutive days: Immediate alert. The PostHog-to-Loops sync is broken.

These alerts bypass the daily summary and go directly to the team.

### 6. Feed signals to the optimization loop

This monitor's output feeds directly into the `autonomous-optimization` drill's Phase 1 (Monitor):

- Daily anomaly classifications (normal, warning, critical) become the trigger for hypothesis generation
- The weekly health brief's "Biggest Opportunity" becomes the starting point for the next experiment
- Per-step performance data tells the optimization loop which email to experiment on first
- Cohort-level data helps the optimization loop decide which inactivity segment to target

Store all signals in a consistent format in Attio so the optimization loop can query them programmatically:
- Record type: Note on play campaign record
- Properties: `metric_name`, `metric_value`, `expected_value`, `classification`, `cohort`, `email_step`, `date`

## Output

- A PostHog dashboard with 6 panels tracking reengagement health
- A daily n8n workflow that checks reengagement metrics and alerts on anomalies
- A weekly n8n workflow that generates and distributes a reengagement health brief
- Trip-wire alerts for critical regressions
- Structured signal data in Attio for the autonomous optimization loop

## Triggers

- Daily check: cron, 09:00 UTC
- Weekly brief: cron, Monday 09:00 UTC
- Regression alerts: real-time via PostHog actions or daily check
