---
name: call-transcript-competitor-extraction
description: Extract competitor mentions, evaluation stages, decision criteria, and competitive sentiment from sales call transcripts using LLM analysis
tool: Fireflies + Anthropic
difficulty: Advanced
---

# Extract Competitive Situation from Call Transcripts

Parse qualification and discovery call transcripts to identify which competitors the prospect is evaluating, how far along each evaluation is, what decision criteria they are using, and how they feel about each alternative. Returns structured competitive situation data for battlecard routing and win strategy selection.

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

### 2. Run competitive situation extraction via Claude API

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
    "content": "Analyze this sales call transcript and extract all competitive intelligence. Identify every competitor or alternative the prospect mentions, their evaluation stage with each, and how they are making their decision.\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"competitors_identified\": [\n    {\n      \"name\": \"Competitor name as stated by prospect\",\n      \"type\": \"direct_competitor|indirect_alternative|status_quo|build_in_house\",\n      \"evaluation_stage\": \"awareness|research|demo_scheduled|demo_completed|proposal_received|finalist|incumbent\",\n      \"prospect_sentiment\": \"positive|neutral|negative|mixed\",\n      \"sentiment_evidence\": \"Exact quote showing their feeling about this competitor\",\n      \"specific_features_compared\": [\"Feature or capability they mentioned comparing\"],\n      \"pricing_mentioned\": null or \"Any pricing info disclosed about this competitor\",\n      \"strengths_cited\": [\"What the prospect says this competitor does well\"],\n      \"gaps_cited\": [\"What the prospect says this competitor lacks or does poorly\"],\n      \"relationship_depth\": \"cold|warm|existing_customer|former_customer\"\n    }\n  ],\n  \"decision_criteria\": [\n    {\n      \"criterion\": \"What matters to them\",\n      \"priority\": \"must_have|important|nice_to_have\",\n      \"evidence_quote\": \"Exact quote showing this criterion matters\"\n    }\n  ],\n  \"decision_process\": {\n    \"timeline\": \"When they expect to decide (exact quote or null)\",\n    \"stakeholders_mentioned\": [\"Names or roles of people involved in the decision\"],\n    \"evaluation_method\": \"formal_rfp|informal_comparison|single_vendor|committee_review|champion_driven|unknown\",\n    \"budget_context\": \"Any budget info that affects competitive positioning (quote or null)\"\n  },\n  \"competitive_discovery_quality\": {\n    \"questions_asked\": [\"Competitive discovery questions the seller asked\"],\n    \"questions_missed\": [\"Questions the seller should have asked but did not\"],\n    \"seller_score\": \"strong|adequate|weak\"\n  },\n  \"status_quo_analysis\": {\n    \"current_solution\": \"What they use today (null if not mentioned)\",\n    \"pain_with_current\": [\"Problems with their current approach\"],\n    \"switching_barriers\": [\"Reasons they might stay with current solution\"],\n    \"do_nothing_risk\": \"low|medium|high — likelihood they choose to do nothing\"\n  },\n  \"recommended_competitive_strategy\": \"displacement|greenfield|co-existence|land_and_expand\",\n  \"deal_competitive_risk\": \"low|medium|high|critical\"\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- Each competitor has a valid `type` and `evaluation_stage` from the permitted values
- `prospect_sentiment` is one of the four permitted values
- `sentiment_evidence` quotes are actual text from the transcript (spot-check at least 1)
- `decision_criteria` has at least 1 entry (if none found, flag the call as needing better discovery)
- `deal_competitive_risk` is consistent with competitor count and evaluation stages

If validation fails, re-prompt Claude with the specific error and the original transcript.

### 4. Enrich with CRM deal context

Pull the deal record from Attio and cross-reference:
- Are the competitors mentioned already tracked in the Competitors object?
- Does this deal already have competitive data from prior calls?
- If a new competitor is identified, create or update the Competitors record

### 5. Store results in CRM

Push the structured competitive situation to Attio via API:

```json
{
  "data": {
    "values": {
      "competitors_evaluated": [{"value": "Competitor A, Competitor B"}],
      "competitor_count": [{"value": 2}],
      "primary_competitor": [{"value": "Competitor A"}],
      "competitive_risk_level": [{"value": "medium"}],
      "decision_criteria_json": [{"value": "{stringified decision_criteria}"}],
      "competitive_situation_json": [{"value": "{full JSON stringified}"}],
      "evaluation_method": [{"value": "informal_comparison"}],
      "competitive_extraction_date": [{"value": "2026-03-30T00:00:00Z"}]
    }
  }
}
```

### 6. Log the extraction event in PostHog

Fire a PostHog event for tracking:
```json
{
  "event": "competitive_situation_extracted",
  "properties": {
    "deal_id": "...",
    "competitor_count": 2,
    "competitors_named": ["Competitor A", "Competitor B"],
    "competitive_risk": "medium",
    "evaluation_method": "informal_comparison",
    "do_nothing_risk": "medium",
    "seller_discovery_quality": "adequate",
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `competitive_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 50 words):** Likely not a substantive call. Skip extraction and log reason.
- **No competitors detected:** Valid result — the prospect may not be evaluating alternatives. Log `competitor_count: 0` and set `status_quo_analysis.do_nothing_risk` to high (they may default to doing nothing).
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds, max 3 retries.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction with structured output |
| Gong | `GET /v2/calls/{call_id}/transcript` + Deal Intelligence | Built-in competitor tracking and deal intelligence |
| Chorus (ZoomInfo) | REST API + Anthropic API | Bundled with ZoomInfo enrichment data |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Clari | Deal intelligence API | Revenue operations platform with competitive signals |
| Manual review | Human reviews recording with competitive discovery template | Fallback for high-stakes deals |
