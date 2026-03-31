---
name: newsletter-pipeline
description: Build, write, and send a recurring newsletter that nurtures prospects and retains customers
category: Content
tools:
  - Loops
  - PostHog
  - Ghost
fundamentals:
  - loops-broadcasts
  - loops-audience
  - posthog-custom-events
  - ghost-blog-publishing
---

# Newsletter Pipeline

This drill sets up a repeatable newsletter workflow: audience building, content creation, sending, and performance tracking. A consistent newsletter builds trust, stays top-of-mind, and drives traffic to your product.

## Prerequisites

- Loops account configured with sending domain authenticated
- Growing email list (at minimum, existing customers and engaged prospects)
- Content pipeline producing regular blog posts, insights, or updates

## Steps

### 1. Define your newsletter strategy

Decide on format, frequency, and audience. Common approaches:

- **Curated insights (weekly)**: 3-5 links with your commentary on industry trends. Low effort, high perceived value.
- **Original content (biweekly)**: One deep-dive article or insight per issue. Higher effort, stronger brand building.
- **Product + content hybrid (monthly)**: Product updates, a feature article, and customer highlights. Works well for existing customers.

Pick one format and commit to it for at least 12 issues before changing.

### 2. Build and segment your audience

Using the `loops-audience` fundamental, organize your subscribers into segments: prospects (never purchased), active customers, churned customers, and partners. Tag subscribers by interest area and acquisition source. Each segment may get slightly different content or different CTAs within the same newsletter.

### 3. Create a newsletter template

Design a simple, consistent template in Loops. Include: a recognizable header, a brief personal intro, the main content section, one clear CTA, and a footer with unsubscribe link. Avoid heavy formatting — plain-text-style newsletters often outperform designed ones for B2B audiences.

### 4. Write each issue

Follow this process for each issue:

- Draft the content 3-4 days before send date
- Write the subject line last — test 2-3 options. Keep under 50 characters. Use specificity over cleverness.
- Write a preview text that complements (not repeats) the subject line
- Include one primary CTA: read an article, try a feature, book a call, or reply with feedback

Using the `loops-broadcasts` fundamental, configure the send settings, preview the email across devices, and send a test to yourself first.

### 5. Send and engage

Send on a consistent day and time. Tuesday-Thursday mornings typically perform best for B2B. After sending, monitor replies — newsletters that invite replies build relationships. Respond to every reply personally within 24 hours.

### 6. Measure and optimize

Track open rate, click rate, unsubscribe rate, and reply rate using `posthog-custom-events`. Healthy benchmarks: 30%+ open rate, 3%+ click rate, under 0.5% unsubscribe rate per send. If open rates drop, test subject lines. If clicks drop, improve your CTA or content relevance. Publish newsletter content as blog posts using `ghost-blog-publishing` for SEO value.
