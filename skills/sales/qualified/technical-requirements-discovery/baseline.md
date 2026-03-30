---
name: technical-requirements-discovery-baseline
description: >
  Technical Requirements Discovery — Baseline Run. Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Technical discovery completed on ≥80% of opportunities over 2 weeks"
kpis: ["Technical discovery completion rate", "Technical fit accuracy", "Solutions engineer engagement rate", "Technical blocker early detection"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
---
# Technical Requirements Discovery — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** Technical discovery completed on ≥80% of opportunities over 2 weeks

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

1. Expand technical discovery to 30-50 opportunities over 2 weeks; build comprehensive technical requirements framework.

2. Create technical requirement categories: Integration (APIs, data sync, SSO), Security (SOC2, GDPR, HIPAA, ISO27001), Infrastructure (cloud, on-prem, hybrid), Performance (SLAs, uptime, scale), Data (migration, formats, volume).

3. Develop technical discovery question bank with 3-5 questions per category; tailor questions by prospect's industry and tech maturity.

4. Set up PostHog event tracking: technical_category_assessed, complex_integration_identified, security_certification_required, custom_development_needed.

5. Build technical handoff process: when technical complexity is high, schedule solutions engineer or architect call within 48 hours.

6. Track technical-to-commercial correlation: measure how technical fit score predicts close rate, deal velocity, and implementation success.

7. Create technical requirement prioritization: separate must-haves from nice-to-haves; focus on deal-critical technical needs first.

8. Set pass threshold: Technical discovery completed on ≥80% of qualified opportunities over 2 weeks with ≥70% accurately predicting technical fit.

9. Build technical objection library: document common technical concerns and how to address them (security questionnaires, architecture diagrams, compliance docs).

10. If threshold met, document technical discovery playbook and proceed to Scalable; if not, refine technical assessment criteria.

---

## KPIs to track
- Technical discovery completion rate
- Technical fit accuracy
- Solutions engineer engagement rate
- Technical blocker early detection

---

## Pass threshold
**Technical discovery completed on ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/technical-requirements-discovery`_
