---
name: creator-prospect-research
description: Find, evaluate, and rank B2B micro-influencers whose audience overlaps with your ICP
category: Influencer
tools:
  - SparkToro
  - Modash
  - Passionfroot
  - Clay
  - Attio
fundamentals:
  - creator-discovery-search
  - clay-table-setup
  - clay-enrichment-waterfall
  - clay-scoring
  - attio-contacts
  - attio-lists
---

# Creator Prospect Research

This drill builds a scored shortlist of B2B micro-influencers to approach for sponsored posts. It covers discovery, audience validation, engagement scoring, and CRM staging.

## Input

- Your ICP definition: job titles, industries, company sizes, pain points
- Budget range per creator post (e.g., $200-500 for micro-influencers)
- Target platform(s): LinkedIn, newsletter, YouTube, Twitter
- Number of creators to shortlist: 10-20 for Smoke, 50+ for Baseline

## Steps

### 1. Run audience intelligence search

Use `creator-discovery-search` with SparkToro:
- Search for your ICP's job title or topic area
- Filter to creators with 1,000-50,000 followers (micro-influencer range)
- Export the top 30 accounts by audience overlap percentage

If SparkToro results are thin, supplement with Modash API search filtered by:
- Platform matching your target
- Bio keywords related to your product category
- Engagement rate above 2%
- Audience demographics matching your ICP age/location/industry

### 2. Browse Passionfroot for ready-to-book creators

Search Passionfroot's marketplace by category and platform. Creators listed here already sell sponsorship slots, which means:
- They are experienced with brand deals (less hand-holding)
- Pricing is transparent (their storefront shows rates)
- Booking is streamlined (no negotiation needed for standard slots)

Add Passionfroot finds to your shortlist with their listed pricing.

### 3. Import into Clay and enrich

Create a Clay table using `clay-table-setup` with columns:
- `creator_name`, `platform`, `handle`, `follower_count`, `engagement_rate`
- `audience_overlap_pct` (from SparkToro), `topic_fit` (1-5 manual score)
- `avg_likes`, `avg_comments`, `post_frequency` (posts per week)
- `email`, `linkedin_url`, `passionfroot_url`
- `estimated_cost` (their rate or your estimate based on follower count)

Use `clay-enrichment-waterfall` to find email addresses for outreach. Stack: Clearbit first, then People Data Labs, then Hunter.io.

### 4. Score and rank creators

Add a scoring formula using `clay-scoring`:

- **Audience fit (40%):** SparkToro overlap percentage, or manual assessment of audience-ICP match based on their content topics and follower demographics
- **Engagement quality (30%):** engagement rate (comments + meaningful replies, not just likes), reply rate on their posts, comment quality (are real professionals commenting?)
- **Content fit (20%):** how naturally could they mention your product category? Creators who already discuss adjacent topics score higher
- **Cost efficiency (10%):** estimated CPL based on follower count and typical conversion rates. Rule of thumb: expect 0.5-2% click rate on creator posts.

Score each factor 0-100, compute weighted total. Rank by score.

### 5. Manually validate top candidates

For the top 15 scored creators, do a manual check:
- Read their last 10 posts. Is the content quality high? Is the engagement genuine (not bots)?
- Check for past brand partnerships. Have they done sponsored posts before? Quality of those posts?
- Verify audience authenticity. Sudden follower spikes or engagement from non-ICP accounts are red flags.
- Check posting frequency. A creator who posts once a month is harder to work with than one posting 3x/week.

Remove any creators that fail manual validation. Backfill from the next tier.

### 6. Push to Attio

Use `attio-contacts` to create a contact record for each validated creator. Use `attio-lists` to create a list named "Creator Prospects — {{campaign_slug}}".

Tag each creator with:
- `creator_score`: their composite score
- `creator_tier`: Tier 1 (80+), Tier 2 (60-79), Tier 3 (40-59)
- `creator_status`: "prospect" (will change to "outreach_sent", "negotiating", "booked", "posted", "completed")
- `creator_platform`: primary platform
- `estimated_cost`: expected fee per post
- `passionfroot_url`: if they have a storefront

## Output

- Clay table with 10-50+ scored and ranked creators
- Attio list of validated creator prospects, ready for outreach
- Top 5-10 creators identified for first batch of outreach

## Triggers

Run once at the start of each campaign. Re-run quarterly to refresh the creator pool with new/emerging creators.
