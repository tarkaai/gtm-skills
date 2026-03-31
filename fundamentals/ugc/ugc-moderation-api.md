---
name: ugc-moderation-api
description: Score and classify user-generated content for quality, relevance, and brand safety using AI
tool: Anthropic
product: Claude API
difficulty: Config
---

# UGC Moderation API

Use an LLM to evaluate submitted user-generated content for quality, relevance, brand safety, and amplification potential. Returns a structured moderation verdict that the automation pipeline uses to route content.

## API Call

**Anthropic Messages API:**

```
POST https://api.anthropic.com/v1/messages
Authorization: Bearer {ANTHROPIC_API_KEY}
Content-Type: application/json
```

**Request body:**

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "You are a UGC moderation agent for [PRODUCT_NAME]. Evaluate this user-submitted content and return a JSON object.\n\nSubmission:\n- Title: {title}\n- Type: {content_type}\n- Content: {content_body_or_url_summary}\n- Author tier: {submitter_tier}\n- Author power user score: {power_user_score}\n\nEvaluate on these dimensions (score 1-5 each):\n1. Quality: Is the content well-written/produced? Does it provide real value to the reader?\n2. Relevance: Does it clearly relate to [PRODUCT_NAME] or problems the product solves?\n3. Brand safety: Is the tone professional? Any complaints, competitor mentions, or negative framing?\n4. Amplification potential: Would sharing this on our channels drive awareness or conversions?\n5. Authenticity: Does this appear to be genuine user experience vs. fabricated or AI-generated fluff?\n\nReturn ONLY this JSON:\n{\n  \"quality_score\": 1-5,\n  \"relevance_score\": 1-5,\n  \"brand_safety_score\": 1-5,\n  \"amplification_score\": 1-5,\n  \"authenticity_score\": 1-5,\n  \"composite_score\": weighted_average,\n  \"verdict\": \"approve|review|reject\",\n  \"verdict_reason\": \"one sentence explaining the decision\",\n  \"suggested_channels\": [\"social\", \"blog\", \"email\", \"case_study\"],\n  \"improvement_suggestions\": \"specific feedback if score < 4 on any dimension\"\n}"
    }
  ]
}
```

**Scoring logic:**

- `composite_score` = `quality * 0.25 + relevance * 0.25 + brand_safety * 0.20 + amplification * 0.20 + authenticity * 0.10`
- `approve`: composite >= 3.5 AND brand_safety >= 3 AND authenticity >= 3
- `review`: composite >= 2.5 but fails approve criteria (human checks)
- `reject`: composite < 2.5 OR brand_safety < 2 OR authenticity < 2

**Response parsing:**

Parse the JSON from the response `content[0].text`. Handle cases where the model wraps JSON in markdown code fences by stripping them.

## n8n Integration

In the UGC processing workflow after the `ugc-submission-webhook`:

1. **HTTP Request node** — POST to the Anthropic API with the submission content
2. **JSON Parse node** — extract the moderation verdict
3. **Switch node** — route based on `verdict`:
   - `approve` -> proceed to amplification pipeline
   - `review` -> create Attio task for human review with the moderation scores
   - `reject` -> log rejection reason, send gentle thank-you to submitter

## PostHog Event

Fire `ugc_moderated` after each moderation:

```json
{
  "submission_id": "...",
  "verdict": "approve",
  "composite_score": 4.2,
  "quality_score": 4,
  "relevance_score": 5,
  "brand_safety_score": 4,
  "amplification_score": 4,
  "authenticity_score": 4,
  "processing_time_ms": 1200
}
```

## Error Handling

- API timeout (>10s): retry once, then mark as `review` for human moderation
- Rate limit (429): queue the submission and retry after the `retry-after` header duration
- Malformed response: mark as `review` for human moderation
- Cost guard: track daily API spend. If >$5/day on moderation, batch submissions and process hourly instead of real-time

## Tool Alternatives

| Tool | Purpose | Notes |
|------|---------|-------|
| Anthropic Claude | Primary moderation via Messages API | ~$3/1M input tokens (Sonnet) |
| OpenAI GPT-4o | Alternative LLM moderation | ~$2.50/1M input tokens |
| Perspective API | Toxicity/spam scoring supplement | Free tier from Google/Jigsaw |
| Hive Moderation | Visual content moderation | For video/image UGC |
| AWS Rekognition | Image moderation | For visual UGC at scale |
