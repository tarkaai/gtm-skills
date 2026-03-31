---
name: talk-proposal-generation
description: Use Claude to generate conference talk proposals tailored to specific CFP requirements and audience
tool: Anthropic
product: Claude API
difficulty: Config
---

# Talk Proposal Generation

Generate conference talk proposals customized to a specific CFP's audience, topics, and format requirements. Each proposal includes title, abstract, outline, takeaways, and speaker positioning.

## Authentication

- Anthropic API key (`ANTHROPIC_API_KEY` environment variable)

## API Call

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  anthropic-version: 2023-06-01
  content-type: application/json
```

## Request Body

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "system": "You are an expert conference speaker who has had 50+ talks accepted at developer conferences. You write proposals that reviewers love: specific, benefit-driven, no buzzwords, no product pitches. Every proposal teaches something the audience can use immediately.",
  "messages": [
    {
      "role": "user",
      "content": "Write a talk proposal for the following CFP:\n\nConference: {conference_name}\nAudience: {audience_description}\nAccepted topics/tracks: {topics}\nTalk format: {format} ({duration} minutes)\nAccepts first-time speakers: {yes_no}\n\nSpeaker context:\n- Company: {company}\n- Expertise: {expertise_areas}\n- Unique angle: {what_makes_your_perspective_unique}\n- Previous talks: {previous_talk_titles_or_none}\n\nContent pillars to draw from:\n{content_pillars}\n\nReturn a JSON object with these fields:\n1. title (under 80 characters, specific and benefit-driven)\n2. abstract (200-300 words: open with audience pain, describe what they learn, promise concrete takeaways, end with why this matters now)\n3. outline (array of 5-7 section descriptions, one per talk section)\n4. key_takeaways (array of 3 specific things the audience leaves with)\n5. target_audience (who should attend and prerequisites)\n6. why_me (2-3 sentences on what unique experience qualifies this speaker)\n\nRules:\n- No product pitches in the abstract. Mention the product only as one tool among several.\n- Use specific numbers: 'reduced latency from 2s to 200ms' not 'significantly improved performance'\n- Reference the conference's specific audience and topics\n- If the speaker has no previous talks, lean into practitioner credibility instead"
    }
  ]
}
```

## Response Format

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"title\": \"...\", \"abstract\": \"...\", \"outline\": [...], \"key_takeaways\": [...], \"target_audience\": \"...\", \"why_me\": \"...\"}"
    }
  ]
}
```

Parse the `text` field as JSON. If Claude returns markdown-wrapped JSON, strip the code fences before parsing.

## Batch Generation

To generate multiple proposal variants for the same CFP (recommended for A/B testing proposal styles):

1. Run the API call 3 times with the same input
2. Score each variant on: specificity (does it use numbers?), audience alignment (does it reference the conference?), and novelty (would a reviewer remember this?)
3. Submit the highest-scoring variant

## Error Handling

- If the response exceeds the abstract word limit, re-prompt with: "The abstract is {word_count} words. Tighten it to 200-300 words without losing specificity."
- If the title exceeds 80 characters, re-prompt: "Shorten the title to under 80 characters while keeping it specific."
- Rate limit: Anthropic API allows ~60 requests/minute on standard tier. Batch proposals with 1-second delays between calls.
- If model returns refusal (unlikely for this use case), retry with slightly rephrased prompt.

## Cost Estimate

- ~2,000 tokens output per proposal at ~$0.015/1K output tokens (Sonnet) = ~$0.03 per proposal
- Generating 3 variants per CFP = ~$0.09 per CFP
- 20 CFPs per quarter = ~$1.80/quarter
