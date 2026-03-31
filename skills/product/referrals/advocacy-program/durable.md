---
name: advocacy-program-durable
description: >
  Formal Advocacy Program — Durable Intelligence. Autonomous optimization loop detects metric
  anomalies, generates hypotheses, runs A/B experiments, and auto-implements winners. Weekly
  optimization briefs. Converges when successive experiments produce <2% improvement.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Events"
level: "Durable Intelligence"
time: "Ongoing, ~4 hours/week agent compute"
outcome: "Advocacy metrics sustained or improving for 6+ months via autonomous optimization"
kpis: ["Advocate retention rate (>=70% with action in last 90 days)", "Referral yield (>=2 per advocate per quarter)", "Experiment velocity (>=2 experiments/month)", "Net metric lift from adopted experiments", "Convergence status (local maximum reached or still optimizing)"]
slug: "advocacy-program"
install: "npx gtm-skills add product/referrals/advocacy-program"
drills:
  - autonomous-optimization
---

# Formal Advocacy Program — Durable Intelligence

> **Stage:** Product -> Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Events

## Outcomes

All advocacy metrics sustained or improving for 6+ months with no manual intervention beyond human-approval gates. The autonomous optimization loop finds the local maximum of the program — the best achievable enrollment rate, activation rate, referral yield, and advocate retention given the current product, audience, and market. Weekly optimization briefs document every change and its impact.

## Leading Indicators

- Autonomous optimization loop running daily (anomaly detection) and weekly (reporting)
- At least 2 experiments completed per month with clear adopt/iterate/revert decisions
- No metric in "critical" status for more than 3 consecutive days without intervention
- Net positive metric lift from adopted experiments (cumulative)
- Convergence signal: successive experiments produce diminishing returns

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on agent loop for the advocacy program. Configure it with these play-specific parameters:

**Primary KPIs to monitor:**
- Advocate enrollment rate (new enrollments / eligible users, weekly)
- Activation rate (first action within 30 days of enrollment)
- Referral yield (referrals per active advocate per quarter)
- Referral conversion rate (referred signups activated / referrals submitted)
- Advocate retention (advocates with action in last 90 days / total advocates)

**Phase 1 — Monitor (daily via n8n cron):**
The agent uses `posthog-anomaly-detection` to check each KPI daily. Compare the trailing 2-week window against the 4-week rolling average. Classify each metric:
- Normal: within +/-10% of rolling average
- Plateau: within +/-2% for 3+ consecutive weeks
- Drop: >20% decline from rolling average
- Spike: >50% increase from rolling average

If all metrics normal, log to Attio and take no action. If any anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current program configuration: tier thresholds, active rewards, message variants, nudge cadence) and PostHog (8-week metric history). It runs `hypothesis-generation` with the anomaly data to produce 3 ranked hypotheses.

Examples of advocacy-specific hypotheses the agent should generate:
- "Activation rate dropped because the testimonial ask is stale after 3 months. Test a new ask type (short video review) as the default first action."
- "Referral yield plateaued because the reward (account credit) has diminishing marginal value for heavy users. Test a feature unlock reward instead."
- "Enrollment rate spiked after a product update but activation did not follow. The new enrollees are lower-quality candidates pulled in by the feature flag, not genuine power users. Test raising the enrollment score threshold from 60 to 65."

Store hypotheses in Attio as notes. If top hypothesis is high-risk (affects >50% of advocates or changes tier structure), send Slack alert for human review and STOP.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent uses `posthog-experiments` to create a feature flag splitting advocates between control and variant. It implements the variant using the appropriate tool:
- Messaging changes: update the Loops sequence or Intercom message variant
- Reward changes: modify the referral reward delivery workflow in n8n
- Threshold changes: adjust the power user score cutoff in the recruitment automation
- Cadence changes: modify the nudge schedule in n8n

Minimum experiment duration: 7 days or 100+ samples per variant, whichever is longer. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` with control vs. variant data. Decision matrix:
- **Adopt** (variant wins with >= 95% confidence): update live configuration, log the change, move to Phase 5
- **Iterate** (directionally positive but not significant): generate a refined hypothesis building on the result, return to Phase 2
- **Revert** (variant loses or neutral): disable variant, restore control, log failure, return to Phase 1
- **Extend** (insufficient data): keep running for another period

Store full evaluation in Attio: decision, confidence interval, sample sizes, reasoning.

**Phase 5 — Report (weekly via n8n cron):**
Every Monday, the agent generates a weekly optimization brief:
- Anomalies detected this week and their classifications
- Hypotheses generated and their risk assessments
- Experiments running: current status, interim results
- Experiments completed: decision (adopt/iterate/revert) with reasoning
- Net metric change from all adopted changes
- Current distance from estimated local maximum
- Recommended focus for next week

Post the brief to Slack and store in Attio.

### 2. Layer in play-specific health monitoring

Run the `autonomous-optimization` drill alongside the autonomous optimization loop. The health monitor provides the advocacy-specific diagnostic layer that the generic optimization loop needs:

**Daily health check (8 metrics):**
The health monitor classifies each advocacy metric as healthy/warning/critical using the thresholds defined at Scalable level. When a metric enters warning or critical, the health monitor runs targeted diagnostics:

- Recruitment rate declining: check if the eligible pool shrank (product engagement upstream problem) or enrollment is failing (invitation mechanic problem)
- Activation rate declining: check nudge sequence performance, compare activation by enrollment cohort, verify the "easiest ask" is still easy
- Referral yield declining: check if advocates are sharing links at all; if sharing but no conversions, the referral landing page or incentive is broken
- Advocate retention declining: cross-reference with product usage to distinguish program churn from product churn

**Automated interventions (4 triggers):**
- Stale enrollment message: auto-rotate if click rate < 5%
- Activation stall: extra personalized nudge if cohort 14-day activation < 20%
- Referral drought: in-app reminder to top advocates if no referrals in 14 days
- Lapsed advocate: re-engagement email with contextual ask based on recent product usage

The health monitor feeds diagnostic data into the autonomous optimization loop. When the monitor detects a warning or critical metric, it provides the context the optimization loop needs to generate better hypotheses in Phase 2.

### 3. Configure guardrails

**Rate limit:** Maximum 1 active experiment at a time on the advocacy program. Never stack experiments.

**Revert threshold:** If any primary metric drops >30% during an experiment, auto-revert immediately.

**Human approval required for:**
- Changes to tier structure (adding/removing tiers, changing score thresholds by more than 5 points)
- Reward value changes > 20%
- Any change the hypothesis generator flags as "high risk"
- Ambassador-tier modifications (these affect your most valuable advocates)

**Cooldown:** After a failed experiment, wait 7 days before testing the same variable.

**Monthly experiment cap:** 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review. The program may need structural changes, not tactical optimization.

### 4. Detect convergence

The optimization loop runs indefinitely. Monitor for convergence: when 3 consecutive experiments produce < 2% improvement on their target metric, the program has reached its local maximum.

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from 2/month to 1/month (maintenance mode)
3. Generate a convergence report: current steady-state metrics for all KPIs, list of all experiments run and their outcomes, estimated ceiling for each metric, and what strategic changes (new channels, product features, market expansion) would be required to break past the current maximum
4. Post the convergence report to Slack and store in Attio

If the market or product changes significantly (major feature launch, competitor shift, audience expansion), reset the convergence flag and return to active optimization.

### 5. Evaluate sustainability

This level runs continuously. Monthly review checkpoints:
- Are all KPIs at or above their Scalable-level baselines?
- Is the optimization loop generating actionable hypotheses, or has it become noise?
- Are experiments still producing meaningful lift, or has the program converged?
- Is the weekly brief useful to the team, or does it need format changes?

**Pass**: all advocacy metrics sustained or improving for 6+ consecutive months with autonomous optimization running. The program is durable.

**Escalate**: if metrics decay despite optimization efforts for 2+ months, the play needs strategic intervention (product changes, new audience segments, program redesign) rather than tactical optimization.

## Time Estimate

- Agent compute: ~4 hours/week (daily monitoring + weekly reporting + experiment management)
- Human review: ~1 hour/week (review weekly brief, approve high-risk experiments, Ambassador nominations)
- Setup: 8 hours initial configuration of the optimization loop and guardrails

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards, health metrics | Usage-based after free tier; expect $0-100/mo at this scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Experiment logging, hypothesis storage, advocate records, convergence tracking | Standard stack |
| Loops | Sequence variants for experiments, re-engagement emails | $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app message variants for experiments, health interventions | $29-85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Optimization loop crons, experiment workflows, health monitor, reporting | Standard stack |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief generation | ~$10-30/mo at 2-4 experiments/month ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated monthly cost: $88-264/mo** (Loops $49 + Intercom $29-85 + Anthropic API $10-30 + PostHog overage $0-100)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners, produce weekly optimization briefs
- `autonomous-optimization` — play-specific monitoring of 8 advocacy metrics with diagnostic triggers, automated interventions, and escalation rules that feed context into the optimization loop
