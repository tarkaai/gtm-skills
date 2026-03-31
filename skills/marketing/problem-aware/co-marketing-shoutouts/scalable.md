---
name: co-marketing-shoutouts-scalable
description: >
    Partner Newsletter Shoutout — Scalable Automation. Run a short co-marketing blurb in a partner
  newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 200 clicks and ≥ 15 leads over 2 months"
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - follow-up-automation
  - tool-sync-workflow
---
# Partner Newsletter Shoutout — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Overview
Partner Newsletter Shoutout — Scalable Automation. Run a short co-marketing blurb in a partner newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 200 clicks and ≥ 15 leads over 2 months

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
Measure against: ≥ 200 clicks and ≥ 15 leads over 2 months. If PASS, proceed to Durable. If FAIL, consolidate to the top 5 highest-performing partnerships.

---

## KPIs to track
- Impressions
- Click-through rate

---

## Pass threshold
**≥ 200 clicks and ≥ 15 leads over 2 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts`_
