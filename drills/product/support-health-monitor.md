---
name: support-health-monitor
description: Ongoing monitoring of support ticket trends, churn signal accuracy, and intervention effectiveness
category: Product
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - n8n-scheduling
  - attio-reporting
---

# Support Health Monitor

This drill creates an always-on monitoring system that tracks support ticket trends, validates churn prediction accuracy, and measures intervention effectiveness. It provides the observability layer that the `autonomous-optimization` drill uses to detect anomalies and drive experiments.

## Input

- PostHog events from `support-ticket-analysis` drill (support_ticket_classified, support_account_summary_updated, support_churn_score_calculated)
- Attio records with support churn scores and intervention logs
- n8n instance for scheduled monitoring
- At least 4 weeks of scored data for meaningful trends

## Steps

### 1. Build the support-churn dashboard

Use `posthog-dashboards` to create a dedicated dashboard with these panels:

- **Ticket volume trend**: Daily ticket count over 30 days. Overlay with churn events to visually correlate spikes.
- **Category distribution**: Stacked bar showing ticket categories per week. Watch for shifts (e.g., bug tickets increasing = product quality issue).
- **Churn score distribution**: Histogram of current churn risk scores across all active accounts. Healthy = skewed left (most accounts low risk).
- **Prediction accuracy**: Of accounts scored high/critical last month, what % actually churned? Of accounts that churned, what % were flagged? Track precision and recall monthly.
- **Intervention funnel**: Alerts generated -> CS acted on -> Customer re-engaged -> Churn prevented. Shows the save rate.
- **CSAT trend**: Rolling 30-day average CSAT. Leading indicator of overall support health.
- **Repeat issue tracker**: Top 5 most-repeated issue categories with count trend. Product team actionable.
- **Time to resolution by severity**: Are critical issues resolved faster? Track SLA compliance.

### 2. Configure anomaly alerts

Use `posthog-anomaly-detection` to set up automated alerts:

- Ticket volume >2x the 4-week average for 3 consecutive days (something broke)
- Average CSAT drops below 3.0 for 7 consecutive days (systemic support quality issue)
- High/critical risk account count increases >50% week-over-week (emerging churn wave)
- Prediction accuracy (precision) drops below 40% (model needs recalibration)
- Intervention save rate drops below 20% (CS approach needs revision)

### 3. Generate weekly support health report

Use `n8n-scheduling` to run a weekly report workflow:

1. Pull last 7 days of support metrics from PostHog
2. Pull intervention outcomes from Attio using `attio-reporting`
3. Compare to previous week and 4-week average
4. Generate a report with Anthropic:

```
Prompt: "Generate a support health report from this data.

This week's metrics:
{metrics_json}

Previous week:
{prev_metrics_json}

4-week average:
{avg_metrics_json}

Include:
1. Headline: one sentence summary (improving/stable/declining)
2. Key changes: what moved significantly this week
3. Top churn risks: accounts requiring immediate attention
4. Product signals: recurring issues that product team should address
5. Recommendation: one specific action for this week

Keep it under 300 words. Write for a CS team lead who makes decisions based on this report."
```

4. Post the report to Slack and store in Attio as a note on the support ops record.

### 4. Track product feedback signals

Use `posthog-cohorts` to create cohorts around specific product issues surfacing through support:

- Accounts with 2+ bug tickets about the same feature
- Accounts requesting the same missing feature
- Accounts hitting the same integration failure

These cohorts feed product prioritization: the feature/fix that would reduce the most support load (and therefore churn risk) should rank higher in the roadmap.

### 5. Monitor model drift

Monthly, compare the churn scoring model's predictions against actuals:

- Calculate precision: Of all high/critical scores, what % actually churned within 30 days?
- Calculate recall: Of all accounts that churned, what % were scored high/critical beforehand?
- Calculate false positive rate: What % of high/critical scores were false alarms?

If precision drops below 35% or recall drops below 50%, flag for recalibration (re-run `support-churn-correlation` drill Step 3 with fresh data).

## Output

- Live PostHog dashboard with support-churn metrics
- Automated anomaly alerts for support quality and churn risk trends
- Weekly support health reports delivered to Slack
- Product feedback signals aggregated by impact
- Model drift monitoring with recalibration triggers

## Triggers

- **Dashboard**: Always-on, updated in real-time as PostHog events flow
- **Anomaly alerts**: Checked daily via n8n cron
- **Weekly report**: Every Monday morning via n8n cron
- **Model drift check**: First of each month via n8n cron
