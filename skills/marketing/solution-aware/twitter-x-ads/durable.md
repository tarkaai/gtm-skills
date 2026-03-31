---
name: twitter-x-ads-durable
description: >
  Twitter/X Ads — Durable Intelligence. AI agent autonomously optimizes X Ads campaigns
  via the detect-diagnose-experiment-evaluate loop. Finds the local maximum of
  creative, audience, and budget performance and maintains it as market conditions change.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained >=60 qualified leads/month over 12 months with CPL trending flat or down via AI-optimized creative and targeting"
kpis: ["Monthly qualified leads", "CPL trend (3-month rolling)", "AI experiment win rate", "Creative fatigue detection speed", "Audience refresh rate", "Convergence distance"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - autonomous-optimization
  - twitter-x-ads-performance-monitor
  - dashboard-builder
---

# Twitter/X Ads — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Outcomes

Deploy the autonomous optimization loop on X Ads. The AI agent continuously monitors campaign performance, detects anomalies, generates hypotheses for improvement, runs controlled experiments, evaluates results, and auto-implements winners. The goal is to find the local maximum — the best possible X Ads performance given current market conditions — and maintain it as conditions change. Target: sustained >=60 qualified leads/month with CPL trending flat or down over 12 months.

## Leading Indicators

- Autonomous optimization loop running uninterrupted for 4+ consecutive weeks
- At least 1 experiment launched per month (agent is actively looking for improvements)
- Experiment win rate >=30% (at least 1 in 3 experiments produces a measurable improvement)
- CPL has not increased >10% quarter-over-quarter
- Agent detects and responds to anomalies within 24 hours (not waiting for human intervention)
- Weekly optimization brief delivered on schedule every Monday

## Instructions

### 1. Build the paid media intelligence dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for Durable-level monitoring:

**Performance layer:**
- ROAS by campaign and ad group (weekly trend, 12-week window)
- CPA trend over time with target line overlay
- Lead quality score by source (X keyword vs. follower-lookalike vs. retargeting)
- Budget utilization: daily spend vs. daily budget
- Creative performance decay curves (CTR over time per variant)

**Optimization layer:**
- Active experiments: current hypothesis, variant vs. control metrics, days remaining
- Experiment history: all past experiments with outcomes (adopted, reverted, extended)
- Convergence tracker: rolling 3-experiment improvement rate. When <2% improvement for 3 consecutive experiments, the play has reached its local maximum.

**Health layer:**
- Audience freshness: days since last audience refresh per ad group
- Creative freshness: age of oldest active variant
- Budget efficiency: CPL vs. target with trend arrow

### 2. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for X Ads:

**Phase 1 — Monitor (daily):**
The n8n cron workflow pulls X Ads stats and PostHog conversion data. Compares last 2 weeks against 4-week rolling average. Classifies each metric as normal, plateau, drop, or spike.

- **Normal**: Log. No action.
- **Plateau**: CPL or conversion rate has not changed >=2% for 3+ weeks. Trigger Phase 2 to find improvement.
- **Drop**: CPL increased >20% or qualified leads decreased >20%. Trigger Phase 2 urgently.
- **Spike**: Positive anomaly. Log the conditions that caused it for replication.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current audience configuration, active creative variants, recent budget changes, competitive landscape signals. It passes this to Claude for hypothesis generation:

```
The X Ads campaign for {play} detected a {anomaly_type} in {metric}.
Current state: {metrics snapshot}
Trend: {14-day daily metrics}
Active creative: {list with individual CTR}
Active audiences: {ad groups with performance}
Recent changes: {budget or targeting changes in last 14 days}

Generate 3 ranked hypotheses for improvement. Each must be:
1. A specific, executable change (e.g., "replace the 3 oldest creative variants with data-hook variants targeting {keyword theme}")
2. Expected impact (e.g., "+15% CTR, -10% CPL")
3. Risk level (low = affects <20% of budget, medium = 20-50%, high = >50%)
```

If top hypothesis is high-risk: send to Slack for human approval. Stop.
If low or medium risk: proceed to Phase 3.

**Phase 3 — Experiment:**
Design a controlled test:
- Use PostHog feature flags to split traffic between control (current configuration) and variant (hypothesis change)
- Run for minimum 7 days or 100 conversions per variant
- Log experiment start in Attio: hypothesis, start date, expected duration, success metric

Types of experiments the agent can run:
- **Creative experiments**: Test new ad copy angles, formats, or CTAs
- **Audience experiments**: Test new keyword themes, handles, or interest categories
- **Bid experiments**: Test bid adjustments on specific ad groups
- **Landing page experiments**: Test CTA copy or form layout changes (via PostHog feature flags)

**Phase 4 — Evaluate:**
Pull experiment results. Determine:
- **Adopt**: Variant outperformed control by >=5% with statistical significance. Implement change. Update campaign configuration.
- **Iterate**: Results inconclusive or marginal. Generate a refined hypothesis building on this data. Return to Phase 2.
- **Revert**: Variant underperformed. Restore control. Log the failure. Wait 7-day cooldown before testing the same variable again.

**Phase 5 — Report (weekly):**
Every Monday, generate a weekly optimization brief:
- Anomalies detected this week
- Experiments run and their outcomes
- Net metric change from adopted experiments
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 3. Configure always-on monitoring

Run the `twitter-x-ads-performance-monitor` drill at Durable intensity:
- Daily cron monitoring continues from Scalable level
- Creative fatigue detection auto-triggers new variant production
- Audience exhaustion detection auto-triggers new audience research
- Budget guardrails prevent overspend even when the optimization loop changes bids

### 4. Define convergence criteria

The optimization loop runs indefinitely, but it should detect when it has found the local maximum:
- Track the improvement rate of the last 3 adopted experiments
- If all 3 produced <2% improvement: the play has converged
- At convergence: reduce monitoring from daily to weekly, report to team that further gains require strategic changes (new platform, new audience segment, or product changes) rather than tactical optimization
- Log convergence in Attio with the final optimized metrics

### 5. Evaluate sustainability

Measure monthly:
- **Qualified leads >= 60/month**: Is the campaign sustaining output?
- **CPL trend**: Is CPL flat or declining over the 3-month rolling average?
- **Experiment win rate >= 30%**: Is the optimization loop still finding improvements?

If metrics sustain over 12 months, the play is durable.
If metrics decay despite optimization, investigate: market saturation, competitive pressure, or audience exhaustion. The agent should detect these patterns and recommend strategic pivots.

## Time Estimate

- 20 hours: Initial Durable setup (dashboard, optimization loop, guardrails)
- 5 hours/month: Review weekly briefs, approve high-risk experiments
- 5 hours/month: Strategic review and direction adjustments
- 3 hours/month: Automation maintenance

**Total: ~180 hours over 12 months (20 setup + ~13/month ongoing)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| X Ads | Promoted tweets, agent-optimized | $5,000-20,000/mo ad spend (varies by optimization) |
| PostHog | Full-funnel analytics, feature flags, experiments | Free tier or ~$50-100/mo at Durable volume |
| n8n | Optimization loop workflows, monitoring, data sync | Free self-hosted or $20/mo cloud |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly briefs | ~$30-60/mo |
| Attio | Campaign records, experiment logs, lead attribution | Standard stack |

## Drills Referenced

- `autonomous-optimization` — The core Durable loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `twitter-x-ads-performance-monitor` — Daily monitoring for creative fatigue, audience exhaustion, budget guardrails, and performance alerts
- `dashboard-builder` — Creates the PostHog intelligence dashboard with performance, optimization, and health layers
