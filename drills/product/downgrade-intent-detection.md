---
name: downgrade-intent-detection
description: Detect behavioral signals indicating a user is considering downgrading their plan, score intent severity, and route to intervention workflows
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-funnels
  - n8n-triggers
  - n8n-scheduling
  - attio-contacts
  - attio-custom-attributes
---

# Downgrade Intent Detection

This drill builds a system that identifies users exhibiting pre-downgrade behavior before they actually click the downgrade button. It scores intent severity and routes users to the appropriate intervention. This is the detection layer for the downgrade-prevention play -- it answers "who is about to downgrade?" so the intercept flow can answer "how do we stop them?"

## Prerequisites

- PostHog tracking active with at least 30 days of user event data
- Billing/subscription events instrumented (plan changes, billing page views, cancellation page views)
- n8n instance for scheduled detection
- Attio CRM with user/company records
- At least 10 historical downgrade events to analyze patterns against

## Steps

### 1. Analyze historical downgrade signals

Using the `posthog-cohorts` fundamental, create two cohorts: "Downgraded Last 90 Days" and "Stayed on Plan Last 90 Days" (users on paid plans who did not downgrade). Compare their behavior in the 14 days before downgrade. Query via PostHog API or HogQL:

```sql
SELECT
  person_id,
  countIf(event = 'billing_page_viewed' AND timestamp > now() - interval 14 day) AS billing_views_14d,
  countIf(event = 'pricing_page_viewed' AND timestamp > now() - interval 14 day) AS pricing_views_14d,
  countIf(event = 'plan_comparison_viewed' AND timestamp > now() - interval 14 day) AS plan_compare_14d,
  countIf(event = 'downgrade_page_viewed' AND timestamp > now() - interval 14 day) AS downgrade_views_14d,
  countIf(event = 'premium_feature_used' AND timestamp > now() - interval 14 day) AS premium_usage_14d,
  countIf(event = 'premium_feature_used' AND timestamp BETWEEN now() - interval 44 day AND now() - interval 14 day) / 4 AS premium_usage_baseline_weekly,
  countIf(event = 'support_ticket_created' AND timestamp > now() - interval 14 day) AS support_tickets_14d,
  countIf(event = 'export_data' AND timestamp > now() - interval 7 day) AS data_exports_7d,
  dateDiff('day', max(timestamp), now()) AS days_since_last_activity
FROM events
WHERE person_id IN (SELECT person_id FROM cohort WHERE name = '{cohort_name}')
GROUP BY person_id
```

Run this for both cohorts. Identify which signals are statistically different between downgraders and retainers.

### 2. Define the downgrade intent scoring model

Assign points based on how strongly each signal correlates with actual downgrade behavior. Start with these defaults and calibrate from your data:

| Signal | Condition | Points |
|--------|-----------|--------|
| Downgrade page view | Visited downgrade/cancellation page in last 7 days | +30 |
| Pricing comparison | Viewed plan comparison 2+ times in 7 days | +20 |
| Billing page visits | Visited billing page 3+ times in 14 days (not just once for routine check) | +15 |
| Premium feature decline | Usage of premium-tier features dropped 50%+ vs. their 30-day average | +25 |
| Premium feature zero | Zero premium feature usage in last 14 days despite having access | +20 |
| Support frustration | 2+ support tickets in 7 days mentioning billing, pricing, or value | +15 |
| Data export spike | 3+ data exports in 7 days (portability signal) | +10 |
| Team shrinkage | Removed seats or team members in last 14 days | +15 |
| Usage decline | Overall activity dropped 40%+ vs. 30-day average | +10 |

Total possible: well above 100. Cap at 100. Score 0 means no downgrade signals detected.

### 3. Build the daily detection workflow

Using the `n8n-scheduling` fundamental, create a workflow triggered by daily cron at 07:00 UTC:

1. Query PostHog for all users on paid plans (not free tier) with their signal metrics from step 1
2. For each user, compute the composite downgrade intent score
3. Classify into tiers:
   - **None (0-15):** No downgrade signals. No action.
   - **Watch (16-35):** Weak signals. Log, check again in 7 days.
   - **Moderate (36-60):** Multiple signals firing. Queue for soft intervention (feature education email, in-app usage tips).
   - **High (61-85):** Strong downgrade pattern. Trigger intercept flow with personalized offer.
   - **Imminent (86-100):** User is likely about to downgrade within days. Trigger high-touch intervention (personal outreach or premium retention offer).
4. Using `posthog-custom-events`, emit a `downgrade_intent_scored` event per user:
   ```javascript
   posthog.capture('downgrade_intent_scored', {
     risk_score: 72,
     risk_tier: 'high',
     top_signals: ['premium_feature_decline', 'pricing_comparison', 'billing_page_visits'],
     current_plan: 'pro',
     monthly_revenue: 99,
     score_date: '2025-03-15'
   });
   ```
5. Using `attio-custom-attributes`, update each user's Attio record with `downgrade_intent_score`, `downgrade_intent_tier`, `downgrade_intent_signals`, and `downgrade_intent_last_scored`
6. Using `attio-contacts`, create a task for the account owner when a user moves to Imminent tier

### 4. Create PostHog cohorts per intent tier

Using the `posthog-cohorts` fundamental, create dynamic cohorts:

- "Downgrade Intent: Moderate" -- `downgrade_intent_tier = moderate`
- "Downgrade Intent: High" -- `downgrade_intent_tier = high`
- "Downgrade Intent: Imminent" -- `downgrade_intent_tier = imminent`

These cohorts feed the `downgrade-intercept-flow` drill's intervention triggers. Intercom and Loops can target these cohorts directly.

### 5. Add real-time trigger for downgrade page visits

In addition to the daily batch scoring, set up a real-time trigger using `n8n-triggers`. When PostHog fires a `downgrade_page_viewed` event:

1. Immediately score that user (even if the daily batch hasn't run yet)
2. If they are already moderate+ intent, escalate to high and trigger the intercept flow immediately
3. If they were previously unscored, run the full scoring model on-demand

This ensures you intercept users in the moment they are actively exploring a downgrade, not 24 hours later.

### 6. Validate and calibrate monthly

Using `posthog-funnels`, measure detection accuracy:

- **Precision:** Of users scored high/imminent, what percentage actually downgraded within 30 days?
- **Recall:** Of users who downgraded, what percentage were scored high/imminent before downgrading?
- **False positive rate:** High/imminent users who did not downgrade (these users received unnecessary interventions)

Target: precision >50%, recall >70%. Log calibration results as `downgrade_model_calibration` events in PostHog.

## Output

- A daily n8n workflow scoring every paid user for downgrade intent
- A real-time webhook trigger for downgrade page visits
- Dynamic PostHog cohorts for each intent tier
- Attio records enriched with downgrade intent scores
- Monthly calibration process with precision/recall tracking

## Triggers

- Daily batch: cron at 07:00 UTC
- Real-time: webhook on `downgrade_page_viewed` events
- Monthly calibration: first Monday of each month
