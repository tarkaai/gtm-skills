---
name: review-ask-to-early-users-scalable
description: >
  Review Ask to Early Users — Scalable Automation. Request reviews from a handful of early users to build social proof and see if new reviews correlate with at least one inbound lead.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 20 new reviews and ≥ 15 inbound leads over 2 months"
kpis: ["3 new reviews", "1 inbound"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - crm-pipeline-setup
  - case-study-creation
  - posthog-gtm-events
---
# Review Ask to Early Users — Scalable Automation

> **Stage:** Marketing → Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Request reviews from a handful of early users to build social proof and see if new reviews correlate with at least one inbound lead.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 20 new reviews and ≥ 15 inbound leads over 2 months

---

## Budget

**Play-specific tools & costs**
- **G2 or Capterra review generation campaign:** ~$500–2,000/mo (sponsored)
- **Review incentive budget (gift cards, credits):** ~$100–500

_Total play-specific: ~$100–2000/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)

---

## Instructions

1. Set your Scalable volume target (e.g. 5–10x Baseline) and confirm the outcome you are aiming for: ≥ 20 new reviews and ≥ 15 inbound leads over 2 months.

2. Ensure all tools (email, CRM, ads, etc.) send events to PostHog so you have a single view of sent, opened, replied, and converted.

3. In n8n (or similar), build workflows triggered by PostHog events: e.g. when a lead replies or books a meeting, trigger a notification or follow-up so no lead sits unattended.

4. Run list-building and execution at the new volume; keep message and offer consistent with Baseline so you can compare fairly.

5. Each week, record 3 new reviews, 1 inbound in PostHog and compute running totals; compare to your Scalable target.

6. Keep conversion or meeting rate within 20% of Baseline; if it drops, pause scaling and refine targeting or copy before adding more volume.

7. Use n8n to automate follow-ups and logging so outcomes flow back to PostHog and CRM without manual entry where possible.

8. At the end of 2 months, confirm you hit or approached the Scalable outcome and that all key events are tracked.

9. If metrics hold, document the workflow and hand off to Durable for agent-driven optimization; if not, iterate before Durable.

10. Prepare a short summary of tools, event flow, and guardrails for the next team or agent to run Durable.

---

## KPIs to track
- 3 new reviews
- 1 inbound

---

## Pass threshold
**≥ 20 new reviews and ≥ 15 inbound leads over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/review-ask-to-early-users`_
