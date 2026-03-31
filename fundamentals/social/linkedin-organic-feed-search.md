---
name: linkedin-organic-feed-search
description: Search and browse LinkedIn feeds to find ICP-relevant posts worth commenting on
tool: LinkedIn
product: LinkedIn Organic
difficulty: Config
---

# Search LinkedIn Feeds for Commentable Posts

## Prerequisites
- LinkedIn account (Premium or Sales Navigator recommended for search filters)
- Defined ICP with target titles, companies, and topics
- Optional: Taplio or Shield for advanced feed monitoring

## Why This Matters

The comment-to-DM motion depends on finding the RIGHT posts to comment on. Commenting on random popular posts wastes time. You need posts by or engaging your ICP prospects where your comment will be seen by the person you want to DM later.

## Steps

### 1. LinkedIn Search API (via Sales Navigator)

Sales Navigator provides the most powerful search for finding prospect posts.

**Search for posts by ICP prospects:**
```
Navigate to Sales Navigator > Search > Posted on LinkedIn
Filters:
  - Title: {target titles from ICP, e.g., "VP Engineering", "CTO", "Head of DevOps"}
  - Company headcount: {your ICP range, e.g., 11-50, 51-200}
  - Industry: {target industries}
  - Posted in: Last 7 days
  - Keywords: {pain points your product solves}
```

Sales Navigator does not have a public API for post search. Use the UI to find posts, then record the post URLs and author profile URLs for your engagement list.

### 2. LinkedIn Native Feed + Hashtag Search

**Search by hashtag:**
```
URL: https://www.linkedin.com/feed/hashtag/{hashtag_name}
```
Browse posts tagged with hashtags relevant to your domain. Filter mentally for posts by people matching your ICP.

**Search by keyword:**
```
URL: https://www.linkedin.com/search/results/content/?keywords={encoded_keywords}
```
LinkedIn content search returns recent posts containing your keywords. Sort by "Top" for high-engagement posts or "Latest" for recency.

### 3. Taplio Feed Monitoring

Taplio provides a "CRM" feature that lets you track specific LinkedIn profiles and see their posts.

**Add prospects to Taplio CRM:**
```
POST https://app.taplio.com/api/v1/crm/contacts
X-API-KEY: {TAPLIO_API_KEY}
Content-Type: application/json

{
  "linkedin_url": "https://www.linkedin.com/in/{handle}",
  "tags": ["icp-prospect", "comment-target"]
}
```

**Pull recent posts from tracked profiles:**
```
GET https://app.taplio.com/api/v1/crm/contacts/{contact_id}/posts
X-API-KEY: {TAPLIO_API_KEY}
```
Returns their recent LinkedIn posts. Filter for posts with 10+ likes (enough engagement to make your comment visible) and topics relevant to your domain.

### 4. Shield Analytics for Competitor/Peer Monitoring

Track competitor founders or industry peers whose audience overlaps your ICP.

```
GET https://api.shieldapp.ai/v1/tracked-profiles/{profile_id}/posts?period=7d
Authorization: Bearer {SHIELD_TOKEN}
```
Returns their recent posts. Comment on these to get exposure to their audience, which contains your ICP.

### 5. LinkedIn Notifications + Activity Feed (Manual)

For a zero-cost approach:
1. Turn on LinkedIn notifications for 20-30 ICP prospects (click the bell on their profile)
2. LinkedIn notifies you when they post
3. Check your LinkedIn notifications tab daily for new posts from tracked prospects
4. This is free and reliable but requires manual checking

### 6. n8n Automated Feed Aggregation

Build an n8n workflow that aggregates commentable posts:

1. **Trigger**: Daily cron at 8am
2. **Fetch from Taplio**: Pull new posts from CRM-tracked prospects
3. **Fetch from Shield**: Pull new posts from tracked peer/competitor accounts
4. **Filter**: Remove posts older than 48 hours (stale), posts with 0 comments (too early), posts with 100+ comments (your comment gets buried)
5. **Score**: Rank by relevance to your ICP topics + author match to ICP
6. **Output**: Send top 10 posts to Slack or email as your daily comment queue

## Key Selection Criteria

| Factor | Good Target | Bad Target |
|--------|------------|------------|
| Author | ICP prospect, peer, or influencer with ICP audience | Random viral poster, news aggregator |
| Post age | 1-24 hours old | 3+ days old |
| Comment count | 5-50 comments | 0 (too early) or 200+ (buried) |
| Topic | Related to problems you solve | Unrelated to your domain |
| Engagement | Author replies to comments | Author never replies |

## Error Handling

- **LinkedIn search rate limits**: LinkedIn throttles search after ~100 searches per day. Space your searches and cache results.
- **Sales Navigator session limits**: SN can flag automated access. Always use the browser UI, not scrapers.
- **Taplio API limits**: 60 requests/minute. Batch fetches.
- **Stale posts**: Posts older than 48 hours get minimal new engagement. Prioritize fresh posts.
