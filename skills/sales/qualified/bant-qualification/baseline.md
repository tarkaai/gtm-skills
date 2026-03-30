---
name: bant-qualification-baseline
description: >
  BANT Qualification Framework — Baseline Run. Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=40% qualification rate over 2 weeks"
kpis: ["Qualification rate", "Time to qualify", "Disqualification reasons", "Call-to-qualified conversion"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
---
# BANT Qualification Framework — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** >=40% qualification rate over 2 weeks

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
- **Cal.com** (Scheduling)
- **Clay** (Enrichment)

---

## Instructions

1. Expand your BANT scorecard to 20-30 leads; add scoring weights (Budget=25%, Authority=25%, Need=30%, Timeline=20%) and threshold (>=70% to qualify).

2. Build a BANT question library in Attio with 5-7 questions per category; tag each with expected answer patterns (red flag, yellow flag, green flag).

3. Create a discovery call template in Attio that auto-populates BANT questions based on lead source and industry.

4. Set pass threshold: qualify >=40% of leads over 2 weeks and reduce time-to-qualify to <48 hours from first call.

5. Conduct 20-30 discovery calls over 2 weeks; for each call, complete the BANT scorecard within 24 hours and update Attio.

6. Sync Attio to PostHog so every BANT update triggers a lead_scored event with BANT breakdown and timestamp.

7. In PostHog, create a funnel: discovery_call_completed → lead_scored → lead_qualified; measure conversion rate and time between stages.

8. For disqualified leads, tag disqualification reason (no budget, wrong authority, weak need, long timeline) in Attio and PostHog.

9. After 2 weeks, analyze which BANT criteria most often disqualify leads; refine weighting or thresholds if <40% qualify.

10. If qualification rate is >=40% and time-to-qualify <=48 hours, document BANT process and move to Scalable; otherwise iterate on questions or scoring model.

---

## KPIs to track
- Qualification rate
- Time to qualify
- Disqualification reasons
- Call-to-qualified conversion

---

## Pass threshold
**>=40% qualification rate over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/bant-qualification`_
