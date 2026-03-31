---
name: community-engagement-tracking
description: Track community engagement metrics (karma, replies, referral clicks) in a structured log
tool: PostHog / Attio / Spreadsheet
difficulty: Setup
---

# Community Engagement Tracking

Set up a structured system to log every community interaction and its outcomes. This enables measuring which communities, content types, and engagement styles generate the most referral traffic and signups.

## Tracking Architecture

### Layer 1: UTM-tagged links

Every link you share in a community must include UTM parameters:

```
https://yoursite.com/PAGE?utm_source=reddit&utm_medium=community&utm_campaign=reddit-niche-communities&utm_content=r_SUBREDDIT_post_TOPIC
```

Parameter schema:
- `utm_source`: Platform name (`reddit`, `discord`, `slack`, `hackernews`)
- `utm_medium`: Always `community` for this play
- `utm_campaign`: Play slug (`reddit-niche-communities`)
- `utm_content`: Subreddit + context (`r_SaaS_comment_pricing`, `r_startups_post_how_to`)

### Layer 2: PostHog event tracking

Fire custom PostHog events for community-driven actions using the `posthog-custom-events` fundamental:

```javascript
posthog.capture('community_referral_visit', {
    source: 'reddit',
    subreddit: 'r/SaaS',
    post_type: 'comment',   // 'comment', 'post', 'dm'
    topic: 'pricing-strategy',
    campaign: 'reddit-niche-communities'
});

posthog.capture('community_signup', {
    source: 'reddit',
    subreddit: 'r/SaaS',
    attribution_post_url: 'https://reddit.com/r/SaaS/comments/...',
    campaign: 'reddit-niche-communities'
});
```

UTM parameters are automatically captured by PostHog if the JS snippet is installed. The custom events above add richer context for analysis.

### Layer 3: Activity log

Maintain a structured log of every community interaction. Store in Attio as notes on a "Community Engagement" list, or in a simple JSON/CSV file:

```json
{
  "date": "2026-03-30",
  "platform": "reddit",
  "subreddit": "r/SaaS",
  "action": "comment",
  "post_url": "https://reddit.com/r/SaaS/comments/abc123/...",
  "your_content_url": "https://reddit.com/r/SaaS/comments/abc123/.../def456",
  "topic": "pricing strategy for early-stage SaaS",
  "included_link": true,
  "link_url": "https://yoursite.com/blog/pricing?utm_source=reddit&utm_medium=community&utm_campaign=reddit-niche-communities&utm_content=r_SaaS_comment_pricing",
  "upvotes_received": 12,
  "replies_received": 3,
  "referral_sessions_24h": 8,
  "signups_24h": 1
}
```

### Layer 4: Attribution in CRM

When a lead signs up and their `first_touch_channel` in PostHog is `community` with `utm_source=reddit`, create or update the contact in Attio with:
- `lead_source`: `reddit-community`
- `lead_source_detail`: The specific subreddit (from `utm_content`)
- `first_touch_url`: The Reddit post/comment URL

## Metrics to Compute

From the activity log and PostHog data, compute weekly:

1. **Referral sessions by subreddit**: PostHog query — pageviews where `utm_source=reddit` grouped by `utm_content`
2. **Signups by subreddit**: PostHog query — signup events where `utm_source=reddit` grouped by `utm_content`
3. **Engagement rate by content type**: (upvotes + replies) / posts, grouped by content type (how-to, opinion, case-study, question)
4. **Karma earned per subreddit**: Track cumulative upvotes from your interactions per community
5. **Time to first referral**: Days between first post in a subreddit and first attributed referral visit
6. **Cost per referral session**: If using paid tools (Syften, etc.), divide monthly tool cost by referral sessions

## PostHog Dashboard Queries

Create a saved insight in PostHog for each:

- **Referral trend**: Line chart of `community_referral_visit` events over time, broken down by `subreddit` property
- **Signup attribution**: Bar chart of `community_signup` events grouped by `subreddit`
- **Conversion funnel**: Funnel from `community_referral_visit` → `page_viewed` (pricing/docs page) → `signup_started` → `signup_completed`

## Error Handling

- **UTM stripping**: Some Reddit clients strip UTM parameters. Use a URL shortener that preserves UTMs (e.g., short.io) or use distinct landing page paths per subreddit as a backup tracking method.
- **Missing attribution**: If signups don't have UTM data, check PostHog's `$initial_referrer` property — it will show `reddit.com` even without UTMs.
- **Double counting**: Deduplicate by user ID when computing signups. A user who visits from Reddit 3 times is still 1 signup.
