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

1. Set volume target: 1,000 emails per week across all founder/sender profiles; confirm list source (Clay, Apollo) can supply enough qualified contacts.

2. In Instantly (or similar), create sequences that mirror your Baseline 3-step flow; configure send limits and warm-up per inbox.

3. Connect Instantly to Attio (or CRM) so every sent, opened, replied, and meeting is synced; add custom properties for reply rate and meeting rate.

4. In PostHog, create events or use existing ones for email_sent, email_replied, meeting_booked; ensure Instantly and CRM send these events via webhooks or integration.

5. In n8n, build a workflow that is triggered by PostHog events (e.g. email_replied): send a notification, update CRM, or trigger a follow-up action; log outcome back to PostHog.

6. Run list-building and enrichment in Clay or Apollo on a weekly cadence so you have a steady pipeline of 1,000+ contacts per week.

7. Launch sequences to the first batch of 500 contacts; monitor deliverability, open rate, and reply rate in the first 2 weeks.

8. Scale to 1,000 emails per week by adding more senders or more sequences; keep message and offer consistent with Baseline.

9. Each week, compute meeting rate and reply rate; ensure meeting rate stays within 20% of your Baseline rate (e.g. if Baseline was 2%, keep Scalable at or above 1.6%).

10. If metrics hold for 2 months, plan Durable: document current workflows and hand off to agent-driven optimization; if metrics drop, reduce volume or refine targeting before moving to Durable.

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
