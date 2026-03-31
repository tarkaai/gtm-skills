---
name: poc-management-framework-durable
description: >
  POC Management Framework — Durable Intelligence. Always-on AI agents optimize POC
  structures, criteria, interventions, and timing through continuous experimentation.
  The autonomous-optimization loop finds the local maximum for POC-to-close conversion.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: "Sustained or improving POC conversion rates over 6 months via autonomous AI-driven optimization of POC structure, criteria, and interventions"
kpis: ["POC-to-close conversion rate", "POC success prediction accuracy", "Intervention effectiveness rate", "Average time to POC completion", "Optimization experiment win rate"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
drills:
  - autonomous-optimization
---

# POC Management Framework — Durable Intelligence

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Outcomes

The POC management system runs autonomously. AI agents continuously monitor POC metrics, detect when performance plateaus or drops, generate hypotheses for improvement, run controlled experiments, and auto-implement winners. The `autonomous-optimization` drill governs the core loop. `autonomous-optimization` provides weekly strategic insight. The system converges on the local maximum for POC-to-close conversion and sustains it as market conditions change.

## Leading Indicators

- Anomaly detection fires within 24 hours of any KPI shift exceeding 10%
- At least 1 optimization experiment running at all times (unless converged)
- Experiment cycle time under 14 days from hypothesis to decision
- Prediction accuracy above 70% for POC outcome forecasting
- Weekly intelligence reports generating with data-backed structural recommendations
- Optimization briefs showing cumulative improvement trend

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the POC management play. This creates the 5-phase always-on loop:

**Phase 1 — Monitor (daily via n8n cron):**
Use `posthog-anomaly-detection` to check the play's primary KPIs daily:
- POC-to-close conversion rate
- Average criteria achievement rate
- POC completion rate
- Average time to decision
- Intervention effectiveness rate

Compare the last 2 weeks against the 4-week rolling average. Classify each KPI: normal (within 10%), plateau (less than 2% change for 3+ weeks), drop (greater than 20% decline), spike (greater than 50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
Gather context: pull the current POC configuration from Attio (default criteria templates, duration settings, intervention thresholds, qualification criteria). Pull 8-week metric history from PostHog. Run `hypothesis-generation` with the anomaly data and context. Receive 3 ranked hypotheses. Example hypotheses for this play:
- "Reducing default POC duration from 14 to 10 days will maintain criteria achievement while compressing the sales cycle"
- "Adding a day-3 proactive check-in call (instead of waiting for mid-point) will improve milestone completion by 15%"
- "Tightening POC qualification criteria (require 3+ use cases instead of 2) will improve close rate by reducing low-intent POCs"
- "Changing the first milestone to a collaborative exercise (instead of solo) will increase engagement scores in the first 3 days"

If the top hypothesis is high-risk (affects 50%+ of POC pipeline or changes qualification criteria), send a Slack alert for human review and pause. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Use `posthog-experiments` to create an A/B test. Split new POCs into control (current configuration) and variant (hypothesis change). Set minimum sample size: 15 POCs per variant or 4 weeks, whichever comes first. Log the experiment in Attio with hypothesis, start date, expected duration, and success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**
Run `experiment-evaluation` with control vs. variant data. Decision tree:
- **Adopt**: Variant outperforms control with statistical significance. Update the default POC configuration. Log the change with before/after metrics.
- **Iterate**: Results inconclusive but directionally positive. Generate a refined hypothesis and return to Phase 2.
- **Revert**: Variant underperforms. Restore control, log the failure, return to Phase 1 monitoring.
- **Extend**: Not enough data yet. Keep running for another cycle.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week
- Experiments running: status, preliminary results
- Experiments completed: decisions made, net impact
- Cumulative optimization impact since Durable started
- Estimated distance from local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Deploy POC intelligence reporting

Run the `autonomous-optimization` drill. This generates weekly strategic reports that complement the optimization loop:

**POC structure effectiveness analysis:** Compare outcomes across POC configurations (duration, criteria count, support model, industry segment). Identify which configurations produce the highest win rates and shortest sales cycles. Recommend structural changes.

**Prediction accuracy tracking:** For every completed POC, compare the risk score prediction at mid-point to the actual outcome. Track rolling accuracy rate. If accuracy drops below 65% for 2 consecutive weeks, flag the predictive model for retraining.

**Optimization hypothesis generation:** Extract structural recommendations from the intelligence report and format them as hypotheses for the autonomous optimization loop. This creates a feedback cycle: intelligence reporting surfaces strategic opportunities, and autonomous optimization tests them experimentally.

### 3. Configure POC-specific guardrails

Add these guardrails to the autonomous optimization configuration:

- **Rate limit**: Maximum 1 active experiment per POC variable at a time. Never test duration AND criteria simultaneously.
- **Revert threshold**: If POC-to-close conversion drops more than 15% during an experiment, auto-revert immediately and alert the team.
- **Human approval required for**:
  - Changes to POC qualification criteria (affects which deals get POCs)
  - Changes to success criteria templates (affects what prospects are evaluated against)
  - Any experiment the hypothesis generator flags as high-risk
- **Cooldown**: After a failed experiment, wait 14 days before testing the same variable again. POCs are slower than email campaigns; give the pipeline time to cycle.
- **Maximum experiments per month**: 2 per variable. If both fail, pause and flag for strategic review.
- **Never experiment on active POCs**: Experiments only apply to newly initiated POCs. Never change the rules mid-POC for an active prospect.

### 4. Build the convergence detection system

The optimization loop should detect when the play has reached its local maximum:

1. Track the cumulative improvement from all adopted experiments.
2. If 3 consecutive experiments produce less than 2% improvement each, declare convergence.
3. At convergence:
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment cadence to 1 per month (maintenance experiments)
   - Generate a convergence report: "POC management is optimized. Current performance: {metrics}. Further gains require strategic changes (new product features, new market segments, new pricing models) rather than tactical POC optimization."
4. Continue monitoring for external disruptions (market changes, competitor moves, product changes) that could shift the local maximum.

### 5. Evaluate sustainability

This level runs continuously. Monthly review:
- Is POC-to-close conversion sustaining or improving vs. the Scalable baseline?
- Are experiments producing actionable results?
- Is prediction accuracy trending upward?
- Is the system detecting and responding to market changes?

If metrics decay for 2+ consecutive months, diagnose: is it market saturation (same prospects seeing repeat POCs), criteria drift (criteria no longer align with prospect needs), or competitive pressure (competitors offering better evaluations)?

## Time Estimate

- Autonomous optimization setup: 16 hours
- Intelligence reporting setup: 12 hours
- Guardrail configuration: 4 hours
- Convergence detection: 4 hours
- Monthly monitoring and refinement: 8 hours/month x 6 months = 48 hours
- Experiment review and decisions: 4 hours/month x 6 months = 24 hours
- Strategic reviews (quarterly): 8 hours x 2 = 16 hours
- Total: ~160 hours over 6 months (front-loaded; decreases as system converges)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, experiment tracking, POC configuration storage | Pro from $29/user/mo |
| PostHog | Anomaly detection, experiments, dashboards, cohorts | Growth from $0 (usage-based) |
| n8n | Optimization loop scheduling, intervention workflows | Cloud from $24/mo; self-hosted free |
| Anthropic API | Hypothesis generation, experiment evaluation, intelligence reports | ~$15-40/mo |
| Loops | Intervention emails, check-in sequences | Starter from $49/mo |
| Intercom | In-app intervention messages | Starter from $39/mo |
| Cal.com | Dynamic check-in scheduling | Team from $12/user/mo |
| Clay | Ongoing prospect enrichment for auto-provisioning | Explorer from $149/mo |

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum for POC-to-close conversion
- `autonomous-optimization` — weekly strategic reports correlating POC usage patterns with deal outcomes, tracking prediction accuracy, and surfacing structural optimization opportunities
