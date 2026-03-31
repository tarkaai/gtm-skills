---
name: cost-of-delay-calculation
description: Use Claude to calculate the monthly and annual cost of delaying a purchase decision based on quantified pain data and timeline context
tool: Anthropic
difficulty: Config
---

# Cost of Delay Calculation

Estimate the monthly dollar cost of NOT solving a prospect's pain point now. Combines pain quantification data with timeline context to produce a delay cost that makes "waiting" feel expensive and concrete.

## Prerequisites

- Pain quantification data from `pain-quantification-prompt` (estimated annual cost of the pain)
- Deal record from Attio with timeline data
- Company enrichment data (headcount, growth rate, industry)
- Anthropic API key

## Steps

### 1. Assemble delay context

Build a context object from the deal record and enrichment data:

```json
{
  "estimated_annual_pain_cost": 288000,
  "pain_summary": "Manual data entry taking 2 hours per rep per day",
  "team_size": 12,
  "company_growth_rate": "hiring 5 more reps this quarter",
  "deal_value_annual": 24000,
  "current_timeline_category": "Medium-term",
  "stated_delay_reason": "Want to wait until Q3 budget cycle",
  "months_of_delay": 4,
  "industry": "B2B SaaS",
  "competitive_context": "Competitor recently adopted similar solution"
}
```

### 2. Run the cost-of-delay prompt

```
POST https://api.anthropic.com/v1/messages
Authorization: x-api-key {ANTHROPIC_API_KEY}
Content-Type: application/json
```

**Request body:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "Calculate the cost of delaying this purchase decision. Be conservative — use lower bounds when ranges exist. Show your math.\n\nPain: {pain_summary}\nEstimated annual pain cost: ${estimated_annual_pain_cost}\nTeam size: {team_size}\nCompany growth rate: {company_growth_rate}\nDeal value (annual): ${deal_value_annual}\nDelay reason: {stated_delay_reason}\nExpected delay: {months_of_delay} months\nIndustry: {industry}\nCompetitive context: {competitive_context}\n\nCalculate THREE types of delay cost:\n\n1. **Direct pain cost**: Monthly pain cost * months delayed. Adjust for growth (if team is growing, pain compounds).\n2. **Opportunity cost**: Revenue, efficiency, or competitive advantage lost during delay period.\n3. **Compounding cost**: How the problem gets worse over time (e.g., more reps = more manual work, competitor gains = harder to win back).\n\nReturn this exact JSON:\n{\n  \"monthly_direct_cost\": 0,\n  \"monthly_opportunity_cost\": 0,\n  \"monthly_compounding_cost\": 0,\n  \"total_monthly_delay_cost\": 0,\n  \"total_delay_cost_over_period\": 0,\n  \"delay_to_deal_ratio\": 0.0,\n  \"calculation_steps\": [\n    {\"component\": \"direct|opportunity|compounding\", \"assumption\": \"...\", \"value\": 0, \"source\": \"pain_data|enrichment|benchmark\"}\n  ],\n  \"executive_framing\": \"One sentence a champion can take to their CFO (e.g., 'Waiting 4 months costs us $96K in wasted rep time and gives Competitor X a 4-month head start')\",\n  \"per_day_cost\": 0,\n  \"comparison_anchors\": [\n    \"The delay costs more than {relatable comparison}\",\n    \"Every week of delay = {tangible loss}\"\n  ],\n  \"confidence\": \"high|medium|low\",\n  \"caveats\": [\"Any assumptions that could significantly change the estimate\"]\n}"
  }]
}
```

### 3. Validate the estimate

Check the response for reasonableness:
- `total_monthly_delay_cost` should approximately equal the sum of the three component costs
- `delay_to_deal_ratio` should equal `total_delay_cost_over_period / deal_value_annual`
- If `delay_to_deal_ratio < 1.0`, the cost of delay is less than the deal value — this is a weak argument. Flag for the seller: "Cost of delay argument is weak for this deal. Consider alternative approaches."
- If `delay_to_deal_ratio > 20`, the estimate may be inflated. Flag for human review.
- Each `calculation_steps` entry should cite its source

### 4. Store the calculation

Update the deal record in Attio with:
- `monthly_cost_of_delay`
- `total_delay_cost`
- `delay_to_deal_ratio`
- `delay_cost_confidence`
- `executive_framing`
- `cost_of_delay_calculated_date`

Fire PostHog event:
```json
{
  "event": "cost_of_delay_calculated",
  "properties": {
    "deal_id": "...",
    "monthly_cost": 24000,
    "total_cost": 96000,
    "delay_months": 4,
    "delay_to_deal_ratio": 4.0,
    "confidence": "medium"
  }
}
```

## Error Handling

- **No pain quantification data:** Cannot compute a credible delay cost. Return an error recommending `pain-quantification-prompt` be run first.
- **Estimated annual pain cost is $0 or null:** Flag the deal for re-discovery. A timing objection with no quantified pain is nearly impossible to overcome with data.
- **Growth rate unknown:** Use industry median growth rate (typically 10-15% for SaaS) and label as benchmark assumption.
- **LLM overestimates:** If `delay_to_deal_ratio > 20`, re-prompt with: "Your estimate seems high. Please recalculate using only the most conservative interpretation of the input data."

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for financial estimates |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Spreadsheet template | Manual calculation | Fallback — input pain data into a formula |
| Clari | Deal intelligence | Has some delay risk scoring but not cost calculation |
