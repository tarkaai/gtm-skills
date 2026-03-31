---
name: briefing-document-creation
description: Generate a structured one-pager briefing document for analyst or consultant meetings using the Anthropic API
tool: Anthropic Claude API
difficulty: Config
---

# Create Analyst Briefing Document via LLM

Generate a structured, one-page briefing document tailored to a specific analyst or consultant. The document positions your product within their coverage area and gives them the information they need to understand and recommend you.

## Prerequisites

- Anthropic API key (or OpenAI API key as fallback)
- Company positioning and messaging (what you do, for whom, differentiation)
- Target analyst profile (name, firm, coverage area, recent publications)
- Product metrics you are willing to share (growth, customers, usage data)

## Steps

### 1. Gather analyst-specific context

Before generating the briefing doc, collect:
- Analyst's recent publications (last 2-3 reports or articles)
- Their known evaluation criteria (if they publish frameworks like Magic Quadrants, know the axes)
- Competitors they have covered or recommended
- Terminology they use for your category (match their language, not yours)

### 2. Generate the briefing document via Anthropic API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2048,
  "system": "You are creating a one-page analyst briefing document. This document will be sent to an industry analyst before a briefing meeting. It must be factual, concise, and structured. No marketing fluff. Analysts see through hype immediately.\n\nRules:\n- Maximum 800 words\n- Use the analyst's own terminology for the category\n- Lead with the market problem, not the product\n- Include specific metrics (customers, growth rate, retention) — analysts respect data\n- Acknowledge competitors objectively — never trash-talk\n- End with 3 specific discussion topics for the briefing meeting\n- Format as clean markdown with clear headers",
  "messages": [
    {
      "role": "user",
      "content": "Create a briefing document for {ANALYST_NAME} at {ANALYST_FIRM}.\n\nTheir coverage area: {COVERAGE_AREA}\nTheir recent work: {RECENT_PUBLICATIONS_SUMMARY}\nTerminology they use: {THEIR_CATEGORY_TERMS}\n\nOur company: {COMPANY_NAME}\nWhat we do: {PRODUCT_DESCRIPTION}\nTarget buyer: {ICP_DESCRIPTION}\nKey metrics: {METRICS — customers, growth, retention, etc.}\nDifferentiation: {HOW_WE_ARE_DIFFERENT}\nCompetitors: {KNOWN_COMPETITORS_AND_POSITIONING}\n\nWhat we want from this briefing: {GOAL — awareness, inclusion in research, referrals, feedback on positioning}\n\nGenerate the briefing document."
    }
  ]
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
    {
      "role": "system",
      "content": "{SAME_SYSTEM_PROMPT_AS_ABOVE}"
    },
    {
      "role": "user",
      "content": "{SAME_USER_PROMPT_AS_ABOVE}"
    }
  ],
  "max_tokens": 2048,
  "temperature": 0.5
}
```

### 4. Structure of the output document

The generated briefing should follow this structure:

```
# Briefing Document: {Company Name}
## Prepared for {Analyst Name}, {Analyst Firm}

### Market Context
- The problem in the market (2-3 sentences, using analyst's terminology)
- Why it matters now (timing/trend)

### Company Overview
- Founded: {year}, Headquarters: {location}
- Team: {size and notable backgrounds}
- Funding: {stage and amount, if public}
- Customers: {count, notable logos if permitted}

### Product & Approach
- What the product does (1 paragraph, factual)
- Key differentiation (what we do that others don't)
- Architecture/technical approach (if relevant to analyst's framework)

### Traction & Metrics
- Growth: {MRR growth, customer growth, usage growth}
- Retention: {net revenue retention, logo retention}
- Engagement: {DAU/MAU, time-to-value, activation rate}

### Competitive Landscape
- How we see the market segmenting
- Where we fit vs. {competitor 1}, {competitor 2}
- What we believe we do better and where we have gaps

### Discussion Topics
1. {Specific topic relevant to analyst's coverage}
2. {Question about market direction we want their perspective on}
3. {Area where we want feedback on our positioning}
```

### 5. Review and customize

**Human action required:** Review every generated briefing before sending. Check:
- Are all metrics accurate and up-to-date?
- Is the competitive positioning fair and defensible?
- Are discussion topics genuinely interesting to this specific analyst?
- Does the language match the analyst's framework/terminology?

Edit as needed. The LLM provides the structure and first draft; the founder adds authenticity and precision.

## Cost Estimates

- Anthropic Claude Sonnet: ~$0.03-0.05 per briefing document
- At scale (50 briefings/year): under $3/year in API costs

## Error Handling

- **Output is too salesy:** Increase the emphasis on "no marketing fluff" in the system prompt. Add examples of what NOT to write.
- **Metrics are missing:** The LLM will leave placeholders. Fill them manually or skip the Metrics section if you cannot share data.
- **Wrong terminology:** Update the analyst's terminology input. Pull exact phrases from their published reports.
