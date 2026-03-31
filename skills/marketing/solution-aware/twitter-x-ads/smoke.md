---
name: twitter-x-ads-smoke
description: >
  Twitter/X Ads — Smoke Test. Launch a $200 promoted tweet campaign on X targeting
  solution-aware prospects via keyword and follower-lookalike audiences.
  Validate that X drives qualified traffic to your landing page before scaling.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=15,000 impressions and >=5 qualified leads from $200 Twitter test"
kpis: ["Impressions", "Click-through rate (CTR)", "Cost per click (CPC)", "Landing page conversion rate", "Qualified leads"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - threshold-engine
---

# Twitter/X Ads — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Outcomes

Run a single $200 promoted tweet campaign on X for 1 week. Prove that X can deliver solution-aware prospects who click through to your landing page and convert. Pass threshold: >=15,000 impressions AND >=5 qualified leads.

## Leading Indicators

- Impressions delivering within 24 hours of launch (confirms audience is large enough)
- CTR above 0.3% by day 3 (confirms creative resonates)
- Landing page visits with >30 second session duration (confirms traffic quality)
- At least 1 form submission by day 4 (confirms conversion path works)

## Instructions

### 1. Define hypothesis and ICP targeting

Before touching X Ads, document:
- **Hypothesis**: "Solution-aware [persona] on X will click promoted tweets about [pain point] and convert on a [offer type] landing page."
- **Target keywords**: 15-25 terms your ICP tweets about or searches for (problem keywords + solution-category keywords)
- **Follower-lookalike handles**: 5-10 competitor and thought-leader handles whose followers match your ICP
- **Geography**: Restrict to your target markets

### 2. Build the campaign

Run the the twitter x ads campaign build workflow (see instructions below) drill with these smoke-test-specific settings:
- **Budget**: $200 total, $30/day for 7 days
- **Ad groups**: Create 2 (keyword targeting + follower-lookalike targeting)
- **Creative**: 3 promoted tweet variants per ad group (data hook, question hook, social proof hook)
- **Objective**: WEBSITE_CLICKS
- **Landing page**: Use an existing page or build a minimal one. Must have PostHog tracking and a conversion form.

The drill handles: campaign creation, audience configuration, creative production, conversion tracking setup, and landing page pipeline.

**Human action required:** Fund the X Ads account with at least $200. Review ad copy before launch. Approve campaign activation.

### 3. Monitor the test (do NOT optimize mid-flight)

Let the campaign run for 7 days without changes. This is a signal test, not an optimization exercise. Log daily in a spreadsheet or Attio:
- Impressions, clicks, CTR, spend
- Landing page visits (from PostHog)
- Form submissions
- Lead quality (are they ICP matches?)

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- **Impressions >= 15,000**: Did X deliver enough reach at this budget?
- **Qualified leads >= 5**: Did the traffic convert into ICP-matching leads?

Decision tree:
- **PASS (both met)**: X works for your ICP. Proceed to Baseline to scale and optimize.
- **PARTIAL (impressions met, leads missed)**: Traffic arrived but did not convert. Diagnose: Is it the landing page (low conversion rate) or the audience (wrong people clicking)?
- **FAIL (impressions missed)**: Audience too small or bids too low. Broaden targeting or increase bids, then re-run.

## Time Estimate

- 1 hour: Hypothesis, ICP targeting research, keyword/handle selection
- 2 hours: Campaign build (ad groups, creative, tracking, landing page)
- 30 minutes: Launch and verify delivery
- 30 minutes/day for 7 days: Monitor (3.5 hours total)
- 1 hour: Final evaluation and documentation

**Total: ~6 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| X Ads | Promoted tweets and accounts | $200 test budget (ad spend) |
| PostHog | Landing page tracking and conversion measurement | Free tier (1M events/mo) |
| Webflow | Landing page (if needed) | Free tier or ~$15/mo Starter |

## Drills Referenced

- the twitter x ads campaign build workflow (see instructions below) — Sets up the full campaign: audience targeting, creative variants, conversion tracking, and landing page pipeline
- `threshold-engine` — Evaluates final results against the >=15,000 impressions and >=5 qualified leads pass threshold
