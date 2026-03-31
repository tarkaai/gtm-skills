---
name: regional-field-events-scalable
description: >
    Regional Field Events — Scalable Automation. Host dinners, happy hours, or lunches in key
  markets to build relationships and generate pipeline with solution-aware and product-aware local
  prospects.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events, Direct"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥200 attendees and ≥50 qualified leads from monthly events over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "regional-field-events"
install: "npx gtm-skills add marketing/solution-aware/regional-field-events"
drills:
  - follow-up-automation
  - ab-test-orchestrator
---
# Regional Field Events — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events, Direct

## Overview
Regional Field Events — Scalable Automation. Host dinners, happy hours, or lunches in key markets to build relationships and generate pipeline with solution-aware and product-aware local prospects.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥200 attendees and ≥50 qualified leads from monthly events over 6 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate event operations
Run the `follow-up-automation` drill to build n8n workflows: auto-send post-event follow-ups based on engagement level (active participants get a different email than passive attendees), auto-create Attio deals for qualified attendees, and auto-schedule next event invitations.

### 2. Test event variations
Run the `ab-test-orchestrator` drill to test: event formats (webinar vs workshop vs AMA), event lengths, topics, speakers, and promotion channels. Use registration and attendance data to identify winning combinations.

### 3. Scale to regular cadence
Move to bi-weekly or monthly events. Automate as much of the operations as possible. Focus your manual effort on content quality and live delivery.

### 4. Evaluate against threshold
Measure against: ≥200 attendees and ≥50 qualified leads from monthly events over 6 months. If PASS, proceed to Durable. If FAIL, reduce frequency and focus on the event format that converts best.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥200 attendees and ≥50 qualified leads from monthly events over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/regional-field-events`_
