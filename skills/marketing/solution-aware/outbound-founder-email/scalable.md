---
name: outbound-founder-email-scalable
description: >
  Outbound founder-led email — Scalable Automation. Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: "Meeting rate ≥ 1.6% over 2 months"
kpis: ["Reply rate", "Time to first reply", "Emails sent"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Outbound founder-led email — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Overview
Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** Meeting rate ≥ 1.6% over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

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

### 1. Scale list building
Run the `build-prospect-list` drill on a weekly cadence to source 1,000+ contacts per week. Use the `enrich-and-score` drill to run Clay enrichment waterfalls and score leads automatically. Use the `clay-scoring` fundamental to set up Tier 1/2/3 prioritization.

### 2. Set up automated email sequences
Run the `cold-email-sequence` drill at scale:
- Use `instantly-campaign` to create campaigns via API with 1,000 contacts/week
- Configure `instantly-warmup` across 6+ sending accounts for volume
- Use `smartlead-inbox-rotation` if using Smartlead for inbox rotation across domains

### 3. Build the automation layer
Run the `follow-up-automation` drill to connect everything via n8n:
- **Reply routing:** Instantly webhook -> n8n -> classify reply -> create Attio deal for positive replies
- **Lead sync:** Clay webhook -> n8n -> push enriched leads to Instantly campaign
- **Activity sync:** Instantly events -> n8n -> PostHog custom events + Attio activity logging

### 4. Set up GTM event tracking
Run the `posthog-gtm-events` drill to create a standard event taxonomy:
- `email_sent`, `email_replied`, `meeting_booked` events flowing from Instantly via n8n
- Properties: campaign_id, lead_source, lead_score, sequence_step
- Build a weekly outbound dashboard in PostHog using the `posthog-dashboards` fundamental

### 5. Launch and monitor
Start with 500 contacts in week 1, scale to 1,000 by week 3. Monitor weekly:
- Reply rate (target: maintain within 20% of Baseline)
- Meeting rate (target: ≥ 1.6%)
- Deliverability (open rate > 40%, bounce rate < 3%)

### 6. Iterate and prepare for Durable
If metrics hold for 2 months, document all workflows and prepare for agent-driven optimization. If metrics drop, reduce volume or refine targeting before scaling further.

---

## KPIs to track
- Reply rate
- Time to first reply
- Emails sent

---

## Pass threshold
**Meeting rate ≥ 1.6% over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-founder-email`_
