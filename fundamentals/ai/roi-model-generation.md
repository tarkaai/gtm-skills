---
name: roi-model-generation
description: Generate a structured ROI model from prospect pain data, product pricing, and industry benchmarks
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# ROI Model Generation

Generate a structured ROI model that takes a prospect's quantified pain data and translates it into a spreadsheet-ready set of inputs, assumptions, calculations, and outputs. The model is conservative by default and cites every assumption source.

## Prerequisites

- Quantified pain data from `pain-quantification-prompt` or `call-transcript-pain-extraction`
- Product pricing and packaging information
- Company enrichment data (headcount, revenue, industry) from Clay or Attio
- Anthropic API key

## Steps

### 1. Assemble model inputs

Build the input object from Attio deal data and enrichment:

```json
{
  "prospect_company": "Acme Corp",
  "prospect_industry": "B2B SaaS",
  "prospect_headcount": 85,
  "prospect_revenue_estimate": "$12M ARR",
  "prospect_role": "VP Sales",
  "pains": [
    {
      "summary": "Manual data entry consuming 2 hours/rep/day",
      "category": "operational",
      "estimated_annual_cost": 172800,
      "confidence": "high",
      "impact_quote": "Our reps spend probably two hours a day just copying data"
    }
  ],
  "total_quantified_pain": 412800,
  "product_name": "Your Product",
  "product_annual_price": 24000,
  "implementation_cost": 5000,
  "implementation_weeks": 2,
  "value_drivers": ["time_savings", "cost_reduction", "revenue_increase", "risk_mitigation"],
  "time_horizon_years": 3
}
```

### 2. Generate the ROI model via Claude API

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
    "content": "Generate a structured ROI model for {prospect_company}. Be conservative: use the lower bound of every range. Every number must cite its source (transcript, enrichment, or benchmark). Do not invent savings not grounded in the pain data.\n\nInputs:\n{stringified inputs}\n\nReturn this exact JSON:\n{\n  \"model_inputs\": [\n    {\"label\": \"description\", \"value\": 0, \"unit\": \"hours|dollars|percent\", \"source\": \"transcript|enrichment|benchmark\", \"adjustable\": true}\n  ],\n  \"assumptions\": [\n    {\"assumption\": \"description\", \"value\": 0, \"basis\": \"why this number\"}\n  ],\n  \"annual_savings_breakdown\": [\n    {\"driver\": \"time_savings|cost_reduction|revenue_increase|risk_mitigation\", \"label\": \"description\", \"year_1\": 0, \"year_2\": 0, \"year_3\": 0, \"source\": \"transcript|enrichment|benchmark\"}\n  ],\n  \"annual_costs\": [\n    {\"label\": \"description\", \"year_1\": 0, \"year_2\": 0, \"year_3\": 0}\n  ],\n  \"summary\": {\n    \"total_savings_year_1\": 0,\n    \"total_cost_year_1\": 0,\n    \"net_benefit_year_1\": 0,\n    \"roi_percentage_year_1\": 0,\n    \"payback_period_months\": 0,\n    \"three_year_net_value\": 0,\n    \"pain_to_price_ratio\": 0\n  },\n  \"sensitivity\": {\n    \"conservative\": {\"roi_percentage\": 0, \"payback_months\": 0},\n    \"moderate\": {\"roi_percentage\": 0, \"payback_months\": 0},\n    \"optimistic\": {\"roi_percentage\": 0, \"payback_months\": 0}\n  },\n  \"comparison_framing\": \"One sentence framing the ROI in relatable terms\"\n}"
  }]
}
```

### 3. Validate the model

Check the response for mathematical consistency:
- `total_savings_year_1` equals the sum of all `annual_savings_breakdown[].year_1`
- `total_cost_year_1` equals the sum of all `annual_costs[].year_1`
- `net_benefit_year_1` equals `total_savings_year_1 - total_cost_year_1`
- `roi_percentage_year_1` equals `(net_benefit_year_1 / total_cost_year_1) * 100`
- `payback_period_months` equals `total_cost_year_1 / (total_savings_year_1 / 12)` (rounded up)
- `pain_to_price_ratio` equals `total_savings_year_1 / product_annual_price`
- No savings line item exceeds its corresponding pain's `estimated_annual_cost`
- `sensitivity.conservative.roi_percentage < sensitivity.moderate.roi_percentage < sensitivity.optimistic.roi_percentage`

Reject and re-prompt if any validation fails.

### 4. Store the model

Update the Attio deal record:
- `roi_model_status` = "generated"
- `roi_year_1` = `summary.roi_percentage_year_1`
- `roi_payback_months` = `summary.payback_period_months`
- `roi_pain_to_price` = `summary.pain_to_price_ratio`
- `roi_three_year_value` = `summary.three_year_net_value`

Store the full model JSON as an Attio note for audit trail.

Fire PostHog event:
```json
{
  "event": "roi_model_generated",
  "properties": {
    "deal_id": "...",
    "roi_percentage": 0,
    "payback_months": 0,
    "pain_to_price_ratio": 0,
    "savings_driver_count": 0,
    "confidence_level": "conservative|moderate|optimistic"
  }
}
```

## Error Handling

- **Insufficient pain data (< 2 quantified pains):** Generate a partial model flagged as `draft_incomplete`. Recommend additional discovery.
- **Negative ROI:** The product costs more than the quantified pain. Flag for review. Either deeper discovery is needed or prospect is not a fit.
- **LLM invents savings:** Cross-check every `annual_savings_breakdown` entry against the input pains. Remove any savings not traceable to a specific pain or benchmark.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for financial models |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gemini (Google) | Generative AI API | Alternative LLM |
| Spreadsheet template | Manual | Fallback for high-stakes enterprise deals |
| Qwilr | API | Professional interactive proposal with ROI section |
