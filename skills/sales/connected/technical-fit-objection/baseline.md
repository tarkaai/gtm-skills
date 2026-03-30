---
name: technical-fit-objection-baseline
description: >
  Technical Fit Objection Handling — Baseline Run. Address concerns about technical compatibility, missing features, or capability gaps with roadmap commitments, workarounds, and technical proof to maintain deal momentum.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Technical objections handled on ≥80% of instances over 2 weeks"
kpis: ["Objection resolution rate", "Deal save rate", "Technical proof effectiveness", "Roadmap commitment accuracy"]
slug: "technical-fit-objection"
install: "npx gtm-skills add sales/connected/technical-fit-objection"
---
# Technical Fit Objection Handling — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Address concerns about technical compatibility, missing features, or capability gaps with roadmap commitments, workarounds, and technical proof to maintain deal momentum.

**Time commitment:** 15 hours over 2 weeks
**Pass threshold:** Technical objections handled on ≥80% of instances over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Apollo (includes dialer) or Aircall:** ~$50–100/mo

_Total play-specific: ~$50–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Expand technical objection handling to 20-30 instances over 2 weeks.

2. Build technical objection playbook: common gaps by category, standard responses, workaround library, roadmap positioning, proof point repository.

3. Create technical proof library: architecture docs, performance benchmarks, integration examples, security certifications, scalability case studies organized by objection type.

4. Set up PostHog event tracking: objection_category, criticality_level, response_type, technical_resource_engaged, resolution_outcome.

5. Develop gap assessment framework: evaluate whether gap is dealbreaker, timing sensitivity, competitive impact, workaround feasibility, roadmap fit.

6. Track technical objection outcomes: measure resolution rates by gap type, deals saved vs lost, time to resolution, impact on deal size and timeline.

7. Build escalation process: define when to engage product team for roadmap commitments, when to scope custom development, when to walk away from bad-fit deals.

8. Set pass threshold: Technical objections addressed on ≥80% of instances over 2 weeks with ≥65% achieving resolution that advances deal.

9. Analyze objection patterns: which technical gaps appear most frequently, which are real dealbreakers vs negotiation tactics, which workarounds work best.

10. If threshold met, document technical objection framework and proceed to Scalable; if not, refine response library or technical proof.

---

## KPIs to track
- Objection resolution rate
- Deal save rate
- Technical proof effectiveness
- Roadmap commitment accuracy

---

## Pass threshold
**Technical objections handled on ≥80% of instances over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/technical-fit-objection`_
