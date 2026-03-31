---
name: usage-revenue-optimization-report
description: Generate weekly usage-to-revenue efficiency reports showing per-tier ARPU trends, tier migration flow, overage revenue health, and pricing model drift detection
category: Product
tools:
  - PostHog
  - Stripe
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - billing-event-streaming
  - stripe-usage-records
  - n8n-scheduling
  - attio-reporting
---

# Usage Revenue Optimization Report

This drill generates a weekly report that connects product usage data to billing outcomes for usage-based pricing models. It answers: is usage growing faster than revenue (value leak), is overage revenue healthy or causing bill shock churn, are tier boundaries still aligned with the usage distribution, and where should the next pricing experiment focus.

This is the play-specific monitoring layer for the `usage-based-pricing` play at Durable level. Its output feeds directly into the `autonomous-optimization` drill as context for hypothesis generation.

## Input

- PostHog with usage events and billing events (via `billing-event-streaming`)
- Stripe with metered billing configured (meters, usage records, tiered prices)
- At least 90 days of combined usage + billing data
- n8n instance for scheduled report generation
- Attio for storing weekly snapshots

## Steps

### 1. Compute usage-to-revenue efficiency metrics

Build a PostHog HogQL query that joins usage and billing data per account per month:

```sql
SELECT
  properties.account_id AS account_id,
  properties.plan_tier AS plan_tier,
  sum(CASE WHEN event = 'resource_consumed' THEN properties.current_count ELSE 0 END) AS total_usage_30d,
  max(CASE WHEN event = 'billing_invoice_paid' THEN properties.amount_usd ELSE 0 END) AS revenue_30d,
  CASE
    WHEN sum(CASE WHEN event = 'billing_invoice_paid' THEN properties.amount_usd ELSE 0 END) > 0
    THEN sum(CASE WHEN event = 'resource_consumed' THEN properties.current_count ELSE 0 END) /
         sum(CASE WHEN event = 'billing_invoice_paid' THEN properties.amount_usd ELSE 0 END)
    ELSE 0
  END AS usage_per_dollar
FROM events
WHERE timestamp > now() - interval 30 day
  AND event IN ('resource_consumed', 'billing_invoice_paid')
GROUP BY account_id, plan_tier
ORDER BY usage_per_dollar DESC
```

Key derived metrics:
- **Usage per dollar (UPD):** Higher UPD means customers extract more value per dollar. Rising UPD across cohorts means your pricing leaks value. Falling UPD means you may be overcharging.
- **Revenue per usage unit (RPU):** Inverse of UPD. Tracks pricing efficiency. Should be stable or increasing.
- **Overage revenue ratio:** overage_revenue / total_revenue. Healthy range: 10-30%. Below 10% means tiers are too generous. Above 40% means bill shock risk.

### 2. Track tier migration flow

Query PostHog for plan changes over the past 30 days:

```sql
SELECT
  properties.previous_plan AS from_tier,
  properties.change_type AS direction,
  properties.plan_name AS to_tier,
  count() AS migration_count,
  avg(properties.mrr_change) AS avg_mrr_change
FROM events
WHERE event = 'billing_subscription_updated'
  AND timestamp > now() - interval 30 day
  AND properties.change_type IN ('upgrade', 'downgrade')
GROUP BY from_tier, direction, to_tier
ORDER BY migration_count DESC
```

Build a tier migration matrix showing:
- Upgrade flow: Free -> Starter (count, avg MRR increase), Starter -> Pro (count, avg MRR increase)
- Downgrade flow: Pro -> Starter (count, avg MRR loss), Starter -> Free (count, avg MRR loss)
- Net flow per tier: is each tier growing or shrinking?
- Auto-upgrade vs. self-serve upgrade ratio (from `auto_upgrade_completed` events)

Alert condition: if net flow for any tier is negative for 3 consecutive weeks, flag for investigation.

### 3. Detect pricing model drift

Compare the current usage distribution against the distribution that was used to set tier boundaries (stored from the initial `usage-pricing-model-analysis` run):

Using `posthog-cohorts`, re-compute the percentile breakpoints for the value metric:

- Current P50, P80, P95 of usage
- Compare against the original P50, P80, P95 that defined tier boundaries

If any percentile has shifted by more than 20%, the tier boundaries no longer match the usage distribution. Flag for re-analysis:

```javascript
posthog.capture('pricing_model_drift_detected', {
  metric: 'api_calls',
  original_p80: 8000,
  current_p80: 12500,
  drift_pct: 56,
  recommendation: 'Tier boundary at 10,000 now captures only 65% of users instead of 80%. Consider raising the boundary or adding an intermediate tier.'
});
```

### 4. Compute bill shock indicators

Bill shock (invoice amount much higher than expected) is the top driver of churn in usage-based models. Query for accounts experiencing invoice growth:

```sql
SELECT
  properties.account_id AS account_id,
  properties.amount_usd AS current_invoice,
  lagInFrame(properties.amount_usd, 1) OVER (PARTITION BY properties.account_id ORDER BY timestamp) AS previous_invoice,
  CASE
    WHEN lagInFrame(properties.amount_usd, 1) OVER (PARTITION BY properties.account_id ORDER BY timestamp) > 0
    THEN (properties.amount_usd - lagInFrame(properties.amount_usd, 1) OVER (PARTITION BY properties.account_id ORDER BY timestamp))
         / lagInFrame(properties.amount_usd, 1) OVER (PARTITION BY properties.account_id ORDER BY timestamp) * 100
    ELSE 0
  END AS invoice_growth_pct
FROM events
WHERE event = 'billing_invoice_paid'
  AND timestamp > now() - interval 60 day
HAVING invoice_growth_pct > 50
ORDER BY invoice_growth_pct DESC
```

Classify accounts:
- **Mild growth (50-100% increase):** Normal for growing teams. Monitor but do not alert.
- **Significant growth (100-200% increase):** Send a proactive usage summary email before next invoice. "Your usage grew significantly this month. Here is what drove the change."
- **Shock risk (>200% increase):** Flag for immediate outreach. These accounts churn within 60 days at 3x the normal rate if not contacted.

### 5. Generate the weekly report

Using `n8n-scheduling`, build a workflow that runs every Monday at 08:00 UTC:

1. Run all four analysis queries above
2. Compile into a structured report:

```
Usage-Based Pricing Weekly Report — {date}

== Revenue Efficiency ==
Overall ARPU: ${current} ({change}% WoW)
Revenue per usage unit: ${rpu} ({change}% WoW)
Overage revenue ratio: {ratio}% (target: 10-30%)

== Tier Migration ==
Net upgrades: {count} (+${mrr_gained}/mo)
Net downgrades: {count} (-${mrr_lost}/mo)
Auto-upgrade acceptance rate: {rate}%
Tier health: {each tier growing/shrinking/stable}

== Model Drift ==
P80 usage: {current} (boundary set at: {boundary})
Drift status: {aligned | drifting | misaligned}
Action: {none | monitor | re-analyze tiers}

== Bill Shock ==
Accounts with >100% invoice growth: {count}
Accounts at shock risk (>200%): {count}
Proactive outreach sent: {count}

== Optimization Candidates ==
1. {highest-impact finding with recommended experiment}
2. {second finding}
3. {third finding}
```

3. Store the report as an Attio note on the pricing project record using `attio-reporting`
4. Post to Slack
5. Feed the "Optimization Candidates" section into `autonomous-optimization` as experiment hypotheses

### 6. Track report accuracy

After each weekly report, log the predictions and revisit them the following week:

```javascript
posthog.capture('usage_revenue_report_generated', {
  arpu: currentArpu,
  overage_ratio: overageRatio,
  drift_status: driftStatus,
  shock_risk_accounts: shockRiskCount,
  optimization_candidates: candidateCount,
  report_week: weekNumber
});
```

Monthly: review which optimization candidates from past reports led to successful experiments. This calibrates the report's hypothesis quality over time.

## Output

- Weekly usage-to-revenue efficiency report
- Tier migration flow analysis
- Pricing model drift detection with re-analysis triggers
- Bill shock early warning system
- Optimization candidate generation for the `autonomous-optimization` drill
- Monthly report accuracy calibration

## Triggers

Runs weekly via n8n cron (Monday 08:00 UTC). On-demand via webhook after pricing changes or major product launches. Drift detection triggers `usage-pricing-model-analysis` re-run when misalignment exceeds 20%.
