---
name: hypothesis-generation
description: Use Claude to generate ranked improvement hypotheses from metric data and play context
tool: Anthropic
difficulty: Advanced
---

# Generate Improvement Hypotheses

Given a play's current metrics, historical trends, and context, use the Claude API to generate ranked hypotheses for what to change to improve performance.

## API Call

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "You are an optimization agent for a GTM play. Analyze this data and generate improvement hypotheses.\n\nPlay: {play_title}\nLevel: Durable\nMotion: {motion}\n\nCurrent metrics (last 2 weeks):\n{metrics_json}\n\nHistorical trend (8 weeks):\n{trend_json}\n\nAnomaly detected: {anomaly_type} — {anomaly_description}\n\nCurrent configuration:\n{current_config_json}\n\nGenerate exactly 3 ranked hypotheses. For each:\n1. What to change (specific, actionable — e.g., 'change email subject line from X to Y', not 'improve messaging')\n2. Why this might work (based on the data)\n3. Expected impact (quantified estimate)\n4. Risk level (low/medium/high — high means it could make things worse)\n5. How to test it (specific A/B test or experiment design)\n\nRespond in JSON: {\"hypotheses\": [{\"change\": \"\", \"rationale\": \"\", \"expected_impact\": \"\", \"risk\": \"\", \"test_design\": \"\"}]}"
  }]
}
```

## Input Requirements

- `metrics_json`: Current KPIs from PostHog (use `posthog-custom-events` fundamental)
- `trend_json`: 8-week trend data (use `posthog-anomaly-detection` fundamental)
- `anomaly_type`: Output from anomaly detection (drop/plateau/spike/normal)
- `current_config_json`: Current play parameters (email copy, targeting, cadence, etc. from CRM/automation)

## Output

JSON with 3 ranked hypotheses. Store in Attio as a note on the play's campaign record. Each hypothesis becomes a candidate for the next optimization experiment.

## Guardrails

- Never generate hypotheses that require budget increases > 20% without human approval
- Never suggest changes to more than 1 variable at a time (isolate for clean testing)
- If risk is "high" on the top hypothesis, flag for human review before proceeding
- Rate limit: max 1 hypothesis generation per play per week
