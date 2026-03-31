---
name: bundle-deal-structuring
description: Design, price, and launch a co-branded product bundle with a complementary partner
category: Partnerships
tools:
  - Anthropic
  - Attio
  - Webflow
  - Stripe
  - PostHog
fundamentals:
  - bundle-pricing-model
  - bundle-landing-page-setup
  - attio-deals
  - attio-contacts
  - posthog-custom-events
---

# Bundle Deal Structuring

This drill takes a qualified partner relationship and produces a live, trackable bundle offer: pricing model agreed by both sides, co-branded landing page with attribution, and checkout flow connected to your CRM. The output is a bundle that either partner can promote to their audience.

## Input

- A qualified partner from the `partner-prospect-research` drill (status: "Active" or "In Conversation")
- Both products' pricing pages and plan structures
- Agreement in principle to explore a bundle (the partner is interested)
- Your PostHog project with tracking configured

## Steps

### 1. Research the partner's pricing and audience overlap

Before designing the bundle, gather data:

- Pull the partner's pricing page and extract plan names, prices, and feature sets. If pricing is not public, request it directly from the partner contact.
- Identify which of YOUR plans and which of THEIR plans are most commonly used by the shared ICP. The bundle should pair the plans that overlap most.
- Check Crossbeam (if configured) for account overlap: how many of your prospects are already their customers, and vice versa? High overlap = high bundle potential.
- Review the partner record in Attio for any notes from previous conversations about pricing flexibility or past bundle attempts.

### 2. Generate the bundle pricing model

Run the `bundle-pricing-model` fundamental with:
- Your product plans and prices
- Partner product plans and prices
- Combined value proposition for the shared audience
- Target discount: 15-25% off combined list price for the first bundle (conservative; you can increase later if conversion justifies it)

Review the output: 3 bundle tiers, revenue split, and billing recommendation. Adjust if needed:
- If the partner is larger (higher ARPU, bigger brand), offer them 55-60% of bundle revenue to incentivize promotion
- If you are the anchor product, keep 55-60% and position the partner as the "add-on" value
- For the first bundle, default to dual invoicing (each bills their own portion) to avoid payment routing complexity

### 3. Propose the bundle to the partner

**Human action required:** Present the pricing model to the partner contact. Share:
- The 3 tier structures with pricing
- Revenue split proposal with rationale
- Draft co-branded landing page wireframe (hero, pricing table, feature grid, CTA)
- Proposed launch timeline (aim for 2-3 weeks from agreement)
- Success metrics: target deal count, revenue per deal, and evaluation period

Log the proposal in Attio as a note on the partner record. Update status to "Bundle Proposed."

### 4. Build the co-branded landing page

Once the partner approves the pricing (or after negotiation):

Run the `bundle-landing-page-setup` fundamental to create:
- A co-branded page at `{your_domain}/bundles/{partner-slug}`
- PostHog tracking for `bundle_page_viewed`, `bundle_tier_selected`, `bundle_cta_clicked`, `bundle_deal_completed`
- UTM-tracked URLs for both partners to distribute
- Checkout or demo booking flow connected to Stripe or Cal.com

### 5. Configure CRM tracking

Using the `attio-deals` fundamental, create a "Bundles" pipeline in Attio (if it does not already exist) with stages:
- Bundle Proposed → Partner Approved → Page Live → Promoting → Deals Closing → Active Bundle

Using the `attio-contacts` fundamental, add custom fields to the partner record:
- `bundle_status`: Select (Proposed / Approved / Live / Paused / Retired)
- `bundle_url`: URL of the co-branded landing page
- `bundle_tier_mix`: Which tiers are included
- `bundle_revenue_split`: Your % / Partner %
- `bundle_deals_closed`: Count
- `bundle_revenue_total`: Currency
- `bundle_launch_date`: Date

Create a deal in the Bundles pipeline for this specific bundle.

### 6. Set up attribution tracking

Using the `posthog-custom-events` fundamental, configure events that tie bundle conversions back to the source:
- `bundle_page_viewed` with properties: `partner_slug`, `utm_source`, `referrer`
- `bundle_deal_completed` with properties: `partner_slug`, `tier_name`, `deal_value`, `attribution_source` (which partner's channel drove the visitor)

This data feeds the `threshold-engine` and later the `autonomous-optimization` drill.

### 7. Launch and distribute

Coordinate launch with the partner:
- Both partners share the bundle URL via their channels (email, in-app, social, sales team)
- Each partner uses their UTM-tagged URL so attribution is clean
- Set a review date: 4 weeks after launch to evaluate performance and decide on continuation

Update the Attio deal to "Promoting" stage.

## Output

- Agreed bundle pricing model with 3 tiers and revenue split
- Live co-branded landing page with PostHog tracking
- UTM-tracked distribution URLs for both partners
- Attio pipeline and deal tracking for bundles
- Attribution system connecting conversions to specific partners and channels

## Triggers

Run this drill once per partner at Smoke level (1 bundle). At Baseline, run for 3-5 partners. At Scalable, templatize the landing page and pricing model so new bundles launch in <1 week.
