---
name: crm-pipeline-setup
description: Set up your Attio CRM pipeline with stages, views, and automations for GTM tracking
category: Operations
tools:
  - Attio
  - n8n
fundamentals:
  - attio-pipeline-config
  - attio-contacts
  - attio-deals
  - attio-automation
  - n8n-crm-integration
---

# CRM Pipeline Setup

This drill configures your Attio CRM from scratch: pipeline stages, required fields, views, and basic automations. A well-configured pipeline is the foundation for all GTM measurement.

## Prerequisites

- Attio workspace with admin access
- Attio MCP server connected (see `attio-mcp-setup` fundamental)
- n8n instance running (see `n8n-mcp-setup` fundamental)

## Steps

### 1. Configure the pipeline

Use the `attio-pipeline-config` fundamental to create your Deal object with stages: Lead, Qualified, Meeting Booked, Proposal Sent, Negotiation, Closed Won, Closed Lost. Add required fields: Company, Contact, Deal Value, Expected Close Date, Source.

### 2. Set up contact management

Use the `attio-contacts` fundamental to configure your People object. Set up required fields, role tagging, and duplicate detection. Every contact must link to a Company record.

### 3. Create deal management workflows

Use the `attio-deals` fundamental to establish deal creation, stage progression, and closing patterns. Define your naming convention and activity logging requirements.

### 4. Build automations

Use the `attio-automation` fundamental with n8n to create: stage-change triggers, auto-assignment rules, stale deal alerts, and cross-tool sync (email bounces updating contact status).

### 5. Connect to other tools

Use the `n8n-crm-integration` fundamental to build bi-directional sync between Attio and your email tools, enrichment platform, and analytics.

### 6. Verify the setup

Create a test deal and run it through every stage. Verify automations fire, views display correctly, and data syncs properly. Delete test data when confirmed.
