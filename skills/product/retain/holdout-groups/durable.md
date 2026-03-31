---
name: holdout-groups-durable
description: >
  Holdout Group Analysis — Durable Intelligence. Autonomous AI agent monitors holdout
  lift, detects when optimization impact plateaus, generates experiment hypotheses,
  runs A/B tests against the treatment group, and auto-implements winners. Weekly
  optimization briefs track convergence toward the local maximum.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Sustained or improving cumulative lift over 6 months via autonomous optimization; convergence detected when 3 consecutive experiments produce <2% incremental lift"
kpis: ["Cumulative lift % (treatment vs holdout)", "Lift trend (accelerating/flat/converging)", "Experiment velocity", "Autonomous win rate (% of agent-initiated experiments adopted)", "Time to convergence"]
slug: "holdout-groups"
install: "npx gtm-skills add product/retain/holdout-groups"
drills:
  - autonomous-optimization
---

# Holdout Group Analysis — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An always-on AI agent manages the holdout analysis system end-to-end. The agent monitors cumulative lift trends, detects when lift growth plateaus, generates improvement hypotheses from the data, designs and launches A/B experiments against the treatment group, evaluates results, and auto-implements winners. The holdout group provides the ground truth for whether the agent's optimizations are actually compounding value. Weekly optimization briefs report cumulative lift, experiment results, and convergence status. The play reaches its local maximum when 3 consecutive agent-initiated experiments produce less than 2% incremental lift improvement.

## Leading Indicators

- Agent autonomously detects lift plateau within 48 hours of occurrence
- Agent generates and launches a new experiment within 72 hours of detecting a plateau or drop
- Holdout integrity checks pass continuously for 6+ months without manual intervention
- Weekly optimization briefs are generated and posted automatically
- Cumulative lift is stable or increasing month over month
- Autonomous win rate (experiments that led to adopted improvements) exceeds 40%

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for the holdout measurement system. The agent loop operates as follows:

**Monitor (daily via n8n cron):**
- Use the the holdout lift measurement workflow (see instructions below) drill's weekly output as the primary data source
- Run `posthog-anomaly-detection` on the cumulative lift trend: is lift accelerating, flat, or declining?
- Classify the current state:
  - **Growing:** Lift increased >2% this week. No action needed — current experiments are working.
  - **Plateau:** Lift changed <2% for 3+ consecutive weeks. Trigger hypothesis generation.
  - **Drop:** Lift decreased >5% this week. Trigger urgent investigation.
  - **Converging:** Three consecutive experiments produced <2% incremental lift. The play has reached its local maximum.

**Diagnose (triggered by plateau or drop):**
- Gather context: which experiments are running, which recently concluded, what the segment-level lift looks like
- Pull 8-week lift trend from PostHog
- Feed all context to `hypothesis-generation` to produce 3 ranked hypotheses for what to optimize next
- Each hypothesis must specify: what to change in the treatment group, expected impact on cumulative lift, risk level, and experiment design
- Store hypotheses in Attio. If the top hypothesis is flagged as "high risk," send alert for human review and STOP.

**Experiment (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Use `posthog-experiments` to create a new A/B test within the treatment group only (holdout remains excluded)
- Implement the variant (e.g., change onboarding flow, adjust in-app messaging timing, modify feature discovery sequence)
- Set minimum duration: 7 days or 100+ samples per variant
- Log experiment start in Attio with hypothesis, start date, and success criteria

**Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to decide: adopt, iterate, revert, or extend
- Measure the incremental impact on cumulative holdout lift: did adopting this change increase the gap between treatment and holdout?
- If adopted: update live configuration. Log the win.
- If reverted: log the failure. Return to monitoring.
- If 3 consecutive experiments were reverted, pause the loop and flag for human strategic review.

**Report (weekly via n8n cron):**
- Generate a weekly optimization brief:
  - Current cumulative lift across all metrics
  - Experiments run this week and their outcomes
  - Net lift change this week
  - Convergence status: "optimizing" (lift still growing), "converging" (diminishing returns detected), or "converged" (local maximum reached)
  - Holdout integrity status
  - Recommended focus for next week
- Post brief to Slack/email and store in Attio

### 2. Maintain holdout integrity at scale

The `autonomous-optimization` drill runs weekly with zero manual intervention. At Durable level, add:
- Automated contamination remediation: if a holdout user is exposed to an experiment, the agent automatically disables that experiment's flag for the contaminated users and logs the incident
- Long-term demographic drift detection: compare holdout vs treatment demographics quarterly (not just weekly) to catch slow-moving shifts
- Holdout refresh assessment: after 6 months, evaluate whether the holdout should be dissolved and recreated to capture a new user mix

### 3. Detect convergence and act on it

The autonomous optimization loop should detect convergence — the point where further experiments yield diminishing returns:

**Convergence criteria:** 3 consecutive experiments produce <2% incremental lift on the primary metric.

**When convergence is detected:**
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment velocity from 4/month to 1/month (maintenance experiments only)
3. Generate a convergence report:
   - Total cumulative lift achieved (final holdout vs treatment gap)
   - Total experiments run and their aggregate contribution
   - Top 3 experiments by impact
   - Estimated revenue/retention impact of the cumulative lift
4. Report: "This play has reached its local maximum. Current cumulative lift is {X}%. Further gains require strategic changes (new features, new markets, pricing changes) rather than tactical optimization."

**Human action required:** At convergence, decide whether to dissolve the holdout (let all users benefit from optimizations) or maintain it as a permanent measurement baseline for future strategic changes.

### 4. Evaluate sustainability

This level runs continuously for 6 months. Monthly checkpoints:
- Month 1-2: Agent should be running experiments and lift should be growing
- Month 3-4: Lift growth may slow as easy wins are captured. Agent shifts to more targeted, segment-specific experiments
- Month 5-6: Expect convergence detection. If not converging, the product or market may be shifting enough to create ongoing optimization opportunities

The play is durable when: cumulative lift is sustained or improving over the 6-month window, holdout integrity has never been compromised, and the agent has operated autonomously with human intervention only on high-risk decisions.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (Month 1)
- 10 hours: monitor and refine agent behavior in first 2 months (5 hours/month)
- 30 hours: ongoing experiment execution by the agent (5 hours/month x 6 months, mostly automated)
- 10 hours: monthly reviews, convergence assessment, strategic decisions (2 hours/month x 5)
- 10 hours: final convergence report and dissolution decision

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, dashboards, anomaly detection | Free up to 1M flag requests/mo; usage-based beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Daily/weekly cron workflows for monitoring, experiments, reporting | Pro: ~$60/mo for 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly briefs | Sonnet 4.6: $3/$15 per MTok; ~$15-30/mo at Durable volume ([claude.com/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners
- the holdout lift measurement workflow (see instructions below) — weekly cumulative lift calculation that feeds the autonomous loop with ground-truth holdout vs treatment data
- `autonomous-optimization` — continuous validation that the holdout group remains clean, with automated contamination remediation
