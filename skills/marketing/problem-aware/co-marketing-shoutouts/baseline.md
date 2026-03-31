---
name: co-marketing-shoutouts-baseline
description: >
    Partner Newsletter Shoutout — Baseline Run. Run a short co-marketing blurb in a partner
  newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 50 clicks and ≥ 3 leads over 2 weeks"
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - warm-intro-request
  - posthog-gtm-events
---
# Partner Newsletter Shoutout — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Overview
Partner Newsletter Shoutout — Baseline Run. Run a short co-marketing blurb in a partner newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 50 clicks and ≥ 3 leads over 2 weeks

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
Run the `posthog-gtm-events` drill to track: `co-marketing-shoutouts_partner_contacted`, `co-marketing-shoutouts_intro_received`, `co-marketing-shoutouts_collab_launched`, `co-marketing-shoutouts_lead_from_partner`. Attribute pipeline to specific partnerships.

### 3. Execute 5-10 partnerships over 2-4 weeks
Run the collaborations: content swaps, co-promotions, intro exchanges, or joint webinars. Track results from each partnership individually to identify which partners and formats drive the most value.

### 4. Evaluate against threshold
Measure against: ≥ 50 clicks and ≥ 3 leads over 2 weeks. If PASS, proceed to Scalable. If FAIL, focus on the partnership format that showed the most promise and try different partners.

---

## KPIs to track
- Impressions
- Click-through rate

---

## Pass threshold
**≥ 50 clicks and ≥ 3 leads over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts`_
