---
name: objection-response-generation
description: Use Claude to generate tailored price objection responses based on objection root cause, deal context, and winning framework patterns
tool: Anthropic
difficulty: Advanced
---

# Generate Price Objection Responses

Given a classified price objection, deal context, and historical win patterns, use the Claude API to generate a tailored response using the highest-success framework for this objection type.

## Prerequisites

- Classified objection data (from `call-transcript-objection-extraction`)
- Deal record from Attio with pain data and deal value
- Anthropic API key
- Historical response effectiveness data (optional, improves quality over time)

## API Call

```
POST https://api.anthropic.com/v1/messages
Authorization: x-api-key {ANTHROPIC_API_KEY}
Content-Type: application/json
```

**Request body:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2500,
  "messages": [{
    "role": "user",
    "content": "Generate a price objection response for a sales conversation.\n\nObjection details:\n- Prospect quote: \"{objection_quote}\"\n- Root cause: {root_cause}\n- Emotional tone: {emotional_tone}\n- Severity: {severity}/10\n- Stated budget: {stated_budget or 'not disclosed'}\n- Comparison anchor: {comparison_anchor or 'none'}\n\nDeal context:\n- Company: {company_name}\n- Deal value: ${deal_value}/year\n- Total quantified pain: ${total_quantified_pain}/year\n- Pain-to-price ratio: {ratio}x\n- Champion: {champion_name}, {champion_title}\n- Decision maker: {decision_maker_name}, {decision_maker_title}\n- Strongest pain: \"{strongest_pain_summary}\"\n- Key pain quote: \"{key_pain_quote}\"\n\nHistorical effectiveness (if available):\n{framework_effectiveness_json}\n\nGenerate the response using the most effective framework for this root cause. Return this exact JSON:\n{\n  \"framework_used\": \"value_reframe|roi_proof|payment_flexibility|competitive_tcm|anchor_to_pain|silence\",\n  \"verbal_response\": \"The exact words to say on a call (2-4 sentences max)\",\n  \"diagnostic_questions\": [\"2-3 follow-up questions to deepen understanding\"],\n  \"follow_up_email\": {\n    \"subject\": \"Email subject line\",\n    \"body\": \"Follow-up email body (under 150 words) reinforcing the verbal response with supporting data\"\n  },\n  \"supporting_asset\": {\n    \"type\": \"roi_calculator|case_study|tco_comparison|payment_options|business_case\",\n    \"description\": \"What to attach and why\"\n  },\n  \"escalation_path\": \"What to do if this response doesn't resolve the objection\",\n  \"expected_next_step\": \"The specific action to propose after delivering this response\"\n}"
  }]
}
```

## Input Requirements

- `objection_quote`: The prospect's exact words (from objection extraction)
- `root_cause`: One of: `no_budget`, `value_gap`, `competitor_comparison`, `sticker_shock`, `authority_gap`, `timing`
- `total_quantified_pain`: From pain discovery data in Attio
- `framework_effectiveness_json`: Optional. Historical win rates per framework per root cause, pulled from PostHog aggregate data

## Framework Selection Logic

When historical data is not available, use these default framework mappings:

| Root Cause | Primary Framework | Why |
|-----------|------------------|-----|
| no_budget | payment_flexibility | Restructure payment to fit budget cycles |
| value_gap | roi_proof | Prove the math works — pain costs more than solution |
| competitor_comparison | competitive_tcm | Total cost of ownership comparison including hidden costs |
| sticker_shock | anchor_to_pain | Re-anchor from absolute price to cost of the problem |
| authority_gap | value_reframe | Arm the champion with language for the decision maker |
| timing | silence | Let the prospect talk — timing objections often mask deeper concerns |

When historical data IS available, override defaults with the highest win-rate framework for that root cause, provided sample size >= 10.

## Output

JSON response object containing:
- Verbal response for live conversation
- Diagnostic questions to deepen understanding
- Follow-up email with supporting data
- Supporting asset recommendation
- Escalation path if initial response fails
- Expected next step to propose

Store in Attio as a note on the deal record. Log in PostHog as `objection_response_generated` event.

## Guardrails

- Never generate responses that offer discounts as the first move — always lead with value
- Never promise features or timelines not confirmed by the product team
- If `pain_to_price_ratio < 3`, flag for the seller: the value story is weak — consider re-running discovery before responding to the price objection
- If `emotional_tone` is "firm" and `severity >= 8`, recommend a human-led response rather than templated — these need judgment
- Rate limit: max 5 response generations per deal per day (avoid spamming the same prospect with multiple angles)

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for nuanced responses |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gong Assist | Built-in AI | Real-time coaching during calls |
| Clari | Deal intelligence | Predictive risk scoring but less response generation |
| Manual | Framework reference sheet | Fallback for enterprise deals |
