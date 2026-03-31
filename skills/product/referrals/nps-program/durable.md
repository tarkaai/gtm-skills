---
name: nps-program-durable
description: >
  NPS Feedback System — Durable Intelligence. Autonomous AI agents continuously optimize
  survey timing, follow-up messaging, and segment routing to find the local maximum of
  NPS score and response rate. The autonomous-optimization loop detects anomalies,
  generates hypotheses, runs experiments, and auto-implements winners.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "30 hours setup + continuous operation over 6 months"
outcome: "NPS ≥40 sustained for 3+ consecutive months with response rate ≥40% AND autonomous experiments produce measurable lift"
kpis: ["NPS score", "NPS response rate", "Detractor close-the-loop rate", "Promoter advocacy conversion", "Experiment velocity", "Optimization lift", "Convergence status"]
slug: "nps-program"
install: "npx gtm-skills add product/referrals/nps-program"
drills:
  - autonomous-optimization
  - nps-health-monitor
---

# NPS Feedback System — Durable Intelligence

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

An always-on NPS system where AI agents autonomously monitor all NPS metrics, detect when performance degrades, generate improvement hypotheses, run A/B experiments, and auto-implement winners. The system finds the local maximum of NPS score and response rate for each user segment, then maintains it as conditions change. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce less than 2% improvement.

## Leading Indicators

- The `autonomous-optimization` loop fires its first anomaly detection within 7 days of activation
- First autonomous experiment launches within 14 days
- At least 1 experiment produces a statistically significant winner in the first month
- NPS health monitor shows all 8 metrics in "healthy" range for 2+ consecutive weeks
- Weekly optimization briefs are generated on schedule with actionable content
- No metric goes critical for more than 3 consecutive days without intervention

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the continuous improvement cycle for this play:

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check the NPS program's primary KPIs: NPS score, response rate, detractor close rate, promoter advocacy conversion
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current survey configuration from Attio (timing, channels, copy, segments), recent experiment results
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context. Example hypotheses the agent might generate:
  - "Response rate dropped because the in-app survey is now competing with a new feature announcement banner. Hypothesis: delay survey by 3 days after any feature announcement."
  - "NPS for new users dropped because onboarding changed. Hypothesis: shift new-user survey from 45 to 60 days to let them stabilize."
  - "Detractor close rate dropped because the team is overwhelmed with tickets. Hypothesis: auto-respond to detractors with score 4-6 citing known issues, reserving personal outreach for score 0-3."
- Receive 3 ranked hypotheses with expected impact and risk level
- If top hypothesis is high risk (e.g., changes affecting >50% of survey volume), send to Slack for human approval and STOP
- If low or medium risk, proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using `posthog-experiments`: create a feature flag that splits the relevant segment between control (current behavior) and variant (hypothesis change)
- Implement the variant: if the hypothesis involves survey timing, update the n8n scheduling workflow for the variant group. If it involves follow-up messaging, create the variant in Loops or Intercom.
- Set experiment duration: minimum 7 days or until 100+ responses per variant, whichever is longer
- Log experiment in Attio: hypothesis text, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live configuration to use the winning variant across the full segment. Log the change and the lift achieved.
- If Iterate: generate a refined hypothesis based on the results. Return to Phase 2.
- If Revert: disable the variant. Log the failure and reasoning. Enter 7-day cooldown before testing the same variable.
- If Extend: keep running. Set a reminder to re-evaluate.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate the week's optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on NPS score, response rate, and advocacy conversion
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy the NPS health monitor

Run the `nps-health-monitor` drill to build the play-specific monitoring layer:

Configure daily health checks for 8 NPS-specific metrics:

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Overall NPS | ≥40 | 25-39 | <25 |
| Response rate | ≥40% | 25-39% | <25% |
| Survey coverage (quarterly) | ≥50% | 30-49% | <30% |
| Detractor close rate | ≥80% | 60-79% | <60% |
| Promoter activation rate | ≥25% | 15-24% | <15% |
| NPS trend slope (12-week) | Positive/flat | Negative <-1pt/wk | Negative <-2pt/wk |
| Theme concentration | <40% | 40-60% | >60% |
| Close-the-loop latency | <24h | 24-48h | >48h |

The health monitor runs independently of the optimization loop. It provides the diagnostic layer: when a metric enters warning or critical, it runs segment-level diagnostics, fires automated interventions for known failure modes, and escalates unresolvable issues to humans.

Automated interventions include:
- Response rate drops for a segment: rotate survey copy automatically
- Close-the-loop latency exceeds 48 hours: escalate to account owner's manager
- Promoter activation below 15%: add an extra in-app nudge at day 7
- NPS declining 3 weeks straight: trigger deep-dive open-text analysis and report

### 3. Configure guardrails

The autonomous optimization loop operates within strict guardrails:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack NPS experiments.
- **Revert threshold:** If any primary metric drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Survey copy changes that affect all segments simultaneously
  - Changes to the detractor escalation SLA
  - Any experiment the hypothesis generator flags as high risk
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for strategic review.
- **Never experiment on detractor follow-up timing for critical detractors** (score ≤3 or MRR ≥$500). These always get immediate personal outreach.

### 4. Monitor convergence

The optimization loop detects convergence: when 3 consecutive experiments produce less than 2% improvement on the target metric. At convergence:

1. The NPS program has reached its local maximum for the current product, audience, and competitive context
2. Reduce the optimization loop from weekly experiments to monthly check-ins
3. Maintain the health monitor at daily frequency (to detect external shocks)
4. Generate a convergence report: "NPS program optimized. Current NPS: [score]. Response rate: [rate]. Promoter advocacy conversion: [rate]. Further gains require strategic changes: product improvements addressing top detractor themes, expansion to new user segments, or changes to the advocacy reward structure."

### 5. Evaluate sustainability

This level runs continuously. Monthly review:

- NPS score: sustained ≥40 for 3+ consecutive months. If it drops below 40 for 2 months, the optimization loop should have already diagnosed the cause and launched experiments.
- Response rate: sustained ≥40%. If declining, check fatigue indicators from the health monitor.
- Experiment velocity: at least 2 experiments per month until convergence. If the loop is not generating experiments, check that anomaly detection thresholds are correctly calibrated.
- Optimization lift: cumulative improvement from all adopted experiments since Durable launch. Track this as the "AI lift" metric.

**Human action required:** Monthly strategic review of the weekly optimization briefs. Approve or reject any queued high-risk experiments. Review the detractor theme report and confirm that product roadmap priorities align with NPS feedback.

## Time Estimate

- Autonomous optimization loop setup: 10 hours
- NPS health monitor setup: 8 hours
- Guardrail configuration and testing: 4 hours
- First month monitoring and tuning: 8 hours
- Ongoing: ~2 hours/month reviewing briefs and approving experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app surveys, advocacy messages, intervention nudges | Proactive Support Plus: $99/mo. [Pricing](https://www.intercom.com/pricing) |
| PostHog | Surveys, experiments, feature flags, anomaly detection, dashboards | Surveys: $0.10/response after 1,500 free. Experiments: $0.0001/request. [Pricing](https://posthog.com/pricing) |
| Loops | Email surveys, follow-up sequences, escalation emails | From $49/mo. [Pricing](https://loops.so/pricing) |
| Attio | Response data, experiment logs, health reports, advocacy tracking | Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |
| n8n | Optimization loop, health monitor, scheduling, routing | Pro: $60/mo recommended for execution volume. [Pricing](https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, theme clustering | Usage-based. ~$10-30/mo for this play's volume. [Pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at this level:** ~$150-400/mo. Primary cost drivers are PostHog survey volume, n8n execution volume, and Anthropic API for the optimization loop's reasoning steps.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop that monitors metrics, generates hypotheses, runs experiments, evaluates results, and auto-implements winners. This is what makes Durable fundamentally different from Scalable.
- `nps-health-monitor` — NPS-specific monitoring layer with 8 health metrics, diagnostic triggers, automated interventions, and escalation rules. Complements the generic optimization loop with play-specific intelligence.
