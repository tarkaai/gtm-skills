---
name: podcast-sponsorships-b2b-smoke
description: >
  B2B Podcast Sponsorships — Smoke Test. Book one paid host-read ad on one niche
  B2B podcast to test whether the audience generates clicks and at least one
  qualified lead before committing recurring sponsorship budget.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Content"
level: "Smoke Test"
time: "5 hours over 3 weeks"
outcome: "≥15 clicks (UTM + vanity URL) and ≥1 qualified lead from a single paid podcast sponsorship"
kpis: ["Total attributed clicks", "Qualified leads", "CPC", "CPL", "Promo code redemptions"]
slug: "podcast-sponsorships-b2b"
install: "npx gtm-skills add marketing/problem-aware/podcast-sponsorships-b2b"
drills:
  - podcast-sponsor-research
  - podcast-sponsor-booking
  - threshold-engine
---

# B2B Podcast Sponsorships — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Content

## Outcomes

One paid host-read mid-roll sponsorship placed on one niche B2B podcast. At least 15 total attributed clicks (UTM show-notes clicks + vanity URL clicks) and at least 1 qualified lead (signup, demo request, or promo code redemption) within 14 days of the episode air date. This proves that buying audio ad placements on podcasts produces measurable signal for your ICP before you invest in a multi-podcast sponsorship program.

## Leading Indicators

- Podcast host responds to your sponsorship inquiry within 7 business days (signal: active ad program)
- Placement cost falls within $100-400 range for a niche B2B podcast with 1,000-10,000 downloads/episode (signal: accessible pricing for testing)
- Show-notes clicks begin arriving within 24 hours of episode publish (signal: engaged audience checking show notes)
- Vanity URL clicks appear within 48 hours (signal: listeners heard the verbal CTA and acted)
- Promo code redemptions within 14 days (signal: purchase-intent audience)

## Instructions

### 1. Research and select one podcast to sponsor

Run the `podcast-sponsor-research` drill with reduced scope: search AdvertiseCast, Podcorn, and Gumball for 15 candidate podcasts in your ICP's industry vertical. Also check 5-10 niche B2B podcasts via ListenNotes for direct sponsorship pages.

Score each podcast on ICP audience density, cost efficiency, and show quality. Select the single best podcast for your first placement based on highest composite score. Prioritize podcasts with:

- 1,000-10,000 downloads per episode (large enough for signal, affordable for testing)
- Host-read mid-roll available (outperforms pre-produced by ~31%)
- Active sponsorship program (existing sponsors prove the pipeline works)
- Placement cost of $100-400

### 2. Book the placement and configure tracking

Run the `podcast-sponsor-booking` drill for your selected podcast:

- Negotiate the rate. For a first-time test, ask for a single-episode test rate with the option to commit to a package if results meet your threshold.
- Set up three attribution signals:
  - **UTM link** for show notes: `{landing_page}?utm_source={podcast_slug}&utm_medium=paid-podcast&utm_campaign=podcast-sponsorships-b2b&utm_content={podcast_slug}-smoke-v1`
  - **Vanity URL** for verbal CTA: `yoursite.com/{podcast-slug}` redirecting to the UTM link
  - **Promo code** for checkout attribution: `{PODCASTNAME}` offering a clear incentive (extended trial, discount, etc.)
- Write 3 host-read ad script variants (problem-led, story-led, data-led). Select the best fit for the podcast's tone.
- Submit the script, show-notes text, vanity URL, and promo code to the host before the script deadline.

**Human action required:** Approve the placement cost and process payment. Review the ad script before submission. Verify the promo code is active in your billing system.

### 3. Prepare the landing page

Ensure the landing page receiving podcast traffic:
- Has one clear CTA matching what the ad promises (demo request, free trial, or resource download)
- Loads in under 3 seconds on mobile
- Has PostHog tracking capturing `$pageview` with UTM parameters, `podcast_sponsor_click` on arrival, and `podcast_sponsor_lead` on CTA completion
- Accepts the promo code if applicable
- Matches the messaging from the ad script (headline and CTA should be consistent with what the host reads)

### 4. Monitor results after episode airs

When the episode publishes:
- Confirm the episode is live and your ad was included (listen to verify)
- Check show notes for your tracked URL
- Monitor PostHog for `podcast_sponsor_click` events and `podcast_sponsor_lead` events
- Check Dub.co/Rebrandly for vanity URL clicks
- Note the click velocity: podcast listeners convert over 1-14 days (slower than newsletter or paid search)

### 5. Evaluate against threshold

Run the `threshold-engine` drill 14 days after the episode air date. Measure:

- **Total clicks**: UTM clicks (PostHog) + vanity URL clicks (Dub.co/Rebrandly)
- **Leads**: `podcast_sponsor_lead` events + promo code redemptions
- **CPC**: placement cost / total clicks
- **CPL**: placement cost / total leads

**Pass threshold: >= 15 total clicks AND >= 1 qualified lead**

- **Pass**: Document which podcast, what ad script angle, and what CPC/CPL you achieved. Proceed to Baseline.
- **Marginal**: 8-14 clicks or 0 leads but strong click engagement. Test one more podcast before deciding.
- **Fail**: <8 clicks. Diagnose: Was the podcast audience misaligned with your ICP? Was the ad script too generic? Did the host skip or butcher the read? Was the show-notes link missing? Try a different podcast with better ICP fit.

## Time Estimate

- Podcast research and selection: 2 hours
- Rate negotiation and booking: 30 minutes (plus wait time for host response — allow 1-2 weeks)
- Ad script writing and tracking setup: 1.5 hours
- Monitoring and evaluation: 1 hour (spread over 14 days post-air)

Total: ~5 hours of active work over 3 weeks (including host response time and the 14-day measurement window)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| AdvertiseCast / Podcorn / Gumball | Podcast ad marketplace discovery | Free for advertisers |
| ListenNotes | Podcast directory search | Free tier: 5 req/min; $9/mo for 300 req/day ([listennotes.com/pricing](https://www.listennotes.com/api/pricing/)) |
| Clay | Podcast publisher research and enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM tracking for sponsorship deals | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Click and lead tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Dub.co | Vanity URL for verbal CTA | Free: 1,000 links/mo ([dub.co/pricing](https://dub.co/pricing)) |
| Anthropic Claude | Ad script copywriting | Pay-per-use, ~$0.10-0.50 per script ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Podcast placement | Paid sponsorship | $100-400 for a single niche B2B placement |

**Estimated cost for this level: $100-400** (the podcast placement itself; all tools within free tiers)

## Drills Referenced

- `podcast-sponsor-research` — find and rank podcasts accepting paid sponsorships based on ICP overlap and cost-efficiency
- `podcast-sponsor-booking` — negotiate, book, write ad script, configure multi-signal tracking, and collect 14-day results
- `threshold-engine` — evaluate clicks and leads against the pass threshold
