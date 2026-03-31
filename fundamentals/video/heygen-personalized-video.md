---
name: heygen-personalized-video
description: Generate personalized AI avatar videos at scale via HeyGen API
tool: HeyGen
difficulty: Config
---

# Generate Personalized AI Avatar Videos via HeyGen API

Use the HeyGen API to programmatically generate personalized videos featuring an AI avatar of the founder/sender. Each video is customized per prospect with dynamic variables (name, company, pain point) without re-recording.

## Prerequisites

- HeyGen account with API access (Scale plan: $330/mo for volume, or Pro API: $99/mo)
- API key from HeyGen dashboard > API Settings
- A trained personal avatar (upload a 2-minute training video of the sender speaking naturally)
- Prospect data with personalization fields: first_name, company, signal, pain_point

## API Authentication

```
Base URL: https://api.heygen.com/v2
Header: X-Api-Key: {HEYGEN_API_KEY}
Content-Type: application/json
```

## Operations

### 1. Create a personal avatar

Train a digital twin of the founder/sender. This is a one-time setup.

```
POST /v2/video/avatar
{
  "training_video_url": "{url_to_2min_training_video}",
  "avatar_name": "{sender_name}-outbound"
}
```

Response includes `avatar_id`. Save this -- it is used in all video generation requests.

Training requirements:
- 2-5 minute video of the person speaking naturally to camera
- Good lighting, neutral background
- Clear audio, no background noise
- Multiple facial expressions and head movements for natural output

### 2. Generate a personalized video

```
POST /v2/video/generate
{
  "video_inputs": [
    {
      "character": {
        "type": "avatar",
        "avatar_id": "{avatar_id}",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "text",
        "input_text": "Hey {first_name}, this is {sender_name} from {sender_company}. I noticed {company} just {signal}. {value_prop_sentence}. We helped {similar_company} achieve {result}. I'd love to show you how -- there's a link below to grab 15 minutes.",
        "voice_id": "{cloned_voice_id}"
      },
      "background": {
        "type": "url",
        "value": "{prospect_website_screenshot_url}"
      }
    }
  ],
  "dimension": {
    "width": 1280,
    "height": 720
  }
}
```

Response:
```json
{
  "data": {
    "video_id": "abc123"
  }
}
```

### 3. Poll for video completion

```
GET /v2/video/{video_id}
```

Response when complete:
```json
{
  "data": {
    "status": "completed",
    "video_url": "https://resource.heygen.com/video/abc123.mp4",
    "thumbnail_url": "https://resource.heygen.com/thumbnail/abc123.jpg",
    "duration": 62
  }
}
```

Status values: `pending`, `processing`, `completed`, `failed`

Typical generation time: 1-3 minutes per video.

### 4. Batch generation pattern

For generating 50+ videos in a batch:

1. Submit all generation requests in parallel (rate limit: 10 concurrent)
2. Collect all `video_id` values
3. Poll status every 30 seconds for the batch
4. As each completes, download the video URL and thumbnail
5. Map each video_id back to the prospect record

### 5. Error handling

- `429 Too Many Requests`: Back off and retry after the `Retry-After` header value
- `400 Bad Request`: Usually malformed script text -- check for special characters
- `402 Payment Required`: Credit balance exhausted -- top up via dashboard
- `500 Internal Server Error`: Retry up to 3 times with exponential backoff

## Credit Costs

- Scale plan: $0.50/credit; a 60-second video costs ~1 credit
- Pro plan: $0.99/credit
- Budget for 400 videos/month: ~$200-400/mo on Scale plan

## Tool Alternatives

| Tool | API | Pricing | Best For |
|------|-----|---------|----------|
| HeyGen | REST API | $330/mo Scale plan | High quality avatars, multilingual |
| Tavus | REST API | $199/mo Business | Record-once-personalize-many |
| Sendspark | REST API | $99/mo Growth | Email-native video, CRM integrations |
| Synthesia | REST API | $89/mo Creator (API) | Enterprise, training videos |
| Colossyan | REST API | Custom | Enterprise compliance |
