---
name: twitter-x-ads-campaign-setup
description: Create and configure promoted tweet campaigns via the Twitter/X Ads API
tool: Twitter/X Ads
difficulty: Setup
---

# Twitter/X Ads Campaign Setup

Create promoted tweet and promoted account campaigns programmatically via the X Ads API v12+.

## Authentication

X Ads API uses OAuth 1.0a. Required credentials:
- Consumer key + secret (from X Developer Portal app)
- Access token + secret (for the ads account owner)
- Ads account ID (`ads_account_id`) from `GET /12/accounts`

All requests go to `https://ads-api.x.com/12/`.

## Step 1: List available funding instruments

```
GET /12/accounts/{account_id}/funding_instruments
```

You need a `funding_instrument_id` to create a campaign.

## Step 2: Create a campaign

```
POST /12/accounts/{account_id}/campaigns

{
  "name": "Twitter Ads - Solution Aware - {YYYYMMDD}",
  "funding_instrument_id": "{FUNDING_ID}",
  "daily_budget_amount_local_micro": 5000000,
  "start_time": "2026-04-01T00:00:00Z",
  "entity_status": "PAUSED"
}
```

Budget is in micros: $5.00 = 5000000. Always create in PAUSED state. Launch only after ad groups and creatives are attached.

## Step 3: Create a line item (ad group)

```
POST /12/accounts/{account_id}/line_items

{
  "campaign_id": "{CAMPAIGN_ID}",
  "name": "Promoted Tweets - ICP Audience",
  "product_type": "PROMOTED_TWEETS",
  "placements": ["ALL_ON_TWITTER"],
  "objective": "WEBSITE_CLICKS",
  "bid_amount_local_micro": 2500000,
  "bid_type": "AUTO",
  "entity_status": "PAUSED"
}
```

Objectives: `AWARENESS`, `TWEET_ENGAGEMENTS`, `WEBSITE_CLICKS`, `APP_INSTALLS`, `FOLLOWERS`, `VIDEO_VIEWS`.

For solution-aware audiences use `WEBSITE_CLICKS` (drive to landing page) or `TWEET_ENGAGEMENTS` (for content distribution).

## Step 4: Configure audience targeting

```
POST /12/accounts/{account_id}/targeting_criteria

{
  "line_item_id": "{LINE_ITEM_ID}",
  "targeting_type": "INTEREST",
  "targeting_value": "technology"
}
```

Targeting types:
- `LOCATION` — country, region, city, or postal code
- `INTEREST` — 350+ interest categories. GET `/12/targeting_criteria/interests` for the full list.
- `FOLLOWER_LOOKALIKES` — target users similar to followers of specific handles
- `KEYWORD` — users who recently tweeted or engaged with tweets containing these keywords
- `CONVERSATION_TOPIC` — 10,000+ conversation topics
- `DEVICE` — iOS, Android, Desktop
- `LANGUAGE` — language code
- `AGE` — age buckets (AGE_18_24, AGE_25_34, etc.)

Create multiple targeting criteria per line item. They combine with AND within the same type and OR across types.

For B2B SaaS ICP targeting, use:
1. `FOLLOWER_LOOKALIKES` of competitor handles and industry thought leaders
2. `KEYWORD` targeting for problem-related and solution-category terms
3. `INTEREST` targeting for technology, SaaS, and industry-specific interests
4. Layer `LOCATION` to restrict to target geographies

## Step 5: Create promoted tweets

First, publish an organic tweet via the X API v2:

```
POST https://api.x.com/2/tweets
Authorization: Bearer {USER_ACCESS_TOKEN}

{
  "text": "Your ad copy here. Include a link to your landing page with UTM parameters."
}
```

Then promote it:

```
POST /12/accounts/{account_id}/promoted_tweets

{
  "line_item_id": "{LINE_ITEM_ID}",
  "tweet_ids": ["{TWEET_ID}"]
}
```

You can also use "dark posts" (promoted-only tweets) that do not appear on your organic timeline:

```
POST /12/accounts/{account_id}/tweet

{
  "text": "Ad copy for promoted-only tweet",
  "as_user_id": "{USER_ID}"
}
```

## Step 6: Set up conversion tracking

Create a website tag:

```
POST /12/accounts/{account_id}/web_event_tags

{
  "name": "Landing Page Conversion",
  "type": "SITE_VISIT",
  "click_window": "30",
  "view_through_window": "1",
  "embed_code": true
}
```

Returns a pixel snippet to install on your landing page or pass conversion events server-side via:

```
POST /12/accounts/{account_id}/web_event_tags/{tag_id}/conversions

{
  "conversion_time": "2026-04-01T12:00:00Z",
  "conversion_id": "{UNIQUE_ID}",
  "click_id": "{twclid}"
}
```

Capture the `twclid` URL parameter on landing page visits and pass it back on conversion.

## Step 7: Launch

```
PUT /12/accounts/{account_id}/campaigns/{campaign_id}

{
  "entity_status": "ACTIVE"
}
```

Also set line items to ACTIVE.

## Alternative: X Ads Manager UI

If API access is not available (requires X Ads API approval):
1. Log in to ads.x.com
2. Create campaign > Choose objective
3. Set daily budget and schedule
4. Build audience: locations, keywords, interests, follower lookalikes
5. Write tweet copy or select existing tweets to promote
6. Launch

## Rate Limits

- 2,000 requests per 15-minute window per ads account
- Batch endpoints available for bulk operations

## Error Handling

- `INSUFFICIENT_FUNDS`: Funding instrument has no balance. Top up the credit card.
- `INVALID_TARGETING`: Targeting criteria too narrow or contradictory. Broaden the audience.
- `ENTITY_NOT_FOUND`: Campaign, line item, or tweet ID invalid. Re-fetch IDs.
- `RATE_LIMIT`: 429 response. Wait until `x-rate-limit-reset` timestamp.
- `AUTHORIZATION_REQUIRED`: OAuth tokens invalid or lack ads permissions.
