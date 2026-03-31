---
name: slack-community-program-scalable
description: >
  Slack Community Program — Scalable Automation. Scale community engagement to 10+
  workspaces with automated health scoring, A/B tested content strategies, and
  data-driven community portfolio reallocation.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Scalable Automation"
time: "75 hours over 4 months"
outcome: ">=750 workspace members, >=200 WAU, and >=25 qualified leads/month sustained over 4 months"
kpis: ["Qualified leads per month", "Referral sessions per community per week", "Engagement efficiency (sessions per hour invested)", "Content type conversion rate", "Community portfolio health score"]
slug: "slack-community-program"
install: "npx gtm-skills add marketing/solution-aware/slack-community-program"
drills:
  - community-health-scoring
  - ab-test-orchestrator
  - threshold-engine
---

# Slack Community Program — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

Find the 10x multiplier: scale from 3-5 communities to 10-15, automate community health monitoring, and run systematic experiments on content strategy to maximize qualified leads per hour invested. Pass threshold: >=750 workspace members, >=200 WAU, and >=25 qualified leads/month sustained over 4 months.

## Leading Indicators

- Community health scoring pipeline running weekly with all communities scored (signal: portfolio visibility)
- At least 2 A/B tests completed in the first 6 weeks with statistically significant results (signal: learning velocity)
- Engagement efficiency (referral sessions per hour invested) improving month-over-month (signal: scaling without proportional effort)
- At least 3 communities consistently scoring 60+ on health scorecard (signal: diversified pipeline)

## Instructions

### 1. Deploy community health scoring

Run the `community-health-scoring` drill. This builds a weekly automated pipeline that:

- Scores every active community (0-100) on five weighted signals: referral volume (30%), conversion rate (25%), engagement efficiency (20%), engagement trend (15%), pipeline attribution (10%)
- Classifies communities as thriving (80-100), healthy (60-79), watch (40-59), declining (20-39), or dormant (0-19)
- Generates a weekly health report posted to Slack with portfolio summary, top performers, declining communities, and reallocation recommendations
- Configures PostHog anomaly detection alerts for referral spikes, referral collapses, and conversion rate shifts

Use the first 2 weeks of health data to establish baselines. After 4 weeks, the trend signals become meaningful.

**Reallocation rules (enforce automatically):**
- Thriving communities: increase posting frequency to daily
- Healthy communities: maintain current cadence (2-3 posts/week)
- Watch communities: reduce to 1 post/week, investigate cause of decline
- Declining communities: pause original content, respond to alerts only
- Dormant communities: archive from active monitoring, re-evaluate quarterly

### 2. Expand community portfolio

Re-run the `slack-discord-reconnaissance` drill (from Smoke) to discover new communities. Target criteria for Scalable:
- Add 5-8 new communities to the portfolio (net 10-15 active communities total)
- Prioritize communities adjacent to your existing top performers (similar ICP, different sub-niche)
- Include 1-2 communities where competitors are NOT present (first-mover advantage)
- Consider upgrading monitoring from n8n polling (30-min delay) to Syften ($20-100/mo) for faster response times in high-value communities

### 3. Run systematic content experiments

Run the `ab-test-orchestrator` drill to test content strategy variables. Run one test at a time, minimum 2 weeks per test, 100+ observations per variant.

**Experiment queue (run in order):**

1. **Content format test:** Expert Answers vs. Tactical Playbooks in your top 3 communities. Metric: referral sessions per post. Hypothesis: Tactical Playbooks generate 2x more referral sessions because they establish deeper authority.

2. **Posting time test:** Morning (9-11am community timezone) vs. Afternoon (1-3pm). Metric: thread replies within 4 hours. Hypothesis: Morning posts get 30% more replies because members check Slack at the start of their day.

3. **Self-reference test:** Posts that mention your product casually mid-post vs. posts with zero product mentions. Metric: DMs and referral sessions. Hypothesis: Casual mid-post mentions generate more referral sessions without hurting engagement score.

4. **Response depth test:** Short expert answers (under 100 words) vs. detailed framework shares (300+ words) to monitoring alerts. Metric: thread continuation rate (does the OP or others reply to your response?). Hypothesis: Detailed responses generate 50% more follow-up conversation.

Document every experiment result. After 4 experiments, you will have a data-backed content playbook: what to post, when, where, and how much to reference your product.

### 4. Scale daily presence with efficiency

Using health scores and experiment results, build a daily engagement workflow:

1. Morning: review monitoring alerts from overnight. Respond to all high-priority, 50%+ of medium.
2. Mid-day: post 1 original content piece in a thriving community (using the winning content format from experiments).
3. Afternoon: follow up on yesterday's threads. Reply to all thread responses.
4. Weekly: review health report, reallocate effort per reallocation rules.

Target: 5-8 community interactions per day across all communities, spending no more than 45 minutes total (efficiency should increase as you develop reusable content templates).

### 5. Upgrade monitoring for scale

If n8n polling (30-min delay) is causing you to miss high-value threads:
- Upgrade to Syften ($20-100/mo) for near-real-time alerts (~1 min delay)
- Or upgrade to Common Room ($1,000+/mo) if you need enriched member profiles and cross-platform aggregation
- For most teams at Scalable level, Syften is the right cost/benefit trade-off

### 6. Evaluate against threshold

Run the `threshold-engine` drill monthly for 4 months:
- Workspace members >= 750
- WAU >= 200
- Qualified leads/month >= 25 (sustained for at least 2 consecutive months)

**Decision:** If PASS for 2+ consecutive months, proceed to Durable. If FAIL with growing trend (improving month-over-month), continue for 2 more months. If FAIL with flat or declining trend, diagnose: are the right communities selected? Is content quality declining? Are competitors saturating your best communities?

## Time Estimate

- Community health scoring setup: 4 hours
- Portfolio expansion (reconnaissance + onboarding): 6 hours
- A/B test design and management (4 experiments over 4 months): 12 hours
- Daily community engagement (45 min/day over 4 months): 45 hours
- Weekly analysis and optimization: 8 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Slack (free or Pro tier) | Participate in communities | Free - [$7.25/user/mo annual](https://slack.com/pricing) |
| Syften | Real-time community keyword monitoring | [$20-$100/mo](https://syften.com/) |
| PostHog | Analytics, experiments, anomaly detection | Standard stack (excluded) |
| n8n | Health scoring automation, alert routing | Standard stack (excluded) |
| Attio | CRM, lead attribution, community records | Standard stack (excluded) |

**Total play-specific cost: ~$20-100/mo** (Syften for monitoring upgrade)

## Drills Referenced

- `community-health-scoring` — weekly automated scoring and portfolio health reporting for all communities
- `ab-test-orchestrator` — design, run, and evaluate A/B tests on content strategy variables
- `threshold-engine` — monthly evaluation against pass criteria over the 4-month window
