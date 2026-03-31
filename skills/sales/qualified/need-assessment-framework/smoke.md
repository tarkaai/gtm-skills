---
name: need-assessment-framework-smoke
description: >
  Need Assessment Framework — Smoke Test. Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥10 need assessments completed in 1 week"
kpis: ["Need assessment completion rate", "Average need score", "Qualification rate", "Critical need identification rate"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - icp-definition
  - threshold-engine
---
# Need Assessment Framework — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** ≥10 need assessments completed in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. Create need assessment scorecard with 5-7 critical business needs your product addresses (e.g., reducing manual work, improving data accuracy, accelerating workflows).

2. On first 10 discovery calls, systematically ask about each need area: current pain severity (1-10), impact on business, attempted solutions, urgency of fixing.

3. Score each need on 3-point scale: Critical (3), Moderate (2), Low (1); calculate total need score out of 21 for 7 needs.

4. Set minimum viable need threshold: prospects must score ≥12 total with at least 2 Critical needs to qualify for continued engagement.

5. Log need scores in Attio custom fields immediately after each discovery call; track which specific needs resonate most by ICP segment.

6. Track PostHog events: need_assessment_completed, critical_need_identified, low_need_disqualified.

7. Compare deal progression: measure conversion rates for high-need (≥15) vs. medium-need (12-14) vs. low-need (<12) prospects.

8. Set pass threshold: Complete need assessments on ≥10 opportunities in 1 week with ≥60% meeting minimum viable need threshold.

9. Disqualify low-need prospects early to focus time on high-fit opportunities; document which need areas drive highest qualification rates.

10. If threshold met, document need assessment questions and proceed to Baseline; if not, refine needs or ICP targeting.

---

## KPIs to track
- Need assessment completion rate
- Average need score
- Qualification rate
- Critical need identification rate

---

## Pass threshold
**≥10 need assessments completed in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/need-assessment-framework`_
