---
name: retargeting-setup
description: Configure retargeting pixels, build audiences, and launch campaigns to re-engage website visitors
category: Paid
tools:
  - Meta Ads
  - LinkedIn Ads
  - Google Ads
  - PostHog
fundamentals:
  - meta-ads-audience-setup
  - linkedin-ads-audience-setup
  - google-ads-remarketing
  - posthog-event-tracking
---

# Retargeting Setup

This drill sets up retargeting infrastructure across ad platforms so you can re-engage website visitors who did not convert on their first visit. Retargeting typically converts at 3-5x the rate of cold traffic.

## Prerequisites

- Website with meaningful traffic (at least 1,000 monthly visitors for retargeting to be effective)
- Ad platform accounts on Meta, LinkedIn, and/or Google
- PostHog tracking installed on your website
- Landing pages with clear conversion actions

## Steps

### 1. Install tracking pixels

Install retargeting pixels on every page of your website:

- **Meta Pixel**: For Facebook and Instagram retargeting
- **LinkedIn Insight Tag**: For LinkedIn retargeting
- **Google Ads tag**: For Google Display and YouTube retargeting

Use a tag manager or install directly. Verify each pixel fires correctly by using platform-specific debugging tools. Using `posthog-event-tracking`, also track pixel-fire events so you have a single source of truth for audience sizes.

### 2. Define audience segments

Not all visitors are equal. Build audiences by intent level:

- **High intent**: Visited pricing page, started signup, viewed demo page but did not convert. Retarget aggressively with direct CTAs.
- **Medium intent**: Read 2+ blog posts, visited the product page, spent 3+ minutes on site. Retarget with case studies or social proof.
- **Low intent**: Visited homepage once and bounced. Retarget with educational content or a compelling hook.
- **Exclusions**: Current customers, people who already converted, and bot traffic. Always exclude these.

Using the platform-specific audience fundamentals (`meta-ads-audience-setup`, `linkedin-ads-audience-setup`, `google-ads-remarketing`), create these segments in each platform.

### 3. Set audience windows

Configure time-based audience windows:

- **1-7 days**: Hottest audience. Highest conversion rate. Bid aggressively.
- **8-30 days**: Warm audience. Good for nurturing with content.
- **31-90 days**: Cooling audience. Lower bids, broader messaging.
- **90+ days**: Typically not worth retargeting unless you have a very long sales cycle.

Layer windows so you can adjust bids and messaging by recency.

### 4. Create retargeting ad creative

Match creative to the audience's intent level and stage:

- **High intent**: Direct CTA ads. "Still evaluating [category]? Book a 15-min demo." Show testimonials from companies like theirs.
- **Medium intent**: Social proof ads. Customer results, case study snippets, or video testimonials.
- **Low intent**: Educational content ads. Blog posts, guides, or webinar invites that provide value without asking for a commitment.

Use dynamic creative testing with 3-4 variations per audience segment.

### 5. Set budgets and frequency caps

Retargeting budgets are typically 10-20% of total ad spend. Set frequency caps to prevent ad fatigue: maximum 3-5 impressions per person per week on display, 1-2 per week on LinkedIn. Monitor frequency closely — when frequency rises above 5 without conversions, refresh creative or narrow the audience.

### 6. Measure retargeting attribution

Using `posthog-event-tracking`, track view-through and click-through conversions separately. Retargeting often assists conversions attributed to other channels, so look at assisted conversions alongside direct. Compare cost per acquisition from retargeting versus cold campaigns. Healthy benchmark: retargeting CPA should be 50-70% lower than cold traffic CPA.
