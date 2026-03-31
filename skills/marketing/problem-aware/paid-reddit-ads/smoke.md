---
name: paid-reddit-ads-smoke
description: >
  Paid Reddit Ads — Smoke Test. Run a $200-500 Reddit ad campaign targeting 2-3 subreddit
  clusters with one landing page to test if paid community placement drives leads or a meeting.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Smoke Test"
time: "4 hours setup + 7 days runtime"
outcome: "≥ 2 leads or ≥ 1 meeting in 7 days"
kpis: ["Click-through rate", "Cost per click", "Landing page conversion rate", "Leads generated"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
drills:
  - reddit-ads-campaign-build
  - threshold-engine
---

# Paid Reddit Ads — Smoke Test

> **Stage:** Marketing -> Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

Prove that Reddit's community-based audiences respond to your offer. A passing Smoke test demonstrates that people in your target subreddits click your ad and convert on your landing page at a rate worth scaling. You need 2 leads or 1 booked meeting from $200-500 in ad spend.

## Leading Indicators

- Ad CTR above 0.4% within the first 3 days (signals creative resonates with the subreddit audience)
- Landing page views matching click count within 10% (signals tracking is working)
- At least 1 form engagement (partial fill or scroll past fold) within the first 50 clicks

## Instructions

### 1. Research and select target subreddits

Run the the reddit ads subreddit targeting workflow (see instructions below) drill. Identify 6-10 subreddits where your ICP is active. Group them into 2 clusters:

- **Cluster A (Core):** 3-4 subreddits with the highest ICP density scores
- **Cluster B (Adjacent):** 3-4 subreddits with related but broader audiences

Skip the third cluster at Smoke level. Focus budget on proving the core thesis.

### 2. Build the campaign

Run the `reddit-ads-campaign-build` drill with these Smoke-level parameters:

- **Budget:** $30-70/day for 7 days ($200-500 total)
- **Objective:** CONVERSIONS
- **Bid strategy:** CPC at $2.00-3.00
- **Ad groups:** 2 (one per subreddit cluster)
- **Ad variants:** 3 per ad group (data hook, question hook, story hook)
- **Landing page:** 1 dedicated page with Reddit Pixel + PostHog tracking

The drill handles subreddit targeting, creative creation, landing page build, and conversion tracking setup.

**Human action required:** Review the landing page and ad creative before launch. Approve the $200-500 test budget. Activate the campaign.

### 3. Let it run — do not optimize mid-flight

This is a signal test, not an optimization exercise. Let the campaign run for the full 7 days without changing bids, targeting, or creative. The only exceptions:

- If an ad is rejected by Reddit, fix the compliance issue and resubmit
- If spend is zero after 48 hours, check that campaigns/ad groups/ads are all set to ACTIVE
- If comments on promoted posts need responses, reply authentically within 4 hours

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure results against the pass criteria: >= 2 leads or >= 1 meeting in 7 days.

Pull the final numbers from PostHog (leads) and your CRM (meetings). Cross-reference against Reddit Ads Manager reported conversions. Document:

- Total spend
- Impressions, clicks, CTR by ad group
- Landing page views, conversion rate
- Leads and meetings by subreddit cluster
- Cost per lead
- Which ad variant (data/question/story hook) performed best
- Qualitative: Were the leads ICP matches? Did they have the problem you solve?

**PASS (>= 2 leads or >= 1 meeting):** Reddit works for your audience. Move to Baseline.
**FAIL:** Diagnose the failure point:
- Low CTR (<0.3%): Creative does not resonate. Test different hooks or subreddits.
- Good CTR but low conversion: Landing page mismatch. Align page with ad promise.
- Good conversion but wrong audience: Subreddit targeting needs refinement.

## Time Estimate

- Subreddit research: 1 hour
- Campaign build (landing page + creative + tracking): 2 hours
- Launch review and approval: 30 minutes
- Monitoring (comment responses, spend checks): 30 minutes total over 7 days
- Analysis and threshold evaluation: 30 minutes

**Total active time: ~4.5 hours. Calendar time: 7 days.**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit Ads | Ad platform | $200-500 test budget. Minimum $5/day. CPC: $0.50-4.00. https://ads.reddit.com |
| PostHog | Analytics & conversion tracking | Free up to 1M events/mo. https://posthog.com/pricing |
| Webflow | Landing page | Free plan available, paid from $14/mo. https://webflow.com/pricing |
| Attio | CRM for lead tracking | Free up to 3 users. https://attio.com/pricing |

**Estimated total cost: $200-500 (ad spend only). No tool costs at Smoke level with free tiers.**

## Drills Referenced

- `reddit-ads-campaign-build` — builds the full campaign (subreddit targeting, creative, landing page, tracking)
- the reddit ads subreddit targeting workflow (see instructions below) — discovers and scores subreddits for ad targeting
- `threshold-engine` — evaluates pass/fail against the 2-lead / 1-meeting threshold
