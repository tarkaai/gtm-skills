---
name: push-notification-setup
description: Configure push notification infrastructure including SDK integration, service worker, opt-in prompt, and event tracking
category: Product
tools:
  - OneSignal
  - Firebase
  - PostHog
  - n8n
fundamentals:
  - onesignal-send-notification
  - fcm-send-notification
  - web-push-service-worker
  - posthog-custom-events
  - n8n-workflow-basics
---

# Push Notification Setup

This drill sets up the complete push notification infrastructure: SDK integration, permission prompts, subscription management, and event tracking. Once complete, you can send targeted push notifications from any other drill or play.

## Prerequisites

- Web or mobile application deployed over HTTPS
- PostHog tracking active on the application
- Decision on push provider: OneSignal (recommended default for managed), FCM (free, lower-level), or raw Web Push (zero vendor lock-in)
- n8n instance for automation workflows

## Steps

### 1. Choose Your Push Provider

Select based on your needs:

- **OneSignal** (recommended default): Managed segments, built-in analytics, A/B testing, cross-platform. Free tier covers most Smoke/Baseline needs. Use `onesignal-send-notification` fundamental.
- **Firebase Cloud Messaging (FCM)**: Free, no per-message cost, requires more custom code for segmentation. Use `fcm-send-notification` fundamental.
- **Raw Web Push (VAPID)**: Zero vendor dependency, full control, web-only. Use `web-push-service-worker` fundamental.
- **Knock**: Best when push is one channel among many in cross-channel workflows. Use `knock-push-workflow` fundamental.

For the default Tarka stack, use OneSignal for push + PostHog for analytics.

### 2. Integrate the SDK

**For OneSignal (web):**
Add the OneSignal SDK to your application:
```html
<script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
<script>
  window.OneSignalDeferred = window.OneSignalDeferred || [];
  OneSignalDeferred.push(async function(OneSignal) {
    await OneSignal.init({
      appId: "YOUR_ONESIGNAL_APP_ID",
      notifyButton: { enable: false }, // We use a custom prompt
    });
  });
</script>
```

**For FCM (web):**
Install Firebase SDK and register the messaging service worker. See `fcm-send-notification` fundamental for full setup.

**For raw Web Push:**
Register a service worker and generate VAPID keys. See `web-push-service-worker` fundamental.

### 3. Build the Opt-In Prompt

Never use the browser's default permission dialog on page load. Build a soft prompt:

1. **Trigger timing**: Show after the user completes a meaningful action (first task completed, account setup finished, 3rd session)
2. **Soft prompt**: Display a banner or modal within your UI explaining what notifications they will receive. Example: "Get notified when teammates comment on your work or when your weekly report is ready."
3. **Clear value proposition**: State the specific notification types, not just "Enable notifications"
4. **On accept**: Call the browser permission API (or OneSignal's `setSubscription(true)`)
5. **On dismiss**: Store the dismissal in PostHog and do not show again for 14 days
6. **On deny**: The browser blocks further requests. Log this in PostHog as `push_permission_denied`

### 4. Track Push Events in PostHog

Using `posthog-custom-events`, instrument these events:

| Event | When | Properties |
|-------|------|------------|
| `push_prompt_shown` | Soft prompt displayed | `trigger_reason`, `session_number` |
| `push_permission_granted` | User accepts push | `provider`, `platform` (web/android/ios) |
| `push_permission_denied` | User denies push | `provider`, `prompt_type` |
| `push_sent` | Notification sent to user | `campaign_id`, `notification_type`, `segment` |
| `push_delivered` | Confirmed delivery | `campaign_id`, `platform` |
| `push_clicked` | User taps/clicks notification | `campaign_id`, `notification_type`, `deep_link` |
| `push_dismissed` | User dismisses notification | `campaign_id` |
| `push_unsubscribed` | User disables push | `reason` (if captured) |

### 5. Build the Subscription Sync Workflow

Using `n8n-workflow-basics`, create an n8n workflow that keeps push subscription status in sync:

1. When a user grants push permission, the app posts to your API
2. n8n receives the webhook and updates the user's CRM record (Attio) with `push_subscribed: true` and the subscription date
3. n8n sets the user's OneSignal tags to match their CRM properties (plan, lifecycle stage, feature usage)
4. When a user unsubscribes, reverse the process: update CRM, remove tags

### 6. Verify the Integration

Send a test notification to yourself:
- Use `onesignal-send-notification` to send to your own external_id
- Verify the notification appears on your device/browser
- Verify the `push_sent`, `push_delivered`, and `push_clicked` events fire in PostHog
- Verify the subscription status synced to your CRM

## Output

- Push notification SDK integrated and configured
- Custom opt-in prompt deployed (not browser default)
- PostHog event tracking for the full push lifecycle
- n8n workflow syncing subscription status to CRM
- Verified end-to-end: send -> deliver -> click -> tracked
