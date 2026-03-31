---
name: competitive-positioning-generation
description: Use Claude to generate tailored competitive positioning responses based on competitor identity, prospect pain profile, and historical win patterns
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Generate Competitive Positioning Responses

Given a detected competitive objection (prospect evaluating or favoring a specific competitor), deal context, and historical competitive win/loss patterns, use the Claude API to generate a positioning response that differentiates without disparaging.

## Prerequisites

- Classified competitive objection data (from `call-transcript-objection-extraction` with competitor context)
- Deal record from Attio with pain data, champion info, and deal value
- Battlecard data for the named competitor (from `competitive-intel-aggregation` or Attio Competitors object)
- Anthropic API key
- Historical competitive win/loss rates (optional, improves framework selection)

## API Call

```
POST https://api.anthropic.com/v1/messages
Authorization: x-api-key {ANTHROPIC_API_KEY}
Content-Type: application/json
```

**Request body:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "Generate a competitive positioning response for a sales conversation where the prospect is evaluating a competitor.\n\nCompetitor context:\n- Competitor name: \"{competitor_name}\"\n- Their known strengths (from battlecard): \"{competitor_strengths}\"\n- Their known weaknesses (from battlecard): \"{competitor_weaknesses}\"\n- Our historical win rate against them: {win_rate_against}%\n- Common objections in competitive deals with them: \"{common_objections}\"\n\nObjection details:\n- Prospect quote: \"{objection_quote}\"\n- Objection type: {competitive_objection_type}\n- Emotional tone: {emotional_tone}\n- Severity: {severity}/10\n- Evaluation stage: {evaluation_stage}\n\nDeal context:\n- Company: {company_name}\n- Industry: {industry}\n- Company size: {company_size}\n- Deal value: ${deal_value}/year\n- Top 3 pains: {top_pains_json}\n- Champion: {champion_name}, {champion_title}\n- Decision criteria (if known): {decision_criteria}\n\nGenerate a competitive positioning response. NEVER disparage the competitor directly. Focus on differentiation aligned to the prospect's specific pains. Return this exact JSON:\n{\n  \"positioning_framework\": \"pain_alignment|capability_gap|tco_comparison|implementation_risk|customer_proof|strategic_fit\",\n  \"verbal_response\": \"The exact words to say on a call (3-5 sentences max). Acknowledge the competitor respectfully, then pivot to differentiation on the prospect's top pain.\",\n  \"trap_questions\": [\"2-3 questions that highlight areas where we are strong and the competitor is weak, without naming the competitor. These questions make the prospect discover the gap themselves.\"],\n  \"comparison_talking_points\": [\n    {\"dimension\": \"dimension name\", \"our_position\": \"what we do\", \"their_gap\": \"what they lack or do differently\", \"why_it_matters\": \"tied to this prospect's specific pain\"}\n  ],\n  \"follow_up_email\": {\n    \"subject\": \"Email subject (no competitor name in subject)\",\n    \"body\": \"Follow-up email under 200 words. Lead with the prospect's pain. Show how our approach uniquely solves it. Include one customer proof point. End with a specific next step.\"\n  },\n  \"champion_ammunition\": {\n    \"internal_talking_points\": \"3 bullet points the champion can use when presenting to the buying committee to differentiate us\",\n    \"evaluation_criteria_suggestions\": [\"Criteria we should suggest the prospect add to their evaluation that favor our strengths\"]\n  },\n  \"supporting_asset\": {\n    \"type\": \"tco_comparison|feature_matrix|customer_case_study|migration_guide|technical_deep_dive\",\n    \"description\": \"What to create or share and why\"\n  },\n  \"if_they_push_back\": \"What to say if the prospect pushes back on this positioning. Second-level response.\",\n  \"deal_risk_assessment\": \"low|medium|high — based on competitor strength against this prospect's specific criteria\"\n}"
  }]
}
```

## Competitive Objection Types

Classify the competitive objection before generating a response:

| Type | Signal | Example |
|------|--------|---------|
| `active_evaluation` | Prospect is comparing side-by-side | "We're also looking at {competitor}" |
| `incumbent_loyalty` | Prospect already uses competitor | "We're happy with {competitor} but exploring" |
| `feature_comparison` | Prospect names a specific feature gap | "{competitor} has X, do you?" |
| `price_comparison` | Competitor is cheaper | "{competitor} quoted us 40% less" |
| `social_proof` | Competitor has stronger brand/references | "Our peer companies all use {competitor}" |
| `switching_cost` | Migration fear | "We've invested a lot in {competitor}" |

## Positioning Framework Selection

When historical data is not available, use these default mappings:

| Objection Type | Primary Framework | Why |
|---------------|------------------|-----|
| active_evaluation | pain_alignment | Anchor evaluation to their pains, not features |
| incumbent_loyalty | implementation_risk | Show cost of staying (stagnation risk) vs switching |
| feature_comparison | capability_gap | Reframe from feature to outcome — what does the feature enable? |
| price_comparison | tco_comparison | Expand the comparison from license cost to total cost of ownership |
| social_proof | customer_proof | Counter with references from same segment who chose us |
| switching_cost | strategic_fit | Reframe from short-term migration cost to long-term strategic alignment |

When historical data IS available, override defaults with the highest win-rate framework for that competitor + objection type, provided sample size >= 5.

## Output

JSON response object containing:
- Positioning framework selected
- Verbal response for live conversation
- Trap questions that surface competitor weaknesses organically
- Comparison talking points tied to prospect pains
- Follow-up email with competitive positioning
- Champion ammunition for internal selling
- Supporting asset recommendation
- Second-level response if prospect pushes back
- Deal risk assessment

Store in Attio as a note on the deal record. Log in PostHog as `competitive_positioning_generated` event.

## Guardrails

- NEVER include competitor disparagement — no "they can't," "they're bad at," "they fail." Always frame as "we do X differently because..."
- NEVER lie about competitor capabilities. If uncertain, say "I'd want to verify that" rather than claiming they lack something.
- If the competitor is genuinely stronger on the prospect's top pain, flag this: "Competitor has a strong position on {pain}. Consider whether secondary pains can carry the deal, or whether this is a competitive loss we should qualify out early."
- If `severity >= 8` and `evaluation_stage` is "finalist_comparison", recommend a human-led competitive strategy session rather than automated response.
- Rate limit: max 3 positioning generations per deal per day.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best for nuanced competitive positioning with structured output |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Klue | Competitive intelligence platform | Purpose-built battlecard management, API available |
| Crayon | Competitive intelligence platform | Real-time competitor monitoring + battlecards |
| Kompyte (Semrush) | Competitive intelligence | Automated competitive tracking |
| Manual | Battlecard reference sheet | Fallback for high-stakes enterprise deals |
