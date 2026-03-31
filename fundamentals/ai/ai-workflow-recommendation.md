---
name: ai-workflow-recommendation
description: Use Claude API to generate personalized workflow optimization suggestions from user behavior data
tool: Anthropic
difficulty: Advanced
---

# Generate Workflow Optimization Suggestions

Given a user's behavioral data (event sequences, feature usage patterns, time-on-task metrics), use the Claude API to generate specific, actionable workflow improvement suggestions tailored to that user's actual usage.

## API Call

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "You are a workflow optimization agent for a SaaS product. Analyze this user's behavior data and generate improvement suggestions.\n\nProduct context:\n{product_description}\n\nAvailable features the user has NOT discovered:\n{undiscovered_features_json}\n\nUser behavior data (last 30 days):\n- Event sequence (most recent 50 actions): {event_sequence_json}\n- Feature usage frequency: {feature_usage_json}\n- Average time per workflow completion: {workflow_times_json}\n- Repeated action patterns (same 3+ step sequence done 5+ times): {repeated_patterns_json}\n- Errors or retries: {error_events_json}\n\nPower user benchmark (top 10% users):\n- Their most-used features: {power_user_features_json}\n- Their average workflow time: {power_user_times_json}\n- Features they use that this user does not: {feature_gap_json}\n\nGenerate exactly 3 ranked suggestions. For each:\n1. What to change (specific action: 'Use keyboard shortcut Cmd+K instead of clicking Menu > Search', not 'try using shortcuts')\n2. Why this helps (quantified: 'saves ~15 seconds per search, you search 20x/day = 5 min/day saved')\n3. How to do it (step-by-step, 3 steps max)\n4. Confidence (high/medium/low based on data strength)\n5. Category (efficiency, discovery, automation, collaboration)\n\nRespond in JSON: {\"suggestions\": [{\"action\": \"\", \"benefit\": \"\", \"steps\": [\"\"], \"confidence\": \"\", \"category\": \"\"}]}"
  }]
}
```

## Input Requirements

- `product_description`: Brief description of the product and its core workflows
- `undiscovered_features_json`: Features available but not yet used by this user (from PostHog feature tracking)
- `event_sequence_json`: Last 50 user actions from PostHog (use `posthog-user-path-analysis`)
- `feature_usage_json`: Feature usage counts from PostHog custom events
- `workflow_times_json`: Time between workflow start and completion events
- `repeated_patterns_json`: Repeated action sequences detected from path analysis
- `error_events_json`: Error events, retries, or undo actions from PostHog
- `power_user_features_json`: Aggregate feature usage from the Power Users cohort (use `posthog-cohorts`)
- `power_user_times_json`: Benchmark workflow times from the Power Users cohort
- `feature_gap_json`: Features used by power users but not by this user

## Output

JSON with 3 ranked suggestions. Each suggestion must be:
- **Specific**: references actual features and UI elements by name
- **Quantified**: includes estimated time or effort savings based on the user's actual usage frequency
- **Actionable**: the user can implement the suggestion in under 2 minutes

Store generated suggestions in PostHog as a person property `last_workflow_suggestions` (JSON string) and in Attio as a note on the contact record.

## Guardrails

- Never suggest features the user's plan does not include — check plan-level feature access first
- Never suggest more than 3 suggestions at once (cognitive overload reduces adoption)
- Rate limit: max 1 suggestion generation per user per week (prevent notification fatigue)
- If the user has fewer than 20 actions in the last 30 days, return `insufficient_data` — not enough behavior to analyze
- If the user is already in the top 20% by efficiency metrics, return `already_optimized` with a single "advanced tip" instead of 3 suggestions
- Cache suggestions: do not regenerate if the user's behavior pattern has not changed significantly (>20% shift in feature usage distribution)

## Cost Estimate

At ~1,500 tokens output per user per week using Claude Sonnet 4.6:
- 100 users/week: ~$0.50/week ($2/month)
- 1,000 users/week: ~$5/week ($20/month)
- 10,000 users/week: ~$50/week ($200/month)

Use prompt caching for the system prompt and product context (90% savings on input tokens).
