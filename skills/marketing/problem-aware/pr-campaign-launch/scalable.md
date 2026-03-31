---
name: pr-campaign-launch-scalable
description: >
  PR Campaign Launch — Scalable. Automate media opportunity detection, pitch generation, and
  relationship management via n8n. Scale to quarterly launch campaigns with 50+ targets,
  continuous source request monitoring, and full referral-to-pipeline attribution.
stage: "Marketing > ProblemAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Scalable"
time: "80 hours over 6 months"
outcome: ">=40 placements and >=60 qualified leads from earned media over 6 months, with pitch-to-placement rate within 20% of Baseline benchmark"
kpis: ["Placements per month", "Pitch-to-placement rate", "Referral traffic per placement", "PR-attributed pipeline value", "Source request win rate", "Cost per PR-attributed lead"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - media-target-research
  - media-pitch-outreach
  - media-relationship-automation
  - pr-performance-monitor
---

# PR Campaign Launch — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

Scale earned media from launch-specific campaigns to a continuous press presence. Opportunity detection, pitch drafting, and relationship nurture are automated via n8n. Brand and competitor mention monitoring runs always-on. The media target list refreshes monthly. Every placement is tracked through to pipeline impact.

**Pass threshold:** >=40 placements and >=60 qualified leads from earned media over 6 months, with pitch-to-placement rate within 20% of Baseline benchmark.

## Leading Indicators

- Placements per month trending upward (goal: 7+ per month by month 3)
- Reactive PR (source requests, trending topics) produces at least 30% of total placements
- Journalist relationship scores improving: 5+ contacts at score >= 3 (repeat relationship)
- Referral traffic from earned media grows month over month
- PR-attributed pipeline value exceeds tool costs by 5x

## Instructions

### 1. Scale the Media List

Run the `media-target-research` drill at Scalable volume (75+ targets):

1. Expand to Tier 3 targets: general business and tech media
2. Re-run monthly to find new outlets, journalists, and podcasts
3. Add competitor coverage tracking: for every competitor mention detected, add the journalist to the target list
4. Maintain the Clay table with automated enrichment refreshes (monthly cron via n8n)
5. Use inbox rotation for Instantly: 2-3 sending accounts to support 50+ pitches per campaign

### 2. Run Quarterly Launch Campaigns

Execute the `media-pitch-outreach` drill as quarterly campaigns:

1. Each quarter, identify 1-2 launch milestones (product release, data report, customer win, funding)
2. Build campaign-specific pitch angles for each milestone
3. Segment targets by angle relevance and tier
4. Execute with tiered personalization: Tier 1 gets full hand-personalization, Tier 2 gets template + 3 merge fields, Tier 3 gets template + 2 merge fields
5. Run each campaign for 3-4 weeks with follow-up sequences
6. Log all activity in Attio with campaign tags for attribution

### 3. Deploy Media Relationship Automation

Run the `media-relationship-automation` drill:

1. **Source request detection:** Build an n8n workflow that ingests Qwoted and Featured.com alerts, evaluates relevance using Claude API, drafts responses, and routes to Slack for founder approval
2. **Brand and competitor monitoring:** Configure Mention API (or Google Alerts + n8n) to detect brand mentions, competitor coverage, and trending topics in your space
3. **Reactive pitch workflow:** When a PR opportunity is detected (trending topic, journalist request, competitor coverage), n8n drafts a personalized pitch, routes for human approval, and sends on approval
4. **Journalist relationship tracking:** Automate relationship score updates in Attio based on interaction history (pitches, replies, placements, social engagement)
5. **Post-placement amplification:** When a placement is logged in Attio as "published," n8n auto-generates social posts, routes for approval, and schedules via Buffer/Typefully

### 4. Deploy PR Performance Monitoring

Run the `pr-performance-monitor` drill:

1. Build the PostHog PR dashboard (5 panels: outreach pipeline, placement tracking, referral traffic, placement-to-pipeline attribution, media relationship health)
2. Implement the PR event taxonomy in PostHog
3. Configure anomaly detection: pitch-to-reply rate drops, placement drought, referral traffic decline, competitor mention surges
4. Deploy weekly automated reports via n8n
5. Build referral traffic attribution with UTM structure

### 5. Set Guardrails

- **Pitch volume cap:** Maximum 20 new pitches per week to protect sender reputation and ensure personalization quality
- **Quality gate:** If pitch-to-reply rate drops below 10% for 2 consecutive campaigns, pause outreach and audit pitch quality
- **Relationship protection:** Never pitch the same journalist more than once per quarter unless they have expressed interest. Track pitch frequency in Attio.
- **Embargo integrity:** Never break an embargo. If a journalist asks for an embargo, track the date in Attio and set an n8n reminder.
- **Source request SLA:** Respond to relevant source requests within 4 hours of detection. Stale responses rarely get selected.

### 6. Monthly Optimization

Monthly review cycle:

1. Pull the monthly deep-dive from the `pr-performance-monitor` drill
2. Analyze:
   - Which outlet types produce the most pipeline value per pitch?
   - Which pitch angles have the highest placement rate?
   - Is reactive PR (source requests, trending topics) outperforming proactive pitching?
   - Which journalists are becoming repeat placements (relationship building working)?
3. Adjust for the next month:
   - Shift outreach effort toward highest-performing outlet types
   - Refresh pitch angles based on what is landing
   - Target specific journalists for relationship deepening
   - Add new outlets from competitive coverage monitoring

## Time Estimate

- 4 hours: Scalable media list setup and monthly refresh automation
- 12 hours: Quarterly campaign execution (3 hours/campaign x 4 campaigns = partial, 2 full campaigns in 6 months)
- 8 hours: Media relationship automation setup (n8n workflows)
- 6 hours: PR performance monitoring setup (dashboard, events, anomaly detection)
- 30 hours: Ongoing reactive PR, source requests, and reply handling (over 6 months)
- 12 hours: Monthly optimization reviews (2 hours/month x 6 months)
- 8 hours: Placement amplification and social distribution

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Sequenced media outreach with inbox rotation | $77/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Mention | Brand and competitor monitoring API | $41/mo (Solo) — [mention.com/pricing](https://mention.com/en/pricing/) |
| Qwoted | Source request monitoring (Pro for faster alerts) | $99/mo (Pro) — [qwoted.com](https://www.qwoted.com) |
| Featured.com | Expert quote placements | Free tier — [featured.com](https://featured.com) |
| n8n | Automation — opportunity detection, reactive pitch, amplification | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — PR dashboards, attribution, anomaly detection | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — media contacts, pitch pipeline, relationship tracking | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — media contact data, monthly refreshes | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Claude API | Pitch drafting, source request responses, opportunity evaluation | ~$30-50/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Instantly ~$77/mo + Mention ~$41/mo + Qwoted ~$99/mo = ~$217/mo play-specific. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `media-target-research` — monthly media list refresh with 75+ targets, Clay enrichment, and scoring
- `media-pitch-outreach` — quarterly launch campaign execution with tiered personalization via Instantly
- `media-relationship-automation` — always-on opportunity detection, reactive pitching, journalist relationship tracking, and post-placement amplification
- `pr-performance-monitor` — continuous monitoring of outreach pipeline, placements, referral traffic, attribution, and relationship health
