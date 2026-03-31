---
name: directories-marketplaces-smoke
description: >
    Directory & Marketplace Listings — Smoke Test. Enrich a couple of listings and gather a few
  reviews to see if directory presence drives views and at least one inquiry.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 50 views and ≥ 1 inquiry in 1 week"
kpis: ["Listing views", "Inquiry rate"]
slug: "directories-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/directories-marketplaces"
drills:
  - icp-definition
  - blog-seo-pipeline
  - threshold-engine
---
# Directory & Marketplace Listings — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Directory & Marketplace Listings — Smoke Test. Enrich a couple of listings and gather a few reviews to see if directory presence drives views and at least one inquiry.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 50 views and ≥ 1 inquiry in 1 week

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
Run the `threshold-engine` drill to measure against: ≥ 50 views and ≥ 1 inquiry in 1 week. If PASS, proceed to Baseline. If FAIL, improve listing copy or target different directories.

---

## KPIs to track
- Listing views
- Inquiry rate

---

## Pass threshold
**≥ 50 views and ≥ 1 inquiry in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/directories-marketplaces`_
