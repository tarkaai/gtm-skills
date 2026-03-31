---
name: onboarding-experiment-durable
description: >
  Onboarding A/B Tests — Durable Intelligence. AI agents autonomously monitor
  onboarding health, generate experiment hypotheses, run A/B tests, evaluate
  results, and implement winners. Converges on the local maximum activation rate
  and maintains it as user mix and product evolve.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "60 hours over 6 months"
outcome: "Activation rate sustained or improving for 6 months via autonomous optimization; <2% improvement from 3 consecutive experiments signals convergence"
kpis: ["Activation rate (rolling 4-week)", "Autonomous experiment velocity (per month)", "Cumulative lift from auto-adopted experiments", "Time from anomaly detection to experiment launch", "Convergence score (% improvement from last 3 experiments)"]
slug: "onboarding-experiment"
install: "npx gtm-skills add product/onboard/onboarding-experiment"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
  - onboarding-experiment-orchestration
---

# Onboarding A/B Tests — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

AI agents run the full onboarding optimization loop autonomously: monitor activation metrics for anomalies, diagnose root causes, generate experiment hypotheses, run A/B tests, evaluate results, and implement winners — all without human intervention for standard operations. The system converges on the local maximum activation rate and sustains it as the user mix, product features, and competitive landscape change. When 3 consecutive experiments produce < 2% improvement, the play has reached its local maximum and the agent shifts from active optimization to maintenance monitoring.

## Leading Indicators

- The autonomous-optimization loop completes its first full cycle (anomaly detected, hypothesis generated, experiment launched, result evaluated, decision implemented) within the first 2 weeks
- Onboarding health monitor detects and correctly classifies an anomaly within 24 hours of it occurring (validated against manual review)
- The agent generates a hypothesis that a human reviewer rates as "reasonable" for 4 out of 5 generated hypotheses (hypothesis quality is high enough to trust automated experimentation)
- Time from anomaly detection to experiment launch is < 48 hours (the system is responsive, not just monitoring)
- No high-risk change is implemented without human approval (guardrails are working)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This creates the core always-on agent loop:

**Phase 1 — Monitor (daily via n8n cron):**
- PostHog anomaly detection checks all onboarding KPIs: activation rate (overall and per-persona), tour completion rate, email engagement, time to activation
- Compares last 2 weeks against 4-week rolling average
- Classifies: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- Normal: log to Attio, no action
- Anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current onboarding configuration, per-persona funnels, recent experiment history
- Pull 8-week metric history from PostHog
- Run hypothesis-generation with anomaly data + context
- Receive 3 ranked hypotheses with expected impact and risk
- High risk: send Slack alert for human review, STOP
- Low/medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Take the top hypothesis
- Create PostHog experiment with feature flag (50/50 split, new users only)
- Implement the variant using the appropriate tool (Intercom tour, Loops email, product code)
- Set minimum duration: 7 days or 100+ samples per variant, whichever is longer
- Log in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Run experiment-evaluation
- Adopt (winner clear): implement permanently, update live config
- Iterate (marginal): generate refined hypothesis, return to Phase 2
- Revert (treatment worse): disable variant, restore control, return to Phase 1
- Extend (insufficient data): keep running, set reminder

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate weekly optimization brief: what changed, why, net impact, distance from estimated local maximum, recommended focus
- Post to Slack and store in Attio

### 2. Deploy the onboarding health monitor

Run the `onboarding-health-monitor` drill. This creates the onboarding-specific monitoring layer that feeds the autonomous optimization loop:

- Per-persona health dashboard in PostHog: activation rate trends, time to activation distributions, tour completion rates, email engagement, persona classification distribution, drop-off heatmap
- Defined anomaly thresholds per metric (normal/warning/critical ranges)
- Daily monitoring n8n workflow that queries PostHog and classifies each metric
- Critical anomalies trigger immediate Slack alerts with persona name, metric, current vs expected value, and suggested investigation steps
- Weekly health report aggregating all per-persona metrics, trends, anomalies, active experiments, and recommended actions
- Cohort drift detection comparing this week's signup profile against historical averages (detects when the user mix changes, requiring onboarding path updates rather than flow fixes)

The health monitor feeds anomaly data directly into the autonomous-optimization loop's Diagnose phase. The anomaly type determines the hypothesis space: tour problem leads to test tour variations, email problem leads to test email copy, classification problem leads to fix classification rules, cohort drift leads to strategic review.

### 3. Configure ongoing experiment execution

Use the `onboarding-experiment-orchestration` drill as the execution framework for each experiment the autonomous loop launches. The agent:

- Creates the PostHog experiment with proper flag setup, metrics, and guardrails
- Implements the variant in the appropriate tool (Intercom, Loops, or product code)
- Instruments tracking with experiment_variant properties
- Evaluates results with statistical rigor (95% confidence, secondary metric checks)
- Logs the complete result for audit trail

The autonomous loop decides WHAT to test. The onboarding-experiment-orchestration drill defines HOW to run each test.

### 4. Set guardrails (critical)

The autonomous optimization loop must respect these constraints:

- **Rate limit:** Maximum 1 active onboarding experiment at a time. Never stack experiments on new users — each user sees exactly one experimental condition.
- **Revert threshold:** If activation rate drops > 30% during an experiment, auto-revert immediately and send alert.
- **Human approval required for:**
  - Changes affecting > 50% of all new signups (persona-wide changes at a persona representing > 50% of traffic)
  - Changes to the activation metric definition
  - Any hypothesis flagged as "high risk" by the generation step
  - Budget increases for tools
- **Cooldown:** After a reverted experiment, wait 7 days before testing on the same onboarding surface.
- **Monthly cap:** Maximum 4 experiments per month. If all 4 fail in a month, pause autonomous optimization and flag for human strategic review.
- **Never optimize unmeasured surfaces:** If a surface does not have PostHog tracking, fix tracking first before running experiments on it.

### 5. Monitor for convergence

The autonomous loop detects convergence: when successive experiments produce diminishing returns. Convergence criteria:

- 3 consecutive experiments produce < 2% improvement on the primary metric (activation rate)
- No anomalies detected in the last 4 weeks
- Per-persona activation rates are within 10 percentage points of each other

At convergence:
1. The play has reached its local maximum activation rate
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment cadence from continuous to monthly exploratory tests
4. Generate a convergence report: current activation rate, improvement trajectory, what was tested, what worked, what the remaining gap (if any) would require to close (product changes, market positioning changes)
5. The agent shifts from active optimization to maintenance mode: monitor for regressions, respond to anomalies, but do not continuously seek improvement

### 6. Evaluate sustainability

This level runs continuously for 6 months minimum. Monthly review:
- Is activation rate sustained or improving?
- Are experiments still producing wins, or has the system converged?
- Are guardrails working? (No unauthorized changes, no metric degradation)
- Is the agent generating good hypotheses? (Spot-check 2-3 per month)

**Pass:** Activation rate sustained or improving over 6 months. The autonomous loop has found and maintains the local maximum. Experiment velocity naturally slowed as the system converged.

**Maintenance mode:** After convergence, the agent monitors weekly and runs 1 exploratory experiment per month. If a product change or user mix shift causes activation to drop, the agent re-enters active optimization automatically.

## Time Estimate

- 12 hours: Autonomous optimization loop setup (n8n workflows, PostHog anomaly detection, hypothesis generation pipeline, evaluation logic, reporting)
- 8 hours: Onboarding health monitor setup (per-persona dashboard, anomaly thresholds, daily/weekly monitoring workflows, cohort drift detection)
- 4 hours: Guardrail configuration and testing
- 8 hours: First-month supervision (reviewing autonomous decisions, tuning hypothesis quality, validating guardrails)
- 16 hours: Months 2-6 light oversight (2-3 hours/month: review weekly briefs, spot-check hypotheses, handle human-approval requests)
- 4 hours: Monthly convergence assessment and reporting
- 8 hours: Buffer for anomaly investigation and strategic reviews

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, anomaly detection, per-persona funnels, session recordings | Free tier: 1M events/mo, 1M flag requests/mo, 5K recordings/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product tour variants, in-app nudge messages, contextual tooltips | Essential: $29/seat/mo + Proactive Support Plus: $99/mo for 500 messages — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Email sequence variants, behavioral trigger emails | Starter: $49/mo for 5,000 contacts with unlimited sends — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Autonomous optimization workflows (monitoring, experiment lifecycle, reporting) | Self-hosted: free; Cloud: from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief generation | Pay-per-use: ~$3-15/mo at this experiment volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated monthly cost at this level:** $128-216/mo (Intercom $128/mo + Loops $49/mo if > 1K contacts; PostHog and n8n free tiers likely sufficient; Anthropic API $3-15/mo)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics for anomalies, diagnose root causes, generate hypotheses, run experiments, evaluate results, implement winners, generate weekly briefs, detect convergence
- `onboarding-health-monitor` — per-persona onboarding monitoring with anomaly thresholds, daily health checks, weekly reports, and cohort drift detection that feeds anomaly data into the autonomous optimization loop
- `onboarding-experiment-orchestration` — execution framework for each experiment: PostHog setup, variant implementation, tracking instrumentation, and statistical evaluation
