---
name: health-score-model-design
description: Design a composite account health score from usage, engagement, support, and adoption dimensions
category: Product
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-retention-analysis
  - posthog-custom-events
  - posthog-cohorts
  - attio-custom-attributes
  - attio-health-score-sync
  - n8n-workflow-basics
---

# Health Score Model Design

This drill builds a composite account health score that combines multiple signal dimensions into a single 0-100 score per account. The score predicts churn risk and expansion opportunity by weighting usage frequency, feature adoption breadth, engagement depth, and support sentiment.

## Prerequisites

- PostHog tracking active with at least 30 days of account-level usage data
- PostHog Group Analytics enabled with `company_id` passed in events
- Attio workspace with Company records matching your customer accounts
- n8n instance for running the scoring pipeline
- At least 20 active customer accounts to calibrate the model

## Steps

### 1. Define the four scoring dimensions

Each dimension contributes to the composite score. Define the signals that feed each dimension:

**Usage dimension (weight: 35%)**
- Weekly active users per account (from `posthog-retention-analysis` per-user activity query)
- Session frequency: average sessions per user per week
- Usage trend: is the account's event volume growing, stable, or declining over the last 4 weeks?
- Login gap: days since any user from the account last logged in

**Engagement dimension (weight: 25%)**
- Feature breadth: number of distinct feature events fired in the last 30 days divided by total available features
- Depth of use: average events per session (shallow browsing vs deep workflows)
- Collaboration signals: number of distinct users from the account active in the last 14 days
- Content consumption: help docs viewed, API docs accessed, changelog visited

**Support dimension (weight: 20%)**
- Ticket volume: support tickets filed in the last 30 days (lower is healthier unless they are feature requests)
- Ticket sentiment: ratio of bug reports and complaints vs feature requests and questions
- Resolution satisfaction: average CSAT from resolved tickets
- Escalation rate: percentage of tickets that required escalation

**Adoption dimension (weight: 20%)**
- Core feature adoption: has the account used each of your 3-5 core features at least once in the last 30 days?
- Integration status: has the account connected at least one integration?
- Team penetration: percentage of invited users who are active
- Milestone completion: has the account reached key value milestones (first report generated, first export, first automation created)?

### 2. Build dimension scoring functions

For each dimension, normalize signals to a 0-100 scale. Use percentile ranking against your customer base rather than absolute thresholds, so the score adapts as your product and customer base evolve.

Using `posthog-cohorts`, define the scoring cohort (all active customers with 30+ days of history). Exclude free/trial accounts unless you want to score them separately.

**Usage dimension scoring:**

Query PostHog using `posthog-retention-analysis`:

```
For each account:
  weekly_active_users = query active users from last 4 weeks
  session_frequency = total sessions / total users / 4 weeks
  usage_trend = (events_last_2w - events_prev_2w) / events_prev_2w
  login_gap_days = days since last event from any user

  usage_raw = (
    percentile_rank(weekly_active_users) * 0.30 +
    percentile_rank(session_frequency) * 0.25 +
    normalize_trend(usage_trend) * 0.25 +    # declining=-1, stable=0, growing=+1 → map to 0-100
    inverse_percentile_rank(login_gap_days) * 0.20  # lower gap = higher score
  ) * 100
```

Apply the same pattern for each dimension, pulling the relevant signals from PostHog and normalizing.

### 3. Compute the composite score

```
health_score = (
  usage_score * 0.35 +
  engagement_score * 0.25 +
  support_score * 0.20 +
  adoption_score * 0.20
)
```

Round to integer. Range: 0-100.

### 4. Classify risk level

Map the composite score to risk tiers:

| Score Range | Risk Level | Color | Action |
|------------|------------|-------|--------|
| 80-100 | Healthy | Green | Monitor only. Look for expansion signals. |
| 60-79 | Monitor | Yellow | Watch weekly. Address any declining dimension. |
| 40-59 | At Risk | Orange | Proactive outreach within 48 hours. |
| 0-39 | Critical | Red | Immediate intervention. Personal outreach from account owner. |

### 5. Compute score trend

Compare the current score to the score from 2 weeks ago:

- **Improving:** Score increased by 5+ points
- **Stable:** Score changed by less than 5 points
- **Declining:** Score decreased by 5+ points

A "Declining" trend on a "Monitor" account is more urgent than a stable "At Risk" account. The trend signals trajectory, not just current state.

### 6. Build the scoring pipeline in n8n

Using `n8n-workflow-basics`, create a daily workflow:

1. **Trigger:** Cron at 06:00 UTC daily
2. **Pull account list:** Query Attio for all active customer company records
3. **Pull usage data:** For each account, query PostHog using the HogQL queries from step 2
4. **Compute scores:** Calculate each dimension score and the composite score
5. **Classify:** Apply risk level and trend classification
6. **Write to CRM:** Use `attio-health-score-sync` to write scores, risk levels, and trends to Attio
7. **Detect changes:** Compare today's scores to yesterday's. Flag accounts that changed risk level.
8. **Log:** Create an Attio note on any account that changed risk level, explaining which dimension changed and why

### 7. Validate the model against known outcomes

Before trusting the model, back-test it:

1. Pull a list of accounts that churned in the last 90 days from Attio
2. Retroactively compute what their health scores would have been 30 days before churn
3. If the model would have classified >70% of them as "At Risk" or "Critical" 30 days before churn, the model has predictive value
4. If not, adjust dimension weights or add new signals until back-testing accuracy exceeds 70%

Using `posthog-custom-events`, log each health score computation as a PostHog event:
```
posthog.capture('health_score_computed', {
  company_id: account.id,
  health_score: 72,
  risk_level: 'Monitor',
  usage_score: 85,
  engagement_score: 60,
  support_score: 90,
  adoption_score: 55,
  trend: 'Declining'
})
```

This creates a time series of health scores in PostHog for trend analysis and model evaluation.

## Output

- A documented health score model with 4 dimensions, weights, and scoring functions
- A daily n8n workflow that computes scores for all accounts
- Health scores, risk levels, and trends synced to Attio company records
- PostHog events logging every score computation for model evaluation
- Back-test results showing the model's predictive accuracy against historical churn

## Triggers

- Daily scoring pipeline: cron, 06:00 UTC
- Model recalibration: monthly (adjust weights based on churn prediction accuracy)
