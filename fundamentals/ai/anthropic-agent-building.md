---
name: anthropic-agent-building
description: Build autonomous GTM agents using Claude that monitor metrics and execute plays
tool: Anthropic
difficulty: Advanced
---

# Build GTM Agents with Claude

### What is a GTM agent?
An autonomous agent that monitors your PostHog metrics, identifies when plays need adjustment, and takes action — updating sequences, pausing underperformers, or escalating to the founder.

### Architecture
1. **Trigger:** n8n cron job runs every 24h (or on PostHog alert)
2. **Gather:** Agent pulls current metrics from PostHog MCP, deal status from Attio MCP
3. **Analyze:** Claude evaluates metrics against play thresholds and the 20% guardrail rule
4. **Decide:** Agent chooses: continue, adjust, pause, or escalate
5. **Act:** Agent executes the decision via n8n (update sequences, send alerts, modify campaigns)
6. **Report:** Agent logs its decision and reasoning to a shared channel

### Guardrails
- Always require human approval for: budget increases >20%, new play launches, pipeline deletions
- Log every agent decision with reasoning for audit
- Set hard stops: if conversion drops >40%, pause all automation and alert the founder
