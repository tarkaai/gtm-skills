---
name: pain-quantification-prompt
description: LLM prompt to estimate the annual dollar cost of a prospect's pain point using contextual clues from calls and enrichment data
tool: Anthropic
product: Claude API
difficulty: Config
---

# Pain Quantification Prompt

Estimate the annual dollar impact of a prospect's pain point by combining transcript clues (team size mentions, time estimates, salary ranges, revenue figures) with enrichment data (company size, industry benchmarks, funding stage).

## Prerequisites

- Extracted pain point data (from `call-transcript-pain-extraction`)
- Company enrichment data from Clay or Attio (headcount, revenue estimate, industry)
- Anthropic API key

## Steps

### 1. Assemble the quantification context

Build a context object combining pain data and enrichment data:

```json
{
  "pain_summary": "Manual data entry taking 2 hours per rep per day",
  "pain_category": "operational",
  "impact_quote": "Our reps spend probably two hours a day just copying data between systems",
  "company_headcount": 85,
  "company_revenue_estimate": "$12M ARR",
  "industry": "B2B SaaS",
  "team_size_mentioned": "12 sales reps",
  "product_annual_price": 24000,
  "additional_context": "Series B, mentioned hiring 5 more reps this quarter"
}
```

### 2. Run the quantification prompt

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
    "content": "Estimate the annual dollar cost of this pain point. Be conservative — use the lower bound when ranges exist. Show your math step by step.\n\nPain: {pain_summary}\nProspect quote: \"{impact_quote}\"\nCompany size: {company_headcount} employees\nRevenue: {company_revenue_estimate}\nIndustry: {industry}\nTeam affected: {team_size_mentioned}\nAdditional context: {additional_context}\n\nReturn this exact JSON:\n{\n  \"estimated_annual_cost\": 0,\n  \"confidence\": \"high|medium|low\",\n  \"calculation_steps\": [\n    {\"assumption\": \"description\", \"value\": 0, \"source\": \"transcript|enrichment|benchmark\"}\n  ],\n  \"low_estimate\": 0,\n  \"high_estimate\": 0,\n  \"pain_to_price_ratio\": 0.0,\n  \"comparison_framing\": \"A sentence framing the cost in relatable terms for the buyer\"\n}"
  }]
}
```

### 3. Validate the estimate

Check the response for reasonableness:
- `estimated_annual_cost` should fall between `low_estimate` and `high_estimate`
- `pain_to_price_ratio` should equal `estimated_annual_cost / product_annual_price`
- Each `calculation_steps` entry should cite its source (transcript quote, enrichment data, or industry benchmark)
- If `confidence` is "low," flag for human review before using in a business case

Reject estimates where:
- The cost exceeds 50% of estimated company revenue (implausible)
- The cost is less than 1% of estimated company revenue for a pain described as severe (underestimate)
- No calculation steps reference transcript data (pure speculation)

### 4. Store the quantification

Update the pain record in Attio with:
- `estimated_annual_cost`
- `cost_confidence`
- `calculation_summary` (stringified calculation_steps)
- `pain_to_price_ratio`
- `comparison_framing`

## Error Handling

- **Insufficient data for quantification:** If the transcript provides no numeric clues (no team size, no time estimates, no revenue mentions), return confidence "low" and use industry benchmarks only. Flag the pain for deeper discovery in the next call.
- **LLM hallucinates numbers:** Cross-check any specific dollar figures in the response against the input context. If the LLM cites a number not present in the input, flag it and re-prompt with: "Only use numbers explicitly stated in the transcript or enrichment data. For everything else, use conservative industry benchmarks and label them as such."

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for financial estimates |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gemini (Google) | Generative AI API | Alternative LLM |
| Manual calculation | Spreadsheet template | Fallback for high-stakes deals |
