---
name: youtube-captions-api
description: Upload, update, and manage closed captions and subtitles via YouTube Data API v3
tool: YouTube Data API v3
difficulty: Config
---

# YouTube Data API v3 — Captions

Manage closed captions and subtitles for YouTube videos. Captions improve accessibility, SEO (YouTube indexes caption text for search), and viewer retention (many viewers watch with captions on).

## Authentication

Requires OAuth 2.0 with `https://www.googleapis.com/auth/youtube.force-ssl` scope.

## Core Operations

### List captions for a video (50 units)

```
GET https://www.googleapis.com/youtube/v3/captions
  ?part=snippet
  &videoId={VIDEO_ID}
Authorization: Bearer {ACCESS_TOKEN}
```

Returns `items[].snippet`: `language`, `name`, `status` (serving/syncing/failed), `isDraft`, `isAutoSynced`, `isCC`, `lastUpdated`.

### Upload captions (400 units)

```
POST https://www.googleapis.com/upload/youtube/v3/captions
  ?uploadType=multipart&part=snippet
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: multipart/related; boundary=boundary_string

--boundary_string
Content-Type: application/json

{
  "snippet": {
    "videoId": "{VIDEO_ID}",
    "language": "en",
    "name": "English",
    "isDraft": false
  }
}
--boundary_string
Content-Type: application/octet-stream

WEBVTT

00:00:00.000 --> 00:00:03.500
Welcome to this tutorial on building AI agents.

00:00:03.500 --> 00:00:07.000
Today we'll cover the three core components...

--boundary_string--
```

Supported formats: SRT, SBVTT (WebVTT), Sub Viewer, and TTML.

### Update existing captions (450 units)

```
PUT https://www.googleapis.com/upload/youtube/v3/captions
  ?uploadType=multipart&part=snippet
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: multipart/related; boundary=boundary_string

--boundary_string
Content-Type: application/json

{
  "id": "{CAPTION_TRACK_ID}",
  "snippet": {
    "isDraft": false
  }
}
--boundary_string
Content-Type: application/octet-stream

<updated SRT/VTT content>
--boundary_string--
```

### Download captions (200 units)

```
GET https://www.googleapis.com/youtube/v3/captions/{CAPTION_TRACK_ID}
  ?tfmt=srt
Authorization: Bearer {ACCESS_TOKEN}
```

`tfmt` options: `sbv`, `scc`, `srt`, `ttml`, `vtt`.

### Delete captions (50 units)

```
DELETE https://www.googleapis.com/youtube/v3/captions
  ?id={CAPTION_TRACK_ID}
Authorization: Bearer {ACCESS_TOKEN}
```

## SEO Value of Captions

YouTube auto-generates captions but they contain errors. Uploading corrected captions:
- Makes your video searchable for every word spoken
- Improves watch time (viewers stay longer with accurate captions)
- Enables multi-language subtitles (each language is a new search surface)
- YouTube weighs manually-uploaded captions higher than auto-generated

## Workflow for SEO-Optimized Captions

1. Record and upload video (use `youtube-data-api-upload`)
2. Wait for YouTube's auto-generated captions (usually 1-24 hours)
3. Download auto-captions via this endpoint
4. Correct errors using Descript transcription or manual review
5. Ensure target keywords appear naturally in the corrected transcript
6. Upload the corrected captions back to the video
7. Optionally add translations for additional language markets

## Quota Costs

| Operation | Cost |
|-----------|------|
| `captions.list` | 50 units |
| `captions.insert` | 400 units |
| `captions.update` | 450 units |
| `captions.download` | 200 units |
| `captions.delete` | 50 units |

Caption operations are expensive quota-wise. Budget carefully with the 10,000 unit/day limit.

## Error Handling

- `403 forbidden`: Must be the video owner. Third-party caption management requires explicit permission.
- `404 captionNotFound`: Invalid caption track ID.
- `400 invalidValue`: Check subtitle file format and encoding (must be UTF-8).

## Pricing

- Free (quota-limited)
- Docs: https://developers.google.com/youtube/v3/docs/captions

## Alternatives

- **Descript**: Transcription + editing ($24/mo Creator plan) — export SRT for upload
- **Rev.com**: Professional captioning ($1.50/min) and AI captioning ($0.25/min)
- **Otter.ai**: AI transcription ($8.33/mo) — export SRT
- **Deepgram API**: Speech-to-text API ($0.0043/min) — generate SRT programmatically
- **AssemblyAI**: Transcription API ($0.00025/sec) — SRT/VTT output
