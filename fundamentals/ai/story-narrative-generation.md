---
name: story-narrative-generation
description: Generate a prospect-specific demo narrative that weaves product capabilities through a customer story matching the prospect's context
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Story Narrative Generation

Generate a complete demo narrative script that anchors product demonstration inside a real customer story. The output is a structured demo flow where every feature is shown through the lens of how a specific customer used it to solve a problem the prospect shares.

## Prerequisites

- Customer story record (company, challenge, solution approach, results, key quotes)
- Prospect context (company, industry, size, pain points from discovery, stakeholder roles)
- Product feature catalog (features with descriptions)
- Anthropic API key

## Steps

### 1. Assemble story and prospect inputs

Build the input object:

```json
{
  "customer_story": {
    "company": "Acme Corp",
    "industry": "B2B SaaS",
    "headcount": 120,
    "challenge": "Manual onboarding taking 3 weeks per customer, causing 20% churn in first 90 days",
    "solution_approach": "Automated onboarding sequences with milestone tracking",
    "results": {
      "primary_metric": "Onboarding time reduced from 3 weeks to 4 days",
      "secondary_metrics": ["First-90-day churn dropped from 20% to 6%", "NPS increased 32 points"],
      "timeframe": "90 days"
    },
    "key_quotes": [
      "We went from losing a customer a week to not losing one in two months",
      "My team finally stopped firefighting and started building"
    ]
  },
  "prospect": {
    "company": "Beta Inc",
    "industry": "B2B SaaS",
    "headcount": 85,
    "pains": ["Slow onboarding frustrating new customers", "CS team overwhelmed with manual setup tasks"],
    "stakeholder_role": "VP Customer Success",
    "discovery_quotes": ["Our onboarding is basically a spreadsheet and prayer"]
  },
  "feature_catalog": [
    {"name": "Automated Workflows", "description": "..."},
    {"name": "Milestone Tracking", "description": "..."}
  ]
}
```

### 2. Generate the story-based demo narrative via Claude API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "Generate a demo narrative that tells a customer story while demonstrating the product. The prospect should see themselves in the customer's shoes.\n\nCustomer story:\n{customer_story_json}\n\nProspect context:\n{prospect_json}\n\nFeature catalog:\n{feature_catalog_json}\n\nRules:\n- Never say 'Let me show you this feature.' Always say 'Here's what [Customer] did when they faced [same challenge].'\n- Open with the customer's pain — the prospect must recognize their own problem.\n- Each feature shown must be anchored to a specific moment in the customer's journey.\n- Use the customer's exact quotes at emotional peaks.\n- Adapt the story details to mirror the prospect's specifics (company size, industry language, role context).\n- Close by connecting the customer's result to the prospect's stated pain.\n\nReturn this exact JSON:\n{\n  \"opening_hook\": \"1-2 sentences connecting the customer story to the prospect's pain. Reference the prospect's own words from discovery if available.\",\n  \"story_arc\": [\n    {\n      \"phase\": \"The Problem\",\n      \"narration\": \"What to say — telling the customer's challenge in words the prospect relates to\",\n      \"product_show\": \"What to demonstrate on screen during this narration\",\n      \"customer_quote\": \"Direct quote from customer, if relevant to this phase\",\n      \"duration_minutes\": 2\n    }\n  ],\n  \"emotional_peak\": \"The single moment in the story with highest emotional resonance — the 'aha' where the customer's pain turned into relief\",\n  \"closing_bridge\": \"1-2 sentences that connect the customer's outcome to the prospect's situation. End with a question, not a statement.\",\n  \"feature_to_story_map\": [\n    {\"feature\": \"feature name\", \"story_moment\": \"when in the story this feature appears naturally\"}\n  ],\n  \"adaptation_notes\": \"How the story was adapted to mirror the prospect's context\"\n}"
  }]
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
    {"role": "system", "content": "You generate story-based demo narratives. Every demo feature must be shown through a customer story, never as a standalone feature tour."},
    {"role": "user", "content": "{SAME_USER_PROMPT_AS_ABOVE}"}
  ],
  "max_tokens": 3000,
  "temperature": 0.5
}
```

### 4. Validate the narrative

Check:
- `story_arc` has 3-5 phases (problem, turning point, solution, result at minimum)
- Every feature in `feature_to_story_map` corresponds to a phase in `story_arc`
- `opening_hook` references the prospect's specific pain, not a generic opener
- `emotional_peak` contains a concrete moment (quote, metric, or event), not an abstract statement
- `closing_bridge` ends with a question
- Total `duration_minutes` across phases is 15-25 minutes

If validation fails, re-prompt with specific corrections.

### 5. Store and attach to demo record

Store the narrative as an Attio note on the deal record, tagged with the customer story used and the prospect. Fire PostHog event:

```json
{
  "event": "story_narrative_generated",
  "properties": {
    "deal_id": "...",
    "customer_story_company": "Acme Corp",
    "prospect_company": "Beta Inc",
    "story_phases": 4,
    "features_mapped": 3,
    "adaptation_depth": "high"
  }
}
```

## Cost Estimates

- Anthropic Claude Sonnet: ~$0.04-0.10 per narrative
- At scale (50 narratives/quarter): under $5/quarter in API costs

## Error Handling

- **No matching customer story available:** Fall back to a composite narrative built from multiple customer data points. Flag `story_type: composite` in output. Recommend creating a real case study for this segment.
- **Insufficient discovery data:** Generate narrative using industry-level pain assumptions. Flag `personalization_depth: low`.
- **Feature catalog missing:** Generate story arc only (no feature mapping). Flag for manual feature selection.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best narrative structure |
| GPT-4 (OpenAI) | Chat Completions API | Good alternative |
| Gemini (Google) | Generative AI API | Alternative LLM |
| Manual | Story template | Fallback with fill-in-the-blank fields |
