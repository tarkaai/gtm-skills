---
name: newsletter-placement-tracking
description: Build UTM-tagged tracking links and PostHog events for individual paid newsletter placements
tool: PostHog
difficulty: Setup
---

# Newsletter Placement Tracking

## Prerequisites
- PostHog project with tracking snippet on your landing page
- Landing page URL for this campaign
- Newsletter name and placement date
- PostHog API key for server-side event creation if needed

## Steps

1. **Build the UTM-tagged URL.** Every newsletter sponsorship placement gets a unique tracked URL:

   ```
   {base_url}?utm_source={newsletter_slug}&utm_medium=paid-newsletter&utm_campaign=newsletter-sponsorships&utm_content={placement_id}
   ```

   Parameter definitions:
   - `utm_source`: Slugified newsletter name (e.g., `the-saas-weekly`, `morning-brew-tech`)
   - `utm_medium`: Always `paid-newsletter` to distinguish from organic/partner newsletters
   - `utm_campaign`: Always `newsletter-sponsorships` for this play
   - `utm_content`: Unique placement ID combining newsletter + date + variant (e.g., `saas-weekly-2026-04-01-v1`)

   Example: `https://yourproduct.com/demo?utm_source=the-saas-weekly&utm_medium=paid-newsletter&utm_campaign=newsletter-sponsorships&utm_content=saas-weekly-2026-04-01-v1`

2. **Verify PostHog captures UTM parameters.** Load the tracked URL in a browser and confirm PostHog records:
   - `$pageview` event with properties: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`
   - `$set` on the person: `$initial_utm_source`, `$initial_utm_medium`, `$initial_utm_campaign`

   If UTM parameters are not captured, check that PostHog autocapture is enabled or add explicit UTM capture in your tracking code:

   ```javascript
   const params = new URLSearchParams(window.location.search);
   posthog.capture('newsletter_sponsor_click', {
     utm_source: params.get('utm_source'),
     utm_medium: params.get('utm_medium'),
     utm_campaign: params.get('utm_campaign'),
     utm_content: params.get('utm_content'),
     newsletter_name: '{newsletter_name}',
     placement_date: '{YYYY-MM-DD}',
     placement_cost: {cost_in_cents}
   });
   ```

3. **Create the conversion event.** Define a PostHog event that fires when a newsletter-sourced visitor takes the primary CTA action:

   ```javascript
   // Fire when the visitor completes signup, demo request, or form submission
   posthog.capture('newsletter_sponsor_lead', {
     utm_source: params.get('utm_source'),
     newsletter_name: '{newsletter_name}',
     placement_id: '{placement_id}',
     lead_type: 'demo_request' // or 'signup', 'download', etc.
   });
   ```

4. **Build a PostHog funnel for this placement.** Create a saved insight:
   - Step 1: `$pageview` where `utm_campaign` = `newsletter-sponsorships` AND `utm_source` = `{newsletter_slug}`
   - Step 2: `newsletter_sponsor_lead` where `utm_source` = `{newsletter_slug}`

   Save as: "Newsletter Sponsorship — {Newsletter Name} — {Date} — Funnel"

5. **Set up real-time monitoring.** On the day the newsletter sends, create a PostHog live view filtered to:
   - Events where `utm_medium` = `paid-newsletter`
   - Grouped by `utm_source`

   This gives you real-time click velocity per newsletter placement.

6. **Calculate placement ROI after 7 days.** Pull from PostHog:
   - Total clicks: count of `$pageview` where `utm_content` = `{placement_id}`
   - Total leads: count of `newsletter_sponsor_lead` where `placement_id` = `{placement_id}`
   - CPC: `placement_cost / total_clicks`
   - CPL: `placement_cost / total_leads`
   - CTR: `total_clicks / estimated_newsletter_audience` (use the subscriber count from your research)

   Store these metrics in Attio on the newsletter placement record.

## Error Handling
- If clicks appear but UTM parameters are missing, the landing page may be stripping query parameters — check for redirects that drop UTMs
- If zero clicks appear within 24 hours of the newsletter send, verify the publisher actually included your link (ask for a screenshot of the sent email)
- If PostHog shows clicks but no leads, the landing page is the bottleneck — optimize the page before rebooking

## Alternative Tools
- **Bitly**: URL shortener with click tracking (backup if UTM capture fails)
- **PostHog**: Primary analytics platform
- **Mixpanel**: Alternative analytics for event tracking
- **Amplitude**: Alternative analytics platform
- **Google Analytics 4**: Alternative with UTM capture built in
- **Plausible**: Privacy-focused alternative analytics
