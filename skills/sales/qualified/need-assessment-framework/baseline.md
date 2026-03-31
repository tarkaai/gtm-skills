---
name: need-assessment-framework-baseline
description: >
    Need Assessment Framework — Baseline Run. Systematically evaluate whether prospects have genuine
  business needs your product solves to avoid wasting time on poor-fit opportunities.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Need assessment completed on ≥80% of opportunities over 2 weeks"
kpis: ["Need assessment completion rate", "Need score correlation with close rate", "Disqualification rate", "Deal velocity by need tier"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Need Assessment Framework — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Need Assessment Framework — Baseline Run. Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Need assessment completed on ≥80% of opportunities over 2 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `need-assessment-framework_email_sent`, `need-assessment-framework_email_replied`, `need-assessment-framework_meeting_booked`, `need-assessment-framework_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: Need assessment completed on ≥80% of opportunities over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Need assessment completion rate
- Need score correlation with close rate
- Disqualification rate
- Deal velocity by need tier

---

## Pass threshold
**Need assessment completed on ≥80% of opportunities over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/need-assessment-framework`_
