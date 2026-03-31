---
name: price-objection-handling-durable
description: >
  Price Objection Handling — Durable Intelligence. Always-on AI agents finding the
  local maximum: autonomous optimization detects metric anomalies, generates improvement
  hypotheses, runs A/B experiments on response frameworks and pricing structures,
  evaluates results, and auto-implements winners. Play-specific monitoring tracks
  objection patterns, discount leakage, and prevention effectiveness.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving objection overcome rate (>=65%) over 6 months via continuous agent-driven response optimization, pricing intelligence, and objection prevention"
kpis: ["Objection overcome rate trend", "Agent experiment win rate", "Discount optimization impact", "Objection prevention rate"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - autonomous-optimization
  - objection-intelligence-monitor
  - objection-detection-automation
---

# Price Objection Handling — Durable Intelligence

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The agent continuously optimizes every variable in the price objection handling system: which response framework wins for which root cause, what follow-up cadence resolves fastest, which value assets drive the most engagement, and what discount levels close deals without leaving money on the table. The agent detects when any metric drifts, generates hypotheses, runs experiments, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement — the play has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop running: daily monitoring, weekly hypothesis generation, experiments always active
- At least 1 experiment running at all times (no idle weeks)
- Weekly optimization brief generated and delivered every Monday
- Anomaly detection triggering within 24 hours of any metric shift >15%
- Convergence tracking: measuring diminishing returns across successive experiments
- Objection prevention rate trending upward (upstream improvements reducing objection frequency)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the price objection handling play. This creates the core loop:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection on the play's primary KPIs: overcome rate, resolution time, discount rate, prevention rate
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected -> trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull play context from Attio: current framework effectiveness, root cause distribution, active experiments
- Pull 8-week metric history from PostHog
- Run hypothesis generation with price-objection-specific context (fed by `objection-intelligence-monitor`)
- Receive 3 ranked hypotheses. Examples specific to this play:
  - "Overcome rate dropped 18% because `sticker_shock` objections doubled — a new competitor entered at a lower price point. Experiment: add a competitive TCO comparison as the first asset in the sticker_shock follow-up sequence."
  - "Average discount increased from 6% to 11% — reps are defaulting to discounts instead of framework responses. Experiment: remove discount from the first two response attempts and only allow after 2 value-first touches."
  - "Resolution time increased from 7 days to 13 days — follow-up sequences are too spread out. Experiment: compress the no_budget sequence from 14 days to 7 days."
- If top hypothesis is high risk -> send Slack alert for human review. Otherwise -> proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Create a PostHog experiment with feature flag splitting incoming objections between control and variant
- Implement the variant in the relevant system (update follow-up sequence in n8n, change asset in Instantly, modify response prompt for Claude)
- Set duration: minimum 7 days or 15+ objections per variant
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: did overcome rate improve >=10%? Did secondary metrics (discount rate, resolution time) stay stable?
- Decision: Adopt (implement permanently), Iterate (test a refined version), Revert (go back to control), or Extend (need more data)
- Store decision with full reasoning in Attio

**Phase 5 — Report (weekly, Mondays via n8n cron):**
- Generate the weekly optimization brief covering: anomalies detected, hypotheses generated, experiments run, decisions made, net KPI impact, distance from estimated local maximum
- Post to Slack, store in Attio

**Guardrails (enforced automatically):**
- Maximum 1 active experiment at a time on this play
- If primary metric drops >30% during any experiment -> auto-revert immediately
- Human approval required for: discount policy changes, response framework retirement, any "high risk" hypothesis
- After a failed experiment (revert), 7-day cooldown before testing the same variable
- Maximum 4 experiments per month. If all 4 fail -> pause optimization, flag for strategic review.

### 2. Deploy the objection intelligence monitor

Run the `objection-intelligence-monitor` drill to create the play-specific monitoring layer that feeds the autonomous optimization loop:

**PostHog dashboard (8 panels):**
- Objection overcome rate (weekly trend line)
- Root cause distribution (stacked bar)
- Framework effectiveness (heatmap: framework x outcome)
- Time to resolution (histogram)
- Discount leakage (average discount trend line)
- Objection prevention rate (monthly trend)
- Objection-to-close conversion funnel
- Revenue impact (deal value comparison: objection vs non-objection deals)

**Daily anomaly detection:**
- Overcome rate drops >15% from rolling average -> trigger optimization loop
- Single root cause exceeds 50% of all objections -> flag systematic issue
- Average discount trending upward for 3+ consecutive weeks -> flag discount creep
- Previously strong framework drops below 50% resolve rate -> flag framework decay

**Weekly pricing intelligence report (Mondays at 9 AM):**
- Headline metric (best and worst this week)
- Framework leaderboard with resolve rates
- Root cause shift analysis
- Discount health check
- Active experiments and status
- Deals currently at risk with recommended actions

### 3. Maintain the detection system

The `objection-detection-automation` drill from Scalable continues running at Durable. At this level, additionally:

- Tune the predictive scoring model monthly: compare predicted objections vs actual to improve accuracy
- Add new detection signals as patterns emerge (e.g., if prospects increasingly mention a new competitor, add that as a detection trigger)
- Monitor false positive rate — if auto-detection flags >20% false positives, retrain the classification prompt

### 4. Convergence detection and steady state

The optimization loop runs indefinitely, but it should detect when the play has reached its local maximum:

- Track the magnitude of improvement from each successive experiment
- If 3 consecutive experiments produce <2% improvement on the primary metric:
  1. Declare convergence
  2. Reduce monitoring frequency from daily to weekly
  3. Generate a convergence report: "Price objection handling is optimized. Current overcome rate: {X}%. Average resolution time: {Y} days. Discount rate: {Z}%. Further gains require strategic changes (new pricing model, new competitive positioning, product changes) rather than tactical optimization."
  4. Switch to maintenance mode: weekly monitoring, monthly hypothesis generation

If the market changes (new competitor, economic shift, pricing change), the agent will detect the resulting metric anomaly and re-enter the full optimization loop automatically.

## Time Estimate

- 20 hours: deploying autonomous optimization loop (n8n workflows, PostHog experiments, Attio integration)
- 15 hours: building the objection intelligence monitor (dashboard, anomaly detection, weekly reports)
- 10 hours: tuning predictive scoring and detection system
- 75 hours: monitoring, reviewing experiment results, approving hypotheses, and iterating (spread over 6 months)
- 10 hours: convergence analysis and steady-state transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, experiment logging, campaign notes | Standard stack (excluded) |
| PostHog | Dashboards, anomaly detection, experiments, feature flags | Standard stack (excluded) |
| n8n | Optimization loop orchestration, cron schedules, webhooks | Standard stack (excluded) |
| Fireflies | Call transcription for ongoing detection | Pro: $18/user/mo — [pricing](https://fireflies.ai/pricing) |
| Instantly | Follow-up email delivery (continued) | Hypergrowth: $97/mo — [pricing](https://instantly.ai/pricing) |
| Clay | Enrichment for predictive scoring and deal context | Launch: $185/mo — [pricing](https://www.clay.com/pricing) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, response generation, weekly reports | ~$50-120/mo (daily monitoring + weekly reports + experiment cycles) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** ~$350-420/mo (Fireflies + Instantly + Clay + Claude API)
Agent compute is variable based on experiment velocity and monitoring frequency.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics -> detect anomalies -> generate hypotheses -> run experiments -> evaluate -> implement winners -> report weekly
- `objection-intelligence-monitor` — play-specific monitoring: 8-panel dashboard, daily anomaly detection, weekly pricing intelligence report, domain-specific hypothesis context for the optimization loop
- `objection-detection-automation` — continued from Scalable: always-on call and email monitoring, predictive scoring, auto-classification
