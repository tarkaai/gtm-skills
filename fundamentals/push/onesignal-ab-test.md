---
name: onesignal-ab-test
description: Run A/B tests on push notification content, timing, and targeting via OneSignal
tool: OneSignal
product: OneSignal
difficulty: Config
---

# A/B Test Push Notifications via OneSignal

## Prerequisites
- OneSignal app with active push subscribers
- Sufficient subscriber volume (minimum 200 per variant recommended)
- REST API key

## Create an A/B Test Notification

OneSignal's API natively supports A/B testing by sending multiple content variants. The platform splits the audience automatically and tracks which variant gets more clicks.

### Two-Variant Content Test

```
POST https://api.onesignal.com/notifications
Content-Type: application/json
Authorization: Key YOUR_REST_API_KEY

{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "included_segments": ["Active Users"],
  "contents": {"en": "Your team posted 5 new updates"},
  "headings": {"en": "Team Activity"},

  "enable_frequency_capping": false,

  "content_available": false
}
```

For built-in A/B testing, use OneSignal's dashboard AB test feature, which sends variant A to a test group, variant B to another test group, then sends the winner to the remaining audience.

### Manual A/B Test via API (Full Control)

When you need programmatic control, split the audience yourself:

**Step 1: Create test segments**

Create two equal segments using OneSignal's segment API or by assigning a random tag:

```
PUT https://api.onesignal.com/apps/YOUR_APP_ID/users/by/external_id/user_123
{
  "properties": {
    "tags": { "ab_group": "A" }
  }
}
```

Assign "A" to 50% of users, "B" to the other 50%.

**Step 2: Send variant A**

```json
{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "filters": [{"field": "tag", "key": "ab_group", "relation": "=", "value": "A"}],
  "contents": {"en": "You have 3 items waiting for review"},
  "headings": {"en": "Action Required"},
  "data": {"experiment_id": "push_copy_test_001", "variant": "A"}
}
```

**Step 3: Send variant B**

```json
{
  "app_id": "YOUR_APP_ID",
  "target_channel": "push",
  "filters": [{"field": "tag", "key": "ab_group", "relation": "=", "value": "B"}],
  "contents": {"en": "3 items need your attention before end of day"},
  "headings": {"en": "Don't Miss This"},
  "data": {"experiment_id": "push_copy_test_001", "variant": "B"}
}
```

**Step 4: Measure results**

Query delivery stats for each notification:

```
GET https://api.onesignal.com/notifications/NOTIFICATION_ID?app_id=YOUR_APP_ID
Authorization: Key YOUR_REST_API_KEY
```

Response includes:
```json
{
  "id": "notification-uuid",
  "successful": 500,
  "converted": 85,
  "clicked": 120
}
```

Compare `clicked / successful` (CTR) between variant A and variant B.

## What to Test

| Variable | Variant A | Variant B | Metric |
|----------|-----------|-----------|--------|
| Copy length | Short (< 10 words) | Descriptive (15-25 words) | CTR |
| Urgency | Neutral tone | Time-pressure ("before end of day") | CTR |
| Personalization | Generic | Includes user data ("You have 3...") | CTR |
| Emoji | No emoji | With emoji | CTR |
| Send time | Morning (9 AM local) | Evening (6 PM local) | CTR |
| Deep link | Home screen | Specific feature/content | Session depth |

## Statistical Significance

Do not call a winner until:
- Each variant has 200+ deliveries
- CTR difference is > 1 percentage point
- Test has run for at least 48 hours (captures weekday/weekend variation)

If results are within 1pp after sufficient sample, variants are equivalent — keep whichever is simpler.

## Error Handling

- If one variant has significantly lower `successful` count, the segments may be unbalanced — re-check tag distribution
- Track `errored` field in response — high error rates invalidate results
- Use `data.experiment_id` to correlate push events with downstream PostHog events for deeper analysis

## Alternatives

- **PostHog feature flags**: Control which push content users see from your own backend; more flexible but requires custom implementation
- **Knock**: Workflow-level A/B testing with built-in analytics
- **Customer.io**: Native push A/B testing with statistical significance calculator
