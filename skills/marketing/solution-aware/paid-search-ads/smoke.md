---
name: paid-search-ads-smoke
description: >
  Paid Search Ads — Smoke Test. Launch a small exact-match Google Ads search campaign
  targeting 10-20 high-intent keywords to test whether paid search produces leads or
  meetings for your product category.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: ">=2 leads or >=1 meeting from search ads within 1 week on $200-500 ad spend"
kpis: ["Click-through rate (target >2%)", "Landing page conversion rate (target >3%)", "Cost per click", "Leads generated"]
slug: "paid-search-ads"
install: "npx gtm-skills add marketing/solution-aware/paid-search-ads"
drills:
  - search-keyword-campaign-build
  - landing-page-pipeline
  - threshold-engine
---

# Paid Search Ads — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Prove that people actively search for your solution category and that a search ad can capture that intent and convert it into a lead or meeting. At this level, everything is a one-shot test. You build a single campaign on Google Ads with exact-match keywords, point it at a landing page, spend $200-500, and measure whether search intent converts.

**Pass threshold:** >=2 leads or >=1 meeting from search ads within 1 week on $200-500 ad spend.

## Leading Indicators

- Ad impressions >500 in the first 3 days (confirms search volume exists for your keywords)
- CTR >2% (confirms your ad copy resonates with searchers)
- Landing page visits >20 (confirms clicks are reaching your page)
- At least 1 form submission by day 5 (confirms the funnel works end-to-end)

## Instructions

### 1. Build a landing page for search traffic

Run the `landing-page-pipeline` drill to create a dedicated landing page. Search traffic has specific expectations:

- The headline must match the search intent. If someone searched "best CRM for startups", the landing page headline should say "CRM Built for Startups" -- not your generic homepage tagline.
- Include a clear, single CTA above the fold: "Book a Demo", "Start Free Trial", or "Get Pricing".
- Add social proof immediately visible: customer logos, a testimonial, or a specific metric ("Used by 400+ startups").
- Install PostHog tracking on the page. Configure events for page view, form view, and form submission.

**Human action required:** Review the landing page before launching ads. Verify the form submits correctly and PostHog events fire (use PostHog's toolbar to confirm).

### 2. Build and launch the search campaign

Run the `search-keyword-campaign-build` drill to:

1. Research 10-20 high-intent keywords using Google Ads Keyword Planner. Focus on exact-match terms where someone is actively looking for a solution: "[category] software", "best [category]", "[competitor] alternative".
2. Build a Google Ads Search campaign with 2-3 ad groups organized by keyword theme.
3. Write Responsive Search Ads with 10+ headlines and 4 descriptions. Lead with outcomes and specifics, not features.
4. Set up conversion tracking for form submissions.
5. Add a negative keyword list to block irrelevant traffic ("free", "jobs", "tutorial", "what is", etc.).
6. Set daily budget to $30-70/day (to spend $200-500 over the week).
7. Set bidding to "Maximize Clicks" (you need data before you can optimize for conversions).

Tag all ad URLs with UTM parameters: `utm_source=google&utm_medium=cpc&utm_campaign=smoke-search&utm_term={keyword}`.

**Human action required:** Set the budget and launch the campaign. Verify ads are approved and showing within 24 hours.

### 3. Monitor without optimizing (days 1-5)

Do NOT touch the campaign for the first 5 days. Let data accumulate. Check daily only for:
- Are ads showing? (Check impression count)
- Are clicks reaching the landing page? (Check PostHog page views vs Google clicks -- they should roughly match)
- Is conversion tracking firing? (Verify in Google Ads conversion column)

If ads are disapproved, fix the policy violation and resubmit. If zero impressions after 48 hours, your keywords may have no search volume -- add broader phrase-match variants.

### 4. Evaluate against threshold

At the end of 7 days, run the `threshold-engine` drill. Pull from PostHog and Google Ads:
- Total ad spend
- Total clicks
- CTR
- Landing page conversion rate (form submissions / page views)
- Total leads (form submissions)
- Meetings booked (if applicable)
- Cost per lead

**Pass:** >=2 leads or >=1 meeting. Proceed to Baseline.
**Fail -- low impressions (<500):** Your keywords lack search volume. Research broader terms or test a different angle (competitor keywords, pain-point keywords).
**Fail -- low CTR (<1%):** Your ad copy does not match search intent. Rewrite headlines to better match the keywords.
**Fail -- clicks but no conversions:** The landing page is the bottleneck. Test a simpler page with fewer form fields, a stronger headline, or a lower-commitment CTA (e.g., "Download Guide" instead of "Book Demo").

## Time Estimate

- 1 hour: Build landing page (or adapt existing page)
- 1.5 hours: Keyword research, campaign build, ad writing, conversion tracking setup
- 0.5 hours: Daily monitoring checks (5 min/day for 7 days)
- 1 hour: Pull results, analyze, evaluate threshold, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Search ad campaign | Pay per click; $200-500 test budget — [ads.google.com](https://ads.google.com) |
| Webflow | Landing page | Basic $14/mo or CMS $23/mo — [webflow.com/pricing](https://webflow.com/pricing) |
| PostHog | Conversion tracking and analytics | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Meeting booking (if CTA is "Book Demo") | Free tier — [cal.com](https://cal.com) |

**Estimated play-specific cost:** $200-500 ad spend + $0-23/mo Webflow (free if you have an existing page)

## Drills Referenced

- `search-keyword-campaign-build` — Research keywords, build campaign structure, write ads, set up conversion tracking
- `landing-page-pipeline` — Build a dedicated landing page with PostHog tracking
- `threshold-engine` — Evaluate pass/fail against the 2-lead or 1-meeting threshold
