---
name: search-keyword-campaign-build
description: Research high-intent keywords, build exact-match search campaigns on Google and Microsoft Ads, and write responsive search ads
category: Paid
tools:
  - Google Ads
  - Microsoft Advertising
  - PostHog
fundamentals:
  - google-ads-keyword-research
  - google-ads-search-campaigns
  - google-ads-campaign-setup
  - google-ads-conversion-tracking
  - microsoft-ads-campaign-setup
  - microsoft-ads-conversion-tracking
  - posthog-custom-events
---

# Search Keyword Campaign Build

This drill takes you from zero to a live search ad campaign on Google Ads and optionally Microsoft Advertising (Bing). It focuses exclusively on search campaigns targeting high-intent keywords -- people actively looking for your solution category.

## Prerequisites

- Google Ads account with billing configured
- Microsoft Advertising account (optional but recommended -- lower CPCs for the same keywords)
- Landing page built and live (run `landing-page-pipeline` drill if needed)
- PostHog tracking installed on landing page
- Clear understanding of your ICP and what problem your product solves

## Input

- Product description and value proposition
- Target audience (job titles, company sizes, industries)
- Landing page URL
- Daily budget ($20-50/day recommended for initial test)
- Target CPA (what you can afford to pay per lead or meeting)

## Steps

### 1. Research high-intent keywords

Run the `google-ads-keyword-research` fundamental. Focus exclusively on bottom-of-funnel, high-intent terms:

**Priority 1 -- Solution-seeking queries:**
- "[category] software" (e.g., "CRM software for startups")
- "best [category]" (e.g., "best cold email tool")
- "[category] pricing" (e.g., "sales automation pricing")
- "[your product name]" (branded defense)

**Priority 2 -- Competitor comparison queries:**
- "[competitor] alternative" (e.g., "HubSpot alternative")
- "[competitor] vs" (e.g., "Salesforce vs")
- "[competitor] pricing" (captures price-sensitive evaluators)

**Priority 3 -- Pain-point queries:**
- "how to [problem your product solves]" (e.g., "how to automate cold outreach")

Start with 10-20 exact-match keywords across 2-3 ad groups. Do NOT use broad match at this stage.

Build a negative keyword list from day one: "free", "jobs", "salary", "tutorial", "what is", "definition", "course", "certification", "internship", "open source" (unless your product is open source).

### 2. Set up conversion tracking

Run `google-ads-conversion-tracking` to create conversion actions for:
- Form submission (demo request, trial signup)
- Thank-you page view (backup conversion signal)
- Optionally: meeting booked (if you can fire a server-side event from Cal.com)

Assign conversion values based on your unit economics: if your ACV is $10K and close rate from demo is 20%, a demo request is worth $2,000.

If also running on Microsoft Ads, run `microsoft-ads-conversion-tracking` to install the UET tag and create matching conversion goals.

### 3. Build the Google Ads campaign

Run `google-ads-campaign-setup` to create:

- **Campaign**: One Search campaign, daily budget $20-50, bidding set to "Maximize Conversions" (or "Maximize Clicks" if you have zero conversion history)
- **Ad groups**: 2-3 groups organized by keyword theme (e.g., "Product Category", "Competitor Alternatives", "Pain Points")
- **Keywords**: 5-8 exact-match keywords per ad group

Run `google-ads-search-campaigns` to create Responsive Search Ads:
- Write 10-15 headlines per ad group. Include: the keyword in at least 2 headlines, a specific benefit/metric, your brand name, and a clear CTA
- Write 4 descriptions: one benefit-focused, one social-proof-focused, one urgency/CTA-focused, one feature-focused
- Pin your strongest headline to position 1 and your CTA headline to position 2

Add sitelink extensions (pricing page, case studies, about page) and callout extensions ("Free Trial", "No Credit Card", "500+ Customers").

### 4. Mirror to Microsoft Advertising (recommended)

Run `microsoft-ads-campaign-setup`. The fastest path: use Microsoft's Google Import feature to copy your entire Google Ads campaign structure to Microsoft Advertising in one API call. Then:
- Reduce bids by 20-30% (Bing CPCs are lower)
- Review and adjust any keyword match types that imported incorrectly
- Ensure conversion tracking (UET tag) is installed and goals are configured

Microsoft Ads reaches ~10% of search volume that Google does not, at a lower CPC. This is free incremental reach.

### 5. Configure PostHog tracking

Using `posthog-custom-events`, set up events on your landing page:
- `search_ad_click` -- fired on page load when UTM source is google or bing (captures the click)
- `search_ad_form_view` -- fired when the form scrolls into view
- `search_ad_form_submit` -- fired on form submission
- `search_ad_conversion` -- fired on thank-you page load

Tag every event with properties: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term` (keyword), `utm_content` (ad variation).

### 6. Launch and monitor

Set campaign status to ENABLED. For the first 3-5 days:
- Do NOT make changes. Let the platform gather data.
- Monitor daily: are ads showing? Are clicks landing on the right page? Are conversion tracking pixels firing?
- Check the search terms report after 3 days for obvious junk queries to add as negatives

After 7 days, make first optimizations:
- Pause keywords with 50+ clicks and zero conversions
- Add negative keywords from the search terms report
- Increase bids on keywords with conversions below target CPA

## Output

- Live Google Ads search campaign with 2-3 ad groups, 10-20 exact-match keywords, and RSAs
- Optional: mirrored Microsoft Ads campaign
- PostHog tracking configured for full-funnel measurement
- Negative keyword list seeded and maintained
- Conversion tracking verified end-to-end

## Triggers

Run this drill once to launch the initial campaign. After launch, switch to `search-ads-performance-monitor` for ongoing optimization, or `google-ads-search-query-mining` for weekly keyword refinement.
