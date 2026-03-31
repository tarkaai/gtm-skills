---
name: contract-comparison-generation
description: Generate a buyer-facing comparison document showing annual vs multi-year contract options with total cost, savings, and risk analysis
tool: Anthropic
difficulty: Config
---

# Contract Comparison Generation

Generate a prospect-facing comparison document that lays out annual vs multi-year contract options side-by-side. The document emphasizes total cost of ownership, savings, rate-lock protection, and risk mitigation. Written from the buyer's perspective so the champion can use it internally for budget approval.

## Prerequisites

- Deal term options from `deal-term-modeling` fundamental
- Prospect company data from Attio
- Anthropic API key

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
    "content": "Generate a buyer-facing contract comparison document. This will be shared with the prospect's champion to circulate internally. Write it from the buyer's perspective — NOT as a vendor sales pitch.\n\nCompany: {company_name}\nContact: {champion_name}, {champion_title}\nCurrent plan: {current_plan} at ${current_monthly}/mo (${current_annual}/yr)\n\nOptions to compare:\n{options_json}\n\nReturn this JSON:\n{\n  \"title\": \"Contract Options for [Company]\",\n  \"intro\": \"2-3 sentences framing the decision from the buyer's perspective\",\n  \"comparison_table\": {\n    \"columns\": [\"Monthly (current)\", \"Annual\", \"2-Year\", \"3-Year\"],\n    \"rows\": [\n      {\"label\": \"Monthly cost\", \"values\": [\"$X\", \"$X\", \"$X\", \"$X\"]},\n      {\"label\": \"Annual cost\", \"values\": [\"$X\", \"$X\", \"$X\", \"$X\"]},\n      {\"label\": \"Total cost over 3 years\", \"values\": [\"$X\", \"$X\", \"$X\", \"$X\"]},\n      {\"label\": \"Savings vs monthly\", \"values\": [\"-\", \"$X (Y%)\", \"$X (Y%)\", \"$X (Y%)\"]},\n      {\"label\": \"Rate lock\", \"values\": [\"No\", \"No\", \"Yes\", \"Yes\"]},\n      {\"label\": \"Included perks\", \"values\": [\"Standard\", \"Standard\", \"...\", \"...\"]}\n    ]\n  },\n  \"risk_analysis\": {\n    \"rate_increase_risk\": \"What happens if prices go up: monthly/annual customers pay more, committed customers are protected\",\n    \"flexibility_tradeoff\": \"Honest assessment of the commitment tradeoff — what you give up vs what you gain\",\n    \"switching_cost\": \"Cost of switching providers mid-term vs end-of-term\"\n  },\n  \"recommendation\": \"1-2 sentences recommending the best option for THIS buyer's situation, with reasoning\",\n  \"next_step\": \"Clear action the buyer should take\"\n}"
  }]
}
```

## Response Validation

- All dollar amounts are internally consistent
- Savings percentages match the actual math
- Risk analysis is honest (not one-sided sales copy)
- Recommendation matches the deal context (don't recommend 3-year to a company that just raised and may pivot)

## Error Handling

- **Only one option provided:** Generate a simplified annual vs multi-year comparison
- **Prospect in active competitive evaluation:** Add a row for "competitive protection" showing rate-lock advantage

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best for buyer-perspective tone |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Qwilr | Interactive Proposals | Visual comparison pages |
| PandaDoc | Document + E-Sign | Comparison doc with built-in signing |
| Proposify | Proposal API | Template-based comparisons |
