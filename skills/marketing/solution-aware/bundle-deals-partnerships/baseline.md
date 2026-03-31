---
name: bundle-deals-partnerships-baseline
description: >
    Bundle Deal Partnerships — Baseline Run. Package your product with partners for special pricing
  to create compelling offers and reach solution-aware audiences through partner channels.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥3 bundle partnerships and ≥12 bundle deals in 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "bundle-deals-partnerships"
install: "npx gtm-skills add marketing/solution-aware/bundle-deals-partnerships"
drills:
  - warm-intro-request
  - posthog-gtm-events
---
# Bundle Deal Partnerships — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Overview
Bundle Deal Partnerships — Baseline Run. Package your product with partners for special pricing to create compelling offers and reach solution-aware audiences through partner channels.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥3 bundle partnerships and ≥12 bundle deals in 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Formalize partner outreach
Run the `warm-intro-request` drill to build a systematic intro request process: identify mutual connections in your network, craft personalized intro requests, and track request-to-intro conversion rates.

### 2. Configure partnership tracking
Run the `posthog-gtm-events` drill to track: `bundle-deals-partnerships_partner_contacted`, `bundle-deals-partnerships_intro_received`, `bundle-deals-partnerships_collab_launched`, `bundle-deals-partnerships_lead_from_partner`. Attribute pipeline to specific partnerships.

### 3. Execute 5-10 partnerships over 2-4 weeks
Run the collaborations: content swaps, co-promotions, intro exchanges, or joint webinars. Track results from each partnership individually to identify which partners and formats drive the most value.

### 4. Evaluate against threshold
Measure against: ≥3 bundle partnerships and ≥12 bundle deals in 8 weeks. If PASS, proceed to Scalable. If FAIL, focus on the partnership format that showed the most promise and try different partners.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥3 bundle partnerships and ≥12 bundle deals in 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/bundle-deals-partnerships`_
