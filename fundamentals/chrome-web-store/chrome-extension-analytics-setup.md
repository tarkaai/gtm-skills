---
name: chrome-extension-analytics-setup
description: Instrument a Chrome extension with PostHog analytics to track installs, popup opens, and lead capture events
tool: PostHog
difficulty: Config
---

# Chrome Extension Analytics Setup

Instrument a Chrome extension with event tracking so you can measure installs, engagement, and lead capture. Chrome extensions cannot use standard web analytics (no page views), so you must send events explicitly via API.

## PostHog Setup for Extensions

Chrome extensions run in a sandboxed environment. You cannot include PostHog's standard JS snippet. Instead, use the PostHog API directly.

### Option 1: PostHog API (Recommended for Teaser Extensions)

Send events directly from the extension's popup or background script:

```javascript
// analytics.js — include in your extension
const POSTHOG_API_KEY = 'phc_YOUR_PROJECT_KEY';
const POSTHOG_HOST = 'https://us.i.posthog.com'; // or eu.i.posthog.com

async function trackEvent(eventName, properties = {}) {
  const distinctId = await getOrCreateDistinctId();
  await fetch(`${POSTHOG_HOST}/capture/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: POSTHOG_API_KEY,
      event: eventName,
      distinct_id: distinctId,
      properties: {
        ...properties,
        $lib: 'chrome-extension',
        extension_version: chrome.runtime.getManifest().version,
        source: 'chrome-web-store-teaser'
      }
    })
  });
}

async function getOrCreateDistinctId() {
  const result = await chrome.storage.local.get('distinct_id');
  if (result.distinct_id) return result.distinct_id;
  const id = crypto.randomUUID();
  await chrome.storage.local.set({ distinct_id: id });
  return id;
}
```

### Required Events to Track

| Event Name | When Fired | Properties |
|-----------|------------|------------|
| `extension_installed` | `chrome.runtime.onInstalled` in background.js | `install_reason` (install, update, chrome_update) |
| `popup_opened` | When popup.html loads | `page` (popup) |
| `waitlist_form_submitted` | Form submission in popup | `email_domain`, `referrer` |
| `feature_preview_clicked` | User clicks a feature preview | `feature_name` |
| `extension_uninstalled` | Set via `chrome.runtime.setUninstallURL()` | Tracked via uninstall survey landing page |

### Background Script Event Tracking

```javascript
// background.js
import { trackEvent } from './analytics.js';

chrome.runtime.onInstalled.addListener((details) => {
  trackEvent('extension_installed', {
    install_reason: details.reason,
    previous_version: details.previousVersion || null
  });

  // Set uninstall URL for exit survey
  chrome.runtime.setUninstallURL(
    'https://yoursite.com/extension-uninstall?source=chrome-web-store-teaser'
  );
});
```

### Popup Event Tracking

```javascript
// popup.js
import { trackEvent } from './analytics.js';

// Track popup opens
trackEvent('popup_opened');

// Track form submissions
document.getElementById('waitlist').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  trackEvent('waitlist_form_submitted', {
    email_domain: email.split('@')[1]
  });
  // Send to your backend / Loops API
});
```

### Permissions Required

Add to `manifest.json`:
```json
{
  "permissions": ["storage"],
  "host_permissions": [
    "https://us.i.posthog.com/*",
    "https://yoursite.com/*"
  ]
}
```

## Verifying Events

1. Install the extension locally (`chrome://extensions` > Load unpacked)
2. Open the popup, submit a test form
3. Check PostHog > Activity > Live Events for incoming events
4. Verify `distinct_id` persists across popup opens (check `chrome.storage.local`)

## Error Handling

- If `fetch` fails (network error), queue events in `chrome.storage.local` and retry on next popup open
- PostHog API returns 200 for valid events. A 400 response means malformed payload — check `api_key` and `event` fields
- Chrome extensions have a 5MB storage limit for `chrome.storage.local`. Flush queued events before approaching this limit
