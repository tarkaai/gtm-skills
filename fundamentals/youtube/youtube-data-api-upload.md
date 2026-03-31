---
name: youtube-data-api-upload
description: Upload a video to YouTube via the Data API v3 resumable upload endpoint
tool: YouTube
product: Data API
difficulty: Config
---

# YouTube Data API v3 — Video Upload

Upload a video file to a YouTube channel programmatically using the resumable upload protocol.

## Authentication

Requires OAuth 2.0 with the `https://www.googleapis.com/auth/youtube.upload` scope. Service accounts work for brand accounts only; personal channels require interactive OAuth consent once to obtain a refresh token.

```
POST https://accounts.google.com/o/oauth2/v2/auth
  ?client_id={CLIENT_ID}
  &redirect_uri=urn:ietf:wg:oauth:2.0:oob
  &response_type=code
  &scope=https://www.googleapis.com/auth/youtube.upload
        https://www.googleapis.com/auth/youtube
```

Exchange the auth code for tokens:

```
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

code={AUTH_CODE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&grant_type=authorization_code
```

Store the `refresh_token` in your secrets manager. Use it to obtain short-lived access tokens:

```
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

refresh_token={REFRESH_TOKEN}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=refresh_token
```

## Resumable Upload (two-step)

### Step 1: Initiate the upload session

```
POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status,contentDetails
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json; charset=UTF-8
X-Upload-Content-Length: {FILE_SIZE_BYTES}
X-Upload-Content-Type: video/mp4

{
  "snippet": {
    "title": "How to Build an AI Agent in 10 Minutes",
    "description": "Step-by-step tutorial showing...",
    "tags": ["ai agent", "tutorial", "automation"],
    "categoryId": "28",
    "defaultLanguage": "en"
  },
  "status": {
    "privacyStatus": "private",
    "selfDeclaredMadeForKids": false,
    "publishAt": "2026-04-05T15:00:00Z"
  }
}
```

Response returns a `Location` header with the upload URI.

### Step 2: Upload the video bytes

```
PUT {UPLOAD_URI}
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: video/mp4
Content-Length: {FILE_SIZE_BYTES}

<binary video data>
```

Response returns the created `video` resource with `id`, `snippet`, `status`, and `contentDetails`.

For files >10MB, chunk uploads in 5MB segments with `Content-Range: bytes {start}-{end}/{total}` headers.

## Quota Cost

- `videos.insert` costs **100 units** per call
- Default daily quota: **10,000 units** (100 uploads/day)
- Request a quota increase via Google Cloud Console if needed

## Error Handling

- `401 Unauthorized`: Refresh the access token using the refresh_token.
- `403 Forbidden`: Check OAuth scopes. Unverified API projects restrict uploads to private only.
- `400 badRequest`: Validate metadata fields. Title max 100 chars, description max 5000 chars, max 500 tags total chars.
- `409 conflict`: Video with this upload URI already exists. Start a new upload session.
- `503 Service Unavailable`: Retry with exponential backoff (1s, 2s, 4s, max 32s).

## Pricing

- YouTube Data API is free (quota-based, not monetary)
- Google Cloud project required (free tier sufficient)
- Pricing page: https://developers.google.com/youtube/v3/getting-started

## Alternatives

- **Descript API** (Enterprise): Programmatic video creation + YouTube export
- **Riverside.fm**: Record and auto-publish to YouTube
- **StreamYard**: Live stream and auto-publish recordings
- **Restream**: Multi-platform publishing including YouTube
- **Zapier/Make**: YouTube upload via no-code connectors
