---
name: twitter-x-ads-baseline
description: >
    Twitter/X Ads — Baseline Run. Run promoted tweets and accounts targeting specific audiences,
  keywords, and interests to build awareness and drive traffic from solution-aware users.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥150,000 impressions and ≥20 qualified leads from $1,500 budget over 2 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - budget-allocation
  - posthog-gtm-events
  - retargeting-setup
---
# Twitter/X Ads — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Overview
Twitter/X Ads — Baseline Run. Run promoted tweets and accounts targeting specific audiences, keywords, and interests to build awareness and drive traffic from solution-aware users.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥150,000 impressions and ≥20 qualified leads from $1,500 budget over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Optimize budget allocation
Run the `budget-allocation` drill to analyze your Smoke test data and allocate budget across ad sets, audiences, and platforms. Shift budget toward the highest-performing segments. Set daily budget caps to prevent overspend.

### 2. Set up retargeting
Run the `retargeting-setup` drill to configure retargeting audiences: website visitors who didn't convert, landing page visitors, and engaged social followers. Create retargeting ad variants with stronger CTAs.

### 3. Configure tracking pipeline
Run the `posthog-gtm-events` drill to set up end-to-end tracking: `twitter-x-ads_ad_click`, `twitter-x-ads_landing_page_view`, `twitter-x-ads_form_submit`, `twitter-x-ads_lead_qualified`. Connect ad platform data to PostHog via webhooks for unified reporting.

### 4. Run for 2 weeks at increased budget
Scale budget to $1,000-3,000 for the test period. Monitor daily: CPA trends, quality of leads entering CRM, ad fatigue indicators (declining CTR). Make weekly adjustments to targeting and creative.

### 5. Evaluate against threshold
Measure against: ≥150,000 impressions and ≥20 qualified leads from $1,500 budget over 2 weeks. If PASS, proceed to Scalable. If FAIL, test different audiences, creatives, or platforms.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥150,000 impressions and ≥20 qualified leads from $1,500 budget over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/twitter-x-ads`_
