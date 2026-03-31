---
name: customer-success-playbooks-durable
description: >
  CS Intervention Playbooks -- Durable Intelligence. The autonomous optimization loop continuously
  monitors playbook performance, detects anomalies, generates improvement hypotheses, runs A/B
  experiments, and auto-implements winners. Playbook-specific health monitoring feeds the loop with
  signal data. Sustained >=55% success rate over 6 months with decreasing cost per save.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained >=55% success rate over 6 months with autonomous optimization converging on local maximum"
kpis: ["Playbook success rate", "Cost per save", "Experiment velocity", "Convergence rate", "Net retention impact"]
slug: "customer-success-playbooks"
install: "npx gtm-skills add product/retain/customer-success-playbooks"
drills:
  - autonomous-optimization
  - cs-playbook-health-monitor
  - churn-model-health-monitor
---

# CS Intervention Playbooks -- Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

The CS playbook system runs autonomously. The `autonomous-optimization` drill continuously monitors all playbook KPIs, detects when metrics plateau or drop, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The `cs-playbook-health-monitor` feeds play-specific signals into the optimization loop. The system converges on the local maximum -- the best possible playbook performance given the current product, audience, and market -- and maintains it as conditions change. Sustained >=55% success rate over 6 months with cost per save trending downward.

## Leading Indicators

- Autonomous optimization loop running without human intervention for 2+ consecutive weeks
- Experiments producing measurable lift (>5% improvement on the target metric) at least 2 out of every 4 experiments
- Convergence signals: successive experiments producing <2% improvement for 3 consecutive experiments on a given playbook (that playbook has reached its local maximum)
- Churn model accuracy sustained >70% (no drift from Scalable-level calibration)
- Weekly optimization briefs generated and posted on schedule
- Cost per save declining quarter over quarter

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on optimization cycle for this play. Configure it with the play's specific KPIs and thresholds:

**Phase 1 -- Monitor (daily via n8n cron):**
The optimization loop uses `posthog-anomaly-detection` to check the play's primary KPIs daily:
- Overall playbook success rate (target: >=55%)
- Per-playbook success rates (flag any playbook dropping >15% below its 4-week average)
- Scenario coverage rate (target: >90%)
- Cost per save (flag if increasing >20% above 4-week average)
- Intervention reach (target: >90% of at-risk users receiving intervention within 24 hours)

Compare last 2 weeks against 4-week rolling average. Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, proceed to Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
The loop gathers context: current playbook configurations, health score model weights, intervention templates, and channel performance data. It pulls 8-week metric history from PostHog and runs `hypothesis-generation` to produce 3 ranked hypotheses.

Example hypotheses the loop might generate:
- "Playbook 'activity-decay' success rate dropped 18% because the reengagement email subject line has been in use for 6 weeks and is fatigued. Expected impact of refreshing: +8-12% success rate. Risk: low."
- "Unmatched at-risk users increased 25% because a product update introduced a new usage pattern the churn model does not recognize. Expected impact of adding a new signal: +5% scenario coverage. Risk: medium."
- "Critical-tier save rate dropped because the Attio task for account owners is not providing enough context for effective calls. Expected impact of enriching task content: +10% critical save rate. Risk: low."

If top hypothesis risk = high, send Slack alert for human review and STOP. Otherwise proceed to Phase 3.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
The loop designs and deploys the experiment. Using `posthog-experiments`, it creates a feature flag splitting at-risk users between control (current playbook) and variant (hypothesis change). Minimum duration: 7 days or 50 interventions per variant, whichever is longer.

Log experiment start in Attio: hypothesis text, start date, expected duration, success criteria, risk level.

**Phase 4 -- Evaluate (triggered by experiment completion):**
Pull experiment results from PostHog. Run `experiment-evaluation` to decide:
- **Adopt:** Variant wins. Update the live playbook configuration. Log the change.
- **Iterate:** Results inconclusive or partial improvement. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Variant performed worse. Restore control. Log the failure. Return to Phase 1.
- **Extend:** Not enough data yet. Continue the experiment for another cycle.

Store full evaluation in Attio: decision, confidence interval, reasoning, net impact.

**Phase 5 -- Report (weekly via n8n cron):**
Generate a weekly optimization brief:
```
# CS Playbook Optimization Brief -- Week of [date]

## What Changed
- [List of experiments completed, decisions made, playbooks updated]

## Net Impact
- Overall success rate: [X%] (change: [+/-Y%] from adopted experiments)
- Cost per save: [$N] (change: [$+/-M])
- Experiments run this week: [N]
- Experiments adopted: [N]
- Experiments reverted: [N]

## Convergence Status
- Playbooks at local maximum (3 consecutive <2% experiments): [list]
- Playbooks still being optimized: [list]
- Estimated distance from local maximum: [assessment]

## Next Week Focus
- [Top hypothesis queued for next experiment]
- [Any playbooks flagged for retirement or creation]
```

Post to Slack and store in Attio.

### 2. Deploy playbook-specific health monitoring

Run the `cs-playbook-health-monitor` drill to build the play-specific signal layer that feeds the optimization loop. This creates:

- A PostHog dashboard with 6 panels tracking per-playbook performance, scenario coverage, step drop-off, and unmatched at-risk users
- A daily n8n workflow that checks playbook metrics against the 4-week rolling average and fires alerts on anomalies
- A weekly playbook health brief identifying the single biggest opportunity for improvement

The health monitor's daily anomaly classifications feed directly into the optimization loop's Phase 1. The weekly brief's "Biggest Opportunity" becomes the starting point for hypothesis generation when no anomaly has triggered the loop.

### 3. Deploy churn model health monitoring

Run the `churn-model-health-monitor` drill to ensure the prediction machinery itself stays accurate. The optimization loop optimizes playbook performance, but if the underlying churn model drifts out of calibration, the entire system degrades:

- Monitor prediction accuracy: true positive rate, false negative rate (most dangerous -- missed churners)
- Detect calibration drift caused by product changes, seasonal effects, or audience shifts
- Trigger model recalibration when false negative rate exceeds 15% or when actual churn rates diverge from predicted by >15 percentage points
- Generate weekly churn intelligence briefs with model accuracy, intervention effectiveness, and recalibration recommendations

### 4. Configure guardrails

Set guardrails that prevent the optimization loop from causing harm:

- **Rate limit:** Maximum 1 active experiment per playbook at a time. Never stack experiments on the same playbook.
- **Revert threshold:** If a playbook's success rate drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Any experiment that changes the escalation path for critical-tier users (these involve human CS reps)
  - Any experiment that changes intervention frequency (could cause alert fatigue)
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same playbook.
- **Maximum experiments per month:** 4 per playbook. If all 4 fail, pause optimization on that playbook and flag for human strategic review.
- **Never optimize what is not measured:** If a playbook does not have complete PostHog event tracking (triggered -> steps -> outcome), fix tracking first before running experiments.

### 5. Detect convergence and maintain the local maximum

The optimization loop runs indefinitely. It should detect convergence on each playbook independently:

When a playbook has 3 consecutive experiments producing <2% improvement:
1. That playbook has reached its local maximum
2. Reduce experiment frequency on that playbook from weekly to monthly
3. Maintain monitoring at daily frequency (to catch external changes that shift the maximum)
4. Report: "Playbook [name] is optimized. Current success rate: [X%]. Further improvement requires strategic changes (product changes, new channels, different audience) rather than tactical optimization."

When ALL playbooks have converged:
1. The play has reached its overall local maximum
2. Reduce the optimization loop frequency from daily to weekly monitoring
3. Generate a convergence report summarizing: final performance by playbook, total experiments run, total lift achieved, cost per save trajectory, and what strategic changes could unlock the next step function improvement
4. Continue monitoring for external shocks (product changes, market shifts, seasonal effects) that could shift the local maximum

### 6. Evaluate sustainability

The Durable level runs continuously. Monthly evaluation:

- Is the overall success rate sustained at >=55%?
- Is cost per save stable or declining?
- Is scenario coverage maintained at >90%?
- Are the monitoring and optimization systems running reliably (no missed daily checks, no stale experiments)?
- Is the churn model still calibrated (prediction accuracy >70%)?

If any metric degrades for 2 consecutive months, the system should self-diagnose: is it an optimization problem (playbooks need improvement), a model problem (churn prediction is drifting), or an external problem (product regression, market shift)?

## Time Estimate

- 15 hours: Deploying and configuring the autonomous optimization loop
- 10 hours: Deploying playbook-specific health monitoring
- 8 hours: Deploying churn model health monitoring
- 5 hours: Configuring guardrails and convergence detection
- 112 hours: Ongoing monitoring, experiment management, and brief review over 6 months (approximately 4-5 hours per week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, feature flags, anomaly detection, dashboards | Free up to 1M events/mo; paid from $0/mo + usage; https://posthog.com/pricing |
| Attio | CRM for health scores, experiment logging, intervention tracking, briefs | Free for small teams; https://attio.com/pricing |
| Intercom | In-app messaging for intervention delivery and NPS surveys | From $39/seat/mo; https://www.intercom.com/pricing |
| Loops | Email sequences for multi-step intervention playbooks | Free up to 1K contacts; https://loops.so/pricing |
| n8n | Workflow automation for optimization loop, scoring, routing, monitoring | Free self-hosted; cloud from $20/mo; https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | Usage-based; https://www.anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` -- the core optimization loop that detects anomalies, generates hypotheses, runs experiments, evaluates results, and auto-implements winners. This is what makes Durable fundamentally different from Scalable.
- `cs-playbook-health-monitor` -- play-specific monitoring that tracks per-playbook performance, scenario coverage, and step drop-off. Feeds signals to the optimization loop.
- `churn-model-health-monitor` -- monitors prediction accuracy and calibration drift to ensure the churn scoring model stays reliable under the optimization loop.
