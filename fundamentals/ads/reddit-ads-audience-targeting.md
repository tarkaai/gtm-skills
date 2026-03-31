---
name: reddit-ads-audience-targeting
description: Configure subreddit, interest, keyword, and custom audience targeting for Reddit Ads campaigns
tool: Reddit
product: Reddit Ads
difficulty: Config
---

# Reddit Ads — Audience Targeting

Configure targeting for Reddit ad groups using subreddit communities, interest categories, keyword targeting, and custom audiences. Reddit's targeting strength is community-based: users self-select into subreddits organized around shared interests, making subreddit targeting unusually precise for B2B.

## Targeting Types

Reddit Ads supports four primary targeting dimensions. When combined within an ad group, they use AND logic (users must match all criteria). Create separate ad groups for different targeting strategies.

### 1. Subreddit Targeting

Target users who are active in specific subreddits. This is Reddit's most powerful B2B targeting option.

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/adgroups
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "adgroup-subreddit-devops",
  "target": {
    "subreddits": ["devops", "sysadmin", "kubernetes", "aws"],
    "expansion": false
  }
}
```

Best practices:
- 3-5 subreddits per ad group for focused testing
- Mix 1 large subreddit (100k+ subscribers) with 2-4 niche ones (10k-50k)
- Set `expansion: false` to prevent Reddit from auto-expanding
- Niche subreddits (<50k members) have higher CPMs but better conversion rates
- Create separate ad groups for each subreddit cluster theme

Discovery: Use the `subreddit-research` fundamental to find relevant communities before building ad groups.

### 2. Interest Targeting

Target users by interest categories inferred from their browsing and engagement behavior across Reddit.

```json
{
  "target": {
    "interests": ["TECHNOLOGY", "BUSINESS_AND_FINANCE", "PROGRAMMING"],
    "expansion": false
  }
}
```

Available interest categories (partial list):
- `TECHNOLOGY` — general tech enthusiasts
- `BUSINESS_AND_FINANCE` — business, finance, entrepreneurship
- `PROGRAMMING` — software development
- `SCIENCE` — science and research
- `GAMING` — gaming (large reach, low B2B relevance)
- `CRYPTO_AND_BLOCKCHAIN` — crypto/web3

Interest targeting is broader than subreddit targeting. Use it to reach users who engage with topics across many communities, not just specific ones. Better for awareness than conversion.

### 3. Keyword Targeting

Target users based on keywords they have recently engaged with in post titles, bodies, and comments.

```json
{
  "target": {
    "keywords": ["deployment automation", "CI/CD pipeline", "devops tools", "infrastructure as code"],
    "keyword_match_type": "BROAD"
  }
}
```

Match types:
- `BROAD`: Matches related terms and variations. "devops tools" matches discussions about DevOps tooling.
- `EXACT`: Matches the exact phrase only. More precise, lower volume.

Keyword targeting increases CTR by ~30% compared to interest-only targeting. Combine with subreddit targeting for highest relevance.

### 4. Custom Audiences

Upload your own audience data (email lists) for targeting or exclusion.

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/custom_audiences
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "existing-customers-exclusion",
  "type": "EMAIL",
  "emails_hashed": ["5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"]
}
```

Notes:
- Hash emails with SHA-256 before uploading (Reddit matches against hashed user emails)
- Minimum audience size: 1,000 matched users
- Use for: excluding existing customers, targeting lookalikes from your best customers
- Refresh weekly via n8n automation

### 5. Geographic Targeting

```json
{
  "target": {
    "geos": [
      {"country": "US"},
      {"country": "GB"},
      {"country": "CA"}
    ]
  }
}
```

Available granularity: country, region/state, metro area (US only).

### 6. Device Targeting

```json
{
  "target": {
    "devices": ["DESKTOP", "MOBILE", "TABLET"]
  }
}
```

Reddit traffic skews mobile (~70%). For B2B conversions that require form fills, consider bidding higher on desktop where conversion rates are typically 2-3x higher.

## Audience Size Estimation

Before launching, check estimated audience size:

```
GET https://ads-api.reddit.com/api/v3/accounts/{account_id}/audience_estimate
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "target": {
    "subreddits": ["devops", "sysadmin"],
    "geos": [{"country": "US"}]
  }
}
```

Returns estimated daily reach. Target 50,000-500,000 for sufficient volume without diluting quality.

## Recommended Ad Group Structure for B2B

Create 3 ad groups for systematic testing:

| Ad Group | Targeting | Purpose |
|---|---|---|
| AG1 — Core Subreddits | 3-5 most ICP-relevant subreddits | Highest relevance, test viability |
| AG2 — Adjacent Subreddits | 3-5 related but broader subreddits | Test if adjacent audiences convert |
| AG3 — Keyword + Interest | Keywords matching your problem space + interest category | Broader reach, discover new pockets |

Run AG1 with 50% of budget, AG2 with 30%, AG3 with 20%. Shift budget toward winners after 1 week of data.

## Error Handling

- **Invalid subreddit**: API returns 400 if a subreddit name does not exist or is banned. Validate subreddit existence via `GET https://oauth.reddit.com/r/{subreddit}/about` before adding to targeting.
- **Audience too small**: Reddit requires minimum audience thresholds for delivery. If estimated reach is below 1,000, broaden targeting.
- **Targeting conflicts**: AND logic can make audiences too narrow. If combining subreddit + keyword + geo results in <5,000 estimated reach, remove one layer.
