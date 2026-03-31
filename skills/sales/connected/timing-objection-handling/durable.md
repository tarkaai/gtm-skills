---
name: timing-objection-handling-durable
description: >
  Timing Objection Handling — Durable Intelligence. Always-on AI agents finding the
  local maximum: autonomous optimization detects metric anomalies, generates improvement
  hypotheses, runs A/B experiments on response strategies and urgency tactics,
  evaluates results, and auto-implements winners. Play-specific monitoring tracks
  timing patterns, smokescreen accuracy, reengagement conversion, and deal velocity.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving timeline acceleration rate (>=50%) over 6 months via continuous agent-driven timing intelligence, smokescreen detection, and urgency optimization"
kpis: ["Timeline acceleration rate trend", "Agent experiment win rate", "Smokescreen detection accuracy", "Reengagement conversion rate", "Deal velocity improvement"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
drills:
  - autonomous-optimization
---

# Timing Objection Handling — Durable Intelligence

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The agent continuously optimizes every variable in the timing objection handling system: which response strategy wins for which root cause, what follow-up cadence accelerates timelines fastest, which urgency assets drive the most engagement, how accurately the system detects smokescreens, and which reengagement approaches convert stalled deals. The agent detects when any metric drifts, generates hypotheses, runs experiments, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement — the play has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop running: daily monitoring, weekly hypothesis generation, experiments always active
- At least 1 experiment running at all times (no idle weeks)
- Weekly optimization brief generated and delivered every Monday
- Anomaly detection triggering within 24 hours of any metric shift >15%
- Convergence tracking: measuring diminishing returns across successive experiments
- Smokescreen detection accuracy trending upward (model improving over time)
- Reengagement conversion rate stable or improving (stalled deals returning)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the timing objection handling play. This creates the core loop:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection on the play's primary KPIs: acceleration rate, resolution time, smokescreen accuracy, reengagement conversion, cost-of-delay impact
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected -> trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull play context from Attio: current strategy effectiveness, root cause distribution, smokescreen trends, active experiments
- Pull 8-week metric history from PostHog
- Run hypothesis generation with timing-objection-specific context (fed by `autonomous-optimization`)
- Receive 3 ranked hypotheses. Examples specific to this play:
  - "Acceleration rate dropped 20% because `competing_priority` objections doubled after a major competitor launched — prospects are distracted by evaluating the competitor. Experiment: add competitive urgency content to the competing_priority follow-up sequence showing risk of falling behind peers who act now."
  - "Smokescreen detection accuracy fell from 78% to 55% — the classification prompt is not accounting for new objection language patterns. Experiment: retrain the classification prompt with the last 30 days of confirmed smokescreen-vs-genuine outcomes."
  - "Cost-of-delay presentations produce 60% acceleration but only 40% of applicable objections receive one. Experiment: expand cost-of-delay generation to all root causes (not just no_urgency and competing_priority)."
  - "Reengagement conversion dropped from 35% to 18% — outreach fires too late. Experiment: trigger reengagement 14 days before the scheduled date instead of 7."
- If top hypothesis is high risk -> send Slack alert for human review. Otherwise -> proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Create a PostHog experiment with feature flag splitting incoming timing objections between control and variant
- Implement the variant in the relevant system (update follow-up sequence in n8n, change urgency asset, modify classification prompt, adjust reengagement timing)
- Set duration: minimum 7 days or 12+ objections per variant
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: did acceleration rate improve >=10%? Did secondary metrics (smokescreen accuracy, reengagement rate) stay stable?
- Decision: Adopt (implement permanently), Iterate (test a refined version), Revert (go back to control), or Extend (need more data)
- Store decision with full reasoning in Attio

**Phase 5 — Report (weekly, Mondays via n8n cron):**
- Generate the weekly optimization brief covering: anomalies detected, hypotheses generated, experiments run, decisions made, net KPI impact, distance from estimated local maximum
- Post to Slack, store in Attio

**Guardrails (enforced automatically):**
- Maximum 1 active experiment at a time on this play
- If primary metric drops >30% during any experiment -> auto-revert immediately
- Human approval required for: strategy retirement, classification prompt changes affecting >50% of objections, any "high risk" hypothesis
- After a failed experiment (revert), 7-day cooldown before testing the same variable
- Maximum 4 experiments per month. If all 4 fail -> pause optimization, flag for strategic review.

### 2. Deploy the timing intelligence monitor

Run the `autonomous-optimization` drill to create the play-specific monitoring layer that feeds the autonomous optimization loop:

**PostHog dashboard (8 panels):**
- Timeline acceleration rate (weekly trend line)
- Root cause distribution (stacked bar)
- Strategy effectiveness (heatmap: strategy x outcome)
- Smokescreen detection accuracy (monthly line graph)
- Cost-of-delay impact (bar chart: presented vs not, grouped by outcome)
- Reengagement success rate (monthly line graph)
- Objection-to-close conversion funnel
- Deal velocity impact (deal cycle with vs without timing objections)

**Daily anomaly detection:**
- Acceleration rate drops >15% from rolling average -> trigger optimization loop
- Smokescreen classifications exceed 50% of all timing objections -> flag upstream discovery problem
- Reengagement conversion drops below 20% -> flag reengagement sequence for review
- Previously strong strategy drops below 30% acceleration rate -> flag strategy decay
- Single root cause exceeds 40% of all objections -> flag systematic issue

**Weekly timing intelligence report (Mondays at 9 AM):**
- Headline metric (best and worst this week)
- Strategy leaderboard with acceleration rates per root cause
- Smokescreen detection accuracy and trends
- Reengagement health (scheduled, converted, rate)
- Cost-of-delay impact analysis
- Active experiments and status
- Deals currently at risk with recommended actions

### 3. Maintain the detection system

The the timing objection detection automation workflow (see instructions below) drill from Scalable continues running at Durable. At this level, additionally:

- Tune the predictive timeline risk model monthly: compare predicted timing objections vs actual to improve scoring weights
- Update the classification prompt quarterly with confirmed smokescreen-vs-genuine outcomes to improve detection accuracy
- Add new detection signals as patterns emerge (e.g., if prospects increasingly mention a new reason for delay, add that to the taxonomy)
- Monitor false positive rate — if auto-detection flags >20% false positives, refine the detection prompt
- Track reengagement pipeline health: deals approaching their scheduled reengagement date, conversion funnel for returning deals

### 4. Convergence detection and steady state

The optimization loop runs indefinitely, but it should detect when the play has reached its local maximum:

- Track the magnitude of improvement from each successive experiment
- If 3 consecutive experiments produce <2% improvement on the primary metric:
  1. Declare convergence
  2. Reduce monitoring frequency from daily to weekly
  3. Generate a convergence report: "Timing objection handling is optimized. Current acceleration rate: {X}%. Average resolution time: {Y} days. Smokescreen detection accuracy: {Z}%. Reengagement conversion: {W}%. Further gains require strategic changes (new discovery methodology, new urgency creation approaches, product changes that create natural urgency) rather than tactical optimization."
  4. Switch to maintenance mode: weekly monitoring, monthly hypothesis generation

If the market changes (new competitor, economic shift, seasonal change), the agent will detect the resulting metric anomaly and re-enter the full optimization loop automatically.

## Time Estimate

- 20 hours: deploying autonomous optimization loop (n8n workflows, PostHog experiments, Attio integration)
- 15 hours: building the timing intelligence monitor (dashboard, anomaly detection, weekly reports)
- 10 hours: tuning predictive scoring and detection system, refining classification prompts
- 85 hours: monitoring, reviewing experiment results, approving hypotheses, and iterating (spread over 6 months)
- 10 hours: convergence analysis and steady-state transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, experiment logging, timeline fields, campaign notes | Standard stack (excluded) |
| PostHog | Dashboards, anomaly detection, experiments, feature flags | Standard stack (excluded) |
| n8n | Optimization loop orchestration, cron schedules, webhooks | Standard stack (excluded) |
| Fireflies | Call transcription for ongoing detection | Pro: $18/user/mo (~$10/user/mo annual) — [pricing](https://fireflies.ai/pricing) |
| Instantly | Follow-up email delivery (continued) | Hypergrowth: $97/mo — [pricing](https://instantly.ai/pricing) |
| Clay | Enrichment for predictive scoring and deal context | Launch: $185/mo — [pricing](https://www.clay.com/pricing) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, classification tuning, cost-of-delay generation, weekly reports | ~$50-120/mo (daily monitoring + weekly reports + experiment cycles) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** ~$350-420/mo (Fireflies + Instantly + Clay + Claude API)
Agent compute is variable based on experiment velocity and monitoring frequency.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics -> detect anomalies -> generate hypotheses -> run experiments -> evaluate -> implement winners -> report weekly
- `autonomous-optimization` — play-specific monitoring: 8-panel dashboard, daily anomaly detection, weekly timing intelligence report, domain-specific hypothesis context for the optimization loop
- the timing objection detection automation workflow (see instructions below) — continued from Scalable: always-on call and email monitoring, predictive scoring, auto-classification, smokescreen detection
