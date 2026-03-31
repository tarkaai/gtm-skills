---
name: hackathon-series-automation
description: Automate recurring hackathon series operations including challenge rotation, participant recruitment, cross-event analytics, and community building
category: Events
tools:
  - n8n
  - Loops
  - Attio
  - PostHog
  - Clay
  - Cal.com
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - loops-broadcasts
  - loops-audience
  - attio-lists
  - attio-contacts
  - posthog-custom-events
  - posthog-funnels
  - calcom-event-types
  - clay-people-search
  - clay-enrichment-waterfall
---

# Hackathon Series Automation

This drill transforms one-off hackathons into a repeatable, automated series that runs quarterly with minimal manual overhead. The agent handles challenge rotation, participant recruitment, cross-event analytics, and community management. The human designs challenges and judges submissions.

## Prerequisites

- At least 1 completed hackathon with performance data (from Baseline level)
- n8n instance with active connections to Loops, Attio, and PostHog
- Hackathon platform account (Devpost, Luma, or Devfolio)
- Clay table with developer prospect data
- A challenge backlog with at least 4 hackathon themes

## Steps

### 1. Build the challenge calendar

Create a challenge backlog ranked by expected participation. Score each theme on:

- **Product feature coverage (1-5)**: Does this challenge showcase a different product capability than the last hackathon? Avoid repeating the same API surface area.
- **Developer demand (1-5)**: Is there active developer interest in this problem domain? Check: GitHub trending repos, dev.to hot topics, Hacker News discussions.
- **Lead quality potential (1-3)**: 1 = broad developer audience, 2 = ICP-adjacent developers, 3 = direct ICP matches. Bias toward 2-3.

Using `attio-lists`, create a "Hackathon Calendar" list with fields: theme, challenge title, target date, target participant count, prize budget, challenge document status, and series position (e.g., "Q2 2026 -- Challenge 3 of 4").

Schedule hackathons quarterly. Alternate between virtual (broader reach) and in-person (deeper engagement) when budget allows.

### 2. Automate the recruitment engine

Using `n8n-scheduling`, create a workflow that triggers 6 weeks before each hackathon:

**Week -6: Recruitment kickoff**
- Create the hackathon event on the platform (Devpost/Luma)
- Generate registration page with challenge preview and prize info
- Draft community announcement posts for Discord, Slack, dev.to, and Reddit

**Week -4: First outreach wave**
- Using `clay-people-search`, find developers who match the challenge theme: contributors to relevant open-source projects, authors of relevant blog posts, speakers at related meetups
- Enrich with `clay-enrichment-waterfall` for email and company data
- Add to Loops audience using `loops-audience`
- Send targeted invite via `loops-broadcasts`: challenge details, prizes, and why their skills are a perfect match
- Post community announcements

**Week -2: Second wave + past participants**
- Send a personalized invite to past hackathon participants who did NOT win (motivation: "Come back and win this time")
- Send to non-openers from wave 1
- Launch any paid promotion (LinkedIn developer targeting, Reddit ads in relevant subreddits)
- Using `attio-contacts`, send personal invites to high-value developer prospects in active pipeline ("Build something cool and show us what you can do")

**Week -1: Final push**
- Send last-chance registration email to all audiences
- Post countdown content on social channels
- Set up Cal.com mentor booking slots using `calcom-event-types`
- Provision API keys and product access for all registered participants

**Day 0: Handoff to execution**
- Trigger the `hackathon-challenge-pipeline` drill with all registrant data
- Activate the event support infrastructure (Discord channel, mentor schedule, submission system)

### 3. Build cross-event analytics

Using `posthog-custom-events` and `posthog-funnels`, track metrics across the entire series:

- **Registration funnel per hackathon**: page_viewed -> registered -> kickoff_attended -> submission_received -> qualified_lead
- **Series-level metrics**: Repeat participation rate (% who join 2+ hackathons), challenge theme-to-pipeline correlation, recruitment channel effectiveness per event
- **Cumulative pipeline**: Total qualified leads across all hackathons, average leads per event, conversion to paid, trend over time
- **Community growth**: Discord/Slack member growth from hackathon participants, ongoing engagement rate

Create a PostHog dashboard for the series: registrations by event (bar chart), submission rate trend (line chart), qualified leads per event (bar chart), recruitment channel breakdown (pie chart), repeat participant count (counter).

### 4. Manage the developer community

Hackathons build a developer community over time. Automate community management:

Using `n8n-workflow-basics`, build workflows that:

- **Welcome new community members**: When a hackathon participant joins your Discord/Slack, send a welcome message with: past winning projects, upcoming events, getting-started resources
- **Spotlight submissions**: After each hackathon, create a showcase gallery on your website or Devpost profile. Post the top 5 projects to social channels.
- **Re-engage dormant members**: If a past participant has not visited the community in 60 days, send a re-engagement email with: what they missed (new hackathon results, feature updates), upcoming events, and a direct ask ("What would bring you back?")
- **Track community health**: Monthly metrics: active members, messages per week, projects shared, help requests answered

### 5. Optimize challenge design based on data

After every 2 hackathons, the agent analyzes:

- Which challenge themes drove the most registrations? Most submissions? Highest quality?
- Which prize structures had the best registration-to-submission conversion? (Higher prizes do not always mean more submissions)
- What duration and format (virtual vs. in-person, 24h vs. 1 week) produced the best results?
- Which recruitment channels (email, community, paid, personal invite) yielded the highest-quality participants?
- Which product features got the most API usage? Which were ignored?

Store findings in Attio as notes on the hackathon calendar. Adjust upcoming hackathons based on data.

## Output

- Automated quarterly hackathon series with minimal manual overhead
- Cross-event analytics dashboard in PostHog
- Growing developer community with re-engagement automation
- Data-driven challenge design optimization

## Triggers

- Series automation runs continuously with event-triggered workflows
- Challenge calendar review: quarterly
- Community health check: monthly
