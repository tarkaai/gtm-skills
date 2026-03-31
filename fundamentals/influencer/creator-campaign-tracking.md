---
name: creator-campaign-tracking
description: Track clicks, leads, and conversions from a creator-sponsored post using UTM links and PostHog
tool: PostHog / Attio / n8n
difficulty: Setup
---

# Creator Campaign Tracking

Measure the performance of each creator-sponsored post by tracking UTM-tagged link clicks through to leads and conversions. This fundamental covers setting up the tracking infrastructure and pulling results.

## Step 1: Generate UTM Links

For each creator post, generate a unique tracking URL:

```
Base URL: https://yoursite.com/landing-page
Parameters:
  utm_source={{creator_handle}}       (e.g., "saasmarketer")
  utm_medium=influencer               (always "influencer" for this play)
  utm_campaign={{campaign_slug}}       (e.g., "micro-influencer-b2b-creators-smoke")
  utm_content={{post_format}}          (e.g., "linkedin-post", "newsletter", "youtube")
```

Full URL example:
```
https://yoursite.com/landing?utm_source=saasmarketer&utm_medium=influencer&utm_campaign=micro-influencer-b2b-creators-smoke&utm_content=linkedin-post
```

Shorten with a branded link if needed (Rebrandly, Bitly). Some creators prefer shorter URLs.

## Step 2: Configure PostHog Event Capture

Using the `posthog-custom-events` fundamental, ensure these events fire on the landing page:

### Page View (automatic with PostHog snippet)
PostHog auto-captures `$pageview` with UTM parameters stored as properties.

### Form Submission / Lead Capture
```javascript
posthog.capture('influencer_lead_captured', {
  creator_handle: new URLSearchParams(window.location.search).get('utm_source'),
  campaign: new URLSearchParams(window.location.search).get('utm_campaign'),
  post_format: new URLSearchParams(window.location.search).get('utm_content'),
  lead_email: formData.email,
  lead_company: formData.company
});
```

### Meeting Booked (if using Cal.com)
```javascript
// Cal.com webhook fires on booking confirmation
// In n8n, receive the webhook and forward to PostHog:
posthog.capture('influencer_meeting_booked', {
  creator_handle: booking.utm_source,
  campaign: booking.utm_campaign,
  lead_email: booking.email
});
```

## Step 3: Build PostHog Funnel

Using the `posthog-funnels` fundamental, create a funnel insight:

1. `$pageview` where `$utm_medium = influencer`
2. `influencer_lead_captured`
3. `influencer_meeting_booked` (if applicable)

Break down by `$utm_source` (creator handle) to compare creator performance.

### PostHog API Query
```
POST https://app.posthog.com/api/projects/{PROJECT_ID}/insights/funnel
Authorization: Bearer {POSTHOG_API_KEY}
Content-Type: application/json

{
  "events": [
    {"id": "$pageview", "properties": [{"key": "$utm_medium", "value": "influencer"}]},
    {"id": "influencer_lead_captured"},
    {"id": "influencer_meeting_booked"}
  ],
  "breakdown": "$utm_source",
  "date_from": "-14d"
}
```

## Step 4: Sync Leads to Attio

Using the `attio-contacts` fundamental, create or update a contact for each captured lead:

```
POST https://api.attio.com/v2/objects/people/records
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json

{
  "data": {
    "values": {
      "email_addresses": [{"email_address": "{{lead_email}}"}],
      "name": [{"first_name": "{{first}}", "last_name": "{{last}}"}],
      "lead_source": [{"value": "influencer"}],
      "influencer_source": [{"value": "{{creator_handle}}"}],
      "campaign": [{"value": "{{campaign_slug}}"}]
    }
  }
}
```

## Step 5: Calculate Creator-Level Metrics

For each creator, compute:

- **Clicks:** Count of `$pageview` where `$utm_source = {{creator_handle}}`
- **Leads:** Count of `influencer_lead_captured` where `creator_handle = {{creator_handle}}`
- **Conversion rate:** Leads / Clicks
- **Cost per lead (CPL):** Creator fee / Leads
- **Cost per click (CPC):** Creator fee / Clicks

Store these in Attio on the creator's contact record for comparison.

## Error Handling

- **UTM parameters stripped:** Some platforms strip UTM params on redirect. Test the full link before sending to the creator. If stripped, use a dedicated landing page per creator instead (e.g., `yoursite.com/creator/saasmarketer`).
- **Zero clicks but post is live:** Verify the creator used the correct link. Check for typos. If they used a different URL, ask them to update.
- **PostHog events not firing:** Check the PostHog snippet is on the landing page. Use PostHog's toolbar to debug event capture in real time.
- **Duplicate leads:** Use Attio's deduplication on email address to prevent double-counting.
