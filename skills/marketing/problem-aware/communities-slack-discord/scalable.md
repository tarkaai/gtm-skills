---
name: communities-slack-discord-scalable
description: >
  Slack/Discord Community Rhythm — Scalable Automation. Scale to 10+ communities
  with health scoring, A/B test response strategies, automate content scheduling,
  and hit 10+ meetings over 2 months without proportional time increase.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">= 10 meetings booked from community engagement over 2 months"
kpis: ["Community health score (portfolio avg)", "Referral sessions per week", "Meetings booked per month", "Cost per meeting", "Engagement efficiency (sessions per hour invested)"]
slug: "communities-slack-discord"
install: "npx gtm-skills add marketing/problem-aware/communities-slack-discord"
drills:
  - community-health-scoring
  - ab-test-orchestrator
---

# Slack/Discord Community Rhythm — Scalable Automation

> **Stage:** Marketing > ProblemAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

Find the 10x multiplier for community engagement. Scale from 5 communities to 10-15 without proportional time increase. Automate community health scoring to detect which communities are worth investment and which should be pruned. A/B test response strategies to maximize conversion from thread response to meeting booked. Achieve 10+ meetings over 2 months at improving efficiency (meetings per hour invested).

## Leading Indicators

- Active communities monitored: 10-15
- Keyword alerts processed per week: 35-75 (5-15/day)
- Threads responded to per week: 10-15
- Original content posts per week: 3-5 across communities
- Referral sessions per week: 25+ (growing)
- Community health scores: portfolio average >= 60/100
- Engagement efficiency: improving week-over-week (more sessions per hour invested)

## Instructions

### 1. Expand community portfolio

Re-run the `slack-discord-reconnaissance` drill (from Smoke) to discover additional communities. The target is 10-15 active communities:
- Promote secondary communities from Baseline that showed traction to primary status.
- Add 3-5 new communities from discovery.
- Drop any communities that produced zero referrals during Baseline.
- Consider paid community memberships for premium Slack groups that gate access (budget: $50-200/mo total across all paid memberships).

Update the Attio community targets list with the expanded portfolio.

### 2. Deploy community health scoring

Run the `community-health-scoring` drill to automate weekly scoring of every community in your portfolio.

**Configure the scoring system:**
- Build an n8n workflow that runs every Monday at 6am.
- For each community, compute a score (0-100) based on: referral volume (30%), conversion rate (25%), engagement efficiency (20%), engagement trend (15%), and pipeline attribution (10%).
- Classify each community: thriving (80-100), healthy (60-79), watch (40-59), declining (20-39), dormant (0-19).
- Post the weekly Community Health Report to Slack.
- Set up PostHog anomaly alerts for referral spikes (3x average) and collapses (<30% of average).

**Use the scores to allocate effort:**
- Thriving communities: increase to daily engagement and 2 content posts/week.
- Healthy communities: maintain 3-4 engagements/week and 1 content post/week.
- Watch communities: 1-2 engagements/week, investigate what changed.
- Declining communities: pause engagement, reallocate time to thriving communities.
- Dormant communities: archive from active list.

### 3. A/B test response strategies

Run the `ab-test-orchestrator` drill to systematically test what drives the most meetings from community engagement.

**Test 1 — Response format:**
- Variant A: Short, direct answers (under 100 words)
- Variant B: Detailed, structured responses with frameworks (200-400 words)
- Metric: DM rate (percentage of responses that result in a DM from the poster or a reader)
- Duration: 2 weeks, minimum 30 responses per variant

**Test 2 — Content type for original posts:**
- Variant A: Tactical Playbook posts (step-by-step guides)
- Variant B: Data Share posts (benchmarks, analysis)
- Variant C: Discussion Starters (questions that prompt community input)
- Metric: Referral sessions per post
- Duration: 4 weeks, minimum 5 posts per variant

**Test 3 — Mention strategy:**
- Variant A: Never mention your product (pure thought leadership)
- Variant B: Mention product casually in 1 of every 5 responses when directly relevant
- Metric: Meeting conversion rate (meetings per 100 responses)
- Duration: 4 weeks

**Test 4 — Response timing:**
- Variant A: Respond within 1 hour of alert (fast)
- Variant B: Respond within 4-6 hours (deliberate, longer response)
- Metric: Thread engagement rate (replies + reactions on your response)
- Duration: 2 weeks

Log all experiment configurations and results in PostHog. After each test, implement the winner across all communities.

### 4. Upgrade monitoring infrastructure

At Scalable level, upgrade from free n8n polling to faster monitoring:
- **Option A:** Add Syften ($39.95/mo Standard plan) for real-time cross-platform keyword monitoring. Route Syften webhooks through n8n for filtering and alerting.
- **Option B:** Add Common Room ($1,000/mo Starter) for unified community intelligence with member enrichment. Common Room auto-enriches community members with LinkedIn and company data, enabling ICP-first response prioritization.

The upgrade is justified when: your Baseline meeting rate proves the channel works, and faster response time would meaningfully increase conversion (test this in Test 4 above).

### 5. Automate content scheduling

Build an n8n workflow to schedule community content:
- Maintain a content queue in Attio or Airtable: topic, community, channel, format, draft, scheduled date.
- The agent generates 5-10 content drafts per week using the `slack-discord-content-posting` drill logic.
- Schedule posts for peak activity hours in each community.
- **Human action required:** Review and approve each draft before it enters the posting queue. Post manually from personal account (or use Slack API scheduled messages for communities where you have API access).

### 6. Evaluate against threshold

Pass threshold: >= 10 meetings booked from community engagement over 2 months.

Track in PostHog and Attio:
- Total community-attributed meetings (UTM or CRM attribution)
- Meetings per community (which communities drive the most?)
- Cost per meeting: (total hours invested + tool costs) / meetings booked
- Engagement efficiency trend: is the ratio of meetings-to-hours improving?

If PASS: The community channel scales. Proceed to Durable.
If FAIL: Diagnose using community health scores:
- If 1-2 communities produce 80%+ of meetings: this is a concentration risk. Invest in diversifying.
- If many communities have high engagement but low conversion: the bottleneck is post-engagement follow-up, not community presence. Optimize the DM-to-meeting conversion path.
- If engagement efficiency is flat: automation is not saving enough time. Audit where manual effort is still required and automate or eliminate it.

## Time Estimate

- 4 hours: Community portfolio expansion and health scoring setup
- 4 hours: A/B test configuration and monitoring infrastructure upgrade
- 20 hours: Daily engagement over 2 months (~15 min/day triage + 30 min/day responses)
- 8 hours: Weekly content creation (1 hour/week x 8 weeks)
- 4 hours: Weekly reporting, test analysis, and community reallocation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Monitoring workflows, content scheduling, health scoring | Free self-hosted; Cloud Pro: EUR 60/mo (https://n8n.io/pricing) |
| PostHog | Attribution tracking, A/B tests, anomaly detection | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Community targets, interaction logging, pipeline attribution | Free for small teams (https://attio.com/pricing) |
| Syften (optional) | Real-time keyword monitoring across platforms | Standard: $39.95/mo (https://syften.com) |
| Common Room (optional) | Unified community intelligence with member enrichment | Starter: $1,000/mo (https://www.commonroom.io/pricing) |
| Paid community memberships | Access to gated Slack/Discord communities | $50-200/mo total |

**Play-specific cost at Scalable level:** $50-240/mo (n8n Cloud + Syften + paid memberships). With Common Room instead of Syften: $1,050-1,260/mo.

## Drills Referenced

- `community-health-scoring` — weekly scoring and ranking of all active communities with reallocation recommendations
- `ab-test-orchestrator` — systematically test response formats, content types, and timing to maximize meeting conversion
