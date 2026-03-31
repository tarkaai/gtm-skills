---
name: newsletter-marketplace-search
description: Search newsletter advertising marketplaces to find paid sponsorship opportunities matching your ICP
tool: Paved / Swapstack / Sparkloop / Letterhead / direct outreach
difficulty: Setup
---

# Newsletter Marketplace Search

## Prerequisites
- ICP definition (industry, buyer title, company size)
- Approximate budget range per placement ($100-5,000)
- Web search access or marketplace API credentials

## Steps

1. **Search Paved (primary marketplace).** Paved is the largest newsletter advertising marketplace. Query their inventory:

   ```
   GET https://www.paved.com/explore
   ```

   Use their search filters:
   - Category: select the industry vertical matching your ICP (e.g., "SaaS", "Developer Tools", "Marketing", "Finance")
   - Audience size: minimum 1,000 subscribers
   - Price range: set to your per-placement budget
   - Format: "Sponsored blurb" or "Dedicated email" depending on your preference

   For each result, record: newsletter name, estimated subscribers, open rate, price per placement, audience description, and Paved listing URL.

   Paved API (if available via partnership): `POST https://api.paved.com/v1/newsletters/search` with body `{"category": "{category}", "min_subscribers": 1000, "max_price": {budget}}`. Response includes `newsletter_id`, `name`, `subscribers`, `open_rate`, `cpm`, `price_per_send`.

2. **Search Swapstack / Sparkloop.** Swapstack (now part of Beehiiv) and Sparkloop offer newsletter recommendation and advertising networks:

   - Swapstack: Browse at `https://swapstack.co/brands` — filter by category and audience size
   - Sparkloop: `https://sparkloop.app/partner` — focused on newsletter cross-promotion with paid options

   Record the same fields: newsletter name, subscribers, open rate, price, audience description.

3. **Search Letterhead and direct outreach targets.** For niche newsletters not on marketplaces:

   - Letterhead: `https://letterhead.email/discover` — curated newsletter directory
   - Google search: `"{your_industry}" newsletter sponsorship OR "sponsor this newsletter" OR "advertise in our newsletter"`
   - Substack leaderboard: `https://substack.com/discover/{category}` — find high-traffic Substacks, then check if they accept sponsors (look for "sponsor" link in footer or about page)
   - Beehiiv Boost network: `https://app.beehiiv.com/boosts/earn` — newsletters seeking paid recommendations

4. **Compile the raw prospect list.** For each newsletter found, capture:
   - Newsletter name
   - Publisher/company name
   - Signup URL
   - Estimated subscribers
   - Published open rate (if available)
   - Price per placement (CPM or flat rate)
   - Marketplace source (Paved, Swapstack, Sparkloop, direct)
   - Contact email or booking URL
   - Category/niche
   - Frequency (daily, weekly, biweekly, monthly)

   Store as a spreadsheet or Clay table. Aim for 30-50 candidates in the initial search.

5. **Calculate effective CPM for each newsletter.** Normalize pricing for comparison:

   ```
   effective_cpm = (price_per_placement / estimated_subscribers) * 1000
   ```

   Also calculate cost per estimated open:
   ```
   cost_per_open = price_per_placement / (estimated_subscribers * open_rate)
   ```

   Sort by cost_per_open ascending. Newsletters with high open rates and reasonable pricing rise to the top.

## Error Handling
- If a marketplace returns no results for your category, broaden the search to adjacent categories
- If pricing is not listed, email the newsletter publisher directly: "We are interested in sponsoring an upcoming issue. Could you share your media kit or rate card?"
- If open rates are not published, assume 30% for niche B2B newsletters as a conservative estimate

## Alternative Tools
- **Paved**: Largest marketplace, best for B2B newsletters
- **Swapstack/Beehiiv**: Strong for creator-led newsletters
- **Sparkloop**: Best for newsletter recommendation placements
- **Letterhead**: Curated directory, good for discovery
- **Who Sponsors Stuff** (whosponsorsstuff.com): Tracks which brands sponsor which newsletters — useful for competitive research
- **The Sample** (thesample.ai): AI-driven newsletter discovery, can surface niche options
