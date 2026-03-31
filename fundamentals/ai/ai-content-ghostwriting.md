---
name: ai-content-ghostwriting
description: Use an LLM API to generate social media posts in a founder's authentic voice
tool: Anthropic
product: Claude API
difficulty: Config
---

# Generate Social Posts in Founder's Voice via LLM

## Prerequisites
- Anthropic API key or OpenAI API key
- 10+ examples of the founder's existing writing (LinkedIn posts, emails, blog posts, talks)
- Defined content pillars and ICP pain points

## Why This Matters

Founder-led content must sound like the founder, not like a marketing team or an AI. This fundamental teaches you to use LLM APIs to generate drafts that capture the founder's voice, opinions, and storytelling style -- then have the founder review and edit before publishing.

## Steps

### 1. Build a voice profile document

Collect 10-20 examples of the founder's best writing. Analyze and document:

- **Sentence length**: Short and punchy? Long and flowing?
- **Vocabulary**: Technical jargon level? Casual or formal?
- **Perspective**: First person ("I") or collective ("we")?
- **Opinions**: What strong takes does the founder hold? What industry beliefs do they challenge?
- **Stories**: What personal/professional experiences do they reference?
- **Tone**: Authoritative, conversational, provocative, educational?
- **Patterns**: Do they use lists? Questions? Analogies? Data?

Create a voice profile document (500-800 words) summarizing these traits with examples.

### 2. Generate post drafts via Anthropic API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "system": "You are ghostwriting LinkedIn posts for a founder. Here is their voice profile:\n\n{VOICE_PROFILE_TEXT}\n\nHere are 5 examples of their actual posts:\n\n{EXAMPLE_POSTS}\n\nRules:\n- Write in first person as the founder\n- Match their sentence structure and vocabulary\n- Include a hook in the first line that creates curiosity or tension\n- Keep posts between 150-300 words\n- End with a question or opinion that invites comments\n- Do NOT use emojis, hashtags, or generic motivational language\n- Do NOT start with 'I'm excited to' or 'Thrilled to share'\n- Reference specific numbers, experiences, or situations -- not abstract advice",
  "messages": [
    {
      "role": "user",
      "content": "Write a LinkedIn post about {TOPIC}. The target audience is {ICP_DESCRIPTION}. The core insight is: {SPECIFIC_INSIGHT_OR_EXPERIENCE}. Make it feel like a real conversation the founder is having with their network."
    }
  ]
}
```

### 3. Generate via OpenAI API (alternative)

```
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer {OPENAI_API_KEY}
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are ghostwriting LinkedIn posts for a founder. {SAME_SYSTEM_PROMPT_AS_ABOVE}"
    },
    {
      "role": "user",
      "content": "Write a LinkedIn post about {TOPIC}. Target audience: {ICP}. Core insight: {INSIGHT}."
    }
  ],
  "max_tokens": 1024,
  "temperature": 0.8
}
```

### 4. Batch-generate a week of content

To create a full week's content in one API call:

```json
{
  "role": "user",
  "content": "Generate 5 LinkedIn posts for the coming week. Each post should cover a different content pillar:\n\n1. {PILLAR_1}: {SPECIFIC_ANGLE_OR_STORY}\n2. {PILLAR_2}: {SPECIFIC_ANGLE_OR_STORY}\n3. {PILLAR_3}: {SPECIFIC_ANGLE_OR_STORY}\n4. {PILLAR_4}: {SPECIFIC_ANGLE_OR_STORY}\n5. {PILLAR_5}: {SPECIFIC_ANGLE_OR_STORY}\n\nFor each post, provide:\n- The hook (first line)\n- The full post body\n- A suggested CTA\n- Which day of the week to publish (Tue-Sat)"
}
```

### 5. Human review loop

**Human action required:** The founder MUST review every generated draft before publishing. The review process:

1. Read the draft aloud. Does it sound like you?
2. Replace any generic phrases with specific details from your experience.
3. Strengthen the hook if it does not create enough tension or curiosity.
4. Check the CTA: does it invite a response, or is it a dead end?
5. Edit for length: cut anything that does not earn its place.

Typical flow: AI generates 80% of the draft, founder edits 20% to add authenticity and specifics. Over time, as the voice profile improves, editing time decreases.

### 6. Improve the voice profile iteratively

After each batch:
1. Note which generated posts needed the most editing and why.
2. Add new examples of the founder's actual posts (especially high-performers).
3. Update the voice profile with patterns that the AI keeps missing.
4. After 4 weeks, the AI output should require minimal editing.

## Cost Estimates

- Claude Sonnet: ~$3/million input tokens, ~$15/million output tokens. A week of 5 posts costs approximately $0.02-0.05.
- GPT-4o: ~$2.50/million input tokens, ~$10/million output tokens. Similar cost.
- At scale (daily posting for 6 months): total LLM cost is under $5/month.

## Error Handling

- **Output sounds generic**: The voice profile is too thin. Add more examples, especially posts where the founder is most opinionated or vulnerable.
- **Output is too long**: Set `max_tokens` lower (512-768) and add "Keep under 250 words" to the prompt.
- **Output uses forbidden patterns**: Add negative examples to the system prompt: "NEVER write posts that start with [bad pattern]."
- **Rate limits**: Anthropic allows 4,000 requests/minute on most plans. Batch requests to stay well under limits.
