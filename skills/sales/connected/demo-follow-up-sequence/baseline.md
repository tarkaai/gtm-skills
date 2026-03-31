---
name: demo-follow-up-sequence-baseline
description: >
  Demo Follow-Up Sequence — Baseline Run. Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Demo follow-up on ≥80% of demos over 2 weeks"
kpis: ["Follow-up sequence completion", "Response rate by touch", "Next step conversion rate", "Time to next step", "Resource engagement rate"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Demo Follow-Up Sequence — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.

**Time commitment:** 15 hours over 2 weeks
**Pass threshold:** Demo follow-up on ≥80% of demos over 2 weeks

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
- **Instantly** (Email)

---

## Instructions

1. Expand demo follow-up to 30-40 opportunities over 2 weeks; develop standardized follow-up sequence framework.

2. Create demo follow-up templates: recap email template, resource compilation templates, check-in email templates, value-add touch templates customized by persona.

3. Build demo-specific resource packages: assemble relevant materials based on what was discussed in demo (technical resources for engineer calls, ROI materials for executive calls).

4. Set up PostHog event tracking: follow_up_sequence_initiated, email_opened, resource_accessed, response_received, next_step_type.

5. Implement follow-up cadence: 0 hours (recap), 24 hours (check-in), 3 days (resources), 7 days (value-add), 10 days (final ask with urgency).

6. Track follow-up effectiveness: measure open rates, click rates, response rates, next step conversion by follow-up touch and content type.

7. Create demo notes capture process: standardize what to document during demo to enable personalized follow-up (questions asked, features highlighted, concerns raised, stakeholders involved).

8. Set pass threshold: Demo follow-up on ≥80% of demos over 2 weeks with ≥55% scheduling next step within 10 days.

9. Analyze follow-up patterns: which touches drive responses, which resources get consumed, which next steps are most common, what timing works best.

10. If threshold met, document demo follow-up playbook and proceed to Scalable; if not, refine sequence timing or content.

---

## KPIs to track
- Follow-up sequence completion
- Response rate by touch
- Next step conversion rate
- Time to next step
- Resource engagement rate

---

## Pass threshold
**Demo follow-up on ≥80% of demos over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-follow-up-sequence`_
