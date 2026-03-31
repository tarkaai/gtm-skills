---
name: workflow-optimization-suggestions-durable
description: >
  AI Workflow Recommendations — Durable Intelligence. Always-on AI agent monitors suggestion
  performance, detects anomalies, generates improvement hypotheses, runs experiments, and
  auto-implements winners. Autonomous optimization finds the local maximum of suggestion
  acceptance and user efficiency, converging when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained ≥30% acceptance rate with efficiency improvements maintained or increasing over 6 months via autonomous optimization"
kpis: ["Suggestion acceptance rate (weekly trend)", "Median user efficiency vs. power user benchmark (%)", "Experiment velocity (experiments completed per month)", "Experiment win rate (%)", "Retention lift (adopters vs. non-adopters)", "System ROI (efficiency gain + retention value / system cost)"]
slug: "workflow-optimization-suggestions"
install: "npx gtm-skills add product/retain/workflow-optimization-suggestions"
drills:
  - autonomous-optimization
  - workflow-optimization-health-monitor
---

# AI Workflow Recommendations — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The suggestion system runs itself. An autonomous optimization loop monitors all suggestion metrics, detects when acceptance rates plateau or drop, generates hypotheses for improvement, runs A/B experiments, and auto-implements winners. The system finds the local maximum of suggestion acceptance and user efficiency, then maintains it as user behavior, product features, and competitive landscape shift. Weekly optimization briefs keep the team informed without requiring their intervention.

## Leading Indicators

- Autonomous optimization loop runs every day without errors for 4+ consecutive weeks
- At least 1 experiment completed per month with statistically significant results
- Weekly optimization brief is generated and distributed automatically
- Convergence detection working: when experiments produce <2% improvement, the system reduces monitoring frequency
- No manual intervention required for 4+ consecutive weeks (the system is truly autonomous)
- Retention correlation strengthens over time (the longer users receive suggestions, the better they retain)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill in full, configured for the workflow suggestion system:

**Phase 1 — Monitor (daily via n8n cron):**

Configure the anomaly detection to watch these suggestion-specific metrics:

| Metric | Source | Anomaly threshold |
|--------|--------|------------------|
| Weekly acceptance rate | PostHog funnel: `suggestion_delivered → suggestion_adopted` | Drop >20% from 4-week rolling average |
| Weekly dismissal rate | PostHog: `suggestion_dismissed / suggestion_delivered` | Rise >30% from 4-week rolling average |
| Median efficiency improvement | PostHog: `suggestion_adopted.efficiency_change_pct` | Drop below 10% for 2 consecutive weeks |
| Suggestion generation success rate | n8n pipeline logs | Below 90% (failed API calls, empty suggestions) |
| Feature discovery rate | PostHog: unique features used per user per week | Plateau (±2%) for 3+ weeks |

The n8n workflow queries PostHog for each metric, compares to the 4-week rolling average, and classifies as normal, plateau, drop, or spike.

If normal → log to Attio, no action.
If anomaly detected → trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

When an anomaly is detected, gather context:
1. Pull the current suggestion pipeline configuration from n8n (segment rules, prompt templates, delivery timing, frequency caps)
2. Pull 8-week metric history from PostHog
3. Pull the current segment distribution (how many users in each maturity x pattern x response segment)
4. Run the `hypothesis-generation` fundamental with this context

The AI generates 3 ranked hypotheses. Examples:
- "Acceptance rate dropped because 40% of suggestions are now 'discovery' type for Advanced users who have already discovered most features. Change: shift Advanced users to automation suggestions only."
- "Dismissal rate increased because the Intercom tooltip appears during workflow execution, interrupting flow. Change: delay tooltip to session end."
- "Efficiency improvement declined because the power user benchmark has not been updated in 6 weeks and is stale. Change: refresh the benchmark weekly."

If the top hypothesis has risk = "high" → send Slack alert for human review and STOP.
If risk = "low" or "medium" → proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Design the experiment using PostHog experiments:
   - Create a feature flag that splits the relevant user segment between control (current behavior) and variant (hypothesis change)
   - Set the experiment primary metric (acceptance rate for most hypotheses)
   - Set guardrail metrics: dismissal rate must not increase, efficiency improvement must not decrease
2. Implement the variant in the n8n pipeline:
   - If the hypothesis changes prompt templates → create a variant branch in n8n
   - If the hypothesis changes delivery timing → create a variant trigger schedule
   - If the hypothesis changes segment rules → create a variant feature flag condition
3. Run for minimum 14 days or until 200+ users per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog
2. Run the `experiment-evaluation` fundamental
3. Decision matrix:
   - **Adopt** (significant improvement, guardrails held): Update the n8n pipeline to use the winning variant for all users. Archive the experiment feature flag. Log the change in Attio.
   - **Iterate** (partial improvement or interesting signal): Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert** (no improvement or guardrail violation): Disable the variant, restore control. Log the failure. Return to Phase 1 monitoring.
   - **Extend** (trending positive but not significant): Continue the experiment for another 7 days.

**Phase 5 — Report (weekly via n8n cron):**

Generate the weekly optimization brief:
1. Anomalies detected this week and their classifications
2. Experiments in progress: status, current metrics, expected completion
3. Experiments completed: results, decisions, implemented changes
4. Net metric impact: acceptance rate change, efficiency change from all adopted experiments
5. Distance from estimated local maximum: "Based on the last 3 experiments, we are approximately [X]% from the ceiling"
6. Recommended focus for next week

Post the brief to Slack and store in Attio.

### 2. Deploy the health monitoring system

Run the `workflow-optimization-health-monitor` drill in full:

1. Build the 8-panel PostHog dashboard (pipeline health, acceptance trends, segment heatmap, efficiency curve, retention correlation, fatigue indicator, suggestion quality, system ROI)
2. Configure the 5 threshold alerts in n8n (acceptance drop, dismissal spike, pipeline stall, efficiency regression, segment imbalance)
3. Set up the automated weekly brief (supplements the autonomous optimization brief with operational details)
4. Build the monthly cohort analysis: track how each signup cohort's efficiency progresses over months 1, 2, 3, 6 — do later cohorts (who received suggestions from day 1) reach power-user efficiency faster?
5. Build the monthly executive ROI report: total system cost vs. estimated retention value saved + efficiency time saved

### 3. Implement convergence detection

The system should detect when it has found the local maximum:

1. After each experiment, log the improvement percentage
2. If 3 consecutive experiments produce <2% improvement each, declare convergence
3. At convergence:
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment cadence from 1/month to 1/quarter
   - Generate a convergence report: "The workflow suggestion system has reached its local maximum. Current performance: [metrics]. Further gains require strategic changes (new suggestion types, new product features, or new user segments) rather than tactical optimization."
4. Continue monitoring for regression — if metrics drop >15% from the converged state, re-activate daily monitoring and the full optimization loop

### 4. Handle product changes

Product updates (new features, UI changes, removed features) invalidate existing suggestions. Build a product change detection mechanism:

1. When a new feature ships, add it to the `undiscovered_features` list in the AI prompt
2. When a feature is removed or renamed, add it to a blocklist so suggestions never reference it
3. When the UI changes, invalidate all efficiency suggestions that reference the old UI (e.g., "click Menu > X" when the menu was reorganized)
4. When new workflow types are added, instrument them with `workflow_started` / `workflow_completed` events and regenerate the power user benchmark

**Human action required:** Notify the system (via a webhook or manual n8n trigger) when significant product changes ship. The system cannot detect UI changes autonomously.

### 5. Evaluate sustainability

**Pass threshold: Sustained ≥30% acceptance rate with efficiency improvements maintained or increasing over 6 months**

This level runs continuously. Monthly checkpoints:

- Month 1-2: Validate the autonomous loop runs without intervention. At least 1 experiment completed.
- Month 3-4: Acceptance rate stable or improving. Retention correlation statistically significant.
- Month 5-6: System approaches convergence. ROI is positive. The team trusts the system to run autonomously.

If acceptance rate degrades below 20% for 4+ consecutive weeks despite autonomous optimization, escalate to strategic review: the suggestion types, delivery channels, or user segments may need fundamental redesign rather than incremental optimization.

## Time Estimate

- 20 hours: configure the autonomous optimization loop (daily monitoring, hypothesis generation, experiment pipeline, weekly reporting)
- 15 hours: build the health monitoring system (dashboard, alerts, weekly brief, monthly reports)
- 10 hours: implement convergence detection and product change handling
- 5 hours: test the full autonomous loop end-to-end with synthetic anomalies
- 70 hours: monitoring and maintenance over 6 months (~3 hours/week, decreasing as the system stabilizes)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Metrics monitoring, experiments, feature flags, dashboards, anomaly detection | Free tier to ~$50-200/month at 500+ user scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude API | Suggestion generation + hypothesis generation + experiment evaluation + weekly briefs | ~$25-75/month at Sonnet 4.6 with prompt caching ([claude.com/pricing](https://claude.com/pricing)) |
| Intercom | In-app suggestion delivery, Custom Bots, tooltips | $29-85/seat/month + Proactive Support Plus $99/month ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email suggestion delivery for inactive users | Free tier to $49/month ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Orchestration: daily monitoring cron, experiment pipeline, weekly reports | Free self-hosted; Cloud from $24/month ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Log experiments, reports, convergence data | Standard stack — not counted ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated Durable cost: ~$175-450/month** (Intercom with Proactive Support + Loops + n8n + Claude API + PostHog paid tier)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics daily, detect anomalies, generate hypotheses with Claude, run A/B experiments via PostHog, evaluate results, auto-implement winners, generate weekly briefs
- `workflow-optimization-health-monitor` — continuous visibility: 8-panel dashboard, 5 threshold alerts, weekly operational brief, monthly cohort analysis, monthly ROI report
