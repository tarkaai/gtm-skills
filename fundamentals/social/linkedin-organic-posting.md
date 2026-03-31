---
name: linkedin-organic-posting
description: Publish text, image, and document posts to LinkedIn via API or scheduling tools
tool: LinkedIn
difficulty: Setup
---

# Publish LinkedIn Posts Programmatically

## Prerequisites
- LinkedIn account with Creator Mode enabled (see `linkedin-organic-profile`)
- One of: LinkedIn API access (OAuth app), Taplio account, Buffer account, or Typefully account

## Option A: LinkedIn API (Direct)

1. **Register a LinkedIn app.** Go to https://www.linkedin.com/developers/apps and create an app. Request the `w_member_social` scope (required for posting). Complete verification by associating a LinkedIn Company Page you admin.

2. **Obtain an OAuth2 access token.** Use the 3-legged OAuth flow:
   ```
   GET https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20profile%20w_member_social
   ```
   Exchange the authorization code for an access token:
   ```
   POST https://www.linkedin.com/oauth/v2/accessToken
   Content-Type: application/x-www-form-urlencoded
   grant_type=authorization_code&code={CODE}&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}
   ```
   Tokens expire in 60 days. Store securely and refresh before expiry.

3. **Get the author URN.** Call the userinfo endpoint to get your member ID:
   ```
   GET https://api.linkedin.com/v2/userinfo
   Authorization: Bearer {ACCESS_TOKEN}
   ```
   Your author URN is `urn:li:person:{sub}`.

4. **Create a text post.**
   ```
   POST https://api.linkedin.com/rest/posts
   Authorization: Bearer {ACCESS_TOKEN}
   LinkedIn-Version: 202401
   Content-Type: application/json

   {
     "author": "urn:li:person:{MEMBER_ID}",
     "commentary": "Your post text goes here.\n\nLine breaks work with \\n.\n\nInclude your hook in the first line.",
     "visibility": "PUBLIC",
     "distribution": {
       "feedDistribution": "MAIN_FEED",
       "targetEntities": [],
       "thirdPartyDistributionChannels": []
     },
     "lifecycleState": "PUBLISHED"
   }
   ```
   Response: `201 Created` with the post URN in the `x-restli-id` header.

5. **Create an image post.** First upload the image:
   ```
   POST https://api.linkedin.com/rest/images?action=initializeUpload
   {
     "initializeUploadRequest": {
       "owner": "urn:li:person:{MEMBER_ID}"
     }
   }
   ```
   Upload the binary to the returned `uploadUrl` via PUT, then reference the `image` URN in the post:
   ```json
   {
     "author": "urn:li:person:{MEMBER_ID}",
     "commentary": "Post text here",
     "visibility": "PUBLIC",
     "distribution": { "feedDistribution": "MAIN_FEED" },
     "content": {
       "media": {
         "id": "urn:li:image:{IMAGE_ID}"
       }
     },
     "lifecycleState": "PUBLISHED"
   }
   ```

6. **Create a document/carousel post.** Upload a PDF the same way using the documents endpoint:
   ```
   POST https://api.linkedin.com/rest/documents?action=initializeUpload
   ```
   Then reference `urn:li:document:{DOC_ID}` in the post content.

## Option B: Taplio API

1. **Get your Taplio API key** from Settings > API in the Taplio dashboard.

2. **Schedule a post via Taplio API:**
   ```
   POST https://app.taplio.com/api/v1/post/schedule
   X-API-KEY: {TAPLIO_API_KEY}
   Content-Type: application/json

   {
     "text": "Your post content here",
     "scheduledDate": "2026-04-01T08:00:00Z"
   }
   ```

3. **Publish immediately:**
   ```
   POST https://app.taplio.com/api/v1/post/publish
   X-API-KEY: {TAPLIO_API_KEY}
   Content-Type: application/json

   {
     "text": "Your post content here"
   }
   ```

## Option C: Buffer API

1. **Get a Buffer access token** from https://buffer.com/developers.

2. **Publish or schedule:**
   ```
   POST https://api.bufferapp.com/1/updates/create.json
   access_token={TOKEN}&profile_ids[]={LINKEDIN_PROFILE_ID}&text=Your+post+content&scheduled_at=2026-04-01T08:00:00Z
   ```

## Option D: Typefully API

1. **Get your Typefully API key** from Settings > API.

2. **Create a draft (LinkedIn):**
   ```
   POST https://api.typefully.com/v1/drafts/
   X-API-KEY: {TYPEFULLY_API_KEY}
   Content-Type: application/json

   {
     "content": "Your post content here",
     "platform": "linkedin",
     "schedule-date": "2026-04-01T08:00:00.000Z"
   }
   ```

## Error Handling

- **401 Unauthorized**: Token expired. Re-authenticate.
- **403 Forbidden**: Missing `w_member_social` scope. Re-request permissions.
- **429 Rate Limited**: LinkedIn allows ~100 API calls per day for posting. Space calls across the day.
- **422 Content too long**: LinkedIn text posts max at 3,000 characters. Trim or split.
