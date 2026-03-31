---
name: status-quo-cost-analysis
description: Use Claude to generate a comprehensive cost-of-staying analysis comparing total cost of current solution vs total cost of switching
tool: Anthropic
difficulty: Advanced
---

# Status Quo Cost Analysis

Generate a structured comparison of the total cost of staying with the current solution versus the total cost of switching. Includes hidden costs, opportunity costs, scaling costs, and risk costs that prospects typically underestimate when anchored to their current spend.

## Prerequisites

- Pain data from discovery (from `call-transcript-pain-extraction` or manual notes)
- Current solution details: name, estimated spend, contract terms
- Company enrichment data from Clay or Attio (headcount, revenue, growth rate)
- Product pricing and implementation costs
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
    "content": "Generate a total cost comparison: staying with the current solution vs switching. Be conservative on switching costs (use high estimates) and thorough on staying costs (include hidden costs prospects overlook). Every number must cite its source.\n\nCurrent solution:\n- Name: {current_solution}\n- Annual spend: ${current_annual_spend}\n- Years on solution: {years_on_current}\n- Contract status: {contract_status}\n- Known limitations: {known_limitations}\n\nProspect context:\n- Company: {company_name}\n- Headcount: {headcount}\n- Growth rate: {growth_rate or 'unknown'}\n- Industry: {industry}\n- Revenue: {revenue_estimate}\n\nQuantified pains (from discovery):\n{pains_json}\n\nNew solution:\n- Annual price: ${new_annual_price}\n- Implementation cost: ${implementation_cost}\n- Implementation timeline: {implementation_weeks} weeks\n- Training required: {training_hours} hours per user\n\nReturn this exact JSON:\n{\n  \"cost_of_staying\": {\n    \"direct_costs\": [\n      {\"label\": \"description\", \"annual_cost\": 0, \"source\": \"transcript|enrichment|benchmark\", \"notes\": \"\"}\n    ],\n    \"hidden_costs\": [\n      {\"label\": \"description\", \"annual_cost\": 0, \"source\": \"transcript|enrichment|benchmark\", \"notes\": \"\"}\n    ],\n    \"opportunity_costs\": [\n      {\"label\": \"description\", \"annual_cost\": 0, \"source\": \"transcript|enrichment|benchmark\", \"notes\": \"\"}\n    ],\n    \"scaling_costs\": [\n      {\"label\": \"description\", \"annual_cost_year_1\": 0, \"annual_cost_year_3\": 0, \"source\": \"transcript|enrichment|benchmark\", \"notes\": \"\"}\n    ],\n    \"total_annual_staying\": 0,\n    \"total_3_year_staying\": 0\n  },\n  \"cost_of_switching\": {\n    \"one_time_costs\": [\n      {\"label\": \"description\", \"cost\": 0, \"source\": \"pricing|estimate\", \"notes\": \"\"}\n    ],\n    \"annual_costs\": [\n      {\"label\": \"description\", \"annual_cost\": 0, \"source\": \"pricing|estimate\", \"notes\": \"\"}\n    ],\n    \"productivity_dip\": {\n      \"duration_weeks\": 0,\n      \"estimated_cost\": 0,\n      \"notes\": \"Conservative estimate of productivity loss during transition\"\n    },\n    \"total_year_1_switching\": 0,\n    \"total_3_year_switching\": 0\n  },\n  \"comparison\": {\n    \"year_1_delta\": 0,\n    \"year_3_delta\": 0,\n    \"break_even_month\": 0,\n    \"savings_per_employee_year_1\": 0,\n    \"cost_of_delay_per_month\": 0\n  },\n  \"framing\": {\n    \"headline\": \"One sentence: staying costs $X more than switching over 3 years\",\n    \"monthly_pain\": \"Each month you wait costs ${X} in continued pain\",\n    \"per_employee\": \"That's ${X} per employee per year in lost productivity\"\n  }\n}"
  }]
}
```

## Input Requirements

- `current_solution`: Name of the incumbent tool/process
- `current_annual_spend`: What they currently pay (if known; estimate from benchmarks if not)
- `pains_json`: Structured pain data from discovery with estimated annual costs
- `new_annual_price`: Your product's annual price for this prospect
- `implementation_cost`: One-time implementation fee

## Validation

Check the response for mathematical consistency:
- `total_annual_staying` equals sum of all direct_costs + hidden_costs + opportunity_costs annual amounts
- `total_3_year_staying` accounts for scaling costs growing over time
- `total_year_1_switching` equals sum of one_time_costs + annual_costs + productivity_dip.estimated_cost
- `year_1_delta` equals `total_annual_staying - total_year_1_switching` (positive = switching saves money)
- `cost_of_delay_per_month` equals approximately `(total_annual_staying - annual_costs_of_new_solution) / 12`
- No hidden_cost or opportunity_cost exceeds 25% of company revenue (sanity check)

Reject and re-prompt if any validation fails.

## Output

JSON response containing:
- Full breakdown of staying costs (direct + hidden + opportunity + scaling)
- Full breakdown of switching costs (one-time + annual + productivity dip)
- Year 1 and 3-year comparison
- Break-even month
- Cost-of-delay per month (powerful urgency driver)
- Ready-to-use framing sentences

Store in Attio as a note on the deal record. Log in PostHog as `status_quo_cost_generated` event.

## Guardrails

- Always include productivity dip in switching costs (never pretend switching is frictionless)
- Hidden costs must be defensible: cite industry benchmarks or transcript quotes
- If the analysis shows switching is MORE expensive in year 1, present it honestly and highlight the 3-year view
- Never fabricate savings categories not grounded in the prospect's actual pain data
- If `current_annual_spend` is unknown, estimate from industry benchmarks and label as "estimated"

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for financial comparison |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Spreadsheet template | Manual | Fallback for enterprise deals requiring CFO review |
| Qwilr | API | Interactive proposal with embedded cost comparison |
