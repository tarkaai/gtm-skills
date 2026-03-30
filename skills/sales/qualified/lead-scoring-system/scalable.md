---
name: lead-scoring-system-scalable
description: >
  Lead Scoring System — Scalable Automation. Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "Hot leads convert at >=4x rate vs Cold leads over 2 months"
kpis: ["Conversion rate by tier", "Score decay impact", "Time to contact by tier", "Rep efficiency (pipeline per hour)"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
---
# Lead Scoring System — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.

**Time commitment:** 65 hours over 2 months
**Pass threshold:** Hot leads convert at >=4x rate vs Cold leads over 2 months

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
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)

---

## Instructions

1. Scale to 500+ leads per month; integrate Clay with Attio to auto-enrich leads with fit data (revenue, employee count, tech stack) before scoring.

2. Build an n8n workflow that triggers on new_lead in Attio: pull enrichment from Clay, calculate fit score, pull intent behaviors from PostHog, calculate intent score, assign tier, log to PostHog.

3. Expand scoring model to 10+ fit attributes and 10+ intent signals; use weighted average so high-intent can overcome weak fit and vice versa.

4. Set up PostHog to track score changes over time; create a cohort of leads that move from Cold → Warm → Hot to understand intent progression.

5. In Attio, create smart lists for Hot/Warm/Cold leads; assign auto-routing rules so Hot leads go to senior reps, Warm to mid-level, Cold to SDRs.

6. Build a lead scoring dashboard in PostHog showing score distribution, meeting conversion by tier, and time-to-contact by tier; target >=4x conversion for Hot vs Cold.

7. Implement score decay: if a lead has no intent activity for 14 days, reduce intent score by 50%; prevents stale high-scorers from clogging pipeline.

8. Each week, analyze which fit+intent combinations yield highest close rates; adjust point values in n8n workflow to reflect learning.

9. Track outreach velocity: are reps contacting Hot leads within 24 hours? If not, set up automated alerts in n8n when Hot leads aren't contacted quickly.

10. After 2 months, if Hot leads convert >=4x better and reps report higher pipeline efficiency, move to Durable; otherwise refine scoring model or routing rules.

---

## KPIs to track
- Conversion rate by tier
- Score decay impact
- Time to contact by tier
- Rep efficiency (pipeline per hour)

---

## Pass threshold
**Hot leads convert at >=4x rate vs Cold leads over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/lead-scoring-system`_
