---
name: quora-ads-campaign-build
description: Build a complete Quora Ads campaign from question/topic research through ad creative, landing page, and conversion tracking
category: Paid
tools:
  - Quora Ads
  - PostHog
  - Webflow
fundamentals:
  - quora-ads-campaign-setup
  - quora-ads-question-targeting
  - quora-ads-creative
  - quora-ads-conversion-tracking
  - webflow-landing-pages
  - posthog-custom-events
---

# Quora Ads Campaign Build

This drill builds a complete Quora Ads campaign: from question and topic research to targeting configuration, ad creative, landing page, conversion tracking, and launch. Designed for B2B SaaS targeting problem-aware prospects who are actively asking questions about problems your product solves.

## Input

- ICP definition: who you are targeting (job title, industry, pain points)
- Landing page offer: what value you are driving to (checklist, guide, demo, free tool)
- Budget: daily budget in dollars (minimum $30/day recommended for meaningful data)
- Duration: campaign run time (minimum 7 days for Smoke, 14+ for Baseline)

## Steps

### 1. Research target questions and topics

Using the `quora-ads-question-targeting` fundamental, identify where your ICP is active on Quora:

**Topic research:**
1. List your ICP's top 5 pain points
2. Search Quora for each pain point and note which topics those questions are tagged with
3. Select 10-20 Tier 1 topics (directly related to the problem your product solves)
4. Note estimated reach per topic from Ads Manager

**Question research:**
1. Search Quora for high-traffic questions matching your ICP problems:
   - "What is the best way to [solve ICP problem]?"
   - "How do you [task your product automates]?"
   - "What tools do you use for [your category]?"
   - "Alternatives to [competitor name]?"
2. Filter to questions with 500+ monthly views
3. Select 50-100 questions, grouped by theme

Organize research into targeting clusters:

| Cluster | Type | Items | Theme |
|---------|------|-------|-------|
| Core Problem | Topics | 8-10 topics | Direct problem match |
| Specific Questions | Questions | 30-50 questions | High-intent question pages |
| Category Keywords | Keywords | 15-25 keywords | Broad problem discovery |

### 2. Build the landing page

Using the `webflow-landing-pages` fundamental, create a dedicated landing page for this campaign:

- Headline matches the ad creative promise (critical for Quora audiences who are skeptical of ads)
- Content delivers immediate value: the offer is visible above the fold
- Form fields: email only for content offers; email + company + role for demo requests
- No navigation links (landing page, not a website page)
- PostHog tracking installed (page view, scroll depth, form submit)
- Quora Pixel installed (see step 3)
- UTM parameter capture and qclid capture implemented

**Human action required:** Review and approve the landing page before launching ads.

### 3. Configure conversion tracking

Using the `quora-ads-conversion-tracking` fundamental:

1. Install the Quora Pixel base code on the landing page
2. Configure event pixels: `ViewContent` on page load, `Lead` on form submit
3. Install qclid capture script to store the Quora click ID in localStorage and cookie
4. Set up server-side CAPI via n8n: when PostHog receives a `quora_ads_lead_captured` event, forward it to Quora's Conversion API with the stored qclid
5. Verify tracking using Quora Pixel Helper browser extension and Ads Manager Event Testing

Using `posthog-custom-events`, fire parallel PostHog events:
- `quora_ads_page_view` on landing page load (with UTM properties and qclid)
- `quora_ads_lead_captured` on form submit (with UTM properties, qclid, and email for person identification)
- `quora_ads_lead_qualified` when Clay enrichment scores the lead 70+ (fired from the lead routing n8n workflow)

### 4. Create the campaign structure

Using the `quora-ads-campaign-setup` fundamental, prepare the campaign specification:

1. Campaign: objective `Conversions`, daily budget, start/end dates
2. Ad Set 1 — Topic Targeting: 8-10 core problem topics, CPC bid $1.50-2.00, geo: US/UK/CA
3. Ad Set 2 — Question Targeting: 30-50 high-intent questions, CPC bid $1.00-1.50, geo: US/UK/CA
4. Ad Set 3 (Baseline+) — Keyword Targeting: 15-25 problem keywords, CPC bid $1.50-2.00
5. All ad sets: disable Audience Expansion, target All Devices

Output the campaign spec as a structured JSON brief for human execution in Ads Manager.

**Human action required:** Create the campaign in Quora Ads Manager following the spec.

### 5. Create ad creative

Using the `quora-ads-creative` fundamental, generate 3-4 ad variants per ad set:

- **Variant A — Data hook**: Lead with a specific stat or research finding related to the ICP problem
- **Variant B — Question hook**: Mirror the user's problem-seeking mental state
- **Variant C — Outcome hook**: Focus on the specific result your product delivers
- **Variant D — Social proof hook**: Lead with customer count or case study result

Each ad includes:
- Headline (under 65 characters, problem-aware framing)
- Body (under 105 characters, value-first)
- CTA button (Learn More for content offers, Sign Up for trial/demo)
- Destination URL with UTM parameters: `utm_source=quora&utm_medium=paid&utm_campaign=quora-ads-targeting-{level}&utm_content={variant-id}`
- Image asset (1200x628px) or Text Ad format

Generate both Image Ad and Text Ad versions of each variant. Quora Text Ads often outperform Image Ads because they blend with the content experience.

### 6. Review and launch

Before activating:
- Verify all UTM parameters and qclid capture across all ad destination URLs
- Confirm Quora Pixel fires on landing page (use Pixel Helper)
- Confirm PostHog events fire alongside Quora events
- Review all ad copy for Quora editorial compliance (no ALL CAPS, no clickbait, landing page matches ad promise)
- Check all image assets meet specs (1200x628px, under 2MB)

**Human action required:** Approve campaign structure and budget. Activate campaign in Ads Manager. Note: Quora reviews all ads manually (24-48 hours before delivery starts).

### 7. Post-launch monitoring (first 48 hours)

- Check ad approval status in Ads Manager (expect 24-48 hours)
- Verify conversion events flowing to both Quora and PostHog
- Monitor CPC against bid — if CPC is >2x bid, targeting may be too narrow
- Verify spend is tracking to budget (no overspend from broad targeting, no underspend from narrow targeting)
- Check landing page conversion rate — if <2% after 100+ clicks, diagnose the page before spending more

## Output

- 1 campaign with 2-3 ad sets targeting different Quora contexts (topics, questions, keywords)
- 6-12 ad variants (3-4 per ad set) with Quora-native creative in both Image and Text formats
- 1 dedicated landing page with Quora Pixel + qclid capture + PostHog tracking
- Server-side CAPI configured via n8n for form submissions
- UTM-tagged URLs for full attribution chain
- Structured campaign brief document for human execution
