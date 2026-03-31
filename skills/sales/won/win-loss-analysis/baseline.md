---
name: win-loss-analysis-baseline
description: >
    Win/Loss Analysis Program — Baseline Run. Systematically analyze won and lost deals to improve
  sales effectiveness, product positioning, and competitive strategy, from manual post-deal
  interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and
  recommends strategic adjustments.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks"
kpis: ["Interview completion rate", "Insights identified", "Changes implemented", "Win/loss reason distribution"]
slug: "win-loss-analysis"
install: "npx gtm-skills add sales/won/win-loss-analysis"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Win/Loss Analysis Program — Baseline Run

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Win/Loss Analysis Program — Baseline Run. Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.

**Time commitment:** 24 hours over 2 weeks
**Pass threshold:** >=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `win-loss-analysis_email_sent`, `win-loss-analysis_email_replied`, `win-loss-analysis_meeting_booked`, `win-loss-analysis_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: >=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Interview completion rate
- Insights identified
- Changes implemented
- Win/loss reason distribution

---

## Pass threshold
**>=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/win-loss-analysis`_
