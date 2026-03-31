---
name: champion-engagement-scoring
description: Use Claude to analyze champion interactions and compute an engagement health score from CRM and email data
tool: Anthropic
difficulty: Advanced
---

# Champion Engagement Scoring

Use Claude (via Anthropic API) to analyze all touchpoints with a champion contact and produce a structured engagement score that predicts whether the champion is actively advocating, passively supportive, or disengaging.

## Prerequisites

- Anthropic API key (`ANTHROPIC_API_KEY`)
- Champion interaction data collected in Attio (notes, emails, meeting transcripts)
- At least 3 interactions logged for the champion (scoring is unreliable with fewer data points)

## How It Works

The scoring model evaluates five dimensions of champion engagement:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Responsiveness | 25% | How quickly they reply, whether they initiate contact |
| Internal Advocacy | 25% | Evidence they've introduced you to colleagues, forwarded materials |
| Knowledge Depth | 20% | How well they understand your product's value prop |
| Urgency Signals | 15% | Language indicating timeline pressure or budget momentum |
| Risk Signals | 15% | Signs of disengagement, competitor mentions, role changes |

## Steps

### 1. Gather Champion Interaction Data

Pull all interaction data for the champion from Attio using the `attio-notes` fundamental:

```
GET https://api.attio.com/v2/notes?parent_object=people&parent_record_id={champion_record_id}
```

Also pull email thread data from Instantly or your email tool's API. Compile into a single interaction timeline:

```json
{
  "champion": {
    "name": "...",
    "title": "...",
    "company": "...",
    "champion_since": "YYYY-MM-DD"
  },
  "interactions": [
    {
      "date": "YYYY-MM-DD",
      "type": "email | meeting | linkedin | call",
      "direction": "inbound | outbound",
      "summary": "...",
      "response_time_hours": null | number,
      "sentiment": "positive | neutral | negative"
    }
  ]
}
```

### 2. Send to Claude for Scoring

Using the `anthropic-api-patterns` fundamental, send the interaction data to Claude:

```
POST https://api.anthropic.com/v1/messages

Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  anthropic-version: 2023-06-01
  Content-Type: application/json

Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [{
    "role": "user",
    "content": "You are a sales intelligence analyst scoring champion engagement. Analyze the following champion interaction history and return a structured JSON score.\n\nChampion data:\n{interaction_timeline_json}\n\nScore each dimension 0-100:\n1. Responsiveness: How quickly do they reply? Do they ever initiate contact? Score 80+ if average response <24h and they've initiated at least once.\n2. Internal Advocacy: Evidence they've introduced colleagues, forwarded materials, scheduled internal meetings. Score 80+ if they've made 2+ introductions.\n3. Knowledge Depth: Do they reference specific features, use cases, or ROI metrics? Score 80+ if they articulate value in their own words.\n4. Urgency Signals: Language about timelines, budget cycles, upcoming decisions. Score 80+ if they mention a specific decision date.\n5. Risk Signals: INVERSE score — 100 means NO risk. Deduct for: competitor mentions (-30), longer response times over time (-20), cancelled meetings (-25), role change (-15).\n\nReturn ONLY valid JSON:\n{\n  \"responsiveness\": {\"score\": N, \"evidence\": \"...\"},\n  \"internal_advocacy\": {\"score\": N, \"evidence\": \"...\"},\n  \"knowledge_depth\": {\"score\": N, \"evidence\": \"...\"},\n  \"urgency_signals\": {\"score\": N, \"evidence\": \"...\"},\n  \"risk_signals\": {\"score\": N, \"evidence\": \"...\"},\n  \"composite_score\": N,\n  \"health\": \"strong\" | \"healthy\" | \"at_risk\" | \"disengaged\",\n  \"recommended_action\": \"...\"\n}"
  }]
}
```

### 3. Parse and Store the Score

Parse Claude's JSON response. Compute composite score using weights:

```
composite = (responsiveness * 0.25) + (internal_advocacy * 0.25) + (knowledge_depth * 0.20) + (urgency_signals * 0.15) + (risk_signals * 0.15)
```

Map composite to health status:
- 75-100: Strong
- 50-74: Healthy
- 25-49: At Risk
- 0-24: Disengaged

Write the score back to Attio using `attio-custom-attributes`:

```
PATCH https://api.attio.com/v2/objects/people/records/{champion_record_id}
{
  "data": {
    "values": {
      "champion_score": [{"value": composite_score}],
      "champion_last_engaged": [{"value": "latest_interaction_date"}]
    }
  }
}
```

### 4. Handle Edge Cases

- **Fewer than 3 interactions:** Return score with a `confidence: "low"` flag. Do not auto-update champion status based on low-confidence scores.
- **All interactions are outbound:** This is a risk signal. The champion is not initiating. Add `-20` to responsiveness score.
- **Champion changed roles:** If the role change is within the same company, re-evaluate. If they left the company, set status to "Lost" immediately.

## Error Handling

- `429 RATE_LIMITED` from Anthropic: Back off exponentially. Start at 5s, double each retry, max 3 retries.
- `500` from Anthropic: Retry once after 10s. If it fails again, skip this champion and flag for manual review.
- Invalid JSON from Claude: Re-send the request with a stricter prompt. If it fails twice, extract scores manually from the text response using regex.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Anthropic Claude | Messages API | Best for nuanced interaction analysis |
| OpenAI GPT-4o | Chat Completions API | Alternative LLM, similar capability |
| Gong | Deal Intelligence API | Pre-built engagement scoring from call data |
| Clari | Revenue Intelligence API | Enterprise engagement scoring |
| Custom ML | Scikit-learn / PyTorch | Roll your own model if you have labeled training data |
