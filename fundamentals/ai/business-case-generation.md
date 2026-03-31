---
name: business-case-generation
description: Generate a structured business case document from quantified pain data, ROI projections, and competitive context
tool: Anthropic
difficulty: Advanced
---

# Business Case Generation

Generate a buyer-ready business case document that translates quantified pain points into ROI projections, risk analysis, and a clear recommendation. Designed to arm your champion with the material they need for internal approval.

## Prerequisites

- Quantified pain data from `call-transcript-pain-extraction` and `pain-quantification-prompt`
- Deal record in Attio with prospect company details
- Product pricing and value proposition
- Anthropic API key

## Steps

### 1. Assemble business case inputs

Pull all required data from Attio and the pain extraction results:

```json
{
  "prospect_company": "Acme Corp",
  "prospect_contact": "Jane Smith, VP Sales",
  "prospect_industry": "B2B SaaS",
  "prospect_headcount": 85,
  "prospect_revenue": "$12M ARR",
  "pains": [
    {
      "summary": "Manual data entry taking 2 hours per rep per day",
      "category": "operational",
      "estimated_annual_cost": 172800,
      "confidence": "high",
      "impact_quote": "Our reps spend probably two hours a day just copying data between systems"
    },
    {
      "summary": "Inconsistent follow-up causing deals to slip",
      "category": "financial",
      "estimated_annual_cost": 240000,
      "confidence": "medium",
      "impact_quote": "We probably lose three or four deals a quarter just from slow follow-up"
    }
  ],
  "total_quantified_pain": 412800,
  "product_name": "Your Product",
  "product_annual_price": 24000,
  "implementation_timeline": "2 weeks",
  "competitive_alternatives": ["Status quo (manual)", "Competitor A", "Competitor B"]
}
```

### 2. Generate the business case via Claude API

```
POST https://api.anthropic.com/v1/messages
Authorization: x-api-key {ANTHROPIC_API_KEY}
Content-Type: application/json
```

**Request body:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Generate a business case document for {prospect_company}. Write it as if the prospect's champion ({prospect_contact}) is presenting it internally to get budget approval. Use their own words (the quotes) to make it feel authentic, not like a vendor pitch.\n\nInputs:\n{stringified inputs}\n\nReturn this exact JSON structure:\n{\n  \"title\": \"Business Case: [Product] for [Company]\",\n  \"executive_summary\": \"3-4 sentences summarizing the problem, cost, solution, and expected ROI\",\n  \"current_state\": {\n    \"description\": \"2-3 paragraphs describing current pain using prospect quotes\",\n    \"total_annual_cost\": 0,\n    \"cost_breakdown\": [{\"pain\": \"...\", \"annual_cost\": 0, \"basis\": \"...\"}]\n  },\n  \"proposed_solution\": {\n    \"description\": \"2-3 paragraphs on what changes with the product\",\n    \"implementation_timeline\": \"...\",\n    \"annual_investment\": 0\n  },\n  \"roi_analysis\": {\n    \"year_1_savings\": 0,\n    \"year_1_investment\": 0,\n    \"year_1_net\": 0,\n    \"roi_percentage\": 0,\n    \"payback_period_months\": 0,\n    \"three_year_value\": 0\n  },\n  \"risk_analysis\": [\n    {\"risk\": \"...\", \"mitigation\": \"...\", \"likelihood\": \"low|medium|high\"}\n  ],\n  \"alternatives_comparison\": [\n    {\"option\": \"...\", \"pros\": [\"...\"], \"cons\": [\"...\"], \"estimated_cost\": 0}\n  ],\n  \"recommendation\": \"2-3 sentences with a clear call to action\",\n  \"next_steps\": [\"...\"],\n  \"appendix_pain_detail\": [{\"pain\": \"...\", \"quote\": \"...\", \"cost\": 0, \"confidence\": \"...\"}]\n}"
  }]
}
```

### 3. Validate the business case

Check:
- `roi_analysis.year_1_net` equals `year_1_savings - year_1_investment`
- `roi_percentage` equals `(year_1_net / year_1_investment) * 100`
- `payback_period_months` is plausible (1-36 months; flag anything outside this range)
- All prospect quotes in `current_state` and `appendix_pain_detail` are from the actual transcript
- `total_annual_cost` in `current_state` matches `total_quantified_pain` from inputs
- At least 2 risks are identified with mitigations

### 4. Format and deliver

Convert the JSON to a formatted document. Delivery options:

**Option A: PDF via Puppeteer**
Render the JSON into an HTML template and convert to PDF using Puppeteer:
```bash
node -e "const puppeteer = require('puppeteer'); /* render HTML template with JSON data */ "
```

**Option B: Google Doc via API**
Create a Google Doc using the Google Docs API with the business case content structured into headings, tables, and paragraphs.

**Option C: Markdown attachment**
Generate a Markdown file and attach it to the deal record in Attio.

### 5. Store and track

- Attach the business case to the deal record in Attio as a note or file
- Fire a PostHog event: `business_case_generated` with properties: `deal_id`, `total_pain`, `roi_percentage`, `pain_to_price_ratio`
- Set the deal's `business_case_status` attribute to `generated`
- If the business case ROI exceeds 500%, flag it as a high-priority deal

## Error Handling

- **Insufficient pain data (< 2 quantified pains):** Generate a partial business case with a note that additional discovery is needed. Set `business_case_status` to `draft_incomplete`.
- **ROI calculation produces negative value:** The product costs more than the quantified pain. Flag for review — either the pain needs deeper quantification or this is not a good-fit prospect.
- **LLM generates unrealistic projections:** Cap savings at the sum of quantified pains. Never let the LLM invent additional savings not grounded in transcript data.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output quality |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Qwilr | API | Professional proposal formatting |
| PandaDoc | API | Document automation with e-sign |
| Manual | Template + spreadsheet | Fallback for enterprise deals |
