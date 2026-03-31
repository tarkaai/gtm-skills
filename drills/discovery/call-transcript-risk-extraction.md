---
name: call-transcript-risk-extraction
description: Extract, classify, and score deal risks and implementation concerns from sales call transcripts using LLM analysis
category: Discovery
tools:
  - Fireflies
  - Anthropic
fundamentals:
  - fireflies-transcription
  - anthropic-api-patterns
---

# Extract Deal Risks from Call Transcripts

Parse discovery and evaluation call transcripts to identify risks, concerns, and implementation fears expressed by the prospect. Returns structured risk data with severity/likelihood scoring, category classification, and supporting quotes. This is distinct from objection extraction (which handles price pushback) and pain extraction (which handles current-state problems) -- risk extraction focuses on forward-looking concerns about what could go wrong if they buy.

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

### 2. Run risk extraction via Claude API

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
    "content": "Analyze this sales call transcript and extract all risks, concerns, and implementation fears expressed by the prospect. Focus on forward-looking worries about what could go wrong -- NOT current-state pain points and NOT price objections (those are handled separately).\n\nRisk categories:\n- Financial: budget overruns, hidden costs, ROI uncertainty, sunk costs\n- Technical: integration complexity, security concerns, data migration, downtime\n- Organizational: change management, adoption resistance, training burden, team disruption\n- Timeline: implementation delays, competing priorities, resource availability\n- Vendor: company stability, support quality, product roadmap, lock-in\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"risks\": [\n    {\n      \"id\": \"risk-001\",\n      \"category\": \"financial|technical|organizational|timeline|vendor\",\n      \"summary\": \"One-sentence description of the risk\",\n      \"concern_quote\": \"Exact quote from prospect expressing the concern\",\n      \"context_quote\": \"What was being discussed when this risk surfaced\",\n      \"severity\": 1-10,\n      \"likelihood\": 1-10,\n      \"risk_score\": 0,\n      \"explicitly_stated\": true,\n      \"emotional_tone\": \"worried|cautious|skeptical|testing|resigned\",\n      \"stakeholder_source\": \"Who raised this concern (by role if identifiable)\",\n      \"seller_response\": \"What the seller said in response (exact quote, or null if unaddressed)\",\n      \"response_effectiveness\": \"resolved|partially_resolved|unaddressed|escalated\",\n      \"mitigation_type_needed\": \"proof_point|case_study|guarantee|technical_demo|reference_call|documentation|executive_sponsor\",\n      \"blocks_decision\": true\n    }\n  ],\n  \"risk_count\": 0,\n  \"unaddressed_risk_count\": 0,\n  \"dominant_category\": \"the category with the most risks\",\n  \"deal_risk_level\": \"low|medium|high|critical\",\n  \"implicit_risks\": [\n    {\n      \"summary\": \"Risk the prospect hinted at but did not state directly\",\n      \"evidence_quote\": \"Quote suggesting the unstated concern\",\n      \"category\": \"financial|technical|organizational|timeline|vendor\",\n      \"probe_question\": \"Question to ask in follow-up to surface this risk explicitly\"\n    }\n  ],\n  \"risk_discovery_gaps\": [\"Risk categories NOT discussed that should be probed in follow-up\"],\n  \"seller_risk_handling_quality\": \"strong|adequate|weak\",\n  \"next_risks_to_probe\": [\"Specific risks to explore in the next conversation\"]\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- Each risk has severity and likelihood between 1-10
- `risk_score` = `severity * likelihood` (compute if LLM did not)
- `category` is one of the five permitted categories
- `emotional_tone` is one of the five permitted values
- All `concern_quote` values are actual text from the transcript (spot-check at least 1)
- `risk_count` matches the length of the `risks` array
- `unaddressed_risk_count` matches risks where `response_effectiveness` is "unaddressed"
- `deal_risk_level` is consistent: critical if any risk has risk_score >= 80, high if >= 50, medium if >= 25, low otherwise

If validation fails, re-prompt Claude with the specific error and the original transcript.

### 4. Compute aggregate risk metrics

Calculate:
- **Total risk score:** Sum of all `risk_score` values
- **Risk density:** `risk_count / call_duration_minutes` (how fast risks surfaced)
- **Mitigation coverage:** Risks with `response_effectiveness` in ["resolved", "partially_resolved"] / `risk_count`
- **Decision-blocking risk count:** Count of risks where `blocks_decision` is true
- **Category distribution:** Count per category

### 5. Store results in CRM

Push the structured risk data to Attio via API:

```json
{
  "data": {
    "values": {
      "risk_count": [{"value": 4}],
      "unaddressed_risk_count": [{"value": 2}],
      "total_risk_score": [{"value": 186}],
      "dominant_risk_category": [{"value": "organizational"}],
      "deal_risk_level": [{"value": "high"}],
      "mitigation_coverage": [{"value": 0.5}],
      "decision_blocking_risks": [{"value": 1}],
      "risk_extraction_date": [{"value": "2026-03-30T00:00:00Z"}],
      "risk_data_json": [{"value": "{full JSON stringified}"}]
    }
  }
}
```

### 6. Log the extraction event in PostHog

Fire a PostHog event for tracking:
```json
{
  "event": "risk_extraction_completed",
  "properties": {
    "deal_id": "...",
    "risk_count": 4,
    "unaddressed_risk_count": 2,
    "total_risk_score": 186,
    "dominant_risk_category": "organizational",
    "deal_risk_level": "high",
    "mitigation_coverage": 0.5,
    "decision_blocking_risks": 1,
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `risk_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 100 words):** Likely not a substantive call. Skip extraction and log reason.
- **No risks detected:** Valid result -- the prospect may have no concerns, or they were not surfaced. Log `risk_count: 0`. Flag for follow-up probing -- zero risks in a sales conversation usually means they were not asked about, not that they do not exist.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds, max 3 retries.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Built-in deal intelligence layers |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Bundled with ZoomInfo data |
| Manual review | Human reviews recording with template | Fallback when automation fails |
