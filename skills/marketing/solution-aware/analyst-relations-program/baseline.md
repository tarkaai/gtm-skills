---
name: analyst-relations-program-baseline
description: >
    Analyst Relations Program — Baseline Run. Engage with Gartner, Forrester, and G2 analysts for
  mentions, placement, and credibility to influence solution-aware buyers in research phase.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Other"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥6 analyst briefings and ≥1 analyst mention or report inclusion in 10 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "analyst-relations-program"
install: "npx gtm-skills add marketing/solution-aware/analyst-relations-program"
drills:
  - case-study-creation
  - newsletter-pipeline
  - posthog-gtm-events
---
# Analyst Relations Program — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Other

## Overview
Analyst Relations Program — Baseline Run. Engage with Gartner, Forrester, and G2 analysts for mentions, placement, and credibility to influence solution-aware buyers in research phase.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥6 analyst briefings and ≥1 analyst mention or report inclusion in 10 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build a PR content machine
Run the `case-study-creation` drill to create 2-3 customer case studies that serve as PR assets. Run the `newsletter-pipeline` drill to start your own newsletter that establishes thought leadership and gives journalists a reason to follow you.

### 2. Configure PR tracking
Run the `posthog-gtm-events` drill to track: `analyst-relations-program_mention_published`, `analyst-relations-program_backlink_acquired`, `analyst-relations-program_referral_traffic`, `analyst-relations-program_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: ≥6 analyst briefings and ≥1 analyst mention or report inclusion in 10 weeks. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥6 analyst briefings and ≥1 analyst mention or report inclusion in 10 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/analyst-relations-program`_
