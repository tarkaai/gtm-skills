---
name: technical-demo-script-generation
description: Generate a prospect-tailored technical demo script covering architecture, APIs, security, and integration patterns
tool: Anthropic
product: Claude API
difficulty: Config
---

# Technical Demo Script Generation

Generate a structured technical demo script customized to a prospect's tech stack, technical requirements, and engineer-level questions. The output is a runnable demo plan with exact API calls to show, architecture diagrams to reference, security topics to cover, and integration code snippets to present.

## Prerequisites

- Anthropic API key (Claude)
- Prospect tech stack data (from `tech-stack-detection` fundamental or discovery notes)
- Prospect pain points and technical requirements (from discovery call transcript or CRM notes)
- Product feature catalog with API documentation references
- Product architecture overview document

## Steps

### 1. Call Claude API with prospect context

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  content-type: application/json
  anthropic-version: 2023-06-01

Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "messages": [
    {
      "role": "user",
      "content": "You are a solutions engineer preparing a technical deep-dive demo. Generate a structured demo script.\n\nProspect context:\n- Company: {company_name}\n- Tech stack: {tech_stack_list}\n- Technical requirements: {requirements_from_discovery}\n- Pain points: {pain_points}\n- Attendees: {attendee_names_and_titles}\n- Their current solution: {current_tooling}\n\nProduct context:\n- Architecture: {architecture_overview}\n- API docs: {api_endpoint_catalog}\n- Integration catalog: {available_integrations}\n- Security certifications: {security_certs}\n\nGenerate JSON:\n{\n  \"demo_modules\": [\n    {\n      \"module\": \"Architecture Overview\",\n      \"duration_minutes\": 5,\n      \"talking_points\": [\"...\"],\n      \"visual\": \"architecture diagram URL or description\",\n      \"prospect_connection\": \"why this matters to them specifically\"\n    },\n    {\n      \"module\": \"API Walkthrough\",\n      \"duration_minutes\": 8,\n      \"live_api_calls\": [\n        {\n          \"endpoint\": \"POST /api/v1/...\",\n          \"description\": \"what this does\",\n          \"request_body\": {},\n          \"expected_response\": {},\n          \"prospect_relevance\": \"maps to their requirement X\"\n        }\n      ],\n      \"talking_points\": [\"...\"]\n    },\n    {\n      \"module\": \"Integration Demo\",\n      \"duration_minutes\": 8,\n      \"integration_target\": \"tool from their tech stack\",\n      \"code_snippet\": \"...\",\n      \"prospect_connection\": \"replaces their current manual process\"\n    },\n    {\n      \"module\": \"Security & Compliance\",\n      \"duration_minutes\": 5,\n      \"topics\": [\"auth flow\", \"encryption\", \"compliance certs\"],\n      \"prospect_connection\": \"addresses their security concern X\"\n    }\n  ],\n  \"anticipated_questions\": [\n    {\n      \"question\": \"likely technical question\",\n      \"answer\": \"prepared response with specifics\",\n      \"supporting_doc\": \"link to relevant documentation\"\n    }\n  ],\n  \"technical_follow_up_package\": {\n    \"api_docs_links\": [\"...\"],\n    \"sdk_repos\": [\"...\"],\n    \"architecture_diagrams\": [\"...\"],\n    \"security_whitepapers\": [\"...\"],\n    \"integration_guides\": [\"...\"]\n  },\n  \"recommended_module_order\": [\"...\"],\n  \"total_duration_minutes\": 30\n}"
    }
  ]
}
```

### 2. Validate the response

Parse the JSON response. Verify:
- All `live_api_calls` reference real endpoints from the product API catalog
- All `integration_target` values match tools from the prospect's actual tech stack
- `total_duration_minutes` does not exceed 45 minutes (technical demos should be dense, not long)
- At least one module directly addresses the prospect's stated pain points

If validation fails, re-prompt with corrections.

### 3. Return the structured script

Return the validated JSON. Consuming drills (e.g., `demo-prep-automation`) will format this into a full demo prep document and store it in the CRM.

## Error Handling

- If the prospect's tech stack is unknown, generate a generic integration module covering the 3 most common integration patterns (REST webhook, native SDK, Zapier/n8n connector)
- If no discovery pain points are available, prioritize modules by what converts best historically (feed conversion data from `demo-performance-monitor` if available)
- If the API returns an error, retry once with a simplified prompt. If it fails again, log the error and fall back to a template demo script

## Output

- Structured JSON demo script with modules, talking points, live API calls, code snippets, and anticipated questions
- Technical follow-up package with documentation links
- Recommended module ordering optimized for the prospect's priorities
