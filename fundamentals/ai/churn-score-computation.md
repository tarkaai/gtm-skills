---
name: churn-score-computation
description: Use Claude to compute weighted churn risk scores from behavioral signals and usage patterns
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Compute Churn Risk Scores

Given a user's behavioral signals extracted from PostHog, use Claude to compute a weighted churn risk score (0-100) with explainability. This replaces traditional ML model training with an LLM-based scoring approach that requires no training data or model infrastructure.

## API Call

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "You are a churn prediction agent. Score this user's churn risk from 0 (no risk) to 100 (will churn imminently).\n\nProduct context:\n- Product type: {product_type}\n- Healthy usage pattern: {healthy_usage_description}\n- Average session frequency for retained users: {avg_sessions_per_week}\n- Core features: {core_feature_list}\n\nUser signals:\n- Activity last 7 days: {events_last_7d} events\n- Activity previous 7 days: {events_prev_7d} events\n- Activity decay rate (week-over-week): {decay_rate}\n- Days since last event: {days_since_last}\n- Abandoned features (previously used, now stopped): {abandoned_features}\n- Distinct event types in last 30 days: {distinct_events_30d}\n- Support tickets last 14 days: {support_tickets}\n- Billing/cancellation page views: {billing_page_views}\n- Account age (days): {account_age}\n- Team size change: {team_size_delta}\n\nScore this user and explain your reasoning. Respond in JSON:\n{\n  \"risk_score\": 0-100,\n  \"risk_tier\": \"low|medium|high|critical\",\n  \"primary_signal\": \"the single strongest churn indicator\",\n  \"contributing_signals\": [\"signal1\", \"signal2\"],\n  \"recommended_intervention\": \"specific action to take\",\n  \"confidence\": 0.0-1.0,\n  \"reasoning\": \"2-3 sentence explanation\"\n}"
  }]
}
```

## Scoring Tiers

- **0-25 (Low):** User is healthy. No intervention needed.
- **26-50 (Medium):** Early warning signs. Light-touch intervention (in-app message, feature highlight).
- **51-75 (High):** Multiple churn signals active. Triggered email with personalized re-engagement.
- **76-100 (Critical):** Imminent churn risk. Personal outreach from team member required.

## Batch Scoring

For scoring multiple users, batch them into a single API call (up to 20 users per request to stay within token limits):

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Score these {n} users for churn risk. Product context: {context}\n\nUsers:\n{users_json}\n\nRespond with a JSON array of scores, one per user."
  }]
}
```

## Calibration

After running for 2+ weeks, compare predicted risk scores against actual churn outcomes. Adjust the system prompt with calibration notes:

- "Users scoring 60+ churned 80% of the time -> scoring is well-calibrated above 60"
- "Users scoring 30-40 churned 45% of the time -> mid-range scores are under-predicting risk, weight activity decay more heavily"

Add calibration notes to the system prompt to improve accuracy over time without retraining a model.

## Output

Store the score in your CRM (Attio custom attribute `churn_risk_score`) and PostHog (user property `churn_risk_score`). This enables cohort analysis of at-risk users and targeted interventions.

## Error Handling

- If user data is incomplete (fewer than 3 signals available), return `confidence: 0.3` and flag for manual review
- If the API returns a non-JSON response, retry once with temperature 0
- Rate limit: score no more than 500 users per day to manage API costs
- Cost estimate: ~$0.01-0.03 per user scored with Sonnet
