---
name: roi-narrative-generation
description: Generate persona-specific ROI narratives that frame product value in the language of the target executive's role and priorities
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# ROI Narrative Generation

Generate executive-persona-specific ROI narratives that translate product value into the financial and strategic language each C-level role cares about. A CEO gets market share and competitive advantage framing. A CFO gets payback period and NPV. A CTO gets technical debt reduction and engineering velocity. A COO gets operational efficiency and scale readiness.

## Prerequisites

- Executive persona (CEO, CFO, CTO, COO, CRO, VP+)
- Quantified pain data from discovery (from `call-transcript-pain-extraction` or `pain-quantification-prompt`)
- Company enrichment data (headcount, revenue, industry) from Clay or Attio
- ROI model output (from `roi-model-generation`) if available
- Anthropic API key

## Steps

### 1. Assemble persona-specific inputs

Build the input object with role-specific framing context:

```json
{
  "exec_name": "Jane Smith",
  "exec_title": "CFO",
  "exec_persona": "CFO",
  "exec_priorities": ["margin improvement", "cash flow predictability", "audit readiness"],
  "company": "Acme Corp",
  "industry": "B2B SaaS",
  "headcount": 85,
  "revenue_estimate": "$12M ARR",
  "pains": [
    {
      "summary": "Manual data entry consuming 2 hours/rep/day",
      "estimated_annual_cost": 172800,
      "confidence": "high"
    }
  ],
  "total_quantified_pain": 412800,
  "product_annual_price": 24000,
  "roi_model": {
    "roi_percentage_year_1": 1620,
    "payback_period_months": 1,
    "three_year_net_value": 1214400
  }
}
```

### 2. Generate the persona-specific narrative via Claude API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Generate an executive ROI narrative for {exec_name}, {exec_title} at {company}.\n\nThis narrative will be used during a 15-20 minute executive demo. It must frame product value in the language this persona cares about. No feature jargon. No technical details unless persona is CTO.\n\nPersona framing rules:\n- CEO: Frame as growth, competitive advantage, market share, strategic positioning. Use 'while competitors are still doing X manually, you would be...'\n- CFO: Frame as payback period, NPV, risk-adjusted ROI, cost avoidance, margin impact. Use exact numbers. Show conservative and moderate scenarios.\n- CTO: Frame as technical debt reduction, engineering velocity, security posture, architecture simplification. Quantify in developer-hours saved.\n- COO: Frame as operational efficiency, process standardization, headcount scaling without proportional cost, SLA improvement.\n- CRO: Frame as pipeline velocity, win rate improvement, rep productivity, quota attainment.\n- VP+: Frame in terms of their specific function's metrics and how this helps them hit their targets.\n\nInputs:\n{stringified_inputs}\n\nReturn this exact JSON:\n{\n  \"opening_hook\": \"One sentence that connects to this exec's top priority. Reference their specific context if available.\",\n  \"value_narrative\": \"3-4 sentences that tell the ROI story in this persona's language. Use their metrics, not yours.\",\n  \"key_numbers\": [\n    {\"metric\": \"persona-relevant metric name\", \"value\": \"formatted number\", \"framing\": \"one sentence contextualizing this number\"}\n  ],\n  \"peer_proof\": \"One sentence referencing what similar companies/roles achieved. Format: 'Companies like yours in {industry} have seen {outcome} in {timeframe}'\",\n  \"risk_framing\": \"One sentence on what happens if they do nothing (cost of inaction in their language)\",\n  \"closing_question\": \"One question that ties the ROI back to their priorities and prompts commitment\",\n  \"slides_talking_points\": [\n    \"Bullet point 1 for the exec summary slide\",\n    \"Bullet point 2\",\n    \"Bullet point 3\"\n  ]\n}"
  }]
}
```

### 3. Generate via OpenAI API (alternative)

```
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer {OPENAI_API_KEY}
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You generate executive-persona-specific ROI narratives for sales demos. Every narrative must use the financial and strategic language of the target persona. No marketing fluff. Exact numbers only."},
    {"role": "user", "content": "{SAME_USER_PROMPT_AS_ABOVE}"}
  ],
  "max_tokens": 2000,
  "temperature": 0.4
}
```

### 4. Validate the narrative

Check:
- `key_numbers` values are consistent with the ROI model input (no inflated numbers)
- `opening_hook` references something specific to the exec or company, not a generic opener
- `value_narrative` uses persona-appropriate language (CFO gets "payback" and "NPV", not "cool feature")
- `peer_proof` references the correct industry and a plausible outcome
- `risk_framing` quantifies cost of inaction, not just states it vaguely

If validation fails, re-prompt with specific correction instructions.

### 5. Store and attach to demo prep

Store the ROI narrative as an Attio note on the deal record, tagged with the exec persona. The demo prep workflow consumes this narrative to populate the exec demo script.

Fire PostHog event:
```json
{
  "event": "roi_narrative_generated",
  "properties": {
    "deal_id": "...",
    "exec_persona": "CFO",
    "key_numbers_count": 3,
    "roi_percentage_used": 1620,
    "personalization_depth": "high|medium|low"
  }
}
```

## Cost Estimates

- Anthropic Claude Sonnet: ~$0.03-0.08 per narrative
- At scale (50 narratives/quarter): under $4/quarter in API costs

## Error Handling

- **No ROI model available:** Generate a qualitative narrative using pain data only. Flag `roi_model_available: false` in the output. Recommend running `roi-model-generation` first for stronger quantitative framing.
- **Exec persona not in standard list:** Map to the closest standard persona based on title keywords. Flag as "mapped persona, verify accuracy."
- **Insufficient pain data:** Generate a role-based narrative using industry benchmarks. Note in output: "Narrative uses benchmark data, not prospect-specific discovery. Personalization depth: low."

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best persona-aware structured output |
| GPT-4 (OpenAI) | Chat Completions API | Good alternative |
| Gemini (Google) | Generative AI API | Alternative LLM |
| Qwilr | API | Can render the narrative into interactive proposals |
| Manual | Template per persona | Fallback with fill-in-the-blank fields |
