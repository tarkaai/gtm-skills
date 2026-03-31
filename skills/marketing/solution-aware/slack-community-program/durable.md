---
name: slack-community-program-durable
description: >
  Slack Community Program — Durable Intelligence. Deploy the autonomous optimization loop
  to continuously detect community engagement anomalies, generate content strategy hypotheses,
  run experiments, and auto-implement winners. Weekly intelligence briefs drive strategy.
  The agent finds and maintains the local maximum.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained community growth (>=10% QoQ) and >=20 qualified leads/month over 12 months with autonomous content optimization"
kpis: ["Quarterly community growth rate", "Qualified leads per month (sustained)", "Experiment win rate", "Engagement efficiency trend (sessions per hour)", "Content strategy adaptation speed"]
slug: "slack-community-program"
install: "npx gtm-skills add marketing/solution-aware/slack-community-program"
drills:
  - autonomous-optimization
  - community-engagement-brief
  - community-health-scoring
---

# Slack Community Program — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

The agent autonomously optimizes community engagement to find and maintain the local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in community health scores and referral data, generate improvement hypotheses (new content formats, different communities, adjusted posting cadence, new keyword sets), run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs from `community-engagement-brief` drive strategy. Converges when successive experiments produce <2% improvement.

Pass threshold: sustained community growth (>=10% QoQ) and >=20 qualified leads/month over 12 months.

## Leading Indicators

- Autonomous optimization loop running daily with anomaly checks producing actionable signals (signal: system is alive)
- At least 1 experiment running at all times with results evaluated within 2 weeks (signal: continuous improvement)
- Weekly engagement briefs generating 3+ specific content recommendations that outperform the 4-week average 60%+ of the time (signal: intelligence is accurate)
- Community portfolio health score trending stable or up quarter-over-quarter (signal: not decaying)
- Experiment win rate above 30% (signal: hypotheses are sound; below 30% indicates the play is near its local maximum)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific KPIs:

**Phase 1 — Monitor (daily via n8n cron):**
- Primary KPIs to watch: qualified leads/month, referral sessions/week, WAU, engagement efficiency
- Pull data from PostHog (`community_referral_visit`, `community_signup`, `community_lead_qualified` events) and community health scores from Attio
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current community portfolio (which communities, posting cadence, content types in rotation), recent experiment results, keyword monitoring configuration
- Pull 8-week metric history from PostHog
- Run hypothesis generation with anomaly data. Community-specific hypothesis templates:
  - "Referral sessions from {community} dropped 35% — hypothesis: posting frequency decreased from 5/week to 2/week due to holiday week. Test: restore 5/week for 2 weeks."
  - "Engagement efficiency declining across all communities — hypothesis: content topics are stale. Test: switch from Tactical Playbooks to Data Shares for 2 weeks."
  - "New community {workspace} producing 3x referral rate of established communities — hypothesis: first-mover advantage in underserved community. Test: increase to daily posting."
  - "Qualified lead rate dropped while referral sessions held steady — hypothesis: landing page or signup flow changed. Test: review product changes; not a community play issue."
- Receive 3 ranked hypotheses. If top hypothesis is high-risk (e.g., exiting a top community, changing brand tone), send Slack alert for human review and STOP. Otherwise proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags where applicable
- For content strategy experiments (most common at Durable): implement the variant content approach for 2 weeks in a subset of communities while maintaining control in others
- For community portfolio experiments: add/remove a community for 4 weeks and measure impact on total qualified leads
- For keyword experiments: adjust monitoring keywords and measure alert quality and response conversion
- Minimum experiment duration: 2 weeks or 50+ data points per variant, whichever is longer
- Log experiment start in Attio with hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog and activity logs
- Decision matrix:
  - **Adopt:** Variant outperformed control by >=10% with 95% confidence. Implement permanently. Log the change.
  - **Iterate:** Results directionally positive but not significant. Generate a refined hypothesis and re-test.
  - **Revert:** Variant underperformed. Restore control. Log the failure and reasoning.
  - **Extend:** Insufficient data. Continue experiment for one more period.
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Generate weekly optimization brief posted to Slack and stored in Attio

**Guardrails (CRITICAL):**
- Maximum 1 active experiment at a time. Never stack experiments.
- If qualified leads drop >30% during an experiment, auto-revert immediately.
- Human approval required for: exiting a top-5 community, changing brand voice/tone, increasing posting frequency above 2x current cadence.
- Cooldown: after a failed experiment (revert), wait 7 days before testing the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.

### 2. Deploy weekly community engagement briefs

Run the `community-engagement-brief` drill. This produces a weekly intelligence report every Monday that synthesizes:

- Community-by-community performance table with health scores, trends, referral sessions, signups
- Content performance analysis: which content types, topics, and communities drove the most engagement and referrals this week vs. 4-week average
- Warm lead identification: community members who replied to 2+ threads, clicked through multiple times, or asked product-category questions
- 3 specific content recommendations for the coming week (topic, community, format)
- Risk flags: declining communities, emerging competitor activity, community rule changes
- Experiment status: active experiments, pending results, recent wins/losses

The brief feeds directly into the autonomous optimization loop — if the brief identifies a declining community or underperforming content type, the optimization loop picks it up in Phase 1 monitoring.

### 3. Maintain community health scoring at scale

Continue running the `community-health-scoring` drill (from Scalable) with these Durable-level enhancements:

- Expand scoring to include **cross-community signals**: members active in multiple of your target communities (high-value targets)
- Add **competitive saturation tracking**: detect when competitors increase presence in your communities (keyword monitoring for competitor brand names in community messages)
- Add **community lifecycle stage**: new (first 4 weeks of engagement), growing (health score improving), mature (health score stable), declining (health score dropping for 4+ weeks)
- Feed lifecycle data into the autonomous optimization loop's hypothesis generation

### 4. Detect convergence and adapt

The autonomous optimization loop runs indefinitely. It detects convergence when successive experiments produce <2% improvement for 3 consecutive experiments. At convergence:

1. The community engagement play has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment cadence to 1 per month (maintenance experiments to detect market shifts)
4. Report to the team: "Community engagement is optimized. Current performance: {metrics}. Further gains require strategic changes — new community platforms (Discord, Reddit), new product positioning, or new ICP segments — rather than tactical optimization."

If a market shift occurs (new competitor enters, community platform changes, ICP behavior shifts), the daily monitoring detects it as an anomaly and re-activates the full optimization loop.

### 5. Evolve the community portfolio

Monthly strategic review (human + agent):
- Which communities are driving the most pipeline value (not just referral sessions)?
- Are there emerging communities the reconnaissance drill should evaluate?
- Should the play expand to Discord or other platforms?
- Are any communities becoming vendor-saturated to the point of diminishing returns?

Quarterly: re-run `slack-discord-reconnaissance` to discover new communities. The agent executes the discovery; the human approves portfolio changes.

## Time Estimate

- Autonomous optimization loop setup: 8 hours
- Community engagement brief setup: 4 hours
- Enhanced health scoring configuration: 4 hours
- Monthly strategic reviews (12 x 2 hours): 24 hours
- Quarterly reconnaissance re-runs (4 x 4 hours): 16 hours
- Ongoing experiment management and monitoring: 124 hours (spread over 12 months, ~2.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Syften | Real-time community keyword monitoring | [$20-$100/mo](https://syften.com/) |
| Common Room (optional) | Cross-platform community intelligence and member enrichment | [$1,000+/mo](https://www.commonroom.io/pricing/) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, brief generation | ~$20-50/mo at this usage level |
| Slack (Pro tier) | Extended history and integrations in your workspace | [$7.25/user/mo annual](https://slack.com/pricing) |
| PostHog | Analytics, experiments, anomaly detection, feature flags | Standard stack (excluded) |
| n8n | Optimization loop scheduling, health scoring, alert routing | Standard stack (excluded) |
| Attio | CRM, experiment logs, community records, brief archive | Standard stack (excluded) |

**Total play-specific cost: ~$50-200/mo** (Syften + Claude API; Common Room optional at $1,000+/mo for teams needing cross-platform member enrichment)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners
- `community-engagement-brief` — weekly intelligence brief synthesizing community performance, content strategy recommendations, warm leads, and risk flags
- `community-health-scoring` — enhanced weekly scoring with cross-community signals, competitive tracking, and lifecycle stages
