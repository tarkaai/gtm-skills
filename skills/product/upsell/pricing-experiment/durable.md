---
name: pricing-experiment-durable
description: >
  Pricing Tests — Durable Intelligence. AI agent autonomously detects pricing anomalies,
  generates experiment hypotheses, runs A/B tests, evaluates results, and auto-implements
  winners. Finds and maintains the pricing local maximum.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + continuous autonomous operation over 6 months"
outcome: "NRR sustained or improving over 6 months via autonomous pricing optimization; convergence detected when 3 consecutive experiments produce <2% improvement"
kpis: ["Net revenue retention (NRR) trend", "ARPU trend by plan", "Autonomous experiment velocity", "Win rate (adopted experiments / total experiments)", "Distance from estimated local maximum", "Time to convergence"]
slug: "pricing-experiment"
install: "npx gtm-skills add product/upsell/pricing-experiment"
drills:
  - autonomous-optimization
  - pricing-health-monitor
  - pricing-experiment-runner
---

# Pricing Tests — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An AI agent runs the complete pricing optimization loop autonomously: it monitors pricing KPIs daily, detects anomalies and plateaus, generates hypotheses for what to change, designs and launches experiments, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs and detects convergence — the point where the pricing has reached its local maximum and further tactical experiments yield diminishing returns (<2% improvement for 3 consecutive experiments).

Human involvement is limited to: reviewing high-risk hypotheses (budget changes >20%, audience changes >50%), approving pricing communication copy, and receiving weekly briefs.

## Leading Indicators

- Daily monitoring workflow firing successfully (check n8n execution logs)
- First autonomous hypothesis generated within 7 days of activation
- First autonomous experiment launched within 14 days
- Weekly optimization brief delivered on schedule
- No false-positive anomaly alerts in the first 2 weeks (monitoring calibrated correctly from Scalable data)

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill to wire up the core loop for pricing:

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check pricing KPIs: NRR, ARPU by plan, churn rate by plan, expansion revenue, contraction revenue, usage-to-revenue ratio
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: pull current pricing configuration from Attio (plans, tiers, prices, recent experiment history)
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data + pricing context + experiment history
- Receive 3 ranked hypotheses with expected impact and risk level
- Store hypotheses in Attio as notes on the pricing project record
- If top hypothesis has risk = "high": send Slack alert for human review and STOP
- If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Use the `pricing-experiment-runner` drill to automatically:
  - Create variant Stripe prices from the hypothesis specification
  - Create the PostHog feature flag with proper targeting (segment-specific from Scalable learnings)
  - Build the n8n subscription migration workflow
  - Set experiment duration: minimum 2 billing cycles or until 200+ samples per variant
  - Log experiment start in Attio with hypothesis, start date, expected duration, success criteria
- Guardrails enforced automatically: 1 active experiment per plan, auto-revert if primary metric drops >30%, human approval for high-risk changes, 7-day cooldown after failed experiments, max 4 experiments per month per plan

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` with control vs. variant data
- Decision:
  - **Adopt:** NRR improved at 95% significance. Update live pricing configuration. Migrate remaining control users. Archive old Stripe prices. Log the change with full reasoning.
  - **Iterate:** Directionally positive but not significant. Generate a refined hypothesis building on the result. Return to Phase 2.
  - **Revert:** Treatment performed worse. Disable feature flag, revert subscriptions, log failure. Return to Phase 1. Observe 7-day cooldown.
  - **Extend:** Promising but insufficient sample. Keep experiment running for 1 more billing cycle.
- Store full evaluation (decision, confidence, reasoning, metric deltas) in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on NRR, ARPU, churn
  - Current distance from estimated local maximum
  - Recommended focus for next week
  - Convergence status: are successive experiments yielding diminishing returns?
- Post brief to Slack and store in Attio

### 2. Run always-on pricing health monitoring

Run the `pricing-health-monitor` drill (continuing from Baseline/Scalable) with Durable-level enhancements:

- Pricing health dashboard runs continuously with daily anomaly detection
- Add convergence tracking panels: plot the magnitude of improvement from each successive experiment over time; trend line approaching zero = convergence
- Add competitive pricing panels: if pricing page visitor rate increases without other changes, it may indicate competitor pricing shifts driving comparison shopping
- Monthly calibration continues: adjust anomaly thresholds based on false positive/negative rates

The pricing health monitor feeds anomaly signals directly into the autonomous optimization loop (Phase 1). This is the sensory input for the agent.

### 3. Maintain autonomous experiment execution

The `pricing-experiment-runner` drill operates continuously under the agent's control:

- The agent generates experiment specifications from hypotheses (Stripe price objects, PostHog flag config, targeting rules, guardrail thresholds)
- The agent executes the full experiment lifecycle without human intervention for low/medium risk experiments
- For each completed experiment, the agent updates the experiment history in Attio, which informs future hypothesis generation (avoiding re-testing failed hypotheses, building on successful ones)
- The agent tracks experiment velocity and win rate as meta-KPIs for the optimization system itself

### 4. Detect convergence and report

The autonomous loop runs indefinitely but detects **convergence**: when 3 consecutive experiments on the same pricing dimension produce <2% improvement each.

At convergence:
1. The agent reports: "Pricing for [plan/segment] has reached its local maximum. Current NRR: [X%]. ARPU: [$Y]. Further gains require strategic changes (new plans, new value metrics, market repositioning) rather than tactical price optimization."
2. Reduce monitoring frequency for converged segments from daily to weekly
3. Continue monitoring non-converged segments and plans at daily frequency
4. If market conditions change (competitor pricing shift, usage pattern change, new product features), the agent detects the shift via anomaly detection and re-enters the optimization loop

## Time Estimate

- 8 hours: autonomous optimization loop setup (n8n workflows for all 5 phases, Anthropic API integration for hypothesis generation and evaluation)
- 4 hours: pricing health monitor Durable enhancements (convergence tracking, competitive panels)
- 4 hours: testing the full loop end-to-end with a controlled experiment
- 4 hours: initial calibration over first 2 weeks (tuning anomaly sensitivity, hypothesis quality)
- Ongoing: ~30 min/week for reviewing weekly briefs and approving high-risk hypotheses

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, anomaly detection, dashboards, cohorts | Free up to 1M flag requests/mo; usage-based beyond — [posthog.com/pricing](https://posthog.com/pricing) |
| Stripe | Dynamic price creation, subscription management, billing events | 2.9% + $0.30/txn + 0.7% Billing fee — [stripe.com/pricing](https://stripe.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief generation | Usage-based; ~$15/MTok input, ~$75/MTok output (Claude Sonnet) — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| n8n | All 5 loop phases (monitor, diagnose, experiment, evaluate, report) | Standard stack (excluded) |
| Intercom | Pricing change communication for adopted experiments | $29-132/seat/mo; Proactive Support Plus $99/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Attio | Experiment history, hypothesis tracking, anomaly logs, pricing project records | Standard stack (excluded) |

**Play-specific cost:** ~$100-200/mo (Intercom Proactive Support Plus $99/mo; Anthropic API ~$10-50/mo depending on experiment frequency; PostHog usage-based charges variable)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies > generate hypotheses > run experiments > evaluate results > auto-implement winners > report weekly
- `pricing-health-monitor` — continuous pricing KPI monitoring with anomaly detection that feeds the autonomous optimization loop
- `pricing-experiment-runner` — execute individual pricing experiments under the agent's autonomous control with full Stripe/PostHog/n8n lifecycle management
