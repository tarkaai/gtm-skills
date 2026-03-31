---
name: executive-roundtables-smoke
description: >
    Executive Roundtables — Smoke Test. Invite senior leaders for intimate, topic-focused
  discussions to build relationships and generate high-value pipeline with solution-aware
  executives.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥8 executive attendees and ≥3 high-value opportunities from first roundtable"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "executive-roundtables"
install: "npx gtm-skills add marketing/solution-aware/executive-roundtables"
drills:
  - icp-definition
  - webinar-pipeline
  - threshold-engine
---
# Executive Roundtables — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Executive Roundtables — Smoke Test. Invite senior leaders for intimate, topic-focused discussions to build relationships and generate high-value pipeline with solution-aware executives.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥8 executive attendees and ≥3 high-value opportunities from first roundtable

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your event ICP
Run the `icp-definition` drill to define who should attend your event. Document: target audience, what they want to learn, ideal event format (webinar, meetup, workshop), and how you will invite them.

### 2. Set up event infrastructure
Run the `webinar-pipeline` drill to configure your event: create Cal.com booking page or registration form, set up email confirmations via Loops, create an Attio list for registrants. Prepare your event content and materials.

**Human action required:** Promote the event through your channels (email, social, communities). Run the event live. The agent prepares everything but you execute the event.

### 3. Track registrations and attendance
Log all registrants in Attio. Track: registrations, attendance rate, engagement during event (questions asked, polls answered), and follow-up actions taken.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥8 executive attendees and ≥3 high-value opportunities from first roundtable. If PASS, proceed to Baseline. If FAIL, adjust event topic, format, promotion channels, or timing.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥8 executive attendees and ≥3 high-value opportunities from first roundtable**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/executive-roundtables`_
