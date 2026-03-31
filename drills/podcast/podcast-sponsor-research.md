---
name: podcast-sponsor-research
description: Find, evaluate, and rank podcasts accepting paid sponsorships based on ICP overlap, listener quality, and cost-efficiency
category: Podcast
tools:
  - AdvertiseCast
  - Podcorn
  - Gumball
  - ListenNotes
  - Clay
  - Attio
fundamentals:
  - podcast-sponsor-marketplace-search
  - podcast-directory-search
  - podcast-host-enrichment
  - clay-table-setup
  - clay-enrichment-waterfall
  - attio-lists
---

# Podcast Sponsor Research

This drill identifies podcasts that accept paid advertising, evaluates their audience quality and pricing, and produces a ranked shortlist of shows ready for sponsorship booking. This is for buying ad placements, not for guest appearances.

## Input

- Your ICP definition (firmographics, buyer persona, pain points, industries)
- Budget range per placement (e.g., $100-300 for Smoke, $200-500 for Baseline)
- Target number of evaluated podcasts (default: 20 candidates, top 5-8 shortlisted)
- Preferred ad format: host-read mid-roll (recommended), pre-roll, or custom integration
- Names of 2-3 competitors who sponsor podcasts (for cross-reference)

## Steps

### 1. Search podcast advertising marketplaces

Use the `podcast-sponsor-marketplace-search` fundamental to query AdvertiseCast, Podcorn, Gumball, and RedCircle. Search for podcasts in your ICP's industry verticals with active ad programs.

For each marketplace, filter by:
- Category matching your ICP (Technology, Business, Marketing, Entrepreneurship, SaaS)
- Downloads per episode: minimum 1,000 (Smoke), 5,000 (Baseline), 10,000 (Scalable)
- Host-read ad availability (preferred over programmatic for B2B trust)

Pull 15-25 candidate podcasts from marketplaces. For each, capture: podcast name, host name, marketplace source, estimated downloads/episode, CPM or flat rate, ad format, and minimum commitment.

### 2. Search podcast directories for direct sponsorship opportunities

Use `podcast-directory-search` (ListenNotes) to find niche B2B podcasts that may sell sponsorships directly (not on marketplaces). Search 3-5 keyword combinations:
- Primary topic: e.g., "B2B SaaS growth"
- Adjacent topics: e.g., "startup marketing", "developer tools"
- Problem-focused: e.g., "customer acquisition for startups"

Filter: English, actively publishing (episode within last 30 days), listen_score >= 25.

For each result, visit the podcast's website and check for:
- "Sponsor" or "Advertise" or "Partner" page
- Sponsor mentions in episode descriptions
- Existing sponsor reads in recent episodes (listen to 1-2 episodes)

Add podcasts that accept sponsorships to the candidate list.

### 3. Cross-reference competitor sponsorships

Search for competitor brand mentions in podcast episodes:
- ListenNotes episode search: `"{competitor_name}" sponsor` or `"{competitor_name}"` as episode content
- Google: `"{competitor_name}" podcast sponsor`
- Listen to competitor-sponsored podcasts to understand their ad positioning

Podcasts where competitors advertise are validated channels — the audience responds to products in your category. Flag these as priority targets.

### 4. Create the prospect table in Clay

Use `clay-table-setup` to create a Clay table called "Podcast Sponsor Prospects — {date}" with columns:

- Podcast name
- Host name
- Website URL
- Marketplace source (AdvertiseCast, Podcorn, Gumball, Direct)
- Estimated downloads per episode
- ListenNotes listen_score (if available)
- CPM rate or flat rate per placement
- Cost per placement (calculated: downloads * CPM / 1000)
- Ad format available (host-read mid-roll, pre-roll, etc.)
- Minimum commitment (1 episode, 3-pack, monthly)
- Ad sales contact name and email
- ICP audience fit score (1-5)
- Sponsor history (which brands currently sponsor)
- Booking status (researched / pitched / booked / completed)

Import all candidates from steps 1-3.

### 5. Enrich ad sales contacts

Run `podcast-host-enrichment` and `clay-enrichment-waterfall` on the Clay table to find verified email addresses for the podcast host, producer, or ad sales contact. Priority: marketplace booking page > podcast website contact > RSS feed email > Clay email finder > Apollo lookup.

### 6. Score and rank podcasts

For each podcast scoring 3+ on ICP audience fit, calculate a composite sponsorship score:

- **ICP audience density (40%)**: How closely does the listener demographic match your buyer persona? Score 1-5 based on: industry match, job title match, company size match.
- **Cost efficiency (30%)**: `1 / effective_cpm` — lower CPM per ICP-matched listener ranks higher. Normalize to 1-5 scale within the candidate set.
- **Show quality (20%)**: Listen_score, episode count (show longevity), publishing consistency, production quality.
- **Accessibility (10%)**: Marketplace booking = 5 (easy), direct with responsive contact = 3, no contact found = 1.

Composite score = `(ICP_density * 0.4) + (cost_efficiency * 0.3) + (show_quality * 0.2) + (accessibility * 0.1)`

### 7. Push shortlist to Attio

Use `attio-lists` to create a list called "Podcast Sponsor Targets — {date}". Push the top 5-8 podcasts (Smoke) or top 15-20 (Baseline+). Include all scored fields.

Tag each with priority tier:
- **Tier 1**: Top 25% by composite score — book first
- **Tier 2**: Middle 50% — book after Tier 1 results confirmed
- **Tier 3**: Bottom 25% — hold in reserve

### 8. Flag competitive intelligence

While researching, record which competitors sponsor which podcasts. Note:
- Competitor brand name
- Ad format they use (host-read, programmatic)
- How frequently they sponsor (one-off or recurring)
- What their CTA is (URL, promo code)

Store on each podcast's Attio record. Podcasts with active competitor sponsorships are validated but may also mean higher CPMs due to demand.

## Output

- Ranked shortlist of 5-8 (Smoke) or 15-20 (Baseline+) podcasts ready for paid sponsorship in Attio
- Each podcast scored on ICP density, cost efficiency, and show quality
- Ad sales contact info for each podcast
- Competitive intelligence on who else sponsors these shows
- Ready for `podcast-sponsor-rate-negotiation` fundamental and `podcast-sponsor-booking` drill

## Triggers

Run this drill once at Smoke level (scope: 15 candidates, shortlist 5). Run quarterly at Baseline+ to refresh the pipeline and discover new sponsorship opportunities. At Scalable, expand to 50+ candidates and shortlist 20+.
