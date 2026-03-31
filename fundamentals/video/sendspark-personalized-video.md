---
name: sendspark-personalized-video
description: Generate personalized prospect videos at scale via Sendspark API with dynamic name/company insertion
tool: Sendspark
difficulty: Config
---

# Generate Personalized Videos via Sendspark API

Use the Sendspark API to record a single template video and automatically personalize it for each prospect by inserting their name (via voice cloning), company logo, and website as the background. Sendspark is purpose-built for sales video prospecting at scale.

## Prerequisites

- Sendspark Growth account ($99/mo) or Team ($299/mo) for API access
- API key from Sendspark dashboard > Integrations > API
- One recorded template video with a placeholder for the prospect's name
- Prospect data: first_name, company, website URL

## API Authentication

```
Base URL: https://api.sendspark.com/v1
Header: Authorization: Bearer {SENDSPARK_API_KEY}
Content-Type: application/json
```

## Operations

### 1. Record a template video

Record a single video (60-90 seconds) where you say "[First Name]" as a placeholder. Sendspark's voice cloning replaces this with each prospect's actual name using the sender's cloned voice.

```
POST /v1/videos/templates
{
  "video_url": "{url_to_recorded_template}",
  "template_name": "{campaign_slug}-template",
  "personalization_type": "name_swap",
  "dynamic_background": true
}
```

Response: `{ "template_id": "t_abc123" }`

### 2. Generate a personalized video

```
POST /v1/videos/personalize
{
  "template_id": "t_abc123",
  "recipient": {
    "first_name": "{first_name}",
    "last_name": "{last_name}",
    "email": "{email}",
    "company": "{company}",
    "website_url": "{prospect_website_url}"
  },
  "cta": {
    "text": "Book 15 Minutes",
    "url": "{cal_com_link}?utm_source=sendspark&utm_campaign={campaign_slug}"
  },
  "callback_url": "{your_webhook_url}"
}
```

Response:
```json
{
  "video_id": "v_xyz789",
  "status": "processing",
  "share_url": "https://share.sendspark.com/v_xyz789",
  "gif_thumbnail_url": "https://cdn.sendspark.com/gif/v_xyz789.gif"
}
```

### 3. Retrieve video status

```
GET /v1/videos/{video_id}
```

Response when complete:
```json
{
  "video_id": "v_xyz789",
  "status": "ready",
  "share_url": "https://share.sendspark.com/v_xyz789",
  "gif_thumbnail_url": "https://cdn.sendspark.com/gif/v_xyz789.gif",
  "mp4_url": "https://cdn.sendspark.com/video/v_xyz789.mp4",
  "duration": 63,
  "views": 0,
  "watch_rate": null
}
```

### 4. Get video analytics

```
GET /v1/videos/{video_id}/analytics
```

Response:
```json
{
  "views": 3,
  "unique_views": 2,
  "average_watch_percentage": 72,
  "cta_clicks": 1,
  "viewer_emails": ["jane@acme.com"]
}
```

### 5. Batch generation pattern

Sendspark supports CSV bulk upload via API:

```
POST /v1/videos/bulk-personalize
{
  "template_id": "t_abc123",
  "recipients_csv_url": "{url_to_prospect_csv}",
  "cta": {
    "text": "Book 15 Minutes",
    "url": "{cal_com_link}"
  },
  "callback_url": "{your_webhook_url}"
}
```

This generates personalized videos for all rows in the CSV. The callback fires per-video as each completes.

### 6. Error handling

- `429`: Rate limited -- wait and retry
- `400`: Invalid template_id or missing required recipient fields
- `402`: Video credit limit reached
- `500`: Retry with exponential backoff

## Pricing

- Growth: $99/mo (3 seats, 20K videos, API access)
- Team: $299/mo (10 seats, 100K videos, advanced integrations)
- Budget for 400 videos/month: $99/mo on Growth plan

## Tool Alternatives

| Tool | Approach | Pricing | Best For |
|------|----------|---------|----------|
| Sendspark | Name-swap + dynamic background | $99/mo Growth | Email-native, highest volume per dollar |
| Tavus | Full lip-sync personalization | $199/mo Business | Most natural personalization |
| HeyGen | Text-to-avatar generation | $330/mo Scale | Multilingual, custom scripts per prospect |
| Loom | Manual recording per prospect | $12.50/mo Business | Low volume, founder authenticity |
