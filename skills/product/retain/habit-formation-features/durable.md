---
name: habit-formation-features-durable
description: >
  Habit-Building Features — Durable Intelligence. An always-on AI agent monitors habit metrics,
  detects decay and anomalies, generates improvement hypotheses, runs A/B experiments, and
  auto-implements winners. Converges when successive experiments yield <2% improvement.
  Sustained or improving DAU ≥35% over 6 months.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving DAU ≥35% over 6 months via autonomous optimization"
kpis: ["Daily active rate", "Streak survival rate at day 30", "Experiment velocity", "Optimization lift per cycle", "Convergence distance"]
slug: "habit-formation-features"
install: "npx gtm-skills add product/retain/habit-formation-features"
drills:
  - autonomous-optimization
  - milestone-retention-monitor
  - gamification-health-monitor
---

# Habit-Building Features — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

DAU ≥35% sustained or improving over 6 months with no manual intervention beyond human-gated approvals. The autonomous optimization loop finds the local maximum for habit mechanics, reminder cadence, personalization rules, and churn interventions. Converges when 3 consecutive experiments produce <2% improvement.

## Leading Indicators

- Optimization loop runs on schedule (daily monitoring, weekly experiments) with zero missed cycles
- At least 2 experiments per month with statistically significant results
- Net positive lift from adopted experiments: cumulative ≥5pp DAU improvement in first 3 months
- Anomaly detection catches metric drops within 24 hours of onset
- Weekly optimization briefs generated and delivered on time

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on agent loop for habit metrics:

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check the play's primary KPIs: DAU, streak survival at day 7/14/30, reminder conversion rate, churn save rate.
- Compare last 2 weeks against 4-week rolling average.
- Classify: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase).
- If normal: log to Attio, no action.
- If anomaly detected: trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull 8-week metric history from PostHog.
- Gather current configuration from Attio: streak mechanic settings, reminder timing, personalization rules, active A/B tests.
- Run `hypothesis-generation` with anomaly data + configuration context.
- Receive 3 ranked hypotheses with expected impact and risk level.
- Store hypotheses in Attio as notes on the habit-formation campaign record.
- If top hypothesis risk = "high": send Slack alert for human review and STOP.
- If risk = "low" or "medium": proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using `posthog-experiments`: create a feature flag splitting traffic between control (current config) and variant (hypothesis change).
- Implement the variant. Examples of habit-specific experiments the agent may generate:
  - Adjust streak grace period from 1 day to 2 days
  - Change reminder email send time for the "Steady Users" segment
  - Add a streak multiplier (2x points during a streak) at the 7-day milestone
  - Modify the churn intervention threshold from 50% frequency decline to 40%
  - Test a new milestone celebration format (progress bar vs badge vs confetti)
- Set experiment duration: minimum 7 days or 100+ users per variant, whichever is longer.
- Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog. Run `experiment-evaluation`.
- **Adopt:** Winner by ≥5% on primary metric with p < 0.05. Update live configuration. Log the change.
- **Iterate:** Result directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Variant underperformed control. Disable variant. Log failure. Return to Phase 1.
- **Extend:** Insufficient sample size. Keep running for another period.
- Store full evaluation in Attio.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made.
- Calculate net metric change from all adopted changes this week.
- Generate the weekly optimization brief:
  - What changed and why
  - Net impact on DAU, streak survival, reminder conversion
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post brief to Slack and store in Attio.

**Guardrails:**
- Maximum 1 active experiment at a time. Never stack experiments on the habit system.
- Auto-revert if DAU drops >30% during any experiment.
- Human approval required for: changes affecting >50% of users, reminder frequency increases, or any "high risk" hypothesis.
- Cooldown: 7 days after a failed experiment before testing the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.

### 2. Monitor milestone retention decay

Run the `milestone-retention-monitor` drill to detect when habit milestone celebrations lose effectiveness:

- Build paired cohorts: users who engaged with milestone celebrations vs users who dismissed them. Compare 7-day, 14-day, and 30-day retention.
- Create the milestone effectiveness dashboard: celebration engagement rate by streak milestone, retention lift trend, CTA conversion at milestones, celebration fatigue index.
- Build a weekly decay detection workflow in n8n: if celebration engagement rate declines ≥15% on any milestone tier, alert the autonomous optimization loop to prioritize that tier.
- Track churned-despite-milestone users: users who hit streak milestones 7+ but still went inactive. Pull their last 5 sessions, which celebrations they saw, and what CTAs they were shown. Store analysis in Attio for the optimization loop's hypothesis generation.
- Calculate per-user `celebration_fatigue_score`: (celebrations dismissed) / (celebrations shown). If >0.5, the agent should test a new celebration format for that user's segment.

### 3. Monitor gamification health

Run the `gamification-health-monitor` drill for habit-specific health signals the generic optimization loop would miss:

- Monitor participation rate: % of active users earning streak points this week. Alert if below 30%.
- Monitor streak distribution: healthy distribution has a long tail (many users at 7+ days). If distribution shifts toward 1-2 day streaks, the habit is not forming.
- Monitor broken streak recovery rate: % of users who restart within 48 hours of a break. Declining recovery rate is an early churn signal.
- Monitor reminder channel health: email open rates, in-app message click rates. If a channel's effectiveness drops ≥20%, flag for the optimization loop.
- Build automated interventions for gamification-specific signals:
  - Streak distribution collapse (median streak dropping): Intercom in-app survey asking what would make the habit easier.
  - Recovery rate decline: test a new streak-save mechanic (e.g., "use a token to restore your streak").
  - Reminder channel death: switch dormant-channel users to the alternate channel automatically.

### 4. Evaluate sustainability

This level runs continuously. Monthly review checkpoints:

- **Month 1-2:** Optimization loop is running on schedule. At least 4 experiments completed. Net DAU lift from experiments is positive.
- **Month 3-4:** Experiment velocity may slow as obvious improvements are captured. Focus shifts to segment-specific optimizations and celebration format testing.
- **Month 5-6:** The loop should approach convergence. If 3 consecutive experiments produce <2% improvement, the play has reached its local maximum. Reduce monitoring from daily to weekly. Report: "Habit system optimized. Current DAU is [X]%. Further gains require product-level changes (new actions, new reward types) rather than parameter optimization."

If at any point DAU drops below 30% for 2 consecutive weeks despite interventions, escalate for human strategic review.

## Time Estimate

- 20 hours: configure autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog experiments integration, Attio logging)
- 10 hours: set up milestone retention monitor and decay detection
- 10 hours: set up gamification health monitor and automated interventions
- 10 hours: initial testing and calibration of the optimization loop (weeks 1-2)
- 100 hours: ongoing operation over 6 months (~4 hours/week for human review of briefs, experiment approvals, and strategic direction)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, anomaly detection, dashboards, feature flags | Usage-based; $0.00005/event above 1M free ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Habit emails, re-engagement sequences | $49-149/mo depending on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app interventions, surveys, celebration messages | $85/seat/mo Advanced ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs | ~$20-50/mo at ~4 experiments/month + weekly briefs ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| n8n | Optimization loop scheduling, decay detection, intervention routing | Standard stack |
| Attio | Experiment logging, campaign records, hypothesis storage | Standard stack |

**Estimated play-specific cost:** ~$154-284/mo (Loops $49-149 + Intercom $85 + Anthropic API $20-50)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners → weekly briefs
- `milestone-retention-monitor` — detect when habit milestone celebrations lose effectiveness and feed decay signals to the optimization loop
- `gamification-health-monitor` — monitor streak distribution, recovery rates, reminder channel health, and trigger habit-specific interventions
