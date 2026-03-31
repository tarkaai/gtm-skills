---
name: discord-community-building-durable
description: >
  Discord Community Building — Durable Intelligence. Always-on AI agents
  that monitor community metrics, detect anomalies, generate improvement
  hypotheses, run A/B experiments, and auto-implement winners. The autonomous
  optimization loop finds the local maximum for member growth, engagement,
  and lead output, then maintains it as conditions change. Weekly optimization
  briefs report what changed and why. Converges when successive experiments
  produce less than 2% improvement.
stage: "Marketing > ProductAware"
motion: "CommunitiesForums"
channels: "Communities, Product"
level: "Durable Intelligence"
time: "20 hours over 6 months (agent runs autonomously; human reviews weekly briefs)"
outcome: "Sustained ≥ 100 DAU and ≥ 30 qualified leads/month for 6 consecutive months with cost per lead trending down quarter over quarter"
kpis: ["DAU sustained ≥ 100 for 6 months (no month below 90)", "Qualified leads/month sustained ≥ 30 for 6 months", "Cost per qualified lead trend (target: declining QoQ)", "Experiment win rate (target ≥ 30% of experiments produce measurable improvement)", "Member-to-member help ratio (target ≥ 60% of help threads resolved by peers)", "Convergence detection (successive experiments <2% improvement for 3 consecutive tests)"]
slug: "discord-community-building"
install: "npx gtm-skills add marketing/product-aware/discord-community-building"
drills:
  - autonomous-optimization
  - community-health-scoring
---

# Discord Community Building — Durable Intelligence

> **Stage:** Marketing > ProductAware | **Motion:** CommunitiesForums | **Channels:** Communities, Product

## Outcomes

The Discord community runs as a self-sustaining, self-optimizing system. AI agents continuously monitor every metric, detect when something changes, hypothesize why, test a fix, and implement winners -- all without human intervention for low-risk changes. The human role shifts from community manager to strategic reviewer: reading weekly optimization briefs and approving high-risk experiments. The play reaches its local maximum when 3 consecutive experiments produce less than 2% improvement, at which point the agent reduces monitoring frequency and reports that tactical optimization is exhausted.

Pass: ≥ 100 DAU and ≥ 30 qualified leads/month sustained for 6 consecutive months, with cost per qualified lead declining quarter over quarter.
Fail: Any 2 consecutive months with DAU below 90 or qualified leads below 25, or cost per lead increasing for 2 consecutive quarters.

## Leading Indicators

- The autonomous optimization loop detects its first anomaly and generates hypotheses within the first 2 weeks of activation (monitoring is calibrated correctly)
- The first experiment produces a statistically significant result (positive or negative) within 3 weeks (experiment design and sample sizes are appropriate for this community's traffic)
- At least 1 experiment winner is auto-implemented in the first month (the evaluate-and-implement pipeline works end to end)
- Weekly optimization briefs are generated on schedule and contain actionable insights (the reporting pipeline is reliable)
- Member-to-member help ratio increases over time without team intervention (the recognition program and community culture are self-reinforcing)

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the Discord community play. This is the core system that makes Durable fundamentally different from Scalable.

**Phase 1 — Monitor (daily via n8n cron):**

Configure the monitoring phase to watch these Discord-specific metrics:

| Metric | Source | Anomaly threshold |
|--------|--------|-------------------|
| DAU | Discord API — unique message authors per day | Drop >20% vs 4-week avg |
| New members/week | Discord API — members with `joined_at` in last 7 days | Drop >25% vs 4-week avg |
| Churn rate | Discord API — member list diff week over week | Increase >30% vs 4-week avg |
| Referral sessions | PostHog — `discord_referral_visit` events per week | Drop >20% vs 4-week avg |
| Qualified leads/month | Attio — contacts with `lead_source=discord-community` + conversion | Drop >15% vs trailing 3-month avg |
| Bot resolution rate | PostHog — `bot_reply_confirmed_helpful` / total #help threads | Drop >10 percentage points vs 4-week avg |
| Content engagement rate | Discord API — threads with 3+ replies / total posts per week | Drop >15% vs 4-week avg |

Use the `posthog-anomaly-detection` fundamental for PostHog metrics and n8n scheduled queries against the Discord API for server-level metrics. When any metric crosses its anomaly threshold, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

The agent gathers context and generates hypotheses using the `hypothesis-generation` fundamental:

1. Pull 8 weeks of the anomalous metric from PostHog via `posthog-dashboards`
2. Pull the latest `community-health-scoring` report for channel-level data
3. Pull the latest `autonomous-optimization` report for member cohort data
4. Generate 3 ranked hypotheses. Discord-specific hypothesis templates:

   - **DAU drop:** "Power users decreased from X to Y this week. Hypothesis: the #office-hours thread was not posted last week, breaking the weekly engagement habit. Test: reinstate and measure DAU recovery over 2 weeks."
   - **Referral drop:** "Channel health score for #resources dropped from 72 to 48. Hypothesis: resource posts shifted from actionable tutorials to generic link shares. Test: post 3 detailed tutorials with UTM links over 2 weeks and compare referral sessions."
   - **Lead drop:** "Conversion rate from Discord referrals dropped 30%. Hypothesis: the pinned CTA in #general has been stale for 6 weeks. Test: rotate the CTA to a current offer and measure conversion rate."
   - **Bot resolution drop:** "Bot resolution rate dropped from 30% to 18%. Hypothesis: 3 new feature questions are appearing that are not in the knowledge base. Test: add documentation for the new features and measure resolution rate recovery."
   - **Churn spike:** "Member churn increased 40% this week. Hypothesis: a recent product change caused confusion. Test: post a detailed explainer in #announcements and create a dedicated #help thread for migration questions."

5. Store hypotheses in Attio. If the top hypothesis has risk = "high" (affects >50% of members or requires budget change >20%), send a Slack alert for human approval and pause. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

Design and run the experiment:

1. Use `posthog-experiments` to create a feature flag for the test (where applicable)
2. Implement the variant using the appropriate fundamental:
   - Content changes: `discord-api-write` to post new content types
   - Bot changes: Update the bot's knowledge base or response thresholds
   - Channel changes: Create/archive channels via Discord API
   - CTA changes: Update pinned messages via `discord-api-write`
3. Set minimum duration: 14 days or 200+ data points per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success metric, success threshold

**Phase 4 — Evaluate (triggered by experiment completion):**

Pull experiment results and run the `experiment-evaluation` fundamental:

- **Adopt:** Improvement is statistically significant (p < 0.05) and > 5% lift. Implement permanently. Log the change.
- **Iterate:** Result is directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Result is negative or flat. Disable the variant. Log the failure with learnings. Return to Phase 1.
- **Extend:** Insufficient data. Continue the experiment for another period.

**Guardrails (from the autonomous-optimization drill, applied to Discord):**
- Maximum 1 active experiment at a time in the Discord community
- If DAU drops >30% during any experiment, auto-revert immediately
- Human approval required for: new channel creation/deletion, bot behavior changes affecting all members, role structure changes
- Cooldown: 7 days after a failed experiment before testing the same variable again
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.

### 2. Run weekly community program reporting

Run the `autonomous-optimization` drill on a weekly automated cadence. This drill produces:

- **Growth metrics:** Member count, new joins, churn, net growth, growth trend
- **Engagement cohort analysis:** Power users, regular contributors, occasional participants, lurkers, churned — with week-over-week shifts between tiers
- **Channel-level ROI:** Each channel scored by engagement, referral value, and team effort required
- **Lead attribution:** Referral sessions, signups, qualified leads, pipeline value attributed to Discord
- **Anomaly flags:** Any metrics that deviated >20% from rolling average

The report is posted to Slack weekly and stored as structured data in Attio. The autonomous optimization loop uses this data as input for its monitoring and diagnosis phases.

### 3. Maintain and evolve community health scoring

Run the `community-health-scoring` drill weekly, adapted for Discord channel dynamics:

- Score every channel weekly using the formula from Scalable level
- When a channel scores "declining" for 3 consecutive weeks, the agent generates an intervention hypothesis: change content type, change posting frequency, merge with another channel, or archive
- When a channel scores "thriving" for 4 consecutive weeks, the agent recommends: increase posting frequency, create a sub-channel for a popular topic, or feature the channel's best content in #announcements
- Track score trends over time. A healthy community has 3+ channels in "thriving" or "healthy" at all times.

### 4. Evolve the bot and member programs

The autonomous optimization loop should include bot and program improvements in its experiment pipeline:

**Bot evolution:**
- Monthly: Analyze questions the bot could not answer. Update the knowledge base.
- Quarterly: Review bot tone and helpfulness ratings. Run an A/B test on response style (concise vs detailed, formal vs casual).
- Track: Resolution rate trend. If it plateaus, the bot has reached its knowledge ceiling — expand the knowledge base or improve retrieval.

**Member program evolution:**
- Monthly: Review Power User and Ambassador criteria. Are the right people being recognized? Adjust thresholds if the program is too exclusive (nobody qualifies) or too easy (everyone qualifies).
- Quarterly: Survey Power Users and Ambassadors on program value. Adjust perks based on feedback.
- Track: Power User retention rate. If Power Users are churning, the program is not providing enough value.

### 5. Generate weekly optimization briefs

**Phase 5 of the autonomous-optimization loop (runs weekly via n8n):**

Aggregate all optimization activity and generate a brief using Claude:

```markdown
## Discord Community Optimization Brief — Week of {date}

### What happened
- Anomalies detected: {count and description}
- Hypotheses generated: {count}
- Experiments running: {description, current status}
- Experiments completed: {description, result, decision}

### Net impact this week
- DAU: {current} ({+/- change} from experiment adoptions)
- Qualified leads: {current month-to-date} (on track for {projected monthly})
- Cost per lead: ${amount} ({trend} vs last month)
- Experiment record: {wins}/{total} ({win_rate}%)

### Distance from local maximum
{Assessment of how much room remains for tactical optimization. Based on recent experiment magnitude. If last 3 experiments all produced <2% improvement, flag convergence.}

### Recommendations for next week
- {Next experiment to run, if any}
- {Any metrics that need human attention}
- {Strategic changes that are beyond tactical optimization scope}
```

Post to Slack. Store in Attio.

### 6. Detect convergence and transition to maintenance

The optimization loop should detect convergence — the point where tactical optimization is exhausted:

**Convergence criteria:** 3 consecutive experiments produce less than 2% improvement on any metric.

When convergence is detected:
1. Report: "The Discord community has reached its local maximum. Current performance: [DAU], [leads/month], [cost per lead]. Further gains require strategic changes (new acquisition channels, product changes that drive community value, or expansion to new audience segments) rather than tactical optimization."
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment frequency from monthly to quarterly
4. Continue weekly reporting to detect regression
5. If any metric drops >15% from the converged baseline, re-activate daily monitoring and the full optimization loop

### 7. Evaluate sustainability at 6 months

This level runs continuously. At the 6-month mark, conduct a comprehensive review:

- **DAU trend:** Plot monthly averages. All 6 months must be ≥ 90 (with target ≥ 100). A sustained flat or upward trend is success. A declining trend even if above threshold is a warning.
- **Lead output:** Plot monthly qualified leads. All 6 months must be ≥ 25 (with target ≥ 30). Confirm attribution methodology has been consistent.
- **Cost efficiency:** Calculate cost per qualified lead for each quarter. Q2 cost per lead should be lower than Q1.
- **Experiment log:** Review all experiments run. What was the cumulative impact? What was the win rate? Has convergence been detected?
- **Community self-sufficiency:** What percentage of #help threads are resolved by peers without team intervention? Target ≥ 60%. This measures whether the community generates value independently.

## Time Estimate

- Autonomous optimization loop setup: 6 hours (one-time)
- Weekly brief review: 30 min/week x 26 weeks = 13 hours
- Human approval for high-risk experiments: ~4 hours total (estimated 4-6 high-risk experiments over 6 months)
- Quarterly strategic reviews: 2 hours x 2 = 4 hours
- Bot knowledge base updates: 3 hours total over 6 months
- Total: ~20 hours of human time over 6 months (agent handles the rest autonomously)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Discord | Community hosting | Free ([discord.com](https://discord.com)) |
| PostHog | Anomaly detection, experiments, dashboards, funnels | Growth plan for experiments: free up to 1M events, then usage-based ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop orchestration, monitoring crons, reporting workflows | Pro $60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Experiment log, lead attribution, community records, hypothesis storage | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs, bot responses | Usage-based ~$3/1M input tokens; expect $20-40/mo at Durable volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Durable:** $80-130/mo (n8n Pro, Anthropic API, existing stack tools). This does not include team time — at Durable, human time should be under 4 hours/month.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop that monitors metrics, detects anomalies, generates hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. This is what makes Durable fundamentally different from Scalable.
- `community-health-scoring` — weekly channel-level scoring that feeds the optimization loop with granular data on where engagement is thriving or declining
- `autonomous-optimization` — weekly community health report with member cohort analysis, channel ROI, and lead attribution data that provides the historical dataset for trend analysis and anomaly detection
