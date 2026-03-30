---
name: poc-management-framework-smoke
description: >
  POC Management Framework — Smoke Test. Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Smoke Test"
time: "10 hours over 2 weeks"
outcome: "Structured POCs completed on ≥5 opportunities in 2 weeks"
kpis: ["POC completion rate", "Success criteria achievement", "POC-to-proposal conversion", "Time to decision"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
---
# POC Management Framework — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Overview
Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.

**Time commitment:** 10 hours over 2 weeks
**Pass threshold:** Structured POCs completed on ≥5 opportunities in 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 5-6 opportunities requiring POC, establish POC framework: define success criteria, timeline (typically 1-2 weeks), resources needed, stakeholder responsibilities.

2. Create POC kickoff doc: document what will be tested, success metrics, timeline, who's involved from both sides, what happens after POC (decision process).

3. Set up POC environment: provision trial account or sandbox with necessary integrations, data, and configurations; ensure prospect can access immediately.

4. Schedule POC kickoff call: review success criteria, demonstrate setup, walk through test scenarios, answer initial questions, establish check-in cadence.

5. Implement POC check-ins: schedule mid-point and final review calls to track progress, address blockers, gather feedback, ensure timeline is on track.

6. Track PostHog events: poc_initiated, poc_kickoff_completed, poc_milestone_achieved, poc_blocker_identified, poc_success_validated.

7. Document POC results: create summary showing which success criteria were met, metrics achieved, stakeholder feedback, next steps.

8. Set pass threshold: Complete structured POCs on ≥5 opportunities in 2 weeks with ≥60% meeting success criteria and progressing to proposal.

9. Measure POC effectiveness: track POC-to-close conversion rate, time from POC completion to decision, impact on deal size.

10. Document which POC structures and success criteria work best; proceed to Baseline if threshold met.

---

## KPIs to track
- POC completion rate
- Success criteria achievement
- POC-to-proposal conversion
- Time to decision

---

## Pass threshold
**Structured POCs completed on ≥5 opportunities in 2 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/poc-management-framework`_
