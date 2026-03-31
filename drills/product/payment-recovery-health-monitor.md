---
name: payment-recovery-health-monitor
description: Track payment failure rates, recovery rates, and dunning sequence effectiveness with weekly health reports
category: Product
tools:
  - PostHog
  - Stripe
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-custom-events
  - stripe-subscription-status
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Payment Recovery Health Monitor

This drill builds the measurement layer for the billing-issue-prevention play. It tracks payment failure rates, recovery rates by failure type and dunning step, time-to-recovery, and involuntary churn from failed payments. Outputs a weekly health report and fires alerts when metrics deviate from baselines.

## Prerequisites

- `payment-failure-detection` drill running and logging events to PostHog
- `dunning-sequence-automation` drill running and logging intervention events
- PostHog with at least 2 weeks of payment failure event data
- n8n instance for scheduled reporting

## Steps

### 1. Build the recovery funnel in PostHog

Using `posthog-funnels`, create a funnel tracking the full recovery journey:

```
payment_failure_detected
  -> dunning_email_sent (step = 1)
  -> dunning_email_opened
  -> payment_update_link_clicked
  -> payment_failure_recovered
```

Create variant funnels filtered by:
- Failure classification (expired_card, insufficient_funds, etc.)
- Recovery priority tier (high, medium, low)
- Account MRR bracket ($0-50, $50-200, $200-1000, $1000+)
- Dunning channel (in-app, email, human)

These funnels show where recovery drops off: do customers open the email but not click? Click but not complete the update? This data drives optimization.

### 2. Build the payment health dashboard

Using `posthog-dashboards`, create a "Payment Recovery Health" dashboard with these panels:

**Panel 1 — Failure Rate Trend (line chart, 12 weeks)**
Query: `payment_failure_detected` events per week / total active subscriptions per week. Target: below 5% failure rate.

**Panel 2 — Recovery Rate by Failure Type (bar chart)**
Query: `payment_failure_recovered` / `payment_failure_detected` grouped by `failure_classification`. Shows which failure types are easiest/hardest to recover.

**Panel 3 — Time to Recovery (histogram)**
Query: time difference between `payment_failure_detected` and `payment_failure_recovered` per account. Target: median < 3 days.

**Panel 4 — Dunning Step Effectiveness (funnel)**
Query: the recovery funnel from Step 1 — which step of the dunning sequence drives the most recoveries?

**Panel 5 — Involuntary Churn Rate (line chart, 12 weeks)**
Query: `payment_failure_churned` events per week / total active subscriptions per week. This is the ultimate metric — involuntary churn that the play failed to prevent.

**Panel 6 — Revenue at Risk vs. Recovered (stacked bar, weekly)**
Query: sum of `amount_due` from `payment_failure_detected` vs. sum of `amount_due` from `payment_failure_recovered`. Shows dollar impact.

### 3. Set up threshold alerts

Using `posthog-custom-events` and n8n, build alert rules:

- **Failure rate spike:** If weekly failure rate exceeds 2x the 4-week average, alert immediately. Could indicate a billing system issue, card network problem, or pricing change impact.
- **Recovery rate drop:** If weekly recovery rate drops below 50% (when baseline is 65%+), alert within 24 hours. Dunning sequence may need adjustment.
- **Time-to-recovery increase:** If median time to recovery exceeds 7 days (when baseline is 3 days), alert. Emails may be going to spam or the update flow is broken.
- **High-value failure:** If any single account with MRR > $1000 enters payment failure, alert the account owner immediately regardless of other thresholds.

### 4. Generate weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

1. Query PostHog for all payment events in the last 7 days
2. Query Stripe for current open invoices and past-due subscriptions using `stripe-subscription-status`
3. Compute:
   - Total failures this week
   - Recovery rate this week vs. 4-week average
   - Median time to recovery
   - Revenue at risk (sum of open invoice amounts)
   - Revenue recovered (sum of recovered invoice amounts)
   - Involuntary churn count
   - Top failure code this week
   - Dunning step with highest conversion rate
4. Format as a report:

```
# Payment Recovery Weekly — {{week_of}}

## Summary
| Metric | This Week | 4-Week Avg | Trend |
|--------|-----------|------------|-------|
| Failures | {{n}} | {{avg}} | {{arrow}} |
| Recovery Rate | {{pct}}% | {{avg_pct}}% | {{arrow}} |
| Median Time to Recover | {{days}}d | {{avg_days}}d | {{arrow}} |
| Revenue at Risk | ${{at_risk}} | ${{avg_risk}} | {{arrow}} |
| Revenue Recovered | ${{recovered}} | ${{avg_recovered}} | {{arrow}} |
| Involuntary Churn | {{n}} | {{avg}} | {{arrow}} |

## Failure Breakdown
| Type | Count | Recovery Rate |
|------|-------|---------------|
| Expired Card | {{n}} | {{pct}}% |
| Insufficient Funds | {{n}} | {{pct}}% |
| Card Declined | {{n}} | {{pct}}% |
| Auth Required | {{n}} | {{pct}}% |

## Dunning Effectiveness
| Step | Sent | Recovered After | Conversion |
|------|------|-----------------|------------|
| In-App Banner | {{n}} | {{n}} | {{pct}}% |
| Email 1 (Day 0) | {{n}} | {{n}} | {{pct}}% |
| Email 2 (Day 3) | {{n}} | {{n}} | {{pct}}% |
| Email 3 (Day 7) | {{n}} | {{n}} | {{pct}}% |
| Email 4 (Day 12) | {{n}} | {{n}} | {{pct}}% |
| Human Outreach | {{n}} | {{n}} | {{pct}}% |

## Action Items
{{agent-generated recommendations based on data}}
```

5. Post to Slack and store in Attio using `attio-reporting`

### 5. Track model accuracy monthly

Monthly, validate that the recovery likelihood scores from `payment-failure-detection` are accurate:

- For each failure classification, compare predicted recovery likelihood against actual recovery rate
- If predicted and actual differ by more than 15 percentage points, recalibrate the classification scores
- Log calibration results as a `payment_model_calibration` PostHog event

## Output

- PostHog recovery funnel and health dashboard
- Threshold alerts for failure spikes, recovery drops, and high-value failures
- Weekly payment recovery health report posted to Slack
- Monthly model calibration tracking
- Data foundation for autonomous optimization at Durable level

## Triggers

- Dashboard: always-on, refreshes automatically
- Alerts: real-time via n8n webhooks
- Weekly report: Monday 09:00 UTC
- Monthly calibration: first Monday of each month
