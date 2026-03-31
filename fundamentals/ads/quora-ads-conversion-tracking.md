---
name: quora-ads-conversion-tracking
description: Install the Quora Pixel, configure conversion events, and set up server-side Conversion API (CAPI) for Quora Ads attribution
tool: Quora Ads
difficulty: Setup
---

# Quora Ads — Conversion Tracking

Set up end-to-end conversion tracking for Quora Ads using the Quora Pixel (client-side) and Conversion API (CAPI, server-side). Both methods work together for maximum match rate.

## Components

1. **Quora Pixel (Base)**: JavaScript snippet installed on every page. Tracks page views and enables audience building.
2. **Quora Pixel (Event)**: Additional JS calls that fire on specific conversion events (form submit, signup, purchase).
3. **Conversion API (CAPI)**: Server-to-server integration that sends conversion events directly to Quora. Improves match rate when cookies are blocked.
4. **qclid**: Quora click identifier appended to landing page URLs. Captured on page load and sent back via CAPI to match conversions to ad clicks.

## Step 1: Install the Base Pixel

### Direct installation

Add the Quora Pixel base code to the `<head>` section of every page on your website:

```html
<script>
!function(q,e,v,n,t,s){if(q.qp) return; n=q.qp=function(){n.qp?n.qp.apply(n,arguments):n.queue.push(arguments)}; n.queue=[];t=document.createElement(e);t.async=!0;t.src=v; s=document.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t,s)}(window,'script','https://a.quora.com/qevents.js');
qp('init', 'YOUR_PIXEL_ID');
qp('track', 'ViewContent');
</script>
<noscript>
<img height="1" width="1" style="display:none" src="https://q.quora.com/_/ad/YOUR_PIXEL_ID/pixel?tag=ViewContent&noscript=1"/>
</noscript>
```

Replace `YOUR_PIXEL_ID` with your pixel ID from Ads Manager > Pixel & Events.

### Google Tag Manager installation

1. In GTM, create a new **Tag**
2. Tag type: search for **Quora Pixel** (built-in template)
3. Enter your Quora Pixel ID
4. Event type: **Page View**
5. Trigger: **All Pages**
6. Save and publish

### Webflow installation

1. In Webflow project settings > **Custom Code** > **Head Code**
2. Paste the base pixel snippet
3. Publish the site

## Step 2: Configure Conversion Events

Fire event pixels on specific conversion actions. Standard event types:

| Event | When to Fire | Pixel Call |
|-------|-------------|------------|
| `ViewContent` | Page load (already in base pixel) | `qp('track', 'ViewContent')` |
| `Lead` | Form submission, email capture | `qp('track', 'Lead')` |
| `CompleteRegistration` | Account signup, trial start | `qp('track', 'CompleteRegistration')` |
| `AddToCart` | Pricing page visit (B2B proxy) | `qp('track', 'AddToCart')` |
| `Purchase` | Closed deal, subscription start | `qp('track', 'Purchase')` |
| `GenerateLead` | Lead Gen Form submission | `qp('track', 'GenerateLead')` |

### Implementation example (form submission)

```javascript
// Fire on successful form submit
document.getElementById('demo-form').addEventListener('submit', function() {
  qp('track', 'Lead');
});
```

### GTM implementation

1. Create a new Quora Pixel tag for each event
2. Set the event type (e.g., Lead)
3. Trigger: custom event matching your form submission (e.g., `formSubmission` dataLayer event)

## Step 3: Capture qclid

When a user clicks a Quora ad, Quora appends `qclid=XXXX` to the destination URL. Capture this on page load and store it for CAPI.

```javascript
// Capture qclid from URL and store in cookie/localStorage
(function() {
  var params = new URLSearchParams(window.location.search);
  var qclid = params.get('qclid');
  if (qclid) {
    localStorage.setItem('quora_qclid', qclid);
    document.cookie = 'quora_qclid=' + qclid + '; max-age=2592000; path=/; SameSite=Lax';
  }
})();
```

Install this snippet alongside the base pixel on all landing pages.

## Step 4: Set Up Conversion API (CAPI)

CAPI sends conversion events server-to-server, bypassing cookie restrictions. Required for accurate attribution in 2025+.

### Generate API Token

1. In Ads Manager, go to **Pixel & Events** > **Conversion API**
2. Click **Generate Token**
3. Store the token securely (environment variable, secret manager)

### Send Conversion Events

```bash
curl -X POST "https://ads-api.quora.com/conversion" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_CAPI_TOKEN" \
  -d '{
    "account_id": "YOUR_AD_ACCOUNT_ID",
    "events": [
      {
        "event_type": "Lead",
        "event_time": "2026-04-01T14:30:00Z",
        "click_id": "CAPTURED_QCLID",
        "event_id": "unique-event-id-123",
        "user": {
          "email_hash": "SHA256_HASHED_EMAIL",
          "ip_address": "USER_IP"
        },
        "custom_data": {
          "currency": "USD",
          "value": 0
        }
      }
    ]
  }'
```

### n8n CAPI Workflow

Build an n8n workflow triggered by PostHog webhook or form submission:

1. **Trigger**: Webhook from PostHog on `quora_ads_lead_captured` event
2. **Extract**: qclid from event properties (stored in PostHog from the landing page capture)
3. **Hash**: SHA-256 hash the user's email address
4. **Send**: HTTP Request node POST to `https://ads-api.quora.com/conversion` with the event payload
5. **Log**: Store the CAPI response in Attio as a note on the contact record

## Step 5: Verify Tracking

1. **Quora Pixel Helper**: Install the browser extension. Visit your landing page and verify the pixel fires.
2. **Ads Manager Event Testing**: In Pixel & Events, use the Test Events tool to verify events arrive.
3. **CAPI verification**: Send a test event via CAPI and confirm it appears in Ads Manager within minutes.
4. **PostHog cross-check**: Verify that PostHog receives the same events (page view, form submit) that Quora pixel tracks.

## Parallel PostHog Events

Fire PostHog events alongside Quora events for unified reporting:

```javascript
// On page load (alongside Quora ViewContent)
posthog.capture('quora_ads_page_view', {
  utm_source: 'quora',
  utm_medium: 'paid',
  utm_campaign: new URLSearchParams(window.location.search).get('utm_campaign'),
  utm_content: new URLSearchParams(window.location.search).get('utm_content'),
  qclid: new URLSearchParams(window.location.search).get('qclid')
});

// On form submit (alongside Quora Lead)
posthog.capture('quora_ads_lead_captured', {
  utm_source: 'quora',
  utm_campaign: new URLSearchParams(window.location.search).get('utm_campaign'),
  qclid: localStorage.getItem('quora_qclid'),
  email: userEmail // for PostHog person identification
});
```

## Error Handling

- **Pixel not firing**: Check for ad blockers, CSP headers blocking `a.quora.com`, or GTM container not published.
- **CAPI 401**: Token expired or invalid. Regenerate in Ads Manager.
- **CAPI 400**: Malformed payload. Check required fields: `event_type`, `event_time`, `account_id`.
- **Low match rate**: Ensure qclid capture is working. Check that qclid cookie persists across page navigations.
- **Duplicate events**: Use unique `event_id` in CAPI payloads to deduplicate between pixel and CAPI.
