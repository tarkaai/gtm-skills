---
name: community-engagement-brief
description: Generate weekly intelligence briefs on community engagement performance, member behavior patterns, and content strategy recommendations
category: Community
tools:
  - PostHog
  - Anthropic
  - n8n
  - Attio
  - Slack API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - hypothesis-generation
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-lists
  - slack-api-read
  - community-engagement-tracking
---

# Community Engagement Brief

Generate a weekly intelligence brief that synthesizes community engagement data into actionable strategy recommendations. This drill bridges raw metrics from `community-health-scoring` and activity logs into a narrative the agent or operator can act on — identifying which content themes are gaining traction, which communities are shifting in engagement quality, and what the agent should prioritize next week.

## Input

- Community health scores from the `community-health-scoring` drill (last 4 weeks minimum)
- Activity log entries from the `community-engagement-tracking` fundamental (last 7 days)
- PostHog community referral and signup data (last 7 days + 4-week rolling average)
- Attio community target list with historical score data

## Steps

### 1. Pull the weekly data package

Build an n8n workflow triggered by a weekly cron (every Monday at 7am, after `community-health-scoring` runs at 6am):

```
Schedule Trigger (weekly, Monday 7am)
  -> PostHog HTTP Request Node:
     Query 1: community_referral_visit events, last 7 days, grouped by source + community
     Query 2: community_signup events, last 7 days, grouped by source + community
     Query 3: Top 10 referring URLs by session count (identifies which specific posts drove traffic)
  -> Attio HTTP Request Node:
     Query: All records from "Slack/Discord Community Targets" list with score history
  -> Slack API Node (slack-api-read):
     For each monitored community workspace:
       Pull last 7 days of messages from your tracked channels
       Count: messages you posted, thread replies received, reactions received
  -> Function Node (aggregate):
     Combine all data sources into a single weekly_data object
```

### 2. Analyze content performance patterns

Using the activity log data, classify every interaction from the past week by content type:

| Content Type | Metric | Calculation |
|-------------|--------|-------------|
| Expert Answer | Engagement score | (thread replies + reactions) / responses of this type |
| Framework Share | Engagement score | (thread replies + reactions) / responses of this type |
| Data Share | Engagement score | (thread replies + reactions) / responses of this type |
| Discussion Starter | Engagement score | (thread replies + reactions) / responses of this type |
| Resource Curator | Engagement score | (thread replies + reactions) / responses of this type |

Identify:
- **Top-performing content type** this week vs. 4-week average
- **Top-performing topic** (what subject matter drove the most engagement)
- **Top-performing community** (which workspace/channel generated the most referral sessions per interaction)
- **Declining content type** (any content format dropping more than 30% in engagement week-over-week)

### 3. Detect member behavior signals

From Slack API read data and PostHog tracking, identify:

**Warm leads** — community members who:
- Replied to 2+ of your threads in the past 14 days
- Clicked through to your site (community_referral_visit) more than once
- Asked a question directly related to your product category

**Cooling engagement** — communities where:
- Your average reactions per post dropped 30%+ vs. 4-week average
- Thread reply count is declining for 2+ consecutive weeks
- No referral sessions in the last 7 days despite active posting

**Emerging topics** — new discussion themes appearing in your target communities:
- Keyword analysis on the last 200 messages per community
- Compare against your existing keyword lists
- Flag topics you have expertise in but have not yet posted about

### 4. Generate the brief using Claude

Pass the aggregated data to the `hypothesis-generation` fundamental (repurposed for content strategy):

```
Prompt structure:
  Context: Weekly community engagement data for {play_slug}
  Data: {weekly_data object from step 1}
  Content performance: {analysis from step 2}
  Member signals: {signals from step 3}

  Generate a weekly community engagement brief with:
  1. Executive summary (3 sentences: what happened, what's working, what needs attention)
  2. Community-by-community performance table (score, trend, sessions, signups)
  3. Content strategy for next week:
     - 3 specific post topics with target communities and recommended format
     - Which content types to increase/decrease
     - Any communities to deprioritize or add
  4. Warm leads to follow up with (name, community, signal, suggested action)
  5. Risks and flags (declining communities, emerging competitors, rule changes)
```

### 5. Distribute the brief

Post the generated brief to:
1. Internal Slack channel (e.g., #community-weekly)
2. Attio — store as a note on the play's campaign record for historical reference
3. If running at Durable level, feed the content strategy recommendations back into the `slack-discord-content-posting` drill's weekly content plan

### 6. Track brief accuracy over time

After 4 weeks of briefs, add a retrospective step:
- Did the recommended post topics actually perform well?
- Were the warm lead predictions accurate (did they convert)?
- Were the risk flags valid?

Score each brief's predictions against actual outcomes. Use this accuracy data to tune the prompt in step 4. Target: 60%+ of weekly content recommendations should outperform the 4-week average engagement.

## Output

- Weekly intelligence brief with community performance summary
- 3 specific content recommendations for the coming week
- Warm lead list with suggested follow-up actions
- Risk flags for declining communities or competitive threats
- Historical brief archive in Attio for trend analysis

## Triggers

- Automated: weekly (every Monday, after community-health-scoring completes)
- Ad-hoc: before quarterly community strategy reviews
- On-demand: when evaluating whether to enter or exit a community
