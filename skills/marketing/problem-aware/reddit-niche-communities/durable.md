---
name: reddit-niche-communities-durable
description: >
  Reddit and community participation — Durable Intelligence. Agent-driven weekly
  optimization of subreddit allocation, content strategy, and engagement timing.
  Auto-detects declining communities, discovers new ones, and sustains referral
  traffic at or above Scalable baseline for 6 months.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving referral sessions and signups over 6 months; never drops >20% below Scalable baseline for 2+ consecutive weeks"
kpis: ["Referral sessions from reddit.com (weekly)", "Signups attributed to reddit.com (weekly)", "Community authority score (avg upvotes per comment, trailing 30 days)", "New subreddits discovered and activated per month"]
slug: "reddit-niche-communities"
install: "npx gtm-skills add marketing/problem-aware/reddit-niche-communities"
drills:
  - community-monitoring-automation
  - community-response-crafting
  - community-content-posting
  - community-reconnaissance
  - dashboard-builder
  - threshold-engine
---

# Reddit and Community Participation — Durable Intelligence

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Make community engagement self-sustaining through agent-driven optimization. The agent monitors performance, detects declines, discovers new communities, recommends content strategy shifts, and ensures referral traffic never drops significantly below the Scalable baseline.

**Pass threshold:** Referral sessions and signups from reddit.com sustained at or above the Scalable baseline (≥ 50 sessions/week, ≥ 6 signups/week) for 6 consecutive months. No 2-week period drops more than 20% below baseline.

## Leading Indicators

- Weekly referral sessions trend stable or increasing
- New subreddits being discovered and activated each month
- Community authority growing: average upvotes per comment trending up over 6 months
- Agent recommendations being acted on and producing measurable improvement
- Declining communities being detected early and reallocated

## Instructions

### 1. Build the community performance dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard with:

**Panel 1 — Referral traffic trend (line chart):**
- Weekly `community_referral_visit` events, last 6 months
- Overlay the Scalable baseline as a reference line
- Break down by subreddit (top 5) with "Other" grouping

**Panel 2 — Signup attribution (bar chart):**
- Weekly `community_signup` events, last 6 months
- Grouped by subreddit

**Panel 3 — Community authority score (line chart):**
- Average upvotes per comment (from activity log), trailing 30-day window
- Trend over 6 months

**Panel 4 — Conversion funnel (funnel chart):**
- `community_referral_visit` → pricing/docs page viewed → `signup_started` → `signup_completed`
- By subreddit

**Panel 5 — Engagement efficiency (line chart):**
- Referral sessions per hour of engagement, weekly
- Tracks whether automation is improving ROI

**Panel 6 — Subreddit health table:**
- Each subreddit as a row
- Columns: sessions this week, sessions change vs last week, avg upvotes, posts/comments this week, status (green/yellow/red)

### 2. Configure automated decline detection

Run the `threshold-engine` drill to set up guardrails:

**Guardrail 1 — Weekly referral drop:**
- If referral sessions from reddit.com drop >20% below the rolling 4-week average for 2 consecutive weeks, trigger an alert
- n8n workflow: weekly PostHog query → compare to trailing average → if below threshold, Slack alert with subreddit-level breakdown

**Guardrail 2 — Subreddit-level decline:**
- If any individual subreddit's referral sessions drop to zero for 2 consecutive weeks, flag it for review
- Possible causes: subreddit rule change, shadowban, topic shift, seasonal dip

**Guardrail 3 — Engagement quality drop:**
- If average upvotes per comment drops below 3 for 2 consecutive weeks, flag for content quality review
- Possible causes: over-posting, wrong tone, community fatigue

### 3. Automate weekly agent analysis

Build an n8n workflow that runs every Monday and produces a strategic recommendation:

```
Schedule Trigger (Monday 8am)
  → PostHog API: Pull weekly metrics (referral sessions, signups, upvotes) by subreddit
  → PostHog API: Pull conversion funnel data
  → Function Node: Compare each subreddit's performance to its trailing 4-week average
  → AI Agent Node (Claude API):
    Input: Weekly metrics, subreddit performance trends, recent A/B test results
    Prompt: "Analyze this week's Reddit community engagement data.
      1. Which subreddits are growing vs declining? Why?
      2. What content types drove the most referral sessions?
      3. Are there any subreddits we should deprioritize or increase focus on?
      4. Recommend 2-3 specific actions for next week.
      5. Flag any guardrail breaches.
      Output as a structured weekly brief."
  → Slack Node: Post the weekly brief to #reddit-engagement
```

### 4. Automate new community discovery

Build a monthly n8n workflow for ongoing reconnaissance:

```
Schedule Trigger (1st of month, 8am)
  → Reddit API Node: Search for subreddits matching ICP keywords (same keywords from reconnaissance)
  → Function Node: Filter out subreddits already in our target list
  → Function Node: For each new candidate, fetch subscriber count, activity, and sample posts
  → AI Agent Node (Claude API):
    Input: New candidate subreddits with metrics and sample posts
    Prompt: "Evaluate these newly discovered subreddits for ICP fit and engagement potential.
      Score each on: ICP fit (1-5), activity (1-5), engagement (1-5), accessibility (1-5).
      Recommend which ones to add to our target list and why."
  → Slack Node: Post recommendations to #reddit-engagement
```

**Human action required:** Review the agent's new subreddit recommendations. For approved subreddits, the agent creates engagement profiles and adds them to the monitoring pipeline.

### 5. Run continuous optimization experiments

Each month, the agent proposes and runs one optimization experiment:

**Month 1:** Optimal posting time — test posting at different times of day and measure referral sessions per post.

**Month 2:** Content format optimization — increase the winning format from Scalable A/B tests and measure whether doubling down maintains or improves performance.

**Month 3:** Cross-pollination — take top-performing content from one subreddit and adapt it for a different subreddit. Measure whether the approach transfers.

**Month 4:** Depth vs breadth — for one month, focus effort on top 3 subreddits only (depth). Compare referral sessions to the previous month's broader approach.

**Month 5:** Emerging community bet — allocate 20% of engagement time to newly discovered subreddits. Measure if any become top performers.

**Month 6:** Full portfolio review — the agent analyzes 6 months of data and recommends the optimal subreddit allocation, content mix, and engagement cadence going forward.

### 6. Monthly health check

The agent produces a monthly report:

```
Reddit Community Play — Month X Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REFERRAL SESSIONS: XXX/month (target: ≥200/month | status: PASS/FAIL)
SIGNUPS: XX/month (target: ≥25/month | status: PASS/FAIL)
GUARDRAIL BREACHES: X this month

SUBREDDIT PORTFOLIO:
  Active: X subreddits
  Added this month: X
  Retired this month: X

TOP PERFORMERS:
  1. r/SUBREDDIT — XX sessions, XX signups
  2. r/SUBREDDIT — XX sessions, XX signups

EXPERIMENTS:
  Current: [experiment name]
  Result of last experiment: [outcome and recommendation]

RECOMMENDATION FOR NEXT MONTH:
  [Agent's strategic recommendation]
```

### 7. Sustain the system

The Durable level runs indefinitely. The agent's role is to:
- Keep the monitoring pipeline running and keywords fresh
- Detect declines before they become crises
- Discover and onboard new communities as the landscape shifts
- Ensure content quality doesn't decay (by analyzing upvote trends)
- Optimize engagement allocation based on data, not habit

The human's role is to:
- Review and post agent-drafted responses daily (15-20 min)
- Act on agent recommendations from weekly briefs
- Approve new subreddit additions and retirements
- Write original posts that require personal experience or opinion

## Time Estimate

| Activity | Time |
|----------|------|
| Dashboard and guardrail setup | 4 hours |
| Weekly agent analysis workflow | 3 hours |
| Monthly discovery workflow | 2 hours |
| Daily engagement (180 days x 20-30 min) | 70-90 hours |
| Original posts (50-70 posts x 30 min) | 25-35 hours |
| Monthly experiment setup and analysis (6x) | 12 hours |
| Monthly health check review (6x) | 6 hours |
| **Total** | **~125-150 hours** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for engagement | Free (personal account) |
| PostHog | Dashboard, funnels, cohorts, attribution | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Monitoring, agent workflows, weekly analysis | Self-hosted: Free / Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Syften | Real-time keyword monitoring | Standard: $39.95/mo ([syften.com](https://syften.com)) |
| Claude API | Agent analysis and response drafting | ~$15-30/mo at typical usage ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated monthly cost:** $80-95/mo (Syften Standard + n8n Cloud + Claude API)

## Drills Referenced

- `community-monitoring-automation` — continuous thread discovery and alerting
- `community-response-crafting` — agent-assisted response drafting with human review
- `community-content-posting` — ongoing original content production
- `community-reconnaissance` — monthly discovery of new subreddits
- `dashboard-builder` — community performance dashboard in PostHog
- `threshold-engine` — guardrails and decline detection automation
