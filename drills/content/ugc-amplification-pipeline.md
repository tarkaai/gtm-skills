---
name: ugc-amplification-pipeline
description: Systematically amplify approved user-generated content across social, email, blog, and in-product channels
category: Content
tools:
  - LinkedIn
  - Loops
  - Intercom
  - PostHog
  - Attio
  - n8n
fundamentals:
  - linkedin-organic-posting
  - linkedin-organic-formats
  - loops-broadcasts
  - intercom-in-app-messages
  - posthog-custom-events
  - attio-notes
  - attio-lists
  - n8n-scheduling
  - n8n-workflow-basics
---

# UGC Amplification Pipeline

This drill takes approved user-generated content from the UGC Library and distributes it across channels to maximize reach, social proof, and referral traffic. Each piece of UGC is formatted for the target channel, scheduled into a content cadence, and tracked for performance.

## Prerequisites

- UGC collection automation running with approved content in Attio's "UGC Library" list
- Creator permission obtained (either via submission form opt-in or explicit follow-up)
- LinkedIn company page and personal posting access
- Loops configured for broadcast emails
- Intercom for in-product showcasing

## Steps

### 1. Score and prioritize content for amplification

Not all approved UGC should be amplified equally. Using the moderation scores from the UGC Library, rank content:

**Tier 1 — Flagship content (amplification score >= 4):**
Full multi-channel treatment: social post, newsletter feature, blog embed, in-product showcase.

**Tier 2 — Channel-specific content (amplification score 3-3.9):**
One or two channels where it fits best. A short testimonial goes to social and email. A tutorial goes to blog and in-product.

**Tier 3 — Archive/aggregate (amplification score < 3):**
Combine with other pieces in roundup posts or testimonial walls. Not amplified individually.

Using `n8n-scheduling`, create a weekly workflow that queries the UGC Library for approved-but-not-amplified content, ranks by amplification score, and queues the top 3-5 pieces for the week.

### 2. Format content for each channel

For each piece of UGC to amplify, create channel-specific versions:

**LinkedIn post format:**
Using `linkedin-organic-formats`, structure the post:
- Hook: Lead with the user's result or insight (not "Check out this user's content")
- Body: Quote the user directly or paraphrase their key point. Add 1-2 sentences of context.
- Attribution: Tag the creator (with permission). "Thanks to @JaneDoe for sharing this."
- CTA: "Have a story like this? Share it [link to submission form]"

Example: "Jane Doe automated her team's weekly reports and cut 6 hours per week. Here's how she set it up with [Product]: [quote or summary]. Want to share your setup? [link]"

**Email newsletter feature:**
Using `loops-broadcasts`, add a "From our community" section to the regular newsletter:
- Creator name + role + company (with permission)
- 2-3 sentence summary of their content
- Link to the full piece
- CTA: "Got a story? We'd love to feature you."

**Blog embed / community page:**
If the UGC is substantial (tutorial, detailed use case), publish it on your blog or community page:
- Full content with creator byline
- Editor's intro: "This tutorial was contributed by [Creator], who uses [Product] to [outcome]."
- Link back to the creator's profile or website
- CTA: "Submit your tutorial"

**In-product showcase:**
Using `intercom-in-app-messages`, display UGC to relevant users:
- Show tutorial UGC to users who haven't used that feature yet
- Show testimonials to users approaching upgrade decisions
- Show use case stories to users in the same industry or role
- Target via PostHog cohorts matching the UGC's topic

### 3. Schedule the amplification cadence

Build a sustainable publishing rhythm:

- **Social (LinkedIn):** 1-2 UGC posts per week, mixed with non-UGC content. Never post UGC back-to-back.
- **Newsletter:** 1 UGC feature per edition (weekly or biweekly). Rotate between testimonials, tips, and tutorials.
- **In-product:** Show UGC contextually based on user behavior. Cap at 1 UGC showcase per user per week.
- **Blog:** 1-2 UGC pieces per month (only for high-quality tutorials or case studies).

Using `n8n-scheduling`, automate the queuing: the weekly workflow selects content, creates draft social posts, queues newsletter features, and sets up Intercom messages with targeting rules.

### 4. Notify creators when their content is featured

Using `attio-notes`, log each amplification event on the creator's contact record: channel, date, URL of the published piece.

Using Loops or Intercom, send the creator a notification: "Your [content type] was featured on our [channel]! Here's the link: [URL]. Feel free to share it with your network."

This serves two purposes:
1. The creator feels valued and is more likely to create again
2. The creator shares the feature with their own audience, multiplying reach

### 5. Track amplification performance

Fire PostHog events for each amplification:

| Event | Properties |
|-------|-----------|
| `ugc_amplified` | content_id, channel, content_type, creator_tier |
| `ugc_amplified_viewed` | content_id, channel, unique_views |
| `ugc_amplified_clicked` | content_id, channel, referral_source |
| `ugc_amplified_converted` | content_id, channel, conversion_type (signup, trial, demo) |

Track per-piece metrics in the Attio UGC Library:
- Impressions/views per channel
- Clicks/engagement per channel
- Referral signups or trials attributed to UGC
- Creator response (did they reshare?)

Build a PostHog funnel: `ugc_amplified` -> `ugc_amplified_viewed` -> `ugc_amplified_clicked` -> `ugc_amplified_converted`

### 6. Feed performance data back to prioritization

After 2+ weeks of amplification data, update the prioritization model:
- Which content types drive the most referral traffic? (tutorials > testimonials > tips?)
- Which channels produce the most conversions from UGC? (social > email > in-product?)
- Which creator tiers produce the best-performing content?

Use these insights to adjust the UGC prompt design (ask for more of what works) and the amplification schedule (allocate more slots to high-performing channels).

## Output

- Weekly content selection and formatting workflow
- Channel-specific UGC templates (LinkedIn, email, blog, in-product)
- Amplification cadence with frequency caps per channel
- Creator notification system
- Full PostHog tracking from amplification through to referral conversion
- Performance feedback loop to prompt design and prioritization

## Triggers

The weekly selection workflow runs every Monday via n8n cron. Creator notifications fire on each amplification event. Performance data aggregates weekly. All workflows are always-on.
