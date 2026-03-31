---
name: churn-risk-scoring
description: Build a behavioral churn risk model that scores users daily based on usage signals and outputs scored cohorts for intervention routing
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
  - n8n-workflow-basics
  - attio-contacts
  - attio-custom-attributes
---

# Churn Risk Scoring

This drill builds a quantitative churn risk model that scores every active user daily. The model ingests behavioral signals from PostHog, weights them based on historical churn correlation, and outputs a 0-100 risk score per user. Scored users are synced to Attio and PostHog cohorts so downstream systems (intervention emails, in-app messages, sales alerts) can act on them.

This is the detection layer. It answers "who is at risk?" The `churn-prevention` drill answers "what do we do about it?"

## Prerequisites

- PostHog tracking active with at least 30 days of usage data for churned and retained users
- n8n instance for daily scoring workflow
- Attio configured with user/company records
- At least 20 churned users to analyze patterns against (fewer and the model is unreliable)

## Steps

### 1. Identify churn signals from historical data

Using the `posthog-cohorts` fundamental, create two cohorts: "Churned Last 90 Days" and "Retained Last 90 Days." Compare their behavior in the 30 days before churn vs. the same 30-day window for retained users. Query via PostHog API or HogQL:

```sql
SELECT
  person_id,
  countIf(event = 'pageview' AND timestamp > now() - interval 14 day) AS sessions_last_14d,
  countIf(event = 'core_action' AND timestamp > now() - interval 14 day) AS core_actions_last_14d,
  dateDiff('day', max(timestamp), now()) AS days_since_last_activity,
  countIf(event = 'support_ticket_created' AND timestamp > now() - interval 14 day) AS support_tickets_14d,
  countIf(event = 'team_member_removed' AND timestamp > now() - interval 30 day) AS team_removals_30d,
  countIf(event = 'billing_page_viewed' AND timestamp > now() - interval 7 day) AS billing_views_7d
FROM events
WHERE person_id IN (SELECT person_id FROM cohort WHERE name = '{cohort_name}')
GROUP BY person_id
```

Run this for both cohorts. Calculate the median and standard deviation of each signal for churned vs. retained users.

### 2. Define the scoring model

Assign point values to each signal based on how strongly it correlates with churn. Start with these defaults and refine based on your data:

| Signal | Condition | Points |
|--------|-----------|--------|
| Usage decline | Sessions dropped >50% vs. user's 30-day average | +25 |
| Core action absence | Zero core actions in last 7 days (was previously active) | +20 |
| Login gap | No login for 7+ days when user averaged 3+/week | +15 |
| Support spike | 3+ support tickets in 7 days | +10 |
| Team shrinkage | Removed 1+ team members in 30 days | +10 |
| Billing page visit | Visited pricing/cancellation page in last 7 days | +15 |
| Feature abandonment | Stopped using a feature they used 5+ times previously | +10 |
| Export spike | Exported data 3+ times in 7 days (data portability signal) | +10 |

Total possible: well above 100. Cap the score at 100. A user with score 0 shows no churn signals.

### 3. Build the daily scoring workflow

Using the `n8n-triggers` fundamental, create a workflow triggered by daily cron (06:00 UTC):

1. Query PostHog for all active users (at least 1 session in the last 60 days) with their signal metrics from step 1
2. For each user, calculate the composite risk score by summing applicable signal points
3. Classify into tiers:
   - **Low risk (0-25):** Normal behavior. No action needed.
   - **Watch (26-45):** One or two weak signals. Monitor but do not intervene yet.
   - **Medium risk (46-65):** Multiple signals firing. Queue for automated intervention.
   - **High risk (66-85):** Strong churn pattern. Trigger immediate automated intervention.
   - **Critical (86-100):** Imminent churn. Route to human for personal outreach.
4. Using `posthog-custom-events`, emit a `churn_risk_scored` event per user with properties: `risk_score`, `risk_tier`, `top_signals` (array of the signals that fired), `score_date`
5. Using `attio-custom-attributes`, update each user's Attio record with `churn_risk_score`, `churn_risk_tier`, and `churn_risk_signals`
6. Using `attio-contacts`, create a task for the account owner when a user moves to Critical tier

### 4. Create PostHog cohorts per risk tier

Using the `posthog-cohorts` fundamental, create dynamic cohorts that filter on the `churn_risk_tier` property:

- "At-Risk: Medium" — users with `churn_risk_tier = medium`
- "At-Risk: High" — users with `churn_risk_tier = high`
- "At-Risk: Critical" — users with `churn_risk_tier = critical`

These cohorts feed the `churn-prevention` drill's intervention triggers. Intercom and Loops can target these cohorts directly.

### 5. Validate and calibrate the model

Using `posthog-funnels`, measure model accuracy monthly:

- **Precision:** Of users scored high/critical, what percentage actually churned within 30 days?
- **Recall:** Of users who churned, what percentage were scored high/critical before churning?
- **False positive rate:** Users scored high/critical who did not churn. High false positives waste intervention resources and annoy healthy users.

Target: precision > 60%, recall > 70%. If precision is low, raise thresholds. If recall is low, add more signals or lower thresholds. Log calibration results as a PostHog custom event (`churn_model_calibration`) with properties: `precision`, `recall`, `false_positive_rate`, `calibration_date`.

### 6. Track score transitions

Monitor how users move between tiers over time. The most important metric is "Medium/High risk users who returned to Low risk within 14 days" — this is your intervention save rate signal. Build a PostHog funnel:

`churn_risk_scored (tier=high)` -> `churn_risk_scored (tier=low)` within 14 days

This funnel's conversion rate is one of the primary KPIs for the at-risk-intervention play.

## Output

- A daily n8n workflow that scores every active user and syncs scores to PostHog + Attio
- Dynamic PostHog cohorts for each risk tier
- Attio records updated with risk scores for team visibility
- A model calibration process that runs monthly
- Score transition tracking that measures intervention effectiveness
