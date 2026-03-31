---
name: experiment-evaluation
description: Use Claude to evaluate A/B test results and decide whether to adopt, iterate, or revert
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Evaluate Experiment Results

After an A/B test runs for a sufficient period, use Claude to analyze results and make a statistically-informed decision: adopt the variant, iterate further, or revert to the control.

## API Call

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "Evaluate this A/B test for a GTM play.\n\nPlay: {play_title}\nHypothesis: {hypothesis_description}\nTest duration: {days} days\nMinimum sample per variant: {min_sample}\n\nControl (A):\n- Sample: {control_n}\n- Primary metric: {control_value}\n- Secondary metrics: {control_secondary_json}\n\nVariant (B):\n- Sample: {variant_n}\n- Primary metric: {variant_value}\n- Secondary metrics: {variant_secondary_json}\n\nDecide:\n1. Is the sample size sufficient for statistical significance? (need >=100 per variant for most GTM metrics, or use Bayesian estimation for smaller samples)\n2. Is the difference meaningful? (>=10% relative improvement on primary metric)\n3. Are secondary metrics stable? (no secondary metric degraded >5%)\n\nRespond in JSON: {\"decision\": \"adopt|iterate|revert|extend\", \"confidence\": 0.0-1.0, \"reasoning\": \"\", \"primary_lift\": \"\", \"secondary_impact\": \"\", \"next_action\": \"\"}"
  }]
}
```

## Decision Criteria

- **Adopt:** Primary metric improved >=10%, no secondary metric degraded >5%, confidence >= 0.9
- **Iterate:** Primary metric improved but <10%, or confidence 0.7-0.9 — run another experiment building on this one
- **Revert:** Primary metric worsened or secondary metrics degraded significantly — go back to control
- **Extend:** Insufficient sample size — keep running for another test period

## Output

JSON decision object. Store in Attio as a note on the experiment record. If "adopt," trigger the `n8n-workflow-basics` fundamental to update the live configuration.

## Guardrails

- Never auto-adopt changes with confidence < 0.85 — flag for human review
- Never evaluate before minimum test duration (7 days for most GTM plays)
- Log every decision with full reasoning for audit trail
