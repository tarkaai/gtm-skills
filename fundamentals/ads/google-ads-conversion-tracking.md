---
name: google-ads-conversion-tracking
description: Implement conversion tracking for Google Ads to measure which actions lead to sign-ups, demos, and purchases
tool: Google
product: Google Ads
difficulty: Intermediate
---

# Set Up Google Ads Conversion Tracking

## Prerequisites
- Google Ads account with API access
- Access to your website codebase or Google Tag Manager

## Steps

1. **Create a conversion action via API.** Use the Google Ads API to define conversion actions:
   ```
   POST /customers/<id>/conversionActions:mutate
   {
     "operations": [{
       "create": {
         "name": "Demo Requested",
         "type": "WEBPAGE",
         "category": "SUBMIT_LEAD_FORM",
         "value_settings": { "default_value": 200, "always_use_default_value": false },
         "counting_type": "ONE_PER_CLICK",
         "click_through_lookback_window_days": 30,
         "view_through_lookback_window_days": 1
       }
     }]
   }
   ```
   Set counting to ONE_PER_CLICK for lead gen, MANY_PER_CLICK for e-commerce.

2. **Install the Google Ads tag.** Add the global site tag (gtag.js) to all pages and the event snippet to your conversion pages:
   ```html
   <script>gtag('event', 'conversion', {'send_to': 'AW-XXXXXX/YYYYYY'});</script>
   ```
   Alternatively, use Google Tag Manager with a form submission trigger.

3. **Set conversion values.** Assign dollar values based on your unit economics: $200 for demo request (based on close rate x ACV), $50 for content download. This enables ROAS-based optimization.

4. **Implement server-side tracking.** For critical conversions, send events server-side via the Google Ads API to complement browser-based tracking and avoid ad-blocker gaps.

5. **Test the conversion.** Submit a test form and verify the conversion appears in the Google Ads API within a few hours: `GET /customers/<id>/conversionActions`.

6. **Verify conversion data.** Query the conversion report via API to confirm conversions are recording correctly. Match conversion counts against your backend data to ensure accuracy.
