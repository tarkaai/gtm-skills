---
name: health-score-dashboard-durable
description: >
  Account Health Scoring — Durable Intelligence. Autonomous AI agent continuously optimizes the
  health score model (weights, signals, thresholds) and intervention strategies. Detects model
  drift, runs experiments to improve prediction accuracy and recovery rates, and generates weekly
  optimization briefs. Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving >=75% prediction accuracy and >=25% recovery rate over 6 months via autonomous optimization"
kpis: ["Prediction accuracy (trailing 30d)", "Intervention recovery rate", "Model drift detection", "Experiment velocity", "Net retention lift vs pre-health-score baseline"]
slug: "health-score-dashboard"
install: "npx gtm-skills add product/retain/health-score-dashboard"
drills:
  - autonomous-optimization
  - health-score-alerting
  - nps-feedback-loop
---
# Account Health Scoring — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Hand the health scoring system to an autonomous AI agent that continuously monitors, diagnoses, experiments, and improves. The agent detects when the model drifts (prediction accuracy drops), generates hypotheses for why (new customer segments, product changes, seasonal patterns), runs A/B experiments on model adjustments and intervention strategies, and auto-implements winners. The system finds its local maximum and maintains it as conditions change.

**Pass threshold:** Sustained or improving >=75% prediction accuracy AND >=25% intervention recovery rate over 6 months, with the autonomous optimization loop running continuously.

## Leading Indicators

- Autonomous optimization loop runs daily monitoring without errors for 30+ consecutive days
- At least 2 experiments per month generated and evaluated by the agent
- Model drift detected within 7 days when accuracy drops below 75%
- Weekly optimization briefs produced every Monday without manual triggering
- Convergence detected after successive experiments produce <2% improvement

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the health score system. The optimization loop targets these metrics:

**Primary metric:** Prediction accuracy — percentage of accounts that churned, downgraded, or escalated that were flagged At Risk or Critical at least 14 days before the event.

**Secondary metrics:**
- Intervention recovery rate (accounts that improved after intervention)
- False positive rate (accounts flagged At Risk that were actually fine)
- Time from risk detection to intervention delivery
- Net retention rate improvement vs pre-health-score baseline

Configure the five phases of the optimization loop:

**Phase 1 — Monitor (daily via n8n):**
Use `posthog-anomaly-detection` to check health score system KPIs daily:
- Pull prediction accuracy for the trailing 30-day window
- Compare to 4-week rolling average
- Pull intervention recovery rate for the trailing 30-day window
- Check false positive rate
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
When prediction accuracy drops or recovery rate declines, the agent investigates:
- Has the customer base composition changed? (New segments with different usage patterns)
- Has the product changed? (New features added, old features deprecated, onboarding flow changed)
- Have dimension weights drifted? (Usage is no longer the strongest predictor)
- Are intervention messages stale? (The same copy has been running for months)
- Is there seasonal pattern? (Usage naturally dips in certain months)

Use `hypothesis-generation` with the anomaly data, recent product changes, and customer composition data. Receive 3 ranked hypotheses with expected impact.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Take the top hypothesis and design an experiment:

*Model experiments (if the hypothesis is about scoring accuracy):*
- Adjust dimension weights (e.g., increase adoption weight from 20% to 30%)
- Add or remove a signal from a dimension (e.g., add "API usage" to engagement)
- Change the risk tier thresholds (e.g., At Risk boundary from 40 to 45)
- Score a subset of accounts with the new model in parallel and compare predictions

*Intervention experiments (if the hypothesis is about recovery rate):*
- Test new message copy, sender, timing, or channel
- Use PostHog feature flags to split accounts into control (current intervention) and variant (new intervention)
- Run for 4+ weeks to accumulate sufficient data

Use `posthog-experiments` to set up each experiment with clear success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**
Use `experiment-evaluation` to analyze results:
- **Adopt:** If the variant produces statistically significant improvement (95% confidence, >2% lift), implement it as the new default. Update model weights in the n8n pipeline or update intervention templates.
- **Iterate:** If results are promising but not significant, generate a refined hypothesis building on this result.
- **Revert:** If the variant performs worse, restore the control configuration. Log the learning.
- **Extend:** If sample size is insufficient after the planned duration, extend by 2 weeks.

**Phase 5 — Report (weekly via n8n):**
Generate a weekly optimization brief:

```
# Health Score Optimization Brief — Week of [date]

## System Health
- Prediction accuracy (30d): [X%] (target: >=75%)
- Recovery rate (30d): [X%] (target: >=25%)
- False positive rate: [X%] (target: <=25%)
- Accounts scored: [N]
- Risk distribution: Healthy [N] | Monitor [N] | At Risk [N] | Critical [N]

## This Week's Activity
- Anomalies detected: [N] ([list])
- Experiments in flight: [N] ([names])
- Experiments completed: [N] ([results])
- Model changes implemented: [list or "none"]

## Model Performance Trend
| Metric | 4 Weeks Ago | 2 Weeks Ago | This Week | Trend |
|--------|-------------|-------------|-----------|-------|
| Accuracy | [X%] | [X%] | [X%] | [arrow] |
| Recovery | [X%] | [X%] | [X%] | [arrow] |
| False Pos | [X%] | [X%] | [X%] | [arrow] |

## Top Interventions (by recovery rate)
1. [Intervention type] — [X%] recovery ([N] accounts)
2. [Intervention type] — [X%] recovery ([N] accounts)

## Convergence Status
[If <2% improvement for 3 consecutive experiments: "CONVERGED — model is at local maximum. Further gains require strategic changes (new product features, new customer segments, or new data sources)."]
[Otherwise: "OPTIMIZING — [N] experiments remaining in current cycle."]

## Next Steps
[Agent's planned actions for next week]
```

Post to Slack, store in Attio.

### 2. Configure health-based interventions for long-term operation

Run the `health-score-alerting` drill in maintenance mode. At Durable level, the intervention system should be self-tuning:

- Intervention templates are refreshed quarterly by the agent (detect when engagement rates drop below historical averages, draft new copy, A/B test it)
- Rate limiting adjusts based on account volume (as customer base grows, ensure intervention capacity scales)
- Tier thresholds adjust based on experiment results (the agent may discover that intervening at score 50 instead of 40 produces higher recovery rates)

### 3. Add qualitative signal via NPS

Run the `nps-feedback-loop` drill to add qualitative health data to the scoring model:

- NPS score becomes a signal in the Engagement dimension. Promoters (9-10) add points, detractors (0-6) subtract points.
- NPS survey timing is coordinated with health scores: do NOT survey accounts that are currently At Risk or Critical (they know something is wrong — surveying them wastes goodwill). Survey Healthy and Monitor accounts.
- Feed NPS open-text responses into the diagnosis phase: when the agent investigates why engagement scores are declining across the base, detractor comments provide qualitative context.

### 4. Implement guardrails

- **Rate limit:** Maximum 1 active model experiment at a time. Never run a model change experiment and an intervention experiment simultaneously on the same accounts.
- **Revert threshold:** If prediction accuracy drops below 60% at any point, auto-revert the last model change and alert the team.
- **Human approval required for:**
  - Changing dimension weights by more than 10 percentage points
  - Adding or removing an entire dimension
  - Changing the risk tier boundaries by more than 10 points
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing a new hypothesis on the same dimension or intervention tier.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Staleness alert:** If the agent has not run a successful experiment in 6 weeks, alert the team. Either the model has converged or the agent is stuck.

### 5. Evaluate sustainability

This level runs continuously. Monthly review:

- Is prediction accuracy sustained at >=75%?
- Is intervention recovery rate sustained at >=25%?
- Is net retention improving compared to the pre-health-score baseline?
- Has the agent detected convergence? If so, reduce monitoring frequency from daily to weekly and focus agent compute on other plays.

If metrics decay below thresholds for 2 consecutive months, the agent diagnoses whether the cause is model drift (fixable with recalibration) or fundamental change (requires strategic product or GTM changes beyond what optimization can address). Report findings to the team with specific recommendations.

## Time Estimate

- 20 hours: Deploy autonomous optimization loop and configure all 5 phases
- 10 hours: Connect NPS feedback to health scoring
- 10 hours: Implement guardrails and rate limiting
- 80 hours: Ongoing agent compute over 6 months (daily monitoring, hypothesis generation, experiment management, weekly briefs)
- 20 hours: Monthly human review and strategic adjustments (4 hours x 5 months)
- 10 hours: Convergence assessment and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data, dashboards, experiments, anomaly detection | Free tier (1M events/mo) or Growth $0/mo + usage — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Account records, score storage, intervention tasks | Free tier or existing plan — [attio.com/pricing](https://attio.com/pricing) |
| n8n | Scoring pipeline, optimization loop, alerting | Self-hosted free or Cloud from EUR 20/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | In-app interventions + NPS surveys | Starter $74/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered intervention emails | Free tier or Starter $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Claude API (Anthropic) | Hypothesis generation, experiment evaluation, brief writing | ~$10-30/mo based on query volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost:** ~$100-175/mo (Intercom + Loops + Claude API compute)

## Drills Referenced

- `autonomous-optimization` — The core optimization loop: monitor, diagnose, experiment, evaluate, report. This is what makes Durable fundamentally different from Scalable.
- `health-score-alerting` — Maintains the intervention routing system and self-tunes intervention strategies
- `nps-feedback-loop` — Adds qualitative NPS data as a signal dimension and coordinates survey timing with health scores
