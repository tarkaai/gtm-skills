---
name: bant-qualification-scalable
description: >
  BANT Qualification Framework — Scalable Automation. Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=35% qualification rate at 100+ leads/month over 2 months"
kpis: ["Qualification rate", "Pre-score accuracy", "Time saved by automation", "False positive rate"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
---
# BANT Qualification Framework — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** >=35% qualification rate at 100+ leads/month over 2 months

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
- **Cal.com** (Scheduling)

---

## Instructions

1. Target 100-200 leads per month; integrate Clay or Apollo with Attio to auto-enrich leads with firmographic data (revenue, funding, tech stack) before first call.

2. Build an n8n workflow triggered by Attio's new_lead event: pull enrichment data from Clay, run automated BANT pre-scoring based on firmographics, tag leads as high/medium/low priority.

3. Create BANT scoring rules in n8n: if company revenue >$5M = Budget green; if contact title includes "VP" or "Director" = Authority yellow; if tech stack includes competitor = Need green.

4. In Attio, segment leads by pre-score and assign discovery call priority; high-priority leads get call within 24 hours, medium within 3 days.

5. Set up PostHog to track pre-score accuracy: for every lead, log pre_score and post_call_score; measure how often pre-score matches final qualification.

6. Build a Cal.com integration that embeds BANT questions in the booking form; auto-populate Attio with answers before the call.

7. During discovery calls, validate pre-scored BANT fields and update discrepancies in Attio; n8n workflow logs corrections to PostHog for model improvement.

8. Each week, compute qualification rate, false positive rate (pre-scored high but disqualified), and time saved by pre-scoring; target >=35% qualification rate.

9. If pre-score accuracy is <70%, refine scoring rules in n8n based on PostHog analysis of false positives/negatives.

10. After 2 months, if qualification rate >=35% and pre-score accuracy >=70%, document automated BANT process and move to Durable; otherwise tune enrichment sources or scoring logic.

---

## KPIs to track
- Qualification rate
- Pre-score accuracy
- Time saved by automation
- False positive rate

---

## Pass threshold
**>=35% qualification rate at 100+ leads/month over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/bant-qualification`_
