---
name: google-ads-youtube-video-campaign
description: Create a YouTube Video campaign in Google Ads with proper ad group structure and bidding
tool: Google Ads
difficulty: Config
---

# Google Ads YouTube Video Campaign

Create and configure a Video campaign in Google Ads to run pre-roll (skippable in-stream), non-skippable in-stream, or bumper ads on YouTube.

## Prerequisites

- Google Ads account with API access enabled
- Google Ads developer token (apply at https://ads.google.com/home/tools/api-access/)
- OAuth 2.0 credentials with `https://www.googleapis.com/auth/adwords` scope
- YouTube video(s) uploaded and set to Public or Unlisted
- Conversion tracking configured (see `google-ads-conversion-tracking`)

## Core Operations

### Create a campaign budget

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/campaignBudgets:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "name": "YouTube Preroll - Q1 Problem Aware",
      "amountMicros": "50000000",
      "deliveryMethod": "STANDARD",
      "explicitlyShared": false
    }
  }]
}
```

`amountMicros` is daily budget in micros (50000000 = $50/day).

### Create a Video campaign

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/campaigns:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "name": "YT Preroll - Problem Aware - [Pain Point]",
      "advertisingChannelType": "VIDEO",
      "advertisingChannelSubType": "VIDEO_ACTION",
      "status": "PAUSED",
      "campaignBudget": "customers/{CUSTOMER_ID}/campaignBudgets/{BUDGET_ID}",
      "biddingStrategyType": "MAXIMIZE_CONVERSIONS",
      "videoBrandSafetySuitability": "EXPANDED_INVENTORY",
      "geoTargetTypeSetting": {
        "positiveGeoTargetType": "PRESENCE",
        "negativeGeoTargetType": "PRESENCE"
      },
      "startDate": "2026-04-01",
      "endDate": "2026-04-30"
    }
  }]
}
```

**Campaign subtypes:**
- `VIDEO_ACTION` — skippable in-stream + in-feed, optimized for conversions (best for lead gen)
- `VIDEO_REACH` — maximize views or impressions (best for awareness)
- `VIDEO_NON_SKIPPABLE_IN_STREAM` — 15-second non-skip ads (best for branding)

For problem-aware lead gen, use `VIDEO_ACTION` with `MAXIMIZE_CONVERSIONS` bidding.

### Set geographic targeting

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/campaignCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "campaign": "customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}",
      "location": {
        "geoTargetConstant": "geoTargetConstants/2840"
      }
    }
  }]
}
```

Common geo constants: US = 2840, UK = 2826, Canada = 2124, Australia = 2036.

### Create an ad group

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroups:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "name": "Problem Aware - Data Integration Pain",
      "campaign": "customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}",
      "type": "VIDEO_TRUE_VIEW_IN_STREAM",
      "cpcBidMicros": "500000",
      "status": "ENABLED"
    }
  }]
}
```

Ad group types for video:
- `VIDEO_TRUE_VIEW_IN_STREAM` — skippable pre-roll
- `VIDEO_NON_SKIPPABLE_IN_STREAM` — 15s non-skip
- `VIDEO_BUMPER` — 6s bumper ads

### Create a video ad

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
          "inStream": {
            "actionButtonLabel": "Learn More",
            "actionHeadline": "Fix Your Data Pipeline in Days, Not Months",
            "companionBanner": {
              "asset": "customers/{CUSTOMER_ID}/assets/{BANNER_ASSET_ID}"
            }
          }
        },
        "finalUrls": ["https://example.com/guide?utm_source=youtube&utm_medium=preroll&utm_campaign={CAMPAIGN_ID}"]
      }
    }
  }]
}
```

### Upload a video asset (link existing YouTube video)

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/assets:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "youtubeVideoAsset": {
        "youtubeVideoId": "dQw4w9WgXcQ",
        "youtubeVideoTitle": "How to Fix Data Pipeline Failures"
      }
    }
  }]
}
```

## Budget Guidelines for B2B

- **Smoke test:** $15-30/day ($300-600 over 2-3 weeks). Expect CPV $0.02-0.10.
- **Baseline:** $30-75/day ($1,000-2,500/month).
- **Scalable:** $100-300/day ($3,000-10,000/month).

## Error Handling

- `CAMPAIGN_BUDGET_CANNOT_BE_SHARED`: Set `explicitlyShared: false` on budget.
- `INVALID_CHANNEL_SUB_TYPE`: Verify subtype matches channel type. VIDEO_ACTION requires advertisingChannelType = VIDEO.
- `VIDEO_NOT_FOUND`: Confirm the YouTube video ID is valid and the video is Public or Unlisted.
- `BIDDING_STRATEGY_NOT_AVAILABLE`: Some bid strategies are not available for all campaign subtypes. VIDEO_ACTION supports MAXIMIZE_CONVERSIONS and TARGET_CPA.

## Pricing

- Google Ads: No platform fee. Pay per view (CPV) or per conversion (CPA). Typical B2B YouTube CPV: $0.02-0.10.
- Docs: https://developers.google.com/google-ads/api/docs/start

## Alternatives

- **DV360 (Display & Video 360)**: Enterprise programmatic video buying. Higher minimum spend ($10K+/mo).
- **TubeSift**: YouTube placement research tool ($47/mo). Finds specific channels/videos for targeting.
- **VidTao**: YouTube ad spy tool. See competitor video ads. Free tier available.
- **Foreplay**: Ad creative swipe file / spy tool ($49/mo).
- **AdSector**: Video ad intelligence for native and YouTube ($249/mo).
