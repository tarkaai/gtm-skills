---
name: tavus-personalized-video
description: Generate personalized AI videos at scale via Tavus record-once-personalize-many API
tool: Tavus
difficulty: Config
---

# Generate Personalized Videos via Tavus API

Use the Tavus API to record a single template video and generate personalized variants for each prospect. Tavus clones the sender's voice and lip-syncs dynamic variables (name, company, signal) into each generated video.

## Prerequisites

- Tavus account with API access (Business plan: $199/mo for 150 video minutes)
- API key from Tavus dashboard
- One recorded template video (the "base video") with placeholder pauses where personalization inserts
- Prospect data with personalization fields

## API Authentication

```
Base URL: https://api.tavus.io/v2
Header: x-api-key: {TAVUS_API_KEY}
Content-Type: application/json
```

## Operations

### 1. Create a personal replica

Train a digital twin from a single 2-minute recording. One-time setup.

```
POST /v2/replicas
{
  "train_video_url": "{url_to_training_video}",
  "replica_name": "{sender_name}-outbound",
  "callback_url": "{your_webhook_url}"
}
```

Response: `{ "replica_id": "r_abc123" }`

Training takes 15-30 minutes. The callback fires when complete.

### 2. Generate a personalized video

```
POST /v2/videos
{
  "replica_id": "r_abc123",
  "script": "Hey {first_name}, this is {sender_name} from {sender_company}. I noticed {company} just {signal}. {value_prop_sentence}. We helped {similar_company} achieve {result}. I'd love to show you how -- there's a link below to grab 15 minutes.",
  "video_name": "{company}-{first_name}-video",
  "background_url": "{prospect_website_screenshot_url}",
  "callback_url": "{your_webhook_url}"
}
```

Response: `{ "video_id": "v_xyz789", "status": "queued" }`

### 3. Retrieve video status and URL

```
GET /v2/videos/{video_id}
```

Response when complete:
```json
{
  "video_id": "v_xyz789",
  "status": "ready",
  "download_url": "https://cdn.tavus.io/videos/v_xyz789.mp4",
  "hosted_url": "https://watch.tavus.io/v_xyz789",
  "thumbnail_url": "https://cdn.tavus.io/thumbnails/v_xyz789.jpg",
  "duration": 58
}
```

Status values: `queued`, `generating`, `ready`, `failed`

Typical generation time: 2-5 minutes per video.

### 4. Batch generation pattern

1. Submit all video generation requests (rate limit: 5 concurrent)
2. Use the `callback_url` webhook to receive completion notifications instead of polling
3. On each callback, download the video URL and map to prospect record
4. For failed videos, retry once with the same parameters

### 5. Error handling

- `429`: Rate limited -- back off per `Retry-After` header
- `400`: Script too long (max 300 words) or invalid replica_id
- `402`: Monthly video minute allocation exhausted
- `500`: Retry with exponential backoff (max 3 retries)

## Credit/Minute Costs

- Business plan: $199/mo for 150 video minutes
- Each 60-second personalized video uses 1 minute of allocation
- Budget for 400 videos/month at 60s each: $199-399/mo (may need Enterprise)

## Tool Alternatives

| Tool | Approach | Pricing | Best For |
|------|----------|---------|----------|
| Tavus | Record-once, personalize-many | $199/mo Business | Natural lip-sync personalization |
| HeyGen | Text-to-avatar | $330/mo Scale | Multilingual, full avatar control |
| Sendspark | Record-once + name insertion | $99/mo Growth | Email-native, simple personalization |
| Synthesia | Text-to-avatar | $89/mo Creator | Enterprise, compliance |
