---
name: website-visitor-identification
description: Identify anonymous website visitors at the company or contact level using reverse-IP and pixel-based identification tools
tool: RB2B / Leadpipe / Koala / Clearbit Reveal / Leadfeeder
difficulty: Setup
---

# Website Visitor Identification

Deanonymize website visitors so you know which companies and contacts are browsing your site before they fill out a form. This is the foundation of first-party intent data.

## Tool Options

| Tool | Level | Match Rate | API | Pricing (2026) |
|------|-------|------------|-----|-----------------|
| RB2B | Contact | ~15-25% | REST + Webhooks | Free (150/mo), Pro+ $149/mo (300/mo) |
| Leadpipe | Contact | ~30-40% | REST + Webhooks | From $149/mo |
| Koala | Contact + Product | ~20-30% | REST + JS SDK | Free (250/mo), paid from $350/mo |
| Clearbit Reveal (Breeze Intelligence) | Company | ~60-70% company | REST API | From $45/mo (100 credits), ~$450/mo (1K) |
| Leadfeeder (Dealfront) | Company | ~50-60% company | REST API | Free (last 7 days), paid from $99/mo |

## Authentication

### RB2B
1. Sign up at `https://app.rb2b.com`
2. Install the pixel on your website — add the JS snippet to your site `<head>`:
   ```html
   <script>
   !function(){var e=document.createElement("script");e.type="text/javascript",e.async=!0,e.src="https://s.rb2b.io/rb2b.js?key=YOUR_PIXEL_ID";var t=document.getElementsByTagName("script")[0];t.parentNode.insertBefore(e,t)}();
   </script>
   ```
3. Generate an API key from Settings > Integrations for webhook/API access

### Koala
1. Sign up at `https://app.getkoala.com`
2. Install the Koala SDK on your website:
   ```html
   <script>
   !function(t){var k=window.ko=window.ko||[];k.queue=k.queue||[];
   var e=document.createElement("script");e.async=!0;
   e.src="https://cdn.getkoala.com/v1/YOUR_PROJECT_KEY/sdk.js";
   document.head.appendChild(e)}();
   </script>
   ```
3. API key available at Settings > API

### Clearbit Reveal
1. Requires HubSpot account (post-acquisition)
2. Enable Breeze Intelligence in HubSpot settings
3. API endpoint: `GET https://reveal.clearbit.com/v1/companies/find?ip=IP_ADDRESS`
4. Auth: Bearer token in header

### Leadfeeder
1. Install the Leadfeeder Tracker script on your site
2. API access via `https://api.leadfeeder.com/`
3. Auth: API token from Settings > Personal > API Tokens

## Core Operations

### Retrieve identified visitors (RB2B example)
```
GET https://api.rb2b.com/v1/visitors?start_date=2026-03-01&end_date=2026-03-30
Authorization: Bearer YOUR_API_KEY

Response:
{
  "visitors": [
    {
      "id": "vis_abc123",
      "email": "jane@acme.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "company": "Acme Corp",
      "title": "VP Engineering",
      "linkedin_url": "https://linkedin.com/in/janedoe",
      "pages_viewed": ["/pricing", "/case-studies", "/demo"],
      "visit_count": 3,
      "first_seen": "2026-03-15T10:30:00Z",
      "last_seen": "2026-03-28T14:22:00Z"
    }
  ]
}
```

### Set up webhook for real-time alerts (RB2B)
```
POST https://api.rb2b.com/v1/webhooks
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "url": "https://your-n8n-instance.com/webhook/rb2b-visitor",
  "events": ["visitor.identified"],
  "filters": {
    "pages": ["/pricing", "/demo", "/case-studies"],
    "visit_count_min": 2
  }
}
```

### Koala intent score retrieval
```
GET https://app.getkoala.com/api/v1/accounts?intent_score_min=70
Authorization: Bearer YOUR_API_KEY

Response:
{
  "accounts": [
    {
      "domain": "acme.com",
      "intent_score": 85,
      "signals": ["pricing_page_view", "docs_deep_read", "return_visitor"],
      "contacts": [
        {
          "email": "jane@acme.com",
          "activity_count": 12,
          "last_active": "2026-03-28"
        }
      ]
    }
  ]
}
```

## Error Handling

- **Rate limits**: RB2B allows 100 req/min, Koala 60 req/min, Clearbit 600 req/min. Implement exponential backoff on 429 responses.
- **No match found**: Not every visitor can be identified. Company-level tools match 50-70% of B2B traffic; contact-level tools match 15-40%. Expect misses.
- **Bot traffic**: Filter out known bot user agents before counting visitors. Most tools do this automatically but verify by checking for suspiciously high page counts from single IPs.
- **GDPR/Privacy**: Visitor identification must comply with local privacy laws. Ensure your cookie consent banner covers analytics and identification pixels. Koala and RB2B operate on first-party data principles but consult legal counsel for your jurisdiction.
