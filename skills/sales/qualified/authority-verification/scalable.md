---
name: authority-verification-scalable
description: >
  Authority Verification Process — Scalable Automation. Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "Authority verified in ≥75% of opportunities at scale over 2 months with deal velocity +20%"
kpis: ["Authority verification rate", "Time to authority confirmation", "Deal velocity improvement", "Close rate with verified authority", "Multi-threading success rate"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Authority Verification Process — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.

**Time commitment:** 50 hours over 2 months
**Pass threshold:** Authority verified in ≥75% of opportunities at scale over 2 months with deal velocity +20%

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
- **LinkedIn Sales Navigator** (Channel)
- **Apollo** (Enrichment)

---

## Instructions

1. Build n8n workflow that enriches every new opportunity with org chart data: pulls LinkedIn data, identifies reporting structure, highlights likely decision makers.

2. Create authority scoring model in PostHog: assign points based on job title, seniority, budget keywords in LinkedIn bio, department; auto-tag authority level in Attio.

3. Set up automated pre-call research: n8n generates briefing doc for every sales call showing org structure, authority likelihood, recommended questions, and intro paths.

4. Implement multi-threading triggers: when authority level is 'Influencer' or 'End User', n8n automatically suggests action items to connect with economic buyer.

5. Create email templates for authority navigation: requesting introductions, confirming budget authority, involving decision makers in next steps.

6. Connect PostHog to n8n: when authority is not verified after 7 days, trigger automated reminder to sales rep with suggested actions.

7. Track authority verification at scale: measure % of pipeline with verified authority, average time to authority confirmation, correlation with close rate.

8. Set guardrails: authority verification rate must stay ≥75% of Baseline level; if it drops for 2+ weeks, revisit qualification process.

9. Build authority intelligence dashboard in PostHog: show authority verification trends, deal velocity by authority type, close rate impact.

10. After 2 months, evaluate impact on deal quality and velocity; if metrics hold, proceed to Durable AI-driven authority intelligence.

---

## KPIs to track
- Authority verification rate
- Time to authority confirmation
- Deal velocity improvement
- Close rate with verified authority
- Multi-threading success rate

---

## Pass threshold
**Authority verified in ≥75% of opportunities at scale over 2 months with deal velocity +20%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/authority-verification`_
