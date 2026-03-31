---
name: podcast-sponsor-placement-tracking
description: Build tracked landing pages, vanity URLs, promo codes, and PostHog events for podcast sponsorship attribution
tool: PostHog
difficulty: Setup
---

# Podcast Sponsor Placement Tracking

Set up end-to-end attribution for paid podcast sponsorship placements. Podcast ads are audio — listeners cannot click a link mid-episode. This requires a multi-signal approach: vanity URLs for verbal CTAs, promo codes for checkout attribution, UTM parameters for show-notes clicks, and PostHog events for full-funnel tracking.

## Prerequisites

- PostHog project with tracking snippet on your landing page
- Landing page URL for the campaign
- Podcast name and episode air date
- Vanity URL domain (e.g., via Dub.co or Rebrandly) or a path on your site
- Stripe or payment system for promo code setup (if applicable)

## Steps

### 1. Build the UTM-tagged landing page URL

Every podcast sponsorship gets a unique tracked URL for show notes:

```
{base_url}?utm_source={podcast_slug}&utm_medium=paid-podcast&utm_campaign=podcast-sponsorships-b2b&utm_content={podcast_slug}-{YYYY-MM-DD}-v{variant}
```

Parameter definitions:
- `utm_source`: Slugified podcast name (e.g., `the-saas-podcast`, `startup-hustle`)
- `utm_medium`: Always `paid-podcast` to distinguish from guest appearances (`guest`) and organic
- `utm_campaign`: Always `podcast-sponsorships-b2b` for this play
- `utm_content`: Unique placement ID: `{podcast_slug}-{episode_date}-v{variant_number}`

Example:
```
https://yourproduct.com/demo?utm_source=startup-hustle&utm_medium=paid-podcast&utm_campaign=podcast-sponsorships-b2b&utm_content=startup-hustle-2026-04-15-v1
```

### 2. Create the vanity URL for verbal CTA

Podcast listeners hear URLs spoken aloud. Complex UTM URLs are unusable verbally. Create a short, memorable redirect:

**Per-podcast vanity path (preferred):**
```
https://yoursite.com/{podcast-slug} → redirects to the UTM-tagged URL
```

**Using Dub.co:**
```http
POST https://api.dub.co/links
Header: Authorization: Bearer {DUB_API_KEY}
Content-Type: application/json

{
  "url": "https://yourproduct.com/demo?utm_source=startup-hustle&utm_medium=paid-podcast&utm_campaign=podcast-sponsorships-b2b&utm_content=startup-hustle-2026-04-15-v1",
  "key": "startup-hustle",
  "domain": "your-short-domain.co"
}
```

**Using Rebrandly:**
```http
POST https://api.rebrandly.com/v1/links
Header: apikey: {REBRANDLY_API_KEY}
Content-Type: application/json

{
  "destination": "https://yourproduct.com/demo?utm_source=startup-hustle&utm_medium=paid-podcast&utm_campaign=podcast-sponsorships-b2b",
  "slashtag": "startup-hustle",
  "domain": { "fullName": "your-brand.link" }
}
```

Requirements:
- Maximum 3 syllables after the domain (speakable)
- Easy to spell when heard (no hyphens, numbers, or ambiguous letters)
- Tested: load the URL and verify the redirect preserves UTM parameters

### 3. Set up the promo code

Create a promo code matching the podcast name for checkout attribution:

**In Stripe:**
```http
POST https://api.stripe.com/v1/coupons
Authorization: Bearer {STRIPE_SECRET_KEY}
Content-Type: application/x-www-form-urlencoded

id={PODCASTNAME}&percent_off=10&duration=once&max_redemptions=500&redeem_by={unix_timestamp_30_days_from_air_date}
```

If you do not sell via Stripe, create the equivalent promo code in your billing system. The code should:
- Match the podcast name in all caps (e.g., `STARTUPHUSTLE`)
- Offer a clear incentive (10-20% discount, extended trial, free month)
- Expire 30 days after the episode air date
- Have a redemption cap to control cost

Log the promo code in Attio on the placement deal record.

### 4. Configure PostHog events

PostHog automatically captures UTM parameters on `$pageview` events. Verify by loading the tracked URL and checking PostHog live events.

Create custom events for the podcast sponsorship funnel:

```javascript
// Fire on landing page load when utm_medium = paid-podcast
const params = new URLSearchParams(window.location.search);
if (params.get('utm_medium') === 'paid-podcast') {
  posthog.capture('podcast_sponsor_click', {
    podcast_name: params.get('utm_source'),
    placement_id: params.get('utm_content'),
    campaign: params.get('utm_campaign')
  });
}

// Fire when visitor completes CTA (signup, demo request, form submit)
posthog.capture('podcast_sponsor_lead', {
  podcast_name: params.get('utm_source'),
  placement_id: params.get('utm_content'),
  lead_type: 'demo_request' // or 'signup', 'trial', 'download'
});

// Fire when promo code is redeemed (server-side or via Stripe webhook)
posthog.capture('podcast_sponsor_promo_redeem', {
  promo_code: '{PODCASTNAME}',
  podcast_name: '{podcast_slug}',
  placement_id: '{placement_id}'
});
```

### 5. Build a PostHog funnel for this placement

Create a saved insight:
- Step 1: `$pageview` where `utm_campaign` = `podcast-sponsorships-b2b` AND `utm_source` = `{podcast_slug}`
- Step 2: `podcast_sponsor_lead` where `podcast_name` = `{podcast_slug}`
- Conversion window: 14 days (podcast listeners often convert days after hearing the ad)

Save as: "Podcast Sponsor — {Podcast Name} — {Date} — Funnel"

### 6. Set up direct traffic spike detection

Many podcast listeners type URLs directly or Google your brand after hearing the ad. To capture this:

- Create a PostHog insight: `$pageview` on your homepage or pricing page, daily trend
- Set a baseline for the 14 days before the episode airs
- After the episode airs, compare the 48-hour traffic spike vs. baseline
- If direct/organic traffic increases by >20% in the 48 hours after air date, attribute the uplift to the podcast placement

This is an estimate, not exact attribution, but captures the "dark social" effect of audio advertising.

### 7. Calculate placement ROI after 14 days

Pull from PostHog and promo code data:

- **Show-notes clicks**: `$pageview` where `utm_content` = `{placement_id}`
- **Vanity URL clicks**: Dub.co or Rebrandly click count for the vanity link
- **Leads from UTM**: `podcast_sponsor_lead` events where `podcast_name` = `{podcast_slug}`
- **Promo code redemptions**: Stripe coupon redemption count for `{PODCASTNAME}`
- **Direct traffic uplift**: Estimated additional visits in 48-hour window post-air
- **Total attributed leads**: UTM leads + promo redemptions
- **CPC**: `placement_cost / (show_notes_clicks + vanity_clicks)`
- **CPL**: `placement_cost / total_attributed_leads`

Store these metrics in Attio on the podcast placement deal record.

## Error Handling

- **Vanity URL not resolving**: Test 24 hours before the script deadline. Check DNS propagation and redirect configuration.
- **Promo code not working**: Test a redemption before submitting the script to the host. Verify the code is active in your billing system.
- **Zero clicks within 72 hours of air date**: Ask the host to confirm the episode was published and that the show notes include the link. Some hosts forget to add links to show notes.
- **UTM parameters stripped by redirects**: Test the full chain: vanity URL → redirect → landing page. Verify PostHog captures UTMs on the final page.
- **Longer attribution window for podcasts**: Unlike newsletter clicks (immediate), podcast listeners may convert 1-14 days later. Use a 14-day attribution window, not 7.

## Alternative Tools

- **PostHog**: Primary analytics (free up to 1M events/mo)
- **Podscribe**: Dedicated podcast attribution platform ($250/mo + $1.50 CPM). Pixel-based household-level tracking.
- **Chartable (Spotify)**: Prefix URL analytics for download tracking
- **Google Analytics 4**: Alternative UTM tracking
- **Mixpanel / Amplitude**: Alternative event analytics
- **Dub.co**: Vanity URL management (free tier: 1,000 links/mo)
- **Rebrandly**: Branded short links ($13/mo starter)
- **Bitly**: Simple click tracking backup
