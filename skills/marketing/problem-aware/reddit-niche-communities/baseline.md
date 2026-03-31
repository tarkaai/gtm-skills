---
name: reddit-niche-communities-baseline
description: >
  Reddit and community participation — Baseline Run. Establish a consistent daily
  engagement cadence across 5-8 subreddits with UTM tracking, PostHog event taxonomy,
  and structured activity logging to prove referral traffic holds over 2 weeks.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 100 referral sessions or ≥ 15 signups over 2 weeks"
kpis: ["Referral sessions from reddit.com", "Signups attributed to reddit.com", "Upvotes per comment (avg)", "Comments responded to per day"]
slug: "reddit-niche-communities"
install: "npx gtm-skills add marketing/problem-aware/reddit-niche-communities"
drills:
  - community-response-crafting
  - community-content-posting
  - posthog-gtm-events
  - threshold-engine
---

# Reddit and Community Participation — Baseline Run

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Prove that daily Reddit community engagement produces consistent, repeatable referral traffic over 2 weeks. The Smoke test proved the signal exists — Baseline proves it's not a fluke and builds the measurement foundation for scaling.

**Pass threshold:** ≥ 100 referral sessions from reddit.com OR ≥ 15 signups attributed to reddit.com over 2 weeks.

## Leading Indicators

- Consistent daily referral sessions from reddit.com (not one-spike-then-nothing)
- Average upvotes per comment increasing week-over-week
- Repeat visitors from reddit.com (people coming back from your profile or saved comments)
- Inbound DMs from community members asking about your product/service

## Instructions

### 1. Implement full tracking

Run the `posthog-gtm-events` drill to set up a community-specific event taxonomy in PostHog:

**Custom events to define:**
- `community_referral_visit`: Fires when a visitor arrives from reddit.com. Properties: `subreddit` (from `utm_content`), `post_type` (comment/post), `campaign` (reddit-niche-communities)
- `community_signup`: Fires when a visitor from reddit.com completes signup. Same properties.
- `community_engagement_logged`: Fires when you log a community interaction. Properties: `subreddit`, `action` (comment/post), `topic`, `link_included`

**PostHog saved insights to create:**
1. Referral traffic trend: daily `community_referral_visit` events, broken down by `subreddit`
2. Signup attribution: `community_signup` events grouped by `subreddit`
3. Conversion funnel: `community_referral_visit` → pageview on pricing/docs → `signup_started` → `signup_completed`

**Time estimate:** 1 hour

### 2. Establish daily engagement cadence

Commit to a daily Reddit engagement routine using the `community-response-crafting` drill:

**Daily routine (30-45 minutes):**
1. Check yesterday's comments for follow-ups — respond to every reply (5 min)
2. Browse top 3-5 subreddits sorted by "new" — identify 3-5 threads where you have expertise (10 min)
3. Write and post 3-5 comments following the response-crafting drill's rules (15-20 min)
4. Log each interaction in the activity log with: date, subreddit, thread URL, comment URL, topic, link included, response type (5 min)

**Weekly targets:**
- 15-25 comments per week across 5-8 subreddits
- 2-3 original posts per week (using `community-content-posting` drill)
- All links include UTM parameters: `?utm_source=reddit&utm_medium=community&utm_campaign=reddit-niche-communities&utm_content=r_SUBREDDIT_topic`

**Human action required:** All posting is still manual from a personal Reddit account. The agent prepares responses and research; the human reviews and posts.

### 3. Optimize content based on Smoke data

Using results from the Smoke test, focus effort on:
- **Subreddits that produced the most referral traffic** — increase posting frequency there
- **Content types that earned the most upvotes** — produce more of those formats
- **Topics that generated follow-up discussions** — these indicate genuine interest

Deprioritize subreddits and content types that produced zero referral sessions during Smoke.

### 4. Test content variations

During the 2-week window, deliberately vary your approach to learn:

- **Week 1:** Focus on comments (responding to others' threads). Track referral sessions.
- **Week 2:** Increase original posts while maintaining comment volume. Track referral sessions.
- Compare: which drives more traffic per hour of effort?

Also test:
- Comments with links vs. comments without links (do links help or hurt upvotes?)
- Long detailed responses vs. short punchy answers
- Technical depth vs. accessible explanations

### 5. Run mid-point review (end of week 1)

At day 7, check PostHog:
- Total referral sessions from reddit.com: on track for ≥ 100 over 2 weeks? (should be ≥ 40 at midpoint)
- Which subreddits drove the most sessions?
- Average upvotes per comment?
- Any signups attributed?

If below 40 sessions at midpoint, adjust:
- Switch to higher-traffic subreddits from your reconnaissance list
- Post more original content (posts generate more traffic than comments)
- Ensure UTM links are working (check PostHog for `utm_source=reddit`)

### 6. Evaluate against threshold

Run the `threshold-engine` drill at the end of 14 days:

**Metrics to check:**
- Total referral sessions from reddit.com over 14 days (PostHog: pageviews where `$initial_referring_domain` = reddit.com)
- Total signups attributed to reddit.com over 14 days
- Sessions per subreddit (identify top performers)
- Engagement rate: average upvotes per comment, average comments on your posts

**PASS (≥ 100 sessions OR ≥ 15 signups):** Document your best subreddits, content types, and engagement patterns. Proceed to Scalable.

**MARGINAL PASS (80-99 sessions):** Stay at Baseline for 1 more week with increased posting in top-performing subreddits.

**FAIL (<80 sessions AND <10 signups):** Revisit subreddit selection. Consider whether your ICP is actually active on Reddit or if another community platform (Slack, Discord, HN) would be more effective.

## Time Estimate

| Activity | Time |
|----------|------|
| PostHog event setup | 1 hour |
| Daily engagement (14 days x 30-45 min) | 8-10 hours |
| Original posts (4-6 posts x 30-45 min) | 3 hours |
| Mid-point review | 30 minutes |
| Final evaluation | 30 minutes |
| **Total** | **~13-15 hours** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for engagement | Free (personal account) |
| PostHog | Event tracking, funnels, attribution | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `community-response-crafting` — daily comment writing with value-first rules
- `community-content-posting` — weekly original Reddit-native posts
- `posthog-gtm-events` — community event taxonomy for tracking
- `threshold-engine` — pass/fail evaluation at end of 2 weeks
