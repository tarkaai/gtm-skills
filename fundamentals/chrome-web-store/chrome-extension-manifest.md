---
name: chrome-extension-manifest
description: Build and configure a Chrome extension manifest.json with proper permissions, icons, and metadata
tool: Google
product: Chrome Extensions
difficulty: Setup
---

# Chrome Extension Manifest

Create a valid `manifest.json` for a Chrome extension. This is the required configuration file that defines the extension's name, version, permissions, and behavior.

## Manifest V3 Template (Current Standard)

```json
{
  "manifest_version": 3,
  "name": "Your Extension Name",
  "version": "0.1.0",
  "description": "One sentence describing what this extension does for the user.",
  "icons": {
    "16": "icons/icon16.png",
    "32": "icons/icon32.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "32": "icons/icon32.png"
    }
  },
  "permissions": [],
  "host_permissions": [],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ]
}
```

## Key Fields for a Teaser Extension

For a minimal teaser extension (proof-of-concept to validate market interest):

- **name**: Use keywords your ICP would search for. Max 45 characters.
- **description**: Lead with the pain point, then the solution. Max 132 characters displayed in search results.
- **version**: Start at `0.1.0`. Increment on each update.
- **permissions**: Request ONLY what you need. Fewer permissions = higher install rate. Common teaser permissions: `storage`, `activeTab`, `tabs`.
- **icons**: Required sizes: 16x16 (toolbar), 32x32 (Windows), 48x48 (extensions page), 128x128 (store listing). Use PNG format.
- **action.default_popup**: The HTML file shown when the user clicks the extension icon. For a teaser, this is your primary UI and lead capture surface.

## Building the Extension Zip

```bash
# Directory structure
mkdir -p extension/icons
# Create manifest.json, popup.html, popup.js, background.js, content.js
# Add icon files

# Package for upload
cd extension && zip -r ../extension.zip . -x ".*"
```

## Validation

Before uploading, validate locally:

1. Open `chrome://extensions/` in Chrome
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked" and select the extension directory
4. Verify: popup opens, permissions prompt is acceptable, no console errors

Common validation errors:
- `manifest_version` must be `3` (v2 is deprecated)
- Icon files must exist at the paths specified
- `service_worker` path must be relative to extension root
- Permissions must be from the allowed list: https://developer.chrome.com/docs/extensions/reference/permissions-list

## Lead Capture in the Popup

For a teaser extension, the popup should:

1. Show a brief value proposition (2-3 sentences)
2. Provide a preview of the functionality or a "coming soon" feature list
3. Include an email capture form that sends to your backend or a service like Loops
4. Track popup opens and form submissions via PostHog or a custom analytics endpoint

```html
<!-- popup.html minimal structure -->
<!DOCTYPE html>
<html>
<head><style>body { width: 350px; padding: 16px; font-family: system-ui; }</style></head>
<body>
  <h2>Extension Name</h2>
  <p>Brief value prop describing what this will do.</p>
  <form id="waitlist">
    <input type="email" id="email" placeholder="your@email.com" required>
    <button type="submit">Get Early Access</button>
  </form>
  <script src="popup.js"></script>
</body>
</html>
```
