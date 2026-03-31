---
name: lead-routing
description: Automatically route inbound and outbound leads to the right owner based on criteria
category: Operations
tools:
  - Attio
  - n8n
fundamentals:
  - attio-automation
  - attio-deals
  - n8n-triggers
  - n8n-workflow-basics
---

# Lead Routing

This drill builds automated lead routing so every new lead is assigned to the right person immediately. Manual routing introduces delays that kill conversion rates.

## Prerequisites

- Attio pipeline configured (run `crm-pipeline-setup` drill first)
- n8n instance running with Attio integration
- Clear ownership rules defined (by territory, deal size, source, etc.)

## Steps

### 1. Define routing rules

Establish your routing criteria. Common rules: deals over $50K go to a senior rep, inbound leads go to the inbound team, specific industries go to the specialist, geographic territories assign by region. Document these rules before building automation.

### 2. Build the routing workflow in n8n

Use the `n8n-triggers` fundamental to set up a trigger for new deal creation in Attio. Use the `n8n-workflow-basics` fundamental to build the routing logic: IF nodes branch on deal value, source, industry, and geography. Each branch updates the Owner field on the deal via the Attio MCP.

### 3. Handle round-robin assignment

For leads that don't match specific rules, implement round-robin distribution. Use an n8n Code node to track the last-assigned rep and rotate to the next one.

### 4. Set up notifications

When a lead is routed, notify the assigned owner via Slack or email with deal details: company, contact, value, and source. Speed-to-lead matters.

### 5. Handle edge cases

Build fallback routing for: unassigned territories, owner on vacation (re-route to backup), and duplicate leads (merge with existing deal instead of creating new).

### 6. Monitor routing effectiveness

Track: average time from lead creation to first contact, routing accuracy (% correctly assigned), and conversion rates by assigned owner.
