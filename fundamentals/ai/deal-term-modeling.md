---
name: deal-term-modeling
description: Generate multi-year deal structures with discount tiers, payment terms, and incentive packages tailored to a specific prospect's profile
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Deal Term Modeling

Given a prospect's deal context (ACV, pain-to-price ratio, competitive landscape, budget cycle), generate a set of multi-year deal structures the seller can present. Each structure includes term length, discount level, payment schedule, rate-lock provisions, and incentive add-ons. The output is a ranked set of options optimized for total contract value (TCV) while remaining attractive to the buyer.

## Prerequisites

- Deal record in Attio with ACV, champion, economic buyer, and stage
- Pain data from `pain-quantification-prompt` or `call-transcript-pain-extraction`
- Product pricing and packaging info
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
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "You are a deal structuring expert. Given the following deal context, generate 3 multi-year deal options optimized for total contract value while remaining attractive to the buyer.\n\nDeal context:\n- Company: {company_name}\n- Current ACV: ${acv}\n- Pain-to-price ratio: {ratio}x\n- Competitive situation: {competitive_context}\n- Budget cycle: {budget_cycle} (fiscal year end month)\n- Decision maker: {economic_buyer_title}\n- Champion: {champion_name}, {champion_title}\n- Renewal timing: {renewal_or_new}\n- Product tier: {current_tier}\n\nConstraints:\n- Maximum discount: {max_discount_pct}% for any term\n- Minimum term: 2 years\n- Maximum term: 3 years\n- Payment options: annual upfront, quarterly, or monthly with commitment\n- Rate lock: always include for 2+ year terms\n\nReturn this exact JSON:\n{\n  \"options\": [\n    {\n      \"name\": \"Option A: [descriptive name]\",\n      \"term_years\": 2,\n      \"annual_price\": 0,\n      \"total_contract_value\": 0,\n      \"discount_pct\": 0,\n      \"payment_schedule\": \"annual_upfront|quarterly|monthly\",\n      \"rate_lock\": true,\n      \"incentives\": [\"list of included perks\"],\n      \"buyer_savings_vs_monthly\": 0,\n      \"seller_tcv_uplift_vs_annual\": 0,\n      \"recommended_for\": \"scenario where this option fits best\",\n      \"negotiation_anchor\": \"start high — present this option first/second/third\",\n      \"concession_room\": \"what can be offered if buyer pushes back\"\n    }\n  ],\n  \"presentation_order\": [\"Option C\", \"Option A\", \"Option B\"],\n  \"anchoring_strategy\": \"explanation of why this order maximizes TCV\",\n  \"walk_away_floor\": {\n    \"min_term_years\": 2,\n    \"min_annual_price\": 0,\n    \"min_tcv\": 0,\n    \"rationale\": \"why this is the floor\"\n  }\n}"
  }]
}
```

## Response Validation

Check the output for internal consistency:
- `total_contract_value` equals `annual_price * term_years`
- `discount_pct` equals `1 - (annual_price / original_acv)` (within 1% rounding)
- `buyer_savings_vs_monthly` equals `(original_monthly * 12 * term_years) - total_contract_value`
- `seller_tcv_uplift_vs_annual` equals `total_contract_value - (acv * term_years)`
- Options are ordered from highest TCV to lowest in `presentation_order` for anchoring
- `walk_away_floor.min_tcv` is above the break-even point for the deal

## Error Handling

- **No pain data available:** Generate structures based on industry benchmarks, but flag: "Pain data unavailable — discount levels may be overgenerous. Run discovery before presenting."
- **ACV below $5,000:** Multi-year may not be worth the negotiation overhead. Return a recommendation to use self-serve annual conversion (see `multiyear-offer-engine` drill) instead.
- **Competitive situation = "active evaluation":** Tighten discount ranges and add exclusivity/early-access incentives rather than deeper price cuts.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best for structured negotiation reasoning |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Qwilr | Proposal API | For formatting the options into a visual proposal |
| PandaDoc | Document API | For contract generation with e-sign |
| DealHub | CPQ API | Enterprise deal structuring and pricing |
