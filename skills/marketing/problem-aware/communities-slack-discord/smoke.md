---
name: communities-slack-discord-smoke
description: >
  Slack/Discord Community Rhythm — Smoke Test. Identify 5-10 Slack/Discord communities
  where your ICP congregates, join them, engage authentically for 1 week, and validate
  whether community engagement generates at least 1 meeting.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">= 1 meeting booked from community engagement within 1 week"
kpis: ["Threads responded to", "Reactions received", "DMs initiated by others", "Meetings booked"]
slug: "communities-slack-discord"
install: "npx gtm-skills add marketing/problem-aware/communities-slack-discord"
drills:
  - slack-discord-reconnaissance
  - slack-discord-response-crafting
  - threshold-engine
---

# Slack/Discord Community Rhythm — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

Validate that engaging in Slack and Discord communities where your ICP congregates produces inbound interest and at least 1 meeting. This is a manual, 1-week test. You discover communities, join them, respond to relevant threads with genuine value, and measure whether anyone reaches out or books a call.

## Leading Indicators

- Number of communities joined where ICP members are active (target: 5+)
- Threads responded to with value-first answers (target: 15+ across all communities)
- Positive reactions on your messages (target: 10+ total)
- DMs received from community members (target: 2+)
- Profile views or website visits from community referrals (target: 5+)

## Instructions

### 1. Discover and rank target communities

Run the `slack-discord-reconnaissance` drill in minimal mode. The goal is to find 5-10 Slack workspaces and Discord servers where your ICP is active.

Specific actions:
- Generate keyword lists from your ICP definition: pain-point keywords, category keywords, and ICP identity keywords.
- Search Slack directories (Slofile, Standuply), Discord directories (Disboard, Discord discovery API), and web search for "{ICP role} slack community" and "{industry} discord server".
- For each candidate, evaluate: member count, daily activity, ICP density, posting rules, and vendor saturation.
- Score and rank candidates. Select the top 5-10.
- Build an engagement profile for each: key channels, rules, peak hours, your angle.
- Store the ranked list in Attio as a "Slack/Discord Community Targets" list.

**Human action required:** Join each community. Some require applications or invitations. Apply to all top-ranked communities immediately since approval can take 1-7 days.

### 2. Lurk and learn (first 48 hours)

Before posting anything, spend 48 hours reading each community:
- Read the last 200 messages in the 3 most relevant channels per community.
- Note the tone (casual vs. professional), format (short messages vs. long posts), and social norms.
- Identify 5-10 threads per community where you could add genuine value.
- Update your engagement profiles with observed patterns.

This is not optional. Posting immediately in a new community without understanding its culture will mark you as a spammer.

### 3. Engage with value-first responses

Run the `slack-discord-response-crafting` drill for each engagement opportunity.

Target: 3-5 responses per day across all communities for 5 consecutive days.

For each response:
- Read the thread fully before responding. Understand what the person actually needs.
- Choose a response type: Expert Answer, Framework Share, Experience Report, Resource Curator, or Clarifying Question.
- Write the response following community formatting norms (Slack mrkdwn or Discord Markdown).
- Lead with value. No product mentions in the first week.
- Log each interaction: date, community, channel, thread URL, response type, topic.

**Human action required:** Post responses manually from your personal Slack/Discord account. The agent prepares and drafts; you post and engage in follow-up conversations.

### 4. Track engagement manually

For each response, log after 24 hours:
- Reactions received (count and type)
- Thread replies to your message
- DMs received from community members
- Any mentions of your content or expertise by others
- Referral visits to your website (check PostHog or analytics for direct/referral traffic from slack.com or discord.com domains)

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Pass threshold: >= 1 meeting booked from community engagement within 1 week.

Count as a meeting: any call, demo, or scheduled conversation that originated from a community interaction — either from a DM, a thread conversation, or someone visiting your site from a community link.

If PASS: Community engagement works for your ICP. Proceed to Baseline.
If FAIL: Diagnose:
- **No engagement on responses (0 reactions/replies):** Your responses may not be specific enough, or you are in the wrong channels. Review the top-performing messages in each community and adjust.
- **Engagement but no DMs:** You are adding value but not building enough curiosity. Try sharing more unique data or frameworks. Include your title/company in your profile.
- **DMs but no meetings:** Your follow-up is not converting. Review how you handle DM conversations — are you offering a clear next step?
- **Wrong communities entirely:** ICP members are not in these communities. Return to step 1 with different search terms or platforms.

## Time Estimate

- 2 hours: Community discovery and evaluation (slack-discord-reconnaissance)
- 1 hour: Lurking and learning (reading community culture)
- 2.5 hours: Responding to threads (15-25 responses over 5 days, ~10 min each)
- 0.5 hours: Tracking engagement and evaluating threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Community discovery and ICP research | Launch: $149/mo (https://www.clay.com/pricing) |
| Attio | Store community targets and track interactions | Free for small teams (https://attio.com/pricing) |
| PostHog | Track referral visits from community links | Free up to 1M events/mo (https://posthog.com/pricing) |

**Play-specific cost at Smoke level:** Free. All tools on free tiers. No paid community memberships required at this level.

## Drills Referenced

- `slack-discord-reconnaissance` — discover, evaluate, and rank Slack/Discord communities where ICP is active
- `slack-discord-response-crafting` — craft value-first responses to community threads
- `threshold-engine` — evaluate pass/fail against the outcome threshold
