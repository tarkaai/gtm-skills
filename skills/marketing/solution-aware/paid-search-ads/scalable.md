---
name: paid-search-ads-scalable
description: >
  Paid Search Ads — Scalable Automation. Scale search ad spend to $3,000-10,000/mo with
  automated search query mining, systematic A/B testing of ads and landing pages, cross-platform
  budget optimization, and CRM-synced conversion tracking.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=30 leads or >=16 meetings over 2 months with CPA within 120% of Baseline"
kpis: ["Cost per lead", "Cost per meeting", "Blended CPA across platforms", "Search impression share on top keywords (>70%)", "Lead-to-meeting conversion rate", "Monthly lead volume trend"]
slug: "paid-search-ads"
install: "npx gtm-skills add marketing/solution-aware/paid-search-ads"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
  - search-ads-performance-monitor
  - budget-allocation
---

# Paid Search Ads — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Find the 10x multiplier for your search ads. At Scalable, you automate the manual work from Baseline (search query mining, negative keyword management, budget rebalancing) and invest in systematic testing to find the best keyword-ad-landing page combinations. The goal is to scale spend 3-5x while keeping CPA within 120% of your Baseline cost per meeting.

**Pass threshold:** >=30 leads or >=16 meetings over 2 months with CPA within 120% of Baseline.

## Leading Indicators

- Weekly lead volume increasing month-over-month without CPA degradation
- Automated search query mining recovering >$200/mo in wasted spend
- A/B tests producing at least 1 statistically significant winner per month
- Google Ads Quality Scores averaging 7+ across top keywords
- Microsoft Ads contributing >=15% of total search leads (cross-platform diversification)
- CRM-to-ad-platform conversion sync working (verified by matching conversion counts)

## Instructions

### 1. Automate search query mining and negative keyword management

Run the `search-ads-performance-monitor` drill to build automated n8n workflows that:

- Pull search term reports from Google Ads and Microsoft Ads weekly
- Classify queries as converting, promising, wasteful, or irrelevant
- Auto-add wasteful/irrelevant queries as campaign-level negative keywords via API
- Flag promising queries (high clicks, no conversions yet) for human review
- Post a weekly search terms digest to Slack: negatives added, keywords promoted, wasted spend recovered

This eliminates the 1-2 hours/week of manual search query mining from Baseline.

### 2. Build systematic A/B testing for ads and landing pages

Run the `ab-test-orchestrator` drill to set up continuous testing:

**Ad copy tests:**
- Test one variable at a time: headline hook, CTA text, social proof claim, or description angle
- Use PostHog feature flags to track which ad variant drove each landing page visit
- Run each test for 14 days or until 200+ clicks per variant (whichever is longer)
- Target: 1 winning ad test per month that improves CTR by >=0.5 percentage points

**Landing page tests:**
- Use PostHog experiments to A/B test: headline, hero section, form length, CTA copy, social proof placement
- Split traffic 50/50 between control and variant
- Measure landing page conversion rate (form submissions / page views) as primary metric
- Guard against false positives: require 95% confidence and >=200 visitors per variant
- Target: 1 winning page test per month that improves conversion rate by >=1 percentage point

### 3. Sync CRM data to ad platforms

Run the `tool-sync-workflow` drill to build bidirectional data flows:

**Leads to CRM (already set up at Baseline):**
- Form submission → n8n → Attio contact creation with source attribution

**CRM outcomes back to ad platforms (new at Scalable):**
- When a lead in Attio progresses to "Meeting Booked" or "Closed Won", fire a server-side conversion event back to Google Ads (using the Google Ads Conversions API) and Microsoft Ads (using CAPI)
- This enables the ad platforms to optimize for downstream outcomes, not just form submissions
- Build the n8n workflow: Attio webhook (deal stage change) → map to conversion event → POST to Google/Microsoft conversion endpoints
- Verify: conversion counts in Google Ads and Microsoft Ads should match Attio within 24 hours

**Exclusion lists:**
- Weekly n8n workflow: export all current customers and active deals from Attio → upload as exclusion audiences to Google and Microsoft Ads
- This prevents spending ad budget on people who are already in your pipeline

### 4. Scale budget with automated guardrails

Run the `budget-allocation` drill at the scaled level:

- Increase total budget to $3,000-10,000/mo
- Allocate: 60% Google Ads, 25% Microsoft Ads, 15% retargeting (adjust based on actual CPA data)
- Build n8n budget monitoring workflows:
  - If any campaign's 7-day CPA exceeds 150% of target, automatically reduce daily budget by 25%
  - If any campaign's 7-day CPA is below 75% of target, increase daily budget by 20% (up to a maximum)
  - If total monthly spend is on pace to exceed budget by day 20, reduce all budgets proportionally
- Shift from "Maximize Conversions" to "Target CPA" bidding on Google once you have 50+ conversions in 30 days. Set target CPA to your Baseline cost per meeting.

### 5. Expand keyword coverage strategically

Add new keyword categories now that budget supports it:
- **Long-tail exact match**: Add 2-3 word variations of your top converters that you discovered via search query mining
- **Competitor keywords**: If not tested at Baseline, add "[competitor] alternative" and "[competitor] vs [your product]" ad groups with dedicated landing pages (comparison pages work best here)
- **Problem/pain keywords**: Add ad groups targeting the specific problems your product solves (e.g., "how to reduce sales cycle time")
- **Branded defense**: If competitors are bidding on your brand name, add branded campaigns to defend your SERP position

Track new keyword categories separately in PostHog so you can measure which expansions are profitable.

### 6. Evaluate against threshold

At the end of 2 months, compile:
- Total leads across Google + Microsoft + retargeting
- Total meetings booked (from Attio)
- Blended CPA: total spend / total meetings
- CPA ratio: Scalable CPA / Baseline CPA (must be <=1.2x)
- Lead volume trend: month 2 leads vs month 1 leads

**Pass:** >=30 leads or >=16 meetings AND CPA within 120% of Baseline. Proceed to Durable.
**Marginal pass (volume close but CPA 120-150% of Baseline):** Stay at Scalable. Focus on CPA optimization: tighter negative keywords, better landing pages, CRM-synced bidding.
**Fail -- CPA blew up:** Scaling too fast. Pull back to Baseline budget, identify which keyword expansions or platform changes caused the CPA increase, and re-scale more conservatively.

Document what worked: which keywords, which ad variants, which landing page version, which platform split. This documentation feeds directly into the Durable agent's knowledge base.

## Time Estimate

- 8 hours: Set up automated search query mining and negative keyword workflows
- 8 hours: Build A/B testing infrastructure for ads and landing pages
- 8 hours: Build CRM-to-ad-platform sync and exclusion list automation
- 6 hours: Budget allocation automation and guardrail workflows
- 4 hours: Keyword expansion research and campaign restructuring
- 8 hours: Monthly optimization reviews and A/B test analysis (4 hours x 2 months)
- 4 hours: Landing page variant creation and testing
- 4 hours: Final threshold evaluation and documentation for Durable handoff

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Search campaigns + retargeting | $2,000-6,000/mo budget — [ads.google.com](https://ads.google.com) |
| Microsoft Advertising | Bing search campaigns | $750-2,500/mo budget — [ads.microsoft.com](https://ads.microsoft.com) |
| Webflow | Landing pages and A/B test variants | CMS $23/mo — [webflow.com/pricing](https://webflow.com/pricing) |
| PostHog | Analytics, experiments, feature flags | Free tier or Growth ~$0-100/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation (query mining, syncs, alerts) | Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM, lead tracking, conversion source | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Meeting booking | Free tier or Team $12/user/mo — [cal.com](https://cal.com) |

**Estimated play-specific cost:** $3,000-10,000/mo ad spend + ~$120-200/mo tooling

## Drills Referenced

- `ab-test-orchestrator` — Systematic A/B testing of ad copy and landing page elements
- `tool-sync-workflow` — Bidirectional CRM-to-ad-platform data sync and exclusion lists
- `search-ads-performance-monitor` — Automated search query mining, negative keywords, and weekly reporting
- `budget-allocation` — Performance-based budget distribution with automated guardrails
