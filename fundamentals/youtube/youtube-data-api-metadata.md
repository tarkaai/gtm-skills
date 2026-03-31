---
name: youtube-data-api-metadata
description: Read and update video metadata (title, description, tags, thumbnails) via YouTube Data API v3
tool: YouTube
product: Data API
difficulty: Config
---

# YouTube Data API v3 — Video Metadata

Read, search, and update metadata for videos on a YouTube channel. Used for SEO optimization, bulk metadata updates, and competitive research.

## Authentication

Requires OAuth 2.0 with `https://www.googleapis.com/auth/youtube` scope for write operations. Read-only operations on public data can use an API key instead.

## Core Operations

### List videos by channel (1 unit per call)

```
GET https://www.googleapis.com/api/youtube/v3/search
  ?part=snippet
  &channelId={CHANNEL_ID}
  &type=video
  &order=date
  &maxResults=50
  &key={API_KEY}
```

Returns `items[].id.videoId` and `items[].snippet` (title, description, publishedAt, thumbnails).

**Note:** `search.list` costs **100 units**. For listing your own channel's videos, use `playlistItems.list` with the channel's uploads playlist (costs only **1 unit**):

```
GET https://www.googleapis.com/youtube/v3/playlistItems
  ?part=snippet,contentDetails
  &playlistId={UPLOADS_PLAYLIST_ID}
  &maxResults=50
  &key={API_KEY}
```

The uploads playlist ID is `UU` + the channel ID (minus the leading `UC`). E.g., channel `UCabc123` has uploads playlist `UUabc123`.

### Get detailed video metadata (1 unit per call)

```
GET https://www.googleapis.com/youtube/v3/videos
  ?part=snippet,statistics,contentDetails,status,topicDetails
  &id={VIDEO_ID_1},{VIDEO_ID_2}
  &key={API_KEY}
```

Returns per video:
- `snippet`: title, description, tags, categoryId, thumbnails, publishedAt
- `statistics`: viewCount, likeCount, commentCount, favoriteCount
- `contentDetails`: duration, dimension, definition, caption (true/false)
- `status`: privacyStatus, publishAt, embeddable, license
- `topicDetails`: topicCategories (Wikipedia URLs for topic classification)

Batch up to 50 video IDs per request.

### Update video metadata (50 units per call)

```
PUT https://www.googleapis.com/youtube/v3/videos?part=snippet,status
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "id": "{VIDEO_ID}",
  "snippet": {
    "title": "Updated Title with Target Keyword",
    "description": "Updated description with keywords in first 2 lines...",
    "tags": ["keyword1", "keyword2", "long tail keyword"],
    "categoryId": "28"
  },
  "status": {
    "privacyStatus": "public"
  }
}
```

**Critical:** You must include ALL existing snippet fields in the update request. Omitted fields are cleared to defaults.

### Set custom thumbnail (50 units per call)

```
POST https://www.googleapis.com/upload/youtube/v3/thumbnails/set
  ?videoId={VIDEO_ID}
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: image/png

<binary image data>
```

Thumbnail requirements: JPG, GIF, or PNG. Max 2MB. Recommended 1280x720 (16:9 aspect ratio). Channel must be verified to upload custom thumbnails.

### Search YouTube for keyword research (100 units per call)

```
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &q={SEARCH_QUERY}
  &type=video
  &order=viewCount
  &maxResults=25
  &publishedAfter=2025-01-01T00:00:00Z
  &key={API_KEY}
```

Use this to find competitor videos ranking for your target keywords. Combine with `videos.list` to get their view counts and engagement metrics.

## Quota Costs Summary

| Operation | Cost |
|-----------|------|
| `videos.list` | 1 unit |
| `playlistItems.list` | 1 unit |
| `channels.list` | 1 unit |
| `search.list` | 100 units |
| `videos.update` | 50 units |
| `thumbnails.set` | 50 units |
| `videos.insert` | 100 units |

Daily quota: 10,000 units (default).

## Error Handling

- `403 quotaExceeded`: Daily quota exhausted. Wait until midnight PT or request increase.
- `404 videoNotFound`: Verify video ID and that the authenticated account owns the video.
- `400 invalidMetadata`: Check title length (<=100), description length (<=5000), tags total chars (<=500).
- `403 forbidden`: Custom thumbnails require channel verification.

## Pricing

- Free (quota-limited)
- Pricing page: https://developers.google.com/youtube/v3/getting-started

## Alternatives

- **TubeBuddy API**: Bulk metadata optimization, A/B test thumbnails ($2.25-$14.50/mo)
- **vidIQ API**: Keyword scoring, metadata grading ($5.98-$17.50/mo)
- **Phyllo API**: Unified YouTube data access across multiple creator accounts
- **SocialBlade API**: Channel statistics and projections
- **Tubular Labs**: Enterprise video analytics and competitive intelligence
