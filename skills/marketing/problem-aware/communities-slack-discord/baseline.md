---
name: communities-slack-discord-baseline
description: >
  Slack/Discord Community Rhythm — Baseline Run. Automate community monitoring with
  keyword alerts, maintain daily engagement cadence, track attribution through PostHog,
  and validate sustained meeting generation over 2 weeks.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: ">= 3 meetings booked from community engagement over 2 weeks"
kpis: ["Referral sessions from communities", "Threads responded to per week", "DMs received", "Meetings booked", "Response rate on posted content"]
slug: "communities-slack-discord"
install: "npx gtm-skills add marketing/problem-aware/communities-slack-discord"
drills:
  - slack-discord-monitoring-automation
  - posthog-gtm-events
  - slack-discord-content-posting
---

# Slack/Discord Community Rhythm — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

Transition from manual browsing to automated community monitoring and sustained daily engagement. Prove that the meeting generation from Smoke is repeatable — not a one-off. This is the first always-on automation: keyword alerts surface engagement opportunities, you respond consistently, and PostHog tracks attribution from community referral to website visit to meeting.

## Leading Indicators

- Keyword monitoring alerts firing at 5-15 per day (system is calibrated)
- Threads responded to: 5+ per week
- Original content posts: 1-2 per week across communities
- Referral sessions tracked in PostHog from community UTM links: 10+ per week
- DMs received: 3+ per week
- Community-attributed signups or demo requests: 1+ per week

## Instructions

### 1. Set up community attribution tracking

Run the `posthog-gtm-events` drill to implement event tracking for community-driven traffic and conversions:

**Events to configure:**
- `community_referral_visit` — fires when a visitor arrives with `utm_source=slack` or `utm_source=discord` and `utm_medium=community`
- `community_signup` — fires when a visitor from a community UTM completes signup
- `community_meeting_booked` — fires when a community-attributed visitor books a meeting

**UTM convention for all community links:**
```
?utm_source={platform}&utm_medium=community&utm_campaign=communities-slack-discord&utm_content={workspace_or_server}_{channel}_{topic}
```

Example:
```
https://yoursite.com/blog/guide?utm_source=slack&utm_medium=community&utm_campaign=communities-slack-discord&utm_content=saas-founders_growth_pricing-strategy
```

Every link you share in a community must use this format. No exceptions.

### 2. Build keyword monitoring automation

Run the `slack-discord-monitoring-automation` drill to set up automated alerting:

**Slack monitoring:**
- Create an n8n workflow that polls the 3-5 most active channels in each of your primary Slack communities every 30 minutes.
- Match messages against your pain-point, buying-intent, and competitor keyword lists.
- Route matches to your internal #community-engagement-queue Slack channel, classified by priority.

**Discord monitoring:**
- Create a parallel n8n workflow for Discord channels using the Discord API.
- Same keyword matching and priority classification.
- Route to the same #community-engagement-queue channel.

**Tuning:**
- Run for 3 days. Review alert quality.
- If >20 alerts/day: add negative keywords, restrict channels.
- If <3 alerts/day: broaden keywords, add more community channels.
- Target: 5-15 actionable alerts per day.

### 3. Establish a daily engagement cadence

For the 2-week Baseline period, execute this daily:

**Morning (15 min):**
- Review overnight keyword alerts in #community-engagement-queue.
- Triage: pick the 2-3 highest-priority threads to respond to.

**Midday (30 min):**
- Craft and post responses using the `slack-discord-response-crafting` drill (from Smoke level).
- Follow up on any threads you responded to yesterday — reply to comments, answer questions.

**Weekly (1 hour):**
- Run the `slack-discord-content-posting` drill to create and post 1-2 original content pieces across your primary communities.
- Choose content format based on what performed in Smoke: Tactical Playbook, Data Share, Honest Retrospective, Discussion Starter.

**Human action required:** Post responses and content manually from your personal account. The agent drafts; you post. Log every interaction in the activity log.

### 4. Track and attribute

At the end of each week, pull data from PostHog:
- Referral sessions where `utm_source` is `slack` or `discord` and `utm_medium` is `community`
- Community-attributed signups (funnel: `community_referral_visit` -> `signup_completed`)
- Community-attributed meetings booked
- Breakdown by community name (from `utm_content`) — which communities drive the most traffic?

Update the Attio community targets list with weekly metrics per community.

### 5. Evaluate against threshold

Pass threshold: >= 3 meetings booked from community engagement over 2 weeks.

Attribution: count any meeting where the contact's first-touch or last-touch UTM includes `utm_campaign=communities-slack-discord`, or where the contact was first contacted via a community DM logged in Attio.

If PASS: Engagement cadence is repeatable and the monitoring pipeline is working. Proceed to Scalable.
If FAIL: Diagnose by checking each stage:
- **Alerts firing but low quality:** Keyword tuning needed. Review which keyword groups produce actionable vs. noise alerts.
- **Good responses but low referral traffic:** Your responses are not creating enough curiosity. Experiment with sharing more unique frameworks or data in responses.
- **Traffic but no conversions:** Landing page or follow-up is the bottleneck, not community engagement. Review the PostHog funnel for drop-off points.
- **Some communities producing, others not:** Reallocate time to producing communities. Drop the lowest-performing community and add a new candidate from your watch list.

## Time Estimate

- 3 hours: PostHog event setup and keyword monitoring automation
- 7 hours: Daily engagement over 2 weeks (15 min morning triage + 30 min responses, 10 days)
- 2 hours: Weekly content creation (1 hour per week, 2 weeks)
- 1 hour: Weekly reporting and attribution review
- 0.5 hours: Threshold evaluation
- 1.5 hours: Monitoring tuning and community list adjustments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Keyword monitoring and alert routing workflows | Free self-hosted; Cloud Starter: EUR 24/mo (https://n8n.io/pricing) |
| PostHog | Community attribution tracking and funnels | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Community targets list and interaction logging | Free for small teams (https://attio.com/pricing) |
| Clay | Community member enrichment (optional) | Launch: $149/mo (https://www.clay.com/pricing) |

**Play-specific cost at Baseline level:** Free if self-hosting n8n. EUR 24/mo if using n8n Cloud. All other tools on free tiers.

## Drills Referenced

- `slack-discord-monitoring-automation` — automated keyword monitoring across Slack/Discord with prioritized alerts
- `posthog-gtm-events` — event taxonomy and tracking for community attribution
- `slack-discord-content-posting` — create and publish original value-first content in communities
