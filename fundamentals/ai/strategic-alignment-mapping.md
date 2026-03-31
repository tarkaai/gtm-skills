---
name: strategic-alignment-mapping
description: Use LLM to map product value propositions to a prospect's known strategic initiatives, generating alignment narratives for executive stakeholders
tool: Anthropic
product: Claude API
difficulty: Config
---

# Strategic Alignment Mapping

Map your product's value propositions to a prospect's declared strategic initiatives (digital transformation, efficiency programs, growth targets, compliance mandates, etc.). Produces structured alignment narratives that connect your solution to what executives already care about, making budget approval easier.

## Prerequisites

- Prospect's strategic initiatives (from 10-K filings, press releases, earnings calls, LinkedIn posts, or discovery call transcripts)
- Company enrichment data from Clay or Attio (industry, headcount, revenue, recent funding)
- Product value propositions list
- Anthropic API key

## Steps

### 1. Gather strategic initiative data

Assemble known initiatives from multiple sources:

```json
{
  "company": "Acme Corp",
  "industry": "B2B SaaS",
  "headcount": 200,
  "revenue_estimate": "$25M ARR",
  "initiatives": [
    {
      "name": "AI-first operations",
      "source": "CEO LinkedIn post, 2026-02-15",
      "detail": "CEO announced initiative to automate 60% of manual workflows by Q4 2026",
      "confidence": "high"
    },
    {
      "name": "Series C readiness",
      "source": "Discovery call transcript",
      "detail": "VP Sales mentioned board pressure to show efficient growth metrics before next raise",
      "confidence": "high"
    },
    {
      "name": "International expansion",
      "source": "Job postings on LinkedIn",
      "detail": "Hiring EMEA sales roles, suggests European market entry",
      "confidence": "medium"
    }
  ],
  "product_value_props": [
    {
      "prop": "Automates sales data entry, saving 2+ hours per rep per day",
      "category": "operational_efficiency"
    },
    {
      "prop": "Provides real-time pipeline visibility for board reporting",
      "category": "reporting"
    },
    {
      "prop": "Reduces ramp time for new hires by 40%",
      "category": "scaling"
    }
  ]
}
```

### 2. Generate alignment mappings via Claude API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json
```

**Request body:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2500,
  "messages": [{
    "role": "user",
    "content": "Map product value propositions to this company's strategic initiatives. For each mapping, write a 2-3 sentence alignment narrative that an executive would find compelling. Frame the product as an accelerator of their existing strategy, not a separate initiative.\n\nCompany: {company}\nIndustry: {industry}\nRevenue: {revenue_estimate}\n\nStrategic Initiatives:\n{initiatives_json}\n\nProduct Value Propositions:\n{value_props_json}\n\nReturn this exact JSON:\n{\n  \"alignments\": [\n    {\n      \"initiative\": \"initiative name\",\n      \"value_prop\": \"matching value proposition\",\n      \"alignment_strength\": \"strong|moderate|weak\",\n      \"executive_narrative\": \"2-3 sentences framing the product as an accelerator of this initiative. Use the exec's language.\",\n      \"target_persona\": \"CEO|CFO|CTO|COO|CRO|VP\",\n      \"proof_point\": \"One specific metric or outcome that validates this alignment\",\n      \"risk_of_inaction\": \"One sentence on what happens to this initiative without the product\"\n    }\n  ],\n  \"unmatched_initiatives\": [\"initiatives with no strong product alignment\"],\n  \"unmatched_value_props\": [\"value props that don't map to any known initiative\"],\n  \"recommended_discovery_questions\": [\"questions to surface additional initiatives that might align\"],\n  \"overall_alignment_score\": 0.0\n}"
  }]
}
```

### 3. Validate the mappings

Check the response:
- Each `alignment_strength` of "strong" must have a direct causal link between the value prop and the initiative (not just thematic similarity)
- `executive_narrative` must reference the specific initiative by name, not use generic framing
- `target_persona` must match the executive who owns the initiative
- `overall_alignment_score` should equal the count of "strong" alignments divided by the total initiative count
- `risk_of_inaction` must be specific to the initiative, not generic competitive fear

Reject and re-prompt if any strong alignment lacks a concrete causal link.

### 4. Store and distribute

Update the Attio deal record:
- `strategic_alignment_score` = `overall_alignment_score`
- `aligned_initiatives_count` = count of strong alignments
- Store the full alignment JSON as an Attio note

Fire PostHog event:
```json
{
  "event": "strategic_alignment_mapped",
  "properties": {
    "deal_id": "...",
    "alignment_score": 0.0,
    "strong_alignments": 0,
    "initiatives_count": 0,
    "unmatched_initiatives": 0,
    "target_personas": ["CFO", "CEO"]
  }
}
```

The alignment narratives feed directly into `business-case-generation` and `roi-narrative-generation` to strengthen the strategic framing sections.

## Error Handling

- **No known initiatives:** Return `overall_alignment_score: 0` and populate `recommended_discovery_questions` with 5 questions designed to uncover strategic priorities. The business case will be weaker without strategic alignment, but can still rely on financial ROI.
- **All alignments are "weak":** The product may not fit this prospect's current priorities. Flag the deal for review and suggest timing-based re-engagement.
- **LLM invents initiatives:** Cross-check every `initiative` name in the response against the input list. Remove any initiative not present in the original data.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best strategic reasoning quality |
| GPT-4 (OpenAI) | Chat Completions API | Good alternative |
| Clay Claygent | Built-in AI | Good for batch processing initiative extraction from news |
| Manual | Spreadsheet mapping | Fallback for high-stakes enterprise deals |
| 6sense | Intent + strategic signals | Enterprise-grade initiative detection |
