---
name: knock-push-workflow
description: Send push notifications through Knock notification workflows with cross-channel orchestration
tool: Knock
difficulty: Config
---

# Send Push Notifications via Knock

## Prerequisites
- Knock account with push channel configured (FCM or APNs provider connected)
- API key (found in Knock dashboard > Developers > API keys)
- Users registered in Knock with push channel tokens
- Notification workflow created in Knock dashboard

## Authentication

```
Authorization: Bearer sk_live_YOUR_SECRET_KEY
```

## Register a User with Push Token

Before sending push, register the user's device token:

```
PUT https://api.knock.app/v1/users/user_123
Content-Type: application/json
Authorization: Bearer sk_live_YOUR_SECRET_KEY

{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

Then set their push channel data:
```
PUT https://api.knock.app/v1/users/user_123/channel_data/FCM_CHANNEL_ID
Content-Type: application/json
Authorization: Bearer sk_live_YOUR_SECRET_KEY

{
  "data": {
    "tokens": ["DEVICE_FCM_TOKEN_1", "DEVICE_FCM_TOKEN_2"]
  }
}
```

## Trigger a Notification Workflow

Knock uses workflows (defined in the dashboard) that can fan out across push, email, in-app, and SMS. Trigger a workflow via API:

```
POST https://api.knock.app/v1/workflows/activity-update/trigger
Content-Type: application/json
Authorization: Bearer sk_live_YOUR_SECRET_KEY

{
  "recipients": ["user_123"],
  "data": {
    "item_count": 3,
    "project_name": "Q1 Campaign",
    "action_url": "https://app.example.com/projects/q1"
  },
  "actor": {
    "id": "user_456",
    "name": "Sarah Chen"
  }
}
```

The workflow template in Knock uses liquid syntax: `{{data.item_count}} items updated in {{data.project_name}}`.

## Batch Trigger (Multiple Recipients)

```
POST https://api.knock.app/v1/workflows/weekly-summary/trigger
Content-Type: application/json
Authorization: Bearer sk_live_YOUR_SECRET_KEY

{
  "recipients": ["user_123", "user_456", "user_789"],
  "data": {
    "week_start": "2026-03-23",
    "summary_url": "https://app.example.com/reports/weekly"
  }
}
```

## Cancel a Scheduled Notification

```
POST https://api.knock.app/v1/workflows/reminder/cancel
Content-Type: application/json
Authorization: Bearer sk_live_YOUR_SECRET_KEY

{
  "recipients": ["user_123"],
  "cancellation_key": "reminder_project_123"
}
```

## User Preferences

Let users control which notifications they receive:

```
PUT https://api.knock.app/v1/users/user_123/preferences
Content-Type: application/json
Authorization: Bearer sk_live_YOUR_SECRET_KEY

{
  "channel_types": {
    "push": true,
    "email": true,
    "sms": false
  },
  "workflows": {
    "activity-update": {
      "channel_types": {
        "push": true,
        "email": false
      }
    }
  }
}
```

## Key Advantages of Knock for Push

- **Cross-channel orchestration**: One workflow can send push, then fall back to email if push is not opened within N minutes
- **Batching**: Knock can batch multiple events into a single notification (e.g., "3 people commented" instead of 3 separate pushes)
- **Preferences**: Built-in per-user, per-workflow, per-channel preference management
- **Idempotency**: Built-in deduplication prevents duplicate notifications

## Error Handling

- **400**: Invalid request — check workflow slug exists and recipient IDs are valid
- **401**: Invalid API key — use the secret key (sk_), not the public key (pk_)
- **404**: Workflow not found — verify the workflow slug matches what's in the Knock dashboard
- **422**: Validation error — check that required data fields for the workflow template are provided

## Pricing

- **Free (Developer)**: 10,000 notifications/month
- **Starter**: 50,000 notifications/month + $0.005/additional message
- Pricing page: https://knock.app/pricing

## Alternatives

- **OneSignal**: Push-first platform with built-in segments and analytics
- **Novu**: Open-source notification infrastructure, self-hostable
- **Customer.io**: Marketing-focused with push, email, SMS
- **MagicBell**: In-app notification inbox with push support
