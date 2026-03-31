---
name: meddic-qualification-durable
description: >
  MEDDIC Qualification System — Durable Intelligence. Always-on AI agents continuously optimize
  MEDDIC scoring weights, discovery strategies, and element gap interventions. Autonomous
  optimization loop detects metric anomalies, generates hypotheses, runs experiments, and
  auto-implements winners. Converges when successive experiments produce <2% improvement.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving MEDDIC-driven close rates (>=15% lift) over 6 months via continuous agent-driven element optimization, call coaching, and market adaptation"
kpis: ["Close rate by MEDDIC score", "Agent experiment win rate", "Element quality trend", "Predictive accuracy"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
drills:
  - autonomous-optimization
---

# MEDDIC Qualification System — Durable Intelligence

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

The MEDDIC qualification system runs autonomously. AI agents continuously monitor deal health, detect when scoring accuracy degrades, experiment with improved discovery strategies and element gap interventions, and auto-implement winners. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in MEDDIC performance -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement, indicating the MEDDIC qualification process has reached its local maximum for your market and deal motion.

## Leading Indicators

- Autonomous optimization loop running daily, generating at least 1 experiment per month
- Scoring accuracy (true positive + true negative rate) trending upward or stable above 75%
- Element predictive power analysis showing which MEDDIC elements most strongly predict deal outcomes
- Weekly optimization briefs being generated and posted to Slack
- At least 1 experiment adopted in the first month (scoring weight adjustment, discovery strategy change, or follow-up intervention improvement)
- Convergence detection active — system can identify when optimization has plateaued

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the MEDDIC qualification play. This creates the always-on agent loop with 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks MEDDIC play KPIs daily using `posthog-anomaly-detection`:
- MEDDIC completeness rate across the pipeline
- Close rate by MEDDIC score quartile
- Per-element completion rates
- Scoring accuracy (true positive / false positive rates)
- Deal velocity by MEDDIC composite score
- Element gap follow-up conversion rates

Classify each metric: normal (within +/-10% of 4-week average), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current scoring weights, discovery question strategies, follow-up templates, pipeline distribution) and 8-week metric history from PostHog. Runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples of MEDDIC-specific hypotheses:

- "Close rate dropped because Economic Buyer weight (20%) is too high — deals with strong Champion but weak Economic Buyer access are being under-scored. Hypothesis: reduce EB weight to 15%, increase Champion to 20%."
- "Element completion rate for Decision Process dropped — the discovery question set for this element is not producing actionable responses. Hypothesis: replace open-ended process questions with structured timeline-mapping questions."
- "Follow-up materials for Metrics gap are not improving scores. Hypothesis: switch from generic case studies to industry-specific ROI calculators."
- "Champion identification rate dropped after hiring a new SDR. Hypothesis: the pre-call question guide needs champion-specific question examples for less experienced callers."

Store hypotheses in Attio. If risk = "high" (e.g., changing scoring weights), send Slack alert for human review. If risk = "low" or "medium", proceed automatically.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment using PostHog feature flags:

- **Scoring weight experiments:** Create a feature flag that splits new deals into control (current weights) and variant (proposed weights). Score both groups with both weight sets. After 20+ deals per group, compare close rate and velocity.
- **Discovery question experiments:** Create a variant question set for the target element. Randomly assign incoming calls to control or variant prep guides. Measure post-call element score improvement.
- **Follow-up intervention experiments:** Create variant follow-up materials or strategies. Randomly assign deals with the target element gap to control or variant. Measure element score improvement after 7 days.

Minimum experiment duration: 14 days or 20 deals per variant, whichever is longer. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt:** Variant outperforms control by 5%+ with statistical confidence. Update live configuration. Log the change.
- **Iterate:** Results inconclusive. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Control outperforms variant. Disable variant. Log the failure. Return to Phase 1.
- **Extend:** Insufficient data. Run for another period.

Store full evaluation in Attio with decision, confidence, reasoning.

**Phase 5 — Report (weekly via n8n cron):**
Generate weekly optimization brief:
```
## MEDDIC Optimization Brief — Week of {date}

### Anomalies Detected
- {metric}: {classification} ({value} vs {4-week avg})

### Experiments Active
- {experiment_name}: {status}. {days remaining or results}

### Decisions Made
- {experiment_name}: {decision}. Net impact: {metric change}

### Scoring Accuracy
- True Positive Rate: {pct}% (target: >75%)
- False Positive Rate: {pct}% (target: <25%)
- Most Predictive Element: {element} (r={correlation})
- Least Predictive Element: {element} (r={correlation})

### Element Health
| Element | Avg Score | Completion Rate | Predictive Power | Trend |
|---------|-----------|-----------------|-------------------|-------|
| Metrics | {score} | {pct}% | {r} | {up/down/flat} |
| Economic Buyer | {score} | {pct}% | {r} | {up/down/flat} |
| Decision Criteria | {score} | {pct}% | {r} | {up/down/flat} |
| Decision Process | {score} | {pct}% | {r} | {up/down/flat} |
| Identify Pain | {score} | {pct}% | {r} | {up/down/flat} |
| Champion | {score} | {pct}% | {r} | {up/down/flat} |

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Estimated distance from local maximum: {assessment}

### Recommended Focus Next Week
- {recommendation based on data}
```

Post to Slack and store in Attio.

Estimated time for setup: 15 hours. Then always-on.

### 2. Maintain deal health monitoring at scale

Continue running the the meddic deal health monitor workflow (see instructions below) drill from Scalable. At Durable level, enhance it:

- **Cross-deal pattern detection:** When 3+ deals show the same element degradation (e.g., Champion scores dropping across the pipeline), flag it as a systemic issue rather than individual deal problems. Feed this into the autonomous optimization loop as a high-priority anomaly.
- **Predictive risk scoring:** Use historical data to predict which deals are likely to stall or lose based on their MEDDIC element trajectory. Alert the founder before problems manifest, not after.
- **Win/loss MEDDIC forensics:** For every closed deal (won or lost), automatically extract the final MEDDIC profile and store it. Over time, build a dataset of "MEDDIC profiles of deals that closed won" vs. "MEDDIC profiles of deals that closed lost." Use this to refine scoring weights and identify the element patterns that predict outcomes.

Estimated time: 10 hours enhancement, then always-on.

### 3. Continuous qualification reporting and calibration

Continue running the `autonomous-optimization` drill from Scalable. At Durable level, enhance it:

- **Monthly scoring weight recalibration:** Automatically run the calibration analysis using won/lost deal data. If data suggests weight changes, generate an experiment (Phase 3 of autonomous optimization) rather than changing weights directly.
- **Per-element predictive power tracking:** Continuously compute the correlation between each element score and deal outcome. If an element's predictive power drops below 0.1 (near zero correlation), flag it for review — that element may not matter for your specific deal motion.
- **Market adaptation detection:** Monitor if win rates are changing independent of MEDDIC scores. If overall market conditions shift (new competitor, market downturn), the agent should detect that MEDDIC scores are stable but close rates changed — indicating an external factor, not a scoring problem.

Estimated time: 5 hours enhancement, then always-on.

### 4. Guardrails (CRITICAL)

The autonomous optimization loop must respect these constraints:

- **Rate limit:** Maximum 1 active experiment per MEDDIC dimension at a time. Never test scoring weight changes and discovery question changes for the same element simultaneously.
- **Revert threshold:** If close rate drops >15% during any experiment, auto-revert immediately and alert the founder.
- **Human approval required for:**
  - Scoring weight changes that shift any element by more than 5 percentage points
  - Adding or removing pipeline stages
  - Changes to the MEDDIC composite threshold (currently 70 for Qualified)
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 14 days before testing a new hypothesis on the same element.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured:** If a MEDDIC element does not have PostHog tracking, fix tracking first before running experiments on it.
- **Data minimum:** Do not run experiments with fewer than 15 deals per variant. Wait for sufficient volume.

### 5. Convergence detection

The optimization loop runs indefinitely but should detect convergence — when the MEDDIC qualification process has reached its local maximum:

- Track the improvement percentage of each successive adopted experiment
- When 3 consecutive experiments produce <2% improvement on their target metric, declare convergence for that dimension
- At convergence for all dimensions:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency to 1 per quarter (maintenance mode)
  3. Report: "MEDDIC qualification is optimized. Current performance: {metrics}. Close rate lift: {pct}%. Scoring accuracy: {pct}%. Further gains require strategic changes (new market segment, product changes, competitive repositioning) rather than tactical optimization."
- Continue watching for market shifts that could break convergence (new competitor, pricing changes, ICP drift)

### 6. Evaluate sustainability

Measure against threshold: Sustained or improving MEDDIC-driven close rates (>=15% lift) over 6 months.

Monthly review checklist:
- Close rate by MEDDIC quartile: still showing 15%+ lift for top quartile?
- Scoring accuracy: true positive rate still above 75%?
- Element predictive power: any elements lost predictive value?
- Autonomous optimization: experiments running and producing results?
- Deal health: pipeline getting healthier or degrading?
- Founder efficiency: time per deal still decreasing or stable?

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay, diagnose whether the issue is market saturation, buyer behavior shift, competitive landscape change, or model drift.

## Time Estimate

- Autonomous optimization setup: 15 hours
- Deal health monitoring enhancement: 10 hours
- Reporting and calibration enhancement: 5 hours
- Ongoing monitoring, experiment review, and strategic oversight: ~110 hours over 6 months (~4-5 hours/week)

**Total: ~140 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MEDDIC pipeline, experiment logs, win/loss data | Standard stack (excluded) |
| PostHog | Dashboards, funnels, feature flags, experiments, anomaly detection | Standard stack (excluded) |
| n8n | Orchestration — optimization loop, health monitor, reporting, experiments | Standard stack (excluded) |
| Clay | Prospect enrichment at scale | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies.ai | Call transcription for ongoing discovery calls | Business: $19/user/mo. [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Instantly | Email sequences for element-gap follow-ups | Growth: $37/mo. [instantly.ai/pricing](https://instantly.ai/pricing) |
| Anthropic API | Claude for optimization loop (hypothesis generation, experiment evaluation, weekly briefs, transcript extraction) | ~$50-150/mo at Durable volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$600-700/mo** (Clay $495 + Fireflies $19 + Instantly $37 + Anthropic ~$50-150)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- the meddic deal health monitor workflow (see instructions below) — enhanced at Durable with cross-deal pattern detection, predictive risk scoring, and win/loss forensics
- `autonomous-optimization` — enhanced at Durable with automatic weight recalibration, predictive power tracking, and market adaptation detection
