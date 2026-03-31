---
name: review-ask-to-early-users-smoke
description: >
    Review Ask to Early Users — Smoke Test. Request reviews from a handful of early users to build
  social proof and see if new reviews correlate with at least one inbound lead.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 3 new reviews and ≥ 1 inbound lead in 2 weeks"
kpis: ["3 new reviews", "1 inbound"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - icp-definition
  - blog-seo-pipeline
  - threshold-engine
---
# Review Ask to Early Users — Smoke Test

> **Stage:** Marketing → Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Review Ask to Early Users — Smoke Test. Request reviews from a handful of early users to build social proof and see if new reviews correlate with at least one inbound lead.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 3 new reviews and ≥ 1 inbound lead in 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Identify target directories
Run the `icp-definition` drill to map where your ICP discovers products: G2, Capterra, Product Hunt, industry-specific directories, GitHub, Chrome Web Store, marketplace listings. Prioritize by relevance and traffic.

### 2. Create optimized listings
Run the `blog-seo-pipeline` drill to research keywords your ICP uses when searching directories. Use these keywords in your listing titles, descriptions, and feature lists. Write compelling copy that differentiates you from competitors on the same platform.

**Human action required:** Create or update your listings on 3-5 directories. Submit for review. Ask 5-10 existing customers to leave reviews. Log all listings in Attio.

### 3. Track listing performance
Monitor: page views, clicks to your website, reviews received, leads generated from each directory. Use UTM parameters on all listing links.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥ 3 new reviews and ≥ 1 inbound lead in 2 weeks. If PASS, proceed to Baseline. If FAIL, improve listing copy or target different directories.

---

## KPIs to track
- 3 new reviews
- 1 inbound

---

## Pass threshold
**≥ 3 new reviews and ≥ 1 inbound lead in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/review-ask-to-early-users`_
