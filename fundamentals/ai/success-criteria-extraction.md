---
name: success-criteria-extraction
description: Use Claude to extract and generate measurable success criteria from discovery call transcripts, deal context, and product capabilities
tool: Anthropic
difficulty: Advanced
---

# Success Criteria Extraction

Given a discovery call transcript, deal context, and product capabilities, use the Claude API to extract prospect-stated goals and generate specific, measurable success criteria. The output is a structured set of criteria the prospect can agree to, each with a metric, target, timeline, and measurement method.

## API Call

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  anthropic-version: 2023-06-01
  content-type: application/json

Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "temperature": 0.2,
  "messages": [{
    "role": "user",
    "content": "You are a success criteria analyst for a B2B sales process. Analyze the following inputs and generate specific, measurable success criteria that the prospect can agree to.\n\nDISCOVERY TRANSCRIPT:\n{transcript}\n\nDEAL CONTEXT:\n- Company: {company_name}\n- Industry: {industry}\n- Headcount: {headcount}\n- Current tools: {current_tools}\n- Deal size: {deal_size}\n- Champion: {champion_name}, {champion_title}\n\nPRODUCT CAPABILITIES:\n{product_capabilities}\n\nHISTORICAL SUCCESS RATES (similar deals):\n{historical_success_json}\n\nExtract and generate success criteria. For each:\n1. The prospect's stated goal (use their exact words when possible)\n2. A specific metric to measure it\n3. A quantified target (use the prospect's number if stated; otherwise derive a conservative estimate from their pain description)\n4. Timeline to achieve it\n5. Who measures it (prospect-side stakeholder)\n6. Baseline value (current state, if mentioned or estimable)\n7. Achievability score (0-100): how likely this criteria is to be met based on historical data and product capabilities. Score 80+ = safe to commit. Score 50-79 = achievable with effort. Score <50 = risky, flag for expectation management.\n8. Category: efficiency, revenue, cost_savings, quality, time_to_value, adoption\n\nReturn JSON:\n{\n  \"success_criteria\": [\n    {\n      \"prospect_goal\": \"\",\n      \"metric\": \"\",\n      \"target\": \"\",\n      \"timeline\": \"\",\n      \"measured_by\": \"\",\n      \"baseline\": \"\",\n      \"achievability_score\": 0,\n      \"category\": \"\",\n      \"source_quote\": \"\",\n      \"measurement_method\": \"\"\n    }\n  ],\n  \"missing_info\": [\"list of things the prospect didn't mention that would strengthen the criteria\"],\n  \"risk_flags\": [\"any criteria that seem unrealistic or unmeasurable\"],\n  \"recommended_follow_up_questions\": [\"questions to ask in the next call to refine criteria\"]\n}"
  }]
}
```

## Input Requirements

- `transcript`: Discovery or follow-up call transcript from Fireflies or Gong (use `fireflies-transcription` or `gong-call-recording` fundamental)
- `company_name`, `industry`, `headcount`, `current_tools`, `deal_size`, `champion_name`, `champion_title`: From Attio deal record
- `product_capabilities`: A JSON summary of what your product can measurably deliver
- `historical_success_json`: Aggregated data from past deals showing which criteria were achieved and at what rates (query from Attio)

## Output

JSON with structured success criteria. Each criterion includes an achievability score that guides whether to commit to it in the mutual success plan.

## Post-Processing

1. Store each criterion in Attio as a custom attribute on the deal record
2. Fire PostHog event `success_criteria_extracted` with properties: `deal_id`, `criteria_count`, `avg_achievability_score`, `categories`
3. Flag any criterion with `achievability_score < 50` for founder review before including in the mutual success plan

## Guardrails

- Never generate success criteria the product cannot measure. Every criterion must have a `measurement_method` that maps to an observable data point.
- Never inflate achievability scores. When in doubt, score lower — it is better to under-promise.
- If the transcript contains fewer than 2 identifiable goals, return `missing_info` noting that additional discovery is needed before criteria can be defined.
- Cap the number of criteria at 5. If more goals are identified, rank by achievability and prospect emphasis, and include the top 5.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured extraction quality |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gemini (Google) | Generative AI API | Alternative LLM |
| Gong AI | Deal insights | Built-in extraction, less customizable |
| Manual | Spreadsheet template | Fallback for enterprise deals requiring human judgment |
