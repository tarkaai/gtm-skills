---
name: risk-assessment-discovery-baseline
description: >
    Risk & Concern Discovery — Baseline Run. Surface concerns, risks, and objections early in the
  sales cycle to address them proactively rather than encountering surprises at decision time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Risks identified and mitigated on ≥80% of opportunities over 2 weeks"
kpis: ["Risk discovery rate", "Risk mitigation success rate", "Close rate impact", "Late-stage surprise reduction"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Risk & Concern Discovery — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Risk & Concern Discovery — Baseline Run. Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Risks identified and mitigated on ≥80% of opportunities over 2 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `risk-assessment-discovery_email_sent`, `risk-assessment-discovery_email_replied`, `risk-assessment-discovery_meeting_booked`, `risk-assessment-discovery_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: Risks identified and mitigated on ≥80% of opportunities over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Risk discovery rate
- Risk mitigation success rate
- Close rate impact
- Late-stage surprise reduction

---

## Pass threshold
**Risks identified and mitigated on ≥80% of opportunities over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/risk-assessment-discovery`_
