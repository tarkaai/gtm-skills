---
name: call-transcript-timing-extraction
description: Extract urgency level, buying timeline, and timing triggers from call transcripts using LLM analysis
category: Discovery
tools:
  - Fireflies
  - Anthropic
fundamentals:
  - fireflies-transcription
  - anthropic-api-patterns
---

# Extract Timing Signals from Call Transcripts

Parse meeting transcripts to identify urgency drivers, buying timeline, and timing triggers. Returns structured timeline categorization and confidence scores per prospect.

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

If using Chorus.ai: `GET /api/v1/calls/{call_id}` with API key header.

### 2. Send to Claude for timing extraction

```
POST https://api.anthropic.com/v1/messages
Authorization: x-api-key {ANTHROPIC_API_KEY}
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Analyze this sales call transcript for timing and urgency signals. Extract:\n\n1. **Timeline Category**: Classify as one of:\n   - Immediate (0-30 days): prospect has a hard deadline, executive mandate, or urgent pain\n   - Near-term (1-3 months): clear project planned, budget allocated, team assigned\n   - Medium-term (3-6 months): interest confirmed but dependencies exist (budget cycle, other projects, org changes)\n   - Long-term (6+ months): early research, no concrete plan, exploring options\n\n2. **Urgency Drivers**: List every timing trigger mentioned:\n   - Hard deadlines (contract expiration, regulatory, fiscal year end)\n   - Executive mandates (new CxO directive, board pressure)\n   - Competitive pressure (competitor adopted similar solution)\n   - Pain escalation (problem getting worse, team morale, revenue impact)\n   - Budget window (use-it-or-lose-it budget, new fiscal year allocation)\n   - Seasonal/cyclical (hiring season, product launch, event-driven)\n\n3. **Timeline Confidence**: Rate 1-5 how confident you are in the timeline assessment:\n   - 5: Prospect stated explicit date with hard deadline\n   - 4: Prospect gave a range tied to a real event\n   - 3: Prospect gave a range but no triggering event\n   - 2: Prospect was vague ('sometime this year')\n   - 1: No timeline discussed or prospect actively avoided the question\n\n4. **Consequence of Inaction**: What happens if the prospect does NOT solve this by their stated timeline? Quote their words if possible.\n\n5. **Slippage Risk**: Rate High/Medium/Low probability the timeline will slip. Indicators:\n   - High: No budget confirmed, no executive sponsor, 'nice to have' language\n   - Medium: Budget likely but not approved, sponsor identified but not committed\n   - Low: Budget approved, exec sponsor active, hard external deadline\n\n6. **Best Timing Questions**: Which questions from the call yielded the most useful timing information? Quote the question and note what signal it produced.\n\nReturn as JSON:\n```json\n{\n  \"timeline_category\": \"Immediate|Near-term|Medium-term|Long-term\",\n  \"target_date\": \"YYYY-MM-DD or null\",\n  \"urgency_drivers\": [{\"type\": \"...\", \"detail\": \"...\", \"quote\": \"...\"}],\n  \"timeline_confidence\": 1-5,\n  \"consequence_of_inaction\": \"...\",\n  \"slippage_risk\": \"High|Medium|Low\",\n  \"slippage_indicators\": [\"...\"],\n  \"effective_questions\": [{\"question\": \"...\", \"signal_produced\": \"...\"}],\n  \"recommended_follow_up_cadence\": \"daily|2-3x_week|weekly|biweekly|monthly\",\n  \"reasoning\": \"...\"\n}\n```\n\nTranscript:\n{transcript_text}"
  }]
}
```

### 3. Parse the response

Extract the JSON from Claude's response. Handle edge cases:
- If `timeline_confidence` <= 2, flag the deal for a follow-up call specifically targeting timeline
- If `slippage_risk` is "High", add a note recommending multi-stakeholder timeline validation
- If no `target_date` is provided, estimate one from `timeline_category` relative to today

### 4. Error handling

| Error | Cause | Resolution |
|-------|-------|------------|
| 400 Bad Request | Transcript too long | Truncate to last 60 minutes or summarize first |
| 429 Rate Limited | Too many concurrent extractions | Queue with exponential backoff (1s, 2s, 4s) |
| Empty urgency_drivers | Prospect avoided timing discussion | Flag for explicit timing follow-up |
| timeline_confidence = 1 | No timeline signal in call | Schedule a dedicated timing qualification call |

### 5. Multi-tool support

| Tool | Transcript Source | API Endpoint |
|------|------------------|--------------|
| Fireflies | Auto-transcribed meetings | GraphQL: `transcript(id)` |
| Gong | Sales call recordings | `GET /v2/calls/{id}/transcript` |
| Chorus.ai | Conversation intelligence | `GET /api/v1/calls/{id}` |
| Otter.ai | Meeting notes | `GET /api/v1/speeches/{id}` |
| Fathom | AI meeting assistant | Export via Zapier webhook |

| LLM Provider | Model | Endpoint |
|--------------|-------|----------|
| Anthropic | claude-sonnet-4-20250514 | `POST /v1/messages` |
| OpenAI | gpt-4o | `POST /v1/chat/completions` |
| Google | gemini-2.0-flash | `POST /v1/models/gemini-2.0-flash:generateContent` |
