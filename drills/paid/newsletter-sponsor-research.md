---
name: newsletter-sponsor-research
description: Find, evaluate, and rank newsletters for paid sponsorship based on ICP overlap, audience quality, and cost-efficiency
category: Paid
tools:
  - Clay
  - Attio
  - Paved
  - Swapstack
fundamentals:
  - newsletter-marketplace-search
  - partner-newsletter-audit
  - clay-company-search
  - clay-enrichment-waterfall
  - attio-lists
---

# Newsletter Sponsor Research

This drill identifies newsletters available for paid sponsorship, evaluates their audience quality and pricing, and produces a ranked shortlist ready for booking. Unlike partner research for free co-marketing, this drill focuses on paid placements and factors in cost-efficiency.

## Input

- Your ICP definition (firmographics, buyer persona, pain points)
- Budget range per placement (e.g., $100-500 for smoke test, $500-2,000 for baseline)
- Target number of evaluated newsletters (default: 30 candidates, top 10 shortlisted)
- Preferred newsletter frequency (weekly preferred for testing velocity)

## Steps

### 1. Search newsletter advertising marketplaces

Use the `newsletter-marketplace-search` fundamental to query Paved, Swapstack, Sparkloop, and Letterhead. Search for newsletters in your ICP's industry vertical. Also run a web search for `"{your_industry}" newsletter sponsorship` and `"{your_industry}" newsletter advertise` to find newsletters selling sponsorships directly.

Pull 30-50 candidate newsletters. For each, capture: name, publisher, subscribers, open rate, price, format, and source.

### 2. Research newsletter publishers via Clay

Use `clay-company-search` to find the companies behind each newsletter. Use `clay-enrichment-waterfall` to enrich with: company size, funding stage, industry, and the contact info for the person who manages ad sales or partnerships. This identifies who to negotiate with and verifies the publisher is a real, operating company.

### 3. Audit each newsletter for quality and fit

For the top 20 candidates (sorted by effective CPM), run the `partner-newsletter-audit` fundamental. For each newsletter:

- Read the last 3-5 issues to verify content quality and audience alignment
- Check if they already run sponsor content (proof of an established ad program)
- Score on the 1-5 scale across four dimensions: audience overlap, audience size, engagement quality, and ad-program maturity
- Flag newsletters that appear to have inflated subscriber counts (very low engagement relative to claimed size)

### 4. Calculate cost-efficiency metrics

For every newsletter that scores 12+ out of 20 on the audit, calculate:

- **Effective CPM**: `(price / subscribers) * 1000`
- **Cost per estimated open**: `price / (subscribers * open_rate)`
- **Cost per estimated click**: `price / (subscribers * open_rate * estimated_ctr)` — use 2% CTR as default for sponsored blurbs if no data available
- **ICP density score**: Multiply the audience overlap score (1-5) by the audience size score (1-5). Higher means more ICP-matched eyeballs per dollar.

### 5. Rank and build the shortlist in Attio

Use the `attio-lists` fundamental to create a list called "Newsletter Sponsors — {date}". Add the top 10-15 newsletters ranked by: `ICP_density_score / effective_CPM` (maximize ICP exposure per dollar). Include fields:

- Newsletter name and URL
- Publisher company name
- Estimated subscribers and open rate
- Price per placement and effective CPM
- Audit score (out of 20)
- ICP density score
- Ad sales contact name, email, and LinkedIn
- Marketplace source (Paved, direct, etc.)
- Status: "Researched" (initial state)

### 6. Flag competitive intelligence

While auditing newsletters, note which competitors are already sponsoring them. Use Who Sponsors Stuff (whosponsorsstuff.com) to check sponsor history. Newsletters where competitors advertise are validated channels — their audience responds to products like yours. Record competitor names on each newsletter's Attio record.

## Output

- Ranked shortlist of 10-15 newsletters ready for paid sponsorship in Attio
- Each newsletter scored on audience quality, ICP overlap, and cost-efficiency
- Ad sales contact info for each newsletter
- Competitive intelligence on who else sponsors these newsletters
- Ready for `newsletter-rate-negotiation` fundamental and `newsletter-sponsor-booking` drill

## Triggers

Run this drill once at Smoke level (minimal scope: 10 candidates, shortlist 3). Run quarterly at Baseline+ to refresh the newsletter pipeline and discover new sponsorship opportunities.
