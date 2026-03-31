---
name: web-push-service-worker
description: Set up browser push notifications using the Web Push API with VAPID keys and a service worker
tool: Web Push API
difficulty: Advanced
---

# Browser Push via Service Worker + VAPID

## Prerequisites
- Web application served over HTTPS
- Node.js backend (or equivalent) for sending push messages
- `web-push` npm package: `npm install web-push`

## Generate VAPID Keys

Run once to generate your application's VAPID key pair:

```bash
npx web-push generate-vapid-keys
```

Output:
```
Public Key: BN...long-base64-string
Private Key: shorter-base64-string
```

Store these as environment variables:
```
VAPID_PUBLIC_KEY=BN...
VAPID_PRIVATE_KEY=...
VAPID_SUBJECT=mailto:notifications@example.com
```

## Register the Service Worker (Client-Side)

```javascript
// In your app's main JavaScript
async function setupPush() {
  // 1. Register service worker
  const registration = await navigator.serviceWorker.register('/sw.js');

  // 2. Request permission
  const permission = await Notification.requestPermission();
  if (permission !== 'granted') return null;

  // 3. Subscribe to push
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
  });

  // 4. Send subscription to your backend
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: currentUserId,
      subscription: subscription.toJSON()
    })
  });

  return subscription;
}
```

## Service Worker (sw.js)

```javascript
// sw.js — handles incoming push events
self.addEventListener('push', function(event) {
  const data = event.data ? event.data.json() : {};
  const options = {
    body: data.body || 'New notification',
    icon: data.icon || '/icon-192.png',
    badge: data.badge || '/badge-72.png',
    image: data.image,
    data: { url: data.url || '/' },
    actions: data.actions || [],
    tag: data.tag,           // Replaces notification with same tag
    renotify: !!data.tag,    // Vibrate again on replace
    requireInteraction: data.requireInteraction || false
  };
  event.waitUntil(
    self.registration.showNotification(data.title || 'Notification', options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  const url = event.notification.data.url;
  event.waitUntil(
    clients.matchAll({type: 'window'}).then(function(clientList) {
      // Focus existing tab if open, otherwise open new one
      for (const client of clientList) {
        if (client.url === url && 'focus' in client) return client.focus();
      }
      return clients.openWindow(url);
    })
  );
});
```

## Send Push from Backend (Node.js)

```javascript
const webpush = require('web-push');

webpush.setVapidDetails(
  process.env.VAPID_SUBJECT,
  process.env.VAPID_PUBLIC_KEY,
  process.env.VAPID_PRIVATE_KEY
);

async function sendPush(subscription, payload) {
  try {
    await webpush.sendNotification(
      subscription,  // The PushSubscription object from the client
      JSON.stringify({
        title: 'New activity',
        body: 'Sarah commented on your project',
        url: 'https://app.example.com/projects/123',
        icon: 'https://app.example.com/icon-192.png',
        tag: 'project-123-comment'
      })
    );
  } catch (err) {
    if (err.statusCode === 410 || err.statusCode === 404) {
      // Subscription expired or invalid — remove from database
      await removeSubscription(subscription.endpoint);
    }
  }
}
```

## Opt-In Prompt Best Practices

Never request permission on page load. Instead:
1. Wait until the user performs a meaningful action (completes onboarding, saves a preference)
2. Show a soft prompt first explaining what notifications they will receive
3. Only call `Notification.requestPermission()` after the user clicks "Enable notifications" on your soft prompt
4. If denied, do not ask again — browsers block repeated requests

## Error Handling

- **410 Gone**: Subscription is no longer valid — the user unsubscribed or the browser expired the subscription. Remove it from your database.
- **404 Not Found**: Invalid subscription endpoint — remove from database.
- **413 Payload Too Large**: Push payload must be under 4096 bytes. Compress or send a data-only push with a fetch URL.
- **429 Too Many Requests**: Browser push service rate limiting — implement exponential backoff.

## Browser Support

Web Push is supported in Chrome, Firefox, Edge, and Safari 16+. Safari requires the same VAPID-based approach as other browsers since Safari 16.

## When to Use This vs OneSignal/Knock

Use raw Web Push when you want zero vendor dependency and full control over subscription management. Use OneSignal or Knock when you want managed segments, analytics, and cross-platform (mobile + web) from a single API.
