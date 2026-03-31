---
name: bundle-landing-page-setup
description: Create a co-branded landing page for a partner bundle deal with tracking and checkout flow
tool: Webflow
product: Webflow
difficulty: Config
---

# Bundle Landing Page Setup

Build a co-branded landing page that presents the bundle offer, shows pricing comparison (separate vs. bundled), and routes visitors to a checkout or demo booking flow. The page must attribute traffic to the correct partner and bundle tier.

## Prerequisites

- Webflow account (or alternative: Framer, Carrd, Unbounce, Instapage)
- PostHog tracking snippet ready to embed
- Bundle pricing model finalized (from `bundle-pricing-model` fundamental)
- Both partners' logos, brand colors, and approved product descriptions
- Checkout or demo booking URL for the bundle (Stripe Checkout, Cal.com, or custom)

## Steps

1. **Create the landing page in Webflow.** Use the Webflow CMS API or Designer to build a page at `{your_domain}/bundles/{partner-slug}`:

   ```
   POST https://api.webflow.com/v2/sites/{SITE_ID}/pages
   Authorization: Bearer {WEBFLOW_API_KEY}
   Content-Type: application/json

   {
     "slug": "bundle-{partner_slug}",
     "title": "{Your Product} + {Partner Product} Bundle",
     "seo": {
       "title": "{Your Product} + {Partner Product} — Save {discount_pct}%",
       "description": "{Combined value prop in 155 characters}"
     }
   }
   ```

   Page structure:
   - Hero: co-branded logos, headline emphasizing combined value, subheadline with savings %
   - Pricing comparison table: "Buy separately" vs. "Bundle" with savings per tier
   - Feature grid: what each product does and how they integrate
   - Social proof: customer quotes mentioning both products (or integration value)
   - CTA: "Start with the bundle" routing to checkout or demo booking
   - FAQ: billing questions, what happens if one product is cancelled, support contacts

2. **Embed PostHog tracking.** Add the PostHog snippet and configure custom events:

   - `bundle_page_viewed` — fires on page load with properties: `partner_slug`, `utm_source`, `utm_campaign=bundle-deals-partnerships`
   - `bundle_tier_selected` — fires when a visitor clicks a pricing tier with property: `tier_name`
   - `bundle_cta_clicked` — fires when visitor clicks the primary CTA with properties: `tier_name`, `partner_slug`
   - `bundle_checkout_started` — fires when visitor reaches the checkout/booking page
   - `bundle_deal_completed` — fires on successful checkout or demo booking

3. **Build UTM-tracked inbound URLs.** Create tracked URLs for each partner to distribute:

   ```
   {your_domain}/bundles/{partner-slug}?utm_source={partner_slug}&utm_medium=bundle&utm_campaign=bundle-deals-partnerships&utm_content={tier_name}
   ```

   Each partner gets their own URL to share via email, social, or in-product. UTM parameters attribute every visit and conversion to the source partner.

4. **Connect checkout flow.** Link the CTA to your payment processor or booking tool:
   - **Stripe Checkout**: Create a Checkout Session with bundle line items using the Stripe API. Pass `client_reference_id` with the partner slug for attribution.
   - **Cal.com**: Create a booking link with prefilled fields for bundle context. Use `?metadata[partner]={partner_slug}&metadata[tier]={tier_name}`.
   - **Custom form**: Embed a Tally or Typeform that captures tier selection, partner attribution, and contact info, then routes to your sales team.

5. **Set up the partner's distribution page (optional).** If the partner wants to host the bundle on their site too, provide an embeddable widget or redirect URL that preserves tracking. Give them the UTM-tagged URL and co-branded assets (logos, screenshots, approved copy).

## Error Handling

- If Webflow API returns 401, verify API token has CMS and Pages write permissions
- If PostHog events do not fire, check that the tracking snippet loads before the custom event calls
- If UTM parameters are stripped by the partner's link shortener, use a server-side redirect that preserves parameters
- If Stripe Checkout Session fails, verify the bundle product and prices are created in Stripe first

## Alternative Tools

- **Framer**: Design-forward landing pages with API-driven content
- **Carrd**: Simple one-page sites for lightweight bundles
- **Unbounce**: Landing page builder with A/B testing built in
- **Instapage**: Enterprise landing pages with personalization
- **Leadpages**: Template-based landing pages with built-in checkout
- **Next.js + Vercel**: Custom-coded landing page for full control
