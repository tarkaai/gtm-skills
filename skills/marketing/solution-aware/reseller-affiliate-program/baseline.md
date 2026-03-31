---
name: reseller-affiliate-program-baseline
description: >
    Reseller & Affiliate Program — Baseline Run. Recruit partners to sell your product for
  commission, expanding reach and generating leads from solution-aware audiences through partner
  networks.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥10 active partners and ≥8 partner-sourced deals in 10 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - warm-intro-request
  - posthog-gtm-events
---
# Reseller & Affiliate Program — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Overview
Reseller & Affiliate Program — Baseline Run. Recruit partners to sell your product for commission, expanding reach and generating leads from solution-aware audiences through partner networks.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥10 active partners and ≥8 partner-sourced deals in 10 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Formalize partner outreach
Run the `warm-intro-request` drill to build a systematic intro request process: identify mutual connections in your network, craft personalized intro requests, and track request-to-intro conversion rates.

### 2. Configure partnership tracking
Run the `posthog-gtm-events` drill to track: `reseller-affiliate-program_partner_contacted`, `reseller-affiliate-program_intro_received`, `reseller-affiliate-program_collab_launched`, `reseller-affiliate-program_lead_from_partner`. Attribute pipeline to specific partnerships.

### 3. Execute 5-10 partnerships over 2-4 weeks
Run the collaborations: content swaps, co-promotions, intro exchanges, or joint webinars. Track results from each partnership individually to identify which partners and formats drive the most value.

### 4. Evaluate against threshold
Measure against: ≥10 active partners and ≥8 partner-sourced deals in 10 weeks. If PASS, proceed to Scalable. If FAIL, focus on the partnership format that showed the most promise and try different partners.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥10 active partners and ≥8 partner-sourced deals in 10 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/reseller-affiliate-program`_
