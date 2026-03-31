---
name: autonomous-optimization
description: Continuous improvement loop that detects metric changes, generates hypotheses, runs experiments, and auto-implements winners
category: Analytics
tools:
  - PostHog
  - Anthropic
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-experiments
  - hypothesis-generation
  - experiment-evaluation
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-deals
---

# Autonomous Optimization

This is the drill that makes the Durable level fundamentally different from Scalable. Instead of running a play and measuring results, this drill creates an always-on agent loop that:

1. **Monitors** — detects when metrics plateau, drop, or spike
2. **Diagnoses** — generates hypotheses for what to change
3. **Experiments** — designs and runs A/B tests on the top hypothesis
4. **Decides** — evaluates results and auto-implements winners
5. **Reports** — generates weekly executive summaries of what changed and why

The goal is to find the **local maximum** of each play — the best possible performance given the current market, audience, and competitive landscape — and maintain it as conditions change.

## Input

- A play that has been running at Scalable level for at least 4 weeks (baseline data required)
- PostHog tracking configured with the play's core events
- n8n instance for scheduling the optimization loop
- Anthropic API key for Claude (hypothesis generation + evaluation)

## The Optimization Loop

### Phase 1: Monitor (runs daily via n8n cron)

Build an n8n workflow triggered by a daily cron schedule:

1. Use `posthog-anomaly-detection` to check the play's primary KPIs
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal → log to Attio, no action needed
5. If anomaly detected → trigger Phase 2

### Phase 2: Diagnose (triggered by anomaly detection)

1. Gather context: pull the play's current configuration from Attio (targeting, messaging, cadence, channel mix)
2. Pull 8-week metric history from PostHog using `posthog-dashboards`
3. Run `hypothesis-generation` with the anomaly data + context
4. Receive 3 ranked hypotheses with expected impact and risk levels
5. Store hypotheses in Attio as notes on the play's campaign record
6. If the top hypothesis has risk = "high" → send Slack alert for human review and STOP
7. If risk = "low" or "medium" → proceed to Phase 3

### Phase 3: Experiment (triggered by hypothesis acceptance)

1. Take the top-ranked hypothesis
2. Design the experiment: use `posthog-experiments` to create a feature flag that splits traffic between control (current) and variant (hypothesis change)
3. Implement the variant using the appropriate fundamental (e.g., if the hypothesis is "change email subject line," use `loops-sequences` or `instantly-campaign` to create the B variant)
4. Set the experiment duration: minimum 7 days or until 100+ samples per variant, whichever is longer
5. Log the experiment start in Attio with: hypothesis, start date, expected duration, success criteria

### Phase 4: Evaluate (triggered by experiment completion)

1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt:** Update the live configuration to use the winning variant. Log the change. Move to Phase 5.
   - **Iterate:** Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert:** Disable the variant, restore control. Log the failure. Return to Phase 1 monitoring.
   - **Extend:** Keep the experiment running for another period. Set a reminder.
4. Store the full evaluation (decision, confidence, reasoning) in Attio

### Phase 5: Report (runs weekly via n8n cron)

1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate: net metric change from all adopted changes this week
3. Generate a weekly optimization brief using Claude:
   - What changed and why
   - Net impact on primary KPIs
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post the brief to Slack and store in Attio

## Guardrails (CRITICAL)

- **Rate limit:** Maximum 1 active experiment per play at a time. Never stack experiments.
- **Revert threshold:** If primary metric drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Budget changes >20%
  - Audience/targeting changes that affect >50% of traffic
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 4 per play. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what isn't measured:** If a KPI doesn't have PostHog tracking, fix tracking first (use `posthog-gtm-events` drill) before running experiments on it.

## Output

- Continuous metric monitoring with anomaly alerts
- Automated hypothesis → experiment → evaluation → implementation cycle
- Weekly optimization briefs
- Audit trail of every change, why it was made, and what happened

## When to Stop

The optimization loop runs indefinitely at Durable level. However, it should detect **convergence** — when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments). At convergence:
1. The play has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Report to the team: "This play is optimized. Current performance is [metrics]. Further gains require strategic changes (new channels, new audience, product changes) rather than tactical optimization."
