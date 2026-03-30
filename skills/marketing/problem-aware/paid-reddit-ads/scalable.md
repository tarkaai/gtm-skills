---
name: paid-reddit-ads-scalable
description: >
  Paid Reddit Ads — Scalable Automation. Run a small Reddit ad budget across a couple of sets and one LP to test if paid community placement drives leads or a meeting.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 30 leads or ≥ 16 meetings over 2 months"
kpis: ["Click-through rate", "Landing page visits"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
---
# Paid Reddit Ads — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Overview
Run a small Reddit ad budget across a couple of sets and one LP to test if paid community placement drives leads or a meeting.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 30 leads or ≥ 16 meetings over 2 months

---

## Budget

**Play-specific tools & costs**
- **Ad spend:** $3,000–10,000/mo
- **Landing page tool:** ~$15–40/mo
- **LinkedIn Campaign Manager (included with ad spend — no extra fee):** Free

_Total play-specific: ~$15–10000/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Google Ads** (Channel)
- **LinkedIn Ads** (Channel)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Set your Scalable volume target (e.g. 5–10x Baseline) and confirm the outcome you are aiming for: ≥ 30 leads or ≥ 16 meetings over 2 months.

2. Ensure all tools (email, CRM, ads, etc.) send events to PostHog so you have a single view of sent, opened, replied, and converted.

3. In n8n (or similar), build workflows triggered by PostHog events: e.g. when a lead replies or books a meeting, trigger a notification or follow-up so no lead sits unattended.

4. Run list-building and execution at the new volume; keep message and offer consistent with Baseline so you can compare fairly.

5. Each week, record Click-through rate, Landing page visits in PostHog and compute running totals; compare to your Scalable target.

6. Keep conversion or meeting rate within 20% of Baseline; if it drops, pause scaling and refine targeting or copy before adding more volume.

7. Use n8n to automate follow-ups and logging so outcomes flow back to PostHog and CRM without manual entry where possible.

8. At the end of 2 months, confirm you hit or approached the Scalable outcome and that all key events are tracked.

9. If metrics hold, document the workflow and hand off to Durable for agent-driven optimization; if not, iterate before Durable.

10. Prepare a short summary of tools, event flow, and guardrails for the next team or agent to run Durable.

---

## KPIs to track
- Click-through rate
- Landing page visits

---

## Pass threshold
**≥ 30 leads or ≥ 16 meetings over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/paid-reddit-ads`_
