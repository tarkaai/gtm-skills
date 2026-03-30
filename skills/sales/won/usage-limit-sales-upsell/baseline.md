---
name: usage-limit-sales-upsell-baseline
description: >
  Usage-Based Upsell — Baseline Run. Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Product, Email, Direct"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=30% upsell conversion rate and expansion ARR >=10% of base ARR over 2 weeks"
kpis: ["Upsell conversion rate", "Expansion ARR", "Time from signal to close", "Proactive vs reactive upsells"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add sales/won/usage-limit-sales-upsell"
---
# Usage-Based Upsell — Baseline Run

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Direct

## Overview
Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.

**Time commitment:** 22 hours over 2 weeks
**Pass threshold:** >=30% upsell conversion rate and expansion ARR >=10% of base ARR over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Instantly** (Email)

---

## Instructions

1. Expand to 30-50 customers over 2 weeks; build a usage monitoring dashboard in PostHog showing each customer's usage vs plan limits, growth trends, and expansion readiness score.

2. Create tiered expansion signals: Tier 1 (approaching hard limit, high urgency), Tier 2 (heavy feature usage, medium urgency), Tier 3 (new use case expansion, low urgency); prioritize Tier 1 for immediate outreach.

3. Set pass threshold: identify >=10 expansion-ready customers, achieve >=30% upsell conversion rate (3+ upsells closed), and average expansion deal size >=40% of original ACV.

4. Build automated usage alert emails: when customer hits 80% of limit, send automated warning + upgrade CTA; when customer hits 95%, send urgent upgrade prompt; when customer exceeds limit, offer immediate upgrade.

5. Sync usage data from PostHog to Attio so customer success and sales teams see real-time expansion signals; create tasks for outreach when signals trigger.

6. Develop expansion playbooks by signal type: seat expansion ("Your team is growing—add seats now"), tier upgrade ("You're using premium features heavily—unlock full power with Pro tier"), add-on sales ("You love X feature—try Y feature to amplify results").

7. Track expansion pipeline in Attio separately from new business pipeline; measure expansion ARR, time from signal to close, and which signals yield largest expansion deals.

8. After upsell closes, log expansion reason in PostHog and Attio; analyze whether upsell was proactive (you reached out first) or reactive (customer requested); optimize for proactive.

9. After 2 weeks, measure expansion conversion rate, average deal size, and expansion ARR as % of base ARR; target >=30% conversion and expansion ARR >=10% of base.

10. If >=30% upsell conversion and expansion metrics are strong, move to Scalable; otherwise refine signal definitions, improve offer positioning, or enhance customer success touchpoints.

---

## KPIs to track
- Upsell conversion rate
- Expansion ARR
- Time from signal to close
- Proactive vs reactive upsells

---

## Pass threshold
**>=30% upsell conversion rate and expansion ARR >=10% of base ARR over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/usage-limit-sales-upsell`_
