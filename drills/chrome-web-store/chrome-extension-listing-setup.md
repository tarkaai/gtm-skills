---
name: chrome-extension-listing-setup
description: Scaffold, build, and publish a minimal Chrome extension with lead capture popup to the Chrome Web Store
category: Chrome Web Store
tools:
  - Chrome Web Store
  - PostHog
  - Loops
fundamentals:
  - chrome-extension-manifest
  - chrome-web-store-api
  - chrome-extension-analytics-setup
  - chrome-web-store-listing-optimization
  - loops-audience
---

# Chrome Extension Listing Setup

This drill walks an agent through building a minimal Chrome extension, instrumenting it with analytics, and publishing it to the Chrome Web Store. The extension serves as a teaser — a lightweight proof-of-concept that validates whether your ICP discovers and installs browser extensions for this problem space.

## Input

- Product name and one-sentence value proposition
- ICP definition (who would search for this type of extension)
- 3-5 keywords your ICP would search in the Chrome Web Store
- Email capture endpoint (Loops API or custom backend URL)

## Steps

### 1. Scaffold the extension

Using the `chrome-extension-manifest` fundamental, create the extension directory structure:

```
extension/
  manifest.json
  popup.html
  popup.js
  background.js
  analytics.js
  icons/
    icon16.png
    icon32.png
    icon48.png
    icon128.png
  styles/
    popup.css
```

Configure `manifest.json` with:
- `name`: Primary keyword + brand (max 45 chars)
- `description`: Pain point + solution (max 132 chars)
- `permissions`: `["storage"]`
- `host_permissions`: PostHog API host + your backend domain
- `action.default_popup`: `popup.html`

### 2. Build the teaser popup

Create `popup.html` with:
- Extension name as heading
- 2-3 sentence value proposition
- Preview of 2-3 features (can be mockups or "coming soon" labels)
- Email capture form with a single field + submit button ("Get Early Access" or "Join Waitlist")
- Link to your product landing page

Keep the popup under 400px wide, under 500px tall. Use system fonts. No external CSS frameworks (they bloat the extension and slow popup load).

### 3. Instrument analytics

Using the `chrome-extension-analytics-setup` fundamental:
- Add PostHog API tracking to `analytics.js`
- Track `extension_installed` in `background.js` via `chrome.runtime.onInstalled`
- Track `popup_opened` on popup load
- Track `waitlist_form_submitted` on form submit
- Set `chrome.runtime.setUninstallURL()` to your uninstall survey page

### 4. Connect lead capture to Loops

Using the `loops-audience` fundamental:
- On form submission, POST the email to Loops API to add the contact to a "Chrome Extension Waitlist" audience
- Tag the contact with `source: chrome-web-store-teaser`
- Trigger a welcome transactional email confirming their waitlist signup

### 5. Validate locally

Load the extension unpacked in Chrome:
1. Navigate to `chrome://extensions/`
2. Enable Developer Mode
3. Click "Load unpacked" and select the extension directory
4. Click the extension icon — verify popup renders correctly
5. Submit a test email — verify it appears in Loops and PostHog
6. Check `chrome://extensions/` for any error badges

### 6. Package and publish

Using the `chrome-web-store-api` fundamental:
1. Package: `cd extension && zip -r ../extension.zip . -x ".*"`
2. Upload to Chrome Web Store via API
3. Fill out store listing details using `chrome-web-store-listing-optimization` fundamental:
   - Detailed description with keyword-optimized copy
   - 3-5 screenshots showing the popup and value proposition
   - Select the most specific category (Developer Tools or Productivity)
   - Add privacy policy URL (required for extensions requesting permissions)
4. Submit for review

**Human action required:** Pay the $5 Chrome Web Store developer registration fee (one-time). Create or provide a privacy policy URL. Approve the final listing before publish.

### 7. Log the listing in CRM

Create an Attio record for this extension listing:
- Name: Extension name
- Channel: Chrome Web Store
- URL: Store listing URL (available after publish)
- Status: Under Review / Published
- Metrics to track: impressions, installs, leads

## Output

- A published Chrome extension on the Chrome Web Store
- PostHog tracking for installs, popup opens, and waitlist signups
- Leads flowing into Loops with proper tagging
- CRM record for tracking listing performance

## Triggers

Run once at Smoke level. Re-run when making major extension updates at higher levels.
