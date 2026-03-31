---
name: youtube-search-seo
description: Research YouTube search keywords and analyze competitor video SEO using the Data API and third-party tools
tool: YouTube
product: Data API
difficulty: Config
---

# YouTube Search and SEO Research

Use the YouTube Data API and third-party tools to discover what your ICP is searching for on YouTube, analyze competitor video optimization, and identify keyword opportunities.

## Authentication

Public search and video data requires only an API key. No OAuth needed for read-only operations on public content.

## Core Operations

### YouTube Autocomplete (free, no quota)

YouTube's search suggest endpoint returns what users are actively searching for. This is the closest thing to a free keyword research tool:

```
GET https://suggestqueries-clients6.youtube.com/complete/search
  ?client=youtube
  &hl=en
  &gl=us
  &ds=yt
  &q={SEED_KEYWORD}
```

Response is JSONP. Parse the second element for suggestion strings. Example seed: "how to build ai agent" returns suggestions like "how to build ai agent from scratch", "how to build ai agent python", etc.

Run this for 10-20 seed keywords from your ICP pain points. Each suggestion is a validated search query real people type.

### Search for competitor videos (100 units per call)

```
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &q={TARGET_KEYWORD}
  &type=video
  &order=relevance
  &maxResults=10
  &key={API_KEY}
```

Then fetch full stats for the top results:

```
GET https://www.googleapis.com/youtube/v3/videos
  ?part=snippet,statistics,contentDetails
  &id={VIDEO_ID_1},{VIDEO_ID_2},...
  &key={API_KEY}
```

### Analyze competitor video SEO signals

For each top-ranking video, extract:

1. **Title**: Does it contain the exact search query? Where in the title?
2. **Description**: First 2 lines (visible before "Show more"). Does it contain the keyword?
3. **Tags**: Use `snippet.tags` array. What keywords are they targeting?
4. **Duration**: `contentDetails.duration` in ISO 8601. What's the average length of top results?
5. **View count**: `statistics.viewCount`. Minimum views to compete?
6. **Engagement ratio**: `(likeCount + commentCount) / viewCount`. Higher = better audience match.
7. **Channel size**: Fetch `channels.list` for each uploader to get subscriber count. Are small channels ranking?
8. **Publish date**: How old are top results? Stale results = opportunity for fresh content.

### Channel keyword research

Find what topics a competitor channel covers:

```
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &channelId={COMPETITOR_CHANNEL_ID}
  &type=video
  &order=viewCount
  &maxResults=50
  &key={API_KEY}
```

Their most-viewed videos reveal which topics have demand in your niche.

## Third-Party YouTube SEO Tools

### vidIQ

- **Keyword Score**: Proprietary metric combining search volume, competition, and channel strength
- **Competitor tracking**: Track ranking positions for specific keywords
- **SEO score**: Grades your video's optimization (title, description, tags, thumbnail)
- Browser extension provides real-time data overlay on YouTube
- API access on higher-tier plans
- Pricing: Pro $5.98/mo, Boost $17.50/mo (annual)
- https://vidiq.com

### TubeBuddy

- **Keyword Explorer**: Search volume, competition, optimization strength
- **SEO Studio**: Step-by-step optimization checklist per video
- **A/B Testing**: Test thumbnails and titles on live videos
- **Bulk Processing**: Update tags, cards, end screens across multiple videos
- Browser extension + mobile app
- Pricing: Pro $2.25/mo, Legend $14.50/mo (annual)
- https://tubebuddy.com

### Ahrefs YouTube Keyword Tool

Use `ahrefs-keyword-research` fundamental with YouTube-specific filters:

```
GET https://api.ahrefs.com/v3/keywords-explorer/youtube/keyword-ideas
  ?keywords=ai+agent+tutorial
  &select=keyword,volume,clicks,global_volume
  &where=volume>100
  &order_by=volume:desc
  &limit=100
Authorization: Bearer {AHREFS_TOKEN}
```

Ahrefs provides YouTube-specific search volume (not just Google). Pricing: $99-$999/mo.

## YouTube SEO Ranking Factors (2026)

Priority order for optimization:

1. **Watch time and retention**: Videos that keep viewers watching rank higher. Target >50% average view percentage.
2. **Click-through rate (CTR)**: Thumbnail + title drive clicks from search results. Target >5% CTR.
3. **Keyword relevance**: Title, description first 2 lines, tags, and spoken words in captions.
4. **Engagement**: Likes, comments, shares, and "save to playlist" signals.
5. **Upload recency**: Fresher content gets a temporary boost in search results.
6. **Channel authority**: Channels with consistent upload schedules and topical focus rank better.

## Error Handling

- `403 quotaExceeded`: YouTube autocomplete has no quota limit. Switch to autocomplete for keyword discovery when API quota runs low.
- `400 badRequest`: URL-encode search queries. Special characters cause 400 errors.

## Pricing

- YouTube Data API: Free (10,000 units/day)
- vidIQ: $5.98-$17.50/mo
- TubeBuddy: $2.25-$14.50/mo
- Ahrefs (YouTube keywords): $99-$999/mo

## Alternatives

- **Keywords Everywhere** ($1/1000 credits): YouTube keyword volume in browser
- **Morningfame** (invite-only): YouTube analytics + keyword research
- **Semrush** ($129.95/mo+): YouTube keyword research module
- **Google Trends** (free): Compare relative search interest over time (filter to YouTube Search)
- **AnswerThePublic** (free tier): Visualize questions people ask around a topic
