---
name: timing-qualification-durable
description: >
  Timing Qualification Process — Durable Intelligence. Always-on AI agents autonomously optimize
  the timeline scoring model, urgency detection accuracy, and forecast precision. The
  autonomous-optimization drill runs the core loop: detect metric anomalies, generate improvement
  hypotheses, run A/B experiments, evaluate results, auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement in forecast accuracy.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving forecast accuracy (within 14 days of predicted close) over 6 months with autonomous optimization finding the local maximum of timeline prediction precision"
kpis: ["Forecast accuracy (days variance between predicted and actual close)", "Autonomous experiment win rate", "Slippage detection rate", "Auto-score prediction accuracy trend", "Urgency detection accuracy", "Cost per timeline-qualified lead trend"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
drills:
  - autonomous-optimization
  - signal-detection
---

# Timing Qualification Process — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

The timing qualification system runs autonomously, continuously improving itself. An AI agent monitors forecast accuracy, detects when prediction quality degrades, generates hypotheses for improvement, runs experiments, and auto-implements winners. The system finds and maintains the local maximum of timeline prediction precision — the best possible forecast accuracy given your market, ICP, and competitive landscape.

Human involvement is limited to: conducting discovery calls with high-priority prospects, reviewing weekly optimization briefs, and approving high-risk changes flagged by the agent.

## Leading Indicators

- Autonomous optimization loop is running: anomalies detected, hypotheses generated, experiments launched without human initiation
- Weekly optimization briefs are being delivered on schedule with actionable content
- Forecast accuracy is stable or improving month-over-month (variance trending toward <=14 days)
- Auto-score prediction accuracy is improving as the model self-calibrates
- Slippage detection catches timeline shifts within 48 hours and auto-adjusts cadences
- Experiments are producing diminishing returns (approaching the local maximum)
- Cost per timeline-qualified lead is stable at or near its minimum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the timing qualification play. This is the core drill that makes Durable fundamentally different from Scalable. Configure the five phases:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check timing qualification KPIs daily
- Compare last 2 weeks against 4-week rolling average for:
  - Forecast accuracy (average days variance between predicted and actual close date)
  - Auto-score prediction accuracy (% of auto-predicted categories matching human-validated categories)
  - Slippage rate (% of deals where timeline_category shifts to a later bucket)
  - Timeline qualification rate (% of deals scored within 48 hours)
  - Urgency signal hit rate (% of enrichment signals that proved accurate post-call)
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current scoring signal weights, enrichment provider coverage, urgency driver distribution, recent experiment results
- Pull 8-week metric history from PostHog
- Run Claude `hypothesis-generation` with the anomaly data
- Receive 3 ranked hypotheses. Examples of timing-specific hypotheses:
  - "Recent funding signal weight is too high — funded companies in our ICP are taking longer than predicted because they are evaluating multiple vendors simultaneously"
  - "Job posting signal has decayed — companies posting roles 6 months ago have already hired and moved past the buying window"
  - "Fiscal year end as an urgency driver is over-indexed — only 30% of 'budget expiration' categorized deals actually close before fiscal year end"
  - "Consequence of inaction is the strongest forecast predictor — deals where the prospect articulated specific consequences close 2x faster. Weight this signal higher in auto-scoring."
  - "Slippage is concentrated in deals with timeline_confidence <= 3 — add a mandatory validation step for low-confidence deals before categorizing as Immediate"
- Store hypotheses in Attio. If top hypothesis is high-risk, alert founder for review.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design experiment using PostHog feature flags
- For scoring changes: split new leads into control (current model) and variant (hypothesis change). Both get auto-scored, but only control model routes deals. After experiment, compare which model better predicted actual outcomes.
- For signal weighting changes: A/B test enrichment signal weights via Clay formula variants
- For cadence changes: split leads by category and test different follow-up frequencies
- Minimum experiment duration: 7 days or 50+ samples per variant

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live scoring model, signal weights, or cadence rules. Log the change in Attio.
- If Revert: restore previous configuration. Log the failure with root cause.
- If Iterate: generate a refined hypothesis building on the result.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity for the week
- Generate a weekly timing qualification optimization brief:
  - Anomalies detected and their root causes
  - Experiments running and current status
  - Experiments completed with results (adopted, reverted, or extended)
  - Net change in forecast accuracy this week
  - Current distance from estimated local maximum
  - Urgency signal effectiveness ranking (which signals best predict actual close timing)
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy signal-based timeline intelligence

Run the `signal-detection` drill to configure always-on monitoring for timing-relevant buying signals:

- **Budget window signals:** Clay monitors for funding rounds, earnings reports showing increased spend, budget-relevant job postings at target accounts
- **Leadership change signals:** New CxO or VP hires that often trigger vendor evaluation cycles
- **Competitive pressure signals:** Competitor adoption at peer companies, competitor pricing changes, negative competitor reviews
- **Deadline signals:** Regulatory filing dates, contract renewal windows (estimated from adoption dates), industry event calendars
- **Pain escalation signals:** Negative employee reviews mentioning the problem you solve, support ticket volume increases (if public), social media complaints

When a signal fires, automatically:
1. Check if the account is already in the pipeline
2. If yes: re-score the deal's timeline and alert the founder if the category shifts to Immediate
3. If no: create a new deal in Attio, run through auto-scoring, and route based on predicted urgency
4. Log `timing_signal_detected` event in PostHog with signal type and resulting action

### 3. Build durable timing intelligence reporting

Run the `autonomous-optimization` drill with Durable-level additions:

- **Scoring model drift dashboard:** Track how the auto-scoring model's prediction accuracy changes over time. If the model that was 70% accurate in month 1 drops to 55% in month 3, the autonomous optimization loop should have detected and addressed this. If it hasn't, flag for strategic review.
- **Experiment performance tracking:** Cumulative impact of all experiments. How much has forecast accuracy improved since Scalable level?
- **Signal decay analysis:** Which enrichment signals lose predictive value fastest? "Recent funding" may be strong for 60 days then decay rapidly. "Job posting" may be strong for 30 days. Feed decay curves into the auto-scoring model so it weights signals by freshness.
- **Seasonal pattern analysis:** Overlay timeline distribution against calendar months. Detect patterns: more Immediate deals in Q4 (budget expiration), more Long-term in Q1 (planning). Adjust scoring model seasonally.
- **Monthly calibration report:** Automated comparison of predicted close dates at qualification time vs actual close dates. Identifies systematic biases (e.g., the model consistently over-estimates urgency for enterprise accounts by 30 days).

### 4. Establish guardrails

Configure safety limits in the autonomous optimization loop:

- **Maximum 1 active experiment at a time** for scoring model changes
- **Revert threshold:** If forecast accuracy degrades >30% during an experiment, auto-revert immediately
- **Human approval required for:**
  - Changing signal weights by more than 25% on any single signal
  - Adding or removing an enrichment signal from the scoring model
  - Changing the threshold that separates Immediate from Near-term
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** 7 days between experiments on the same variable
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for strategic review.

### 5. Monitor for convergence

The optimization loop runs indefinitely. It should detect convergence — when successive experiments produce <2% improvement in forecast accuracy for 3 consecutive experiments. At convergence:

1. The timeline scoring model has reached its local maximum for your current market
2. Reduce monitoring frequency from daily to weekly
3. Report to the team: "Timing qualification is optimized. Current forecast accuracy: {X} days average variance. Prediction accuracy: {Y}%. Further gains require strategic changes (new ICP segments, new enrichment providers, product changes) rather than scoring formula optimization."
4. Shift the agent's focus to signal detection and pipeline monitoring rather than scoring optimization

### 6. Evaluate sustainability

Measure against: sustained or improving forecast accuracy (within 14 days of predicted close) over 6 months with the autonomous optimization loop finding and maintaining the local maximum.

This level runs continuously. Monthly review:
- Is the optimization loop producing value? (Experiments winning, accuracy improving)
- Is the loop converging? (Diminishing returns on experiments)
- Are there market shifts the loop cannot handle? (New competitor, economic change, product pivot)
- Are seasonal adjustments being applied automatically?
- Is cost per timeline-qualified lead stable?

## Time Estimate

- Autonomous optimization loop setup: 12 hours
- Signal detection configuration: 8 hours
- Reporting and guardrail setup: 6 hours
- Ongoing monitoring and brief review: 4 hours/month (24 hours over 6 months)
- Discovery calls (ongoing, Immediate/Near-term only): 6 hours/month (36 hours over 6 months)
- Strategic reviews and calibration: 3 hours/month (18 hours over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with timeline pipeline and experiment logging | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment + signal monitoring at scale | Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| Instantly | Cold email sequences (auto-optimized cadences) | Hypergrowth $97/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation: optimization loop, reporting, alerts | Pro $60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription for ongoing discovery calls | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics, experiments, anomaly detection, feature flags | Usage-based ~$50-200/mo at scale — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, auto-scoring | ~$50-100/mo at Durable volume — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost:** ~$750-1,000/mo (Clay $495 + Instantly $97 + n8n $60 + Fireflies $18 + PostHog ~$50-200 + Anthropic ~$50-100)

## Drills Referenced

- `autonomous-optimization` — the core always-on optimization loop: monitor > diagnose > experiment > evaluate > implement
- `autonomous-optimization` — durable-level dashboards with model drift tracking, experiment impact, signal decay, and seasonal analysis
- `signal-detection` — always-on monitoring for timing-relevant buying signals that trigger re-scoring or new lead creation
