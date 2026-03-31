---
name: stakeholder-sentiment-extraction
description: Extract per-stakeholder sentiment, priorities, and concerns from discovery call transcripts using Claude API
tool: Anthropic
product: Claude API
difficulty: Config
---

# Stakeholder Sentiment Extraction

Analyze discovery call transcripts to extract each stakeholder's individual sentiment, priorities, concerns, and level of support for the proposed solution. Produces a structured per-stakeholder assessment from a single call or across multiple calls.

## Prerequisites

- Anthropic API key from console.anthropic.com
- Call transcript from Fireflies (via `fireflies-transcription` fundamental)
- Stakeholder role classifications (from `stakeholder-role-classification` fundamental)
- Deal context from Attio (deal stage, known contacts)

## Steps

### 1. Retrieve the transcript

Use the Fireflies API to fetch the full transcript with speaker labels:

```graphql
query {
  transcript(id: "{transcript_id}") {
    id
    title
    sentences {
      speaker_name
      text
      start_time
      end_time
    }
  }
}
```

Group sentences by speaker. If speaker names are not correctly labeled, use title/role context to match speakers to known contacts.

### 2. Call Claude API for per-stakeholder extraction

```
POST https://api.anthropic.com/v1/messages
Headers: x-api-key: {ANTHROPIC_API_KEY}, anthropic-version: 2023-06-01
Body: {
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "temperature": 0.2,
  "messages": [{"role": "user", "content": "TRANSCRIPT:\n{full_transcript}\n\nSTAKEHOLDER MAP:\n{name_1}: {title_1}, {role_1}\n{name_2}: {title_2}, {role_2}\n...\n\nFor EACH stakeholder who spoke in this call, extract:\n1. SENTIMENT: Positive, Neutral, Cautious, Negative, or Hostile toward the proposed solution\n2. SUPPORT_LEVEL: Champion (actively advocates), Supporter (positive but passive), Neutral, Skeptic (has concerns), Blocker (actively resists)\n3. TOP_PRIORITIES: 1-3 things this stakeholder cares most about (ranked by how much time they spent on each)\n4. CONCERNS: Specific objections, worries, or risks they raised (with direct quotes)\n5. QUESTIONS_ASKED: Key questions they asked (verbatim)\n6. DECISION_CRITERIA: What would need to be true for this stakeholder to say yes\n7. ENGAGEMENT_LEVEL: High (asked many questions, leaned in), Medium (participated when prompted), Low (quiet, checked out)\n8. RELATIONSHIP_TO_OTHERS: Any dynamics observed between stakeholders (agreements, disagreements, deference)\n9. KEY_QUOTE: The single most revealing thing this stakeholder said (verbatim)\n\nAlso extract:\n- CONSENSUS_AREAS: Topics where all stakeholders agreed\n- CONFLICT_AREAS: Topics where stakeholders disagreed or had competing priorities\n- UNRESOLVED: Questions or concerns that were raised but not addressed\n\nReturn as JSON:\n{\n  \"stakeholders\": [{\"name\": \"...\", \"sentiment\": \"...\", \"support_level\": \"...\", \"top_priorities\": [...], \"concerns\": [...], \"questions_asked\": [...], \"decision_criteria\": [...], \"engagement_level\": \"...\", \"relationship_notes\": \"...\", \"key_quote\": \"...\"}],\n  \"consensus_areas\": [...],\n  \"conflict_areas\": [...],\n  \"unresolved\": [...]\n}"}]
}
```

### 3. Parse and validate

Extract the JSON response. Validate:
- Every stakeholder from the map who spoke is represented
- Sentiments are one of the 5 defined levels
- Key quotes are actual verbatim excerpts from the transcript (spot-check 2-3)
- Conflict areas match actual disagreements in the transcript

### 4. Store in CRM

Push per-stakeholder sentiment to Attio using `attio-custom-attributes`:

```json
{
  "data": {
    "values": {
      "stakeholder_sentiment": [{"option": "{sentiment}"}],
      "stakeholder_support_level": [{"option": "{support_level}"}],
      "stakeholder_priorities": [{"value": "{priorities_json}"}],
      "stakeholder_concerns": [{"value": "{concerns_json}"}],
      "engagement_level": [{"option": "{engagement_level}"}]
    }
  }
}
```

Store the full extraction as an Attio note on the deal with tag `stakeholder-sentiment`.

### 5. Track sentiment changes over time

When extracting sentiment from subsequent calls, compare to prior extractions:
- Sentiment improved: positive signal, the stakeholder is warming
- Sentiment degraded: risk signal, something went wrong since last interaction
- New concern raised: flag for follow-up
- Prior concern resolved: remove from active risk list

Log changes as PostHog events: `stakeholder_sentiment_changed` with properties `{stakeholder_role, old_sentiment, new_sentiment, deal_id}`.

## Via Gong

If using Gong instead of Fireflies:
1. Use `gong-call-recording` to retrieve the transcript
2. Gong provides its own speaker identification and key topic detection
3. Use the same Claude API prompt above with Gong's transcript format

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Anthropic Claude | Messages API | Best for nuanced multi-stakeholder extraction |
| OpenAI GPT-4 | Chat Completions API | Good alternative |
| Gong | Native deal intelligence | Tracks stakeholder engagement automatically |
| Chorus.ai (ZoomInfo) | Call intelligence | Similar native stakeholder tracking |
| Fireflies + Claude | Transcription + API | Most flexible, works with any video platform |

## Error Handling

- **Speakers not identified**: If the transcript does not label speakers, use Claude to infer speakers from context (title mentions, voice patterns described, topic expertise). Accuracy drops to ~70% without labels.
- **Large group calls (6+ participants)**: Some stakeholders may barely speak. Flag anyone with <5% of speaking time as `engagement_level: Low` and note that sentiment assessment has low confidence.
- **Conflicting signals**: A stakeholder who asks tough questions but then says "this looks promising" is likely a Cautious Supporter, not a Blocker. Use the overall arc of the conversation, not isolated quotes.
- **API token limits**: For calls >90 minutes, split the transcript into 30-minute chunks and run extraction per chunk, then merge results with a final consolidation call.
