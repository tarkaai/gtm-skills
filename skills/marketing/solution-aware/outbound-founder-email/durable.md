---
name: outbound-founder-email-durable
description: >
  Outbound founder-led email — Durable Intelligence. Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Durable Intelligence"
time: "250 hours over 6 months"
outcome: "Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Reply rate", "Time to first reply", "Emails sent"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - multi-channel-cadence
  - dashboard-builder
  - ab-test-orchestrator
---
# Outbound founder-led email — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Overview
Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.

**Time commitment:** 250 hours over 6 months
**Pass threshold:** Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo

_Total play-specific: ~$100–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Instantly** (Email)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Apollo** (Enrichment)
- **Loops** (Email)

---

## Instructions

### 1. Build the unified dashboard
Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard:
- Reply rate, meeting rate, and pipeline value trending weekly
- Breakdown by campaign, ICP segment, and sequence variant
- Comparison to Scalable baseline metrics
- Use the `posthog-dashboards` fundamental to create via API

### 2. Set up A/B testing infrastructure
Run the `ab-test-orchestrator` drill to enable continuous experimentation:
- Use the `posthog-experiments` fundamental to create experiments
- Test one variable at a time: subject line, send time, sequence length, CTA
- Agent analyzes results via PostHog MCP and applies winning variant to Instantly

### 3. Build agent-driven optimization workflows
Use n8n to create AI-powered monitoring and optimization:
- **Weekly review:** Scheduled n8n workflow queries PostHog via API, compares current week to baseline, outputs recommendations
- **Auto-adjustment:** When a variant wins with 95% significance, the agent updates the Instantly campaign via API
- **Alert on degradation:** If meeting rate drops 20%+ below baseline for 2 consecutive weeks, trigger Slack alert with suggested corrective actions

### 4. Automate the full prospecting pipeline
Run the `multi-channel-cadence` drill to add LinkedIn and call touches alongside email:
- n8n orchestrates the cadence: email Day 0, LinkedIn Day 1, follow-up email Day 3, call Day 5
- Each touch logged to Attio and PostHog automatically
- Reply classification uses AI to route positive responses

### 5. Monitor deliverability and scaling health
Use n8n scheduled workflows to:
- Pull `instantly-warmup` health scores daily
- Alert when any account drops below 80% warmup score
- Suggest inbox rotation changes using the `smartlead-inbox-rotation` pattern
- Monitor Clay enrichment hit rates and credit usage

### 6. Continuous improvement cycle
Monthly review: which experiments improved meeting rate, which to retire, what new hypotheses to test. Agent runs the `threshold-engine` drill monthly to verify the play still passes. Adapt to seasonal and market changes by refreshing ICP criteria quarterly.

---

## KPIs to track
- Reply rate
- Time to first reply
- Emails sent

---

## Pass threshold
**Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-founder-email`_
