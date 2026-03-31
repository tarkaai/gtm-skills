---
name: budget-allocation
description: Allocate and rebalance paid media budget across channels based on performance data
category: Paid
tools:
  - PostHog
  - Google Ads
  - LinkedIn Ads
  - Meta Ads
fundamentals:
  - posthog-event-tracking
  - posthog-funnel-tracking
  - google-ads-campaign-setup
  - linkedin-ads-campaign-setup
  - meta-ads-campaign-setup
---

# Budget Allocation

This drill provides a framework for distributing your paid media budget across channels and campaigns, then rebalancing based on performance data. It prevents the common trap of spreading budget evenly or sticking with an initial split that no longer matches reality.

## Prerequisites

- Active campaigns on at least 2 ad platforms
- PostHog tracking conversions from all paid channels
- At least 30 days of campaign data (enough to identify trends)
- Clear definition of your target cost per acquisition (CPA) or target return on ad spend (ROAS)

## Steps

### 1. Establish your total budget and constraints

Define your monthly paid media budget and any constraints: minimum spend per platform (some platforms need a threshold to gather data), contractual commitments, or seasonal adjustments. Set your target CPA or ROAS as the primary metric. Secondary metrics: pipeline generated, qualified leads, and time to conversion.

### 2. Audit current performance by channel

Using `posthog-funnel-tracking`, pull conversion data for each channel. For every platform, calculate:

- **Cost per click (CPC)**
- **Click-through rate (CTR)**
- **Cost per lead (CPL)**
- **Cost per qualified lead**
- **Cost per customer acquired (CPA)**
- **Return on ad spend (ROAS)** if revenue attribution is possible

Do not compare CPCs across platforms — compare CPAs. A $15 LinkedIn click that converts at 5% ($300 CPA) might outperform a $2 Google click that converts at 0.5% ($400 CPA).

### 3. Apply the 70/20/10 framework

Allocate budget in three buckets:

- **70% to proven performers**: Channels and campaigns with CPA below your target. These are your workhorses. Scale them until performance degrades.
- **20% to optimization experiments**: Campaigns that show promise but need more data or refinement. Test new audiences, creative, or keywords. Promote winners to the 70% bucket.
- **10% to new channel exploration**: Test entirely new platforms or campaign types. Accept that most will fail, but the winners refresh your pipeline.

### 4. Set rebalancing triggers

Do not wait for monthly reviews to shift budget. Define triggers:

- If a campaign's CPA exceeds 150% of target for 7 consecutive days, reduce budget by 30%
- If a campaign's CPA is below 75% of target for 7 days, increase budget by 20%
- If a new test channel hits target CPA within 14 days, promote to optimization bucket
- If a test channel exceeds 200% of target CPA after 21 days, pause it

### 5. Account for full-funnel attribution

Using `posthog-event-tracking`, track the full customer journey across channels. First-touch attribution overvalues awareness channels. Last-touch overvalues bottom-of-funnel. Use a multi-touch model: assign partial credit to each touchpoint. This prevents cutting awareness spending that actually feeds your retargeting and search campaigns.

### 6. Review and adjust monthly

Run a monthly budget review: compare actual CPA to target by channel, review which campaigns moved between buckets, calculate overall blended CPA, and project next month's allocation. Document what you learned. Over time, your allocation should converge toward the most efficient channel mix for your specific product and market.
