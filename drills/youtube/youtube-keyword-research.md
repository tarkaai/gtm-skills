---
name: youtube-keyword-research
description: Research YouTube search demand, analyze competitor videos, and build a keyword-driven content calendar
category: YouTube
tools:
  - YouTube Data API v3
  - Ahrefs
  - vidIQ
  - TubeBuddy
fundamentals:
  - youtube-search-seo
  - youtube-data-api-metadata
  - ahrefs-keyword-research
---

# YouTube Keyword Research

This drill produces a ranked list of YouTube video topics backed by search demand data, competitive analysis, and a publishing calendar. Each row in the output becomes one video to produce.

## Input

- Your ICP definition: who you serve, what problems they have, what they search for
- 10-20 seed keywords from your product domain (e.g., "crm setup", "cold email automation", "sales pipeline")
- Your YouTube channel ID (or "new channel" if starting fresh)

## Steps

### 1. Mine YouTube autocomplete for real search queries

For each seed keyword, query the YouTube autocomplete endpoint:

```
GET https://suggestqueries-clients6.youtube.com/complete/search
  ?client=youtube&hl=en&gl=us&ds=yt&q={SEED}
```

Collect all suggestions. Then run a second pass: append each letter a-z to the seed ("crm a", "crm b", ...) and collect those suggestions too. This alphabet-soup method expands coverage.

Target output: 200-500 raw keyword suggestions from 10-20 seeds.

### 2. Validate search volume

Batch the raw keywords through Ahrefs YouTube keyword metrics (if available) or vidIQ keyword scores:

**Ahrefs:**
```
POST https://api.ahrefs.com/v3/keywords-explorer/youtube/keywords-metrics
Authorization: Bearer {AHREFS_TOKEN}
Content-Type: application/json

{
  "keywords": ["how to set up crm", "crm for startups", ...],
  "select": ["keyword", "volume", "clicks", "global_volume"]
}
```

**vidIQ/TubeBuddy:** Use browser extension to manually check high-potential keywords if API unavailable.

Filter: keep keywords with volume >= 50/month (or vidIQ score >= 40). Discard the rest.

### 3. Analyze competition for each keyword

For each surviving keyword, use `youtube-search-seo` to search YouTube and pull the top 5 results:

For each top-ranking video, record:
- View count (from `statistics.viewCount`)
- Channel subscriber count (from `channels.list`)
- Video age (days since `snippet.publishedAt`)
- Title keyword placement (exact match, partial match, or absent)
- Video duration
- Like-to-view ratio

Score competition:
- **Low**: Top results have <50K views, small channels (<10K subs), or videos are >1 year old
- **Medium**: Top results have 50K-500K views, mid-size channels
- **High**: Top results have >500K views, large channels (>100K subs), fresh content

Prioritize Low and Medium competition keywords.

### 4. Build the keyword matrix

Create a structured dataset with one row per video topic:

| Field | Source |
|-------|--------|
| target_keyword | Autocomplete + validation |
| search_volume | Ahrefs/vidIQ |
| competition | Step 3 analysis |
| priority_score | `volume * (3 - competition_level)` |
| video_title | Optimized title with keyword in first 60 chars |
| content_angle | What unique perspective you bring vs existing videos |
| target_duration | Based on top-ranking video average |
| cta | What action viewers should take |
| related_keywords | 3-5 related terms to mention in the video |
| publish_week | Scheduled week number |

### 5. Build the content calendar

Sort by priority_score descending. Assign to weekly publish slots:

- **Week 1-4**: Top 4 keywords (highest priority, prove the channel concept)
- **Week 5-8**: Next 4 keywords (expand topic coverage)
- **Ongoing**: 1-2 videos per week from remaining keywords

Group related keywords into "series" — viewers who watch one video in a series are likely to watch the next, boosting session time and recommendations.

## Output

- Keyword matrix (JSON or CSV): 50-200 validated video topics ranked by priority
- Content calendar: 8-12 weeks of planned videos with titles and target keywords
- Competition brief: for each target keyword, the top 3 existing videos and their weaknesses

## Triggers

- Run once at play start to build the initial calendar
- Re-run monthly to discover new keyword opportunities
- Re-run after each video to refine based on actual performance data from `youtube-analytics-api`
