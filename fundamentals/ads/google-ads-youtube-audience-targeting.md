---
name: google-ads-youtube-audience-targeting
description: Configure YouTube video campaign audience targeting via Google Ads API (topics, placements, custom segments, affinity)
tool: Google Ads
difficulty: Config
---

# Google Ads YouTube Audience Targeting

Configure precise audience targeting for YouTube Video campaigns. YouTube supports targeting by channel/video placement, topic, custom intent (search-based), affinity, in-market, demographics, and combined audiences.

## Prerequisites

- Google Ads Video campaign created (see `google-ads-youtube-video-campaign`)
- Google Ads API access with OAuth 2.0
- ICP definition with known pain points and intent signals

## Core Operations

### Placement targeting (specific channels and videos)

The highest-precision targeting. Show ads on specific YouTube channels or videos your ICP watches.

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "placement": {
        "url": "youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw"
      },
      "status": "ENABLED"
    }
  }]
}
```

For individual video placements:
```json
{
  "placement": {
    "url": "youtube.com/video/VIDEO_ID"
  }
}
```

**Finding placements:** Use the YouTube Data API to search for channels by keyword, then filter by subscriber count and topic relevance. Also use TubeSift or manually compile a list of 20-50 channels your ICP watches.

### Topic targeting

Show ads on videos categorized under specific topics. Broader than placements but still relevant.

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "topic": {
        "topicConstant": "topicConstants/3"
      },
      "status": "ENABLED"
    }
  }]
}
```

Retrieve available topics:
```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT topic_constant.id, topic_constant.topic_constant_parent, topic_constant.path FROM topic_constant WHERE topic_constant.path LIKE '%Technology%' LIMIT 100"
}
```

Relevant B2B topics: Computers & Electronics > Software, Business & Industrial > Business Services, Business & Industrial > Business Operations.

### Custom segments (intent-based)

Target people based on their recent Google search terms. This is extremely powerful for B2B — target users who recently searched for terms related to your problem space.

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/customAudiences:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "name": "Custom Intent - Data Pipeline Problems",
      "type": "SEARCH",
      "members": [
        {"memberType": "KEYWORD", "keyword": "data pipeline failures"},
        {"memberType": "KEYWORD", "keyword": "ETL tool comparison"},
        {"memberType": "KEYWORD", "keyword": "data integration best practices"},
        {"memberType": "KEYWORD", "keyword": "how to fix data sync issues"},
        {"memberType": "KEYWORD", "keyword": "data quality monitoring tools"}
      ]
    }
  }]
}
```

Then attach the custom audience to an ad group:
```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "customAudience": "customers/{CUSTOMER_ID}/customAudiences/{AUDIENCE_ID}",
      "status": "ENABLED"
    }
  }]
}
```

### Affinity and in-market audiences

Google's pre-built audiences based on browsing behavior.

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT user_interest.user_interest_id, user_interest.name, user_interest.user_interest_parent FROM user_interest WHERE user_interest.name LIKE '%Software%' LIMIT 50"
}
```

Attach to ad group:
```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "userInterest": {
        "userInterestCategory": "userInterests/{INTEREST_ID}"
      },
      "status": "ENABLED"
    }
  }]
}
```

Relevant B2B affinity audiences: Technology/Technophiles, Business Professionals, Cloud Services.
Relevant in-market audiences: Business Services, Software/Business Software, Marketing Software.

### Demographic layering

Add demographic filters on top of any targeting method:

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [
    {
      "create": {
        "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
        "ageRange": {"type": "AGE_RANGE_25_34"},
        "negative": false
      }
    },
    {
      "create": {
        "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
        "ageRange": {"type": "AGE_RANGE_18_24"},
        "negative": true
      }
    }
  ]
}
```

For B2B, exclude AGE_RANGE_18_24 (unlikely decision-makers) and PARENTAL_STATUS_NOT_A_PARENT only if your ICP skews older.

### Exclusion lists (negative targeting)

Exclude irrelevant placements, topics, or audiences:

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/adGroupCriteria:mutate
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "operations": [{
    "create": {
      "adGroup": "customers/{CUSTOMER_ID}/adGroups/{AD_GROUP_ID}",
      "placement": {
        "url": "youtube.com/channel/IRRELEVANT_CHANNEL_ID"
      },
      "negative": true
    }
  }]
}
```

Also exclude content categories (violence, profanity, sensitive social issues) at the campaign level via `videoBrandSafetySuitability`.

## Targeting Strategy by Level

| Level | Primary Targeting | Secondary |
|-------|------------------|-----------|
| Smoke | 20-50 hand-picked channel placements + custom intent (5-10 search terms) | None |
| Baseline | Expand to 100+ placements + 2 custom intent segments | Topic targeting as broadening layer |
| Scalable | All of the above + affinity/in-market layering + combined audiences | Lookalike via Customer Match |
| Durable | Agent-managed: auto-discovers new placements, refreshes custom intent terms, rotates audiences based on saturation | Autonomous A/B on audience segments |

## Error Handling

- `CRITERION_NOT_ALLOWED_FOR_CAMPAIGN_TYPE`: Some criteria types are incompatible with Video campaigns. Verify the criterion type matches VIDEO_TRUE_VIEW_IN_STREAM.
- `AUDIENCE_NOT_ELIGIBLE`: Custom audience may be too narrow (<1,000 users). Add more keywords.
- `PLACEMENT_NOT_FOUND`: YouTube channel or video URL may be malformed. Use `youtube.com/channel/{ID}` format.

## Pricing

- No additional cost for audience targeting. You pay per view/conversion as usual.
- TubeSift (placement research): $47/mo. https://tubesift.com
- VidTao (competitor ad spy): Free tier. https://vidtao.com

## Alternatives

- **TubeSift**: Automated YouTube channel/video placement finder ($47/mo)
- **vidIQ**: YouTube analytics with audience insights ($5.98-$17.50/mo)
- **Keywords Everywhere**: Search volume for YouTube keyword targeting ($1.25 for 100K credits)
- **SparkToro**: Audience research for finding channels your ICP watches ($50-$225/mo)
- **Audiense**: Audience intelligence platform for cross-channel targeting ($696/mo+)
