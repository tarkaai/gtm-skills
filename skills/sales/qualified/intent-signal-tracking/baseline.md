---
name: intent-signal-tracking-baseline
description: >
  Intent Signal Tracking — Baseline Run. Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=20 high-intent accounts and >=35% reply rate over 2 weeks"
kpis: ["High-intent accounts per week", "Reply rate by intent tier", "Signal-to-outreach time", "Meeting rate by intent"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Intent Signal Tracking — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** >=20 high-intent accounts and >=35% reply rate over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Instantly** (Email)

---

## Instructions

1. Expand intent tracking to 50+ accounts over 2 weeks; create an intent scoring model where each signal has a point value (demo request=30, pricing page=15, case study=10, etc.).

2. In PostHog, set up cohorts for accounts with high intent (>=40 points), medium intent (20-39), and low intent (<20); track cohort size daily.

3. Set pass threshold: >=20 accounts reach high intent over 2 weeks, and high-intent outreach yields >=35% reply rate and >=20% meeting rate.

4. Build a daily workflow: each morning, query PostHog for accounts that crossed into high intent in the past 24 hours; export to Attio with intent score and signal breakdown.

5. For high-intent accounts, use Clay to enrich with firmographics, find decision-makers, and pull recent company news; prioritize accounts with recent funding or executive hires.

6. Send personalized emails within 4 hours of intent signal; reference specific behaviors ("Noticed your team has been exploring our API docs—here's a sandbox to test").

7. Sync Attio to PostHog so every outreach logs an intent_outreach_sent event; track response time and meeting conversion by intent tier.

8. For medium-intent accounts, add to nurture sequence; for low-intent accounts, add to retargeting audience but don't reach out yet.

9. After 2 weeks, analyze: which signals most strongly predict reply/meeting? Adjust point values to boost high-signal behaviors.

10. If >=20 accounts reach high intent and reply rate >=35%, document intent model and move to Scalable; otherwise refine signals or account enrichment.

---

## KPIs to track
- High-intent accounts per week
- Reply rate by intent tier
- Signal-to-outreach time
- Meeting rate by intent

---

## Pass threshold
**>=20 high-intent accounts and >=35% reply rate over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/intent-signal-tracking`_
