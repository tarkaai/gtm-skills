---
name: github-project-promotion-baseline
description: >
    GitHub Project Promotion — Baseline Run. Promote open-source projects on GitHub to build
  developer awareness, drive repository stars, and generate inbound technical leads.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥500 stars and ≥15 qualified developer leads in 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "github-project-promotion"
install: "npx gtm-skills add marketing/solution-aware/github-project-promotion"
drills:
  - posthog-gtm-events
  - landing-page-pipeline
---
# GitHub Project Promotion — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Social

## Overview
GitHub Project Promotion — Baseline Run. Promote open-source projects on GitHub to build developer awareness, drive repository stars, and generate inbound technical leads.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥500 stars and ≥15 qualified developer leads in 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure tracking
Run the `posthog-gtm-events` drill to track: `github-project-promotion_listing_view`, `github-project-promotion_listing_click`, `github-project-promotion_listing_signup`, `github-project-promotion_review_submitted`. Use UTM parameters per directory for attribution.

### 2. Build landing pages for directory traffic
Run the `landing-page-pipeline` drill to create directory-specific landing pages. Match the messaging to what users expect when coming from each directory. Include social proof relevant to that directory's audience.

### 3. Scale review collection
Implement a systematic review collection process: after positive customer interactions, send a Loops email requesting a review on the relevant directory. Track review velocity in PostHog.

### 4. Evaluate against threshold
Measure against: ≥500 stars and ≥15 qualified developer leads in 8 weeks. If PASS, proceed to Scalable. If FAIL, focus on the directories driving the most qualified traffic.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥500 stars and ≥15 qualified developer leads in 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/github-project-promotion`_
