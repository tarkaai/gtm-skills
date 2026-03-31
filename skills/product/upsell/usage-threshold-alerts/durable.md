---
name: usage-threshold-alerts-durable
description: >
  Plan Limit Notifications — Durable Intelligence. Autonomous agent loop that monitors alert
  system metrics, detects when conversion rates plateau or detection accuracy drifts, generates
  improvement hypotheses, runs experiments on thresholds and messaging, and auto-implements
  winners. Converges when successive experiments produce <2% improvement.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving upgrade rate ≥35% over 6 months via autonomous optimization"
kpis: ["Upgrade rate from alerted users", "Revenue from alert-driven upgrades (trailing 30d)", "Detection true positive rate", "Upgrade 30-day retention", "Experiment velocity", "AI lift vs. Scalable baseline"]
slug: "usage-threshold-alerts"
install: "npx gtm-skills add product/upsell/usage-threshold-alerts"
drills:
  - autonomous-optimization
  - usage-alert-delivery
---

# Plan Limit Notifications — Durable Intelligence

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The alert system operates autonomously. An always-on agent loop monitors detection accuracy, alert conversion rates, and revenue impact. When any metric plateaus, declines, or spikes, the agent diagnoses the cause, generates improvement hypotheses, designs and runs A/B experiments, evaluates results, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement — the alert system has found its local maximum for the current product and pricing structure.

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 1 experiment per month is auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted to Slack
- Detection accuracy (true positive rate) stays above 65% without manual recalibration
- No manual threshold adjustments needed — the agent handles drift from product changes, pricing updates, and seasonal usage patterns
- Guardrail alerts fire correctly when tested (simulated metric drop triggers the expected response)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the usage threshold alerts play. The optimization loop has 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent queries the `autonomous-optimization` drill's webhook endpoint to retrieve current metrics: upgrade conversion rate, detection true positive rate, false positive rate, revenue impact, alert volume, and upgrade retention. It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current detection thresholds, alert templates, routing rules, A/B test history from Scalable, 8-week metric trends. It runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples specific to this play:

- "Lower the imminent threshold from 85% to 80% for API-call alerts — conversion rate for this resource dropped 15% after a product update that increased per-request API consumption, meaning users hit limits faster than before"
- "Switch critical-tier email template from urgency-focused to value-focused — the current template's open rate declined 20% over 6 weeks, suggesting users have become desensitized to urgency messaging"
- "Add a new detection signal: billing page visits by non-billing-admin users — 40% of recent self-serve upgraders visited the billing page 2-3 times before upgrading, suggesting intent to upgrade that the current system does not capture"
- "Adjust velocity calculation to use 14-day window instead of 7-day — seasonal patterns in API usage are causing a 35% false positive spike at month boundaries"

If the top hypothesis is high-risk (affects >50% of alert volume or changes detection thresholds by >20%), the agent sends a Slack alert and waits for human approval before proceeding.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent implements the experiment using PostHog feature flags. It splits traffic between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 7 days or 100 alerted accounts per variant, whichever is longer.

For detection experiments (threshold or velocity changes): the agent creates a variant detection configuration that runs in parallel. Flagged accounts from both configurations are tracked, but only control-config alerts are sent. After the experiment period, compare which configuration had better true positive rates and projected conversion.

For messaging experiments (template copy, format, timing): the agent creates variant templates in Intercom or Loops and routes a random subset of alerted users to the variant. Measure upgrade rate, click-through rate, and sentiment (support ticket volume).

For routing experiments (channel mix, MRR thresholds for sales involvement): the agent modifies routing rules for the variant group and measures upgrade rate, time-to-upgrade, and upgrade retention.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` to decide:
- **Adopt:** Update the live configuration to use the winning variant. Log the change in Attio with full context.
- **Iterate:** The result was directionally positive but not conclusive. Generate a refined hypothesis and return to Phase 2.
- **Revert:** The variant hurt performance. Disable the variant, restore control, log the failure, and return to Phase 1.
- **Extend:** Insufficient data. Keep the experiment running for another period.

Every decision is stored in Attio with: hypothesis text, experiment parameters, results (conversion rate delta, confidence interval), and reasoning.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net metric change from all adopted changes
- Current performance vs. Scalable baseline (AI lift)
- Revenue impact: MRR from alert-driven upgrades this week and trailing 30 days
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure play-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add alert-system-specific safeguards:

- **Alert fatigue guard:** If the average user receives more than 2 usage alerts per month across all resources, pause the lowest-converting resource alerts and flag for review. Users should feel helped, not nagged.
- **False positive spike:** If the false positive rate exceeds 35% for 2 consecutive weeks, pause all experiments and revert detection thresholds to the last known good configuration. Investigate whether a product change altered consumption patterns.
- **Upgrade retention guard:** If 30-day retention of alert-driven upgraders drops below 70%, pause urgency-focused messaging experiments. Pressure upgrades that lead to downgrades destroy LTV. Switch experiment focus to value-based messaging.
- **Support ticket correlation:** If support tickets mentioning "billing," "limit," or "upgrade" increase >50% week over week coinciding with an active experiment, auto-revert the experiment immediately.
- **Revenue sanity check:** If alert-driven upgrade MRR drops >25% week over week with no corresponding drop in alert volume, something is broken in the upgrade flow. Pause experiments and alert the team.

### 3. Deploy the alert health monitor at Durable cadence

Run the `autonomous-optimization` drill with Durable-level configuration:

- Health check: runs daily (detection accuracy, delivery success, conversion funnel)
- Detection accuracy recalibration: runs weekly instead of monthly (the autonomous loop needs faster feedback)
- Upgrade retention tracking: runs weekly with 30-day and 90-day cohort analysis
- Weekly health report: integrates with the `autonomous-optimization` weekly brief as a subsection

The health monitor feeds data to the autonomous optimization loop via its webhook endpoint. When it detects drift — detection accuracy declining, conversion rate plateauing, retention dropping — that becomes an anomaly that triggers the optimization cycle.

### 4. Maintain alert delivery at Durable level

The `usage-alert-delivery` drill continues to run daily. The autonomous optimization loop may modify:
- Detection thresholds (what percentage triggers each urgency tier)
- Alert copy (Intercom templates, Loops email content)
- Routing rules (channel selection, MRR thresholds for sales routing)
- Timing (alert cadence, cooldown periods, follow-up sequence delays)

The delivery system executes whatever the current best configuration is. Each configuration change is version-controlled in Attio so the agent can revert to any previous state.

### 5. Detect convergence

The autonomous optimization loop monitors experiment outcomes for convergence. When 3 consecutive experiments produce <2% improvement on the primary KPI (upgrade conversion rate):

1. The alert system has reached its local maximum for the current product and pricing structure
2. Reduce experiment frequency from continuous to monthly maintenance checks
3. Generate a convergence report: current performance levels, total improvement since Durable started, total revenue impact, recommended strategic changes for further gains

Strategic changes that could break convergence and unlock further improvement (these require human decision-making, not agent optimization):
- New plan tier or pricing restructure
- New metered resource added to the product
- New alert channel (push notifications, SMS, Slack)
- Fundamental product change that alters usage patterns

When any strategic change occurs, the agent re-activates the full optimization loop to find the new local maximum.

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Upgrade rate: sustained at or above 35% across all alerted accounts, or improving
- Revenue impact: alert-driven MRR maintained or growing month over month
- Detection accuracy: true positive rate above 65% with no sustained drops
- Upgrade retention: 30-day retention above 80% for alert-driven upgraders
- Experiment velocity: at least 2 experiments per month during active optimization
- AI lift: measurable improvement attributable to autonomous optimization vs. the Scalable-level static configuration

This level runs continuously. Review monthly: what improved, what converged, what external factors changed.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations)
- 10 hours: configure play-specific guardrails and test them (simulate metric drops, verify correct responses)
- 10 hours: enhance health monitor for Durable cadence and integrate with optimization loop
- 80 hours: ongoing monitoring, hypothesis review, guardrail management over 6 months (~3 hours/week)
- 20 hours: monthly strategic reviews, convergence analysis, and report generation
- 10 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards, funnels | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation, experiment evaluation, weekly briefs | ~$50-150/mo at Durable scale — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Intercom | In-app alerts (templates modified by optimization loop) | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email alerts and sequences (modified by optimization loop) | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Detection, routing, optimization loop scheduling | Free self-hosted; Cloud from EUR 24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | Expansion deals, experiment audit trail, configuration versioning | Free up to 3 seats; from $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost: $150-400/mo** (Anthropic API for optimization + Loops + Intercom + increased PostHog events)

## Drills Referenced

- `autonomous-optimization` — the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for alert conversion and revenue
- `autonomous-optimization` — monitors detection accuracy, conversion rates, upgrade retention, and system health; feeds metrics to the optimization loop
- `usage-alert-delivery` — executes the current best alert configuration, updated by the optimization loop as experiments produce winners
