---
name: google-ads-youtube-creative
description: Create and manage YouTube video ad creatives (skippable in-stream, bumper, companion banners) via Google Ads API
tool: Google Ads
difficulty: Config
---

# Google Ads YouTube Creative

Upload video assets, create video ads with companion banners, and manage creative variants for YouTube pre-roll campaigns.

## Prerequisites

- Google Ads Video campaign and ad groups created (see `google-ads-youtube-video-campaign`)
- Video(s) uploaded to YouTube (Public or Unlisted)
- Companion banner image (300x60px for desktop) prepared
- Google Ads API access with OAuth 2.0

## Core Operations

### Link a YouTube video as an asset

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/assets:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "youtubeVideoAsset": {
        "youtubeVideoId": "YOUR_VIDEO_ID",
        "youtubeVideoTitle": "Stop Wasting 20 Hours a Week on Broken Data Pipelines"
      }
    }
  }]
}
```

### Upload a companion banner image

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/assets:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "imageAsset": {
        "data": "{BASE64_ENCODED_IMAGE}",
        "fileSize": 15000,
        "mimeType": "IMAGE_PNG",
        "fullSizeInfo": {
          "heightPixels": 60,
          "widthPixels": 300
        }
      },
      "name": "Companion Banner - Data Pipeline Guide"
    }
  }]
}
```

### Create a skippable in-stream ad (pre-roll)

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupAds:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "status": "PAUSED",
      "ad": {
        "name": "Preroll - Stat Hook - Data Pipeline",
        "videoAd": {
          "video": {
            "asset": "customers/{CUSTOMER_ID}/assets/{VIDEO_ASSET_ID}"
          },
          "inStream": {
            "actionButtonLabel": "Get the Guide",
            "actionHeadline": "Free Data Pipeline Checklist — 50+ Teams Use It",
            "companionBanner": {
              "asset": "customers/{CUSTOMER_ID}/assets/{BANNER_ASSET_ID}"
            }
          }
        },
        "finalUrls": ["https://example.com/guide?utm_source=youtube&utm_medium=preroll&utm_campaign=problem-aware&utm_content=stat-hook"]
      }
    }
  }]
}
```

### Create a bumper ad (6 seconds, non-skippable)

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupAds:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "status": "PAUSED",
      "ad": {
        "videoAd": {
          "video": {
            "asset": "customers/{CUSTOMER_ID}/assets/{BUMPER_VIDEO_ASSET_ID}"
          },
          "bumper": {}
        },
        "finalUrls": ["https://example.com/guide?utm_source=youtube&utm_medium=bumper"]
      }
    }
  }]
}
```

Bumper ads MUST be 6 seconds or shorter. Use for retargeting or brand reinforcement.

### Create a non-skippable in-stream ad (15 seconds)

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupAds:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "status": "PAUSED",
      "ad": {
        "videoAd": {
          "video": {
            "asset": "customers/{CUSTOMER_ID}/assets/{VIDEO_ASSET_ID}"
          },
          "nonSkippable": {}
        },
        "finalUrls": ["https://example.com/guide?utm_source=youtube&utm_medium=nonskip"]
      }
    }
  }]
}
```

Non-skippable ads must be 15 seconds or shorter. Higher CPM but guaranteed full view.

## Video Creative Specs

| Format | Length | Skip | Best For |
|--------|--------|------|----------|
| Skippable in-stream | 15s-3min (recommend 30-60s) | After 5s | Lead gen, conversions |
| Non-skippable in-stream | Max 15s | No | Brand awareness, key messages |
| Bumper | Max 6s | No | Retargeting, frequency |

### Video Production Checklist (for AI agent)

The agent does NOT produce video. The agent prepares a creative brief for each variant:

1. **Hook (first 5 seconds):** This is the ONLY part most viewers see. Must contain the pain point or a surprising stat. Structure: "[Stat or question] — here's what you can do about it."
2. **Body (5-25 seconds):** Describe the solution approach (NOT your product). Educate. Show credibility.
3. **CTA (last 5 seconds):** Clear action. "Download the free checklist." "Watch the full breakdown." Never "Sign up for a demo" at problem-aware stage.
4. **On-screen text:** Repeat the headline and CTA as text overlay for sound-off viewers (53% of YouTube is watched on mobile, many without sound).

### Variant Framework for Testing

For each pain point, create 3 video ad variants:
- **Stat Hook:** "83% of data teams spend 20+ hours a week on pipeline maintenance. Here's why."
- **Question Hook:** "Is your data team stuck maintaining pipelines instead of building models?"
- **Proof Hook:** "How [Company] cut data pipeline failures by 90% in 30 days."

## Error Handling

- `VIDEO_NOT_FOUND`: YouTube video ID is invalid or video is Private. Must be Public or Unlisted.
- `VIDEO_TOO_LONG`: Bumper ads must be <=6s, non-skippable must be <=15s.
- `IMAGE_ERROR`: Companion banner must be 300x60px PNG or JPG, under 150KB.
- `FINAL_URL_DOES_NOT_MATCH_DISPLAY_URL`: Ensure final URL domain matches the display URL domain.

## Pricing

- No additional cost for creative setup. You pay per view or conversion.
- Video production: $0 (DIY with Descript/Loom) to $2,000+ (professional)
- Descript: $24/mo for video editing with AI. https://www.descript.com/pricing
- Pictory: $23/mo for AI video generation from scripts. https://pictory.ai/pricing
- Synthesia: $22/mo for AI avatar videos. https://www.synthesia.io/pricing

## Alternatives

- **Descript**: Script-based video editing, AI voice, subtitles ($24/mo)
- **Pictory**: Convert text/blog to video ($23/mo)
- **Synthesia**: AI avatar spokesperson videos ($22/mo)
- **InVideo**: Template-based video editor ($25/mo)
- **Canva Video**: Simple video creation, free tier available
- **Loom**: Screen recording for demo-style prerolls (free tier)
