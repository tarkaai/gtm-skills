---
name: lead-scoring-system-baseline
description: >
  Lead Scoring System — Baseline Run. Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Hot leads convert at >=3x rate vs Cold leads over 2 weeks"
kpis: ["Meeting rate by tier", "Score accuracy", "False negative rate", "Time to contact by tier"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Lead Scoring System — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** Hot leads convert at >=3x rate vs Cold leads over 2 weeks

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
- **PostHog** (CDP)
- **Clay** (Enrichment)

---

## Instructions

1. Expand to 100 leads over 2 weeks; build a lead scoring model in Attio with fit attributes (company size, industry, role, tech stack) and intent behaviors (website visits, email opens, content downloads).

2. Assign points: fit (company >$5M = 15pts, target industry = 10pts, decision-maker role = 15pts, uses competitor = 10pts) and intent (demo request = 30pts, pricing page = 20pts, case study = 10pts).

3. Set pass threshold: >=30% of leads score as Hot (>=80), and Hot leads have >=3x meeting rate vs Cold (<50) over 2 weeks.

4. Integrate PostHog with Attio to automatically log intent behaviors; configure PostHog to send lead_behavior events (page_viewed, email_clicked) to Attio with scores.

5. In Attio, create an automation that updates lead score in real-time as PostHog events arrive; recalculate score daily and update tier (Hot/Warm/Cold).

6. Prioritize outreach: contact Hot leads within 24 hours, Warm leads within 3 days, Cold leads within 7 days; log all outreach in Attio.

7. Track meeting conversion rate by tier in PostHog; create a funnel showing lead_scored → outreach_sent → meeting_booked by score tier.

8. After 2 weeks, analyze: did >=30% score as Hot? Did Hot leads convert >=3x better? If not, adjust point values or add/remove signals.

9. Identify leads that scored Cold but booked meetings (false negatives); investigate what signals were missed and add to scoring model.

10. If Hot leads convert >=3x better and score distribution is balanced, document scoring model and proceed to Scalable; otherwise iterate on fit criteria or intent signals.

---

## KPIs to track
- Meeting rate by tier
- Score accuracy
- False negative rate
- Time to contact by tier

---

## Pass threshold
**Hot leads convert at >=3x rate vs Cold leads over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/lead-scoring-system`_
