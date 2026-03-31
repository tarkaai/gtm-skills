---
name: reddit-niche-communities-smoke
description: >
  Reddit and community participation — Smoke Test. Discover 5-10 subreddits where
  your ICP is active, post 15-20 value-first comments over 1 week, and measure
  whether authentic community engagement generates referral traffic and signups.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 30 referral sessions or ≥ 5 signups in 1 week"
kpis: ["Referral sessions from reddit.com", "Comment upvotes received", "Link clicks via UTM"]
slug: "reddit-niche-communities"
install: "npx gtm-skills add marketing/problem-aware/reddit-niche-communities"
drills:
  - community-reconnaissance
  - community-response-crafting
  - community-content-posting
---

# Reddit and Community Participation — Smoke Test

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Prove that engaging authentically in Reddit communities where your ICP hangs out can generate measurable referral traffic and signups. This is a 1-week manual test: no automation, no tools beyond Reddit and PostHog.

**Pass threshold:** ≥ 30 referral sessions from reddit.com OR ≥ 5 signups attributed to reddit.com in 1 week.

## Leading Indicators

- Upvotes on your comments (signal that the community finds your contributions valuable)
- Reply threads on your comments (engagement depth)
- DMs or follow requests from community members
- PostHog shows increasing daily referral sessions from reddit.com

## Instructions

### 1. Discover and profile target subreddits

Run the `community-reconnaissance` drill. Using your ICP definition, generate keyword lists for pain points, product category, and ICP roles. Search Reddit for subreddits matching these keywords. Evaluate each subreddit for ICP fit, activity level, engagement, accessibility, and competition. Produce a ranked list of 5-10 target subreddits with engagement profiles.

**Time estimate:** 1 hour

### 2. Set up basic tracking

Ensure PostHog is tracking website visits. Verify that visits from `reddit.com` appear in PostHog under the `$referrer` or `$initial_referring_domain` property. No custom events needed for Smoke — just confirm PostHog captures Reddit referral traffic.

Create a PostHog insight: pageviews where `$initial_referring_domain` contains `reddit.com`, broken down by day, for the next 7 days.

**Time estimate:** 15 minutes

### 3. Engage in your top 3-5 subreddits

Run the `community-response-crafting` drill daily for 5 days. Each day:

1. Browse your top 3-5 subreddits for 15-20 minutes
2. Identify 3-5 threads where you have genuine expertise to contribute
3. Write thoughtful, value-first responses following the drill's format rules:
   - Lead with the direct answer
   - Be specific (include numbers, benchmarks, real examples)
   - Keep under 300 words per comment
   - Maximum 1 in 10 comments should include a link to your content
   - When linking, always include UTM parameters: `?utm_source=reddit&utm_medium=community&utm_campaign=reddit-niche-communities&utm_content=r_SUBREDDIT_topic`
4. Return to yesterday's comments and respond to any follow-ups

**Daily time:** ~20-30 minutes
**Total:** ~2 hours across 5 days

### 4. Post 1-2 original pieces of content

Run the `community-content-posting` drill. During the week, write and post 1-2 original posts in your highest-fit subreddits. Choose from the drill's format archetypes:
- A playbook post sharing a specific process you use
- A lessons-learned post about a challenge you overcame
- A data share with benchmarks from your domain

Stay active for 2 hours after posting to respond to every comment.

**Time estimate:** 30-45 minutes per post

### 5. Log all activity

Maintain a simple log of every interaction:

```
Date | Subreddit | Type (comment/post) | Thread URL | Topic | Link included? | Upvotes (after 24h)
```

**Human action required:** All posting must be done by a human from a personal Reddit account with existing karma. Do not use a brand account or a new account — established accounts get more visibility and trust.

### 6. Evaluate against threshold

At the end of 7 days, check PostHog:
- Total pageviews where `$initial_referring_domain` contains `reddit.com` in the last 7 days
- Total signups where `$initial_referring_domain` contains `reddit.com` in the last 7 days

**PASS (≥ 30 referral sessions OR ≥ 5 signups):** Document which subreddits and content types drove the most traffic. Proceed to Baseline.

**FAIL (<30 sessions AND <5 signups):** Review your engagement log. Were you posting in the right subreddits? Was your content genuinely helpful? Try different subreddits or content angles and re-run.

## Time Estimate

| Activity | Time |
|----------|------|
| Community reconnaissance | 1 hour |
| PostHog tracking setup | 15 minutes |
| Daily comment engagement (5 days) | 2 hours |
| Original posts (1-2) | 45 minutes |
| **Total** | **~4 hours** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for engagement | Free (personal account) |
| PostHog | Track referral traffic and signups | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `community-reconnaissance` — discover and rank target subreddits with engagement profiles
- `community-response-crafting` — write value-first comments that build authority
- `community-content-posting` — create Reddit-native original posts
