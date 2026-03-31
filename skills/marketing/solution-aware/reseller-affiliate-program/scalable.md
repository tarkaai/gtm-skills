---
name: reseller-affiliate-program-scalable
description: >
    Reseller & Affiliate Program — Scalable Automation. Recruit partners to sell your product for
  commission, expanding reach and generating leads from solution-aware audiences through partner
  networks.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥30 active partners and ≥25 partner-sourced deals/quarter over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - follow-up-automation
  - tool-sync-workflow
---
# Reseller & Affiliate Program — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Overview
Reseller & Affiliate Program — Scalable Automation. Recruit partners to sell your product for commission, expanding reach and generating leads from solution-aware audiences through partner networks.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥30 active partners and ≥25 partner-sourced deals/quarter over 6 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate partner workflows
Run the `follow-up-automation` drill to build n8n workflows: auto-track partner referrals via UTM parameters, auto-create Attio deals from partner-sourced leads, and auto-send partner performance reports monthly.

### 2. Build partner ecosystem
Run the `tool-sync-workflow` drill to connect: partner referral tracking to Attio deals, PostHog events to partner attribution, and Loops emails for partner nurture sequences.

### 3. Scale partnerships
Expand to 20+ active partnerships. Systematize the collaboration formats that worked. Create templates and playbooks for common partnership types.

### 4. Evaluate against threshold
Measure against: ≥30 active partners and ≥25 partner-sourced deals/quarter over 6 months. If PASS, proceed to Durable. If FAIL, consolidate to the top 5 highest-performing partnerships.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥30 active partners and ≥25 partner-sourced deals/quarter over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/reseller-affiliate-program`_
