---
name: call-transcript-need-extraction
description: Extract business need signals from call transcripts using LLM analysis — severity, urgency, impact, and attempted solutions
category: Discovery
tools:
  - Fireflies
  - Anthropic
fundamentals:
  - fireflies-transcription
  - anthropic-api-patterns
---

# Extract Need Signals from Call Transcripts

Parse meeting transcripts to identify, categorize, and score business needs the prospect describes. Returns structured need assessments with severity, urgency, impact on business, and prior solution attempts.

## Prerequisites

- Fireflies account with transcribed calls (see `fireflies-transcription`)
- Anthropic API key (Claude) or OpenAI API key for LLM analysis
- Need categories defined (output from `need-scorecard-setup` drill)

## Steps

### 1. Retrieve the transcript

Fetch the full transcript from Fireflies using the GraphQL API:

```graphql
query {
  transcript(id: "<transcript-id>") {
    title
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

Alternatively, if using Gong: `GET /v2/calls/{call_id}/transcript` with Bearer token.

### 2. Run need extraction via Claude API

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
    "content": "Analyze this sales call transcript and extract business need signals. The prospect may describe multiple needs — identify each one separately. Return JSON only.\n\nNeed categories to score against:\n{need_categories_json}\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"needs\": [\n    {\n      \"category\": \"string — one of the predefined need categories\",\n      \"description\": \"one-sentence summary of the specific need expressed\",\n      \"severity\": 1-3,\n      \"severity_label\": \"Critical|Moderate|Low\",\n      \"urgency\": \"immediate|this_quarter|this_year|someday\",\n      \"business_impact\": \"string — how this need affects their business, in their words\",\n      \"attempted_solutions\": [\"what they've tried before\"],\n      \"stakeholders_affected\": [\"roles/teams impacted\"],\n      \"supporting_quotes\": [\"exact quotes from transcript\"],\n      \"product_fit\": \"direct|partial|tangential\",\n      \"confidence\": 0.0-1.0\n    }\n  ],\n  \"total_need_score\": 0-21,\n  \"critical_need_count\": 0-7,\n  \"needs_above_threshold\": true|false,\n  \"qualification_notes\": \"string — summary of whether this prospect has genuine needs your product solves\",\n  \"gaps_not_explored\": [\"need categories not discussed in the call\"],\n  \"next_discovery_questions\": [\"questions to ask in follow-up to probe unexplored areas\"]\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- Each need has a severity score of 1-3
- `total_need_score` is the sum of all severity scores (max 3 per category * number of categories)
- `critical_need_count` equals the number of needs with severity = 3
- `needs_above_threshold` is true when total_need_score >= 12 and critical_need_count >= 2
- All supporting quotes actually appear in the transcript text

If validation fails, re-prompt with the error.

### 4. Store results in CRM

Push the structured need scores to Attio via MCP or API:

```json
{
  "data": {
    "values": {
      "need_total_score": [{"value": 16}],
      "need_critical_count": [{"value": 3}],
      "need_tier": [{"value": "high_need"}],
      "need_strongest_category": [{"value": "reducing manual work"}],
      "need_assessment_source": [{"value": "Discovery Call"}],
      "need_last_assessed": [{"value": "2026-03-30T00:00:00Z"}]
    }
  }
}
```

### 5. Log the extraction event

Fire a PostHog event for tracking:
```json
{
  "event": "need_extraction_completed",
  "properties": {
    "deal_id": "...",
    "total_need_score": 16,
    "critical_need_count": 3,
    "needs_above_threshold": true,
    "need_count": 5,
    "product_fit_direct_count": 3,
    "source": "call_transcript",
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `need_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 50 words):** Likely a no-show or quick cancel. Skip extraction.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds.
- **No needs identified:** Return empty needs array and log — this is a valid signal (prospect may not have genuine needs).

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Better call analytics built-in |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Owned by ZoomInfo |
| Manual review | Human listens to recording | Fallback when automation fails |
