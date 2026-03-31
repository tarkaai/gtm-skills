---
name: churn-signal-extraction
description: Extract behavioral churn signals from PostHog usage data and compute weighted risk scores for each user
category: Product
tools:
  - PostHog
  - Anthropic
  - Attio
fundamentals:
  - posthog-retention-analysis
  - posthog-cohorts
  - posthog-custom-events
  - churn-score-computation
  - attio-custom-attributes
  - attio-contacts
---

# Churn Signal Extraction

This drill builds the data pipeline that turns raw product usage data into per-user churn risk scores. It extracts behavioral signals from PostHog, feeds them through an LLM-based scoring model, and writes the results back to your CRM and analytics for downstream action.

## Input

- PostHog project with at least 30 days of tracked user events
- List of core product features (event names that indicate healthy usage)
- Definition of what "healthy usage" looks like for your product (sessions per week, features used, etc.)
- Anthropic API key for Claude (scoring computation)
- Attio workspace with a `churn_risk_score` custom attribute on person records

## Steps

### 1. Define your churn signal taxonomy

Before extracting data, define which signals indicate churn risk for your specific product. Using `posthog-cohorts`, analyze users who churned in the last 90 days vs. users who retained. Compare their behavior in the 30 days before churn:

Typical signals to extract:
- **Activity decay rate:** Week-over-week change in event count. Declining activity is the strongest single predictor.
- **Feature abandonment:** Core features the user previously used regularly but stopped using entirely.
- **Login gap:** Days since last meaningful event (exclude passive events like page loads).
- **Engagement breadth narrowing:** Number of distinct event types in last 30 days dropping below their personal average.
- **Support escalation:** Spike in support tickets or help article views (frustration signal).
- **Billing page visits:** Views of pricing, downgrade, or cancellation pages.
- **Team shrinkage:** Removal of team members from the account.

Use `posthog-custom-events` to ensure all these signals are being tracked. If any are missing, instrument them before proceeding.

### 2. Build the extraction query

Using `posthog-retention-analysis`, run the per-user activity decay query and feature abandonment query. Combine the results into a signal vector per user:

```json
{
  "user_id": "usr_abc123",
  "events_last_7d": 3,
  "events_prev_7d": 15,
  "decay_rate": -0.80,
  "days_since_last_event": 4,
  "abandoned_features": ["reports", "integrations"],
  "distinct_event_types_30d": 3,
  "support_tickets_14d": 2,
  "billing_page_views": 1,
  "team_size_delta": -2,
  "account_age_days": 120
}
```

### 3. Score each user

Pass each user's signal vector to the `churn-score-computation` fundamental. Use batch scoring (20 users per API call) for efficiency. The LLM returns a risk score (0-100), risk tier, primary signal, and recommended intervention for each user.

### 4. Write scores back to your stack

Using `attio-custom-attributes`, write the `churn_risk_score` and `churn_risk_tier` to each person's record in Attio. Using `posthog-custom-events`, fire a `churn_risk_scored` event for each user with properties: `risk_score`, `risk_tier`, `primary_signal`. This enables PostHog cohort creation for at-risk users.

### 5. Create at-risk cohorts in PostHog

Using `posthog-cohorts`, create dynamic cohorts:
- **Critical risk (76-100):** Immediate intervention needed
- **High risk (51-75):** Triggered email intervention
- **Medium risk (26-50):** Light-touch in-app nudge
- **Low risk (0-25):** Healthy, no action

These cohorts feed into the `churn-intervention-routing` drill.

## Output

- Per-user churn risk scores stored in Attio and PostHog
- Dynamic at-risk cohorts in PostHog segmented by risk tier
- Signal vectors logged for model calibration
- List of users per risk tier for downstream intervention

## Triggers

- **Smoke:** Run once manually to validate signal extraction and scoring accuracy
- **Baseline:** Run daily via n8n cron to maintain current risk scores
- **Scalable/Durable:** Run daily, with weekly calibration passes comparing predicted scores to actual outcomes
