---
name: reddit-ads-campaign-setup
description: Create and configure Reddit Ads campaigns, ad groups, and ads via the Reddit Ads API v3
tool: Reddit Ads API
difficulty: Setup
---

# Reddit Ads — Campaign Setup

Create and manage Reddit advertising campaigns programmatically via the Reddit Ads API v3. The API provides full CRUD control over accounts, campaigns, ad groups, and ads.

## Authentication

Reddit Ads API uses OAuth2. You need a Reddit Ads account and API access.

1. Apply for Reddit Ads API access at https://business.reddithelp.com/s/article/Reddit-Ads-API
2. Create an OAuth2 app at https://www.reddit.com/prefs/apps (type: `web`)
3. Required scopes: `ads:read` (GET), `ads:manage` (POST, PATCH, DELETE)

Get an access token:

```bash
curl -X POST https://www.reddit.com/api/v1/access_token \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "grant_type=client_credentials&scope=ads:read ads:manage" \
  -A "YourApp/1.0"
```

Response: `{"access_token": "TOKEN", "token_type": "bearer", "expires_in": 86400}`

Base URL: `https://ads-api.reddit.com/api/v3`

## Rate Limits

- 1 request per second per access token
- Batch operations where possible to stay within limits
- Implement exponential backoff on 429 responses

## Campaign Hierarchy

Reddit Ads follows: **Account -> Campaign -> Ad Group -> Ad**

- **Campaign**: Budget, objective, start/end dates
- **Ad Group**: Targeting (subreddits, interests, keywords), bid, schedule
- **Ad**: Creative (headline, body, image/video, CTA, destination URL)

## Create a Campaign

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "paid-reddit-ads-smoke-{date}",
  "objective": "CONVERSIONS",
  "daily_budget_micro": 50000000,
  "start_time": "2026-04-01T00:00:00Z",
  "end_time": "2026-04-08T00:00:00Z",
  "is_paid": true,
  "configured_status": "PAUSED"
}
```

Notes:
- `daily_budget_micro` is in microdollars (multiply dollars by 1,000,000). $50/day = 50000000.
- Objectives: `CONVERSIONS`, `TRAFFIC`, `AWARENESS`, `VIDEO_VIEWS`, `APP_INSTALLS`
- For lead generation, use `CONVERSIONS` with a landing page form
- Start campaigns in `PAUSED` status to review before launching
- Minimum daily budget: $5 (5000000 micro)

## Create an Ad Group

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/adgroups
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "adgroup-subreddit-{target_subreddits}",
  "bid_micro": 3000000,
  "bid_strategy": "CPC",
  "target": {
    "subreddits": ["startups", "SaaS", "devops"],
    "geos": [{"country": "US"}],
    "devices": ["DESKTOP", "MOBILE"],
    "expansion": false
  },
  "start_time": "2026-04-01T00:00:00Z",
  "end_time": "2026-04-08T00:00:00Z",
  "configured_status": "PAUSED"
}
```

Notes:
- `bid_micro`: CPC bid in microdollars. $3.00 CPC = 3000000.
- `bid_strategy`: `CPC` (cost per click), `CPM` (cost per 1000 impressions), `CPV` (cost per view)
- Subreddit targeting: pass subreddit names without the `r/` prefix
- Best practice: 3-5 subreddits per ad group, mix one large community with 2-4 niche ones
- Set `expansion: false` to prevent Reddit from auto-expanding targeting beyond your selected subreddits

## Create an Ad

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/adgroups/{adgroup_id}/ads
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "ad-variant-{variant_id}",
  "post_url": null,
  "headline": "How 200+ teams cut deploy incidents by 73%",
  "body": "Free checklist: the 5 steps that actually work. No signup needed.",
  "thumbnail_url": "https://yoursite.com/images/ad-creative-1.png",
  "click_url": "https://yoursite.com/reddit-lp?utm_source=reddit&utm_medium=paid&utm_campaign=paid-reddit-ads&utm_content=deploy-checklist",
  "call_to_action": "LEARN_MORE",
  "configured_status": "PAUSED"
}
```

Notes:
- `headline`: Max 300 characters. Keep under 100 for readability.
- `body`: Optional expanded text. Keep authentic and non-salesy for Reddit audiences.
- `call_to_action`: `LEARN_MORE`, `SIGN_UP`, `SHOP_NOW`, `DOWNLOAD`, `GET_QUOTE`, `CONTACT_US`, `APPLY_NOW`
- Always include UTM parameters in `click_url` for PostHog attribution
- `thumbnail_url`: Upload image via the creative upload endpoint first, then reference the URL

## Upload Creative Assets

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/creatives
Authorization: Bearer TOKEN
Content-Type: multipart/form-data

file=@/path/to/creative.png
```

Supported formats: PNG, JPG, GIF (static only for promoted posts). Video: MP4, MOV (for video ads).
Recommended image sizes: 1200x628 for link ads, 1080x1080 for carousel.

## Update Campaign Status (Launch)

```
PATCH https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "configured_status": "ACTIVE"
}
```

Also activate ad groups and ads with the same PATCH pattern.

## List Campaigns

```
GET https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns
Authorization: Bearer TOKEN
```

Returns all campaigns with their status, budget, and performance summary.

## Error Handling

- **401 Unauthorized**: Token expired. Re-authenticate.
- **403 Forbidden**: Missing `ads:manage` scope or insufficient account permissions.
- **404 Not Found**: Invalid account, campaign, or ad group ID.
- **429 Rate Limited**: Back off for the duration specified in `Retry-After` header.
- **400 Bad Request**: Validation error. Check response body for field-level errors (e.g., budget below minimum, invalid subreddit name).

## Python Client Alternative

```python
import requests

class RedditAdsClient:
    BASE_URL = "https://ads-api.reddit.com/api/v3"

    def __init__(self, client_id, client_secret):
        self.token = self._authenticate(client_id, client_secret)

    def _authenticate(self, client_id, client_secret):
        resp = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials", "scope": "ads:read ads:manage"},
            headers={"User-Agent": "GTMSkills/1.0"}
        )
        return resp.json()["access_token"]

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def create_campaign(self, account_id, payload):
        url = f"{self.BASE_URL}/accounts/{account_id}/campaigns"
        return requests.post(url, json=payload, headers=self._headers()).json()

    def create_adgroup(self, account_id, campaign_id, payload):
        url = f"{self.BASE_URL}/accounts/{account_id}/campaigns/{campaign_id}/adgroups"
        return requests.post(url, json=payload, headers=self._headers()).json()

    def create_ad(self, account_id, campaign_id, adgroup_id, payload):
        url = f"{self.BASE_URL}/accounts/{account_id}/campaigns/{campaign_id}/adgroups/{adgroup_id}/ads"
        return requests.post(url, json=payload, headers=self._headers()).json()
```

## n8n Alternative

Use the HTTP Request node in n8n with OAuth2 credentials:
1. Create Reddit Ads OAuth2 credentials in n8n
2. Use HTTP Request nodes for each API call
3. Chain: Create Campaign -> Create Ad Group -> Create Ad
4. Store IDs from each response for subsequent calls
