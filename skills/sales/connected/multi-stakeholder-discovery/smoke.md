---
name: multi-stakeholder-discovery-smoke
description: >
  Multi-Stakeholder Discovery Process — Smoke Test. Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "Multi-stakeholder discovery completed on ≥5 complex deals in 1 week"
kpis: ["Stakeholder discovery completion rate", "Average stakeholders per deal", "Consensus building success", "Deal progression rate"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
---
# Multi-Stakeholder Discovery Process — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** Multi-stakeholder discovery completed on ≥5 complex deals in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 5-8 complex deals (3+ stakeholders), map all decision participants: economic buyer, technical buyer, end users, influencers, blockers.

2. Request discovery calls with each stakeholder group: 'To ensure we address everyone's needs, I'd like to speak with your technical team, end users, and procurement separately'.

3. Tailor discovery questions by stakeholder: executives focus on business impact and ROI; technical buyers focus on architecture and integration; end users focus on usability and workflow.

4. Document stakeholder-specific needs in Attio: create custom fields for each stakeholder group's priorities, concerns, success criteria, and level of support.

5. Identify consensus vs. conflict: note where stakeholder needs align and where they diverge; develop strategies to address conflicts.

6. Track PostHog events: stakeholder_mapped, discovery_call_completed, stakeholder_need_identified, conflict_detected, consensus_built.

7. Create stakeholder matrix in Attio showing each person's role, influence level, support level (champion/neutral/blocker), and key needs.

8. Set pass threshold: Complete multi-stakeholder discovery on ≥5 complex deals in 1 week with ≥3 stakeholder groups per deal.

9. Measure impact: compare close rates and deal velocity for deals with comprehensive stakeholder discovery vs. single-threaded deals.

10. Document which stakeholder discovery approaches work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Stakeholder discovery completion rate
- Average stakeholders per deal
- Consensus building success
- Deal progression rate

---

## Pass threshold
**Multi-stakeholder discovery completed on ≥5 complex deals in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/multi-stakeholder-discovery`_
