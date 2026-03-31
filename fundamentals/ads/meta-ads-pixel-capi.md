---
name: meta-ads-pixel-capi
description: Install Meta Pixel and configure the Conversions API for accurate tracking and attribution of Meta ad campaigns.
tool: Meta Ads
difficulty: Config
---

# Set Up Meta Pixel and Conversions API

### Step-by-step
1. Go to Meta Events Manager > Data Sources > Create New Pixel.
2. Name the pixel and add your website URL.
3. Install the pixel base code: add the Meta Pixel JavaScript snippet to every page of your website, in the <head> tag.
4. Set up standard events: add event code for key actions — Lead (form submission), CompleteRegistration (sign-up), Purchase (if applicable).
5. Use the Meta Pixel Helper browser extension to verify the pixel is firing correctly on each page.
6. Set up Conversions API (CAPI): this sends events server-side, complementing the pixel for better accuracy (especially with iOS privacy changes).
7. Implement CAPI via your backend: when a conversion happens, send an event to Meta's API with user data (email hash, phone hash) for matching.
8. Alternatively, use a CAPI partner integration: many website platforms (Webflow, WordPress) have built-in CAPI connectors.
9. Deduplicate events: set the same event_id for pixel and CAPI events so Meta doesn't double-count conversions.
10. Verify in Events Manager: check that events are being received from both Pixel (Browser) and CAPI (Server), and that the Event Match Quality score is above 6.
