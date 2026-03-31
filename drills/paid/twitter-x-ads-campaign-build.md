---
name: twitter-x-ads-campaign-build
description: Build a complete Twitter/X promoted tweet campaign from audience definition through launch and initial creative testing
category: Paid
tools:
  - Twitter/X Ads
  - PostHog
  - Webflow
fundamentals:
  - twitter-x-ads-campaign-setup
  - twitter-x-ads-audience-targeting
  - twitter-x-ads-creative
  - posthog-custom-events
  - webflow-landing-pages
---

# Twitter/X Ads Campaign Build

End-to-end workflow to launch a promoted tweet campaign on X targeting solution-aware prospects. Covers campaign structure, audience configuration, creative production, conversion tracking, and initial A/B testing.

## Input

- ICP definition (persona, pain points, solution awareness level)
- Landing page URL (or Webflow page to build one)
- Budget allocation (daily and total for the test period)
- 3-5 competitor/thought-leader X handles for follower-lookalike targeting
- 3-5 problem-keyword themes your ICP discusses on X

## Steps

### 1. Set up conversion tracking

Using `posthog-custom-events`, configure landing page events:
- `twitter_ad_click` — fired on page load when URL contains `utm_source=twitter&utm_medium=paid`
- `twitter_ad_form_view` — fired when form scrolls into viewport
- `twitter_ad_form_submit` — fired on form submission
- `twitter_ad_lead_qualified` — fired when lead scores above ICP threshold in Attio

Also install the X website tag on the landing page using `twitter-x-ads-campaign-setup` (Step 6) so X can optimize delivery toward conversions.

### 2. Build the landing page (if needed)

Using `webflow-landing-pages`, create a dedicated page for this campaign:
- Headline mirrors the ad promise (match message to ad copy)
- Single CTA: form submit or demo booking
- No navigation links — landing pages have no exits
- Add UTM parameter capture to store source data with each lead
- Track scroll depth and form interactions in PostHog

### 3. Create the campaign and ad groups

Using `twitter-x-ads-campaign-setup`:
1. Create campaign in PAUSED state with daily budget ($25-50/day for smoke test, $100-200/day for baseline)
2. Create 2-3 line items (ad groups) with different audience strategies:
   - **Ad group A**: Keyword targeting — 25-50 problem/solution keywords
   - **Ad group B**: Follower lookalike targeting — 10-20 competitor/thought-leader handles
   - **Ad group C** (optional): Interest + conversation topic targeting
3. Set objective to WEBSITE_CLICKS for lead generation
4. Apply geo and language targeting to match your ICP's location

### 4. Configure audience targeting per ad group

Using `twitter-x-ads-audience-targeting`:
- For each ad group, add the appropriate targeting criteria
- Upload exclusion audiences: existing customers from Attio, recent converters
- Check audience size estimates — target 50,000-500,000 per ad group
- If audience is too small, broaden criteria. If too large, add additional filters.

### 5. Create creative variants

Using `twitter-x-ads-creative`, produce 3-5 promoted tweet variants per ad group:
- Variant A: Data hook + link to guide/checklist
- Variant B: Question hook + link to landing page
- Variant C: Contrarian take + link to breakdown
- Variant D: Social proof + link to case study
- Variant E: Thread-style tweet with line breaks

All tweets include UTM parameters: `?utm_source=twitter&utm_medium=paid&utm_campaign={campaign-slug}&utm_content={variant-id}`

For each variant, also create a Website Card version with an image (800x418px) for split testing card vs. text-only formats.

### 6. Launch and monitor

1. Set all line items and the campaign to ACTIVE
2. Let the campaign run for 48 hours without changes (allow X's algorithm to learn)
3. After 48 hours, check: Are impressions delivering? Is CTR above 0.3%? Are any ad groups severely underperforming?
4. After 500 impressions per variant: pause variants with CTR below 0.3%
5. After 2,000 impressions per variant: identify top 2 performers

### 7. Sync data to PostHog

Using `twitter-x-ads-reporting`, build a daily sync via n8n:
- Pull campaign, line item, and promoted tweet stats daily
- Send as PostHog custom events for unified dashboard reporting
- Compare X Ads metrics with on-site conversion data to calculate true CPA and ROAS

## Output

- Live X Ads campaign with 2-3 audience-segmented ad groups
- 10-15 promoted tweet variants under test
- Conversion tracking connected end-to-end: X click to PostHog event to Attio lead
- Daily data sync pipeline to PostHog
- Initial performance data after 1 week

## Triggers

- Run once at campaign launch
- Re-run the creative production steps (Step 5) every 2 weeks to refresh creative and prevent fatigue
