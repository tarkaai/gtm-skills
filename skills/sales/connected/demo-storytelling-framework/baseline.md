---
name: demo-storytelling-framework-baseline
description: >
    Demo Storytelling Framework — Baseline Run. Transform product demos from feature walkthroughs
  into compelling narratives using customer stories and prospect-specific scenarios to drive
  emotional engagement and conviction.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Storytelling demos on ≥80% of opportunities over 2 weeks"
kpis: ["Storytelling adoption rate", "Demo-to-proposal improvement", "Prospect engagement score", "Story resonance rate"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Demo Storytelling Framework — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Demo Storytelling Framework — Baseline Run. Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** Storytelling demos on ≥80% of opportunities over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up cold outreach tooling
Run the `cold-email-sequence` drill to configure Instantly with warmed-up sending accounts. Import your prospect list from Attio (built during Smoke). Create 3-5 email variants using the ICP pain points validated in Smoke. Set up A/B subject line testing.

### 2. Launch LinkedIn outreach in parallel
Run the `linkedin-outreach` drill to set up a connection request + follow-up message sequence targeting the same prospect list. Coordinate timing so LinkedIn and email touches don't overlap for the same prospect.

### 3. Configure tracking
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `demo-storytelling-framework_email_sent`, `demo-storytelling-framework_email_replied`, `demo-storytelling-framework_meeting_booked`, `demo-storytelling-framework_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: Storytelling demos on ≥80% of opportunities over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Storytelling adoption rate
- Demo-to-proposal improvement
- Prospect engagement score
- Story resonance rate

---

## Pass threshold
**Storytelling demos on ≥80% of opportunities over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-storytelling-framework`_
