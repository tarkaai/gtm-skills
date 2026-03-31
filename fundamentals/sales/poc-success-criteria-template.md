---
name: poc-success-criteria-template
description: Generate a structured POC success criteria document with measurable outcomes, timeline, stakeholder responsibilities, and decision framework
tool: Anthropic
product: Claude API
difficulty: Config
---

# POC Success Criteria Template

Generate a structured proof-of-concept success criteria document from discovery call data. The document defines what will be tested, how success is measured, who is responsible, and what happens after the POC concludes.

## When to Use

After a discovery call when the deal has entered the Aligned stage and both parties agree a POC is the right next step. This fundamental produces the document; the drill layer handles the workflow around it (stakeholder review, sign-off, kickoff scheduling).

## Instructions

### 1. Gather inputs from CRM

Pull the following from the deal record in Attio (or your CRM):
- Discovery call notes or transcript (from Fireflies)
- Prospect's stated pain points and use cases
- Prospect's current workflow or competing solution
- Stakeholders identified (champion, economic buyer, technical evaluator)
- Deal size and urgency signals
- Industry and company size

### 2. Generate the success criteria document

Call the Anthropic Messages API to generate a structured document:

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  anthropic-version: 2023-06-01
  content-type: application/json

Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Generate a POC success criteria document from this context.\n\nProspect: {company_name}, {industry}, {company_size} employees\nChampion: {champion_name}, {champion_title}\nPain points: {pain_points}\nUse cases to validate: {use_cases}\nCurrent solution: {current_solution}\nDeal size: {deal_value}\n\nReturn a JSON object with this structure:\n{\n  \"poc_title\": \"POC: {company_name} - {primary_use_case}\",\n  \"duration_days\": <7|14|21 based on complexity>,\n  \"success_criteria\": [\n    {\n      \"criterion\": \"<specific measurable outcome>\",\n      \"metric\": \"<how to measure>\",\n      \"target\": \"<specific threshold>\",\n      \"priority\": \"must-have|nice-to-have\"\n    }\n  ],\n  \"milestones\": [\n    {\n      \"name\": \"<milestone name>\",\n      \"day\": <target day number>,\n      \"deliverable\": \"<what is produced>\",\n      \"owner\": \"prospect|vendor|both\"\n    }\n  ],\n  \"stakeholder_responsibilities\": {\n    \"prospect\": [\"<action items>\"],\n    \"vendor\": [\"<action items>\"]\n  },\n  \"decision_framework\": {\n    \"pass_criteria\": \"<what must be true to proceed>\",\n    \"fail_criteria\": \"<what would cause a no-go>\",\n    \"decision_date\": \"<date relative to POC end>\",\n    \"decision_maker\": \"<role/name>\"\n  },\n  \"support_model\": {\n    \"check_in_cadence\": \"<frequency>\",\n    \"support_channel\": \"<slack/email/intercom>\",\n    \"escalation_path\": \"<who to contact for blockers>\"\n  }\n}\n\nRules:\n- Every success criterion must be objectively measurable (no subjective language)\n- Include 3-5 must-have criteria and 1-2 nice-to-have\n- Milestones should be evenly distributed across the POC duration\n- First milestone must be achievable within 48 hours (quick win)\n- Decision framework must include a specific date and named decision maker"
  }]
}
```

### 3. Validate the output

Parse the JSON response. Verify:
- At least 3 must-have success criteria exist
- Each criterion has a measurable target (contains a number or binary yes/no)
- Milestones cover the full POC duration (first within 48 hours, last before final day)
- Decision date is within 5 business days of POC end
- Both prospect and vendor have at least 2 responsibilities

If validation fails, re-prompt Claude with the specific missing elements.

### 4. Store the document

Write the success criteria document to the deal record:
- Store the full JSON as an Attio note on the deal
- Set custom attributes: `poc_duration_days`, `poc_start_date`, `poc_decision_date`, `poc_criteria_count`

## Error Handling

- **Insufficient context**: If discovery notes are too thin to generate specific criteria, return a warning and ask the agent to schedule a brief scoping call before generating the document.
- **Overly broad criteria**: If Claude generates criteria like "prospect is satisfied," reject and re-prompt with explicit instruction to use measurable targets.
- **Missing stakeholders**: If no decision maker is identified, flag this as a blocker the deal owner must resolve before POC kickoff.

## Output

A structured JSON document containing POC success criteria, milestones, stakeholder responsibilities, and decision framework, stored as a note on the Attio deal record.
