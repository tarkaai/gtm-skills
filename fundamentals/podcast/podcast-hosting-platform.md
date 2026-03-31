---
name: podcast-hosting-platform
description: Create, configure, and publish podcast episodes via hosting platform APIs (Buzzsprout, Transistor, RSS.com)
tool: Buzzsprout
difficulty: Setup
---

# Podcast Hosting Platform

Upload audio files, set episode metadata, and publish episodes to your podcast hosting platform. The hosting platform generates and maintains your RSS feed, which all podcast directories consume.

## Tool Options

| Tool | API | Best For |
|------|-----|----------|
| Buzzsprout | REST API (`api.buzzsprout.com/v1`) | Simplest API, auto-transcription, built-in website |
| Transistor | REST API (`api.transistor.fm/v1`) | Multiple shows per account, private podcasts, analytics API |
| RSS.com | REST API (`api.rss.com/v1`) | Cheapest paid option, AI transcription |
| Podbean | REST API (`api.podbean.com/v1`) | Monetization features, live streaming |
| Spotify for Podcasters | Web dashboard (limited API) | Free hosting, direct Spotify integration |

## Buzzsprout API (Primary)

### Authentication
```
Header: Authorization: Token token={BUZZSPROUT_API_KEY}
Base URL: https://www.buzzsprout.com/api/{PODCAST_ID}
```

Free tier: 2 hours/month upload. Paid: $12/mo for 3 hours, $18/mo for 6 hours, $24/mo for 12 hours.

### Create a new episode

```http
POST https://www.buzzsprout.com/api/{PODCAST_ID}/episodes.json
Authorization: Token token={BUZZSPROUT_API_KEY}
Content-Type: application/json

{
  "title": "Episode Title",
  "description": "<p>Episode description with HTML formatting.</p>",
  "summary": "Short plain-text summary for podcast apps.",
  "artist": "Host Name",
  "tags": "b2b,saas,growth",
  "published_at": "2026-04-15T09:00:00-04:00",
  "duration": 1845,
  "season_number": 1,
  "episode_number": 5,
  "explicit": false,
  "private": false,
  "audio_url": "https://storage.example.com/episode-5.mp3"
}
```

Key fields:
- `published_at`: Set to future datetime for scheduled publishing. Omit to publish immediately.
- `audio_url`: URL to the MP3 file. Buzzsprout downloads it from this URL. Alternatively, upload via multipart form.
- `private`: Set `true` for draft episodes not yet ready to publish.

### Upload audio file directly

```http
POST https://www.buzzsprout.com/api/{PODCAST_ID}/episodes.json
Authorization: Token token={BUZZSPROUT_API_KEY}
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="audio_file"; filename="episode-5.mp3"
Content-Type: audio/mpeg

{binary audio data}
--boundary
Content-Disposition: form-data; name="title"

Episode Title
--boundary--
```

### List episodes

```http
GET https://www.buzzsprout.com/api/{PODCAST_ID}/episodes.json
Authorization: Token token={BUZZSPROUT_API_KEY}
```

Returns array of episode objects with: `id`, `title`, `audio_url`, `total_plays`, `published_at`.

### Update episode metadata

```http
PUT https://www.buzzsprout.com/api/{PODCAST_ID}/episodes/{EPISODE_ID}.json
Authorization: Token token={BUZZSPROUT_API_KEY}
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "<p>Updated description.</p>",
  "published_at": "2026-04-16T09:00:00-04:00"
}
```

### Get episode stats

```http
GET https://www.buzzsprout.com/api/{PODCAST_ID}/episodes/{EPISODE_ID}/stats.json
Authorization: Token token={BUZZSPROUT_API_KEY}
```

Returns: `total_plays`, `plays_by_day` (array), `plays_by_source` (Apple Podcasts, Spotify, etc.).

## Transistor API

### Authentication
```
Header: x-api-key: {TRANSISTOR_API_KEY}
Base URL: https://api.transistor.fm/v1
```

Pricing: $19/mo (unlimited shows, 20K downloads), $49/mo (unlimited shows, 100K downloads).

### Create episode

```http
POST https://api.transistor.fm/v1/episodes
x-api-key: {TRANSISTOR_API_KEY}
Content-Type: application/json

{
  "episode": {
    "show_id": "{SHOW_ID}",
    "title": "Episode Title",
    "summary": "Short summary.",
    "description": "<p>Full description.</p>",
    "media_url": "https://storage.example.com/episode-5.mp3",
    "season": 1,
    "number": 5,
    "type": "full",
    "status": "published",
    "published_at": "2026-04-15T09:00:00Z"
  }
}
```

### Publish a draft episode

```http
PATCH https://api.transistor.fm/v1/episodes/{EPISODE_ID}/publish
x-api-key: {TRANSISTOR_API_KEY}
Content-Type: application/json

{
  "episode": {
    "status": "published"
  }
}
```

### Get analytics

```http
GET https://api.transistor.fm/v1/analytics/{SHOW_ID}?start_date=2026-04-01&end_date=2026-04-30
x-api-key: {TRANSISTOR_API_KEY}
```

Returns: downloads per episode, downloads by day, listener geography, listening app breakdown.

## RSS Feed Setup

After creating your first episode, the hosting platform generates an RSS feed URL:
- Buzzsprout: `https://feeds.buzzsprout.com/{PODCAST_ID}.rss`
- Transistor: `https://feeds.transistor.fm/{SHOW_SLUG}`

This RSS feed is what you submit to Apple Podcasts, Spotify, and other directories. See the `podcast-rss-distribution` fundamental for directory submission.

## Show Configuration Checklist

Before publishing your first episode, configure the show-level settings:
1. **Show title**: Your podcast name
2. **Show description**: What the podcast is about, who it is for (used by directories for search)
3. **Cover art**: 3000x3000px square JPEG or PNG (required by Apple Podcasts)
4. **Category**: Select 1-3 iTunes categories (Business > Entrepreneurship, Technology, etc.)
5. **Language**: en (English)
6. **Author**: Host/company name
7. **Owner email**: Email for directory communications (usually the host or a shared inbox)
8. **Website URL**: Landing page for the podcast (with UTM tracking)
9. **Explicit rating**: yes/no (affects directory listing)

## Error Handling

- **Upload fails (413)**: Audio file too large. Compress to 128kbps MP3. Target <100MB per episode.
- **Scheduled publish doesn't fire**: Verify timezone in `published_at`. Buzzsprout uses Eastern time by default.
- **RSS feed not updating**: Force a cache refresh by making any metadata change on the latest episode. Directories poll RSS feeds every 1-24 hours.
- **Audio quality issues**: Record at 44.1kHz/16-bit WAV, then export to 128kbps mono MP3 for upload. Hosting platforms do not re-encode.
