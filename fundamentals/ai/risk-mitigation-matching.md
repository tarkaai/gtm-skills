---
name: risk-mitigation-matching
description: Match identified deal risks to the best mitigation asset (case study, security doc, ROI proof, reference) using LLM analysis
tool: Anthropic
difficulty: Config
---

# Risk Mitigation Matching

Given a structured risk extracted from a sales call, match it to the most effective mitigation asset from a content library. Returns a ranked list of assets with an explanation of why each addresses the specific concern, plus a draft delivery message.

## Prerequisites

- Anthropic API key (Claude)
- Structured risk data from `call-transcript-risk-extraction`
- Mitigation content library indexed in Attio or a structured JSON file (case studies, security whitepapers, ROI calculators, reference contacts, product documentation, guarantees)

## Steps

### 1. Pull the risk data

Receive the risk object:
```json
{
  "id": "risk-001",
  "category": "technical",
  "summary": "Worried about data migration complexity from legacy system",
  "concern_quote": "We've been burned before by migrations that took 6 months instead of 6 weeks",
  "severity": 8,
  "likelihood": 7,
  "mitigation_type_needed": "case_study"
}
```

### 2. Query the mitigation content library

Pull all available mitigation assets from Attio (or a local JSON file). Each asset should have:
```json
{
  "id": "asset-001",
  "type": "case_study|security_doc|roi_proof|reference_contact|product_doc|guarantee|technical_demo",
  "title": "...",
  "risk_categories_addressed": ["technical", "timeline"],
  "industry": "...",
  "company_size": "...",
  "key_claims": ["Migration completed in 4 weeks", "Zero data loss"],
  "url_or_path": "..."
}
```

### 3. Match risk to assets via Claude API

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
    "content": "A sales prospect expressed this concern:\nRisk: {risk_summary}\nExact quote: \"{concern_quote}\"\nCategory: {category}\nSeverity: {severity}/10\n\nHere are available mitigation assets:\n{json_array_of_assets}\n\nRank the top 3 assets that best address this specific concern. For each:\n1. Asset ID and title\n2. Why it addresses this risk (reference specific claims from the asset)\n3. A 2-3 sentence delivery message that connects the asset to the prospect's exact words\n4. Confidence score 0.0-1.0 that this asset will reduce the prospect's concern\n\nReturn JSON:\n{\n  \"matched_assets\": [\n    {\n      \"asset_id\": \"...\",\n      \"title\": \"...\",\n      \"relevance_explanation\": \"...\",\n      \"delivery_message\": \"...\",\n      \"confidence\": 0.0\n    }\n  ],\n  \"gap_identified\": true/false,\n  \"gap_description\": \"If no asset scores above 0.6 confidence, describe what content should be created\"\n}"
  }]
}
```

### 4. Handle content gaps

If `gap_identified` is true (no asset has confidence >= 0.6), log this as a content gap:
- Fire PostHog event `mitigation_content_gap` with the risk category and summary
- Create an Attio note: "Content gap: need {mitigation_type_needed} for {risk_category} risk: {summary}"
- Fall back to a generic response framework for the risk category

### 5. Return the match result

Output the ranked asset list with delivery messages ready for the seller to send or the agent to deliver automatically.

## Error Handling

- **Empty content library:** Return `gap_identified: true` for all risks. The team needs to build mitigation assets.
- **No matching category:** Expand search to all assets regardless of `risk_categories_addressed`. Cross-category assets sometimes address the underlying concern.
- **LLM returns malformed JSON:** Retry once. If still malformed, return top asset by simple category matching (no LLM).

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude | Anthropic API | Best semantic matching |
| GPT-4 | OpenAI API | Alternative LLM |
| Embeddings search | OpenAI or Voyage embeddings | Better at scale with 100+ assets |
| Manual lookup | Human searches content library | Fallback |
