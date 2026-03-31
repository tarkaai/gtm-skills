---
name: sdk-library-development-smoke
description: >
    SDK & Library Development — Smoke Test. Build and distribute SDKs and libraries for popular
  languages and frameworks to reduce friction and drive developer adoption.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥100 SDK downloads and ≥5 developer signups in 4 weeks"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "sdk-library-development"
install: "npx gtm-skills add marketing/solution-aware/sdk-library-development"
drills:
  - icp-definition
  - blog-seo-pipeline
  - threshold-engine
---
# SDK & Library Development — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Product

## Overview
SDK & Library Development — Smoke Test. Build and distribute SDKs and libraries for popular languages and frameworks to reduce friction and drive developer adoption.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥100 SDK downloads and ≥5 developer signups in 4 weeks

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
Run the `threshold-engine` drill to measure against: ≥100 SDK downloads and ≥5 developer signups in 4 weeks. If PASS, proceed to Baseline. If FAIL, improve listing copy or target different directories.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥100 SDK downloads and ≥5 developer signups in 4 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/sdk-library-development`_
