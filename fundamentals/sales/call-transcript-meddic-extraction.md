---
name: call-transcript-meddic-extraction
description: Extract MEDDIC signals (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) from call transcripts using LLM analysis
tool: Fireflies + Anthropic
difficulty: Advanced
---

# Extract MEDDIC Signals from Call Transcripts

Parse meeting transcripts to identify and score all six MEDDIC elements. Returns structured scores per deal with supporting evidence, red flags, and gap analysis.

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

If using Chorus (ZoomInfo): `GET /api/v1/calls/{callId}/transcript` with API key.

### 2. Run MEDDIC extraction via Claude API

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
    "content": "Analyze this sales call transcript and extract MEDDIC qualification signals. MEDDIC = Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion. Return JSON only.\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"metrics\": {\n    \"score\": 0-100,\n    \"signals\": [\"exact quotes where prospect mentions measurable business outcomes, KPIs, or quantifiable impact they expect\"],\n    \"red_flags\": [\"quotes indicating vague or absent success metrics\"],\n    \"status\": \"quantified|directional|vague|absent\",\n    \"identified_metrics\": [\"specific business metrics the prospect cares about (e.g., revenue increase, cost reduction, time savings)\"]\n  },\n  \"economic_buyer\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes identifying who controls budget and final approval\"],\n    \"red_flags\": [\"quotes indicating contact is not the economic buyer and hasn't identified who is\"],\n    \"status\": \"identified_and_engaged|identified_not_engaged|unknown\",\n    \"buyer_name\": \"name if mentioned, null otherwise\",\n    \"buyer_title\": \"title if mentioned, null otherwise\",\n    \"access_path\": \"how to reach the economic buyer based on conversation\"\n  },\n  \"decision_criteria\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes revealing what criteria the prospect will use to evaluate solutions\"],\n    \"red_flags\": [\"quotes indicating they have no clear evaluation criteria or are using criteria that disadvantage us\"],\n    \"status\": \"documented|partially_known|unknown\",\n    \"criteria_list\": [\"specific decision criteria mentioned (e.g., integration with existing stack, price, implementation time, security compliance)\"]\n  },\n  \"decision_process\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes describing the steps from evaluation to purchase\"],\n    \"red_flags\": [\"quotes indicating a complex or unclear buying process\"],\n    \"status\": \"mapped|partially_mapped|unknown\",\n    \"process_steps\": [\"steps mentioned (e.g., demo, security review, procurement, legal, board approval)\"],\n    \"timeline_estimate\": \"estimated weeks/months to decision based on process\"\n  },\n  \"identify_pain\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes where prospect describes current pain, frustration, or business impact of the problem\"],\n    \"red_flags\": [\"quotes suggesting the pain is not urgent or is tolerable\"],\n    \"status\": \"acute|moderate|mild|absent\",\n    \"pain_points\": [\"specific pain points articulated\"],\n    \"business_impact\": \"quantified business impact of the pain if mentioned\"\n  },\n  \"champion\": {\n    \"score\": 0-100,\n    \"signals\": [\"quotes indicating the contact (or someone else) will advocate internally for this solution\"],\n    \"red_flags\": [\"quotes indicating no internal advocate or passive interest only\"],\n    \"status\": \"active_champion|potential_champion|no_champion\",\n    \"champion_name\": \"name if identified, null otherwise\",\n    \"champion_influence\": \"their level of influence in the organization based on conversation\"\n  },\n  \"composite_score\": 0-100,\n  \"qualification_verdict\": \"qualified|needs_work|disqualified\",\n  \"weakest_elements\": [\"the 1-2 MEDDIC elements with lowest scores\"],\n  \"next_steps\": [\"specific recommended actions to strengthen the weakest elements\"]\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- All six MEDDIC elements have scores between 0-100
- `composite_score` equals the weighted average: Metrics (15%) + Economic Buyer (20%) + Decision Criteria (15%) + Decision Process (15%) + Identify Pain (20%) + Champion (15%)
- `qualification_verdict` matches: qualified (composite >= 70), needs_work (40-69), disqualified (< 40)
- `weakest_elements` contains the 1-2 elements with the lowest scores

If validation fails, re-prompt with the error and ask for corrected JSON.

### 4. Store results in CRM

Push the structured MEDDIC scores to Attio via MCP or API:

```json
{
  "data": {
    "values": {
      "meddic_metrics_score": [{"value": 85}],
      "meddic_economic_buyer_score": [{"value": 40}],
      "meddic_decision_criteria_score": [{"value": 70}],
      "meddic_decision_process_score": [{"value": 55}],
      "meddic_identify_pain_score": [{"value": 90}],
      "meddic_champion_score": [{"value": 60}],
      "meddic_composite_score": [{"value": 65}],
      "meddic_verdict": [{"value": "needs_work"}],
      "meddic_last_assessed": [{"value": "2026-03-30T00:00:00Z"}],
      "meddic_assessment_source": [{"value": "Discovery Call"}]
    }
  }
}
```

### 5. Log the extraction event

Fire a PostHog event for tracking:
```json
{
  "event": "meddic_extraction_completed",
  "properties": {
    "deal_id": "...",
    "composite_score": 65,
    "verdict": "needs_work",
    "source": "call_transcript",
    "call_id": "...",
    "weakest_elements": ["economic_buyer", "decision_process"]
  }
}
```

## Scoring Weights

MEDDIC element weights reflect enterprise deal dynamics:

| Element | Weight | Rationale |
|---------|--------|-----------|
| Metrics | 15% | Quantified outcomes anchor the business case |
| Economic Buyer | 20% | Deals stall without access to the person who signs |
| Decision Criteria | 15% | Understanding criteria lets you shape the evaluation |
| Decision Process | 15% | Mapped process = predictable timeline |
| Identify Pain | 20% | No pain = no urgency = no deal |
| Champion | 15% | Internal advocate drives the deal through bureaucracy |

## Error Handling

- **No transcript available:** Skip extraction, log `meddic_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 50 words):** Likely a no-show or quick cancel. Skip extraction.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds.
- **Ambiguous signals:** If the LLM returns scores of exactly 50 for 3+ elements, the transcript may lack substance. Flag for human review.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Better call analytics built-in, native MEDDIC scoring in Gong Engage |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Owned by ZoomInfo, good for large teams |
| Clari + Claude | REST API + Anthropic API | Strong revenue intelligence integration |
| Manual review | Human listens to recording | Fallback when automation fails |
