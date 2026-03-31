---
name: landing-page-pipeline
description: Build, launch, and optimize landing pages for paid campaigns and lead capture
category: Paid
tools:
  - Webflow
  - PostHog
  - Loops
fundamentals:
  - webflow-landing-pages
  - posthog-custom-events
  - posthog-funnels
  - loops-audience
---

# Landing Page Pipeline

This drill covers building high-converting landing pages for paid campaigns, content offers, and product signups. It includes the creation process, tracking setup, and ongoing optimization.

## Prerequisites

- Webflow or equivalent page builder configured
- PostHog tracking ready to install on new pages
- Clear offer or CTA for the page (demo, trial, download, webinar registration)
- Ad campaigns or traffic sources planned

## Steps

### 1. Define the page goal and audience

Every landing page has one goal and one audience. Define both before designing:

- **Goal**: What action should the visitor take? (Sign up, book a demo, download a resource, register for a webinar)
- **Audience**: Who is arriving? (Cold traffic from ads, warm traffic from email, referred traffic from partners)
- **Source context**: What did the ad or link say? The landing page must deliver on that specific promise.

One page per offer. Never send paid traffic to your homepage.

### 2. Build the page structure

Using the `webflow-landing-pages` fundamental, construct the page following a proven layout:

- **Hero section**: Headline (benefit-driven, under 10 words), subheadline (how you deliver the benefit), CTA button, and a visual (screenshot, demo video, or illustration)
- **Social proof**: Customer logos, testimonial quote, or a specific metric ("Used by 500+ teams")
- **Problem/Solution**: 3 pain points your audience recognizes, matched with your solutions
- **Features or benefits**: 3-4 specific capabilities, each with a brief explanation
- **Objection handling**: FAQ section addressing the top 3-4 concerns
- **Final CTA**: Repeat the CTA with urgency or a guarantee

Remove navigation links. Landing pages should have no exits except the CTA or the back button.

### 3. Optimize the form

Keep the form as short as possible for the offer value. For a content download: name and email only. For a demo request: name, email, company, role. Every additional field reduces conversions by 10-15%. Use inline validation and clear error messages. Place the form above the fold or as a sticky element.

### 4. Install tracking

Using `posthog-custom-events`, track: page view, scroll depth (25%, 50%, 75%, 100%), form focus, form submission, and thank-you page view. Set up UTM parameter capture so every conversion carries its source data. Using `posthog-funnels`, build a micro-funnel: page view to scroll to form focus to submission.

### 5. Connect to your lead pipeline

Using `loops-audience`, route form submissions to the appropriate email list and trigger sequence. For demo requests: also create a lead in Attio. For content downloads: deliver the asset immediately via email and add to a nurture sequence. Every lead should enter your system within seconds of submitting.

### 6. Test and iterate

After 200+ visitors, analyze the data. If bounce rate is above 60%, the headline or hero section is not resonating with the traffic source — test new headlines. If scroll depth drops sharply at a section, that section is losing people — rewrite or remove it. If form views are high but submissions are low, simplify the form. Run A/B tests on one element at a time: headline, CTA copy, form length, or social proof placement.
