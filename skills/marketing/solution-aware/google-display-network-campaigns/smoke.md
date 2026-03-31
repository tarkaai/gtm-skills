---
name: google-display-network-campaigns-smoke
description: >
  Google Display Network — Smoke Test. Launch a $300-500 GDN test campaign targeting
  in-market and custom intent audiences to prove that display ads on industry sites
  can produce qualified leads for your product category.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=20,000 impressions with CTR >=0.35% and >=3 form submissions from $300-500 GDN spend"
kpis: ["Impressions (target >=20,000)", "CTR (target >=0.35%)", "Landing page conversion rate (target >=3%)", "Form submissions (target >=3)", "Cost per click"]
slug: "google-display-network-campaigns"
install: "npx gtm-skills add marketing/solution-aware/google-display-network-campaigns"
drills:
  - display-campaign-build
  - landing-page-pipeline
  - threshold-engine
---

# Google Display Network — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Prove that solution-aware prospects in your category can be reached via display ads on the Google Display Network, and that this traffic converts into leads. At this level, you build one GDN campaign targeting in-market audiences and custom intent segments, point it at a single landing page, spend $300-500 over one week, and measure whether display impressions convert into form submissions. Display ads operate differently than search -- the prospect is not actively looking for your product, so your creative must interrupt their browsing with a relevant problem statement.

**Pass threshold:** >=20,000 impressions with CTR >=0.35% and >=3 form submissions from $300-500 GDN spend.

## Leading Indicators

- Impressions >5,000 in the first 48 hours (confirms your audiences have sufficient reach)
- CTR >0.30% by day 3 (confirms your creative is relevant to the audience -- GDN average is 0.35%)
- At least 10 landing page visits from display by day 4 (confirms clicks are real and reaching your page)
- At least 1 form submission by day 5 (confirms the display-to-landing-page funnel works end-to-end)
- Placement report shows ads on relevant industry sites, not gaming or utility apps (confirms targeting is working)

## Instructions

### 1. Build a landing page for display traffic

Run the `landing-page-pipeline` drill to create a dedicated landing page. Display traffic behaves differently from search traffic:

- The visitor was NOT looking for your product. Your headline must connect to the problem they were reading about, not your solution. If your display ad targets "business software" in-market audiences on a SaaS review site, the headline should say "Still spending 10 hours/week on manual data entry?" -- not "Try Our Platform."
- Include a clear, single CTA above the fold. For solution-aware prospects, use "See How It Works" or "Get a Free Assessment" rather than "Book a Demo" (display traffic is colder).
- Add social proof immediately visible: customer logos, a specific result metric ("Reduced onboarding time by 60%"), or a count ("Used by 500+ teams").
- Install PostHog tracking on the page. Configure events for: `page_view`, `scroll_50`, `form_view`, `form_submit`. Tag all events with `source: display-ads` and `campaign: smoke-gdn`.

**Human action required:** Review the landing page before launching ads. Verify the form submits correctly, PostHog events fire (use PostHog's toolbar), and the page loads in under 3 seconds (display visitors are impatient).

### 2. Build and launch the display campaign

Run the `display-campaign-build` drill with the following Smoke-level configuration:

1. **Create a single GDN campaign** with two ad groups:
   - Ad Group A: "In-Market - [Your Product Category]" -- target the in-market audience for your software category using `google-ads-display-audiences`. Query the in-market taxonomy for your vertical (e.g., "Business Software", "CRM Software", "Project Management Software").
   - Ad Group B: "Custom Intent - [ICP Keywords]" -- build a custom audience from 10-15 keywords your ICP searches when evaluating solutions, plus 3-5 competitor URLs and 2-3 review site URLs (G2, Capterra pages for your category).

2. **Create Responsive Display Ads** for each ad group:
   - Upload at least 3 landscape images (1200x628) and 3 square images (1200x1200). Use product screenshots, benefit-focused graphics, or bold text overlays on brand colors. Avoid stock photos.
   - Write 5 headlines (under 30 chars): mix stat hooks ("Cut Data Entry by 73%"), question hooks ("Still Using Spreadsheets?"), and proof hooks ("500+ Teams Switched").
   - Write 3 descriptions (under 90 chars): agitate the problem, state the outcome, include social proof.
   - Set long headline to your core value proposition.
   - CTA: LEARN_MORE (for solution-aware traffic, softer CTAs outperform aggressive ones on GDN).

3. **Configure targeting and exclusions:**
   - Geographic targeting: your primary market country
   - Content exclusions: exclude mobile app placements, parked domains, below-the-fold, sexually suggestive content
   - Frequency cap: 5 impressions per user per week
   - Set bidding to Maximize Conversions (you need initial conversion data)
   - Set daily budget to $40-70/day to spend $300-500 over the week

4. **Set UTM parameters on all ad URLs:**
   `?utm_source=google&utm_medium=display&utm_campaign=smoke-gdn&utm_content={ad-group-name}`

5. **Set up conversion tracking** via `google-ads-conversion-tracking`:
   - Create a conversion action for form submissions
   - Verify the conversion tag fires on the thank-you page or form submission event

**Human action required:** Set the budget, review ad creative for brand alignment, and launch the campaign. Verify ads are approved within 24 hours. Check the placement report after 48 hours -- if ads are appearing on irrelevant gaming or children's sites, add those placements as exclusions immediately.

### 3. Monitor without optimizing (days 1-5)

Do NOT optimize the campaign during the first 5 days. Let data accumulate. Check daily for:
- Are ads showing? (Check impression count in Google Ads)
- Are clicks reaching the landing page? (Compare PostHog page views with `source: display-ads` against Google Ads click count -- they should roughly match)
- Is conversion tracking firing? (Check Google Ads conversion column)
- What sites are your ads appearing on? (Pull the placement report -- flag obvious junk sites but do not exclude aggressively yet)

If ads are disapproved, review the policy violation and fix the creative. If zero impressions after 48 hours, your audience targeting is too narrow -- broaden to a parent in-market category or add more keywords to the custom intent audience.

### 4. Evaluate against threshold

At the end of 7 days, run the `threshold-engine` drill. Pull from PostHog and Google Ads:
- Total impressions
- Total clicks and CTR
- Landing page conversion rate (form submissions / page views)
- Total form submissions
- Cost per click and cost per form submission
- Placement report: top 20 sites by impressions

**Pass:** >=20,000 impressions with CTR >=0.35% and >=3 form submissions. Proceed to Baseline.

**Fail -- low impressions (<10,000):** Your audiences are too narrow. Broaden: add more in-market categories, expand custom intent keywords, or increase the geographic scope.

**Fail -- low CTR (<0.25%):** Your creative does not resonate. Display CTR is inherently lower than search, but below 0.25% means the ad is being ignored. Test different hooks: switch from benefit statements to provocative questions or specific data points. Check if your images are too generic (stock photos perform worst on GDN).

**Fail -- clicks but no conversions:** The landing page is the bottleneck. Display visitors need more persuasion than search visitors. Test: shorter forms (name + email only), a lead magnet instead of a demo CTA ("Download the 2026 [Category] Benchmark Report"), or a video instead of text.

**Fail -- high spend on junk placements:** If >30% of impressions went to irrelevant sites, your targeting allowed too much drift. Add aggressive placement exclusions and consider using managed placements instead of broad audience targeting for the next test.

## Time Estimate

- 1 hour: Build or adapt a landing page with PostHog tracking
- 1.5 hours: Research audiences, build custom intent segment, create campaign structure, write ad copy, upload creatives
- 1 hour: Set up conversion tracking, UTM parameters, and verify everything fires
- 0.5 hours: Daily monitoring checks (5-10 min/day for 7 days)
- 1 hour: Pull results, analyze placement report, evaluate threshold, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Display campaign | $300-500 test budget -- [ads.google.com](https://ads.google.com) |
| Webflow | Landing page | Basic $14/mo or CMS $23/mo -- [webflow.com/pricing](https://webflow.com/pricing) |
| PostHog | Conversion tracking and analytics | Free tier (1M events/mo) -- [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost:** $300-500 ad spend + $0-23/mo Webflow (free if you already have a page builder)

## Drills Referenced

- `display-campaign-build` -- Build GDN campaign with in-market and custom intent audience targeting, responsive display ads, conversion tracking, and placement exclusions
- `landing-page-pipeline` -- Build a dedicated landing page with PostHog tracking, optimized for display traffic (colder than search)
- `threshold-engine` -- Evaluate pass/fail against the 20K impressions / 0.35% CTR / 3 submissions threshold
