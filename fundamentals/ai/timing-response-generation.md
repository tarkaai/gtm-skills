---
name: timing-response-generation
description: Use Claude to generate tailored timing objection responses based on objection subtype, deal context, and urgency driver analysis
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Generate Timing Objection Responses

Given a classified timing objection, deal context with urgency drivers, and cost-of-delay data, use the Claude API to generate a response that reframes timing from "not now" to "the cost of waiting."

## Prerequisites

- Classified timing objection data (from `call-transcript-timing-extraction`)
- Deal record from Attio with pain data, timeline fields, and urgency drivers
- Anthropic API key
- Cost-of-delay estimate (from `cost-of-delay-calculation`, optional but improves quality)
- Historical response effectiveness data (optional, improves framework selection over time)

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
    "content": "Generate a timing objection response for a sales conversation where the prospect says it's 'not the right time.'\n\nObjection details:\n- Prospect quote: \"{objection_quote}\"\n- Objection subtype: {subtype}\n- Emotional tone: {emotional_tone}\n- Severity: {severity}/10\n- Timeline category: {timeline_category}\n- Stated timeline: {stated_timeline or 'vague'}\n\nDeal context:\n- Company: {company_name}\n- Deal value: ${deal_value}/year\n- Total quantified pain: ${total_quantified_pain}/year\n- Pain-to-price ratio: {ratio}x\n- Monthly cost of delay: ${monthly_cost_of_delay}\n- Champion: {champion_name}, {champion_title}\n- Decision maker: {decision_maker_name}, {decision_maker_title}\n- Strongest pain: \"{strongest_pain_summary}\"\n- Key pain quote: \"{key_pain_quote}\"\n- Known urgency drivers: {urgency_drivers_json}\n- Competitive landscape: {competitor_status or 'unknown'}\n\nHistorical effectiveness (if available):\n{framework_effectiveness_json}\n\nGenerate the response using the most effective framework for this subtype. The frameworks are:\n- cost_of_delay: Quantify what each month of inaction costs. Best when pain is quantified.\n- manufactured_urgency: Create legitimate urgency via pricing lock, pilot slot, or implementation timeline. Best when no natural deadline exists.\n- bridging_solution: Propose a minimal starting scope that can begin immediately. Best when the blocker is resource constraints or competing priorities.\n- event_anchoring: Anchor to an external event (fiscal year, contract renewal, seasonal deadline). Best when a real event exists.\n- social_proof_timing: Show what competitors or peers did at this same stage. Best when competitive pressure exists.\n- status_quo_challenge: Challenge the assumption that waiting is safe — inaction has its own risks. Best when the prospect treats delay as zero-cost.\n\nReturn this exact JSON:\n{\n  \"framework_used\": \"cost_of_delay|manufactured_urgency|bridging_solution|event_anchoring|social_proof_timing|status_quo_challenge\",\n  \"verbal_response\": \"The exact words to say on a call (3-5 sentences max). Must reference their specific situation, not generic advice.\",\n  \"diagnostic_questions\": [\"3-4 follow-up questions to surface the true blocker behind the timing objection\"],\n  \"cost_of_delay_framing\": \"One sentence that frames delay cost in the prospect's terms (e.g., 'Every month you wait costs your team 480 hours of manual work')\",\n  \"follow_up_email\": {\n    \"subject\": \"Email subject line\",\n    \"body\": \"Follow-up email body (under 200 words) that reinforces the timing argument with data\"\n  },\n  \"bridging_proposal\": {\n    \"scope\": \"What a minimal starting engagement looks like\",\n    \"timeline\": \"When they could start and what the first 30 days look like\",\n    \"investment\": \"Reduced scope pricing or phased payment approach\"\n  },\n  \"supporting_asset\": {\n    \"type\": \"cost_of_delay_analysis|implementation_timeline|quick_start_plan|peer_case_study|roi_with_timeline\",\n    \"description\": \"What to attach and why\"\n  },\n  \"escalation_path\": \"What to do if this response doesn't resolve the objection\",\n  \"expected_next_step\": \"The specific action to propose after delivering this response\",\n  \"nurture_strategy\": {\n    \"if_delay_accepted\": \"How to stay engaged if the prospect genuinely needs to wait\",\n    \"re_engagement_trigger\": \"What signal should trigger re-engagement\",\n    \"cadence\": \"How often to touch base during the wait period\"\n  }\n}"
  }]
}
```

## Input Requirements

- `objection_quote`: The prospect's exact words
- `subtype`: One of: `budget_cycle` (waiting for next budget), `competing_priorities` (other projects first), `organizational_change` (reorg, new leadership), `no_urgency` (don't see why now), `evaluation_fatigue` (too many vendor evaluations), `resource_constraints` (no bandwidth to implement)
- `monthly_cost_of_delay`: From cost-of-delay calculation. If unavailable, set to "not calculated" and the response will emphasize qualitative cost.
- `urgency_drivers_json`: Array of known urgency triggers from timeline extraction

## Framework Selection Logic

When historical data is not available, use these default framework mappings:

| Subtype | Primary Framework | Why |
|---------|------------------|-----|
| budget_cycle | manufactured_urgency | Lock pricing or reserve implementation slot to create urgency within their budget timeline |
| competing_priorities | bridging_solution | Reduce scope so it fits alongside other priorities |
| organizational_change | event_anchoring | Anchor to the transition as an opportunity, not a blocker |
| no_urgency | cost_of_delay | Quantify what waiting actually costs — make inaction feel expensive |
| evaluation_fatigue | bridging_solution | Simplify the decision with a low-risk starting point |
| resource_constraints | bridging_solution | Propose a white-glove implementation that requires minimal internal resources |

When historical data IS available, override defaults with the highest win-rate framework for that subtype, provided sample size >= 8.

## Output

JSON response containing:
- Verbal response tailored to the specific timing subtype
- Diagnostic questions to surface the true blocker
- Cost-of-delay framing sentence
- Follow-up email with data reinforcement
- Bridging proposal for a minimal starting scope
- Supporting asset recommendation
- Escalation path and nurture strategy for genuine delays

Store in Attio as a note on the deal record. Log in PostHog as `timing_response_generated` event.

## Guardrails

- Never pressure a prospect with fake urgency (made-up deadlines, fictional scarcity). All urgency must be grounded in real business impact or real constraints.
- Never dismiss a legitimate timing concern. If the prospect's company is mid-acquisition or mid-layoff, acknowledge the reality and propose a nurture cadence.
- If `monthly_cost_of_delay` is unavailable and `pain_to_price_ratio < 3`, flag for the seller: the value story is too weak to challenge timing effectively. Re-run discovery first.
- If `emotional_tone` is "firm" and `severity >= 8`, recommend a human-led response with empathy — these need judgment, not frameworks.
- Rate limit: max 3 response generations per deal per day.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for nuanced responses |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gong Assist | Built-in AI | Real-time coaching during calls |
| Manual | Framework reference sheet | Fallback for enterprise deals |
