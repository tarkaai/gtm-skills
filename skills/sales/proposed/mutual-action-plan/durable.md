---
name: mutual-action-plan-durable
description: >
  Mutual Action Plan (MAP) — Durable Intelligence. Autonomous AI agents continuously optimize
  MAP templates, scoring models, and communication strategies. The autonomous-optimization loop
  detects performance anomalies, generates hypotheses for improvement, runs A/B experiments on
  milestone structures and cadences, auto-implements winners, and produces weekly optimization
  briefs. The system finds the local maximum for MAP-driven deal acceleration and maintains it
  as market conditions and buyer behavior change.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving MAP impact (>=35% velocity lift, >=25% win rate lift) over 6 months via continuous agent-driven milestone optimization, risk detection, and timeline personalization"
kpis: ["MAP impact on velocity/win rate", "Agent experiment win rate", "Risk prediction accuracy", "Milestone optimization effectiveness"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
drills:
  - autonomous-optimization
  - map-risk-scoring
  - dashboard-builder
---

# Mutual Action Plan (MAP) — Durable Intelligence

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The MAP system runs autonomously. AI agents monitor MAP performance across the entire pipeline, detect when milestone completion rates, deal velocity, or risk prediction accuracy change, generate hypotheses for what to improve, run A/B experiments on templates and communication strategies, auto-implement winners, and produce weekly optimization briefs. The system finds the local maximum for MAP-driven deal acceleration and maintains it as buyer behavior, market conditions, and competitive dynamics change.

Pass: MAP velocity lift >= 35% and win rate lift >= 25% sustained for 6 consecutive months, with <= 2 hours/week team involvement (reviewing briefs and approving strategic changes only).
Fail: MAP impact decays below 25% velocity lift for 3 consecutive weeks despite automated interventions, or the system requires more than 4 hours/week of manual effort.

## Leading Indicators

- The `autonomous-optimization` loop produces a winning experiment at least once per month for the first 3 months (the system is still finding improvements)
- Risk prediction accuracy holds at >= 75% (Healthy deals win >= 75%, Critical deals win < 20%)
- MAP-based close date predictions stay within 7 days of actual for >= 65% of deals
- Milestone adherence rate trends upward as templates are optimized
- Successive experiments produce diminishing returns after month 4 (convergence toward local maximum — this is the goal)
- Weekly optimization briefs are generated and delivered without human triggering
- Escalation interventions produce recovery in >= 50% of At Risk deals

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for the MAP system. This is the core of Durable — an always-on agent that monitors, diagnoses, experiments, and implements.

**Configure the monitoring phase (daily via n8n cron):**

The agent checks daily using MAP data from Attio and PostHog:

- Overall MAP velocity lift: 7-day rolling average of (non-MAP days to close - MAP days to close) / non-MAP days to close. Compare against 4-week rolling average.
- MAP win rate lift: 7-day rolling win rate for MAP deals vs non-MAP. Compare against 4-week rolling average.
- Milestone adherence rate per milestone type: percentage completed on time. Per-template and per-milestone breakdown.
- Risk score distribution: percentage of deals at each risk level. Compare against historical baseline.
- Risk prediction accuracy: compare last month's risk scores against actual outcomes for closed deals.
- Forecast accuracy: compare MAP-predicted close dates against actual for deals that closed this week.
- Stall rate: percentage of active MAPs with stall events this week.
- Escalation recovery rate: percentage of escalated deals that returned to Healthy or Watch status.

Classification thresholds (from `autonomous-optimization`):
- **Normal:** within +/- 10% of 4-week rolling average
- **Plateau:** within +/- 2% for 3+ weeks (no improvement, no degradation)
- **Drop:** > 20% decline from rolling average
- **Spike:** > 50% increase (investigate — could be good or bad)

If anomaly detected on any metric: trigger the diagnosis phase.

**Configure the diagnosis phase (triggered by anomaly):**

The agent gathers context:
1. Pull current MAP configuration from Attio: active templates, milestone structures, update cadences, escalation rules
2. Pull 8-week metric history from PostHog for all MAP KPIs
3. Pull deal mix data: has the proportion of deal types changed? (More Enterprise deals have different MAP dynamics than SMB)
4. Pull milestone-level data: which specific milestones are causing the anomaly? Is one milestone type dragging down the overall rate?
5. Run `hypothesis-generation` with the anomaly data + context

Example hypotheses the agent might generate:
- "Milestone adherence for 'Legal Review' dropped 30% this month. 4 of 5 affected deals are Enterprise. Hypothesis: the legal review duration estimate is too short for Enterprise deals. Test extending from 7 days to 14 days for Enterprise template."
- "MAP velocity lift dropped from 38% to 22%. New rep started this month and is sending MAPs without the planning call. Hypothesis: MAPs co-created on a call outperform MAPs sent cold. Test adding a required 'MAP planning call' milestone at the start of every MAP."
- "Stall rate increased 40% over 3 weeks. All stalled deals have buyer-owned 'Executive Alignment' milestone overdue. Hypothesis: prospects don't know how to run internal alignment. Test including a 'Suggested Internal Email' template with the MAP that helps champions sell internally."
- "Risk scores predict accurately for SMB (82%) but poorly for Enterprise (54%). Hypothesis: the risk model weights are calibrated on SMB data. Test separate scoring models per deal type."

Store hypotheses in Attio. If risk = "high" (changing milestone structure for > 50% of active deals, modifying the risk scoring model, or changing the escalation rules), send Slack alert for human approval. Otherwise proceed to experiment.

**Configure the experiment phase (triggered by hypothesis acceptance):**

Use PostHog feature flags to split new MAP deals between control and variant. The agent:
1. Creates the variant (e.g., modified template, different cadence, new escalation timing)
2. Sets up the PostHog experiment with control (current) vs variant
3. Defines the primary metric (the anomalous KPI) and secondary metrics (other MAP KPIs as guardrails)
4. Sets the experiment duration: minimum 14 days or 15 deals per variant, whichever is longer
5. Logs the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Configure the evaluation phase (triggered by experiment completion):**

The agent pulls PostHog experiment results and runs `experiment-evaluation`:
- **Adopt:** The variant wins with >= 90% statistical significance and the improvement is >= 5% relative. Secondary metrics (win rate, velocity lift) did not decline by more than 10%. Update the live MAP configuration. Log the change in Attio.
- **Iterate:** Results are inconclusive or improvement < 5%. Generate a new hypothesis building on this result. Return to diagnosis.
- **Revert:** The variant performed worse, or secondary metrics degraded significantly. Disable the variant, restore control. Log the failure. Return to monitoring.

**Guardrails (enforced by n8n):**
- Maximum 1 active experiment at a time across the MAP system. Never stack experiments.
- If MAP velocity lift drops below 20% at any point during an experiment, auto-revert immediately.
- If milestone adherence drops below 40% during an experiment, auto-revert immediately.
- Human approval required for: changes to the risk scoring model, changes affecting > 50% of active deals, changes to escalation rules that modify who gets contacted.
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- Never experiment on milestone structures for deals in the last 30% of their MAP timeline (too disruptive to change milestones mid-deal).

### 2. Deploy continuous risk model calibration

Extend the `map-risk-scoring` drill with autonomous recalibration.

**Monthly model calibration (n8n cron, 1st of each month):**
1. Pull all deals that closed in the last 30 days with MAP data
2. For each deal: compare the risk score 14 days before close with the actual outcome
3. Calculate prediction accuracy: percentage of Healthy deals that won, Watch that won, At Risk that won, Critical that won
4. If accuracy drifts below 70% for any risk level:
   - Retrain the model by re-analyzing historical patterns via Claude API
   - Adjust signal weights based on which signals were most predictive in recent data
   - Deploy the updated model to the daily scoring workflow
   - Log the model update in Attio with old weights, new weights, and accuracy before/after

**Deal type segmentation:**
If overall accuracy is >= 75% but accuracy for one deal type is < 65%, create a separate scoring model for that deal type. Enterprise deals may need different weights than SMB because the milestone structures and stall patterns are different.

**Intervention effectiveness tracking:**
For each intervention recommendation the agent generates:
- Track whether the rep executed it (did they take action within 48 hours?)
- Track the outcome: did the deal recover, stay at risk, or get lost?
- Feed this data back into the recommendation engine to improve future suggestions

### 3. Build the Durable performance dashboard

Run the `dashboard-builder` drill to create the Durable-level PostHog dashboard.

**Dashboard panels:**

- **MAP velocity lift trend:** 12-week rolling average of velocity improvement for MAP vs non-MAP deals, with Scalable baseline (35%) as a threshold line
- **MAP win rate lift trend:** 12-week rolling average of win rate improvement, with 25% threshold line
- **Risk distribution over time:** Stacked area chart showing how the pipeline's risk profile changes week by week
- **Risk prediction accuracy:** Monthly accuracy percentage for each risk level (Healthy/Watch/At Risk/Critical vs actual outcomes)
- **Forecast accuracy trend:** Monthly comparison of MAP-predicted revenue vs actual closed revenue
- **Milestone adherence heatmap:** Per-template, per-milestone completion rate. Color-coded. Updated weekly.
- **Stall rate trend:** Weekly stall count with recovery rate overlay
- **Escalation effectiveness:** Recovery rate by escalation level and intervention type
- **Active experiment status:** Current test, variant, days running, interim metric values
- **Experiment history:** Log of all experiments: hypothesis, result, impact, date
- **Convergence indicator:** Rolling average improvement from the last 3 experiments. When < 2%, the system has reached its local maximum.
- **Model drift indicator:** Risk prediction accuracy trend. Alert line at 70%.
- **Team time tracker:** Hours of human involvement per week. Target <= 2.

**Alerts (via n8n):**

- MAP velocity lift drops below 25% for 2 consecutive weeks -> agent diagnoses, may trigger experiment
- Risk prediction accuracy drops below 70% -> trigger model recalibration
- Milestone adherence drops below 50% for any milestone type -> investigate template problem
- No experiments completed in 21+ days -> check if the optimization loop is running
- Stall rate exceeds 30% of active MAPs -> pipeline health problem, alert leadership
- Forecast accuracy drops below 60% for 2 consecutive months -> investigate prediction model
- Convergence detected (3 experiments < 2% improvement) -> reduce optimization frequency

### 4. Generate weekly optimization briefs

Build an n8n workflow (configured in `autonomous-optimization` Phase 5) that runs every Monday:

1. **Status summary:** Active MAPs this week, overall MAP velocity lift, win rate lift, comparison to Scalable baseline and prior 4-week average
2. **Risk summary:** Deals at each risk level. New At Risk and Critical deals with key risk factors. Deals that recovered this week.
3. **Milestone health:** Top 3 and bottom 3 milestone types by adherence rate. Any milestone types trending downward.
4. **Forecast update:** This month's expected MAP-influenced revenue. Forecast accuracy for last month.
5. **Experiment update:** What experiment ran, what the result was, what was implemented or reverted.
6. **Intervention report:** How many At Risk deals were flagged, how many had interventions, how many recovered.
7. **Next week plan:** What the agent plans to test or investigate. Any hypotheses queued.
8. **Convergence status:** Are experiments still producing improvements, or has the system converged?

Deliver via Slack to the team. Store in Attio as a campaign note.

**Human action required:** The team reads the weekly brief (5 minutes). If the brief recommends a strategic change (new deal type template, scoring model overhaul, fundamentally different MAP approach), the team decides. All tactical changes (milestone duration adjustments, update cadence tweaks, escalation timing) execute automatically.

### 5. Run monthly deep review

Build an n8n workflow that runs on the 1st of each month:

1. Pull 30-day aggregate metrics: MAP adoption, velocity lift, win rate lift, milestone adherence, forecast accuracy
2. Compare to prior month and to the original Scalable baseline
3. Segment performance by deal type: which deal types benefit most from MAPs?
4. Identify:
   - Templates performing well (high adherence, high win rate): maintain
   - Templates underperforming: flag for optimization experiments
   - New deal types or deal patterns that don't fit existing templates: flag for template creation
5. Calculate ROI: (revenue from MAP wins - revenue from equivalent non-MAP wins) / cost of MAP system
6. Flag convergence: if 3 consecutive experiments produced < 2% improvement, MAP optimization has reached its local maximum. Recommend reducing experimentation from weekly to biweekly.

**Human action required:** The team reviews the monthly deep review (~15 minutes). Decides on template additions/retirements and strategic changes.

### 6. Sustain for 6 months

The system runs continuously. The agent's responsibilities:
- Monitor all MAP performance metrics daily for anomalies
- Run the optimization loop: detect -> diagnose -> experiment -> evaluate -> implement
- Calibrate the risk scoring model monthly
- Track intervention effectiveness and improve recommendations
- Generate weekly optimization briefs and monthly deep reviews
- Detect convergence and reduce optimization intensity when the local maximum is reached
- Adapt templates when deal mix changes (new industries, new deal sizes, new buyer personas)

The team's responsibilities:
- Read the weekly Slack brief (5 minutes)
- Approve strategic changes flagged in the monthly review (~15 minutes/month)
- Approve high-risk experiments (risk model changes, major template changes)
- Conduct MAP planning calls with prospects (the human element remains critical for co-creation)

### 7. Evaluate sustainability after 6 months

Compute over the full 6-month period:

- Monthly MAP velocity lift for each of the 6 months (target: >= 35% every month)
- Monthly MAP win rate lift for each of the 6 months (target: >= 25% every month)
- Velocity lift trend: stable, improving, or decaying?
- Risk prediction accuracy trend: stable or improving?
- Forecast accuracy trend: stable or improving?
- Number of experiments run, number that produced significant improvements
- Convergence status: has the system found its local maximum?
- Total team hours: target <= 2 hours/week average over 6 months
- ROI: revenue attributed to MAP improvement / cost of MAP system

**PASS (>= 35% velocity lift and >= 25% win rate lift for all 6 months, <= 2 hours/week team time):** The play is durable. The MAP system is a self-optimizing deal acceleration engine. Consider: extending MAP concepts earlier in the funnel (pre-proposal milestone planning), applying MAP patterns to customer onboarding, or building MAP into a competitive differentiation narrative.

**CONVERGED (lifts stable at target but experiments no longer produce gains):** The local maximum has been found. Reduce the optimization loop from daily to weekly monitoring. Shift experiment resources to other plays. The MAP system is in maintenance mode.

**DECLINING (lifts held for 4+ months then decayed):** Market conditions or buyer behavior changed. The agent should detect this via anomaly monitoring and recommend strategic changes: new milestone structures for new buying patterns, different communication approaches, or adjusting for longer/shorter sales cycles.

**FAIL (velocity lift below 25% for 3+ consecutive weeks at any point):** The optimization loop is not adapting fast enough. Diagnose: Are experiments running? Are they targeting the right variables? Is the risk model accurate? Are reps still co-creating MAPs with prospects, or have they started sending them cold? Fix the specific broken component.

## Time Estimate

- Autonomous optimization loop setup: 16 hours (Month 1)
- Risk model calibration system: 8 hours (Month 1)
- Dashboard and alert system: 8 hours (Month 1)
- Weekly brief and monthly review workflows: 6 hours (Month 1)
- Setup subtotal: 38 hours
- Agent monitoring and loop execution: 3 hours/week x 24 weeks = 72 hours
- Weekly team time: 15 min/week x 24 weeks = 6 hours
- Monthly team review: 15 min x 6 months = 1.5 hours
- Experiment execution and implementation: 2 hours/month x 6 months = 12 hours
- Ongoing subtotal: ~91.5 hours
- Grand total: ~130 hours over 6 months (~116 agent, ~8 team, ~6 buffer)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MAP data, risk scores, experiment log, optimization history | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Automation — optimization loop, risk scoring, milestone tracking, forecasting, briefs | Pro $60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| PostHog | Analytics — MAP funnels, experiments, feature flags, anomaly detection, dashboards | Free (1M events/mo); paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| Claude API | Hypothesis generation, experiment evaluation, intervention recommendations, brief generation | Sonnet: $3/$15 per M input/output tokens ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Loops | Prospect MAP emails and update sequences | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Fireflies | Record MAP planning calls for milestone analysis | Pro $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |

**Estimated monthly cost for Durable:** ~$200-350/mo (n8n $60 + Claude API ~$40-80 for daily hypothesis/evaluation cycles + Loops $49 + Fireflies $10 + Attio $29 + PostHog likely within free tier)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect MAP performance anomalies, generate improvement hypotheses, run A/B experiments on templates and cadences, evaluate results, auto-implement winners, and produce weekly optimization briefs. Converges when successive experiments produce < 2% improvement.
- `map-risk-scoring` — continuous risk model calibration: monthly accuracy tracking, automatic weight adjustment, deal-type-specific scoring, and intervention effectiveness feedback loop
- `dashboard-builder` — build the Durable PostHog dashboard with velocity lift trends, risk prediction accuracy, forecast tracking, experiment history, convergence indicators, and model drift alerts
