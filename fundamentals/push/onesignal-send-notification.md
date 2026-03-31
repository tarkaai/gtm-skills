---
name: onesignal-send-notification
description: Send a push notification to users or segments via the OneSignal REST API
tool: OneSignal
product: OneSignal
difficulty: Setup
---

# Send Push Notification via OneSignal

## Prerequisites
- OneSignal account with an app created
- REST API key (found in Settings > Keys & IDs)
- App ID (found in Settings > Keys & IDs)
- Users subscribed to push notifications via OneSignal SDK

## Authentication

All requests require the REST API key in the `Authorization` header:
```
Authorization: Key YOUR_REST_API_KEY
```

## Send to a Segment

```
POST https://api.onesignal.com/notifications
Content-Type: application/json
Authorization: Key YOUR_REST_API_KEY

{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "included_segments": ["Active Users"],
  "contents": {"en": "Your weekly activity summary is ready"},
  "headings": {"en": "Activity Report"},
  "url": "https://app.example.com/reports/weekly",
  "chrome_web_image": "https://app.example.com/img/report-icon.png"
}
```

## Send to Specific Users

Target by external user ID (your internal user ID):
```json
{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "include_aliases": {"external_id": ["user_123", "user_456"]},
  "contents": {"en": "You have 3 unread messages"},
  "headings": {"en": "New Messages"},
  "url": "https://app.example.com/inbox"
}
```

## Send with Data Payload (Silent Push)

For triggering background app actions without visible notification:
```json
{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "included_segments": ["Active Users"],
  "content_available": true,
  "data": {
    "action": "sync_data",
    "resource": "activity_feed"
  }
}
```

## Schedule for Later

```json
{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "included_segments": ["Active Users"],
  "contents": {"en": "Don't miss today's challenge!"},
  "send_after": "2026-04-01T09:00:00-05:00"
}
```

## Send in User's Timezone

Delivers at the specified time in each user's local timezone:
```json
{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "included_segments": ["Active Users"],
  "contents": {"en": "Good morning! Check your dashboard"},
  "delayed_option": "timezone",
  "delivery_time_of_day": "9:00AM"
}
```

## Response

Success (200):
```json
{
  "id": "notification-uuid",
  "recipients": 1500,
  "external_id": null
}
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `contents` | object | Notification body by language code |
| `headings` | object | Notification title by language code |
| `url` | string | URL opened when notification is clicked |
| `chrome_web_image` | string | Large image for web push |
| `big_picture` | string | Large image for Android |
| `ios_attachments` | object | Rich media for iOS |
| `ttl` | integer | Seconds before notification expires |
| `priority` | integer | 1-10, delivery priority |
| `collapse_id` | string | Replaces previous notification with same ID |

## Error Handling

- **400**: Invalid parameters — check `app_id` and segment names
- **401**: Invalid API key — verify REST API key (not User Auth key)
- **429**: Rate limited — OneSignal limits to ~300 requests/second; batch requests or add backoff
- If `recipients` is 0: the segment exists but no users match, or no users have push subscriptions

## Pricing Reference

- **Free**: Unlimited push subscribers; 10,000 web push subscribers messageable at a time
- **Growth**: $19/mo + $0.012/mobile MAU + $0.004/web subscriber
- Pricing page: https://onesignal.com/pricing
