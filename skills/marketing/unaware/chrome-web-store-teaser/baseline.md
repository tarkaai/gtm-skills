---
name: chrome-web-store-teaser-baseline
description: >
    Chrome Extension Teaser — Baseline Run. Ship a minimal preview extension with a landing page to
  see if installs and at least one lead show dev or power-user interest before investing further.
stage: "Marketing > Unaware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 50 installs and ≥ 3 leads over 2 weeks"
kpis: ["Store listing views", "Install rate"]
slug: "chrome-web-store-teaser"
install: "npx gtm-skills add marketing/unaware/chrome-web-store-teaser"
drills:
  - posthog-gtm-events
  - landing-page-pipeline
---
# Chrome Extension Teaser — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Chrome Extension Teaser — Baseline Run. Ship a minimal preview extension with a landing page to see if installs and at least one lead show dev or power-user interest before investing further.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 50 installs and ≥ 3 leads over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure tracking
Run the `posthog-gtm-events` drill to track: `chrome-web-store-teaser_listing_view`, `chrome-web-store-teaser_listing_click`, `chrome-web-store-teaser_listing_signup`, `chrome-web-store-teaser_review_submitted`. Use UTM parameters per directory for attribution.

### 2. Build landing pages for directory traffic
Run the `landing-page-pipeline` drill to create directory-specific landing pages. Match the messaging to what users expect when coming from each directory. Include social proof relevant to that directory's audience.

### 3. Scale review collection
Implement a systematic review collection process: after positive customer interactions, send a Loops email requesting a review on the relevant directory. Track review velocity in PostHog.

### 4. Evaluate against threshold
Measure against: ≥ 50 installs and ≥ 3 leads over 2 weeks. If PASS, proceed to Scalable. If FAIL, focus on the directories driving the most qualified traffic.

---

## KPIs to track
- Store listing views
- Install rate

---

## Pass threshold
**≥ 50 installs and ≥ 3 leads over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/chrome-web-store-teaser`_
