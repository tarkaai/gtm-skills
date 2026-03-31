---
name: change-management-objection-smoke
description: >
  Change Management Objection Handling — Smoke Test. Overcome resistance to changing from current solution by quantifying switching costs vs ongoing pain costs, and providing comprehensive change support to reduce adoption risk.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Change objections handled on ≥5 opportunities in 1 week"
kpis: ["Change objection resolution rate", "Status quo cost acceptance", "Change plan acceptance rate", "Deal progression rate"]
slug: "change-management-objection"
install: "npx gtm-skills add sales/connected/change-management-objection"
drills:
  - icp-definition
  - threshold-engine
---
# Change Management Objection Handling — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Overcome resistance to changing from current solution by quantifying switching costs vs ongoing pain costs, and providing comprehensive change support to reduce adoption risk.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** Change objections handled on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. When 5-8 prospects express change resistance, diagnose root cause: fear of disruption, past failed implementations, training concerns, data migration anxiety, team pushback, political dynamics.

2. Quantify status quo cost: calculate total cost of staying with current solution (license costs + hidden costs + opportunity costs + pain costs); present vs total cost of change (implementation + training + migration).

3. Build change support plan: outline migration assistance, training program, onboarding support, phased rollout option, success metrics, risk mitigation strategies.

4. Share change management case studies: provide examples of similar customers who successfully migrated, highlighting timeline, challenges overcome, adoption rates achieved, ROI realized.

5. Offer risk reduction options: pilot with small team, phased rollout by department, parallel running period, money-back guarantee, dedicated implementation support.

6. Address team adoption concerns: provide training resources, change management playbook, communication templates, stakeholder engagement plan.

7. Track PostHog events: change_objection_raised, root_cause_identified, cost_comparison_presented, change_plan_delivered, risk_reduction_offered.

8. Set pass threshold: Handle change objections on ≥5 opportunities in 1 week with ≥60% accepting change support plan and advancing to proposal.

9. Measure effectiveness: track change objection resolution rate, deals saved from status quo bias, implementation success rate for converted customers.

10. Document which change management approaches work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Change objection resolution rate
- Status quo cost acceptance
- Change plan acceptance rate
- Deal progression rate

---

## Pass threshold
**Change objections handled on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/change-management-objection`_
