---
name: tool-sync-workflow
description: Build n8n workflows that keep your GTM tools in sync automatically
category: Operations
tools:
  - n8n
  - Attio
  - PostHog
  - Instantly
  - Loops
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - n8n-error-handling
  - n8n-crm-integration
  - n8n-email-integration
---

# Tool Sync Workflow

This drill builds the n8n automation layer that connects all your GTM tools. Without sync workflows, data gets siloed and manual data entry wastes hours every week.

## Prerequisites

- n8n instance running with MCP connected
- All GTM tool API keys configured in n8n credentials
- Attio CRM as the central data hub

## Steps

### 1. Map your data flows

Define what data needs to flow between tools: Clay enriched leads -> Attio contacts, Instantly replies -> Attio deals, PostHog product events -> Attio contact properties, Attio deal stages -> Loops segments. Draw the flow before building.

### 2. Build the enrichment-to-CRM sync

Use the `n8n-crm-integration` fundamental. Create a workflow: Clay webhook (new enriched row) -> Set node (map fields) -> Attio node (create/update contact). Handle deduplication by searching Attio by email first.

### 3. Build the email-to-CRM sync

Use the `n8n-email-integration` fundamental. Create workflows for: Instantly reply received -> classify intent -> create deal for positive replies. Loops unsubscribe -> update Attio contact opt-out status.

### 4. Build the product-to-CRM sync

Create a workflow: PostHog webhook (key product events) -> Attio node (update contact properties with usage data). This enriches your CRM with product engagement data.

### 5. Add error handling and monitoring

Use the `n8n-error-handling` fundamental. Configure error workflows, retry logic, and Slack alerts. Build a daily health check workflow that verifies all sync workflows ran successfully.

### 6. Schedule data hygiene

Use the `n8n-scheduling` fundamental. Build weekly workflows for: stale deal alerts, duplicate contact detection, and sync status reporting. These keep your data clean as volume grows.
