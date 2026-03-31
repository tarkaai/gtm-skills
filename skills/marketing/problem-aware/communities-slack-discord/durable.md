---
name: communities-slack-discord-durable
description: >
  Slack/Discord Community Rhythm — Durable Intelligence. Always-on AI agents
  detect metric anomalies across community portfolio, generate improvement hypotheses,
  run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Sustained >= 5 meetings/month from communities for 6 consecutive months with cost-per-meeting trending downward. Convergence: optimization pauses when 3 consecutive experiments produce <2% improvement."
kpis: ["Meetings per month (sustained >= 5)", "Cost per meeting (trending down)", "Community portfolio health (avg score >= 65)", "Experiment win rate", "Weeks since last >2% improvement"]
slug: "communities-slack-discord"
install: "npx gtm-skills add marketing/problem-aware/communities-slack-discord"
drills:
  - autonomous-optimization
  - community-health-scoring
---

# Slack/Discord Community Rhythm — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Outcomes

The community engagement channel runs autonomously. AI agents monitor the health of every community in the portfolio, detect when metrics plateau or drop, generate hypotheses for improvement, run controlled experiments, evaluate results, and auto-implement winners. Human involvement is limited to weekly brief review and approving high-risk changes. The system converges to a local maximum — the best achievable performance given current communities, audience, and competitive landscape — and maintains it as conditions shift.

## Leading Indicators

- Autonomous optimization loop running without manual intervention
- Weekly community health scores stable or improving (portfolio avg >= 65/100)
- At least 1 experiment running at all times until convergence
- Experiment results evaluated within 48 hours of completion
- Weekly optimization briefs posted to Slack
- Cost per meeting trend: flat or declining over 3-month rolling window
- Convergence detection: system auto-reduces monitoring frequency when local maximum is reached

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill to build the always-on improvement cycle for community engagement.

**Phase 1 — Monitor (daily via n8n cron):**

Build an n8n workflow triggered daily at 6am:

1. Query PostHog for the play's primary KPIs:
   - `community_referral_visit` events, last 7 days vs. 4-week rolling average
   - `community_meeting_booked` events, last 7 days vs. 4-week rolling average
   - Conversion rate: `community_referral_visit` -> `community_meeting_booked`, last 7 days vs. 4-week average
2. Query the `community-health-scoring` drill output for portfolio-level metrics:
   - Portfolio average health score vs. prior week
   - Count of communities in each classification (thriving/healthy/watch/declining/dormant)
   - Any communities with >20% score change week-over-week
3. Classify the overall play state:
   - **Normal:** All KPIs within +/-10% of 4-week average. Log to Attio. No action.
   - **Plateau:** Primary KPI (meetings/month) within +/-2% for 3+ consecutive weeks. Trigger Phase 2.
   - **Drop:** Any primary KPI declined >20% vs. 4-week average. Trigger Phase 2 with "urgent" flag.
   - **Spike:** Any primary KPI increased >50% vs. 4-week average. Trigger Phase 2 to investigate and replicate.

**Phase 2 — Diagnose (triggered by anomaly detection):**

1. Gather context from Attio: current community portfolio, channel allocation, content strategy, A/B test history, last 3 experiment results.
2. Pull 8-week metric history from PostHog broken down by community, content type, response format, and posting time.
3. Run the `hypothesis-generation` fundamental (via Claude API):
   - Input: anomaly type, metric data, current strategy configuration, experiment history
   - Output: 3 ranked hypotheses, each with: description, expected impact, risk level (low/medium/high), implementation steps, and how to measure
4. Store hypotheses in Attio as notes on the "Communities Slack/Discord" campaign record.
5. **If top hypothesis risk = "high":** Send Slack alert to human for review. STOP until approved.
6. **If risk = "low" or "medium":** Proceed to Phase 3 automatically.

**Example hypotheses the system might generate:**
- "Community X's referral volume dropped 35% this week. The community's daily message volume also dropped 40%, suggesting the community itself is becoming less active — not our engagement quality. Test: reduce engagement effort in Community X by 50% and reallocate to Community Y which is trending upward."
- "Meeting conversion rate from Slack communities is 2x higher than Discord. Test: shift 30% of Discord engagement time to additional Slack communities for 2 weeks."
- "Our Data Share content format produces 3x the referral sessions of Discussion Starters. Test: increase Data Share posts from 1/week to 3/week and reduce Discussion Starters to 1/week."
- "Response time averages 4.2 hours. Threads responded to within 1 hour convert at 2.5x the rate. Test: add a second daily triage window at 2pm to reduce average response time to 2 hours."

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis.
2. Design the experiment using PostHog feature flags (via `posthog-experiments` fundamental):
   - Create a feature flag that controls the variant behavior.
   - For community experiments, the "flag" may be a configuration change rather than code: e.g., "engage in Community X at 2x frequency" is tracked by tagging responses in Attio.
3. Set minimum duration: 7 days or 30+ data points per variant, whichever is longer.
4. Log the experiment in Attio: hypothesis, start date, expected duration, success criteria, variant description.

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog.
2. Run the `experiment-evaluation` fundamental (via Claude API):
   - Input: control data, variant data, experiment duration, sample size
   - Output: recommendation (Adopt/Iterate/Revert/Extend) with confidence level and reasoning
3. Execute the decision:
   - **Adopt:** Update the live strategy to use the winning variant. Log the change in Attio. Move to Phase 5.
   - **Iterate:** Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** Restore the prior configuration. Log the failure reason. Return to Phase 1.
   - **Extend:** Continue the experiment for another cycle if sample size is insufficient.
4. Store the full evaluation in Attio.

**Phase 5 — Report (weekly via n8n cron, every Monday at 8am):**

Generate a weekly optimization brief:

```markdown
## Community Optimization Brief — Week of {date}

### Play Health
- Meetings this month: {count} (target: >= 5)
- Cost per meeting: ${amount} (trend: {up/down/flat})
- Portfolio health: {avg_score}/100 across {count} active communities

### This Week's Activity
- Anomalies detected: {count} ({types})
- Hypotheses generated: {count}
- Experiments active: {count}
- Experiments completed: {count}
- Decisions made: {Adopt: N, Iterate: N, Revert: N}

### Changes Implemented
{List each adopted change with its measured impact}

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Status: {Active Optimization / Approaching Convergence / Converged}
- {If converged: "Play has reached local maximum. Further gains require strategic changes."}

### Next Week Focus
{What the system plans to test next, or why it's monitoring only}
```

Post to Slack and store in Attio.

### 2. Maintain community health scoring

Continue running the `community-health-scoring` drill from Scalable level. The weekly scores feed directly into the autonomous optimization loop:

- Communities classified as "declining" are flagged as anomalies in Phase 1.
- The hypothesis generator in Phase 2 uses community health data to propose portfolio reallocation.
- New communities discovered in quarterly reconnaissance refreshes enter the portfolio as "watch" status.

At Durable level, add one enhancement to health scoring:
- **Member enrichment tracking:** For communities where you use Common Room or similar tools, track what percentage of engaged members match your ICP. If ICP density drops below 30%, flag the community for review.

### 3. Handle convergence

The optimization loop detects convergence when 3 consecutive experiments produce <2% improvement in the primary KPI (meetings/month). At convergence:

1. The play has reached its local maximum for community engagement.
2. Reduce the monitoring frequency from daily to weekly.
3. Reduce the optimization brief from weekly to monthly.
4. Continue community health scoring weekly to detect market shifts (new communities emerging, existing ones declining).
5. Post a convergence report:
   - "Community engagement play has converged. Current performance: {X} meetings/month at ${Y} cost per meeting across {Z} communities. Further gains require strategic changes: entering new communities, launching your own community, or changing the product offering."
6. If a significant external change is detected (e.g., a major community shuts down, a new community with 5000+ ICP members launches), exit convergence and restart the optimization loop.

### 4. Guardrails

Per the `autonomous-optimization` drill guardrails:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold:** If meetings/month drops >30% during any experiment, auto-revert immediately.
- **Human approval required for:**
  - Dropping a community that has produced >20% of total meetings
  - Increasing paid community membership spend by >$100/mo
  - Any hypothesis flagged as "high risk"
  - Changes to the core engagement guidelines (response format, self-promotion rules)
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.

## Time Estimate

- 8 hours: Initial setup of autonomous optimization loop (n8n workflows, PostHog experiments integration, Attio logging)
- 4 hours/month: Weekly brief review and human approval of high-risk changes (15 min/week)
- 2 hours/month: Quarterly community portfolio refresh (reconnaissance re-run)
- 4 hours/month: Content creation for original posts (agent drafts, human reviews)
- ~80 hours total over 6 months, declining as system converges

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Optimization loop orchestration, monitoring workflows, health scoring | Cloud Pro: EUR 60/mo (https://n8n.io/pricing) |
| PostHog | KPI tracking, anomaly detection, experiment feature flags | Free up to 1M events/mo; paid starts at $0.00005/event (https://posthog.com/pricing) |
| Attio | Campaign records, experiment logs, community portfolio management | Free for small teams (https://attio.com/pricing) |
| Common Room | Unified community intelligence, member enrichment | Starter: $1,000/mo (https://www.commonroom.io/pricing) |
| Anthropic API (Claude) | Hypothesis generation and experiment evaluation | ~$0.01-0.05 per optimization cycle (https://www.anthropic.com/pricing) |
| Syften (alternative to Common Room) | Real-time keyword monitoring | Standard: $39.95/mo (https://syften.com) |
| Paid community memberships | Access to gated communities | $50-200/mo total |

**Play-specific cost at Durable level:** $150-300/mo (n8n Cloud + Syften + memberships + API costs). With Common Room: $1,150-1,300/mo. Anthropic API costs are minimal (~$5-15/mo for weekly optimization cycles).

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners
- `community-health-scoring` — weekly scoring and ranking of all active communities, feeding anomaly data into the optimization loop
