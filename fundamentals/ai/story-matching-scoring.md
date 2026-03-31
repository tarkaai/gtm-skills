---
name: story-matching-scoring
description: Score and rank customer stories against a prospect profile to select the highest-resonance story for a demo
tool: Anthropic
difficulty: Config
---

# Story Matching Scoring

Given a prospect profile and a library of customer stories, score each story on relevance dimensions and return a ranked list. The top-ranked story is the best candidate for the demo narrative.

## Prerequisites

- Story library: structured records of customer stories (company, industry, size, challenge, solution, results)
- Prospect profile: company, industry, headcount, pain points from discovery, stakeholder role
- Anthropic API key (or OpenAI)

## Steps

### 1. Prepare the scoring request

Build the input:

```json
{
  "prospect": {
    "company": "Beta Inc",
    "industry": "B2B SaaS",
    "headcount": 85,
    "pains": ["Slow onboarding", "CS team overwhelmed"],
    "stakeholder_role": "VP Customer Success"
  },
  "stories": [
    {
      "id": "story-001",
      "company": "Acme Corp",
      "industry": "B2B SaaS",
      "headcount": 120,
      "challenge_summary": "Manual onboarding causing churn",
      "result_summary": "Onboarding time reduced 80%, churn dropped 70%",
      "primary_metric": "Onboarding time from 3 weeks to 4 days"
    },
    {
      "id": "story-002",
      "company": "Delta Ltd",
      "industry": "Fintech",
      "headcount": 300,
      "challenge_summary": "Compliance reporting consuming 40 hours/month",
      "result_summary": "Automated compliance, 90% time reduction",
      "primary_metric": "Compliance reporting time from 40h to 4h/month"
    }
  ]
}
```

### 2. Score stories via Claude API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "Score each customer story for relevance to this prospect. The best story is one where the prospect will see themselves in the customer's shoes.\n\nProspect:\n{prospect_json}\n\nStory library:\n{stories_json}\n\nScore each story 0-100 on these dimensions:\n- industry_match (0-25): Same industry = 25, adjacent = 15, unrelated = 5\n- size_match (0-20): Within 2x headcount = 20, within 5x = 10, beyond = 5\n- pain_overlap (0-30): How closely the customer's challenge maps to the prospect's stated pains. Exact match = 30, partial = 15, tangential = 5\n- role_relevance (0-15): Customer story resonates with this stakeholder persona. Same role = 15, same department = 10, different = 5\n- result_impact (0-10): How impressive the results are in absolute terms. Transformative = 10, solid = 7, modest = 4\n\nReturn JSON:\n{\n  \"rankings\": [\n    {\n      \"story_id\": \"story-001\",\n      \"total_score\": 85,\n      \"scores\": {\"industry_match\": 25, \"size_match\": 18, \"pain_overlap\": 27, \"role_relevance\": 10, \"result_impact\": 5},\n      \"rationale\": \"One sentence explaining why this story fits\",\n      \"adaptation_hint\": \"One sentence on how to adapt the story for this prospect\"\n    }\n  ]\n}"
  }]
}
```

### 3. Score via OpenAI API (alternative)

```
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer {OPENAI_API_KEY}
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You score customer stories for prospect relevance. Return structured JSON rankings."},
    {"role": "user", "content": "{SAME_USER_PROMPT_AS_ABOVE}"}
  ],
  "max_tokens": 1500,
  "temperature": 0.2
}
```

### 4. Select and validate

Take the top-ranked story. Validate:
- `total_score` >= 50 (below 50, the story is too dissimilar — flag for case study gap)
- `pain_overlap` >= 15 (if the pain doesn't match, the story won't resonate regardless of other factors)
- If the top 2 stories score within 5 points of each other, flag both as candidates and let the rep choose

Store the ranking in Attio on the deal record. Fire PostHog event:

```json
{
  "event": "story_match_scored",
  "properties": {
    "deal_id": "...",
    "top_story_id": "story-001",
    "top_score": 85,
    "stories_evaluated": 5,
    "pain_overlap_score": 27,
    "story_gap_flagged": false
  }
}
```

## Error Handling

- **No stories score above 50:** Flag a story gap for this segment. Recommend creating a new case study targeting this industry/pain combination. Use a composite narrative as fallback.
- **Only 1 story in library:** Skip scoring, return it as default. Flag that story diversity is needed.

## Cost Estimates

- Anthropic Claude Sonnet: ~$0.01-0.03 per scoring run
- At scale (100 scorings/quarter): under $3/quarter

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured scoring |
| GPT-4 (OpenAI) | Chat Completions API | Good alternative |
| Embeddings + cosine similarity | openai-embeddings | Faster for large libraries, less nuanced |
| Manual | Spreadsheet lookup | Fallback for <5 stories |
