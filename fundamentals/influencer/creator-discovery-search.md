---
name: creator-discovery-search
description: Search for B2B creators and micro-influencers by audience, topic, and engagement metrics
tool: SparkToro / Modash / Passionfroot / Clay
difficulty: Setup
---

# Creator Discovery Search

Find B2B micro-influencers whose audience overlaps with your ICP. This fundamental covers searching creator databases and audience intelligence platforms to build a shortlist of potential partners.

## Option 1: SparkToro (Audience Intelligence)

Best for: finding which creators your ICP already follows.

### API / Web App

SparkToro does not expose a public REST API. Use the web app.

1. Navigate to `https://sparktoro.com`
2. Search by audience description: enter your ICP job title or topic (e.g., "DevOps engineers" or "B2B SaaS marketing")
3. SparkToro returns:
   - Social accounts the audience follows (ranked by % overlap)
   - Podcasts the audience listens to
   - YouTube channels the audience watches
   - Websites and publications the audience reads
4. Filter by follower count: set range to 1,000-50,000 followers to target micro-influencers
5. Export the list of creators as CSV (available on paid plans)

### Output Fields
- Creator name, platform, handle, follower count, audience overlap %

### Authentication
- Free: 5 searches/month, sampled results
- Standard ($50/mo): 50 searches/month, full results, CSV export
- Agency ($225/mo): 500 searches/month

## Option 2: Modash (Influencer Database)

Best for: detailed creator analytics across Instagram, YouTube, TikTok.

### API

```
GET https://api.modash.io/v1/influencers/search
Authorization: Bearer {MODASH_API_KEY}
Content-Type: application/json

{
  "platform": "instagram",
  "filters": {
    "followers": { "min": 1000, "max": 50000 },
    "engagement_rate": { "min": 2.0 },
    "audience": {
      "interests": ["technology", "business"],
      "age_groups": ["25-34", "35-44"],
      "genders": ["male"]
    },
    "bio_keywords": ["SaaS", "B2B", "startup", "devtools"]
  },
  "limit": 50,
  "offset": 0
}
```

### Response Format
```json
{
  "influencers": [
    {
      "id": "abc123",
      "username": "saasmarketer",
      "platform": "instagram",
      "followers": 12400,
      "engagement_rate": 3.2,
      "avg_likes": 380,
      "avg_comments": 24,
      "audience_demographics": {
        "top_countries": ["US", "UK", "CA"],
        "age_groups": { "25-34": 42, "35-44": 28 }
      }
    }
  ],
  "total": 312
}
```

### Authentication
- API key from Modash dashboard → Settings → API
- Pricing: starts at $16,200/year for API access; web app plans from $199/mo

## Option 3: Passionfroot (B2B Creator Marketplace)

Best for: finding B2B creators who already sell sponsorship slots.

### Web App

1. Navigate to `https://www.passionfroot.me/creators`
2. Browse by category: "Tech", "Business", "Marketing", "SaaS"
3. Filter by:
   - Platform (LinkedIn, Newsletter, YouTube, Twitter, Podcast)
   - Audience size range
   - Price range per post
4. Each creator profile shows: audience size, engagement rate, pricing, availability, past brand partners
5. Bookmark creators to a shortlist

### No API Available
Passionfroot is web-app only. Use browser automation or manual curation.

### Pricing
- Free to browse and book creators
- 2% transaction fee on direct deals (paid by brand)
- 15% sourcing fee on Partner Network deals

## Option 4: Clay (Manual Enrichment)

Best for: building a custom creator list from LinkedIn or Twitter data.

1. Create a Clay table with columns: `creator_name`, `platform`, `handle`, `follower_count`, `topic`, `post_frequency`, `avg_engagement`
2. Use `clay-claygent` to research each creator: "Find the LinkedIn follower count, posting frequency, and average engagement for [handle]"
3. Use `clay-enrichment-waterfall` to enrich with email addresses for outreach
4. Score creators using a Clay formula column (see `creator-outreach-pipeline` drill)

## Error Handling

- **Rate limits:** SparkToro and Modash both rate-limit API calls. Implement exponential backoff. Modash returns `429 Too Many Requests` with a `Retry-After` header.
- **No results:** If searches return zero creators, broaden the topic keywords or increase the follower range. B2B micro-influencers are often categorized under general "business" or "tech" rather than niche terms.
- **Stale data:** Creator metrics change. Re-run discovery monthly to catch new creators and drop inactive ones.
