---
name: change-resistance-diagnosis
description: Use Claude to classify change management objection root causes from call transcripts or CRM notes and assess organizational change readiness
tool: Anthropic
difficulty: Advanced
---

# Change Resistance Diagnosis

Given a prospect's statements about reluctance to switch from their current solution, classify the root cause of resistance, assess organizational change readiness, and identify which change support interventions are most likely to unlock the deal.

## Prerequisites

- Call transcript or CRM notes containing change resistance signals (from `fireflies-transcription` or `attio-notes`)
- Deal record from Attio with existing solution info and stakeholder data
- Company enrichment data from Clay (headcount, funding stage, industry)
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
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "Analyze this sales conversation for change management resistance. Classify the root causes, assess organizational change readiness, and recommend interventions.\n\nTranscript/Notes:\n{transcript_or_notes}\n\nDeal context:\n- Company: {company_name}\n- Headcount: {headcount}\n- Industry: {industry}\n- Current solution: {current_solution}\n- Time on current solution: {years_on_current}\n- Contract status: {contract_status or 'unknown'}\n- Stakeholders engaged: {stakeholder_list}\n- Champion: {champion_name}, {champion_title}\n- Decision maker: {dm_name}, {dm_title}\n\nReturn this exact JSON:\n{\n  \"resistance_signals\": [\n    {\n      \"id\": \"res-001\",\n      \"root_cause\": \"disruption_fear|past_failure|training_burden|data_migration|team_pushback|political_dynamics|vendor_lock_in|sunk_cost_bias|compliance_risk|unknown\",\n      \"prospect_quote\": \"Exact quote expressing resistance\",\n      \"stakeholder\": \"Name and role of who raised it\",\n      \"severity\": 1-10,\n      \"emotional_tone\": \"firm|anxious|resigned|exploratory|political\",\n      \"addressable\": true or false,\n      \"intervention\": \"migration_support|training_program|phased_rollout|pilot_program|parallel_running|case_study|executive_alignment|data_migration_guarantee|compliance_mapping\"\n    }\n  ],\n  \"change_readiness_score\": 1-100,\n  \"readiness_factors\": {\n    \"pain_urgency\": 1-10,\n    \"champion_strength\": 1-10,\n    \"executive_sponsorship\": 1-10,\n    \"change_history\": \"positive|neutral|negative|unknown\",\n    \"team_openness\": 1-10,\n    \"current_solution_lock_in\": 1-10\n  },\n  \"primary_blocker\": \"The single biggest barrier to change\",\n  \"recommended_sequence\": [\n    {\n      \"step\": 1,\n      \"action\": \"Description of what to do\",\n      \"target_stakeholder\": \"Who to engage\",\n      \"asset_needed\": \"migration_plan|training_preview|case_study|roi_comparison|pilot_proposal|compliance_mapping\",\n      \"expected_impact\": \"What this unblocks\"\n    }\n  ],\n  \"deal_risk_level\": \"low|medium|high|critical\",\n  \"change_timeline_estimate\": \"Estimated weeks from decision to full adoption\"\n}"
  }]
}
```

## Input Requirements

- `transcript_or_notes`: Full call transcript or detailed CRM notes capturing the change objection
- `current_solution`: The solution the prospect is currently using (critical for diagnosis)
- `years_on_current`: How long they have been on the current solution (longer = higher switching inertia)
- `contract_status`: Whether they are mid-contract, month-to-month, or approaching renewal

## Root Cause Classification

| Root Cause | Definition | Typical Quote Pattern |
|-----------|-----------|----------------------|
| disruption_fear | Fear that switching will disrupt daily operations | "We can't afford any downtime" |
| past_failure | Previous migration went badly | "We tried switching before and it was a disaster" |
| training_burden | Concern about retraining the team | "My team is already stretched thin" |
| data_migration | Anxiety about losing or corrupting data | "We have 5 years of data in this system" |
| team_pushback | End users resisting the change | "My team loves the current tool" |
| political_dynamics | Internal politics favoring the incumbent | "The VP of Ops chose the current system" |
| vendor_lock_in | Technical or contractual lock-in | "We're locked in until Q4" |
| sunk_cost_bias | Reluctance to abandon investment | "We spent $200K customizing this" |
| compliance_risk | Regulatory or audit concerns about switching | "Our auditors approved the current workflow" |

## Output

JSON response containing:
- All detected resistance signals with root cause classification
- Organizational change readiness score (1-100)
- Recommended intervention sequence ordered by expected impact
- Deal risk level assessment

Store in Attio as a note on the deal record. Log in PostHog as `change_resistance_diagnosed` event.

## Guardrails

- Never classify resistance as "unknown" if the transcript provides enough context to determine root cause. Only use "unknown" when the prospect is vague about their concerns.
- If `change_readiness_score < 30`, flag the deal as requiring human strategic review before investing more time.
- If `past_failure` is a root cause, always recommend `case_study` as the first intervention (proof that others succeeded).
- Never recommend `parallel_running` (most expensive intervention) unless `severity >= 8` and the prospect explicitly mentions risk of disruption.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for nuanced classification |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Gong Assist | Built-in AI | Real-time call coaching but less structured extraction |
| Manual | Framework reference sheet | Fallback for strategic enterprise deals |
