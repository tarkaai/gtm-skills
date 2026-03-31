---
name: outbound-founder-email-baseline
description: >
  Outbound founder-led email — Baseline Run. Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "≥ 2% meeting rate over 2 weeks"
kpis: ["Reply rate", "Time to first reply", "Emails sent"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Outbound founder-led email — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Overview
Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** ≥ 2% meeting rate over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Instantly** (Email)
- **PostHog** (CDP)

---

## Instructions

### 1. Refine your ICP
Run the `icp-definition` drill to expand your ICP with firmographic and role criteria. Define a list size target of 100 contacts for this 2-week run.

### 2. Build your prospect list
Run the `build-prospect-list` drill to source 100 contacts. This uses the `apollo-search` and `clay-table-setup` fundamentals to source contacts, then `clay-enrichment-waterfall` to enrich with verified emails, titles, and company data. Push qualified contacts to Attio using the `attio-contacts` fundamental.

### 3. Set up your email sequence
Run the `cold-email-sequence` drill to create a 3-step sequence in Instantly using the same structure that passed Smoke:
- Use the `instantly-campaign` fundamental to create the campaign via API
- Upload your enriched lead list from Clay
- Configure sending schedule (weekdays, 8-11am recipient timezone)
- Set daily limits to 20 sends and ramp after 3 days

### 4. Execute the campaign
Launch the Instantly campaign. In parallel, add one LinkedIn touch per lead where possible (connection request referencing your email). Log each touch in Attio.

### 5. Handle replies and route to CRM
Use the `instantly-reply-detection` fundamental to monitor Unibox. For positive replies, create deals in Attio at "Meeting Requested" stage. Send Cal.com booking link within 1 hour.

### 6. Measure against threshold
Run the `threshold-engine` drill after 2 weeks:
- **Pass:** ≥ 2% meeting rate from 100 contacts
- **If pass:** Document volume, conversion rates, and sequence. Proceed to Scalable.
- **If fail:** Refine list quality, adjust messaging, or switch ICP segment and re-run Baseline.

---

## KPIs to track
- Reply rate
- Time to first reply
- Emails sent

---

## Pass threshold
**≥ 2% meeting rate over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-founder-email`_
