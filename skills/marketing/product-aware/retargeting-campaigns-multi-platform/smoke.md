---
name: retargeting-campaigns-multi-platform-smoke
description: >
  Multi-platform Retargeting — Smoke Test. Launch a single-platform retargeting campaign
  against website visitors who viewed pricing or demo pages, proving that re-engaging
  product-aware prospects generates clicks and conversions at a viable cost.
stage: "Marketing > Product Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3% CTR and >=5 conversions from a $300-500 single-platform retargeting test"
kpis: ["CTR", "Conversions", "Cost per conversion", "Landing page conversion rate"]
slug: "retargeting-campaigns-multi-platform"
install: "npx gtm-skills add marketing/product-aware/retargeting-campaigns-multi-platform"
drills:
  - ad-campaign-setup
  - landing-page-pipeline
  - threshold-engine
---

# Multi-platform Retargeting — Smoke Test

> **Stage:** Marketing → Product Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Prove that retargeting website visitors who showed product intent generates conversions at a cost that justifies scaling. You need >=3% CTR and >=5 conversions from a $300-500 test budget on a single ad platform. If retargeting does not outperform cold traffic by at least 2x on CPA, the play fails.

## Leading Indicators

- Retargeting pixel fires confirmed on all key pages within first 24 hours (verify in platform debug tools)
- Audience size reaches 500+ matched visitors within 48 hours of pixel installation
- First clicks arrive within 24 hours of campaign launch
- CTR exceeds 1% within the first 3 days (early signal of creative-audience fit)
- Landing page receives at least 20 visits from retargeting clicks by day 4

## Instructions

### 1. Choose one platform and install tracking

Pick the platform where you have the most existing website traffic data:
- **Meta**: Best if you already have Meta Pixel installed or have 1,000+ monthly visitors. Use `meta-ads-pixel-capi` to set up the pixel and Conversions API.
- **LinkedIn**: Best for B2B with defined ICP by job title/seniority. Use `linkedin-ads-campaign-setup` to install the Insight Tag.
- **Google Display**: Best for broad reach at low CPM. Use `google-ads-conversion-tracking` to install the Google tag.

Run the `ad-campaign-setup` drill with these parameters:
- Objective: Conversions (not traffic, not awareness)
- Budget: $300-500 total over 7 days ($43-71/day)
- Platform: your chosen single platform
- Campaign type: Retargeting (website visitors only)

### 2. Build retargeting audiences

Create two audiences on your chosen platform:

**High-intent audience**: Visitors to pricing page, demo page, or signup page in the last 14 days who did NOT convert. This is your primary audience.

**Medium-intent audience**: Visitors who viewed 2+ product pages in the last 30 days. This is your test audience.

Exclude: current customers (export email list from Attio, hash with SHA-256, upload as exclusion audience), people who already converted, and your own team's IP addresses.

Verify each audience has at least 500 people. If high-intent is below 500, extend the lookback window to 30 days.

### 3. Build a dedicated landing page

Run the `landing-page-pipeline` drill to create a retargeting-specific landing page:
- Headline must match the ad copy exactly (message match reduces bounce rate by 20-40%)
- Include one specific proof point: a customer result, a metric, or a testimonial
- Single CTA: "Start Free Trial", "Book Demo", or "Get Started" — match to your product's primary conversion action
- Install PostHog tracking: `page_view`, `scroll_depth`, `cta_click`, `form_submit` events
- Remove all navigation links — the only exit should be the CTA or back button

### 4. Create 3 ad variants

Write 3 retargeting ad variants. These visitors already know your product, so lead with conversion-focused messaging, not education:

- **Variant A — Direct CTA**: "Still evaluating {category}? Start your free trial today." Focus on removing friction.
- **Variant B — Social proof**: "Join {N} teams already using {product}. See why on a quick demo." Focus on momentum.
- **Variant C — Urgency/scarcity**: "Your {product} evaluation expires in {N} days. Pick up where you left off." Focus on re-engagement.

Upload all 3 variants. Let the platform optimize delivery across them. Do NOT pick a winner manually during the test.

### 5. Launch and collect data for 7 days

**Human action required:** Set the campaign live with $300-500 total budget. Do not adjust targeting, creative, or bids during the 7-day test window. Let the data accumulate without interference.

Monitor daily (read-only): impressions, clicks, CTR, conversions, cost per conversion, landing page conversion rate. Log each day's numbers in a PostHog custom event: `retargeting_daily_report` with properties `{day, impressions, clicks, ctr, conversions, cpa, spend}`.

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 7 days with these criteria:

- **Pass**: CTR >= 3% AND conversions >= 5 AND CPA is at least 2x better than your cold traffic CPA
- **Marginal pass**: CTR >= 2% AND conversions >= 3 — extend the test 7 more days with same budget
- **Fail — creative problem**: CTR < 1% with 500+ impressions — the ads are not resonating. Write 3 new variants and retest.
- **Fail — audience problem**: CTR >= 2% but 0 conversions — the landing page or offer is the bottleneck. Revise the landing page and retest.
- **Hard fail**: CTR < 1% AND 0 conversions after 1,000+ impressions — retargeting may not work for your traffic volume or product. Consider whether you have enough website visitors (need 1,000+/month) before retrying.

Document all results: which platform, which audience performed better (high vs. medium intent), which ad variant got the most clicks, landing page conversion rate, and total CPA.

## Time Estimate

- Platform setup and pixel installation: 1 hour
- Audience creation and exclusion list upload: 1 hour
- Landing page build with PostHog tracking: 2 hours
- Ad creative writing and upload: 1 hour
- Daily monitoring over 7 days + final evaluation: 1 hour
- **Total: 6 hours active work over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Meta Ads | Retargeting on Facebook/Instagram | Ad spend only; $300-500 test budget. No platform fee. https://www.facebook.com/business/ads/pricing |
| LinkedIn Ads | Retargeting on LinkedIn (alternative) | Ad spend only; $300-500 test budget. Min $10/day. https://business.linkedin.com/advertise/ads/pricing |
| Google Ads | Retargeting on Display Network (alternative) | Ad spend only; $300-500 test budget. No minimum. https://ads.google.com/intl/en/home/pricing/ |
| Webflow | Landing page builder | Free plan for 1 page, or $14/mo Starter. https://webflow.com/pricing |
| PostHog | Conversion tracking and analytics | Free up to 1M events/mo. https://posthog.com/pricing |

**Estimated total cost: $300-500 ad spend + $0-14 for landing page = $300-514**

## Drills Referenced

- `ad-campaign-setup` — configure the retargeting campaign on your chosen platform with proper tracking and budget
- `landing-page-pipeline` — build a high-converting retargeting landing page with PostHog tracking
- `threshold-engine` — evaluate results against pass/fail criteria and recommend next action
