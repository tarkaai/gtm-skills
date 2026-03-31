---
name: meta-ads-pixel-capi
description: Install Meta Pixel and configure the Conversions API for accurate tracking and attribution
tool: Meta
product: Meta Ads
difficulty: Intermediate
---

# Set Up Meta Pixel and Conversions API

## Prerequisites
- Meta Business Manager with Events Manager access
- Access to your website codebase and backend

## Steps

1. **Create a Pixel via API.** Use the Meta Marketing API to create a pixel:
   ```
   POST /act_<ad-account-id>/adspixels
   { "name": "My Website Pixel" }
   ```
   Note the pixel ID for installation.

2. **Install the pixel base code.** Add the Meta Pixel JavaScript snippet to every page in the `<head>` tag:
   ```html
   <script>!function(f,b,e,v,n,t,s){...}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
   fbq('init', '<pixel-id>');fbq('track', 'PageView');</script>
   ```

3. **Track standard events.** Add event code for key actions:
   ```javascript
   fbq('track', 'Lead', {value: 50.00, currency: 'USD'});  // Form submission
   fbq('track', 'CompleteRegistration');  // Sign-up
   ```

4. **Set up Conversions API (CAPI).** Send events server-side for better accuracy (especially with iOS privacy changes):
   ```
   POST /v18.0/<pixel-id>/events
   {
     "data": [{
       "event_name": "Lead",
       "event_time": 1711843200,
       "user_data": {"em": ["<sha256-hashed-email>"]},
       "event_source_url": "https://yoursite.com/thank-you",
       "event_id": "unique-event-id"
     }],
     "access_token": "<token>"
   }
   ```

5. **Deduplicate events.** Set the same `event_id` for pixel and CAPI events so Meta does not double-count conversions. This is critical for accurate attribution.

6. **Verify via API.** Check Events Manager data via the API to confirm events are received from both Pixel (Browser) and CAPI (Server). Target Event Match Quality score above 6.
