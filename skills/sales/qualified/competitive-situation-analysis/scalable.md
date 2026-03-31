---
name: competitive-situation-analysis-scalable
description: >
  Competitive Situation Assessment — Scalable Automation. Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "54 hours over 2 months"
outcome: "Competitive situation assessed on ≥75% of opportunities at scale over 2 months with improved win rates"
kpis: ["Competitive discovery rate", "Win rate by competitor", "Competitive positioning speed", "Deal velocity in competitive situations", "Intelligence automation effectiveness"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Competitive Situation Assessment — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.

**Time commitment:** 54 hours over 2 months
**Pass threshold:** Competitive situation assessed on ≥75% of opportunities at scale over 2 months with improved win rates

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

---

## Instructions

1. Build n8n workflow that prompts competitive discovery questions after every qualification call; auto-tags competitive situation in Attio.

2. Create competitive intelligence automation: n8n monitors competitor websites, G2 reviews, social media, funding news; alerts sales team to competitive changes.

3. Implement automated battlecard delivery: when specific competitor is tagged in deal, n8n automatically sends relevant battlecard, case studies, and differentiation talking points to rep.

4. Set up competitive trigger alerts: n8n monitors deal notes and emails for competitor mentions; surfaces relevant competitive intelligence and suggests positioning strategies.

5. Connect PostHog to n8n: when prospect visits competitor comparison pages or pricing pages, trigger personalized competitive positioning content.

6. Build competitive intelligence dashboard: track competitor appearance frequency, win/loss rates by competitor, competitive deal velocity, positioning effectiveness.

7. Create A/B testing framework for competitive messaging: test different competitive positioning approaches; measure which narratives drive highest conversion.

8. Set guardrails: competitive discovery rate must stay ≥75% of Baseline level; win rates against specific competitors must not decline by >15%.

9. Implement competitive early warning system: flag deals where competitor engagement is advanced as needing accelerated strategy.

10. After 2 months, evaluate competitive intelligence impact on win rates; if metrics hold, proceed to Durable AI-driven competitive intelligence.

---

## KPIs to track
- Competitive discovery rate
- Win rate by competitor
- Competitive positioning speed
- Deal velocity in competitive situations
- Intelligence automation effectiveness

---

## Pass threshold
**Competitive situation assessed on ≥75% of opportunities at scale over 2 months with improved win rates**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/competitive-situation-analysis`_
