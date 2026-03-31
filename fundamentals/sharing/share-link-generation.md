---
name: share-link-generation
description: Generate unique, tracked share URLs with attribution for viral loop tracking
tool: Dub.co
difficulty: Setup
---

# Share Link Generation

Create unique, trackable share URLs for each user and each shareable resource. Every share link carries attribution (who shared, what they shared, where they shared it) so the viral loop funnel is fully measurable.

## Approach

Generate a short URL per (user, resource, channel) tuple. When a recipient clicks the link, record the click with full attribution, then redirect to the shared resource. The click data feeds the viral coefficient calculation.

## Tools (pick one)

| Tool | Method | Strengths |
|------|--------|-----------|
| **Custom API** | Your own `/api/share` endpoint + database table | Full control, no external dependency, free |
| **Dub.co** | REST API for branded short links | Built-in analytics, team features, generous free tier (1,000 links/mo) |
| **Short.io** | REST API for custom-domain short links | Custom domains, bulk creation, API-first |
| **Rebrandly** | REST API for branded links | Enterprise features, UTM builder |
| **Bitly** | REST API for short links | Widely recognized, but limited free tier |

## Implementation (Custom API — default stack)

### 1. Create the share links table

```sql
CREATE TABLE share_links (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  short_code VARCHAR(12) UNIQUE NOT NULL,
  sharer_user_id UUID NOT NULL REFERENCES users(id),
  resource_type VARCHAR(50) NOT NULL,  -- 'dashboard', 'report', 'achievement', 'workspace'
  resource_id UUID NOT NULL,
  channel VARCHAR(20),  -- 'twitter', 'linkedin', 'email', 'slack', 'copy'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  click_count INT DEFAULT 0,
  signup_count INT DEFAULT 0,
  metadata JSONB DEFAULT '{}'
);

CREATE TABLE share_clicks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  share_link_id UUID NOT NULL REFERENCES share_links(id),
  clicked_at TIMESTAMPTZ DEFAULT NOW(),
  referrer VARCHAR(500),
  user_agent VARCHAR(500),
  ip_hash VARCHAR(64),
  converted BOOLEAN DEFAULT FALSE,
  converted_user_id UUID
);
```

### 2. Generate share link endpoint

```
POST /api/share
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "resource_type": "dashboard",
  "resource_id": "abc-123",
  "channel": "linkedin"
}

Response 201:
{
  "share_url": "https://yourapp.com/s/Xk9mP2",
  "og_image_url": "https://yourapp.com/api/og?title=My+Dashboard&user=Jane",
  "share_text": "Check out my dashboard on YourProduct"
}
```

The endpoint:
1. Generates a unique `short_code` (6-8 alphanumeric characters)
2. Creates the `share_links` row
3. Returns the share URL, pre-generated OG image URL, and suggested share text
4. Fires a PostHog event: `share_link_created` with properties `resource_type`, `resource_id`, `channel`

### 3. Handle share link clicks

```
GET /s/{short_code}
```

The redirect handler:
1. Looks up the `share_links` row by `short_code`
2. Increments `click_count`
3. Creates a `share_clicks` row with referrer, user agent, IP hash
4. Fires a PostHog event: `share_link_clicked` with properties `sharer_user_id`, `resource_type`, `channel`
5. Sets a first-party cookie `ref={short_code}` (30-day expiry) for signup attribution
6. Redirects (302) to the shared resource URL with `?ref={short_code}` query parameter

### 4. Track conversions

When a new user signs up, check for the `ref` cookie or query parameter:
1. Look up the `share_links` row by `short_code`
2. Increment `signup_count` on the share link
3. Update the `share_clicks` row: set `converted = TRUE`, `converted_user_id`
4. Fire PostHog event: `share_referral_converted` with `sharer_user_id`, `referee_user_id`, `resource_type`, `channel`
5. Notify the sharer (via Intercom or Loops) that their share led to a signup

## Implementation (Dub.co API)

```bash
# Create a share link via Dub.co API
curl -X POST https://api.dub.co/links \
  -H "Authorization: Bearer {DUB_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/shared/dashboard/abc-123?ref=user_456",
    "domain": "share.yourapp.com",
    "key": "Xk9mP2",
    "tagIds": ["share", "dashboard"],
    "externalId": "user_456_dashboard_abc-123_linkedin"
  }'
```

Retrieve click analytics:
```bash
curl "https://api.dub.co/analytics?linkId={link_id}&event=clicks&interval=30d" \
  -H "Authorization: Bearer {DUB_API_KEY}"
```

## Error Handling

- Duplicate short code: regenerate with retry (collision probability is negligible with 8-char alphanumeric codes)
- Resource not found: redirect to a generic "this content is no longer available" page with a signup CTA
- Rate limiting: cap share link creation at 50/user/day to prevent abuse
