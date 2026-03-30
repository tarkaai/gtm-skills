---
name: gtm-tools-automation-n8n
description: n8n-specific instructions for automation tasks in GTM plays. Reference when the user's configured automation platform is n8n.
---

# n8n — GTM Skills Reference

When a GTM skill says "set up automation" or "build a workflow", use n8n as follows:

## Setup
- Self-hosted (free): run via Docker or n8n.io cloud (free tier: 5 active workflows)
- n8n cloud: $20/mo for 5 workflows, unlimited runs

## Core patterns used in GTM plays

### Event-triggered workflow (Scalable + Durable levels)
```
Trigger: Webhook (from PostHog, CRM, or email tool)
  → Filter/condition node
  → Action (send email, update CRM, send Slack alert)
  → HTTP Request to PostHog (log outcome event)
```

### PostHog → n8n → CRM
1. PostHog → Destinations → Webhook → your n8n webhook URL
2. n8n: Webhook trigger → parse event → Attio/HubSpot/Salesforce node → update record

### Email tool reply → CRM update
1. Email tool (Instantly) → Webhook on reply
2. n8n: Webhook → find contact in CRM → update Sequence Status → notify Slack

### AI-personalized outreach (Durable level)
1. Schedule trigger (daily)
2. Fetch new leads from CRM or Clay
3. OpenAI/Anthropic node → generate personalized first line
4. Instantly/Smartlead node → add to sequence with custom intro
5. Log to PostHog

### A/B test orchestration (Durable level)
1. PostHog Feature Flag node → route to variant A or B workflow
2. Run different message variants
3. PostHog → log conversion event per variant
4. Weekly: check PostHog experiment results → update n8n to route to winner

## Tips
- Use n8n's "Error Trigger" node to catch failures and alert via Slack
- Use "Wait" nodes for time-delayed follow-ups instead of cron jobs
- n8n's Code node (JavaScript) lets you write custom logic when no native node exists
- For Durable plays, build modular sub-workflows called via the "Execute Workflow" node
- Store API keys in n8n Credentials (never hardcode)
