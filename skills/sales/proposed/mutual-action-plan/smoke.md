---
name: mutual-action-plan-smoke
description: >
  Mutual Action Plan (MAP) — Smoke Test. Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "7 hours over 2 weeks"
outcome: ">=3 MAPs created and >=25% faster close time for MAP deals within 2 weeks"
kpis: ["MAP adoption rate", "Deal velocity (MAP vs non-MAP)", "Milestone completion rate", "Stall rate"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
---
# Mutual Action Plan (MAP) — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.

**Time commitment:** 7 hours over 2 weeks
**Pass threshold:** >=3 MAPs created and >=25% faster close time for MAP deals within 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Create a MAP template in a spreadsheet or doc with columns: Milestone, Owner (your team or prospect's), Due Date, Status, Dependencies; include milestones for both sides (demo, technical review, proposal, legal review, approval, contract signing).

2. Select 3 active opportunities in proposal/negotiation stage; schedule MAP planning calls with champion or key stakeholder to build shared timeline.

3. Set pass threshold: build MAPs for >=3 deals, and MAP deals close >=25% faster than deals without MAPs within 2 weeks.

4. During MAP call, collaboratively define milestones: "What steps need to happen on your end before you can approve?" "Who needs to review?" "When can we schedule executive alignment?" Get specific dates and owners.

5. For each milestone, identify dependencies: "You can't do legal review until we deliver security docs—we'll have those by [date]" ensures clarity on blockers and sequencing.

6. Share MAP with all stakeholders via email or shared doc; make it visible and accessible so everyone knows what's next and who's responsible.

7. Log MAP in Attio with custom fields for map_created_date, expected_close_date, completion_percentage, and at_risk_status; track MAP progress weekly.

8. In PostHog, create events for map_created, milestone_completed, milestone_delayed with properties for milestone type, owner, and delay reason.

9. Send weekly MAP updates to prospect: "We completed [milestone X], next up is [milestone Y] owned by [person] due [date]—are you on track?" Keeps deal momentum visible.

10. If MAPs accelerate >=3 deals by >=25%, shared timelines reduce friction and ambiguity; document MAP process and proceed to Baseline; otherwise refine milestone definitions or engagement process.

---

## KPIs to track
- MAP adoption rate
- Deal velocity (MAP vs non-MAP)
- Milestone completion rate
- Stall rate

---

## Pass threshold
**>=3 MAPs created and >=25% faster close time for MAP deals within 2 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/mutual-action-plan`_
