---
name: call-transcript-tech-requirements-extraction
description: Extract technical requirements, integration needs, security constraints, and infrastructure preferences from call transcripts using LLM analysis
tool: Fireflies + Anthropic
difficulty: Advanced
---

# Extract Technical Requirements from Call Transcripts

Parse discovery or technical call transcripts to identify integration requirements, security/compliance needs, infrastructure constraints, performance expectations, and data migration demands. Returns structured technical requirements with fit scores and blocker flags.

## Prerequisites

- Fireflies account with transcribed calls (see `fireflies-transcription`)
- Anthropic API key (Claude) for LLM analysis
- n8n instance for automation (optional but recommended)

## Steps

### 1. Retrieve the transcript

Fetch the full transcript from Fireflies using the GraphQL API:

```graphql
query {
  transcript(id: "<transcript-id>") {
    title
    sentences {
      speaker_name
      text
      start_time
      end_time
    }
    summary
    action_items
  }
}
```

Alternatively, if using Gong: `GET /v2/calls/{call_id}/transcript` with Bearer token.

### 2. Run technical requirements extraction via Claude API

Send the transcript to Claude with a structured extraction prompt:

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
    "content": "Analyze this technical discovery call transcript and extract all technical requirements. Return JSON only.\n\nTranscript:\n{transcript_text}\n\nReturn this exact JSON structure:\n{\n  \"integrations\": {\n    \"score\": 0-100,\n    \"requirements\": [\n      {\n        \"system\": \"name of system to integrate with\",\n        \"type\": \"api|sso|data_sync|webhook|file_import|native\",\n        \"priority\": \"must_have|nice_to_have\",\n        \"complexity\": \"simple|moderate|complex|custom_dev\",\n        \"quote\": \"exact prospect quote\"\n      }\n    ],\n    \"blockers\": [\"any integration that would block the deal\"]\n  },\n  \"security_compliance\": {\n    \"score\": 0-100,\n    \"certifications_required\": [\"SOC2|GDPR|HIPAA|ISO27001|FedRAMP|PCI_DSS|other\"],\n    \"requirements\": [\n      {\n        \"area\": \"data_residency|encryption|access_control|audit_logging|pen_testing|vendor_review\",\n        \"detail\": \"specific requirement\",\n        \"priority\": \"must_have|nice_to_have\",\n        \"quote\": \"exact prospect quote\"\n      }\n    ],\n    \"blockers\": [\"any security requirement that would block the deal\"]\n  },\n  \"infrastructure\": {\n    \"score\": 0-100,\n    \"deployment_preference\": \"cloud_saas|private_cloud|on_premise|hybrid\",\n    \"cloud_provider\": \"aws|azure|gcp|other|unknown\",\n    \"requirements\": [\n      {\n        \"area\": \"hosting|networking|disaster_recovery|backup|environment_isolation\",\n        \"detail\": \"specific requirement\",\n        \"priority\": \"must_have|nice_to_have\",\n        \"quote\": \"exact prospect quote\"\n      }\n    ],\n    \"blockers\": []\n  },\n  \"performance\": {\n    \"score\": 0-100,\n    \"requirements\": [\n      {\n        \"area\": \"uptime_sla|latency|throughput|concurrent_users|data_volume\",\n        \"target\": \"specific number or range\",\n        \"priority\": \"must_have|nice_to_have\",\n        \"quote\": \"exact prospect quote\"\n      }\n    ],\n    \"user_volume\": \"estimated number of users or unknown\",\n    \"data_volume\": \"estimated data volume or unknown\",\n    \"blockers\": []\n  },\n  \"data_migration\": {\n    \"score\": 0-100,\n    \"current_systems\": [\"systems data must migrate from\"],\n    \"requirements\": [\n      {\n        \"area\": \"data_format|migration_timeline|data_volume|historical_data|mapping_complexity\",\n        \"detail\": \"specific requirement\",\n        \"priority\": \"must_have|nice_to_have\",\n        \"quote\": \"exact prospect quote\"\n      }\n    ],\n    \"blockers\": []\n  },\n  \"tech_stack_context\": {\n    \"existing_tools\": [\"tools/platforms mentioned by prospect\"],\n    \"tech_maturity\": \"early_stage|growing|mature|enterprise\",\n    \"internal_technical_resources\": \"none|limited|moderate|strong\",\n    \"decision_influencers\": [\"technical stakeholders mentioned by name/role\"]\n  },\n  \"composite_fit_score\": 0-100,\n  \"total_blockers\": [\"combined list of all blockers across categories\"],\n  \"technical_verdict\": \"strong_fit|moderate_fit|weak_fit|no_fit\",\n  \"gaps_requiring_followup\": [\"areas where requirements are unclear and need another conversation\"],\n  \"recommended_next_steps\": [\"specific actions to address gaps or blockers\"]\n}"
  }]
}
```

### 3. Parse and validate the response

Parse the JSON response. Validate:
- All five category scores are between 0-100
- `composite_fit_score` equals the weighted average: Integrations (30%) + Security (25%) + Infrastructure (15%) + Performance (15%) + Data Migration (15%)
- `technical_verdict` matches: strong_fit (>=75), moderate_fit (50-74), weak_fit (25-49), no_fit (<25)
- Every blocker has a corresponding requirement entry with `priority: must_have`

If validation fails, re-prompt with the error.

### 4. Store results in CRM

Push the structured technical requirements to Attio via MCP or API:

```json
{
  "data": {
    "values": {
      "tech_integrations_score": [{"value": 70}],
      "tech_security_score": [{"value": 85}],
      "tech_infrastructure_score": [{"value": 90}],
      "tech_performance_score": [{"value": 65}],
      "tech_migration_score": [{"value": 50}],
      "tech_composite_fit_score": [{"value": 72}],
      "tech_verdict": [{"value": "moderate_fit"}],
      "tech_blocker_count": [{"value": 2}],
      "tech_blockers_summary": [{"value": "Requires HIPAA certification; Needs native Salesforce integration"}],
      "tech_last_assessed": [{"value": "2026-03-30T00:00:00Z"}],
      "tech_assessment_source": [{"value": "discovery_call"}]
    }
  }
}
```

### 5. Log the extraction event

Fire a PostHog event for tracking:
```json
{
  "event": "tech_requirements_extraction_completed",
  "properties": {
    "deal_id": "...",
    "composite_fit_score": 72,
    "verdict": "moderate_fit",
    "blocker_count": 2,
    "integration_count": 4,
    "certifications_required": ["HIPAA", "SOC2"],
    "source": "call_transcript",
    "call_id": "..."
  }
}
```

## Error Handling

- **No transcript available:** Skip extraction, log `tech_requirements_extraction_skipped` event with reason `no_transcript`.
- **LLM returns malformed JSON:** Retry once with explicit instruction to return valid JSON only. If still malformed, flag for manual review.
- **Transcript too short (< 50 words):** Likely a no-show or quick cancel. Skip extraction.
- **No technical content in transcript:** If the LLM determines the call had no technical discussion, return all scores as 0 with `gaps_requiring_followup: ["No technical requirements discussed — schedule a dedicated technical discovery call"]`.
- **Rate limit on Anthropic API:** Back off exponentially starting at 5 seconds.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Fireflies + Claude | GraphQL API + Anthropic API | Best for async extraction |
| Gong + Claude | REST API + Anthropic API | Better call analytics built-in; Gong can tag technical topics automatically |
| Fireflies + OpenAI | GraphQL API + OpenAI API | Alternative LLM provider |
| Chorus + Claude | REST API + Anthropic API | Owned by ZoomInfo |
| Manual review | Human listens to recording | Fallback when automation fails |
