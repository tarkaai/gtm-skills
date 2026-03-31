---
name: gong-engagement-analysis
description: Extract engagement signals from Gong demo recordings to measure prospect attention, emotional connection, and storytelling effectiveness
tool: Gong
difficulty: Advanced
---

# Gong Engagement Analysis

Use the Gong API to analyze recorded demo calls for engagement signals: prospect questions, verbal affirmations, story connection moments, and periods of sustained attention. Produces a structured engagement scorecard per demo.

## Prerequisites

- Gong account with API access
- Demo calls recorded in Gong
- Gong API key (Settings > API > Generate API Key)

## Steps

### 1. Retrieve demo call data

Fetch the call recording and transcript for a specific demo:

```
GET https://api.gong.io/v2/calls/{call_id}/transcript
Authorization: Basic {base64(access_key:access_key_secret)}
Content-Type: application/json
```

Also fetch the call metadata:

```
GET https://api.gong.io/v2/calls/{call_id}
Authorization: Basic {base64(access_key:access_key_secret)}
```

Response includes: `duration`, `speakers[]`, `media` (recording URL), `collaboration.notes`.

### 2. Retrieve Gong's built-in analytics

Gong auto-computes several engagement signals. Fetch them:

```
GET https://api.gong.io/v2/calls/{call_id}/detailed
Authorization: Basic {base64(access_key:access_key_secret)}
```

Extract from the response:
- `talkRatio`: % of time each speaker talked. In a good demo, prospect should talk 30-50%.
- `longestMonologue`: if the rep talked for 5+ minutes uninterrupted, engagement likely dropped.
- `questionsAsked`: count of questions the prospect asked. More questions = more engaged.
- `nextStepsDiscussed`: boolean — did the call end with a clear next step.
- `topicsDiscussed`: Gong-detected topics (pricing, competitors, implementation, etc.).

### 3. Extract storytelling-specific engagement signals

Send the transcript to Claude for deeper narrative engagement analysis:

```
POST https://api.anthropic.com/v1/messages

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "Analyze this demo call transcript for storytelling engagement signals.\n\nTranscript:\n{transcript_text}\n\nExtract:\n1. story_connection_moments: Times when the prospect explicitly related to the customer story ('We have the same problem', 'That sounds like us', 'How did they...'). Include the exact quote and timestamp.\n2. prospect_questions_about_story: Questions the prospect asked about the customer story (wanting more detail = high engagement).\n3. emotional_indicators: Verbal signals of emotional engagement (laughter, surprise, concern, excitement). Include quote and timestamp.\n4. disengagement_signals: Long silences after story elements, topic changes away from the story, or multitasking indicators.\n5. feature_request_triggers: Moments where the story prompted the prospect to ask about specific features or capabilities.\n\nReturn JSON:\n{\n  \"engagement_score\": 0-100,\n  \"story_connection_moments\": [{\"timestamp\": \"12:34\", \"quote\": \"...\", \"signal_strength\": \"strong|moderate|weak\"}],\n  \"prospect_story_questions\": [{\"timestamp\": \"15:20\", \"question\": \"...\"}],\n  \"emotional_indicators\": [{\"timestamp\": \"18:45\", \"type\": \"excitement\", \"quote\": \"...\"}],\n  \"disengagement_signals\": [{\"timestamp\": \"22:10\", \"type\": \"silence\", \"duration_seconds\": 8}],\n  \"feature_triggers\": [{\"timestamp\": \"14:00\", \"feature_asked\": \"...\", \"triggered_by_story_element\": \"...\"}],\n  \"narrative_effectiveness\": {\n    \"story_held_attention\": true,\n    \"prospect_saw_themselves\": true,\n    \"emotional_peak_landed\": true,\n    \"closing_bridge_prompted_action\": false\n  }\n}"
  }]
}
```

### 4. Build the engagement scorecard

Combine Gong metrics + Claude analysis into a single scorecard:

| Signal | Weight | Score |
|--------|--------|-------|
| Prospect talk ratio (30-50% optimal) | 20% | 0-100 |
| Questions asked (5+ = high engagement) | 20% | 0-100 |
| Story connection moments (2+ = strong) | 25% | 0-100 |
| Emotional indicators (1+ = resonance) | 15% | 0-100 |
| Next steps committed | 10% | 0 or 100 |
| No disengagement signals | 10% | 0-100 |

Weighted total = engagement score for this demo.

### 5. Store and track

Store the scorecard as an Attio note on the deal. Fire PostHog event:

```json
{
  "event": "demo_engagement_scored",
  "properties": {
    "deal_id": "...",
    "call_id": "...",
    "engagement_score": 78,
    "story_connection_count": 3,
    "prospect_questions": 7,
    "emotional_peaks": 2,
    "disengagement_signals": 1,
    "next_steps_committed": true,
    "story_used": "story-001"
  }
}
```

## Error Handling

- **No Gong recording available:** Fall back to manual engagement scoring via post-demo survey. Log `scoring_method: manual`.
- **Transcript too short (<5 minutes):** Skip narrative analysis, flag as incomplete demo.
- **API rate limits:** Gong limits to 600 calls/minute. Batch requests for bulk analysis.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Gong | REST API + Claude analysis | Best for recorded demos |
| Fireflies | GraphQL API + Claude analysis | Lower cost alternative |
| Chorus (ZoomInfo) | API + Claude analysis | Alternative conversation intelligence |
| Clari Copilot | API + Claude analysis | Alternative |
| Manual scoring | Post-demo checklist | Fallback when no recording available |
