---
name: partnerships-warm-intros-baseline
description: >
    Partnerships & Warm Intros — Baseline Run. Ask advisors, angels, or partners for intros to test
  whether warm routes yield a few intros and meetings before refining ask and materials.
stage: "Sales > Qualified"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 6 intros and ≥ 4 meetings over 2 weeks"
kpis: ["Briefings scheduled", "Follow-up requests"]
slug: "partnerships-warm-intros"
install: "npx gtm-skills add sales/qualified/partnerships-warm-intros"
drills:
  - warm-intro-request
  - posthog-gtm-events
---
# Partnerships & Warm Intros — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Overview
Partnerships & Warm Intros — Baseline Run. Ask advisors, angels, or partners for intros to test whether warm routes yield a few intros and meetings before refining ask and materials.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 6 intros and ≥ 4 meetings over 2 weeks

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
Run the `posthog-gtm-events` drill to track: `partnerships-warm-intros_partner_contacted`, `partnerships-warm-intros_intro_received`, `partnerships-warm-intros_collab_launched`, `partnerships-warm-intros_lead_from_partner`. Attribute pipeline to specific partnerships.

### 3. Execute 5-10 partnerships over 2-4 weeks
Run the collaborations: content swaps, co-promotions, intro exchanges, or joint webinars. Track results from each partnership individually to identify which partners and formats drive the most value.

### 4. Evaluate against threshold
Measure against: ≥ 6 intros and ≥ 4 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, focus on the partnership format that showed the most promise and try different partners.

---

## KPIs to track
- Briefings scheduled
- Follow-up requests

---

## Pass threshold
**≥ 6 intros and ≥ 4 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/partnerships-warm-intros`_
