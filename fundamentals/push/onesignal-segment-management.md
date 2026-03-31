---
name: onesignal-segment-management
description: Create, update, and query user segments in OneSignal for targeted push notification delivery
tool: OneSignal
difficulty: Config
---

# OneSignal Segment Management

## Prerequisites
- OneSignal account with app configured
- REST API key
- Users with tracked properties (tags) in OneSignal

## How Segments Work

OneSignal segments are dynamic groups of users defined by filters on user properties (tags), session data, and device attributes. Users automatically enter and exit segments as their properties change.

## Create a Segment

```
POST https://api.onesignal.com/apps/YOUR_APP_ID/segments
Content-Type: application/json
Authorization: Key YOUR_REST_API_KEY

{
  "name": "Power Users - Weekly Active",
  "filters": [
    {"field": "session_count", "relation": ">", "value": "10"},
    {"operator": "AND"},
    {"field": "last_session", "relation": ">", "hours_ago": "168"},
    {"operator": "AND"},
    {"field": "tag", "key": "plan", "relation": "=", "value": "pro"}
  ]
}
```

## Filter Types

| Field | Description | Example |
|-------|-------------|---------|
| `last_session` | Hours since last session | `"hours_ago": "24"` |
| `first_session` | Hours since first session | `"hours_ago": "720"` |
| `session_count` | Total sessions | `"value": "5"` |
| `session_time` | Total seconds of usage | `"value": "3600"` |
| `tag` | Custom user property | `"key": "feature_used", "value": "export"` |
| `language` | Device language | `"value": "en"` |
| `app_version` | App version string | `"value": "2.1.0"` |
| `country` | User country code | `"value": "US"` |

## Set User Tags (Properties) via API

Tags drive segmentation. Set them from your backend when user behavior changes:

```
PUT https://api.onesignal.com/apps/YOUR_APP_ID/users/by/external_id/user_123
Content-Type: application/json
Authorization: Key YOUR_REST_API_KEY

{
  "properties": {
    "tags": {
      "plan": "pro",
      "feature_export_used": "true",
      "sessions_this_week": "12",
      "churn_risk": "low",
      "last_feature": "dashboard"
    }
  }
}
```

## Delete a Segment

```
DELETE https://api.onesignal.com/apps/YOUR_APP_ID/segments/SEGMENT_ID
Authorization: Key YOUR_REST_API_KEY
```

## Recommended Segments for Push Engagement

Build these segments to power the push notification engagement play:

1. **New Users (< 7 days)**: `first_session` < 168 hours ago
2. **Active This Week**: `last_session` < 168 hours ago AND `session_count` > 3
3. **At-Risk (Usage Drop)**: `last_session` > 168 hours ago AND `session_count` > 10 (were active, now quiet)
4. **Power Users**: `session_count` > 50 AND `last_session` < 72 hours ago
5. **Feature Discovery**: tag `feature_X_used` != "true" AND `session_count` > 5 (active users who haven't found a feature)
6. **Re-engagement**: `last_session` > 336 hours ago AND `session_count` > 3 (dormant users with prior engagement)

## Error Handling

- **400**: Invalid filter syntax — verify field names and relation operators
- **404**: Segment not found — verify segment ID
- **409**: Segment name already exists — use a unique name
- Tags must be strings — convert numbers and booleans to string values before setting

## Alternatives

- **Firebase (FCM)**: Topic subscriptions for segment-like targeting (subscribe/unsubscribe users to topics)
- **Knock**: Preference-based routing with channel conditions
- **Novu**: Subscriber management with topic-based grouping
- **Customer.io**: Segment builder with behavioral filters and push channel
- **Pushwoosh**: Tag-based segmentation with geo-targeting
