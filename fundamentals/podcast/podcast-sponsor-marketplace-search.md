---
name: podcast-sponsor-marketplace-search
description: Search podcast advertising marketplaces to find shows accepting paid sponsorships matching your ICP
tool: AdvertiseCast
difficulty: Setup
---

# Podcast Sponsor Marketplace Search

Search podcast ad marketplaces and networks to find shows that accept paid sponsorships from advertisers, matching your ICP's industry, audience size, and budget constraints.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| AdvertiseCast (Libsyn Ads) | Self-serve marketplace (web) | 1,300+ indie podcasts, host-read + programmatic, $500+ minimum |
| Podcorn | Self-serve marketplace (web) | No minimum spend, direct podcast-to-brand matching, 10% commission |
| Acast | Self-serve + managed | Programmatic + host-read, large podcast network, CPA models via Podscribe |
| Gumball | Marketplace (web) | Mid-size indie podcasts, transparent CPM pricing |
| RedCircle | Marketplace + network (web) | Self-serve, flexible budgets, cross-promotion options |
| Spotify Ad Studio | Self-serve (web) | Spotify-exclusive shows, audio + display ads, $250 minimum |
| iHeart Ad Builder | Self-serve (web) | Large-audience shows, $500 minimum |

None of these platforms have public REST APIs for programmatic search. All discovery is done via their web interfaces or by contacting their sales teams.

## AdvertiseCast / Libsyn Ads (Primary for B2B)

### Discovery

Browse the marketplace at `https://advertising.libsyn.com/` or `https://www.advertisecast.com/`.

Use filters:
- **Category**: Select industry verticals (Technology, Business, Marketing, Entrepreneurship, Science)
- **Downloads per episode**: Minimum 1,000 (Smoke), 5,000+ (Baseline), 10,000+ (Scalable)
- **Ad type**: Host-read (preferred for B2B trust) or Pre-produced
- **Placement**: Pre-roll, mid-roll, or post-roll
- **Price range**: Set to your per-placement budget

For each result, capture:
- Podcast name and host name
- Category/genre
- Estimated downloads per episode
- CPM rate (host-read mid-roll typically $25-40 CPM for B2B)
- Minimum commitment (episodes or spend)
- Contact email or booking URL

### Pricing Model

AdvertiseCast uses CPM pricing. Revenue split: 70% to podcaster, 30% to AdvertiseCast. Minimum campaign: $500.

Typical B2B niche rates:
- Pre-roll (15-30 sec): $15-25 CPM
- Mid-roll host-read (60 sec): $25-40 CPM
- Post-roll (15-30 sec): $10-20 CPM

Calculate cost per placement: `downloads_per_episode * cpm / 1000`

Example: 5,000 downloads/episode at $30 CPM mid-roll = $150/placement.

## Podcorn (Low-Budget Entry)

### Discovery

Browse at `https://www.podcorn.com/` — create a brand account (free).

Post a campaign brief with:
- Campaign name and description
- Target audience description
- Budget range per episode
- Preferred ad format: host-read, product review, topical discussion, or custom integration
- Campaign dates

Podcasters matching your criteria will send proposals. You can also browse podcasters directly and invite them to your campaign.

### Pricing Model

No minimum spend. Podcorn takes 10% commission from the podcaster's side. Pricing is negotiated directly between brand and podcaster. Typical niche B2B podcast rates on Podcorn: $50-300 per episode for shows with 500-5,000 downloads.

## Acast

### Discovery

Contact Acast sales at `https://advertise.acast.com/` or use their self-serve platform. Acast offers:
- Programmatic ad insertion (DAI) across their network
- Host-read sponsorships on specific shows
- CPA models integrated with Podscribe attribution

### Pricing

Self-serve: starts at $250 minimum campaign spend. Managed: custom quotes. CPM rates: $15-35 for programmatic, $25-50 for host-read.

## Gumball

### Discovery

Browse at `https://www.gumball.fm/`. Gumball focuses on mid-size indie podcasts with transparent pricing.

- Search by category and audience size
- See published CPM rates upfront
- Book host-read spots directly through the platform

### Pricing

Transparent CPM-based. Typical mid-roll rates: $20-35 CPM. Gumball takes 25% commission.

## RedCircle

### Discovery

Browse at `https://redcircle.com/brands`. Self-serve platform for booking ads across indie podcasts.

- Category-based search
- Audience size filters
- Direct messaging with podcast hosts

### Pricing

Flexible budgets, no stated minimum. CPM or flat-rate pricing negotiated per show.

## Direct Outreach (for Podcasts Not on Marketplaces)

Many high-value B2B podcasts sell sponsorships directly. To find them:

1. Search Google: `"{your_industry}" podcast sponsorship OR "sponsor this podcast" OR "become a sponsor"`
2. Check podcast websites for "Sponsors," "Advertise," or "Partner" pages
3. Look at competitors' podcast appearances — if they sponsor a show, it validates the audience
4. Use ListenNotes (`podcast-directory-search` fundamental) to find niche shows, then visit their websites for sponsorship info

For direct outreach, email the host/producer requesting their media kit or rate card.

## Qualifying a Podcast for Sponsorship

For each podcast found, evaluate:

1. **Downloads per episode**: Minimum 1,000 for Smoke, 5,000+ for Baseline
2. **Audience fit**: Does the podcast's listener demographic match your ICP? Check the media kit for audience data.
3. **Accepts advertising**: Confirmed — the show is on a marketplace or has a sponsorship page
4. **Host-read available**: Host-read ads outperform pre-produced by ~31% in purchase rate (Podscribe data)
5. **Publishing cadence**: Weekly or biweekly preferred (more frequent = faster testing)
6. **Sponsor history**: Shows with existing sponsors have proven ad programs

Store qualified podcasts in a Clay table or Attio list with fields: show name, host, downloads/episode, CPM, cost per placement, marketplace source, ad format, booking status.

## Error Handling

- **No results in your niche**: Broaden category search. Try adjacent verticals (e.g., if "DevOps" returns nothing, try "Software Engineering" or "Technology")
- **Rates not published**: Email the podcast or marketplace for a rate card. Assume $25-40 CPM for niche B2B as a planning estimate.
- **Marketplace requires minimum spend above budget**: Use Podcorn (no minimum) or direct outreach for Smoke testing
