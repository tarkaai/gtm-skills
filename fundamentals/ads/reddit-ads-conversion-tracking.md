---
name: reddit-ads-conversion-tracking
description: Set up Reddit Pixel and Conversions API (CAPI) for server-side conversion tracking
tool: Reddit
product: Reddit Ads
difficulty: Config
---

# Reddit Ads — Conversion Tracking

Set up the Reddit Pixel (browser-side) and Reddit Conversions API (CAPI, server-side) to track ad-driven conversions. Use both together for maximum attribution accuracy.

## Reddit Pixel (Browser-Side)

The Reddit Pixel is a JavaScript tag that fires when users perform actions on your site.

### Install the Pixel

1. Log into Reddit Ads Manager at https://ads.reddit.com
2. Navigate to Events Manager -> Pixel
3. Copy your Pixel ID (format: `t2_XXXXXX`)

Add to your site's `<head>`:

```html
<script>
!function(w,d){if(!w.rdt){var p=w.rdt=function(){p.sendEvent?p.sendEvent.apply(p,arguments):p.callQueue.push(arguments)};p.callQueue=[];var t=d.createElement("script");t.src="https://www.redditstatic.com/ads/pixel.js";t.async=!0;var s=d.getElementsByTagName("script")[0];s.parentNode.insertBefore(t,s)}}(window,document);
rdt('init','PIXEL_ID');
rdt('track', 'PageVisit');
</script>
```

Replace `PIXEL_ID` with your actual pixel ID.

### Track Standard Events

Fire conversion events on key pages:

```javascript
// Landing page view
rdt('track', 'PageVisit');

// Form submit / lead capture
rdt('track', 'Lead');

// Demo booked or signup
rdt('track', 'SignUp');

// Custom event
rdt('track', 'Custom', { customEventName: 'demo_booked' });
```

Standard events recognized by Reddit:
- `PageVisit` — page view
- `ViewContent` — viewed specific content
- `Search` — performed a search
- `AddToCart` — added item to cart
- `AddToWishlist` — saved item
- `Lead` — submitted lead form
- `SignUp` — completed signup
- `Purchase` — completed purchase (include `value` and `currency`)
- `Custom` — custom event with your own name

### Event Properties

```javascript
rdt('track', 'Lead', {
  value: 50.00,
  currency: 'USD',
  transactionId: 'lead-12345',
  customEventName: 'paid-reddit-ads_lead_captured'
});
```

## Reddit Conversions API (CAPI, Server-Side)

CAPI sends conversion events server-to-server, bypassing ad blockers and browser cookie restrictions. Reddit recommends using both Pixel and CAPI together for redundancy.

### Generate Access Token

1. In Reddit Ads Manager, go to Events Manager -> Pixel Settings
2. Generate a Conversions API Access Token
3. Store securely (environment variable, never in code)

### Send Server-Side Events

```bash
curl -X POST https://ads-api.reddit.com/api/v2/conversions/events/{account_id} \
  -H "Authorization: Bearer CAPI_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test_mode": false,
    "events": [
      {
        "event_at": "2026-04-01T12:00:00Z",
        "event_type": {
          "tracking_type": "Lead"
        },
        "user": {
          "email": "sha256_hashed_email",
          "ip_address": "sha256_hashed_ip",
          "user_agent": "Mozilla/5.0...",
          "click_id": "rdt_cid_value_from_url"
        },
        "event_metadata": {
          "item_count": 1,
          "value_decimal": 50.00,
          "currency": "USD"
        }
      }
    ]
  }'
```

Key fields:
- `click_id`: Captured from the `rdt_cid` URL parameter when the user clicks your ad. This is critical for attribution.
- `email`: SHA-256 hashed, lowercase, trimmed. This enables cross-device matching.
- `ip_address`: SHA-256 hashed. Used for probabilistic matching.
- `event_at`: ISO 8601 timestamp. Must be within 7 days of the actual event.

### Capture the Click ID

When a user clicks your Reddit ad, Reddit appends `?rdt_cid=CLICK_ID` to your landing page URL. Capture and store this value:

```javascript
// On landing page load
const urlParams = new URLSearchParams(window.location.search);
const rdtClickId = urlParams.get('rdt_cid');
if (rdtClickId) {
  // Store in cookie or session for later CAPI calls
  document.cookie = `rdt_cid=${rdtClickId}; max-age=2592000; path=/; SameSite=Lax`;
}
```

Pass this `rdt_cid` value to your backend when the user converts, then include it in the CAPI event.

## PostHog Integration

Route Reddit conversion data to PostHog for unified reporting:

1. Fire PostHog events alongside Reddit events:

```javascript
// When a Reddit ad visitor converts
posthog.capture('lead_created', {
  source: 'reddit',
  channel: 'paid',
  campaign: 'paid-reddit-ads',
  reddit_click_id: rdtClickId,
  utm_source: 'reddit',
  utm_medium: 'paid'
});
```

2. In n8n, build a webhook workflow that:
   - Receives form submissions
   - Fires the Reddit CAPI event (server-side)
   - Creates the PostHog event (server-side)
   - Creates or updates the Attio contact

This ensures every conversion is tracked in Reddit (for ad optimization), PostHog (for unified analytics), and Attio (for sales follow-up).

## Deduplication

When using both Pixel and CAPI, Reddit deduplicates events using:
- `click_id` match (preferred)
- `email` hash match (fallback)
- `event_at` timestamp within 5-minute window

Always include `click_id` in CAPI events to ensure proper deduplication and prevent double-counting.

## Verification

After setup, verify tracking is working:

1. Open Reddit Ads Manager -> Events Manager -> Event Testing
2. Use Reddit Pixel Helper browser extension to confirm pixel fires
3. Send a test CAPI event with `"test_mode": true`
4. Confirm events appear in the Events Manager within 30 minutes
5. Check PostHog for the corresponding events with matching properties

## Error Handling

- **401 Unauthorized**: CAPI token expired or invalid. Regenerate.
- **400 Bad Request**: Missing required fields or invalid hash format. SHA-256 must be lowercase hex.
- **422 Unprocessable**: Event timestamp too old (>7 days). Send events within hours of occurrence.
- **429 Rate Limited**: Batch events (up to 1000 per request) to reduce API calls.
