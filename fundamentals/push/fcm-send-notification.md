---
name: fcm-send-notification
description: Send push notifications to mobile and web clients via Firebase Cloud Messaging HTTP v1 API
tool: Google
product: Firebase
difficulty: Setup
---

# Send Push Notification via Firebase Cloud Messaging (FCM)

## Prerequisites
- Firebase project with Cloud Messaging enabled
- Service account JSON credentials (Firebase Console > Project Settings > Service Accounts > Generate New Private Key)
- Client app with FCM SDK integrated and device tokens collected
- OAuth 2.0 access token generated from service account credentials

## Authentication

FCM HTTP v1 API uses OAuth 2.0 access tokens (not the deprecated server key):

```bash
# Generate access token using Google Auth library
# Node.js example:
# const {GoogleAuth} = require('google-auth-library');
# const auth = new GoogleAuth({scopes: ['https://www.googleapis.com/auth/firebase.messaging']});
# const token = await auth.getAccessToken();
```

Or use a service account to get a short-lived token:
```
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=SIGNED_JWT
```

## Send to a Single Device

```
POST https://fcm.googleapis.com/v1/projects/YOUR_PROJECT_ID/messages:send
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

{
  "message": {
    "token": "DEVICE_FCM_TOKEN",
    "notification": {
      "title": "New activity on your project",
      "body": "Sarah commented on your design file"
    },
    "webpush": {
      "fcm_options": {
        "link": "https://app.example.com/projects/123"
      }
    },
    "data": {
      "project_id": "123",
      "action": "view_comment"
    }
  }
}
```

## Send to a Topic (Segment)

Subscribe users to topics from your backend:
```
POST https://iid.googleapis.com/iid/v1:batchAdd
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

{
  "to": "/topics/weekly-active-users",
  "registration_tokens": ["token1", "token2", "token3"]
}
```

Then send to the topic:
```json
{
  "message": {
    "topic": "weekly-active-users",
    "notification": {
      "title": "Your weekly summary is ready",
      "body": "You completed 12 tasks this week"
    }
  }
}
```

## Send with Condition (Multiple Topics)

Target users subscribed to topic A AND topic B:
```json
{
  "message": {
    "condition": "'active-users' in topics && 'pro-plan' in topics",
    "notification": {
      "title": "Pro feature update",
      "body": "Advanced analytics is now available"
    }
  }
}
```

## Platform-Specific Configuration

```json
{
  "message": {
    "topic": "active-users",
    "notification": {
      "title": "Check your dashboard",
      "body": "3 items need attention"
    },
    "android": {
      "priority": "high",
      "notification": {
        "icon": "ic_notification",
        "color": "#2A9E96",
        "click_action": "OPEN_DASHBOARD"
      }
    },
    "apns": {
      "payload": {
        "aps": {
          "badge": 3,
          "sound": "default",
          "category": "DASHBOARD_ACTION"
        }
      }
    },
    "webpush": {
      "notification": {
        "icon": "https://app.example.com/icon-192.png",
        "badge": "https://app.example.com/badge-72.png"
      },
      "fcm_options": {
        "link": "https://app.example.com/dashboard"
      }
    }
  }
}
```

## Response

Success (200):
```json
{
  "name": "projects/YOUR_PROJECT_ID/messages/message-id"
}
```

## Error Handling

- **400 INVALID_ARGUMENT**: Malformed request — check token format and message structure
- **401 UNAUTHENTICATED**: Access token expired or invalid — regenerate OAuth token
- **404 NOT_FOUND**: Device token is invalid or user uninstalled — remove token from your database
- **429 QUOTA_EXCEEDED**: Sending too fast — implement exponential backoff
- **503 UNAVAILABLE**: FCM server temporarily down — retry with backoff

## Pricing

FCM is free with no per-message cost. Firebase pricing: https://firebase.google.com/pricing

## Alternatives

- **OneSignal**: Higher-level API with built-in segments and A/B testing; wraps FCM internally
- **Knock**: Unified notification API with push as one channel
- **Novu**: Open-source alternative with FCM integration
- **AWS SNS**: Amazon's push notification service with FCM/APNs integration
- **Pusher Beams**: Simple push API with pub/sub model
