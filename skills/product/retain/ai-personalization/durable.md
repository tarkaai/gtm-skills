---
name: ai-personalization-durable
description: >
  AI Product Personalization — Durable Intelligence. Always-on autonomous optimization
  finds the local maximum of personalization performance via continuous experimentation.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "40 hours setup + ongoing autonomous operation over 6 months"
outcome: "Sustained or improving engagement >=45% over 6 months. Successive experiments produce <2% improvement (local maximum reached)."
kpis: ["Personalization engagement rate (trailing 30 days)", "Retention lift vs non-personalized baseline", "Experiment velocity (experiments completed per month)", "Autonomous optimization win rate", "Convergence metric (improvement per experiment)"]
slug: "ai-personalization"
install: "npx gtm-skills add product/retain/ai-personalization"
drills:
  - autonomous-optimization
  - personalization-health-monitor
  - nps-feedback-loop
---

# AI Product Personalization — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The personalization system sustains or improves engagement at 45%+ over 6 months without manual intervention. The `autonomous-optimization` loop runs continuously: detecting metric anomalies, generating improvement hypotheses, running A/B experiments, evaluating results, and auto-implementing winners. The system converges toward a local maximum where successive experiments produce less than 2% improvement for 3 consecutive experiments. At convergence, monitoring frequency drops and the agent reports that tactical optimization is exhausted.

## Leading Indicators

- Autonomous optimization loop fires daily (monitor phase) without failure for 30+ consecutive days
- At least 2 experiments completed per month (velocity target: 3-4/mo)
- Win rate of experiments is >= 30% (at least 1 in 3 experiments produces a winner)
- No red health alerts sustained for more than 48 hours without autonomous or human remediation
- Weekly optimization briefs generated and posted to Slack on schedule
- NPS scores for personalized users trend stable or upward quarter-over-quarter

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the personalization system:

**Phase 1 — Monitor (daily via n8n cron at 09:00 UTC):**

1. Use `posthog-anomaly-detection` to check personalization KPIs: overall engagement rate, per-segment engagement rates, retention lift vs control, dismissal rate, fallback rate
2. Compare last 2 weeks against the 4-week rolling average
3. Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If all normal: log to Attio, no action
5. If any anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**

1. Pull the current personalization configuration from Attio: active segments, variant assignments, dynamic selection rules, LLM prompt template, email sequences, active experiments
2. Pull 8-week metric history from PostHog using `posthog-dashboards`
3. Run `hypothesis-generation` with the anomaly data + configuration context. Prompt structure:

```
Context: AI personalization system for product retention.
Anomaly detected: {metric} has {classification} — current value: {current}, baseline: {baseline}.
Current configuration: {config snapshot}.
Recent changes: {last 3 experiment results}.

Generate 3 ranked hypotheses for what to change. For each:
1. What to change (specific: which surface, variant, rule, or content)
2. Expected impact (percentage improvement)
3. Risk level (low/medium/high)
4. How to test (what PostHog experiment to create)
```

4. Store hypotheses in Attio as notes on the personalization campaign record
5. If the top hypothesis has risk = "high": send Slack alert for human review, STOP
6. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis
2. Create a PostHog experiment: feature flag splitting traffic between control (current) and variant (hypothesis change)
3. Implement the variant: if the hypothesis targets a surface variant, update the dynamic selection rules via n8n; if it targets email content, update the LLM prompt; if it targets message timing or triggers, update the Intercom/n8n configuration
4. Minimum duration: 7 days or 200+ samples per variant, whichever is longer
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt:** Variant wins by >= 3pp at 95% confidence. Update live configuration. Log the change.
   - **Iterate:** Result is directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant loses or result is flat. Disable variant, restore control. Log the failure. Return to Phase 1 monitoring.
   - **Extend:** Insufficient sample size. Keep running for another period.
4. Store the full evaluation in Attio: decision, confidence, reasoning, metric impact

**Phase 5 — Report (weekly via n8n cron, Monday 10:00 UTC):**

1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on personalization engagement rate, retention lift, and per-segment performance
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Deploy the personalization health monitor

Run the `personalization-health-monitor` drill:

1. Configure the daily health check pipeline (n8n cron, 08:00 UTC — runs BEFORE the optimization loop)
2. Set thresholds:
   - Overall engagement rate: healthy >= 40%, amber 30-39%, red < 30%
   - Per-segment engagement: healthy within 10pp of baseline, amber 10-20pp below, red > 20pp below
   - Fallback rate: healthy < 10%, amber 10-20%, red > 20%
   - Pipeline reliability: healthy = all pipelines ran, amber = 1 pipeline missed, red = 2+ missed
3. Build the weekly health report (Monday 09:00 UTC — runs BEFORE the optimization brief)
4. Set up retention correlation tracking: personalization-engaged-retained vs not-engaged-churned cohorts
5. Monitor pipeline infrastructure: segmentation, scoring, variant selection, email generation

The health monitor feeds the autonomous optimization loop: red alerts automatically trigger the Monitor phase even if the daily cron hasn't fired yet.

### 3. Launch the NPS feedback loop for personalized users

Run the `nps-feedback-loop` drill targeted specifically at personalized users:

1. Deploy NPS surveys via Intercom at two milestones:
   - After 30 days of receiving personalized experiences
   - Quarterly for long-term personalized users
2. Segment NPS responses by behavioral segment and personalization variant
3. Close the loop per score:
   - Promoters (9-10): feed into referral pipeline. Log which personalization variant they received — this variant is a proven winner.
   - Passives (7-8): send targeted follow-up asking what would make the experience better. Feed responses into hypothesis generation.
   - Detractors (0-6): personal outreach. Log their segment, variants received, and specific complaints. If 3+ detractors cite the same issue, auto-create a hypothesis in the optimization loop.
4. Track NPS trend per segment monthly. If any segment's NPS drops below 20, flag for immediate investigation.

### 4. Configure convergence detection

The autonomous optimization loop should detect when it has reached the local maximum:

1. Track the improvement percentage of each adopted experiment
2. If 3 consecutive experiments produce < 2% improvement each, declare convergence
3. At convergence:
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment velocity from 3-4/mo to 1/mo (maintenance experiments)
   - Generate a convergence report: "Personalization has reached its local maximum. Current performance: [metrics]. Further gains require strategic changes (new personalization surfaces, new data signals, product changes) rather than tactical optimization."
   - Post the report to Slack and store in Attio
4. Continue weekly monitoring to detect external changes (seasonal shifts, product updates, competitive pressure) that could move the local maximum

### 5. Define guardrails for autonomous operation

**Critical guardrails (built into the n8n optimization workflow):**

- Maximum 1 active experiment at a time. Never stack experiments.
- Auto-revert if primary metric drops > 30% during any experiment.
- Human approval required for: changes affecting > 50% of users, changes to the LLM prompt template, changes to segment definitions.
- Cooldown: 7 days after a failed experiment before testing the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- Never optimize what is not measured: if a new surface is added, instrument tracking first (via `posthog-gtm-events`) before including it in optimization.

## Time Estimate

- 12 hours: autonomous optimization loop setup (5 phases in n8n)
- 8 hours: personalization health monitor deployment and threshold calibration
- 6 hours: NPS feedback loop setup and integration with optimization
- 4 hours: convergence detection logic and reporting
- 4 hours: guardrail implementation and testing
- 6 hours: first-month monitoring, tuning, and initial experiment review
- Ongoing: 2-4 hours/month for human review of weekly briefs and high-risk approvals

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, anomaly detection, dashboards, feature flags | Paid: ~$0.00005/event. At scale: $100-300/mo. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages, NPS surveys, product tours | Advanced: $85/seat/mo. Proactive Support: $349/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Personalized email sequences and transactional emails | $49-79/mo. [loops.so/pricing](https://loops.so/pricing) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, LLM email content | Sonnet 4.6: $3/$15 per MTok. Haiku 4.5 for email: $1/$5 per MTok. Estimated: $20-50/mo. [claude.com/pricing](https://claude.com/pricing) |
| n8n | All automation: optimization loop, health monitor, segmentation, scoring | Cloud: $60-120/mo at this execution volume. [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM for experiment tracking, health logs, convergence records | $29/seat/mo. [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost at Durable:** $300-700/mo (Intercom + n8n at volume + Claude API for optimization + Loops + PostHog at scale)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor, diagnose, experiment, evaluate, implement, report. Finds the local maximum of personalization performance through continuous A/B testing.
- `personalization-health-monitor` — daily health checks, weekly reports, retention correlation tracking, and pipeline reliability monitoring
- `nps-feedback-loop` — NPS surveys for personalized users, closed-loop follow-ups, and feedback-to-hypothesis pipeline
