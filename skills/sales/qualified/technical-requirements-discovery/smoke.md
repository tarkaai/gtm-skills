---
name: technical-requirements-discovery-smoke
description: >
  Technical Requirements Discovery — Smoke Test. Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Technical discovery completed on ≥5 opportunities in 1 week"
kpis: ["Technical discovery completion rate", "Technical fit score", "Early blocker identification rate", "Integration complexity assessment"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
---
# Technical Requirements Discovery — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** Technical discovery completed on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. Create technical requirements checklist covering: integrations needed, security/compliance requirements, data migration needs, technical architecture, performance expectations, user volume/scale.

2. On first 5-10 qualified opportunities, conduct technical discovery call with prospect's technical stakeholder (IT, engineering, DevOps, security).

3. Ask systematic questions in each area: 'What systems must we integrate with?', 'What security certifications do you require?', 'What's your deployment preference?'.

4. Document all technical requirements in Attio custom fields; flag any show-stoppers or complex requirements immediately.

5. Assess technical fit score (1-10) based on how well your product meets their technical needs; identify gaps that need product roadmap commitment.

6. Track PostHog events: technical_discovery_completed, integration_required, security_requirement_identified, technical_blocker_found.

7. Loop in technical team (engineering, solutions architect, security) early for complex technical requirements.

8. Set pass threshold: Complete technical discovery on ≥5 opportunities in 1 week with ≥80% technical fit score.

9. Compare deal outcomes: measure how technical discovery impacts close rate and identifies deal risks early.

10. Document which technical questions uncover most critical requirements; proceed to Baseline if threshold met.

---

## KPIs to track
- Technical discovery completion rate
- Technical fit score
- Early blocker identification rate
- Integration complexity assessment

---

## Pass threshold
**Technical discovery completed on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/technical-requirements-discovery`_
