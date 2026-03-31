---
name: call-transcript-pain-extraction
description: Extract, categorize, and quantify prospect pain points from discovery call transcripts using LLM analysis
category: Discovery
tools:
  - Fireflies
  - Anthropic
fundamentals:
  - fireflies-transcription
  - anthropic-api-patterns
---

# Extract Pain Points from Call Transcripts

Parse discovery call transcripts to identify, categorize, and quantify prospect pain points. Returns structured pain data with severity scores, dollar-impact estimates, and supporting quotes.

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
| Gong | `GET /v2/calls/{call_id}/transcript` | Built-in call analytics |
| Chorus (ZoomInfo) | REST API | Bundled with ZoomInfo enrichment |
| Otter.ai | REST API | Budget option |
| Rev.ai | REST API | High-accuracy transcription |

### 2. Run pain extraction via Claude API

Send the transcript to Claude with a structured extraction prompt:

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
    "content": "Analyze this discovery call transcript and extract all prospect pain points. For each pain, estimate the dollar impact based on clues in the conversation (team size, time wasted, revenue lost, cost of current solution, etc.).\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"pains\": [\n    {\n      \"id\": \"pain-001\",\n      \"category\": \"operational|financial|strategic|technical|compliance\",\n      \"summary\": \"One-sentence description of the pain\",\n      \"severity\": 1-10,\n      \"frequency\": \"daily|weekly|monthly|quarterly|annually\",\n      \"current_workaround\": \"How they handle it today\",\n      \"impact_quote\": \"Exact quote from prospect describing the impact\",\n      \"trigger_quote\": \"Exact quote revealing why this matters now\",\n      \"estimated_annual_cost\": 0,\n      \"cost_basis\": \"How the dollar estimate was derived from transcript clues\",\n      \"affected_stakeholders\": [\"roles affected by this pain\"],\n      \"explicitly_stated\": true,\n      \"confidence\": 0.0-1.0\n    }\n  ],\n  \"total_quantified_pain\": 0,\n  \"pain_count\": 0,\n  \"quantification_rate\": 0.0,\n  \"strongest_pain_id\": \"pain-001\",\n  \"gaps\": [\"Areas the call did not explore that should be probed in follow-up\"],\n  \"prospect_emotional_state\": \"frustrated|concerned|curious|neutral|skeptical\",\n  \"urgency_signals\": [\"Quotes indicating time pressure\"]\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- Each pain has a severity between 1-10 and confidence between 0.0-1.0
- `total_quantified_pain` equals the sum of all `estimated_annual_cost` values
- `quantification_rate` equals (pains with estimated_annual_cost > 0) / pain_count
- `strongest_pain_id` references the pain with the highest severity * confidence product
- All `impact_quote` and `trigger_quote` values are actual text from the transcript (spot-check 2-3)

If validation fails, re-prompt Claude with the specific error and the original transcript.

### 4. Classify pains by discovery depth

For each extracted pain, classify how deeply it was explored:

- **Surface** (severity 1-3): Prospect mentioned it in passing. No quantification. Need follow-up.
- **Explored** (severity 4-6): Prospect described the problem and current workaround. Partial quantification.
- **Quantified** (severity 7-10): Prospect gave specific numbers, timelines, or dollar amounts. Ready for business case.

Add a `depth` field to each pain: `surface`, `explored`, or `quantified`.

### 5. Store results in CRM

Push the structured pain data to Attio via API:

```json
{
  "data": {
    "values": {
      "pain_count": [{"value": 5}],
      "total_quantified_pain": [{"value": 340000}],
      "pain_quantification_rate": [{"value": 0.8}],
      "pain_to_price_ratio": [{"value": 12.5}],
      "strongest_pain_category": [{"value": "operational"}],
      "pain_extraction_date": [{"value": "2026-03-30T00:00:00Z"}],
      "pain_data_json": [{"value": "{full JSON stringified}"}]
    }
  }
}
```

### 6. Log the extraction event in PostHog

Fire a PostHog event for tracking:
```json
{
  "event": "pain_extraction_completed",
  "properties": {
    "deal_id": "...",
    "pain_count": 5,
    "total_quantified_pain": 340000,
    "quantification_rate": 0.8,
    "pain_to_price_ratio": 12.5,
    "source": "call_transcript",
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `pain_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 100 words):** Likely a no-show or introductory call with no discovery. Skip extraction and log reason.
- **No pains detected:** This is a valid result — log it. The prospect may not have pain, or the discovery questions were not effective. Flag the call for question bank review.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds, max 3 retries.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Built-in call analytics + LLM extraction |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Bundled with ZoomInfo data |
| Manual review | Human reviews recording with template | Fallback when automation fails |
