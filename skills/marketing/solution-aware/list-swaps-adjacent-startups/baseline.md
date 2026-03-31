---
name: list-swaps-adjacent-startups-baseline
description: >
    List Swap With Partner — Baseline Run. Swap one email each with an adjacent startup partner to
  test cross-audience reach and whether clicks and a meeting justify more swaps.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 80 clicks and ≥ 2 meetings over 2 weeks"
kpis: ["Click-through rate", "Email open rate"]
slug: "list-swaps-adjacent-startups"
install: "npx gtm-skills add marketing/solution-aware/list-swaps-adjacent-startups"
drills:
  - warm-intro-request
  - posthog-gtm-events
---
# List Swap With Partner — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Overview
List Swap With Partner — Baseline Run. Swap one email each with an adjacent startup partner to test cross-audience reach and whether clicks and a meeting justify more swaps.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 80 clicks and ≥ 2 meetings over 2 weeks

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
Run the `posthog-gtm-events` drill to track: `list-swaps-adjacent-startups_partner_contacted`, `list-swaps-adjacent-startups_intro_received`, `list-swaps-adjacent-startups_collab_launched`, `list-swaps-adjacent-startups_lead_from_partner`. Attribute pipeline to specific partnerships.

### 3. Execute 5-10 partnerships over 2-4 weeks
Run the collaborations: content swaps, co-promotions, intro exchanges, or joint webinars. Track results from each partnership individually to identify which partners and formats drive the most value.

### 4. Evaluate against threshold
Measure against: ≥ 80 clicks and ≥ 2 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, focus on the partnership format that showed the most promise and try different partners.

---

## KPIs to track
- Click-through rate
- Email open rate

---

## Pass threshold
**≥ 80 clicks and ≥ 2 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/list-swaps-adjacent-startups`_
