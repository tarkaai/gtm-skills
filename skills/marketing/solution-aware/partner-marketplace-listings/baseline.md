---
name: partner-marketplace-listings-baseline
description: >
  Partner Marketplace Listings — Baseline Run. Get listed in partner app marketplaces (Salesforce AppExchange, HubSpot, Shopify) to drive discovery and leads from solution-aware users of those platforms.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥3 marketplace listings and ≥20 marketplace leads in 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "partner-marketplace-listings"
install: "npx gtm-skills add marketing/solution-aware/partner-marketplace-listings"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - crm-pipeline-setup
  - threshold-engine
---
# Partner Marketplace Listings — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Get listed in partner app marketplaces (Salesforce AppExchange, HubSpot, Shopify) to drive discovery and leads from solution-aware users of those platforms.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥3 marketplace listings and ≥20 marketplace leads in 8 weeks

---

## Budget

**Play-specific tools & costs**
- **G2, Capterra, Product Hunt — free listings:** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Clay** (Enrichment)

---

## Instructions

1. Expand scope to 100-500 targets for repeatable 2-week partner marketplace listings experiment; define detailed ICP criteria.

2. Build structured targeting list or content plan using Clay or Apollo; ensure quality and relevance to ICP.

3. Set up proper tracking in PostHog and Attio CRM to measure all activities, responses, and outcomes consistently.

4. Define pass threshold for Baseline (e.g., ≥2% conversion, ≥10 qualified results) with clear measurement criteria.

5. Create multi-touch or multi-format approach (3-5 touchpoints or content pieces) to test repeatability and engagement.

6. Execute play systematically; log every activity, response, and outcome in PostHog and CRM for complete dataset.

7. Monitor performance weekly; adjust tactics within same play framework (e.g., refine messaging, timing, targeting).

8. Track key metrics: response rate, conversion rate, cycle time from first touch to qualified outcome, and cost per result.

9. After 2 weeks, analyze results against pass threshold; identify what drove success (specific messages, channels, timing).

10. Decide: proceed to Scalable if passed threshold, iterate on targeting or approach if close, or pivot to different play if fundamentally not working.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥3 marketplace listings and ≥20 marketplace leads in 8 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/partner-marketplace-listings`_
