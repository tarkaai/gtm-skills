---
name: ticket-churn-signal-scoring
description: Score accounts for churn risk based on support ticket patterns using LLM analysis
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Score Churn Risk from Support Ticket Patterns

Analyze an account's support ticket history and produce a churn risk score (0-100) with specific signals and recommended intervention.

## Prerequisites
- Normalized ticket data from `intercom-conversations-export` fundamental
- Tags applied via `intercom-ticket-tagging` fundamental
- Account-level aggregation (all tickets for a given company/contact)

## Input: Account Ticket Summary

Before calling the scoring API, aggregate the following per account:

```json
{
  "account_id": "company_123",
  "account_name": "Acme Corp",
  "plan": "pro",
  "mrr": 299,
  "tenure_months": 8,
  "tickets_last_30_days": 7,
  "tickets_last_90_days": 12,
  "avg_monthly_tickets_historical": 2,
  "categories": {"bug": 4, "how-to": 2, "billing": 1},
  "severities": {"critical": 1, "high": 2, "medium": 3, "low": 1},
  "avg_csat_rating": 2.8,
  "repeat_issues": ["csv-export-fails", "slow-dashboard-load"],
  "sentiment_trend": "declining",
  "last_ticket_date": "2025-03-28",
  "escalation_count": 2,
  "competitor_mentions": ["competitor-x"],
  "cancellation_intent_signals": 1
}
```

## API Call

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "You are a churn risk scoring agent. Given an account's support ticket history, produce a churn risk score and recommended action.\n\nAccount data:\n{account_summary_json}\n\nScoring rules:\n- Base score starts at 0\n- Ticket volume: +5 per ticket above their monthly average (last 30 days)\n- Severity: +15 per critical, +8 per high\n- CSAT below 3.0: +15\n- Repeat issues (same problem twice+): +10 per repeat\n- Declining sentiment trend: +10\n- Escalations: +10 per escalation\n- Competitor mentions: +15 per mention\n- Cancellation intent: +25\n- Billing-category tickets: +10\n- Tenure < 3 months with high tickets: +10 (new customer struggling)\n- Cap at 100\n\nRespond in JSON:\n{\n  \"score\": <0-100>,\n  \"risk_level\": \"low|medium|high|critical\",\n  \"top_signals\": [\"signal 1\", \"signal 2\", \"signal 3\"],\n  \"recommended_action\": \"specific action\",\n  \"urgency\": \"immediate|this-week|this-month\",\n  \"talking_points\": [\"point for CS rep to address\"]\n}"
  }]
}
```

## Risk Level Thresholds

- **Low (0-25)**: Normal ticket patterns. No intervention needed. Monitor.
- **Medium (26-50)**: Elevated activity. Add to watch list. Proactive check-in within 2 weeks.
- **High (51-75)**: Clear distress signals. CS outreach within 48 hours. Prepare retention offer.
- **Critical (76-100)**: Imminent churn risk. Immediate escalation to CS lead or founder. Personal call within 24 hours.

## Output

Store the score and signals in your CRM (Attio) as custom attributes on the company record:

```
PUT https://api.attio.com/v2/objects/companies/records/{record_id}
{
  "data": {
    "values": {
      "support_churn_score": [{"value": 72}],
      "support_risk_level": [{"value": "high"}],
      "support_top_signals": [{"value": "3 critical bugs in 30 days, competitor mention, declining CSAT"}],
      "support_recommended_action": [{"value": "CS call within 48h to address recurring export failures"}],
      "support_score_updated_at": [{"value": "2025-03-28T10:00:00Z"}]
    }
  }
}
```

Also fire a PostHog event for trend tracking:

```
POST https://app.posthog.com/capture/
{
  "api_key": "{posthog_project_key}",
  "event": "support_churn_score_calculated",
  "distinct_id": "{account_id}",
  "properties": {
    "score": 72,
    "risk_level": "high",
    "tickets_30d": 7,
    "source": "support-issue-tracking"
  }
}
```

## Cost

- Claude Sonnet per scoring call: ~$0.01-0.02
- At 100 accounts scored weekly: ~$4-8/month
- At 1000 accounts scored weekly: ~$40-80/month
