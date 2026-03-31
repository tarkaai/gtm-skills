---
name: feature-flag-management-durable
description: >
  Feature Flag System -- Durable Intelligence. Always-on AI agents autonomously optimize
  flag rollout strategies, detect anomalies, run improvement experiments, and maintain
  the flag system at its local maximum. autonomous-optimization drives the core loop.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "Ongoing (20 hours setup, then continuous)"
outcome: "Rollout success rate sustained >=90% over 6 months with autonomous experiment-driven improvement and <2% degradation between optimization cycles"
kpis: ["Rollout success rate (6-month sustained)", "Autonomous experiment velocity", "Experiment win rate", "Mean time to detect regression", "Flag debt ratio trend", "AI lift vs Scalable baseline"]
slug: "feature-flag-management"
install: "npx gtm-skills add product/retain/feature-flag-management"
drills:
  - autonomous-optimization
  - dashboard-builder
---
# Feature Flag System -- Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
An always-on AI agent operates the flag system autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in flag health KPIs, generate hypotheses for improving rollout strategies, run A/B experiments on the flag system itself, evaluate results, and auto-implement winners. The agent produces weekly optimization briefs. The system converges when successive experiments produce <2% improvement -- the flag system has reached its local maximum.

## Leading Indicators
- Autonomous optimization loop fires daily without human intervention
- Hypotheses generated are specific and testable (not generic "improve things")
- At least 1 experiment running at all times on flag system parameters
- Weekly optimization briefs delivered on schedule with net impact calculations
- Rollout success rate trend is flat or improving (not declining)
- Flag debt ratio trend is flat or declining

## Instructions

### 1. Deploy autonomous optimization on the flag system
Run the `autonomous-optimization` drill configured for feature flag management. The agent monitors these primary KPIs:

- **Rollout success rate**: the percentage of flags reaching 100% without rollback
- **Mean time to full rollout**: average days from creation to full deployment
- **Rollback rate**: percentage of flags that require rollback
- **Flag debt ratio**: stale flags divided by active flags
- **Regression gate accuracy**: false positive rate (blocked but no real regression) and false negative rate (passed but regression occurred later)

The optimization loop operates as follows:

**Monitor (daily):** Use `posthog-anomaly-detection` to check each KPI against its 4-week rolling average. Classify as normal, plateau, drop, or spike.

**Diagnose (on anomaly):** When an anomaly is detected, the agent gathers context: current rollout schedule parameters, regression gate thresholds, recent rollback details, flag volume trends. It runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples of valid hypotheses:
- "Reducing the medium-risk canary period from 2 days to 1 day will decrease mean time to full rollout by 15% without increasing rollback rate, because the 48-hour canary window catches 95% of regressions in the first 24 hours based on historical data"
- "Increasing the regression gate error-rate threshold from 10% to 15% will reduce false-positive blocks by 40%, because 60% of current blocks are for error-rate deltas between 10-15% that resolve without intervention"
- "Adding a load-time guardrail metric to regression gates will catch 2 regressions per month that currently pass the error-rate-only gate, because the last 3 rollback-after-completion incidents were performance regressions"

**Experiment (on accepted hypothesis):** Use `posthog-experiments` to A/B test the hypothesis. Split new flags into control (current parameters) and treatment (hypothesis parameters). Run for minimum 2 weeks or 20 flags per group, whichever is longer.

**Evaluate (on experiment completion):** Use `experiment-evaluation` to determine: Adopt (update parameters system-wide), Iterate (refine hypothesis), Revert (restore original), or Extend (more data needed).

**Report (weekly):** Generate a weekly optimization brief covering: anomalies detected, hypotheses generated, experiments running, decisions made, net metric change, estimated distance from local maximum.

### 2. Maintain flag health monitoring at Durable cadence
Run the `autonomous-optimization` drill at elevated monitoring frequency:
- Daily health checks (upgraded from weekly at Scalable)
- Real-time anomaly alerts for critical metrics (rollback rate spike, flag evaluation errors)
- Monthly comprehensive report with 6-month trend analysis
- Per-flag product impact tracking with automatic escalation when a flag shows sustained negative impact

The health monitor feeds data into the autonomous optimization loop. When health metrics degrade, the optimization loop detects the anomaly and generates improvement hypotheses.

### 3. Build the flag system intelligence dashboard
Run the `dashboard-builder` drill to create a Durable-level dashboard:

| Panel | Purpose |
|-------|---------|
| Optimization loop status | Current state: monitoring, diagnosing, experimenting, evaluating |
| Active experiment | Current hypothesis being tested, control vs treatment metrics, days remaining |
| Experiment history | Timeline of all experiments with outcomes: adopted, iterated, reverted |
| KPI trends (6-month) | All primary KPIs with rolling averages and anomaly markers |
| AI lift | Cumulative improvement from autonomous experiments vs Scalable baseline |
| Convergence indicator | Rolling 3-experiment average improvement -- when <2%, the system is converged |
| Weekly brief archive | Links to all weekly optimization briefs |

### 4. Configure convergence detection
The agent monitors its own effectiveness. When 3 consecutive experiments produce <2% improvement on any primary KPI, that KPI has converged:

1. Log `flag_system_converged` event with the KPI name and final optimized value
2. Reduce monitoring frequency for that KPI from daily to weekly
3. Report to the team: "Flag rollout success rate has converged at {value}. Further gains require strategic changes (new regression detection methods, different rollout schedule paradigms, infrastructure changes) rather than parameter tuning."
4. Continue monitoring for regression -- if a converged KPI drops >10% from its optimized value, re-enter the full optimization loop

### 5. Guardrails for autonomous flag optimization

- **Never modify regression gates during an active rollout**: parameter changes only apply to newly created flags
- **Maximum 1 experiment at a time** on flag system parameters -- never stack experiments
- **Human approval required for**: removing a regression gate metric, changing the rollback threshold, modifying the high-risk rollout schedule
- **Auto-revert if**: rollback rate exceeds 20% during any experiment, or flag evaluation latency exceeds 100ms
- **Cooldown**: after a reverted experiment, wait 14 days before testing a new hypothesis on the same parameter
- **Maximum 2 experiments per month** on flag system parameters -- the flag system is infrastructure, not a growth lever; stability matters more than optimization velocity

## Time Estimate
- 8 hours: Configure autonomous-optimization drill for flag system KPIs
- 4 hours: Upgrade flag-rollout-health-monitor to daily cadence with real-time alerts
- 4 hours: Build the Durable-level intelligence dashboard
- 4 hours: Configure convergence detection and guardrails
- Ongoing: the agent runs the optimization loop continuously; human reviews weekly briefs

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, anomaly detection, dashboards | Free tier: 1M events/mo. Growth from $0 pay-per-use. https://posthog.com/pricing |
| n8n | Workflow automation for optimization loop scheduling | Self-hosted free; Cloud from EUR20/mo. https://n8n.io/pricing |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Pay-per-token. https://www.anthropic.com/pricing |
| Attio | Logging optimization decisions and experiment audit trail | Free tier available. https://attio.com/pricing |

## Drills Referenced
- `autonomous-optimization` -- the core Durable loop: monitor anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` -- daily/weekly flag health measurement feeding into the optimization loop
- `dashboard-builder` -- builds the intelligence dashboard showing optimization status, experiment history, and convergence
