---
name: cross-platform-retargeting-sync
description: Sync retargeting audiences, exclusion lists, and conversion data across Meta, LinkedIn, and Google Ads via their APIs
tool: Meta Ads, LinkedIn Ads, Google Ads
difficulty: Advanced
---

# Cross-Platform Retargeting Sync

## Prerequisites
- Meta Business Manager with Marketing API access and valid access token
- LinkedIn Campaign Manager with Marketing API access and OAuth 2.0 token
- Google Ads account with API access and developer token
- n8n instance for orchestrating syncs
- Attio CRM with customer records (for exclusion lists)

## Steps

### 1. Export customer exclusion list from CRM

Query Attio for all current customers and recently converted leads. These must be excluded from retargeting on every platform.

```
GET https://api.attio.com/v2/lists/{customer-list-id}/entries
Headers: Authorization: Bearer {attio-api-key}
```

Extract email addresses. Hash each with SHA-256 for privacy compliance before uploading to ad platforms.

### 2. Upload exclusion audience to Meta

```
POST https://graph.facebook.com/v18.0/act_{ad-account-id}/customaudiences
{
  "name": "Exclusion - Current Customers",
  "subtype": "CUSTOM",
  "customer_file_source": "USER_PROVIDED_ONLY"
}
```

Then upload hashed emails:
```
POST https://graph.facebook.com/v18.0/{audience-id}/users
{
  "payload": {
    "schema": ["EMAIL_SHA256"],
    "data": [["<sha256-hash-1>"], ["<sha256-hash-2>"]]
  }
}
```

### 3. Upload exclusion audience to LinkedIn

```
POST https://api.linkedin.com/v2/dmpSegments
{
  "name": "Exclusion - Current Customers",
  "type": "USER",
  "sourcePlatform": "FIRST_PARTY"
}
```

Upload hashed emails via the DMP Segment entity upload endpoint. LinkedIn requires SHA-256 hashed emails.

### 4. Upload exclusion audience to Google Ads

Use the Google Ads API UserListService:
```
POST /customers/{customer-id}/userLists:mutate
{
  "operations": [{
    "create": {
      "name": "Exclusion - Current Customers",
      "crmBasedUserList": {
        "uploadKeyType": "CRM_ID",
        "dataSourceType": "FIRST_PARTY"
      },
      "membershipLifeSpan": 30
    }
  }]
}
```

Then upload via OfflineUserDataJobService with SHA-256 hashed emails.

### 5. Sync website visitor segments across platforms

Each platform has its own pixel/tag for building visitor audiences. Ensure consistent segment definitions:

| Segment | Meta Rule | LinkedIn Rule | Google Rule |
|---------|-----------|---------------|-------------|
| High intent (pricing/demo page, 14d) | `url contains /pricing OR /demo, retention_days: 14` | Insight Tag + URL rule `/pricing OR /demo`, lookback 14d | Google Ads tag + URL rule, membership 14d |
| Medium intent (2+ pages, 30d) | `event: PageView, count >= 2, retention_days: 30` | Insight Tag + page count rule, lookback 30d | Google Analytics audience: sessions >= 2, 30d |
| Low intent (homepage bounce, 7d) | `url = homepage, retention_days: 7` | Insight Tag + URL rule, lookback 7d | Google Ads tag, homepage only, 7d |

Verify audience sizes via each platform's API after 48 hours of pixel data collection.

### 6. Sync conversion events for optimization

Report conversions back to each platform so their algorithms optimize toward the right outcomes:

**Meta CAPI:**
```
POST https://graph.facebook.com/v18.0/{pixel-id}/events
{
  "data": [{
    "event_name": "Lead",
    "event_time": {unix-timestamp},
    "user_data": {"em": ["{sha256-email}"]},
    "event_source_url": "{landing-page-url}",
    "event_id": "{unique-id}"
  }]
}
```

**LinkedIn Conversions API:**
```
POST https://api.linkedin.com/rest/conversionEvents
{
  "conversion": "{conversion-urn}",
  "conversionHappenedAt": {epoch-ms},
  "user": {"userIds": [{"idType": "SHA256_EMAIL", "idValue": "{hash}"}]}
}
```

**Google Ads offline conversions:**
```
POST /customers/{id}/offlineUserDataJobs:create
```
Upload click ID + conversion data pairs via OfflineUserDataJobService.

### 7. Schedule automated sync via n8n

Build an n8n workflow triggered by a daily cron at 02:00 UTC:
1. Pull new customers and conversions from Attio (last 24h)
2. Hash emails with SHA-256
3. Upload to Meta, LinkedIn, and Google exclusion audiences in parallel
4. Push conversion events to all three CAPI/offline endpoints
5. Log sync results to PostHog: `retargeting_audience_sync` event with properties `{platform, records_synced, errors}`

### Error handling

- If any platform API returns 429 (rate limit): retry with exponential backoff (2s, 4s, 8s, max 3 retries)
- If audience upload fails: log error to PostHog, send Slack alert, do not block other platform syncs
- If audience size drops below 100 on any platform: alert — audiences below 100 cannot be targeted
