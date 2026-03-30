---
name: gtm-tools-automation-make
description: Make (formerly Integromat) instructions for automation tasks in GTM plays. Reference when the user's configured automation platform is Make.
---

# Make — GTM Skills Reference

When a GTM skill says "set up automation" or "build a workflow", use Make as follows:

## Setup
- Make.com free tier: 1,000 operations/mo, 2 active scenarios
- Core team: $9/mo for 10,000 operations
- Scenarios are Make's equivalent of n8n workflows

## Core patterns used in GTM plays

### Scalable: Email reply → CRM update
1. Trigger: Webhooks module (catch reply from email tool)
2. Router: branch on reply type (positive / negative / auto-reply)
3. CRM module (HubSpot / Attio / Salesforce): update contact status
4. Slack module: notify founder of positive reply
5. HTTP module: POST event to PostHog

### Scalable: Lead enrichment pipeline
1. Trigger: Google Sheets / Airtable new row (new lead added)
2. HTTP module: POST to Clay API for enrichment
3. CRM module: create/update contact with enriched data
4. Email tool module: add to sequence
5. PostHog HTTP: log `lead.enriched` event

### Durable: PostHog → Make → action
1. Trigger: Webhooks (PostHog destination webhook)
2. JSON parse event
3. Filter module: only process specific events (e.g., `user.churned`)
4. Branch: run different re-engagement sequences based on user segment
5. Email tool: enroll in winback sequence
6. CRM: update account health status

### A/B test routing
1. Trigger: new lead webhook
2. Make's "Random" or "Incrementer" module → assign variant A or B
3. Branch per variant → different email sequences
4. PostHog HTTP: log variant assignment as feature flag event

## Tips
- Make's visual canvas is easier to debug than n8n for non-technical users
- Use Make's "Error handler" route to catch failures gracefully
- Data stores (Make's built-in key-value store) can replace simple databases for Scalable plays
- For Durable plays requiring complex AI logic, consider augmenting Make with Claude Code scripts triggered via webhooks
- Make has native modules for most GTM tools: HubSpot, Salesforce, Instantly, Clay, Slack, PostHog (via HTTP)
