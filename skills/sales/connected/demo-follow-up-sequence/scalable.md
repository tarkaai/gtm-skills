---
name: demo-follow-up-sequence-scalable
description: >
  Demo Follow-Up Sequence — Scalable Automation. Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "Automated demo follow-up on ≥80% of demos at scale over 2 months with maintained conversion rates"
kpis: ["Sequence completion rate", "Response rate", "Next step conversion", "Follow-up efficiency", "Demo-to-proposal rate"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Demo Follow-Up Sequence — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** Automated demo follow-up on ≥80% of demos at scale over 2 months with maintained conversion rates

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Instantly** (Email)

---

## Instructions

1. Build n8n workflow that triggers demo follow-up sequence immediately after demo is marked complete in Attio; auto-generates personalized recap from demo notes.

2. Create intelligent content selection: n8n analyzes demo topics discussed and automatically selects most relevant resources and case studies for each follow-up.

3. Implement automated follow-up scheduling: n8n sends follow-up touches at optimal times; pauses sequence if prospect responds; resumes if conversation stalls.

4. Set up behavioral triggers: n8n monitors PostHog for prospect engagement with follow-up content; sends additional resources when specific pages are viewed.

5. Connect PostHog to n8n: when prospect visits pricing or competitor comparison pages after demo, trigger personalized follow-up addressing those specific topics.

6. Build follow-up intelligence dashboard: track sequence performance, touch effectiveness, content engagement, next step conversion rates, optimal timing.

7. Create A/B testing framework: test different subject lines, content types, timing, and CTAs; automatically promote winning variations.

8. Set guardrails: next step scheduling rate must stay ≥50% of Baseline level; response rate must not decline >15%.

9. Implement follow-up priority scoring: flag demos where prospect showed high interest but hasn't responded to follow-up for additional personalized outreach.

10. After 2 months, evaluate follow-up automation impact on demo-to-proposal conversion; if metrics hold, proceed to Durable AI-driven follow-up intelligence.

---

## KPIs to track
- Sequence completion rate
- Response rate
- Next step conversion
- Follow-up efficiency
- Demo-to-proposal rate

---

## Pass threshold
**Automated demo follow-up on ≥80% of demos at scale over 2 months with maintained conversion rates**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-follow-up-sequence`_
