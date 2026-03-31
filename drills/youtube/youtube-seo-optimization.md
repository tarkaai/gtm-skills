---
name: youtube-seo-optimization
description: Audit and optimize existing YouTube video metadata, thumbnails, and captions for improved search ranking
category: YouTube
tools:
  - YouTube Data API v3
  - vidIQ
  - TubeBuddy
fundamentals:
  - youtube-data-api-metadata
  - youtube-search-seo
  - youtube-analytics-api
  - youtube-captions-api
---

# YouTube SEO Optimization

Audit existing videos on your YouTube channel and optimize their metadata for better search rankings and click-through rates. This drill is for improving videos already published — it finds underperforming videos with fixable SEO issues and applies corrections.

## Input

- YouTube channel with OAuth credentials (write access)
- YouTube Analytics data (at least 30 days of data per video)
- The keyword matrix from `youtube-keyword-research` drill

## Steps

### 1. Pull full video inventory

Using `youtube-data-api-metadata`, list all videos on the channel via the uploads playlist:

```
GET /youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={UPLOADS_PLAYLIST_ID}&maxResults=50
```

Paginate through all results. For each video, fetch detailed metadata:

```
GET /youtube/v3/videos?part=snippet,statistics,contentDetails&id={VIDEO_IDS}
```

Build a dataset: video_id, title, description, tags, published_date, view_count, like_count, comment_count, duration, has_captions.

### 2. Pull search performance per video

Using `youtube-analytics-api`, for each video get:

- Total impressions (how often the video appeared in search/browse)
- Click-through rate (impressions that turned into views)
- Average view duration and average view percentage
- Traffic source breakdown (what % comes from YT_SEARCH vs SUGGESTED vs BROWSE)
- Top search terms driving traffic to this specific video

### 3. Score each video's SEO health

For each video, compute an SEO score (0-100):

| Factor | Weight | Scoring |
|--------|--------|---------|
| Title contains target keyword | 20 | 20 if exact match in first 60 chars, 10 if partial, 0 if absent |
| Description first 2 lines contain keyword | 15 | 15 if present, 0 if absent |
| Tags include target + related keywords | 10 | 10 if >=5 relevant tags, 5 if 1-4, 0 if none |
| Custom thumbnail set | 10 | 10 if yes, 0 if auto-generated |
| Captions uploaded (not auto-generated) | 10 | 10 if manual captions, 0 if only auto |
| Description length >= 500 chars | 5 | 5 if yes, 0 if no |
| Description has timestamps/chapters | 5 | 5 if yes, 0 if no |
| CTR >= 5% | 10 | 10 if >=5%, 5 if 3-5%, 0 if <3% |
| Avg view percentage >= 50% | 15 | 15 if >=50%, 8 if 30-50%, 0 if <30% |

Videos scoring <60 are optimization candidates. Sort by `views * (100 - seo_score)` to prioritize high-traffic videos with the most room for improvement.

### 4. Optimize titles

For each optimization candidate:

1. Check if the video's actual search terms (from analytics) match the current title
2. If the top search term driving traffic differs from the title keyword, consider retitling to match actual demand
3. Apply title formula: `{Target Keyword} — {Benefit or Unique Angle} [{Year}]`
4. Keep under 60 characters for full display in search results
5. Front-load the keyword (YouTube weighs the first words more heavily)

Using `youtube-data-api-metadata`, update:
```
PUT /youtube/v3/videos?part=snippet
{
  "id": "{VIDEO_ID}",
  "snippet": {
    "title": "{optimized title}",
    "description": "{existing description}",
    "tags": ["{existing tags}"],
    "categoryId": "{existing category}"
  }
}
```

### 5. Optimize descriptions

For each candidate:

1. Rewrite the first 2 lines to include the target keyword and a compelling hook (these show in search results before "Show more")
2. Add timestamps/chapters if missing (YouTube creates chapter markers from timestamps in descriptions)
3. Include 3-5 related keywords naturally in the body text
4. Add a CTA with link to website landing page
5. Ensure total description is >= 500 characters

### 6. Optimize tags

For each candidate:

1. Pull the target keyword and related keywords from the keyword matrix
2. Add tags in priority order: exact target keyword, variations, related terms, broad category
3. Stay under the 500-character total limit
4. Remove irrelevant or overly broad tags

### 7. Fix captions

For videos with only auto-generated captions:

1. Using `youtube-captions-api`, download the auto-generated SRT
2. Correct errors, especially for product names, technical terms, and branded words that auto-captions consistently get wrong
3. Ensure target keywords appear correctly in the transcript
4. Upload the corrected SRT track

### 8. Flag thumbnail issues

For videos with CTR < 3%:

1. Check if the video has a custom thumbnail (auto-generated thumbnails consistently underperform)
2. If custom thumbnail exists but CTR is still low, flag for redesign with guidance:
   - Use contrasting colors (not blue/red like YouTube's UI)
   - Include readable text (3-5 words max)
   - Show a human face with clear emotion
   - Create visual consistency across the channel

**Human action required:** Design or approve new thumbnails for flagged videos.

### 9. Document changes and measure impact

For each optimized video, log:
- Video ID, old title, new title
- Changes made (title, description, tags, captions)
- Date of change
- Views/day before change (7-day average)
- Measure views/day after change (check after 14 days)

A successful optimization typically shows a 20-50% increase in search traffic within 2-4 weeks.

## Output

- SEO score audit for all channel videos
- Prioritized optimization queue
- Updated metadata for each optimized video
- Corrected captions uploaded
- Change log with before/after metrics for impact measurement

## Triggers

- Run once at play start to audit and fix all existing videos
- Run monthly to audit new videos and catch any that were published without full optimization
- Run on-demand when a video's search traffic declines
