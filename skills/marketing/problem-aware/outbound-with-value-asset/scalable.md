---
name: outbound-with-value-asset-scalable
description: >
  Outbound With Value Asset — Scalable Automation. Share a one-page checklist asset in 100 emails to see if asset-led messaging drives replies that reference the asset.
stage: "Marketing > Problem Aware"
motion: "Outbound Founder-Led"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 15 positive replies referencing asset over 2 months"
kpis: ["Reply rate", "Open rate"]
slug: "outbound-with-value-asset"
install: "npx gtm-skills add marketing/problem-aware/outbound-with-value-asset"
---
# Outbound With Value Asset — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Outbound Founder-Led | **Channels:** Other

## Overview
Share a one-page checklist asset in 100 emails to see if asset-led messaging drives replies that reference the asset.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 15 positive replies referencing asset over 2 months

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Instantly** (Email)
- **Clay** (Enrichment)
- **Attio** (CRM)
- **Apollo** (Enrichment)

---

## Instructions

1. Set your Scalable volume target (e.g. 5–10x Baseline) and confirm the outcome you are aiming for: ≥ 15 positive replies referencing asset over 2 months.

2. Ensure all tools (email, CRM, ads, etc.) send events to PostHog so you have a single view of sent, opened, replied, and converted.

3. In n8n (or similar), build workflows triggered by PostHog events: e.g. when a lead replies or books a meeting, trigger a notification or follow-up so no lead sits unattended.

4. Run list-building and execution at the new volume; keep message and offer consistent with Baseline so you can compare fairly.

5. Each week, record Reply rate, Open rate in PostHog and compute running totals; compare to your Scalable target.

6. Keep conversion or meeting rate within 20% of Baseline; if it drops, pause scaling and refine targeting or copy before adding more volume.

7. Use n8n to automate follow-ups and logging so outcomes flow back to PostHog and CRM without manual entry where possible.

8. At the end of 2 months, confirm you hit or approached the Scalable outcome and that all key events are tracked.

9. If metrics hold, document the workflow and hand off to Durable for agent-driven optimization; if not, iterate before Durable.

10. Prepare a short summary of tools, event flow, and guardrails for the next team or agent to run Durable.

---

## KPIs to track
- Reply rate
- Open rate

---

## Pass threshold
**≥ 15 positive replies referencing asset over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/outbound-with-value-asset`_
