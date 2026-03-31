---
name: bant-qualification-smoke
description: >
  BANT Qualification Framework — Smoke Test. Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 qualified leads in 1 week"
kpis: ["Qualification rate", "Time to qualify", "Discovery call completion rate"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
drills:
  - icp-definition
  - threshold-engine
---
# BANT Qualification Framework — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** >=3 qualified leads in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Cal.com** (Scheduling)

---

## Instructions

1. Create a BANT scorecard in a spreadsheet with columns for Budget (yes/no), Authority (yes/no), Need (1-5), Timeline (<3mo, 3-6mo, >6mo), and overall score.

2. Identify 5-10 recent inbound leads or outbound replies from your CRM; for each, fill out the BANT scorecard based on available information.

3. Set a pass threshold: at least 3 out of 5 leads must score "qualified" (Budget=yes, Authority=yes, Need>=3, Timeline<=6mo) to proceed.

4. For leads missing BANT data, draft 3-5 discovery questions per category (e.g., Budget: "Do you have budget allocated?"; Authority: "Who else needs to approve this?").

5. Schedule discovery calls with 5 leads; during each call, ask your BANT questions and take notes in the scorecard.

6. After each call, update the lead's BANT score in the spreadsheet and log the outcome in Attio with a custom field for BANT status.

7. Track how many leads qualify vs disqualify; if >=3 qualify in 1 week, your BANT criteria are working.

8. Log qualification outcomes in PostHog as events (lead_qualified, lead_disqualified) with BANT properties for analysis.

9. Compare time spent on qualified vs unqualified leads; calculate time saved by early disqualification.

10. If >=3 leads qualified and you saved >2 hours by disqualifying bad fits early, document your BANT questions and thresholds, then proceed to Baseline; otherwise refine criteria.

---

## KPIs to track
- Qualification rate
- Time to qualify
- Discovery call completion rate

---

## Pass threshold
**>=3 qualified leads in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/bant-qualification`_
