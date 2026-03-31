---
name: chrome-web-store-api
description: Interact with the Chrome Web Store API to publish, update, and query extension listings
tool: Google
product: Chrome Web Store
difficulty: Advanced
---

# Chrome Web Store API

Programmatic access to publish, update, and manage Chrome extension listings on the Chrome Web Store.

## Authentication

The Chrome Web Store API uses OAuth 2.0. Required setup:

1. Create a project in Google Cloud Console: `https://console.cloud.google.com/`
2. Enable the Chrome Web Store API: `https://console.cloud.google.com/apis/library/chromewebstore.googleapis.com`
3. Create OAuth 2.0 credentials (type: Desktop application)
4. Store `client_id` and `client_secret` in your environment or secrets manager
5. Obtain a refresh token via the OAuth consent flow:

```bash
# Step 1: Get authorization code (open this URL in a browser)
# https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&client_id=${CLIENT_ID}&redirect_uri=urn:ietf:wg:oauth:2.0:oob

# Step 2: Exchange code for refresh token
curl -X POST https://oauth2.googleapis.com/token \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "code=${AUTH_CODE}" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob"
```

Store the `refresh_token` from the response. Use it to get access tokens:

```bash
curl -X POST https://oauth2.googleapis.com/token \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "refresh_token=${REFRESH_TOKEN}" \
  -d "grant_type=refresh_token"
```

## Operations

### Upload a new extension

```bash
curl -X POST \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-api-version: 2" \
  -T extension.zip \
  "https://www.googleapis.com/upload/chromewebstore/v1.1/items"
```

Response includes `id` (the extension ID). Store this for future updates.

### Update an existing extension

```bash
curl -X PUT \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-api-version: 2" \
  -T extension.zip \
  "https://www.googleapis.com/upload/chromewebstore/v1.1/items/${EXTENSION_ID}"
```

### Publish an extension

```bash
# Publish to all users
curl -X POST \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-api-version: 2" \
  -H "Content-Length: 0" \
  "https://www.googleapis.com/chromewebstore/v1.1/items/${EXTENSION_ID}/publish"

# Publish to trusted testers only
curl -X POST \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-api-version: 2" \
  -H "Content-Length: 0" \
  "https://www.googleapis.com/chromewebstore/v1.1/items/${EXTENSION_ID}/publish?publishTarget=trustedTesters"
```

### Get extension metadata

```bash
curl -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-api-version: 2" \
  "https://www.googleapis.com/chromewebstore/v1.1/items/${EXTENSION_ID}?projection=DRAFT"
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Expired or invalid token | Refresh the access token using the refresh_token |
| 403 Forbidden | Missing API scope or no developer account | Verify OAuth scope includes `chromewebstore`, register at https://chrome.google.com/webstore/devconsole |
| 409 Conflict | Extension already published with this version | Increment version in manifest.json |
| 400 Bad Request | Invalid zip structure or manifest errors | Validate manifest.json format, ensure zip root contains manifest.json |

## Notes

- One-time registration fee: $5 for a Chrome Web Store developer account
- Review times: typically 1-3 business days for new extensions, faster for updates
- The API does not provide install counts or analytics - use Chrome Web Store Developer Dashboard or scrape the public listing
- Rate limits: 2,000 requests per day per project
