---
name: slack-community-program-baseline
description: >
  Slack Community Program — Baseline Run. Deploy automated keyword monitoring across
  target Slack communities, respond to high-opportunity threads daily, and track
  community-attributed signups and pipeline through PostHog and Attio.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Baseline Run"
time: "18 hours over 6 weeks"
outcome: ">=150 workspace members, >=40 WAU, and >=8 qualified leads attributed to community in 6 weeks"
kpis: ["Community-attributed signups", "Qualified leads from community", "Response rate to monitored alerts", "Referral sessions per post"]
slug: "slack-community-program"
install: "npx gtm-skills add marketing/solution-aware/slack-community-program"
drills:
  - posthog-gtm-events
  - slack-discord-monitoring-automation
  - slack-discord-response-crafting
  - threshold-engine
---

# Slack Community Program — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

Establish always-on community monitoring and response workflows that produce repeatable, trackable results. Pass threshold: >=150 workspace members, >=40 WAU, and >=8 qualified leads attributed to community engagement in 6 weeks.

## Leading Indicators

- Monitoring pipeline producing 5-15 actionable alerts per day within first week (signal: keyword coverage is right)
- Response-to-alert rate above 60% for high-priority threads (signal: team is keeping up)
- Referral sessions from community UTMs appearing in PostHog within first 2 weeks (signal: content drives clicks)
- At least 2 community members moving to "qualified lead" status in Attio by week 3 (signal: pipeline forming)

## Instructions

### 1. Set up community event tracking in PostHog

Run the `posthog-gtm-events` drill. Configure the following custom events specific to this play:

- `community_post_published` — fires when you post content in a community. Properties: `platform` (slack), `community` (workspace name), `channel`, `content_type` (expert-answer, playbook, discussion-starter, data-share, resource-roundup), `post_url`.
- `community_referral_visit` — fires when a visitor arrives via community UTM. Properties: `source` (slack), `community` (workspace name), `channel`, `post_url`.
- `community_signup` — fires when a referral visitor creates an account. Properties: `source`, `community`, `attribution_post_url`.
- `community_lead_qualified` — fires when a community-sourced contact meets qualification criteria. Properties: `source`, `community`, `qualification_reason`.

Set up the attribution funnel in PostHog: `community_referral_visit` -> `page_viewed` (pricing or docs) -> `signup_started` -> `signup_completed` -> `community_lead_qualified`.

### 2. Deploy automated community monitoring

Run the `slack-discord-monitoring-automation` drill. This builds:

- An n8n workflow that polls your target Slack communities every 30 minutes for messages matching your pain-point, buying-intent, and competitor-mention keyword lists
- Priority classification (high/medium/low) based on keyword group matches
- Alerts routed to an internal Slack channel (#community-engagement-queue) with message preview, priority, permalink, and response deadline
- A daily summary of alerts generated, alerts responded to, and referral sessions

Configure keyword lists from the Smoke test learnings — tighten keywords that produced false positives, add phrases that appeared in high-engagement threads.

Target: 5-15 actionable alerts per day. If fewer than 3, broaden keywords or add communities. If more than 20, add negative keywords or restrict channels.

### 3. Respond to high-opportunity threads

Run the `slack-discord-response-crafting` drill for every high-priority alert and at least 50% of medium-priority alerts. For each response:

1. Read the full thread context (original message + all existing replies)
2. Identify the gap — what hasn't been addressed or was addressed poorly
3. Choose a response archetype: Expert Answer, Framework Share, Experience Report, Resource Curator, or Clarifying Question
4. Draft the response following platform-specific formatting and self-promotion guardrails
5. Post the response (agent drafts, human posts in communities where API access is not available)
6. Follow up within 24 hours on any thread replies

**Human action required:** Review and post agent-drafted responses in communities that restrict bot access. The agent handles drafting, UTM tagging, and logging. The human handles posting and real-time follow-up conversation.

Daily target: respond to 3-5 threads across all monitored communities.

### 4. Maintain original content cadence

Continue posting 2-3 original content pieces per week (from the `slack-discord-content-posting` drill used in Smoke). Focus on:
- Content types that performed best during Smoke (check your activity log)
- Communities with the highest engagement scores
- Topics matching trending keyword alerts from the monitoring pipeline

### 5. Evaluate against threshold

Run the `threshold-engine` drill at week 6 to measure:
- Workspace member count (from Slack API `team.info`) >= 150
- Weekly active users (unique posters in the last 7 days) >= 40
- Qualified leads in Attio where `lead_source = slack-community` >= 8

**Decision:** If PASS, proceed to Scalable. If FAIL with strong referral sessions but low lead quality, refine ICP targeting and content strategy — run one more 4-week cycle. If FAIL with low referral sessions, review community selection and keyword coverage.

## Time Estimate

- PostHog event setup: 2 hours
- Monitoring pipeline build (n8n workflow): 3 hours
- Response crafting (3-5/day over 6 weeks, ~15 min each): 10 hours
- Content posting (2-3/week over 6 weeks): 2 hours
- Evaluation and analysis: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Slack (free tier) | Participate in communities | Free |
| n8n | Polling workflows for keyword monitoring | Standard stack (excluded) |
| PostHog | Track referral visits, signups, and attribution | Standard stack (excluded) |
| Attio | Store leads and community engagement logs | Standard stack (excluded) |

**Total play-specific cost: Free** (all tools are standard stack)

## Drills Referenced

- `posthog-gtm-events` — set up community-specific event tracking and attribution funnels
- `slack-discord-monitoring-automation` — build automated keyword monitoring and alert routing
- `slack-discord-response-crafting` — craft value-first responses to high-opportunity community threads
- `threshold-engine` — evaluate 6-week results against pass criteria
