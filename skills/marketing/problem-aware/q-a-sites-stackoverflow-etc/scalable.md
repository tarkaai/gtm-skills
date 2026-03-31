---
name: q-a-sites-stackoverflow-etc-scalable
description: >
  Q&A Site Authority — Scalable Automation. Answer a few relevant questions on Q&A sites with a soft CTA to test if authority-building drives profile clicks and a lead.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 300 profile clicks and ≥ 15 leads over 2 months"
kpis: ["Profile views", "Profile click rate"]
slug: "q-a-sites-stackoverflow-etc"
install: "npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc"
drills:
  - social-content-pipeline
  - crm-pipeline-setup
  - content-repurposing
  - tool-sync-workflow
  - posthog-gtm-events
---
# Q&A Site Authority — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Other

## Overview
Answer a few relevant questions on Q&A sites with a soft CTA to test if authority-building drives profile clicks and a lead.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 300 profile clicks and ≥ 15 leads over 2 months

---

## Budget

**Play-specific tools & costs**
- **Premium community memberships (Slack groups, paid newsletters):** ~$50–200/mo

_Total play-specific: ~$50–200/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Discord** (Communication)
- **Slack** (Communication)

---

## Instructions

1. Set your Scalable volume target (e.g. 5–10x Baseline) and confirm the outcome you are aiming for: ≥ 300 profile clicks and ≥ 15 leads over 2 months.

2. Ensure all tools (email, CRM, ads, etc.) send events to PostHog so you have a single view of sent, opened, replied, and converted.

3. In n8n (or similar), build workflows triggered by PostHog events: e.g. when a lead replies or books a meeting, trigger a notification or follow-up so no lead sits unattended.

4. Run list-building and execution at the new volume; keep message and offer consistent with Baseline so you can compare fairly.

5. Each week, record Profile views, Profile click rate in PostHog and compute running totals; compare to your Scalable target.

6. Keep conversion or meeting rate within 20% of Baseline; if it drops, pause scaling and refine targeting or copy before adding more volume.

7. Use n8n to automate follow-ups and logging so outcomes flow back to PostHog and CRM without manual entry where possible.

8. At the end of 2 months, confirm you hit or approached the Scalable outcome and that all key events are tracked.

9. If metrics hold, document the workflow and hand off to Durable for agent-driven optimization; if not, iterate before Durable.

10. Prepare a short summary of tools, event flow, and guardrails for the next team or agent to run Durable.

---

## KPIs to track
- Profile views
- Profile click rate

---

## Pass threshold
**≥ 300 profile clicks and ≥ 15 leads over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc`_
