---
name: competitive-situation-analysis-baseline
description: >
    Competitive Situation Assessment — Baseline Run. Discover which competitors prospects are
  evaluating to position differentiation effectively and develop winning strategies against specific
  alternatives.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Competitive situation assessed on ≥80% of opportunities over 2 weeks"
kpis: ["Competitive discovery rate", "Win rate by competitor", "Competitive positioning effectiveness", "Intelligence accuracy"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Competitive Situation Assessment — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Competitive Situation Assessment — Baseline Run. Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.

**Time commitment:** 15 hours over 2 weeks
**Pass threshold:** Competitive situation assessed on ≥80% of opportunities over 2 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `competitive-situation-analysis_email_sent`, `competitive-situation-analysis_email_replied`, `competitive-situation-analysis_meeting_booked`, `competitive-situation-analysis_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: Competitive situation assessed on ≥80% of opportunities over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Competitive discovery rate
- Win rate by competitor
- Competitive positioning effectiveness
- Intelligence accuracy

---

## Pass threshold
**Competitive situation assessed on ≥80% of opportunities over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/competitive-situation-analysis`_
