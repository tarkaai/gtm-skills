---
name: plg-sales-hybrid-durable
description: >
  PLG + Sales-Assist Model — Durable Intelligence. Always-on AI agents run the
  autonomous optimization loop: detect metric anomalies, generate improvement
  hypotheses, run A/B experiments, evaluate results, and auto-implement winners.
  Sustained or improving conversion >=45% over 6 months.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving conversion >=45% over 6 months via autonomous optimization"
kpis: ["Sales-assist conversion rate", "Self-serve upgrade rate", "Experiment velocity", "Net optimization lift", "Convergence distance"]
slug: "plg-sales-hybrid"
install: "npx gtm-skills add product/upsell/plg-sales-hybrid"
drills:
  - autonomous-optimization
  - nps-feedback-loop
---

# PLG + Sales-Assist Model — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

The AI agent runs the PLG-to-sales pipeline autonomously. It monitors every metric in the conversion funnel, detects when performance plateaus or degrades, generates hypotheses for what to change, runs A/B experiments, evaluates results, and auto-implements winners. The goal is to find and maintain the local maximum -- the best possible conversion performance given the current market, product, and audience. Target: sustained or improving conversion >=45% over 6 months with <2% human intervention time.

## Leading Indicators

- Autonomous optimization loop running daily without errors
- At least 2 experiments completed per month with clear adopt/revert decisions
- Weekly health reports generating on schedule with actionable insights
- Anomaly detection catching real issues within 48 hours of onset
- NPS scores stable or improving among upgraded accounts

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core loop that makes Durable fundamentally different from Scalable. Configure it for the PLG pipeline:

**Phase 1 -- Monitor (daily via n8n cron):**
- Feed the play's primary KPIs into the anomaly detection system: self-serve conversion rate, sales-assist conversion rate, PQL signal volume, routing accuracy, MRR added per week
- Compare the last 2 weeks against the 4-week rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If all metrics are normal, log to Attio and continue monitoring
- If any metric is anomalous, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
- Pull the full pipeline context: current PQL thresholds, routing configuration, prompt copy variants, signal distribution, and AE capacity
- Pull 8-week metric history from PostHog
- Run hypothesis generation via Claude: "Given that [metric] has [anomaly type] from [baseline] to [current], and the current configuration is [context], generate 3 ranked hypotheses for what to change, with expected impact and risk level"
- Store hypotheses in Attio as notes on the PLG campaign record
- If the top hypothesis has risk = "high" (e.g., changing the routing threshold by more than 20 points, removing a PQL signal entirely), send a Slack alert for human review and wait for approval
- If risk is "low" or "medium", proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Design the experiment using PostHog feature flags: split traffic between control (current configuration) and variant (hypothesis change)
- Example hypotheses the agent might generate:
  - "Self-serve conversion dropped because the prompt copy mentions the feature name, not the outcome. Test outcome-focused copy."
  - "Sales-assist conversion dropped because new AEs are getting accounts without enough context. Test adding a 3-bullet account summary to the Slack alert."
  - "PQL volume dropped because the engagement scoring model weights are stale. Test updated weights based on the last 90 days of conversion data."
- Set experiment duration: minimum 7 days or 100+ samples per variant
- Log the experiment in Attio: hypothesis, start date, duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation via Claude: compare control vs variant on primary and secondary metrics
- Decision: Adopt (implement winner permanently), Iterate (generate new hypothesis building on this result), Revert (restore control), or Extend (keep running for more data)
- Store the full evaluation in Attio: decision, confidence, reasoning, metric impact
- If Adopt: update the live configuration and log the change

**Phase 5 -- Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on primary KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

**Guardrails (critical):**
- Maximum 1 active experiment at a time. Never stack experiments.
- If the primary conversion metric drops >30% during an experiment, auto-revert immediately.
- Human approval required for: routing threshold changes >15 points, PQL signal additions/removals, budget allocation changes.
- After a failed experiment (revert), wait 7 days before testing the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.

### 2. Deploy the PLG conversion health monitor

Run the `autonomous-optimization` drill. This provides the monitoring and reporting layer that feeds the autonomous optimization loop:

1. **Build the PLG pipeline dashboard** in PostHog with 6 panels: PQL funnel, self-serve conversion trend, sales-assist pipeline, routing quality, time metrics, and PQL signal distribution.

2. **Configure anomaly detection** for 6 conditions: self-serve conversion drop, sales-assist meeting rate drop, PQL volume drop, mis-route rate spike, time-to-upgrade increase, and ACV drop.

3. **Deploy the weekly health check** via n8n: pull metrics from PostHog and Attio every Monday, compute health scores (self-serve health, sales-assist health, routing health, overall PLG health), generate a 1-page report via Claude, and distribute to Slack.

4. **Build cohort conversion curves:** Track what percentage of each weekly signup cohort becomes PQLs within 14, 30, and 60 days. Compare cohort curves over time to detect upstream pipeline changes before they affect conversion rates.

5. **Monitor sales-assist deal health:** Maintain Attio lists for stalled deals (no stage change in 14+ days), at-risk deals (engagement score dropped since deal creation), and won deals (current month).

6. **Build the convergence detector:** Track the net conversion lift from each optimization experiment. When the last 3 experiments each produce <2% improvement, the play has reached its local maximum. At convergence, reduce monitoring to biweekly and generate a convergence report.

### 3. Close the feedback loop with NPS

Run the `nps-feedback-loop` drill to collect qualitative signal from upgraded accounts:

1. Trigger NPS surveys 30 days after upgrade via Intercom. Target only accounts that went through the PLG-to-sales pipeline (not manual upgrades).

2. Segment responses by upgrade path (self-serve vs sales-assist) and PQL signal type. Look for patterns: do accounts that upgraded via a plan-limit prompt have different satisfaction than those who upgraded after a sales conversation?

3. Route detractor feedback (NPS 0-6) to the autonomous optimization loop as a signal. If NPS among sales-assisted accounts drops below 30, generate a hypothesis about the sales handoff quality.

4. Route promoter feedback (NPS 9-10) to the `referral-program` or `case-study-candidate-pipeline` drills for expansion.

5. Feed qualitative themes back into hypothesis generation: if detractors consistently cite "the upgrade was pushed on me too early," the agent should test higher PQL thresholds or longer delay before prompting.

### 4. Evaluate sustainability

This level runs continuously for 6 months. Monthly evaluation:

- **Month 1-2:** Autonomous loop stabilizes. First experiments run. Expect some failed experiments as the agent learns the system.
- **Month 3-4:** Winning patterns emerge. Conversion rate should be stable or improving. Experiment velocity should be 2-4 per month.
- **Month 5-6:** Convergence expected. Successive experiments produce diminishing returns. The play reaches its local maximum.

**Success criteria:** Conversion rate sustained at >=45% over 6 months. The autonomous optimization loop runs without human intervention except for high-risk approval gates. If conversion dips below 45% for 2 consecutive weeks, the agent diagnoses and corrects within 1 experiment cycle.

**At convergence:** The agent reports: "This play is optimized. Current performance: [metrics]. Further gains require strategic changes (new plan tiers, product feature changes, new market segments) rather than tactical optimization."

## Time Estimate

- 30 hours: autonomous optimization loop setup and initial calibration
- 20 hours: PLG conversion health monitor dashboard and anomaly detection
- 10 hours: NPS feedback loop configuration and routing
- 60 hours: 6 months of monitoring, experiment cycles, and weekly reports (2.5 hours/week agent-managed)
- 30 hours: monthly reviews, threshold recalibration, convergence analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Pipeline dashboard, anomaly detection, A/B experiments, cohort analysis | Usage-based: ~$50-200/mo at scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app prompts, NPS surveys, sales handoff messages | Advanced: $85/seat/mo; Proactive Support: $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered emails for upgrade and expansion | From $49/mo based on contact count ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly report synthesis | ~$20-50/mo at typical experiment volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Cal.com | Sales booking links | Free tier or $12/seat/mo ([cal.com/pricing](https://cal.com/pricing)) |
| Attio | Deal pipeline, optimization audit trail, campaign records | Standard stack (excluded) |
| n8n | Optimization loop cron, routing workflows, health check automation | Standard stack (excluded) |

**Play-specific cost:** ~$200-650/mo (PostHog usage + Intercom Advanced + Proactive Support + Loops + Anthropic API)

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and report weekly
- `autonomous-optimization` -- build the PLG pipeline dashboard, configure anomaly detection, generate weekly health reports, track cohort conversion curves, and detect convergence
- `nps-feedback-loop` -- collect NPS from upgraded accounts, segment by upgrade path, feed qualitative signals into the optimization loop, and route promoters to expansion programs
