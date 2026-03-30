---
name: mutual-action-plan-baseline
description: >
  Mutual Action Plan (MAP) — Baseline Run. Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=70% MAP adoption and >=30% faster close time with >=20% higher win rate for MAP deals over 2 weeks"
kpis: ["MAP adoption rate", "Deal velocity (MAP vs non-MAP)", "Win rate (MAP vs non-MAP)", "Milestone adherence rate"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
---
# Mutual Action Plan (MAP) — Baseline Run

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.

**Time commitment:** 20 hours over 2 weeks
**Pass threshold:** >=70% MAP adoption and >=30% faster close time with >=20% higher win rate for MAP deals over 2 weeks

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

---

## Instructions

1. Expand MAPs to 10-15 deals over 2 weeks; create professional MAP templates in Notion, Google Sheets, or dedicated tools like Recapped with branded milestones and clear ownership.

2. Define standard MAP milestone templates by deal type: SMB (demo, proposal, approval, signature—2 weeks), Mid-Market (demo, technical review, proposal, legal, approval—4-6 weeks), Enterprise (discovery, demo, POC, proposal, procurement, legal, approval—8-12 weeks).

3. Set pass threshold: >=70% of deals have MAPs, and MAP deals close >=30% faster with >=20% higher win rate vs non-MAP deals.

4. Introduce MAPs immediately after successful demo: "Great call! Let's align on next steps—I'll create a shared timeline showing what we'll do and what you'll do. When can we review it together?"

5. Build MAPs collaboratively: don't dictate timeline, co-create with champion; ask "When can you realistically complete [milestone]?" and "What could delay this?" to surface risks early.

6. Track MAP health in Attio: calculate completion percentage, identify overdue milestones, flag at-risk deals (multiple milestones delayed, low stakeholder engagement with MAP).

7. Sync MAP data from Attio to PostHog; create dashboards showing MAP completion trends, average time per milestone, common delay reasons, and correlation between MAP adherence and close rate.

8. When milestones slip, escalate immediately: "We were expecting [milestone] by [date], but it's delayed. What's blocking progress? How can we help?" Prevents silent stalls.

9. After 2 weeks, analyze MAP vs non-MAP deals: measure deal velocity, win rate, and stall rate; if MAP deals perform >=30% better, MAPs are high-leverage.

10. If >=70% adoption and MAP deals significantly outperform, move to Scalable; otherwise improve MAP positioning or make milestone templates more realistic.

---

## KPIs to track
- MAP adoption rate
- Deal velocity (MAP vs non-MAP)
- Win rate (MAP vs non-MAP)
- Milestone adherence rate

---

## Pass threshold
**>=70% MAP adoption and >=30% faster close time with >=20% higher win rate for MAP deals over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/mutual-action-plan`_
