---
name: engagement-scoring-durable
description: >
  User Engagement Scoring — Durable Intelligence. The autonomous optimization loop monitors
  scoring accuracy, recalibrates dimension weights, experiments on intervention strategies,
  and self-corrects as user behavior evolves. The agent finds the local maximum of churn
  prediction and re-engagement performance, then maintains it.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving churn prediction accuracy >=70% and re-engagement rate >=15% over 6 months via autonomous agent optimization"
kpis: ["Churn prediction accuracy (trailing 60-day back-test, monthly)", "Re-engagement rate (trailing 30-day, monthly)", "Model stability (weight change <5% for 3+ consecutive months = converged)", "Experiment velocity (experiments run per month)", "AI lift (accuracy improvement from agent-driven weight tuning vs static weights)"]
slug: "engagement-scoring"
install: "npx gtm-skills add product/retain/engagement-scoring"
drills:
  - autonomous-optimization
  - engagement-score-computation
---

# User Engagement Scoring — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The engagement scoring system operates autonomously. An always-on agent loop monitors scoring accuracy, recalibrates dimension weights when prediction accuracy drifts, runs experiments on intervention strategies, evaluates results, and auto-implements winners. The system self-corrects as user behavior evolves with product changes, market shifts, and user base composition changes.

Over 6 months, the agent maintains or improves:
- Churn prediction accuracy at 70%+ (back-tested monthly)
- Re-engagement rate at 15%+ for At Risk users receiving interventions
- Model convergence: when 3 consecutive monthly weight recalibrations produce <5% change, the model has found its local maximum

The Durable level is fundamentally different from Scalable because the agent optimizes the system itself, not just the outputs. It changes the scoring weights, the intervention timing, the messaging, and the tier thresholds based on measured outcomes.

## Leading Indicators

- The `autonomous-optimization` loop fires daily monitoring checks without human intervention
- Monthly weight recalibration runs complete with documented accuracy deltas
- At least 1 experiment per month is designed, run, and evaluated by the agent
- Weekly optimization briefs are generated and posted to Slack
- When the agent detects accuracy drops, it generates hypotheses and initiates corrective experiments within 48 hours
- Convergence detection: the agent identifies when successive experiments produce <2% improvement and shifts to maintenance mode

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the engagement scoring play:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs: churn prediction accuracy, re-engagement rate, false positive rate, intervention coverage
2. Compare the last 2 weeks against the 4-week rolling average
3. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal, log to Attio. No action needed.
5. If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Pull 8-week metric history from PostHog
2. Identify which KPI is anomalous and which dimension or intervention channel is the root cause
3. Run `hypothesis-generation` with the anomaly context
4. Receive 3 ranked hypotheses: e.g., "recency dimension weight is too low after product shipped a new daily-use feature," "re-engagement email subject line has fatigued after 4 months," "user base shifted toward enterprise accounts that have different engagement patterns"
5. If top hypothesis is high risk (requires changing tier thresholds affecting 50%+ of users), send Slack alert for human review and STOP
6. If low or medium risk, proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags to split users between control (current configuration) and variant (hypothesis change)
2. Implement the variant: if the hypothesis targets scoring weights, create a parallel scoring computation with adjusted weights; if it targets interventions, create a variant message or timing
3. Set experiment duration: minimum 14 days or 200+ users per variant
4. Log experiment start in Attio

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`:
   - **Adopt:** Update the live configuration. Log the change.
   - **Iterate:** Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Disable the variant. Log the failure. Return to Phase 1.
3. Store full evaluation in Attio (decision, confidence, reasoning, metric deltas)

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on churn prediction accuracy and re-engagement rate
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Deploy engagement score weight tuning

Run the the engagement score weight tuning workflow (see instructions below) drill to automate monthly model recalibration:

1. Build the outcome-labeled dataset: label each user as Churned, Expanded, Retained, or Declined based on their 60-day outcome
2. Measure each dimension's separation score (how well it predicts churn in isolation)
3. Compute optimal weights proportional to predictive power, with constraints (no dimension >40%, none <10%)
4. Back-test the proposed new weights against historical data
5. If new weights improve accuracy by 5%+ points, deploy them to the live scoring pipeline
6. If weights have not changed for 2 consecutive months, trigger hypothesis generation for new signal discovery
7. Track weight history, accuracy history, and false positive rate on the engagement scoring dashboard

### 3. Maintain the scoring pipeline

Run the `engagement-score-computation` drill in maintenance mode:

1. The daily n8n workflow continues computing scores for all active users
2. When the the engagement score weight tuning workflow (see instructions below) drill produces new weights, update the computation workflow automatically
3. Monitor for pipeline failures: if the scoring workflow misses a day, alert and re-run
4. As the user base grows, scale the pipeline: batch queries, parallel processing, error retry logic
5. When PostHog events or product features change, update the engagement event taxonomy and re-validate dimension queries

### 4. Implement convergence detection

Configure the agent to detect when the scoring system has reached its local maximum:

1. Track the accuracy improvement from each monthly weight recalibration
2. Track the re-engagement improvement from each A/B experiment on interventions
3. When 3 consecutive experiments produce <2% improvement:
   - The play has converged. Log: "Engagement scoring model is optimized. Current accuracy: [X]%. Re-engagement rate: [Y]%. Further improvement requires strategic changes (new product features, new engagement signals, different intervention channels)."
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment cadence from monthly to quarterly
   - Shift agent focus to anomaly detection and maintaining current performance

### 5. Evaluate sustainability

This level runs continuously. Monthly review:

1. Run the 60-day back-test: is churn prediction accuracy still 70%+?
2. Check re-engagement rates: still 15%+?
3. Review the agent's weekly briefs: are experiments producing gains or has the system converged?
4. Check for environmental shifts: has the product launched major new features that require new engagement signals? Has the user base composition changed (more/fewer enterprise accounts)?

If metrics sustain or improve over 6 months via agent-driven optimization, the play is durable.

If metrics decay despite agent optimization, the system needs strategic input:
- New engagement dimensions (the current 4 may not capture new product behaviors)
- New intervention channels (maybe SMS or push notifications outperform email)
- Segmented models (enterprise and self-serve users may need different scoring models)

## Time Estimate

- 20 hours: Deploy and configure the autonomous optimization loop (step 1)
- 15 hours: Deploy weight tuning automation (step 2)
- 10 hours: Pipeline maintenance and scaling over 6 months (step 3)
- 5 hours: Convergence detection configuration (step 4)
- 100 hours: Ongoing agent monitoring, experiment cycles, brief generation over 6 months (step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring queries, experiments, anomaly detection, dashboards | Free tier: 1M events/mo. https://posthog.com/pricing |
| n8n | Daily scoring, optimization loop, weight tuning automation | Free (self-hosted) or $20/mo (cloud). https://n8n.io/pricing |
| Attio | Score storage, experiment logging, optimization audit trail | Free tier: 3 users. https://attio.com/pricing |
| Intercom | In-app intervention messages | Starter: ~$74/mo. https://www.intercom.com/pricing |
| Loops | Re-engagement email interventions | Free tier: 1,000 contacts. https://loops.so/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs | Pay-per-use: ~$15/MTok input, ~$75/MTok output (Claude Sonnet). https://www.anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` -- the core detect-diagnose-experiment-evaluate-report loop that makes Durable fundamentally different from Scalable
- the engagement score weight tuning workflow (see instructions below) -- monthly automated recalibration of scoring dimension weights based on prediction accuracy back-tests
- `engagement-score-computation` -- the daily scoring pipeline maintained and updated by the optimization loop
