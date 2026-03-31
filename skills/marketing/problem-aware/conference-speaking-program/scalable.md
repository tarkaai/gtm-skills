---
name: conference-speaking-program-scalable
description: >
    Conference Speaking — Scalable Automation. Secure speaking slots at industry conferences for
  brand building, thought leadership, and lead generation with solution-aware and problem-aware
  attendees.
stage: "Marketing > Problem Aware"
motion: "Micro Events"
channels: "Events, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥12 speaking slots and ≥80 qualified leads over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "conference-speaking-program"
install: "npx gtm-skills add marketing/problem-aware/conference-speaking-program"
drills:
  - follow-up-automation
  - ab-test-orchestrator
---
# Conference Speaking — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Micro Events | **Channels:** Events, Social

## Overview
Conference Speaking — Scalable Automation. Secure speaking slots at industry conferences for brand building, thought leadership, and lead generation with solution-aware and problem-aware attendees.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥12 speaking slots and ≥80 qualified leads over 6 months

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
Measure against: ≥12 speaking slots and ≥80 qualified leads over 6 months. If PASS, proceed to Durable. If FAIL, reduce frequency and focus on the event format that converts best.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥12 speaking slots and ≥80 qualified leads over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/conference-speaking-program`_
