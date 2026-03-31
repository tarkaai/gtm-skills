---
name: usage-drop-detection
description: Detect per-account engagement drops by comparing recent activity to historical baselines, then classify risk tiers for intervention routing
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-custom-attributes
  - attio-lists
---

# Usage Drop Detection

This drill builds the system that detects when individual accounts or users experience a meaningful decline in product engagement. Unlike broad cohort analysis, this operates at the per-account level — catching the specific users whose activity is fading before they churn.

## Input

- PostHog tracking active with at least 30 days of per-user event data
- A defined "core engagement signal" for your product (logins, key actions, API calls, etc.)
- n8n instance for scheduled detection runs
- Attio CRM for storing risk scores and routing interventions

## Steps

### 1. Define engagement baselines per account

Using the `posthog-custom-events` fundamental, identify the 2-3 events that best represent real engagement (not vanity metrics). Good signals: feature usage, content creation, data exports, collaboration actions. Bad signals: page views, passive logins with no action.

Run a HogQL query to compute each account's personal baseline:

```sql
SELECT
  person_id,
  count() AS events_last_30d,
  count() / 4 AS weekly_avg_30d
FROM events
WHERE event IN ('core_action_completed', 'feature_used', 'data_exported')
  AND timestamp > now() - interval 30 day
GROUP BY person_id
HAVING events_last_30d >= 4
```

Store each account's `weekly_avg_30d` as their personal engagement baseline. This accounts for the fact that a power user doing 50 actions/week and a light user doing 3 actions/week have very different "normal" — a 50% drop means different things for each.

### 2. Build the drop detection query

Using `posthog-anomaly-detection`, compare each account's last-7-day activity against their 30-day weekly average:

```sql
SELECT
  person_id,
  baseline.weekly_avg_30d AS baseline_weekly,
  recent.events_last_7d AS current_weekly,
  (recent.events_last_7d - baseline.weekly_avg_30d) / baseline.weekly_avg_30d * 100 AS pct_change
FROM (
  SELECT person_id, count() AS events_last_7d
  FROM events
  WHERE event IN ('core_action_completed', 'feature_used', 'data_exported')
    AND timestamp > now() - interval 7 day
  GROUP BY person_id
) recent
JOIN (
  SELECT person_id, count() / 4 AS weekly_avg_30d
  FROM events
  WHERE event IN ('core_action_completed', 'feature_used', 'data_exported')
    AND timestamp BETWEEN now() - interval 37 day AND now() - interval 7 day
  GROUP BY person_id
  HAVING weekly_avg_30d >= 1
) baseline ON recent.person_id = baseline.person_id
WHERE pct_change < -30
ORDER BY pct_change ASC
```

This surfaces every account whose recent week dropped 30%+ compared to their personal norm.

### 3. Classify risk tiers

Assign each flagged account to a tier based on drop severity and account value:

- **Watch (pct_change between -30% and -50%):** Early signal. Log it but do not intervene yet. Check again in 7 days.
- **Alert (pct_change between -50% and -80%):** Significant drop. Route to automated intervention (in-app message or email).
- **Critical (pct_change below -80% OR zero activity for 7+ days from a previously active account):** Likely pre-churn. Route to human outreach via Attio task.

Using `posthog-cohorts`, create three dynamic cohorts: `usage-drop-watch`, `usage-drop-alert`, `usage-drop-critical`. These cohorts update automatically as the detection query runs.

### 4. Store risk data in the CRM

Using the `attio-custom-attributes` fundamental, add these fields to the company/contact record in Attio:

- `engagement_risk_tier`: watch | alert | critical | healthy
- `engagement_pct_change`: the numeric drop percentage
- `engagement_baseline_weekly`: their normal weekly activity count
- `engagement_last_checked`: timestamp of last detection run
- `engagement_alert_count`: how many consecutive weeks they have been flagged

Using `attio-lists`, maintain a list called "Engagement Drops — Active" that auto-populates with all alert and critical accounts.

### 5. Build the scheduled detection workflow

Using `n8n-scheduling`, create a workflow that runs daily at 08:00 UTC:

1. Query PostHog for all accounts with 30%+ engagement drops (Step 2 query)
2. Classify into risk tiers (Step 3 logic)
3. Update Attio records with current risk data (Step 4)
4. For accounts that moved from healthy to alert or critical, fire a webhook to trigger the `engagement-alert-routing` drill
5. For accounts that recovered (were flagged, now back to normal), clear the risk tier and log the recovery

Using `n8n-triggers`, add a webhook endpoint so other systems can request an on-demand detection run for a specific account.

### 6. Track detection accuracy

Using `posthog-custom-events`, log every detection event:

```javascript
posthog.capture('usage_drop_detected', {
  person_id: accountId,
  risk_tier: 'alert',
  pct_change: -62,
  baseline_weekly: 24,
  current_weekly: 9
});
```

After 30 days, measure: of accounts flagged as "critical," what percentage actually churned within 60 days? Target: 60%+ of critical flags should correspond to real churn risk (not vacations, seasonal dips, etc.). If false positive rate exceeds 40%, tighten the thresholds or add exclusion rules (e.g., exclude accounts that filed a support ticket saying "on holiday").

## Output

- Daily per-account engagement drop detection running in n8n
- Three PostHog cohorts (watch, alert, critical) updated automatically
- Attio records enriched with risk tier and engagement metrics
- Webhook trigger for downstream intervention routing
- Detection accuracy tracking via PostHog events

## Triggers

Runs daily via n8n cron. On-demand via webhook for individual account checks. Re-calibrate baselines monthly to account for natural usage evolution.
