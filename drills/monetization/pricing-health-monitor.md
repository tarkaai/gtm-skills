---
name: pricing-health-monitor
description: Continuously monitor pricing KPIs (ARPU, NRR, churn by plan, usage-to-revenue ratio) and alert on anomalies
category: Conversion
tools:
  - PostHog
  - Stripe
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - billing-event-streaming
  - n8n-scheduling
  - attio-reporting
---

# Pricing Health Monitor

This drill builds an always-on monitoring system for pricing-related metrics. It detects when pricing is causing churn, when usage patterns shift beyond current tier boundaries, and when revenue efficiency changes. This is the observation layer that feeds the `autonomous-optimization` drill at Durable level.

## Prerequisites

- `billing-event-streaming` fundamental configured (Stripe events flowing into PostHog)
- At least 90 days of billing + usage data in PostHog
- n8n instance for scheduled monitoring

## Steps

### 1. Build the pricing health dashboard

Using `posthog-dashboards`, create a "Pricing Health" dashboard with these panels:

**Revenue Panels:**
- ARPU trend (30-day rolling): total revenue / active customers
- ARPU by plan: breakdown per pricing tier
- Net Revenue Retention (NRR): monthly, trailing 12-month
- Expansion revenue: revenue from upgrades and usage growth
- Contraction revenue: revenue lost from downgrades

**Churn Panels:**
- Churn rate by plan: which plan has highest churn?
- Churn rate by usage band: are low-usage users churning more? (pricing too high for value received)
- Churn rate by tenure: is churn front-loaded (onboarding) or distributed (pricing fatigue)?
- Revenue churn vs. logo churn: losing big accounts or many small ones?

**Usage-to-Revenue Panels:**
- Usage per dollar spent: are customers getting more value per dollar over time? (good — means stickiness)
- Percentage of customers at plan limits: >30% means your tiers are too tight
- Overage revenue as percentage of total: >40% means the base plan is underpriced
- Usage growth rate vs. revenue growth rate: if usage grows faster than revenue, your pricing is leaking value

### 2. Set anomaly detection rules

Using `posthog-anomaly-detection`, configure alerts for:

| Metric | Alert Condition | Severity |
|--------|----------------|----------|
| ARPU | Drops >10% month-over-month | High |
| NRR | Falls below 100% for 2 consecutive months | Critical |
| Churn rate (any plan) | Exceeds 2x the 90-day average | High |
| Customers at plan limit | Exceeds 40% of plan subscribers | Medium |
| Overage complaints | >5 support tickets mentioning "bill" or "charge" in 7 days | High |
| Expansion revenue | Drops >20% month-over-month | Medium |

### 3. Build the daily monitoring workflow

Using `n8n-scheduling`, create a workflow that runs daily at 07:00 UTC:

1. Query PostHog for all pricing health metrics (ARPU, NRR, churn by plan, usage distribution)
2. Compare each metric against its 30-day rolling average and the anomaly thresholds from Step 2
3. If any metric is anomalous:
   a. Log `pricing_anomaly_detected` event in PostHog using `posthog-custom-events` with properties: `metric_name`, `current_value`, `baseline_value`, `severity`, `affected_plan`
   b. Create an Attio note on the pricing project record with the anomaly details
   c. If severity = Critical, send a Slack alert to the pricing owner
4. If all metrics are normal, log `pricing_health_check_passed` event

### 4. Build the weekly pricing digest

Using `n8n-scheduling`, create a weekly workflow (Monday 09:00 UTC):

1. Aggregate the full week's pricing health data
2. Compute week-over-week changes for all metrics
3. Identify the top 3 trends (positive or negative)
4. Generate a structured report:
   ```
   Pricing Health Digest — Week of {date}

   ARPU: ${current} ({change}% WoW)
   NRR: {current}% ({change}pp WoW)
   Churn by plan:
     - Free: {rate}%
     - Starter: {rate}%
     - Pro: {rate}%

   Top trends:
   1. {trend description}
   2. {trend description}
   3. {trend description}

   Action items:
   - {item if anomaly detected}
   ```
5. Post to Slack and store in Attio

### 5. Track pricing sensitivity cohorts

Using `posthog-cohorts`, maintain dynamic cohorts that signal pricing stress:

- **Pricing page visitors (active customers):** Users who visited the pricing/billing page 2+ times in 7 days while on a paid plan. This correlates with considering a change.
- **Limit-approaching:** Users at 80%+ of a plan limit. They will either upgrade or churn.
- **Overage shock:** Users whose last invoice was 50%+ higher than their previous invoice (usage spike causing bill shock).
- **Downgrade candidates:** Users whose usage dropped below the threshold for their current plan for 2+ consecutive weeks.

Update these cohorts daily. Feed them into the `churn-prevention` and `upgrade-prompt` drills.

### 6. Calibrate monthly

At the end of each month:

1. Compare predicted anomalies vs. actual outcomes. Were the alerts accurate?
2. Adjust thresholds: if false positives exceed 30%, tighten thresholds. If misses exceed 20%, loosen them.
3. Check if the usage distribution has shifted enough to warrant tier boundary changes (feed back into `usage-pricing-model-analysis`)
4. Log calibration results as a PostHog event: `pricing_monitor_calibration` with `precision`, `recall`, `threshold_changes`

## Output

- A PostHog dashboard with real-time pricing health visibility
- Daily anomaly detection with severity-based alerting
- Weekly pricing digest posted to Slack
- Dynamic cohorts tracking pricing stress signals
- Monthly calibration loop for monitoring accuracy

## Triggers

Daily monitoring runs via n8n cron. Weekly digest on Mondays. Monthly calibration on the 1st. On-demand via webhook for ad-hoc checks after pricing changes.
