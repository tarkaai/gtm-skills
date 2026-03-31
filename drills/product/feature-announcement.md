---
name: feature-announcement
description: Announce new features through coordinated in-app messages, email campaigns, and changelog updates
category: Product
tools:
  - Intercom
  - Loops
  - Ghost
  - PostHog
fundamentals:
  - intercom-in-app-messages
  - loops-broadcasts
  - ghost-blog-publishing
  - posthog-custom-events
---

# Feature Announcement

This drill coordinates a feature launch across in-app messaging, email, blog, and social channels to maximize awareness and adoption. It ensures the right users hear about the right features through the right channel.

## Prerequisites

- Feature is shipped and stable (do not announce what is not ready)
- Intercom configured with user segments
- Loops audience segmented by plan and feature usage
- Clear understanding of which users benefit from this feature

## Steps

### 1. Define the announcement tier

Not every feature deserves the same rollout. Classify the feature:

- **Tier 1 (major)**: New capability that changes workflows. Full multi-channel launch: in-app, email, blog, social, changelog.
- **Tier 2 (notable)**: Meaningful improvement to existing feature. In-app message, email to relevant segment, changelog.
- **Tier 3 (minor)**: Bug fix, UI tweak, small enhancement. Changelog only.

This drill focuses on Tier 1 and Tier 2 announcements.

### 2. Write the announcement copy

Lead with the benefit, not the feature name. Structure:

- **Headline**: What the user can now do (not what you built)
- **One-paragraph summary**: The problem this solves and how it works
- **Visual**: Screenshot, GIF, or short video showing the feature in action
- **CTA**: "Try it now" linking directly to the feature, not to a generic dashboard

Write different copy for different audiences — power users want technical details, new users want simple benefits.

### 3. Build the in-app announcement

Using the `intercom-in-app-messages` fundamental, create a targeted in-app message. Show it only to users who would benefit: segment by plan, feature usage, or user role. Use a banner or modal for Tier 1 features, a subtle tooltip or badge for Tier 2. Include a dismiss option and do not show it again once dismissed.

### 4. Send the email announcement

Using the `loops-broadcasts` fundamental, send a feature announcement email to the relevant segment. For Tier 1: send to all active users. For Tier 2: send only to users of the related feature. Include the visual, a short explanation, and a direct link. Time the email to go out on the same day the in-app message activates.

### 5. Publish the blog post and changelog

Using the `ghost-blog-publishing` fundamental, publish a detailed blog post for Tier 1 features. Include the backstory (why you built it), a walkthrough, and use cases. Update your changelog for all tiers. The blog post serves SEO and gives you a URL to share on social and in sales conversations.

### 6. Track adoption

Using `posthog-custom-events`, track feature adoption: how many users saw the announcement, how many clicked through, and how many actually used the feature within 7 days. Compare adoption rates across channels to learn which drives the most actual usage. If adoption is low despite high awareness, the feature may need better discoverability or onboarding.
