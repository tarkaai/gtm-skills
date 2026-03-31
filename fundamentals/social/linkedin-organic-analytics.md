---
name: linkedin-organic-analytics
description: Pull LinkedIn post and profile analytics via API or analytics tools
tool: LinkedIn
product: LinkedIn Organic
difficulty: Config
---

# Pull LinkedIn Analytics Programmatically

## Prerequisites
- LinkedIn account with Creator Mode enabled
- One of: LinkedIn API access (with `r_organization_social` or `r_liteprofile`), Taplio account, Shield account, or AuthoredUp account

## Option A: LinkedIn API (Direct)

1. **Get post engagement metrics.** For a specific post (you need the post URN from when you published):
   ```
   GET https://api.linkedin.com/rest/socialActions/{POST_URN}
   Authorization: Bearer {ACCESS_TOKEN}
   LinkedIn-Version: 202401
   ```
   Returns: `likesSummary.totalLikes`, `commentsSummary.totalFirstLevelComments`, `sharesSummary.totalShares`.

2. **Get post impressions and unique views.** Use the organizationPageStatistics endpoint (requires Company Page admin) or the share statistics endpoint:
   ```
   GET https://api.linkedin.com/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:{ORG_ID}&shares=List({POST_URN})
   ```
   For personal profiles, LinkedIn's API does not expose impression counts directly. Use Taplio or Shield (Options B/C) for personal profile impression data.

3. **Get profile view count.** LinkedIn does not expose exact profile view counts via API for personal profiles. The `r_liteprofile` scope only returns basic profile data. Use Taplio or Shield for profile visit trends.

## Option B: Taplio (Recommended for Personal Profiles)

1. **Pull post analytics via Taplio API:**
   ```
   GET https://app.taplio.com/api/v1/analytics/posts
   X-API-KEY: {TAPLIO_API_KEY}
   ```
   Returns per-post: impressions, likes, comments, shares, engagement rate, and click-through data.

2. **Pull profile analytics:**
   ```
   GET https://app.taplio.com/api/v1/analytics/profile
   X-API-KEY: {TAPLIO_API_KEY}
   ```
   Returns: profile views over time, follower growth, search appearances.

3. **Pull audience demographics:**
   ```
   GET https://app.taplio.com/api/v1/analytics/audience
   X-API-KEY: {TAPLIO_API_KEY}
   ```
   Returns: follower breakdown by job title, company size, industry, location.

## Option C: Shield Analytics

1. **Get your Shield API token** from Settings > API.

2. **Pull post performance:**
   ```
   GET https://api.shieldapp.ai/v1/posts?start_date=2026-03-01&end_date=2026-03-30
   Authorization: Bearer {SHIELD_TOKEN}
   ```
   Returns per-post: views, likes, comments, shares, engagement rate, and estimated reach.

3. **Pull profile growth metrics:**
   ```
   GET https://api.shieldapp.ai/v1/profile/stats?period=30d
   Authorization: Bearer {SHIELD_TOKEN}
   ```
   Returns: follower count over time, profile views, post frequency.

## Option D: AuthoredUp

1. AuthoredUp provides a Chrome extension with analytics dashboards. No API access. Use for manual review and content analysis. Best for: identifying top-performing hooks, comparing post formats, and tracking content pillars.

## Option E: Manual LinkedIn Export + n8n

1. **Scrape your own post stats.** From your LinkedIn Activity page, each post shows like/comment counts in the HTML. Use n8n's HTTP Request node to fetch your activity page and parse engagement numbers. This is fragile (HTML changes break it) but works as a fallback.

2. **LinkedIn Creator Analytics (native).** In Creator Mode, LinkedIn shows: impressions, profile views, search appearances, and follower demographics in the Analytics tab. No API for this data -- screenshot or manually record weekly.

## Key Metrics to Track

| Metric | What It Tells You | Good Benchmark |
|--------|-------------------|----------------|
| Impressions | How many people saw the post | 500+ for accounts with <5K followers |
| Engagement rate | (likes + comments + shares) / impressions | 2-5% is good, 5%+ is excellent |
| Profile views | Interest in you as a person (lead signal) | 50+ per week while actively posting |
| Follower growth | Audience building velocity | 50-200 per week with consistent posting |
| DMs received | Strongest lead signal | 1-3 per week = play is working |
| Click-through rate | CTA effectiveness | 1-3% on posts with links |

## Error Handling

- **Taplio/Shield rate limits**: Both throttle to ~60 requests/minute. Batch analytics pulls.
- **LinkedIn API limitations**: Personal profile analytics are severely limited via API. Always pair API access with Taplio or Shield for complete data.
- **Stale data**: LinkedIn updates post metrics with a 12-24 hour delay. Do not pull analytics on same-day posts.
