---
name: ai-guest-post-drafting
description: Generate guest article drafts via Anthropic API tailored to a target blog's style, audience, and editorial guidelines
tool: Anthropic Claude API
difficulty: Config
---

# AI Guest Post Drafting

Generate high-quality guest article drafts using the Anthropic Claude API, customized for each target blog's editorial style, audience, and topic requirements. Each draft includes strategic backlink placement that provides genuine value to readers rather than forced promotion.

## Prerequisites

- Anthropic API key (`ANTHROPIC_API_KEY`)
- Target blog analysis: 3-5 recent articles from the blog, their editorial guidelines, audience description
- Company positioning: product description, key differentiators, target landing pages for backlinks
- Author bio and credentials

## Core Operation: Generate Guest Article Draft

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "system": "You are writing a guest article for publication on {{blog_name}}. Your task is to write an article that:\n\n1. Matches the editorial voice and style of this blog. Here are 3 example articles from the blog:\n\n{{example_article_1_title}}: {{example_article_1_excerpt_500_words}}\n{{example_article_2_title}}: {{example_article_2_excerpt_500_words}}\n{{example_article_3_title}}: {{example_article_3_excerpt_500_words}}\n\n2. Follows the blog's editorial guidelines:\n{{editorial_guidelines}}\n\n3. Provides genuinely useful, actionable content for the blog's audience: {{audience_description}}\n\n4. Naturally incorporates {{backlink_count}} contextual backlinks to these URLs where they add value:\n{{backlink_url_1}}: {{backlink_context_1}}\n{{backlink_url_2}}: {{backlink_context_2}}\n\nRules:\n- Write in the author's voice as described: {{author_voice_notes}}\n- Target {{word_count}} words (typically 1200-2000)\n- Use the blog's heading style and formatting conventions\n- Backlinks must appear as natural references that help the reader, NOT promotional plugs\n- Include original insights, data, or frameworks the reader cannot find elsewhere\n- Do NOT mention the author's company in the first 3 paragraphs\n- Structure: compelling intro hook -> problem framing -> actionable solution steps -> conclusion with takeaway\n- Include a suggested author bio (2-3 sentences with one link to author's site)",
  "messages": [
    {
      "role": "user",
      "content": "Write a guest article titled: {{article_title}}\n\nTopic: {{topic_description}}\n\nKey points to cover:\n{{key_point_1}}\n{{key_point_2}}\n{{key_point_3}}\n\nUnique angle/data the author brings: {{unique_angle}}"
    }
  ]
}
```

## Batch Generation: Multiple Pitches

To generate article drafts for multiple accepted pitches in one session:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 8192,
  "messages": [
    {
      "role": "user",
      "content": "Generate 3 guest article drafts for different publications:\n\n---\nArticle 1: {{blog_1_name}}\nTitle: {{title_1}}\nGuidelines: {{guidelines_1}}\nTarget word count: {{wc_1}}\nBacklink URLs: {{urls_1}}\n\n---\nArticle 2: {{blog_2_name}}\nTitle: {{title_2}}\nGuidelines: {{guidelines_2}}\nTarget word count: {{wc_2}}\nBacklink URLs: {{urls_2}}\n\n---\nArticle 3: {{blog_3_name}}\nTitle: {{title_3}}\nGuidelines: {{guidelines_3}}\nTarget word count: {{wc_3}}\nBacklink URLs: {{urls_3}}\n\nFor each article, produce the full draft with headings, body, and author bio."
    }
  ]
}
```

## Pitch Angle Generation

Generate pitch angles before outreach:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2048,
  "system": "You are generating guest post pitch ideas for {{author_name}}, {{author_role}} at {{company}}. The author's expertise areas: {{expertise}}. Generate pitches that would appeal to editors because they offer unique value their readers cannot get elsewhere.",
  "messages": [
    {
      "role": "user",
      "content": "Generate 5 guest post pitch ideas for {{blog_name}}.\n\nBlog audience: {{audience}}\nRecent popular topics on this blog: {{recent_topics}}\nContent gaps (topics not yet covered): {{gaps}}\n\nFor each pitch provide:\n1. Article title\n2. One-paragraph pitch summary\n3. 3 key takeaways for the reader\n4. Which backlink URL fits naturally\n5. Why this pitch would appeal to this blog's editor"
    }
  ]
}
```

## Editorial Review Prompt

After generating a draft, run a quality check:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2048,
  "messages": [
    {
      "role": "user",
      "content": "Review this guest article draft for publication readiness:\n\n{{draft_text}}\n\nEvaluate against:\n1. Does it match the target blog's voice? (Blog examples: {{blog_examples}})\n2. Are backlinks placed naturally, or do they feel forced?\n3. Is the content genuinely useful or just thinly veiled promotion?\n4. Would an editor accept this without major revisions?\n5. Is the word count within ±10% of target ({{target_wc}})?\n\nReturn: PASS/FAIL with specific line-level revision notes."
    }
  ]
}
```

## Cost Estimates

- Claude Sonnet: ~$3/million input tokens, ~$15/million output tokens
- One 1,500-word article draft: ~$0.03-0.05 per draft
- 20 articles/month at scale: ~$0.60-1.00/month in API costs
- Pitch generation (5 pitches): ~$0.01

## Error Handling

- **Draft sounds generic**: Include more example articles from the target blog in the system prompt. Add specific data points the author can reference.
- **Backlinks feel forced**: Reduce backlink count to 1-2 per article. Rewrite the surrounding paragraph to make the reference serve the reader's need.
- **Draft too long/short**: Adjust `max_tokens` and explicitly state word count target in the prompt.
- **Style mismatch**: Add negative instructions ("Do NOT use bullet points" if the blog uses prose, "Do NOT use first person" if the blog prefers third person).
- **Rate limits**: Anthropic standard rate limits apply: 4,000 requests/minute on most plans.

## Alternatives

- **OpenAI GPT-4o API** ($2.50/$10 per million tokens): Similar capability, slightly different writing style
- **Google Gemini API** ($7/$21 per million tokens for 1.5 Pro): Alternative LLM option
- **Mistral Large API** ($3/$9 per million tokens): Open-weight alternative
- **Cohere Command R+** ($3/$15 per million tokens): Good for structured content generation
- **Together AI** (various models, $0.20-$3 per million tokens): Access to multiple open models
