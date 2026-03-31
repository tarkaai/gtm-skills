---
name: call-transcript-bant-extraction
description: Extract Budget, Authority, Need, and Timeline signals from call transcripts using LLM analysis
category: Discovery
tools:
  - Fireflies
  - Anthropic
fundamentals:
  - fireflies-transcription
  - anthropic-api-patterns
---

# Extract BANT Signals from Call Transcripts

Parse meeting transcripts to identify and score Budget, Authority, Need, and Timeline qualification signals. Returns structured BANT scores per prospect.

## Prerequisites

- Fireflies account with transcribed calls (see `fireflies-transcription`)
- Anthropic API key (Claude) or OpenAI API key for LLM analysis
- n8n instance for automation (optional but recommended)

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

### 2. Run BANT extraction via Claude API

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
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Analyze this sales call transcript and extract BANT qualification signals. Return JSON only.\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"budget\": {\n    \"score\": 0-100,\n    \"signals\": [\"exact quotes or paraphrases indicating budget availability\"],\n    \"red_flags\": [\"quotes indicating budget constraints\"],\n    \"status\": \"confirmed|likely|unclear|absent\"\n  },\n  \"authority\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes indicating decision-making power\"],\n    \"red_flags\": [\"quotes indicating this person cannot decide\"],\n    \"status\": \"decision_maker|influencer|champion|unknown\",\n    \"other_stakeholders\": [\"names and roles mentioned\"]\n  },\n  \"need\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes describing pain points or requirements\"],\n    \"red_flags\": [\"quotes suggesting no real need\"],\n    \"status\": \"critical|important|nice_to_have|absent\"\n  },\n  \"timeline\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes indicating urgency or deadlines\"],\n    \"red_flags\": [\"quotes indicating no timeline\"],\n    \"status\": \"immediate|this_quarter|this_year|no_timeline\",\n    \"estimated_close\": \"YYYY-MM or null\"\n  },\n  \"composite_score\": 0-100,\n  \"qualification_verdict\": \"qualified|needs_work|disqualified\",\n  \"next_steps\": [\"recommended actions based on gaps\"]\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- All four BANT dimensions have scores between 0-100
- `composite_score` equals the weighted average: Budget (25%) + Authority (25%) + Need (30%) + Timeline (20%)
- `qualification_verdict` matches: qualified (composite >= 70), needs_work (40-69), disqualified (< 40)

If validation fails, re-prompt with the error.

### 4. Store results in CRM

Push the structured BANT scores to Attio via MCP or API:

```json
{
  "data": {
    "values": {
      "bant_budget_score": [{"value": 75}],
      "bant_authority_score": [{"value": 60}],
      "bant_need_score": [{"value": 90}],
      "bant_timeline_score": [{"value": 45}],
      "bant_composite_score": [{"value": 68}],
      "bant_verdict": [{"value": "needs_work"}],
      "bant_last_assessed": [{"value": "2026-03-30T00:00:00Z"}]
    }
  }
}
```

### 5. Log the extraction event

Fire a PostHog event for tracking:
```json
{
  "event": "bant_extraction_completed",
  "properties": {
    "deal_id": "...",
    "composite_score": 68,
    "verdict": "needs_work",
    "source": "call_transcript",
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `bant_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 50 words):** Likely a no-show or quick cancel. Skip extraction.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Better call analytics built-in |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Owned by ZoomInfo |
| Manual review | Human listens to recording | Fallback when automation fails |
