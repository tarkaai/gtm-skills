---
name: sdk-library-development-baseline
description: >
    SDK & Library Development — Baseline Run. Build and distribute SDKs and libraries for popular
  languages and frameworks to reduce friction and drive developer adoption.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Product"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥500 downloads and ≥20 qualified developer signups across 2-3 SDKs in 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "sdk-library-development"
install: "npx gtm-skills add marketing/solution-aware/sdk-library-development"
drills:
  - posthog-gtm-events
  - landing-page-pipeline
---
# SDK & Library Development — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Product

## Overview
SDK & Library Development — Baseline Run. Build and distribute SDKs and libraries for popular languages and frameworks to reduce friction and drive developer adoption.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥500 downloads and ≥20 qualified developer signups across 2-3 SDKs in 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure tracking
Run the `posthog-gtm-events` drill to track: `sdk-library-development_listing_view`, `sdk-library-development_listing_click`, `sdk-library-development_listing_signup`, `sdk-library-development_review_submitted`. Use UTM parameters per directory for attribution.

### 2. Build landing pages for directory traffic
Run the `landing-page-pipeline` drill to create directory-specific landing pages. Match the messaging to what users expect when coming from each directory. Include social proof relevant to that directory's audience.

### 3. Scale review collection
Implement a systematic review collection process: after positive customer interactions, send a Loops email requesting a review on the relevant directory. Track review velocity in PostHog.

### 4. Evaluate against threshold
Measure against: ≥500 downloads and ≥20 qualified developer signups across 2-3 SDKs in 8 weeks. If PASS, proceed to Scalable. If FAIL, focus on the directories driving the most qualified traffic.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥500 downloads and ≥20 qualified developer signups across 2-3 SDKs in 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/sdk-library-development`_
