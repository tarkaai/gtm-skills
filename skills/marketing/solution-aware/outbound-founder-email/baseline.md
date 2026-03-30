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

1. Expand your ICP brief with firmographic and role criteria; define list size target of 100 contacts for this 2-week run.

2. Build a list of 100 contacts using Apollo, Clay, or LinkedIn Sales Nav; enrich with verified email and role; export to a spreadsheet or CRM (Attio).

3. Create a 3-step email sequence in Instantly (or similar) or send manually: intro, follow-up at day 4, final follow-up with Calendly at day 8; use the same structure that passed Smoke.

4. Add one LinkedIn touch (connection request or InMail) and one call attempt per lead where possible; log each touch in the CRM.

5. Set pass threshold for Baseline: e.g. ≥ 1.5–2.5% meeting rate over 2 weeks; define where you will log every outcome (PostHog and CRM).

6. Sync leads and activity from your email tool and CRM to PostHog so you have a single view of sent, opened, replied, meeting booked.

7. Send the sequence to all 100 contacts over the first 3–5 days; execute LinkedIn and call touches according to your cadence.

8. Log every reply, meeting booked, and no-response in PostHog and the CRM; tag positive replies and meetings for follow-up.

9. At the end of 2 weeks, compute meeting rate, reply rate, and cycle time (first touch to meeting).

10. Compare to pass threshold. If pass, document volume and conversion rates and proceed to Scalable; if fail, switch pillar, refine list quality, or adjust offer and re-run Baseline.

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
