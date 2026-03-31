---
name: call-transcript-objection-extraction
description: Extract, classify, and score price objections from sales call transcripts using LLM analysis
category: Discovery
tools:
  - Fireflies
  - Anthropic
fundamentals:
  - fireflies-transcription
  - anthropic-api-patterns
---

# Extract Price Objections from Call Transcripts

Parse proposal and negotiation call transcripts to identify price objections, classify their root cause, assess severity, and extract the prospect's exact language. Returns structured objection data for response routing and pattern analysis.

## Prerequisites

- Fireflies account with transcribed calls (see `fireflies-transcription`)
- Anthropic API key (Claude) for LLM analysis
- n8n instance for automation (optional but recommended)

## Steps

### 1. Retrieve the transcript

Fetch the full transcript from Fireflies using the GraphQL API:

```graphql
query {
  transcript(id: "<transcript-id>") {
    title
    date
    sentences {
      speaker_name
      text
      start_time
      end_time
    }
    summary
    action_items
  }
}
```

Alternative tools:
| Tool | API | Notes |
|------|-----|-------|
| Fireflies | GraphQL API | Best async extraction, auto-join meetings |
| Gong | `GET /v2/calls/{call_id}/transcript` | Built-in deal intelligence |
| Chorus (ZoomInfo) | REST API | Bundled with ZoomInfo enrichment |
| Otter.ai | REST API | Budget option |
| Rev.ai | REST API | High-accuracy transcription |

### 2. Run objection extraction via Claude API

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
    "content": "Analyze this sales call transcript and extract all price-related objections. For each objection, classify its root cause and assess severity.\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"objections\": [\n    {\n      \"id\": \"obj-001\",\n      \"root_cause\": \"no_budget|value_gap|competitor_comparison|sticker_shock|authority_gap|timing\",\n      \"objection_quote\": \"Exact quote from prospect stating the objection\",\n      \"context_quote\": \"Quote showing what triggered the objection (e.g., pricing reveal)\",\n      \"severity\": 1-10,\n      \"explicitly_stated_budget\": null or dollar amount,\n      \"comparison_anchor\": null or \"what they are comparing to\",\n      \"emotional_tone\": \"firm|exploratory|defensive|negotiating|genuine_concern\",\n      \"response_given\": \"What the seller said in response (exact quote)\",\n      \"response_effectiveness\": \"resolved|partially_resolved|unresolved|escalated\",\n      \"follow_up_needed\": true or false,\n      \"recommended_response_framework\": \"value_reframe|roi_proof|payment_flexibility|competitive_tcm|anchor_to_pain|silence\"\n    }\n  ],\n  \"objection_count\": 0,\n  \"primary_root_cause\": \"the most common root cause across all objections\",\n  \"deal_risk_level\": \"low|medium|high|critical\",\n  \"seller_diagnosis_quality\": \"strong|adequate|weak\",\n  \"diagnosis_gaps\": [\"Questions the seller should have asked but didn't\"],\n  \"pricing_signals\": {\n    \"stated_budget_range\": null or range,\n    \"willingness_to_pay_signals\": [\"positive signals extracted from conversation\"],\n    \"walk_away_signals\": [\"negative signals suggesting deal at risk\"]\n  }\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- Each objection has severity between 1-10
- `root_cause` is one of the six permitted categories
- `emotional_tone` is one of the five permitted values
- All `objection_quote` values are actual text from the transcript (spot-check at least 1)
- `objection_count` matches the length of the `objections` array
- `deal_risk_level` is consistent with severity scores (high severity = high risk)

If validation fails, re-prompt Claude with the specific error and the original transcript.

### 4. Enrich with deal context

Pull the deal record from Attio and append context:
- Deal value vs stated budget (if any)
- Pain-to-price ratio from discovery (if available)
- Competitor mentions from enrichment data
- Number of stakeholders engaged
- Champion strength score

This context determines which response framework is most likely to succeed.

### 5. Store results in CRM

Push the structured objection data to Attio via API:

```json
{
  "data": {
    "values": {
      "price_objection_count": [{"value": 2}],
      "primary_objection_root_cause": [{"value": "value_gap"}],
      "deal_risk_level": [{"value": "medium"}],
      "objection_extraction_date": [{"value": "2026-03-30T00:00:00Z"}],
      "objection_data_json": [{"value": "{full JSON stringified}"}],
      "seller_diagnosis_quality": [{"value": "adequate"}]
    }
  }
}
```

### 6. Log the extraction event in PostHog

Fire a PostHog event for tracking:
```json
{
  "event": "price_objection_extracted",
  "properties": {
    "deal_id": "...",
    "objection_count": 2,
    "primary_root_cause": "value_gap",
    "deal_risk_level": "medium",
    "seller_diagnosis_quality": "adequate",
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `objection_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 50 words):** Likely not a substantive call. Skip extraction and log reason.
- **No objections detected:** Valid result — the call may have had no price pushback. Log `objection_count: 0` and proceed.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds, max 3 retries.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Built-in deal intelligence layers |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Bundled with ZoomInfo data |
| Manual review | Human reviews recording with template | Fallback when automation fails |
