---
name: paid-search-ads-baseline
description: >
  Paid Search Ads — Baseline Run. Run search ads continuously for 2 weeks with expanded
  budget, A/B keyword coverage across Google and Microsoft Ads, search query mining,
  and retargeting to achieve a sustainable cost per meeting.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "<=800 cost per meeting over 2 weeks with >=4 meetings booked"
kpis: ["Cost per meeting", "Cost per lead", "Landing page conversion rate", "Search impression share", "Click-through rate"]
slug: "paid-search-ads"
install: "npx gtm-skills add marketing/solution-aware/paid-search-ads"
drills:
  - budget-allocation
  - posthog-gtm-events
  - retargeting-setup
  - search-keyword-campaign-build
---

# Paid Search Ads — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Prove that paid search can produce meetings at a repeatable cost per meeting. At Baseline you scale budget to $1,000-3,000, expand keyword coverage, add Microsoft Ads as a second channel, mine search queries to cut wasted spend, and set up retargeting to recapture non-converters. The campaign runs always-on for 2 weeks with weekly optimization cycles.

**Pass threshold:** <=800 cost per meeting over 2 weeks with >=4 meetings booked.

## Leading Indicators

- Search impression share >60% on your top exact-match keywords (confirms adequate budget)
- CTR sustained >2% across both platforms (confirms ad relevance holds at higher volume)
- Landing page conversion rate stable or improving vs Smoke (confirms page is not the bottleneck)
- Cost per click trending flat or down (confirms quality scores are improving)
- At least 2 meetings by end of week 1 (signals you are on pace for the threshold)

## Instructions

### 1. Expand keyword coverage and add Microsoft Ads

Using the Smoke campaign data, extend your search campaign:

Run `search-keyword-campaign-build` to:
- Add 10-15 additional exact-match keywords discovered during Smoke (from search query reports and Keyword Planner exploration)
- Add phrase-match variants of your top 5 converting keywords to capture long-tail queries
- Mirror the full Google campaign to Microsoft Advertising using the Google Import feature. Reduce Microsoft bids by 20-30% (lower CPCs on Bing)
- Expand negative keyword lists based on Smoke search term data

### 2. Set up end-to-end tracking

Run the `posthog-gtm-events` drill to create a standardized event pipeline:

- `paid_search_ad_click` — fired on landing page load when UTM source is google or bing
- `paid_search_form_view` — fired when form scrolls into view
- `paid_search_form_submit` — fired on form submission
- `paid_search_lead_qualified` — fired when lead is marked qualified in Attio
- `paid_search_meeting_booked` — fired when Cal.com booking is completed (connect Cal.com webhook to PostHog via n8n)
- `paid_search_meeting_held` — fired when meeting is marked as attended in Attio

Tag every event with: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `platform` (google or bing), `ad_group`, `keyword_match_type`.

This creates a full-funnel view from ad click to meeting held.

### 3. Optimize budget allocation

Run the `budget-allocation` drill to distribute your $1,000-3,000 monthly budget:

- Pull CPA data from Smoke: which keywords, ad groups, and the Google vs Microsoft split produce the cheapest leads
- Apply the 70/20/10 framework: 70% to proven converting keywords, 20% to promising keywords that need more data, 10% to new keyword experiments
- Set up n8n alerts: if any ad group's CPA exceeds 2x your target for 3 consecutive days, reduce its budget by 30%
- Switch bidding from "Maximize Clicks" to "Maximize Conversions" once you have 15+ conversions (Google needs at least 15 to optimize effectively)

### 4. Set up retargeting for non-converters

Run the `retargeting-setup` drill. Most search traffic will not convert on the first visit. Retargeting recaptures them:

- Create a retargeting audience in Google Ads: visitors who clicked a search ad but did not submit the form (using the PostHog `paid_search_ad_click` event minus `paid_search_form_submit`)
- Build a Google Display retargeting campaign with a small daily budget ($5-10/day)
- Create 2-3 retargeting ad variants: one with social proof ("Join 500+ teams"), one with an alternative CTA ("Download our guide" instead of "Book a demo"), one with urgency ("Limited beta spots")
- Set frequency cap to 3 impressions per person per week to avoid annoyance

### 5. Run weekly search query mining

At the end of each week, manually run the search query mining process from the `search-keyword-campaign-build` drill:

1. Pull the search terms report from Google Ads and Microsoft Ads
2. Add any irrelevant or wasteful queries as negative keywords
3. Promote any converting queries that are not yet exact-match keywords
4. Estimate wasted spend recovered from new negative keywords

This is manual at Baseline. It becomes automated at Scalable.

### 6. Optimize landing page based on data

After week 1, review PostHog data:
- If bounce rate >60%: the headline or hero section does not match search intent. A/B test a new headline that mirrors your top-performing keyword.
- If form view rate is high but submission rate is low: reduce form fields. Try name + email only.
- If conversion rate differs significantly between Google and Bing traffic: create separate landing pages with tailored messaging for each source.

### 7. Evaluate against threshold

At the end of 2 weeks, run the `threshold-engine` drill. Calculate:
- Total spend across Google + Microsoft + retargeting
- Total meetings booked (from Cal.com / Attio)
- Cost per meeting = total spend / meetings booked
- Cost per lead = total spend / form submissions
- Blended CTR and conversion rate across platforms

**Pass:** <=800 cost per meeting AND >=4 meetings. Proceed to Scalable.
**Marginal pass (cost per meeting $800-1,000):** Stay at Baseline. Test new landing page variants, tighter keyword targeting, or different ad copy angles. Re-run for 2 more weeks.
**Fail -- high CPA, low volume:** Search volume may be insufficient for your category. Consider broadening to phrase match, testing competitor keywords more aggressively, or supplementing with Microsoft Ads Shopping campaigns (if applicable).

## Time Estimate

- 2 hours: Expand keywords, set up Microsoft Ads, extend negative keyword lists
- 2 hours: Configure PostHog event pipeline and tracking
- 2 hours: Budget allocation analysis and bid strategy optimization
- 2 hours: Retargeting setup (audiences, ads, frequency caps)
- 2 hours: Weekly search query mining (1 hour per week x 2)
- 1 hour: Landing page optimization based on data
- 1 hour: Final threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Search campaigns + retargeting | Pay per click; $1,000-3,000/mo budget — [ads.google.com](https://ads.google.com) |
| Microsoft Advertising | Bing search campaigns | Pay per click; included in above budget — [ads.microsoft.com](https://ads.microsoft.com) |
| Webflow | Landing page hosting and A/B variants | CMS $23/mo — [webflow.com/pricing](https://webflow.com/pricing) |
| PostHog | Full-funnel tracking and analytics | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Webhook routing (Cal.com to PostHog), budget alerts | Starter EUR24/mo or self-hosted free — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking | Free tier — [cal.com](https://cal.com) |
| Attio | Lead and meeting tracking | Free tier or Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost:** $1,000-3,000/mo ad spend + ~$50-75/mo tooling

## Drills Referenced

- `budget-allocation` — Analyze Smoke data and distribute budget across keywords, ad groups, and platforms
- `posthog-gtm-events` — Set up standardized event taxonomy for full-funnel search ad tracking
- `retargeting-setup` — Build retargeting audiences and campaigns to recapture non-converters
- `search-keyword-campaign-build` — Expand keyword coverage and mirror campaigns to Microsoft Ads
