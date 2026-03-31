---
name: poc-management-framework-baseline
description: >
  POC Management Framework — Baseline Run. Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Baseline Run"
time: "24 hours over 4 weeks"
outcome: "POCs on ≥80% of qualified opportunities over 4 weeks"
kpis: ["POC qualification accuracy", "Success criteria achievement rate", "POC-to-close conversion", "Time from POC to decision", "POC engagement score"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# POC Management Framework — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Overview
Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.

**Time commitment:** 24 hours over 4 weeks
**Pass threshold:** POCs on ≥80% of qualified opportunities over 4 weeks

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

1. Expand POC management to 15-25 opportunities over 4 weeks; develop standardized POC framework and governance.

2. Create POC playbook: templates for success criteria definition, kickoff agendas, check-in formats, results summaries, decision-making frameworks.

3. Build POC qualification criteria: not every deal needs POC; define when POC is appropriate (deal size, complexity, technical risk, competitive situation, budget authority).

4. Set up PostHog event tracking: poc_qualified, poc_scoped, kickoff_scheduled, usage_tracked, milestone_reached, blocker_resolved, results_reviewed.

5. Implement POC usage monitoring: track prospect engagement with POC environment in PostHog; identify low usage early and intervene.

6. Develop POC support structure: define what support you'll provide during POC (slack channel, office hours, technical assistance, training resources).

7. Create POC escalation process: when POC encounters blocker or goes off track, establish clear escalation path to resolve quickly.

8. Set pass threshold: POCs on ≥80% of qualified opportunities over 4 weeks with ≥65% achieving success criteria and ≥50% converting to closed-won.

9. Analyze POC patterns: which success criteria predict closes, what POC length is optimal, which support interventions improve outcomes.

10. If threshold met, document POC management playbook and proceed to Scalable; if not, refine POC structure and support model.

---

## KPIs to track
- POC qualification accuracy
- Success criteria achievement rate
- POC-to-close conversion
- Time from POC to decision
- POC engagement score

---

## Pass threshold
**POCs on ≥80% of qualified opportunities over 4 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/poc-management-framework`_
