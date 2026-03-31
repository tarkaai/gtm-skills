---
name: q-a-sites-stackoverflow-etc-baseline
description: >
  Q&A Site Authority -- Baseline Run. First always-on automation: monitor Q&A platforms
  for new questions, answer 3-5 per day, track performance with PostHog attribution.
stage: "Marketing > Problem Aware"
motion: "CommunitiesForums"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">= 80 profile clicks and >= 3 leads over 2 weeks"
kpis: ["Profile views", "Profile click rate"]
slug: "q-a-sites-stackoverflow-etc"
install: "npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc"
drills:
  - posthog-gtm-events
  - qa-monitoring-automation
  - qa-answer-crafting
  - threshold-engine
---

# Q&A Site Authority -- Baseline Run

> **Stage:** Marketing > Problem Aware | **Motion:** CommunitiesForums | **Channels:** Other

## Outcomes

Pass threshold: >= 80 profile clicks and >= 3 leads (signups, demo requests, or inbound emails) over 2 weeks.

This proves the play works as an always-on system, not just a one-off effort. The agent monitors platforms for new questions automatically and maintains a daily answering cadence. You are testing: (a) whether consistent presence compounds authority, (b) whether monitoring automation catches good questions before competitors, and (c) whether UTM-attributed traffic from Q&A platforms converts.

## Leading Indicators

- Daily question alerts arriving in Slack with >= 5 actionable questions per day
- Answers averaging >= 5 upvotes within 72 hours (authority building)
- Stack Overflow reputation crossing the 50-point threshold (unlocks commenting privilege)
- Referral sessions from Q&A platforms appearing in PostHog with UTM attribution
- Week-over-week growth in profile views

## Instructions

### 1. Set up PostHog event tracking

Run the `posthog-gtm-events` drill to configure Q&A-specific tracking:

1. Define events: `qa_referral_visit` (fired when a visitor arrives with `utm_source=stackoverflow|quora|devto`), `qa_signup`, `qa_meeting_booked`.
2. Configure UTM parameter capture: all links shared in Q&A answers use `utm_source=PLATFORM&utm_medium=qa&utm_campaign=q-a-sites-stackoverflow-etc&utm_content=ANSWER_ID`.
3. Set up referrer-based detection as fallback: if `$initial_referrer` contains `stackoverflow.com`, `quora.com`, or `dev.to`, tag the session as Q&A-sourced.
4. Create a PostHog funnel: `qa_referral_visit` -> `page_viewed` (beyond landing) -> `qa_signup`.
5. Set person properties: `first_touch_channel: qa-platform`, `lead_source_detail: PLATFORM_NAME`.

### 2. Deploy monitoring automation

Run the `qa-monitoring-automation` drill to build the always-on pipeline:

1. **Stack Overflow monitor** (n8n workflow, every 30 minutes): Polls `GET /search/advanced?tagged=TAGS&fromdate=TIMESTAMP&accepted=false&site=stackoverflow` for new questions. Deduplicates against stored IDs. Scores by answer count, views, recency, and tag relevance. Sends high/medium priority alerts to `#qa-engagement` Slack channel.

2. **Quora monitor** (n8n workflow, every 6 hours): Searches `site:quora.com KEYWORDS` via SerpAPI restricted to last 24 hours. Parses question URLs and titles. Alerts to the same Slack channel.

3. **Dev.to monitor** (n8n workflow, every 2 hours): Polls `GET /api/articles?tag=help&top=1&per_page=30` for recent help posts matching your keywords.

4. **Daily summary** (n8n workflow, 9 AM): Aggregates questions discovered, alerted, and responded to. Posts summary to Slack.

Target: 5-15 actionable alerts per day across all platforms. If volume is too high or too low after the first week, tune tag filters and score thresholds.

### 3. Answer 3-5 questions per day

Run the `qa-answer-crafting` drill for each alert. Maintain a daily cadence:

1. Triage morning alerts: pick the top 3-5 by priority score.
2. For each, the agent reads the full question and existing answers, identifies the gap, drafts the answer.
3. For Stack Overflow: include UTM-tagged links only when linking to genuinely useful educational content (1 in 10 answers max). For Quora: same rule.
4. Post answers. For Quora, **human action required** to post via web interface.
5. Follow up on yesterday's answers: respond to comments, log performance metrics.

Over 2 weeks, target 30-50 answers total.

### 4. Track performance in Attio

Update the Attio "Q&A Answer Queue" list with performance data for each answer:
- Upvote count (at 24h, 72h, 1 week)
- Accepted answer status
- Referral sessions attributed (from PostHog)
- Any leads generated (signups with Q&A attribution)

Create a CRM contact record for each lead with `lead_source: qa-platform` and `lead_source_detail: stackoverflow|quora|devto`.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the end of 2 weeks:

- Profile clicks: aggregate across platforms -- target >= 80 total.
- Leads: count signups, demo requests, or inbound emails with Q&A attribution -- target >= 3.

**PASS**: >= 80 profile clicks and >= 3 leads. Proceed to Scalable.
**FAIL**: Diagnose. Check: Are answers getting upvoted? (If not, quality issue.) Are profile clicks happening but no leads? (Profile or landing page issue.) Are alerts catching the right questions? (Keyword tuning issue.) Iterate and re-run Baseline.

## Time Estimate

- PostHog event setup: 1 hour
- n8n monitoring workflows (3 platforms + summary): 2 hours
- Answering 30-50 questions (15-20 min each): 7.5-16 hours
- Performance tracking and follow-ups: 1.5 hours
- Total: ~12-20 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stack Exchange API | Read/write questions and answers | Free (10,000 req/day with key) |
| Dev.to API | Read articles, post responses | Free |
| SerpAPI | Monitor Quora questions via Google search | From ~$50/mo for 5,000 searches ([serpapi.com/pricing](https://serpapi.com/pricing)) |
| PostHog | Track referral traffic, conversions, funnels | Free tier up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Monitoring workflows and scheduling | Free self-hosted or from $20/mo cloud ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Store answer queue, contact records, logs | Included in standard stack |

Estimated play-specific cost: $0-50/mo (SerpAPI only needed if monitoring Quora; everything else is free tier)

## Drills Referenced

- `posthog-gtm-events` -- set up Q&A-specific event tracking and attribution
- `qa-monitoring-automation` -- automated monitoring pipeline for new questions across platforms
- `qa-answer-crafting` -- draft and post authoritative answers
- `threshold-engine` -- evaluate pass/fail against 80 profile clicks / 3 leads threshold
