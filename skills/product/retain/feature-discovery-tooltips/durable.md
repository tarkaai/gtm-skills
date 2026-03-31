---
name: feature-discovery-tooltips-durable
description: >
  Contextual Feature Tooltips — Durable Intelligence. Always-on AI agent that monitors
  tooltip performance, generates improvement hypotheses, runs experiments, auto-implements
  winners, and retires exhausted tooltips. Finds and maintains the local maximum for
  feature discovery via in-app nudges.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "Ongoing after 20 hours setup"
outcome: "Sustained or improving CTR >=35% over 6 months with autonomous optimization"
kpis: ["Tooltip CTR trend", "Sustained adoption rate", "Experiment velocity", "AI lift vs manual baseline", "Convergence status"]
slug: "feature-discovery-tooltips"
install: "npx gtm-skills add product/retain/feature-discovery-tooltips"
drills:
  - autonomous-optimization
---

# Contextual Feature Tooltips — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

The tooltip system runs autonomously. An AI agent monitors all tooltip metrics, detects when performance plateaus or drops, generates hypotheses for improvement, runs A/B experiments, auto-implements winners, and retires exhausted tooltips. The system sustains or improves CTR >=35% over 6+ months without human intervention. Weekly optimization briefs report what changed and why.

## Leading Indicators

- Anomaly detection triggering correctly on metric deviations (not generating false positives)
- At least 1 experiment per month completing with statistical significance
- Net positive lift from adopted experiments (cumulative AI lift trending up)
- Tooltip retirement pipeline removing exhausted tooltips automatically
- Convergence not yet reached (successive experiments still finding >2% improvements)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the always-on monitor-diagnose-experiment-evaluate-implement cycle for this play:

**Phase 1 -- Monitor (daily via n8n cron)**:
1. Use `posthog-anomaly-detection` to check these KPIs daily:
   - Aggregate tooltip CTR (2-week rolling average vs 4-week rolling average)
   - Sustained adoption rate per segment
   - Tooltip fatigue index (sequential dismissal rate)
   - Feature coverage ratio
2. Classify each KPI: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
3. If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly)**:
1. Pull the current tooltip configuration from Intercom and PostHog: which tooltips are active, what targeting rules, what copy variants, what delivery timing
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with the anomaly data. Example hypotheses the agent should generate:
   - "CTR dropped because the tooltip for feature X has reached audience saturation -- 80% of eligible users have already seen it"
   - "Adoption rate declined because new users in the last cohort have different usage patterns and the prerequisite-based targeting is misaligned"
   - "Fatigue index spiked because the 48-hour frequency cap is too aggressive for power users who visit daily"
4. Rank hypotheses by expected impact and risk. Store in Attio.
5. If top hypothesis risk = "high" (e.g., changing targeting rules for >50% of users), send Slack alert for human review and STOP
6. If risk = "low" or "medium", proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance)**:
1. Design the experiment using PostHog feature flags:
   - If hypothesis involves copy: create a new tooltip copy variant in Intercom, split traffic 50/50 via PostHog experiment
   - If hypothesis involves timing: create a variant trigger rule, split via PostHog
   - If hypothesis involves targeting: create a variant cohort, split via PostHog
   - If hypothesis involves retirement: disable the tooltip for 50% of users, measure if overall metrics improve
2. Set minimum experiment duration: 7 days or 200+ impressions per variant
3. Log experiment in Attio: hypothesis, start date, variants, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion)**:
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`:
   - **Adopt**: Variant wins with >=95% confidence and >=3% improvement. Update the live tooltip configuration. Log the change.
   - **Iterate**: Results inconclusive or improvement <3%. Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert**: Variant loses. Restore control. Log failure. Return to Phase 1 monitoring.
3. Store evaluation in Attio with full reasoning

**Phase 5 -- Report (weekly via n8n cron)**:
1. Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate: net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on CTR and adoption rate
   - Current distance from estimated local maximum
   - Active experiments in progress
   - Tooltips approaching retirement criteria
4. Post to Slack and store in Attio

### 2. Configure tooltip lifecycle management

Run the `autonomous-optimization` drill with Durable-level configuration:

- **Auto-retirement**: Tooltips that meet any of these criteria are automatically disabled:
  - Active 60+ days AND CTR below 10%
  - Shown to 80%+ of eligible users (audience exhausted)
  - Target feature adoption reached 70%+ (tooltip succeeded, no longer needed)
- **Auto-creation triggers**: When a new feature ships or an existing feature's usage drops below 30% of active users, the agent flags it as a tooltip candidate and generates draft tooltip copy using the patterns from the highest-performing existing tooltips
- **Seasonal adjustment**: The agent detects seasonal patterns (e.g., lower engagement in December) and adjusts anomaly detection baselines accordingly

### 3. Maintain the targeting pipeline

Run the the tooltip targeting automation workflow (see instructions below) drill in maintenance mode:

- The daily n8n pipeline continues to compute per-user tooltip priorities
- The autonomous optimization loop can modify targeting parameters (prerequisite feature requirements, segment definitions, frequency caps) as part of its experiments
- When the agent retires a tooltip, the pipeline automatically promotes the next-ranked tooltip for affected users
- When the agent identifies a new tooltip candidate, the pipeline creates the eligibility cohort and starts collecting data

### 4. Evaluate sustainability

This level runs continuously. Monthly review criteria:

- **Sustained**: CTR >=35% for each of the last 3 months. Adoption rate stable or improving. System is durable.
- **Improving**: CTR or adoption rate increased in 2 of the last 3 months due to adopted experiments. System is actively optimizing.
- **Converging**: Last 3 experiments produced <2% improvement each. The play has reached its local maximum. Reduce monitoring to weekly. Report: "Tooltip system is optimized. Current CTR: {X}%. Further gains require product changes (new features, UI redesign) rather than tooltip optimization."
- **Degrading**: CTR dropped below 35% for 2+ consecutive months despite optimization. Diagnose root cause (product changes, user base shift, competitive pressure). May require strategic intervention.

## Time Estimate

- 8 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiments, Attio logging)
- 6 hours: Tooltip lifecycle management (retirement rules, auto-creation triggers)
- 4 hours: Targeting pipeline maintenance mode configuration
- 2 hours: Weekly brief template and Slack integration
- Ongoing: ~1 hour/week reviewing weekly briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, feature flags | Free up to 1M events/mo; paid from $0.00031/event (https://posthog.com/pricing) |
| Intercom | Tooltip delivery, targeting, user properties | From $39/seat/mo with Engage add-on (https://www.intercom.com/pricing) |
| n8n | Optimization loop scheduling, reporting automation | Free self-hosted or from $24/mo cloud (https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation | $3/MTok input, $15/MTok output for Claude Sonnet (https://www.anthropic.com/pricing) |
| Attio | Experiment audit trail and campaign records | From $29/seat/mo (https://attio.com/pricing) |

## Drills Referenced

- `autonomous-optimization` -- the core monitor-diagnose-experiment-evaluate-implement loop that makes this level self-optimizing
- `autonomous-optimization` -- measurement layer with auto-retirement pipeline and fatigue detection
- the tooltip targeting automation workflow (see instructions below) -- personalized tooltip delivery pipeline running in maintenance mode
