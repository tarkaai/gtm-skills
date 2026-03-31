---
name: outbound-founder-email-smoke
description: >
  Outbound founder-led email — Smoke Test. Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 2 meetings in 1 week"
kpis: ["Reply rate", "Time to first reply", "Emails sent"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
  - threshold-engine
---
# Outbound founder-led email — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Overview
Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.

**Time commitment:** 4 hours over 1 week
**Pass threshold:** ≥ 2 meetings in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Instantly** (Email)

---

## Instructions

### 1. Define your ICP
Run the `icp-definition` drill to define your Ideal Customer Profile. Document industry, role, company size, and pain points. At Smoke level this is manual -- write a short brief.

### 2. Source 10 prospects manually
Search Apollo or LinkedIn for 10 contacts matching your ICP. For each, collect: email, first name, last name, company, title, and one personalization hook (recent news, tech stack, hiring signal). Log them in Attio using the `attio-contacts` fundamental.

### 3. Write a 3-step email sequence
Write your emails manually at Smoke level (no automation tool needed):
- **Step 1 (Day 0):** Personalized opener referencing the hook, clear value prop, soft CTA
- **Step 2 (Day 3):** Different angle, lead with value
- **Step 3 (Day 7):** Include Cal.com booking link as the CTA

Send from the founder's primary email. Keep each email under 100 words.

### 4. Send manually and track
Send all 10 intro emails. Schedule follow-ups in your calendar. Log each send in Attio with status: Sent, Replied, Meeting Booked, No Response.

### 5. Handle replies
Respond to positive replies within 1 hour. Use the `attio-deals` fundamental to create a deal at "Meeting Requested" stage for every positive reply.

### 6. Measure against threshold
Run the `threshold-engine` drill to evaluate results after 7 days:
- **Pass:** ≥ 2 meetings from 10 emails
- **If pass:** Document the winning ICP and sequence, proceed to Baseline
- **If fail:** Adjust ICP, messaging, or list source and re-run Smoke

---

## KPIs to track
- Reply rate
- Time to first reply
- Emails sent

---

## Pass threshold
**≥ 2 meetings in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-founder-email`_
