---
name: pricing-presentation-scoring
description: Score a completed pricing presentation's effectiveness using deal outcome data, prospect engagement signals, and conversation analysis
tool: Anthropic
product: Claude API
difficulty: Config
---

# Pricing Presentation Scoring

After a pricing conversation, score how effectively the seller presented pricing using structured signals: did they lead with value, present tiers correctly, handle objections without premature discounting, and advance the deal? The score feeds the optimization loop at Durable level.

## Prerequisites

- Pricing presentation completed (call or email)
- Call transcript from Fireflies or recording tool (optional but preferred)
- Deal record in Attio with pricing tier presented, outcome, and any discount given
- Anthropic API key

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
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Score the effectiveness of a pricing presentation in a sales conversation. Evaluate the seller's approach against best practices.\n\nPresentation context:\n- Tiers presented: {tiers_presented_json}\n- Presentation format: {format} (live_call|email_proposal|video_walkthrough|in_person)\n- Value recap given before pricing: {value_recap_given} (true|false)\n- Pains referenced during pricing: {pains_referenced}\n- Prospect's initial reaction: {initial_reaction} (positive|neutral|pushback|silence|asked_for_discount)\n- Tier selected or discussed: {tier_discussed}\n- Discount requested: {discount_requested} (true|false)\n- Discount given: {discount_pct}%\n- Outcome: {outcome} (accepted|negotiating|requested_time|objected|lost)\n- Days since presentation: {days_since}\n- Deal advanced to next stage: {advanced} (true|false)\n\nCall transcript excerpt (pricing segment):\n{transcript_excerpt}\n\nReturn this exact JSON:\n{\n  \"overall_score\": 0,\n  \"dimension_scores\": {\n    \"value_anchoring\": {\"score\": 0, \"max\": 25, \"feedback\": \"What went well or poorly with value-before-price\"},\n    \"tier_presentation\": {\"score\": 0, \"max\": 25, \"feedback\": \"Did they present all tiers in the right order with clear differentiation?\"},\n    \"discount_discipline\": {\"score\": 0, \"max\": 25, \"feedback\": \"Did they hold price, offer alternatives to discounting, and follow guardrails?\"},\n    \"close_progression\": {\"score\": 0, \"max\": 25, \"feedback\": \"Did the conversation end with a clear next step and deal advancement?\"}\n  },\n  \"win_signals\": [\"List of positive indicators from this presentation\"],\n  \"improvement_areas\": [\"Specific, actionable changes for the next pricing presentation\"],\n  \"pattern_tag\": \"value_led_success|discount_leak|premature_price_reveal|strong_anchor_weak_close|objection_fumble|textbook_execution\"\n}"
  }]
}
```

## Scoring Dimensions

| Dimension | Max Score | What to Evaluate |
|-----------|-----------|-----------------|
| Value Anchoring | 25 | Did the seller recap discovered pains and agreed outcomes BEFORE revealing price? Was ROI referenced? |
| Tier Presentation | 25 | Were all 3 tiers shown? Correct order (Best first for anchoring)? Clear differentiation? Better recommended? |
| Discount Discipline | 25 | Did the seller resist premature discounting? Offer alternatives (restructure, bundle, payment terms) before reducing price? |
| Close Progression | 25 | Did the conversation end with a clear, specific next step? Did the deal advance or stall? |

## Pattern Tags

Classify each presentation into one of these patterns for aggregate analysis:

- `value_led_success` — Seller led with pain, anchored on value, prospect accepted without heavy discounting
- `discount_leak` — Good presentation but seller offered a discount before being asked or too early in objection handling
- `premature_price_reveal` — Pricing shown before value was established; prospect fixated on cost
- `strong_anchor_weak_close` — Great value framing but no clear next step or urgency to decide
- `objection_fumble` — Pricing presented well but seller struggled with the objection response
- `textbook_execution` — Near-perfect execution across all dimensions

## Output

JSON scoring object containing:
- Overall score (0-100)
- Per-dimension scores and feedback
- Win signals (for reinforcement)
- Improvement areas (for coaching)
- Pattern tag (for aggregate trend analysis)

Store as an Attio note on the deal record. Fire PostHog event `pricing_presentation_scored` with `overall_score`, `pattern_tag`, `discount_pct`, and `outcome`.

## Error Handling

- **No transcript available:** Score based on Attio deal data only (outcome, discount given, stage progression). Reduce confidence and note: "Scored without transcript — dimension feedback is estimated."
- **Presentation via email only:** Skip `tier_presentation` live-delivery scoring; focus on document structure, value framing in email body, and follow-up timing.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best for nuanced sales conversation analysis |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gong | Call analytics API | Automated talk-track analysis with built-in coaching |
| Chorus (ZoomInfo) | Conversation intelligence | Similar to Gong, alternative vendor |
| Manual scoring | Rubric spreadsheet | Fallback for low-volume teams |
