---
name: slack-community-program-smoke
description: >
  Slack Community Program — Smoke Test. Identify target Slack communities where your ICP
  congregates, join 3-5 workspaces, and post value-first content to test whether community
  engagement generates inbound interest and qualified conversations.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=30 members recruited to your own workspace and >=10 weekly active users within 2 weeks"
kpis: ["Thread reply rate on your posts", "DMs or connection requests received", "Referral visits to your site"]
slug: "slack-community-program"
install: "npx gtm-skills add marketing/solution-aware/slack-community-program"
drills:
  - icp-definition
  - slack-discord-reconnaissance
  - slack-discord-content-posting
  - threshold-engine
---

# Slack Community Program — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

Prove that engaging in existing Slack communities where your ICP is active generates inbound interest. Pass threshold: >=30 workspace members and >=10 weekly active users within 2 weeks.

## Leading Indicators

- Thread replies on your posts within 4 hours of posting (signal: content resonates)
- DMs from community members asking follow-up questions (signal: authority building)
- Profile views or connection requests on LinkedIn after community engagement (signal: curiosity)
- At least 3 communities scored 35+ on the reconnaissance scorecard (signal: viable channel)

## Instructions

### 1. Define your ICP for community engagement

Run the `icp-definition` drill. Focus specifically on:
- Which job titles and roles participate in Slack communities (not all ICP segments are active in Slack)
- What pain points they discuss in community settings vs. what they search for on Google
- What competitor communities they might already be in

Output: ICP document with a "Community Behavior" section appended.

### 2. Discover and score target Slack communities

Run the `slack-discord-reconnaissance` drill. This produces:
- A scored list of 10-15 Slack workspaces ranked by ICP fit, activity level, engagement quality, accessibility, and competition saturation
- Engagement profiles for the top 3-5 communities (primary tier, score 35+)
- Keyword lists (pain-point, category, ICP identity) for future monitoring
- Join URLs and community rules summaries

**Human action required:** Join the top 3-5 communities manually. Read #rules or #guidelines channels. Introduce yourself in #introductions if the community has one. Do NOT post promotional content during your first 48 hours — observe and react to others' messages only.

### 3. Post value-first content

Run the `slack-discord-content-posting` drill to create and publish 5-8 pieces of content across your target communities over 1 week. Content types to test:
- 2 Expert Answers (reply to existing threads with genuine expertise)
- 2 Tactical Playbooks (step-by-step guides solving a community pain point)
- 1-2 Discussion Starters (prompt the community to share their approaches)
- 1 Data Share or Honest Retrospective (if you have original data or experience to share)

Post 1-2 times per day across different communities. Stay in the thread for 2 hours after posting to reply to every response.

**Human action required:** Post content manually for the first week. The agent drafts the content; the human posts it and handles real-time conversation. Log every interaction: community name, channel, content type, thread replies received, reactions, DMs.

### 4. Track results and evaluate

Log all activity in a structured format (spreadsheet or Attio notes):
- Date, community, channel, content type, thread URL
- Reactions count, thread replies count, DMs received
- Any referral visits (check UTM tags if you included links)
- Qualitative notes: what resonated, what fell flat, what questions came up repeatedly

Run the `threshold-engine` drill to evaluate against pass criteria:
- >=30 members in your workspace (or equivalent: 30 meaningful interactions across communities)
- >=10 weekly active conversations where you participated

**Decision:** If PASS, proceed to Baseline. If FAIL with >=50% of threshold, iterate on content types and communities for one more week. If hard FAIL (<50% of threshold), reassess whether Slack communities are the right channel for your ICP.

## Time Estimate

- ICP community behavior analysis: 1 hour
- Slack community reconnaissance: 2 hours
- Content creation and posting (5-8 posts over 1 week): 2.5 hours
- Tracking and evaluation: 0.5 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Slack (free tier) | Join and participate in communities | Free |
| Attio | Log interactions and community targets | Standard stack (excluded) |
| Clay | ICP enrichment for community behavior | Standard stack (excluded) |

**Total play-specific cost: Free**

## Drills Referenced

- `icp-definition` — define community-specific ICP with behavioral signals
- `slack-discord-reconnaissance` — discover, score, and profile target Slack communities
- `slack-discord-content-posting` — create and publish value-first content in Slack communities
- `threshold-engine` — evaluate results against pass/fail criteria
