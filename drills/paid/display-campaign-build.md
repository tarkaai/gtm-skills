---
name: display-campaign-build
description: Build and launch display advertising campaigns on Google Display Network and Meta Audience Network with placement targeting, creative, and conversion tracking
category: Paid
tools:
  - Google Ads
  - Meta Ads
  - PostHog
  - Attio
  - Clay
  - Loops
fundamentals:
  - google-ads-display-campaign
  - google-ads-conversion-tracking
  - meta-ads-campaign-setup
  - meta-ads-audiences
  - meta-ads-pixel-capi
  - posthog-custom-events
  - posthog-funnels
  - attio-contacts
  - attio-deals
  - clay-enrichment-waterfall
  - clay-scoring
  - loops-sequences
---

# Display Campaign Build

This drill constructs display advertising campaigns from scratch: platform selection, placement targeting, creative setup, conversion tracking, lead routing, and CRM integration. It is designed for problem-aware audiences who encounter banner ads on industry publications and relevant websites.

## Prerequisites

- Google Ads account with Display campaign access and billing configured
- Meta Business Manager with Audience Network enabled
- PostHog installed on all landing pages
- Landing pages built (run `landing-page-pipeline` drill if needed)
- ICP defined with documented pain points
- Attio CRM configured
- Clay account for lead enrichment

## Input

- ICP document with firmographic and psychographic criteria
- 3 primary pain points for the problem-aware audience
- Banner creative assets (landscape 1200x628, square 1200x1200, logo)
- Landing page URLs with UTM parameters configured
- Monthly budget allocation ($1,000-3,000 for Baseline)

## Steps

### 1. Select platforms and allocate budget

For display advertising targeting problem-aware prospects on industry sites:

- **Google Display Network (primary):** 60% of budget. Reaches 90%+ of internet users via 2M+ publisher sites. Use managed placements for industry sites and custom intent audiences for broader reach.
- **Meta Audience Network (secondary):** 40% of budget. Extends Meta ads beyond Facebook/Instagram to partner apps and websites. Strong retargeting via Pixel data.

Split rationale: GDN offers direct placement targeting on industry publications. Meta Audience Network offers better retargeting and lookalike capabilities.

### 2. Build the Google Display campaign

Using the `google-ads-display-campaign` fundamental:

1. **Create 2 campaign groups:**
   - Campaign A: "Display - Managed Placements - [Industry]" — ads on specific industry sites
   - Campaign B: "Display - Custom Intent - [ICP Pain Point]" — ads shown to users searching for related topics

2. **Configure Campaign A (managed placements):**
   - Research 15-25 industry publications and blogs where ICP reads
   - Add each as a managed placement via the API
   - Set daily budget to 60% of GDN allocation / 30
   - Bidding: Maximize Conversions for first 2 weeks, switch to Target CPA after 15+ conversions

3. **Configure Campaign B (custom intent):**
   - Build custom intent audiences from:
     - 10-15 keywords the ICP searches when experiencing the pain point
     - 5-10 competitor URLs
     - 3-5 industry resource URLs
   - Set daily budget to 40% of GDN allocation / 30
   - Bidding: Maximize Conversions

4. **Create 3 ad groups per campaign** (one per pain point):
   - Each ad group targets a different ICP pain point
   - Each gets 3-5 responsive display ad variants

5. **Upload responsive display ads:**
   - 3 headlines per pain point (stat hook, question hook, proof hook)
   - 2 descriptions per pain point
   - Landscape and square images per pain point
   - Long headline summarizing the value offer

6. **Configure exclusions:**
   - Exclude mobile app placements (accidental clicks)
   - Exclude below-the-fold placements
   - Exclude parked domains and error pages
   - Set frequency cap: 5 impressions per user per week

### 3. Build the Meta Audience Network campaign

Using the `meta-ads-campaign-setup` and `meta-ads-audiences` fundamentals:

1. **Create the campaign:**
   - Objective: Lead Generation or Traffic (depending on whether you use Instant Forms or landing pages)
   - Placements: select Audience Network manually (do NOT use Automatic Placements, which will spread budget across Facebook/Instagram)

2. **Build audiences:**
   - Custom Audience: website visitors from last 30 days who did not convert (from Meta Pixel)
   - Lookalike Audience: 1% lookalike from best customers (export from Attio, hash emails, upload)
   - Interest-based Audience: interests matching the problem space (not solution category)

3. **Create ad sets** (one per audience):
   - Daily budget: split Meta allocation across audiences (50% retargeting, 30% lookalike, 20% interest)

4. **Build display ad creative:**
   - Single image format for Audience Network
   - Problem-agitation headlines matching GDN ads for cross-platform consistency
   - Include a clear CTA button

### 4. Install conversion tracking

Using `google-ads-conversion-tracking` and `meta-ads-pixel-capi`:

1. **Google Ads:** Create conversion actions for page_view, form_submit, demo_booked. Import PostHog events as Google Ads conversions via the offline conversion import API.
2. **Meta:** Verify Pixel fires on all landing pages. Configure Conversions API (CAPI) for server-side event deduplication.
3. **PostHog:** Using `posthog-custom-events`, track:
   - `display_impression` (via platform API sync)
   - `display_click` (landing page UTM parameter capture)
   - `display_conversion` (form submission with source attribution)
   - Properties on each event: `platform`, `campaign_id`, `ad_group`, `placement`, `pain_point`
4. **UTM structure:** `utm_source=google|meta&utm_medium=display&utm_campaign=display-baseline-{pain-point}&utm_content={creative-variant}`
5. Build the PostHog funnel: `display_click > page_view > scroll_50 > form_focus > form_submit > demo_booked`

### 5. Deploy lead routing

Using `attio-contacts`, `attio-deals`, `clay-enrichment-waterfall`, `clay-scoring`, and `loops-sequences`:

Build an n8n workflow triggered by PostHog `display_conversion` webhook:

1. Extract lead data from form submission
2. Enrich via Clay: company data, LinkedIn profile, ICP scoring
3. Create or update contact in Attio with: `source: display-ads`, `campaign`, `platform`, `placement`, `lead_score`
4. If lead_score >= 70: create deal in Attio, add to Loops high-intent nurture, send Slack alert
5. If lead_score < 70: add to Loops educational nurture
6. Log all enrichment and routing decisions as PostHog events for attribution analysis

### 6. Launch sequence

1. Launch GDN Campaign A (managed placements) first — this is your controlled test
2. After 3 days and 1,000+ impressions: review placement report, exclude any irrelevant sites
3. Launch GDN Campaign B (custom intent) — broader reach test
4. Launch Meta Audience Network retargeting campaign
5. After 7 days: launch Meta lookalike and interest campaigns
6. Stagger launches to isolate performance signals per campaign type

## Output

- 2 GDN campaigns (managed placements + custom intent) with 3 ad groups each
- 1 Meta Audience Network campaign with 3 ad sets
- PostHog funnel tracking display click-through to conversion
- n8n lead routing workflow: display conversion > Clay enrichment > Attio CRM > Loops nurture
- UTM-tagged landing pages with full attribution

## Triggers

- Campaign monitoring: daily manual check during first 2 weeks
- Placement exclusion review: weekly
- Creative refresh: every 2-3 weeks
- Lead quality report: weekly via n8n
