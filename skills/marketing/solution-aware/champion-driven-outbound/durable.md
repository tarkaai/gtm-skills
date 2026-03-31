---
name: champion-driven-outbound-durable
description: >
  Champion-driven Outbound — Durable Intelligence. Always-on AI agents autonomously optimize
  every stage of the champion funnel: detect metric anomalies, generate improvement hypotheses,
  run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained champion conversion (≥3%) over 12 months via AI-powered champion identification and enablement"
kpis: ["Sustained conversion rate", "Experiment win rate", "Champion pipeline velocity trend", "Cost efficiency trend", "Champion yield per account"]
slug: "champion-driven-outbound"
install: "npx gtm-skills add marketing/solution-aware/champion-driven-outbound"
drills:
  - autonomous-optimization
  - champion-outbound-reporting
---
# Champion-driven Outbound — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Overview
Always-on AI agents find and maintain the local maximum for this play. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in the champion funnel, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. The `champion-outbound-reporting` drill provides the play-specific monitoring layer. Weekly optimization briefs. The play converges when successive experiments produce <2% improvement.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained champion conversion (≥3%) over 12 months via AI-powered champion identification and enablement

---

## Budget

**Play-specific tools & costs**
- **Instantly:** scaled email sequences — $77/mo (Hypergrowth, https://instantly.ai/pricing)
- **Clay:** continuous enrichment and signal refresh — $349/mo (Team, https://clay.com/pricing)
- **LinkedIn Sales Navigator:** champion search — $99/mo (Core)
- **Loops:** enablement sequences — $49/mo (Starter, https://loops.so/pricing)
- **Loom:** personalized video — $12.50/user/mo (Business, https://loom.com/pricing)
- **Anthropic API:** hypothesis generation, experiment evaluation, report generation — ~$50-150/mo depending on volume

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

**Estimated monthly cost:** ~$640-740/mo

---

## Instructions

### 1. Deploy autonomous optimization loop
Run the `autonomous-optimization` drill, configured for the champion-driven-outbound play. The drill creates an always-on n8n workflow with these phases:

**Phase 1 — Monitor (daily cron):**
The agent checks the play's primary KPIs via `posthog-anomaly-detection`:
- Champion recruitment reply rate (target: ≥10%)
- Enablement kit forward rate (target: ≥15%)
- Account-to-meeting conversion rate (target: ≥3%)
- Champion pipeline velocity (target: ≤21 days profiling-to-meeting)
- Cost per champion-facilitated meeting (target: declining or stable)

Compare the last 2 weeks against the 4-week rolling average. Classify each metric as normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), or spike (>50% increase).

If all normal: log to Attio, no action.
If anomaly detected: trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio and PostHog:
- Current champion funnel configuration (signal criteria, scoring weights, recruitment copy, enablement kit content, cadence timing)
- 8-week metric history
- Recent A/B test results from Scalable level
- Champion health distribution

Feed this context to Claude via `hypothesis-generation`. Receive 3 ranked hypotheses. Examples of champion-specific hypotheses the agent might generate:
- "Recruitment reply rate dropped because the top-performing signal type (job changes) has been saturated — test funding announcement signals instead"
- "Enablement kit forward rate declined because the business case template uses outdated ROI numbers — regenerate with fresh case study data"
- "Pipeline velocity increased because the breakup email is landing before champions have time to pitch internally — extend the sequence from 14 to 21 days"

Store hypotheses in Attio. If risk = high (e.g., changing the ICP or disabling a channel), alert for human review and STOP. If risk = low/medium, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent designs and launches the experiment:
1. Create a PostHog feature flag via `posthog-experiments` that splits new champion candidates between control and variant
2. Implement the variant using the appropriate tool (e.g., new Instantly campaign variant, updated Clay scoring weights, refreshed enablement kit via Loops)
3. Set duration: minimum 7 days or 100+ candidates per variant, whichever is longer
4. Log the experiment in Attio with hypothesis, start date, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog and runs `experiment-evaluation`:
- **Adopt:** implement the winner as the new default. Update Instantly campaigns, Clay scoring, or Loops sequences accordingly. Log the change.
- **Iterate:** if results are promising but inconclusive, generate a refined hypothesis and return to Phase 2.
- **Revert:** disable the variant, restore control. Log the failure. Return to Phase 1.
- **Extend:** keep running if sample size is insufficient. Set a reminder.

**Phase 5 — Report (weekly cron):**
Generate the weekly optimization brief using Claude:
- Anomalies detected this week
- Hypotheses generated and their risk levels
- Experiments running, completed, or reverted
- Net impact on champion funnel metrics
- Estimated distance from local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Deploy champion-specific monitoring
Run the `champion-outbound-reporting` drill. This builds the monitoring layer unique to this play:

**Champion Funnel Dashboard (PostHog):**
- Full funnel from accounts targeted through deals created
- Champion yield by account segment (size, industry, signal type)
- Champion engagement health distribution
- Time-to-meeting by champion source and recruitment track
- Pipeline value from champion pathway vs non-champion outbound

**Anomaly Detection (6 champion-specific metrics):**
- Champion profiling → contacted rate
- Recruitment reply rate
- Enablement kit forward rate
- Champion-facilitated meetings/week
- Average champion score
- Champion-sourced pipeline value/month

Alerts route via n8n: medium severity to Slack channel, high severity to founder DM.

**Weekly Champion Pipeline Report (Monday 7:00 AM):**
Automated report covering: funnel metrics, week-over-week changes, top-performing accounts, at-risk champions requiring action. Posted to Slack and stored in Attio.

**Monthly Cohort Analysis:**
Track whether recent champion cohorts perform better or worse than historical ones. Flag if the recruitment cycle is lengthening (market saturation signal). Compare champion vs non-champion deals on close rate, deal size, and sales cycle.

### 3. Configure Durable-level guardrails
In addition to the `autonomous-optimization` drill's built-in guardrails (max 1 experiment at a time, auto-revert on >30% metric drop, human approval for high-risk changes, 7-day cooldown after failures, max 4 experiments/month):

**Champion-specific guardrails:**
- If champion-sourced pipeline drops below non-champion outbound pipeline for 4+ consecutive weeks, escalate: the champion strategy may have lost its advantage. Requires human strategic review.
- If champion recruitment rate drops below 3% for 8+ weeks despite optimization, investigate whether the market is saturated for the current ICP segment. Recommend ICP expansion or new signal types.
- If the average time-to-meeting exceeds 45 days for 3+ consecutive monthly cohorts, the enablement process is too slow. Run a focused experiment on accelerating the internal selling cycle.
- Never run optimization experiments on the champion health monitoring thresholds — those are safety mechanisms, not performance levers.

### 4. Detect convergence and maintain
The `autonomous-optimization` drill detects convergence when 3 consecutive experiments produce <2% improvement on the target metric. At convergence:

1. The play has found its local maximum for the current ICP, channels, and market conditions
2. Reduce the monitoring cron from daily to weekly
3. Reduce experiment frequency from up to 4/month to 1/month (maintenance experiments)
4. Generate a convergence report: "Champion-driven outbound has reached its local maximum. Current performance: {metrics}. Further gains require strategic changes (new ICP segments, new channels, product positioning changes) rather than tactical optimization."
5. Continue weekly champion pipeline reports and monthly cohort analyses to detect market shifts that break convergence

If metrics begin declining after convergence (detected by the weekly monitoring), automatically re-enter the daily optimization loop.

---

## KPIs to track
- Sustained conversion rate (≥3% over 12 months)
- Experiment win rate (adopted / total experiments)
- Champion pipeline velocity trend (days profiling-to-meeting, should be stable or declining)
- Cost efficiency trend (cost per champion-facilitated meeting, should be declining)
- Champion yield per account (meetings facilitated per active champion)

---

## Pass threshold
**Sustained champion conversion (≥3%) over 12 months via AI-powered champion identification and enablement**

This level runs continuously. Review monthly: what the optimization loop changed, which experiments won or lost, and whether the play is converging toward its local maximum.

---

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Scaled recruitment email sequences | Hypergrowth: $77/mo (https://instantly.ai/pricing) |
| Clay | Continuous enrichment and signal monitoring | Team: $349/mo (https://clay.com/pricing) |
| LinkedIn Sales Nav | Champion candidate search | Core: $99/mo (https://linkedin.com/sales-solutions) |
| Loops | Automated enablement kit delivery | Starter: $49/mo (https://loops.so/pricing) |
| Loom | Personalized recruitment videos | Business: $12.50/user/mo (https://loom.com/pricing) |
| Anthropic API | Hypothesis generation, evaluation, reporting | ~$50-150/mo (https://anthropic.com/pricing) |

**Estimated monthly cost:** ~$640-740/mo

---

## Drills Referenced
- `autonomous-optimization` — the core Durable loop: monitor metrics → diagnose anomalies → generate hypotheses → run experiments → evaluate and implement winners → weekly briefs
- `champion-outbound-reporting` — champion-specific funnel dashboards, anomaly detection, weekly pipeline reports, and monthly cohort analysis

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/champion-driven-outbound`_
