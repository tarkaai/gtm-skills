---
name: gift-selection-scoring
description: Use Claude to score and select the optimal gift type, value, and personalization for a prospect based on enrichment data
tool: Anthropic
difficulty: Config
---

# AI Gift Selection & Scoring

Use Claude to analyze prospect enrichment data and select the optimal gift type, value, and personalization angle. This replaces guesswork with data-driven gift matching.

## Input

Provide Claude with the prospect's enrichment data:
- Company size, industry, stage, recent funding
- Prospect's role, seniority, tenure at company
- Signal type that triggered outreach (job change, funding, hiring, competitor use)
- Any known interests from LinkedIn profile, recent posts, or company culture signals
- Budget ceiling for this send tier

## Prompt Template

```
You are a B2B gift selection agent. Given the prospect data below, recommend the optimal gift.

PROSPECT DATA:
- Name: {{first_name}} {{last_name}}
- Title: {{title}} at {{company}}
- Company size: {{employee_count}} employees
- Industry: {{industry}}
- Signal: {{signal_type}} — {{signal_detail}}
- Location: {{city}}, {{state}}, {{country}}
- LinkedIn interests: {{interests}}
- Budget ceiling: ${{max_gift_value}}

AVAILABLE GIFT CATEGORIES:
1. Books ($15-30) — Business/tech books relevant to their role or challenge
2. eGift cards ($25-100) — Digital gift cards (coffee, lunch, Amazon, charity donation in their name)
3. Branded swag ($20-50) — High-quality branded items (notebook, water bottle, tech accessories)
4. Gourmet food ($30-75) — Artisan coffee, chocolate, snack boxes
5. Experiential ($50-150) — Online class, event ticket, subscription trial

OUTPUT FORMAT (JSON):
{
  "gift_category": "books|egift|swag|gourmet|experiential",
  "specific_recommendation": "Exact item description",
  "gift_value": 0,
  "personalization_angle": "Why this gift specifically for this person",
  "note_draft": "The handwritten-style note to include (2-3 sentences, reference their specific situation)",
  "confidence": 0.0-1.0,
  "reasoning": "Why this gift over alternatives"
}

RULES:
- Match gift to signal: job-change prospects get "welcome to your new role" gifts; funding prospects get celebration gifts
- Higher seniority = higher value gifts (within budget)
- Default to books or eGift cards when you lack personal interest data
- Never recommend alcohol (cultural/religious sensitivity)
- For international recipients, prefer digital gifts or locally sourceable items
- The note MUST reference something specific about their situation — never generic
```

## API Call

```
POST https://api.anthropic.com/v1/messages
x-api-key: {{ANTHROPIC_API_KEY}}
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 500,
  "messages": [
    {
      "role": "user",
      "content": "{{prompt_with_prospect_data}}"
    }
  ]
}
```

## Output

JSON object with gift recommendation, personalized note draft, value, and confidence score. Parse the JSON and pass to the appropriate gifting platform fundamental (`sendoso-send-gift`, `tremendous-send-reward`, `reachdesk-send-gift`, or `giftsenda-send-gift`).

## Error Handling

- If confidence < 0.5, default to a $25 eGift card with a generic-but-warm note and flag for human review
- If the recommended gift category is not available on your gifting platform, re-prompt with the available catalog
- If the prospect is international and the recommendation is a physical gift, verify the gifting platform supports delivery to that country before proceeding

## Cost

Anthropic API: ~$0.003 per gift selection (one Claude Sonnet call with ~1000 tokens input, ~300 tokens output). At 500 gifts/month: ~$1.50/month.

https://www.anthropic.com/pricing
