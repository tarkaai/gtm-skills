---
name: podcast-sponsor-booking
description: Negotiate, book, submit ad copy, configure tracking, and collect results for a paid podcast sponsorship placement
category: Podcast
tools:
  - Attio
  - Anthropic
  - PostHog
  - Dub.co
fundamentals:
  - podcast-sponsor-rate-negotiation
  - podcast-sponsor-ad-copy
  - podcast-sponsor-placement-tracking
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Podcast Sponsor Booking

This drill handles the end-to-end process of booking a paid podcast sponsorship: negotiating the rate, writing the host-read ad script, setting up multi-signal tracking (UTM + vanity URL + promo code), submitting creative, and collecting results. One run of this drill produces one confirmed, tracked podcast sponsorship placement.

## Input

- Podcast selected from the shortlist (from `podcast-sponsor-research` drill)
- Approved budget for this placement
- Landing page URL for the campaign
- CTA type (demo request, free trial, resource download)
- Product one-liner and key benefit for this audience

## Steps

### 1. Negotiate the rate and book the placement

Use the `podcast-sponsor-rate-negotiation` fundamental to contact the podcast's ad contact and secure a placement:

- Request the media kit if not already obtained during research
- Evaluate: downloads per episode, audience demographics, ad format options, pricing
- If the rate exceeds budget, negotiate using: test-placement discount, off-peak episodes, or value exchange
- Target effective CPM of $20-50 for niche B2B podcasts
- Book a host-read mid-roll placement (60 seconds) as the default — this outperforms pre-roll and post-roll for B2B conversion

Once terms are agreed, create a deal record in Attio using `attio-deals`:
- Deal name: "Podcast Sponsor — {podcast_name} — {episode_date}"
- Amount: agreed price
- Stage: "Booked"
- Close date: episode air date
- Custom fields: podcast name, host, ad format, read duration, script deadline, estimated downloads, promo code, vanity URL

### 2. Set up multi-signal placement tracking

Use the `podcast-sponsor-placement-tracking` fundamental to configure all three attribution signals:

**Signal 1 — Show notes UTM link:**
```
{landing_page}?utm_source={podcast_slug}&utm_medium=paid-podcast&utm_campaign=podcast-sponsorships-b2b&utm_content={podcast_slug}-{date}-v1
```

**Signal 2 — Vanity URL for verbal CTA:**
Create a speakable redirect URL (e.g., `yoursite.com/startup-hustle`) pointing to the UTM-tagged landing page. Use Dub.co or Rebrandly API. Test that the redirect works and UTMs are preserved.

**Signal 3 — Promo code for checkout attribution:**
Create a promo code matching the podcast name (e.g., `STARTUPHUSTLE`). Configure in Stripe or your billing system. Set a 30-day expiry from the air date.

Create PostHog events: `podcast_sponsor_click`, `podcast_sponsor_lead`, `podcast_sponsor_promo_redeem` using `posthog-custom-events`. Build a saved funnel for this placement.

### 3. Write the host-read ad script

Use the `podcast-sponsor-ad-copy` fundamental to generate 3 ad script variants tailored to this podcast:

- Listen to 2-3 recent episodes to understand the host's style and ad read approach
- Generate: problem-led, story-led, and data-led variants
- Validate word count against the booked duration (60-sec mid-roll = 140-170 words)
- Read each variant aloud to verify it sounds natural at speaking pace

Select the strongest variant. If this is a repeat placement with this podcast, check past performance in Attio and lean toward the angle that produced the best results.

### 4. Prepare show notes text

Write 2-3 sentences for the episode description that includes the tracked URL:

```
{Product_name} helps {audience} {key_benefit}. {One line of social proof or a specific stat.} Learn more at {tracked_URL}.
```

This captures listeners who read show notes instead of (or in addition to) hearing the verbal CTA.

### 5. Submit the package to the host

Send to the podcast host/producer before the script deadline:

- **Talking points document**: The selected ad script variant as bullet points
- **Show notes text**: 2-3 sentences + tracked URL for the episode description
- **Vanity URL**: Confirmed working
- **Promo code**: Confirmed active, with the offer details (e.g., "10% off with code STARTUPHUSTLE")
- **Logo/brand assets**: PNG, 500px+ square, if the podcast uses sponsor logos in episode art
- **Pronunciation guide**: For your product name, if needed

Include: "Feel free to adjust the wording to match your style — these are talking points. The URL ({vanity_url}) and promo code ({PROMO}) are the two things that need to stay exact."

Log the submission in Attio using `attio-notes`: script text, variant used, vanity URL, promo code, tracked URL.

### 6. Confirm placement on air date

On the scheduled episode release date:

- Check the podcast feed (RSS or Spotify/Apple) to confirm the episode was published
- Listen to the episode to verify your ad was included and the CTA was correct
- Check show notes for your tracked URL
- Monitor PostHog for incoming `podcast_sponsor_click` events
- Log confirmation in Attio. Update deal stage to "Live"

**Human action required:** If the ad was not included or the CTA was incorrect, contact the host immediately to resolve. Request a make-good (re-run in the next episode) if the read was materially different from the agreed script.

### 7. Collect results after 14 days

Podcast attribution has a longer tail than newsletter or paid search. Wait 14 days, then pull results:

From PostHog:
- **Show-notes clicks**: `$pageview` where `utm_content` = `{placement_id}`
- **Vanity URL clicks**: Dub.co/Rebrandly click count
- **Total clicks**: show-notes + vanity URL
- **Leads**: `podcast_sponsor_lead` events where `podcast_name` = `{podcast_slug}`

From billing system:
- **Promo code redemptions**: Count of `{PODCASTNAME}` code uses

Calculate:
- **CPC**: `placement_cost / total_clicks`
- **CPL**: `placement_cost / (leads + promo_redemptions)`
- **Direct traffic uplift**: Compare 48-hour post-air direct traffic vs. baseline

Update the Attio deal record with actual performance using `attio-notes`. Update deal stage to "Completed" with outcome: "Pass" or "Fail" based on whether CPL meets targets.

## Output

- One confirmed, tracked podcast sponsorship placement
- Host-read ad script submitted and verified on air
- Multi-signal tracking: UTM + vanity URL + promo code + direct traffic
- Full cost and performance data logged in Attio
- Ready for `threshold-engine` evaluation

## Triggers

Run this drill for each podcast sponsorship placement. At Smoke: 1-2 placements. At Baseline: 3-6 placements over 6 weeks. At Scalable: 8-15 placements/month across multiple podcasts.
