---
name: poc-management-framework-baseline
description: >
    POC Management Framework — Baseline Run. Run structured proof-of-concept with clear success
  criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Baseline Run"
time: "24 hours over 4 weeks"
outcome: "POCs on ≥80% of qualified opportunities over 4 weeks"
kpis: ["POC qualification accuracy", "Success criteria achievement rate", "POC-to-close conversion", "Time from POC to decision", "POC engagement score"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# POC Management Framework — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Overview
POC Management Framework — Baseline Run. Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.

**Time commitment:** 24 hours over 4 weeks
**Pass threshold:** POCs on ≥80% of qualified opportunities over 4 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `poc-management-framework_email_sent`, `poc-management-framework_email_replied`, `poc-management-framework_meeting_booked`, `poc-management-framework_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: POCs on ≥80% of qualified opportunities over 4 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- POC qualification accuracy
- Success criteria achievement rate
- POC-to-close conversion
- Time from POC to decision
- POC engagement score

---

## Pass threshold
**POCs on ≥80% of qualified opportunities over 4 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/poc-management-framework`_
