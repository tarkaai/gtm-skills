---
name: retargeting-campaigns-multi-platform-baseline
description: >
  Multi-platform Retargeting — Baseline Run. Expand retargeting to 2+ ad platforms
  with proper audience segmentation, conversion tracking pipeline, and budget
  allocation, running always-on for 2 weeks to prove repeatable conversions.
stage: "Marketing > Product Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=2.5% blended CTR and >=20 conversions from $1,500 retargeting spend over 2 weeks across 2+ platforms"
kpis: ["Blended CTR", "Conversions", "CPA by platform", "Landing page conversion rate", "Lead quality rate"]
slug: "retargeting-campaigns-multi-platform"
install: "npx gtm-skills add marketing/product-aware/retargeting-campaigns-multi-platform"
drills:
  - retargeting-setup
  - posthog-gtm-events
  - budget-allocation
---

# Multi-platform Retargeting — Baseline Run

> **Stage:** Marketing → Product Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Prove that multi-platform retargeting produces repeatable conversions when run always-on. You need >=2.5% blended CTR across platforms AND >=20 conversions from $1,500 total spend over 2 weeks. CPA must remain within 70% of your cold traffic CPA, confirming retargeting's structural advantage.

## Leading Indicators

- Retargeting pixels confirmed firing on all platforms within 24 hours of setup
- Audience sizes on each platform reach minimum thresholds (500 for LinkedIn, 1,000 for Meta, 100 for Google) within 48 hours
- First conversions appear on both platforms within 3 days
- CPA on retargeting is at least 30% lower than cold traffic CPA by day 5
- PostHog retargeting funnel shows consistent click-to-conversion rates week over week (variance < 20%)
- At least 60% of retargeting conversions match your ICP when checked in Attio

## Instructions

### 1. Set up multi-platform retargeting infrastructure

Run the `retargeting-setup` drill to configure retargeting across 2+ platforms:

1. Install tracking pixels on every page of your website for each platform you did not set up during Smoke:
   - Meta Pixel + Conversions API (use `meta-ads-pixel-capi` fundamental)
   - LinkedIn Insight Tag (via `linkedin-ads-campaign-setup`)
   - Google Ads remarketing tag (via `google-ads-conversion-tracking`)

2. Build 3 audience segments per platform following the retargeting-setup drill:
   - **High intent (14-day)**: Pricing page, demo page, or signup page visitors who did not convert
   - **Medium intent (30-day)**: 2+ product page visitors
   - **Low intent (7-day)**: Homepage visitors who bounced (test only on cheapest platform — typically Google Display)

3. Set audience windows per the retargeting-setup drill: 1-7 day hot audience, 8-30 day warm audience. Bid higher on the hot audience.

4. Upload exclusion lists: current customers and recent converters from Attio. Hash emails with SHA-256 before uploading to each platform.

### 2. Configure the tracking pipeline

Run the `posthog-gtm-events` drill to establish end-to-end conversion tracking:

1. Define retargeting-specific events in PostHog:
   - `retargeting_impression` — logged via n8n from platform APIs (properties: `platform`, `campaign_id`, `creative_id`, `audience_segment`)
   - `retargeting_click` — logged via PostHog UTM capture on landing pages
   - `retargeting_landing_page_view` — PostHog pageview with UTM source matching retargeting campaigns
   - `retargeting_conversion` — PostHog form submission or signup event
   - `retargeting_lead_qualified` — logged when Attio marks the lead as qualified

2. Build PostHog funnels: impression -> click -> page_view -> conversion -> qualified_lead, filterable by `platform` and `audience_segment`

3. Set up an n8n workflow that pulls ad performance data from each platform's API daily and pushes it to PostHog. This gives you one dashboard for all platforms instead of checking 2-3 ad manager UIs.

### 3. Allocate budget across platforms

Run the `budget-allocation` drill with $1,500 total budget over 2 weeks ($107/day):

1. Use your Smoke test data to seed the allocation. If Meta had the best CPA in Smoke, allocate 60% to Meta, 30% to the next platform, 10% to the third.

2. If no Smoke data for a platform, start with equal splits and let the first 5 days of data guide reallocation.

3. Set daily budget caps on each platform to prevent overspend. Configure n8n alerts if any platform's daily spend exceeds 120% of its daily budget.

4. Apply the 70/20/10 framework from the budget-allocation drill:
   - 70% to the platform/audience combo with the lowest CPA from Smoke
   - 20% to the second platform for optimization testing
   - 10% to test the low-intent audience on the cheapest platform

5. Set rebalancing triggers: if a platform's CPA exceeds 150% of target for 5 consecutive days, reduce its budget by 30% and shift to the better-performing platform.

### 4. Launch retargeting campaigns on all platforms

Create campaigns on each platform with these specifications:

**Per platform:**
- Campaign objective: Conversions
- 3-5 ad variants per audience segment (reuse the winning variant from Smoke + 2-4 new variants)
- Frequency cap: maximum 5 impressions/person/week on Meta and Google, 3/week on LinkedIn
- Ad creative: retargeting-specific messaging — reference the visitor's previous action ("Saw our pricing? Here's what {N} teams chose.")
- Landing page: use the retargeting landing page from Smoke, or build a platform-specific variant

**Human action required:** Activate all campaigns simultaneously. Running all platforms at the same time ensures comparable data for budget allocation decisions.

### 5. Monitor and adjust weekly

**Week 1 (days 1-7):**
- Daily: check PostHog retargeting dashboard for each platform's CTR, CPA, and conversion count
- Day 3: verify all tracking is working — each platform should show impressions, and PostHog should show corresponding clicks and pageviews
- Day 5: first budget reallocation. Shift 10-20% from the worst-performing platform to the best. Do NOT pause any platform yet — you need 7 days minimum.
- Day 7: evaluate creative performance. Pause any ad variant with CTR below 1% (Meta/Google) or 0.5% (LinkedIn) after 500+ impressions.

**Week 2 (days 8-14):**
- Day 8: launch 2-3 replacement creatives for any paused variants
- Day 10: second budget reallocation based on full-week CPA data
- Day 14: final evaluation

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 14 days:

- **Pass**: Blended CTR >= 2.5% AND total conversions >= 20 AND CPA at least 30% better than cold traffic
- **Marginal pass**: Blended CTR >= 2% AND conversions >= 15 — continue for 2 more weeks to confirm repeatability
- **Fail — platform problem**: One platform converting well, others not — consolidate to the winning platform and add budget. Retest multi-platform later with different audiences.
- **Fail — audience problem**: High-intent audience converts but medium/low do not — narrow focus to high-intent only and reduce audience windows to 7 days
- **Hard fail**: Blended CTR < 1.5% AND conversions < 10 after $1,500 spend — your website traffic volume may be too low for effective retargeting (need 3,000+ monthly visitors across platforms)

Document: per-platform CPA, per-audience-segment CPA, best-performing creative per platform, lead quality rate (% of conversions that are ICP matches).

## Time Estimate

- Multi-platform pixel setup and audience creation: 4 hours
- PostHog event taxonomy and n8n sync workflows: 4 hours
- Budget allocation modeling and campaign creation: 3 hours
- Ad creative writing (3-5 variants per platform): 3 hours
- Weekly monitoring and adjustments (2 weeks): 3 hours
- Final evaluation and documentation: 1 hour
- **Total: 18 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Meta Ads | Retargeting on Facebook/Instagram | Ad spend: ~$600-900 of total budget. No platform fee. https://www.facebook.com/business/ads/pricing |
| LinkedIn Ads | Retargeting on LinkedIn | Ad spend: ~$300-600 of total budget. Min $10/day. https://business.linkedin.com/advertise/ads/pricing |
| Google Ads | Retargeting on Display Network | Ad spend: ~$150-300 of total budget. CPC ~$0.66-1.23 for remarketing. https://ads.google.com/intl/en/home/pricing/ |
| Webflow | Landing page hosting | Free or $14/mo Starter. https://webflow.com/pricing |
| PostHog | Unified tracking and funnels | Free up to 1M events/mo. https://posthog.com/pricing |

**Estimated total cost: $1,500 ad spend + $0-14 landing page = $1,500-1,514/2 weeks**

## Drills Referenced

- `retargeting-setup` — configure retargeting pixels, build segmented audiences, set frequency caps across all platforms
- `posthog-gtm-events` — establish the event taxonomy and funnels for unified retargeting measurement
- `budget-allocation` — distribute and rebalance budget across platforms based on CPA performance data
