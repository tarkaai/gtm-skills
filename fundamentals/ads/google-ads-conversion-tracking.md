---
name: google-ads-conversion-tracking
description: Implement conversion tracking for Google Ads to measure which clicks lead to valuable actions like sign-ups, demos, and purchases.
tool: Google Ads
difficulty: Config
---

# Set Up Google Ads Conversion Tracking

### Step-by-step
1. Go to Google Ads > Tools > Measurement > Conversions > New Conversion Action.
2. Choose the conversion source: Website, App, Phone Calls, or Import.
3. For website conversions: define the conversion (e.g., 'Demo Requested', 'Sign Up Completed', 'Purchase').
4. Set the conversion value: assign a dollar value if possible (e.g., $200 for a demo request based on your close rate and ACV).
5. Set the count: 'One' for lead gen (count one conversion per click) or 'Every' for e-commerce.
6. Set the conversion window: 30-day click-through and 1-day view-through are standard for B2B.
7. Install the Google Ads tag on your website: add the global site tag to all pages and the event snippet to your thank-you/confirmation page.
8. Alternatively, use Google Tag Manager: create a trigger for form submissions or page views of your confirmation page.
9. Test the conversion: submit a test form and verify the conversion appears in Google Ads within a few hours.
10. Verify in the Conversions report: check that conversions are recording. If not, use the Google Tag Assistant browser extension to debug.
