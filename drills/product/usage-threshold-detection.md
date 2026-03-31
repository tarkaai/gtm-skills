---
name: usage-threshold-detection
description: Detect per-account usage approaching plan limits by comparing current consumption against plan caps, then classify urgency tiers for alert routing
category: Conversion
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - n8n-scheduling
  - n8n-triggers
  - attio-custom-attributes
  - attio-lists
---

# Usage Threshold Detection

This drill builds the system that identifies individual accounts approaching their plan limits — API calls, seats, storage, projects, or any metered resource. It operates at the per-account level, comparing current consumption against plan caps and classifying urgency so downstream alerts fire at the right time.

## Input

- PostHog tracking usage events per account (metered resources must be instrumented)
- Plan tier definitions with specific limits per resource (e.g., Free: 5 seats, Pro: 25 seats)
- n8n instance for scheduled detection runs
- Attio CRM for storing threshold proximity data

## Steps

### 1. Define metered resources and plan caps

Enumerate every resource that differs between plan tiers. For each resource, document the exact cap per tier:

| Resource | Free | Starter | Pro | Enterprise |
|----------|------|---------|-----|------------|
| Seats | 3 | 10 | 25 | Unlimited |
| API calls/mo | 1,000 | 10,000 | 100,000 | Unlimited |
| Projects | 5 | 20 | Unlimited | Unlimited |
| Storage (GB) | 1 | 10 | 100 | Unlimited |

Store this mapping as a JSON config accessible to n8n workflows. The detection system references this config to know each account's limits based on their current plan.

### 2. Instrument usage tracking in PostHog

Using the `posthog-custom-events` fundamental, ensure every metered resource emits events:

```javascript
posthog.capture('resource_consumed', {
  account_id: accountId,
  resource_type: 'api_calls',
  current_count: 8500,
  plan_limit: 10000,
  plan_tier: 'starter',
  pct_used: 85
});
```

If your product already tracks these internally, create a daily sync job that pushes current consumption totals to PostHog. The detection system needs `current_count` and `plan_limit` per resource per account.

### 3. Build the threshold detection query

Run a HogQL query to find accounts approaching limits:

```sql
SELECT
  properties.account_id AS account_id,
  properties.resource_type AS resource_type,
  properties.current_count AS current_count,
  properties.plan_limit AS plan_limit,
  properties.plan_tier AS plan_tier,
  round(properties.current_count / properties.plan_limit * 100, 1) AS pct_used
FROM events
WHERE event = 'resource_consumed'
  AND timestamp > now() - interval 1 day
  AND properties.plan_limit > 0
  AND properties.current_count / properties.plan_limit >= 0.7
ORDER BY pct_used DESC
```

This surfaces every account that has consumed 70%+ of any plan limit.

### 4. Classify urgency tiers

Assign each flagged account-resource pair to an urgency tier:

- **Approaching (70-84% consumed):** Early warning. Log it, but only alert if the consumption velocity suggests they will hit the limit within the current billing period.
- **Imminent (85-94% consumed):** The user will hit the limit soon. Trigger a helpful in-product alert and email.
- **Critical (95-100% consumed):** The user is at or about to hit the wall. Trigger an urgent alert with a one-click upgrade path.
- **Exceeded (>100% consumed, if soft limits):** The user has exceeded their limit. Show a blocking or degraded-experience prompt.

Using `posthog-cohorts`, create four dynamic cohorts: `usage-approaching`, `usage-imminent`, `usage-critical`, `usage-exceeded`. These update daily as the detection runs.

### 5. Compute consumption velocity

Raw percentage is not enough. An account at 80% on day 1 of their billing cycle is very different from 80% on day 28. Calculate the daily consumption rate and project the hit date:

```sql
SELECT
  account_id,
  resource_type,
  current_count,
  plan_limit,
  days_into_billing_period,
  days_remaining_in_period,
  current_count / greatest(days_into_billing_period, 1) AS daily_rate,
  (plan_limit - current_count) / greatest(current_count / greatest(days_into_billing_period, 1), 0.01) AS days_until_limit
FROM (
  -- subquery to compute billing period context per account
)
```

Accounts projected to hit the limit before period end get escalated one urgency tier. Accounts on track to stay well under the limit get de-escalated.

### 6. Store threshold data in the CRM

Using the `attio-custom-attributes` fundamental, add these fields to the company record in Attio:

- `usage_alert_tier`: approaching | imminent | critical | exceeded | healthy
- `usage_alert_resource`: which resource triggered the alert
- `usage_pct_consumed`: the percentage consumed
- `usage_projected_hit_date`: when they will hit the limit at current velocity
- `usage_alert_last_checked`: timestamp of last detection run
- `usage_plan_tier`: current plan

Using `attio-lists`, maintain a list called "Usage Threshold — Active Alerts" that auto-populates with all imminent, critical, and exceeded accounts.

### 7. Build the scheduled detection workflow

Using `n8n-scheduling`, create a workflow that runs daily at 06:00 UTC:

1. Query PostHog for all accounts at 70%+ of any limit (Step 3 query)
2. Compute consumption velocity and project hit dates (Step 5)
3. Classify into urgency tiers (Step 4)
4. Update Attio records with current threshold data (Step 6)
5. For accounts that moved to imminent, critical, or exceeded, fire a webhook to trigger the `usage-alert-delivery` drill
6. For accounts that upgraded or had their usage drop below 70%, clear the alert tier and log the resolution

Using `n8n-triggers`, add a webhook endpoint so other systems can request an on-demand check for a specific account (useful when a user performs a bulk action that spikes usage).

### 8. Track detection accuracy

Using `posthog-custom-events`, log every detection event:

```javascript
posthog.capture('usage_threshold_detected', {
  account_id: accountId,
  resource_type: 'api_calls',
  urgency_tier: 'imminent',
  pct_consumed: 87,
  plan_tier: 'starter',
  projected_hit_date: '2026-04-05'
});
```

After 30 days, measure: of accounts flagged as critical, what percentage actually hit the limit within 7 days? Target: 70%+ of critical flags should correspond to real limit hits. If the false positive rate exceeds 30%, tighten velocity calculations or add billing cycle awareness.

## Output

- Daily per-account usage threshold detection running in n8n
- Four PostHog cohorts (approaching, imminent, critical, exceeded) updated automatically
- Attio records enriched with threshold proximity data and projected hit dates
- Webhook trigger for downstream alert delivery
- Detection accuracy tracking via PostHog events

## Triggers

Runs daily via n8n cron. On-demand via webhook for individual account checks when bulk actions occur. Re-calibrate plan cap configs whenever pricing tiers change.
