---
name: pricing-tier-generation
description: Generate Good/Better/Best pricing tier structures with value anchoring, discount guidelines, and presentation framing tailored to a specific prospect
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Pricing Tier Generation

Given a prospect's deal context (discovered pains, company size, competitive landscape, product fit), generate a Good/Better/Best pricing tier structure with value anchoring language, discount guardrails, and presentation order. The output is a ready-to-present pricing breakdown the seller delivers live or in a proposal document.

## Prerequisites

- Deal record in Attio with discovered pains, champion, and deal value
- Pain data from `pain-quantification-prompt` or `call-transcript-pain-extraction`
- Product pricing catalog (tiers, features, add-ons)
- ROI model if available (from `roi-model-generation`)
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
    "content": "You are a pricing strategist. Generate a Good/Better/Best pricing tier structure for a specific prospect. Anchor pricing to their quantified pain and ROI, not to features alone.\n\nProspect context:\n- Company: {company_name}\n- Industry: {industry}\n- Headcount: {headcount}\n- Estimated revenue: {revenue_estimate}\n- Champion: {champion_name}, {champion_title}\n- Economic buyer: {economic_buyer_title}\n- Budget cycle: {budget_cycle}\n\nPain data:\n{pains_json}\n- Total quantified annual pain: ${total_pain}\n- Pain-to-price ratio at list price: {pain_to_price_ratio}x\n\nROI context:\n- Year 1 ROI: {roi_year_1}%\n- Payback period: {payback_months} months\n- 3-year net value: ${three_year_net}\n\nProduct pricing:\n- Base tier: ${base_price}/year — features: {base_features}\n- Pro tier: ${pro_price}/year — features: {pro_features}\n- Enterprise tier: ${enterprise_price}/year — features: {enterprise_features}\n\nCompetitive situation: {competitive_context}\n\nConstraints:\n- Maximum discount authority: {max_discount_pct}%\n- Minimum deal size: ${min_deal_size}/year\n- Payment options: annual upfront, quarterly, monthly with annual commitment\n- Term options: annual, 2-year, 3-year\n\nReturn this exact JSON:\n{\n  \"tiers\": [\n    {\n      \"label\": \"Good|Better|Best\",\n      \"name\": \"Descriptive tier name\",\n      \"annual_price\": 0,\n      \"product_tier\": \"base|pro|enterprise\",\n      \"term_years\": 1,\n      \"discount_applied_pct\": 0,\n      \"features_included\": [\"list\"],\n      \"features_excluded\": [\"list of higher-tier features not included\"],\n      \"value_anchor\": \"One sentence linking this tier's price to the prospect's quantified pain. Format: For [specific savings/outcome], the investment is [price/time period].\",\n      \"roi_framing\": \"ROI at this tier: X%, payback: Y months\",\n      \"recommended_for\": \"When this option is the right choice\",\n      \"objection_preempt\": \"The likely pushback on this tier and the one-sentence response\"\n    }\n  ],\n  \"recommended_tier\": \"Better\",\n  \"recommended_reason\": \"Why Better is the right anchor for this prospect\",\n  \"presentation_order\": [\"Best\", \"Good\", \"Better\"],\n  \"anchoring_script\": \"The exact words to say when presenting pricing. Open with pain recap, then reveal each tier in presentation_order. 5-8 sentences total.\",\n  \"pause_instruction\": \"After presenting all three tiers, stop talking. Wait for the prospect to respond. Do not preemptively discount or justify.\",\n  \"discount_guardrails\": {\n    \"max_discount_without_approval\": 0,\n    \"discount_triggers\": [\"Conditions under which discounting is acceptable\"],\n    \"counter_to_discount_request\": \"What to say instead of discounting: reframe, restructure, or bundle\",\n    \"walk_away_floor\": 0\n  },\n  \"monthly_vs_annual_framing\": \"Show the monthly equivalent alongside annual to make annual feel smaller: $X/month billed annually saves you $Y vs monthly billing.\",\n  \"multi_year_upsell\": {\n    \"two_year_price\": 0,\n    \"two_year_savings\": 0,\n    \"three_year_price\": 0,\n    \"three_year_savings\": 0,\n    \"when_to_mention\": \"Only if prospect selects Better or Best and shows budget confidence\"\n  }\n}"
  }]
}
```

## Response Validation

Check the output for internal consistency:
- `recommended_tier` is "Better" (default anchor) unless deal context justifies otherwise
- `presentation_order` follows contrast anchoring: show Best first (high anchor), then Good (lower), then Better (Goldilocks middle)
- `discount_applied_pct` does not exceed `max_discount_pct` for any tier
- `value_anchor` for each tier references a specific pain point from the input, not generic language
- `walk_away_floor` is above the minimum deal size
- `annual_price` for each tier matches `product_tier_price * (1 - discount_applied_pct / 100)`
- `roi_framing` values are mathematically consistent with input ROI data adjusted for the tier price
- All three tiers are present and distinct (different product tier or different term)

## Error Handling

- **No pain data available:** Generate tiers using list pricing only and flag: "No pain data — value anchoring will be generic. Run discovery before presenting pricing."
- **Pain-to-price ratio < 3:** Flag: "Weak value story (ratio: {ratio}x). Consider deeper discovery or a lower product tier. Discounting will not fix a value problem."
- **Competitive pressure (active eval):** Tighten discount guardrails and add implementation speed / support quality as differentiators rather than price concessions.
- **Budget unknown:** Generate all three tiers but instruct the seller to open with a budget qualification question before revealing specific numbers.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best for structured pricing reasoning with value anchoring |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| PandaDoc | Proposal API | For formatting pricing into visual proposals with e-sign |
| Qwilr | Interactive proposal | Dynamic pricing pages prospects can interact with |
| DealHub | CPQ API | Enterprise configure-price-quote with approval workflows |
| Proposify | Proposal management | Template-based proposal generation |
