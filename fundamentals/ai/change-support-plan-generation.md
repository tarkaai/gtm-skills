---
name: change-support-plan-generation
description: Use Claude to generate a tailored change management support plan matched to the prospect's diagnosed resistance factors and organizational profile
tool: Anthropic
difficulty: Advanced
---

# Change Support Plan Generation

Given diagnosed change resistance root causes and organizational readiness data, generate a comprehensive change support plan tailored to the prospect's specific concerns. The plan is written from the buyer's perspective and designed to be forwarded internally as a "here's how we'll support your transition" document.

## Prerequisites

- Change resistance diagnosis data (from `change-resistance-diagnosis`)
- Deal record from Attio with pain data, stakeholder mapping, and timeline
- Company enrichment data from Clay
- Product implementation details (timeline, training requirements, migration scope)
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
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Generate a change management support plan for a prospect evaluating a switch from their current solution. The plan should address their specific resistance factors and be written so the champion can forward it to stakeholders.\n\nResistance diagnosis:\n{diagnosis_json}\n\nDeal context:\n- Company: {company_name} ({headcount} employees, {industry})\n- Current solution: {current_solution} (used for {years} years)\n- Our product: {product_name}\n- Deal value: ${deal_value}/year\n- Champion: {champion_name}, {champion_title}\n- Key resisters: {resister_list}\n- Implementation timeline: {implementation_weeks} weeks\n- Data migration scope: {migration_scope}\n- Training scope: {training_scope}\n\nReturn this exact JSON:\n{\n  \"plan_title\": \"{company_name} Transition Support Plan\",\n  \"executive_summary\": \"2-3 sentences summarizing the transition approach and risk mitigation\",\n  \"phases\": [\n    {\n      \"phase\": 1,\n      \"name\": \"Phase name\",\n      \"duration\": \"X weeks\",\n      \"description\": \"What happens in this phase\",\n      \"milestones\": [\"Milestone 1\", \"Milestone 2\"],\n      \"risk_mitigations\": [\n        {\"risk\": \"Specific risk from diagnosis\", \"mitigation\": \"How this phase addresses it\"}\n      ],\n      \"stakeholder_actions\": [\n        {\"stakeholder\": \"Role\", \"action\": \"What they need to do\", \"time_commitment\": \"X hours\"}\n      ]\n    }\n  ],\n  \"rollout_strategy\": {\n    \"approach\": \"phased|parallel|big_bang|pilot_first\",\n    \"rationale\": \"Why this approach for this company\",\n    \"pilot_scope\": \"If pilot: which team/department/use case goes first\",\n    \"success_criteria\": [\"Metric that must be hit before expanding\"]\n  },\n  \"training_plan\": {\n    \"total_hours_per_user\": 0,\n    \"format\": \"live_sessions|self_paced|blended\",\n    \"sessions\": [\n      {\"topic\": \"...\", \"audience\": \"...\", \"duration\": \"...\", \"timing\": \"Week X\"}\n    ],\n    \"ongoing_support\": \"Description of post-training support resources\"\n  },\n  \"data_migration\": {\n    \"scope\": \"Description of what data moves\",\n    \"approach\": \"automated|manual|hybrid\",\n    \"validation\": \"How data integrity is verified\",\n    \"rollback_plan\": \"What happens if migration fails\"\n  },\n  \"risk_register\": [\n    {\n      \"risk\": \"Specific risk\",\n      \"likelihood\": \"low|medium|high\",\n      \"impact\": \"low|medium|high\",\n      \"owner\": \"Who manages this risk\",\n      \"mitigation\": \"Specific action to prevent or reduce\",\n      \"contingency\": \"What to do if it happens anyway\"\n    }\n  ],\n  \"success_metrics\": [\n    {\"metric\": \"Name\", \"target\": \"Number\", \"measurement\": \"How and when\"}\n  ],\n  \"timeline_summary\": {\n    \"total_weeks\": 0,\n    \"key_dates\": [\n      {\"week\": 0, \"milestone\": \"Description\"}\n    ]\n  },\n  \"guarantee\": {\n    \"type\": \"pilot_exit|phased_rollback|parallel_run|money_back|none\",\n    \"description\": \"What risk reduction guarantee we offer\"\n  }\n}"
  }]
}
```

## Input Requirements

- `diagnosis_json`: Output from the `change-resistance-diagnosis` fundamental
- `migration_scope`: Description of data that needs to move (e.g., "5 years of CRM records, 10K contacts, 500 deals")
- `training_scope`: Who needs training and their technical proficiency level
- `resister_list`: Stakeholders who have expressed resistance (from diagnosis)

## Rollout Strategy Selection

When historical data is not available, use these defaults:

| Change Readiness Score | Recommended Approach | Rationale |
|----------------------|---------------------|-----------|
| 70-100 | big_bang | High readiness; team is eager; rip the bandaid |
| 50-69 | phased | Moderate readiness; prove value with early adopters first |
| 30-49 | pilot_first | Low readiness; need a win before expanding |
| 0-29 | parallel | Very low readiness; run both systems until confidence builds |

Override defaults when specific resistance factors dominate:
- `past_failure` root cause -> always start with pilot_first regardless of score
- `team_pushback` root cause -> prefer phased with champions in each department
- `data_migration` root cause -> always include parallel running period

## Output

JSON response containing:
- Phased implementation plan with milestones and risk mitigations
- Rollout strategy matched to organizational readiness
- Training plan with sessions and ongoing support
- Data migration approach with rollback plan
- Risk register with mitigations and contingencies
- Success metrics and timeline

Store in Attio as a note on the deal record. Log in PostHog as `change_support_plan_generated` event.

## Guardrails

- Never promise implementation timelines shorter than realistic (pad by 25% for safety)
- Always include a rollback or exit plan (prospects need to know they can reverse course)
- Training plan must account for different skill levels within the prospect's team
- Risk register must address every root cause identified in the diagnosis
- If `change_readiness_score < 30`, the plan MUST include a pilot phase (no big bang)
- Never skip data migration planning even if scope seems small

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best structured output for multi-section plans |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Notion template | Manual | Pre-built transition plan template, filled manually |
| Qwilr | API | Interactive proposal with embedded change plan |
| Manual | Project management tool | Build in Asana/Linear for complex enterprise transitions |
