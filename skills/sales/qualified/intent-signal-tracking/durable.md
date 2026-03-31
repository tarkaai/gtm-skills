---
name: intent-signal-tracking-durable
description: >
  Intent Signal Tracking — Durable Intelligence. Deploy autonomous optimization that continuously
  monitors scoring accuracy, detects signal decay, runs experiments on weights and thresholds,
  and auto-implements improvements. The agent finds and maintains the local maximum of intent-driven
  outreach performance.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving intent-driven conversion (>=3x vs cold) over 6 months with autonomous agent optimization achieving <2% improvement delta indicating local maximum reached"
kpis: ["Intent conversion rate (Hot vs Cold ratio)", "Scoring model precision and recall", "Agent experiment win rate", "Signal-to-meeting pipeline velocity"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Intent Signal Tracking — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

Deploy always-on AI agents that autonomously monitor, diagnose, experiment, and optimize the intent signal tracking pipeline. The `autonomous-optimization` drill runs the core loop: detect when scoring accuracy degrades or conversion rates plateau, generate hypotheses (adjust signal weights, add new signal sources, change tier thresholds, modify outreach cadence), run controlled experiments, evaluate results, and auto-implement winners. The system converges when successive experiments produce <2% improvement, indicating the local maximum has been reached.

## Leading Indicators

- Weekly optimization briefs are generating actionable hypotheses (not just "everything looks fine")
- At least 1 experiment is running at all times during the first 3 months
- Scoring model precision stays above 15% and recall above 50%
- Signal sources are being automatically validated — any source with zero signals for 7 days triggers an alert
- Hot:Cold conversion ratio is stable or improving month over month
- Signal-to-outreach time median remains under 30 minutes despite volume growth

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for intent signal tracking. The optimization loop monitors these play-specific KPIs:

**Primary KPI:** Hot-tier conversion rate (replied + meeting_booked) vs Cold-tier conversion rate. Target ratio: >=3x.

**Secondary KPIs:**
- Scoring model precision (% of Hot accounts that respond)
- Scoring model recall (% of responding accounts that were scored Hot)
- Signal-to-outreach median time
- Reply rate by signal source
- Meeting-to-deal conversion by intent tier

Configure the `autonomous-optimization` drill phases:

**Phase 1 — Monitor (daily cron via n8n):**
Use `posthog-anomaly-detection` to check all KPIs against 4-week rolling averages. Classify as normal (within 10%), plateau (within 2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). For intent signal tracking specifically, also monitor:
- Signal source health: each source (website, G2, enrichment) producing expected volume
- Score distribution shift: if the percentage of Hot accounts drifts above 25% or below 3%, the model is miscalibrated
- Decay effectiveness: if stale accounts are not dropping tiers, decay multipliers need adjustment

**Phase 2 — Diagnose (triggered by anomaly):**
When an anomaly is detected, the agent generates hypotheses specific to intent signal tracking:

*Scoring model hypotheses:*
- "Pricing page visits are overweighted — reduce from 15 to 10 points" (if Hot accounts that only have website signals convert poorly)
- "G2 signals are underweighted — increase from 20 to 30 points" (if G2-sourced Hot accounts convert at 2x the rate of website-sourced)
- "Decay is too aggressive — extend the 7-day full-value window to 14 days" (if accounts with signals 8-14 days old still convert well)
- "Add a signal for repeat G2 visits — companies that check alternatives twice in a week are 4x more likely to convert"

*Outreach hypotheses:*
- "Hot-tier outreach timing has degraded — test immediate vs next-morning send"
- "AI personalization is producing generic outputs — tighten the Claygent prompt with more signal context"
- "Warm-tier cadence is too slow — test 3-day gaps instead of 4-day"

*Pipeline hypotheses:*
- "Reply-to-meeting conversion is dropping — the positive reply follow-up is too slow"
- "A new competitor is capturing intent signals before us — add their name to G2 monitoring"

Store top 3 hypotheses in Attio. If any hypothesis is flagged high-risk (changes scoring weights by >30% or affects >50% of outreach volume), send for human approval.

**Phase 3 — Experiment (automated):**
Take the top hypothesis and design the experiment using `posthog-experiments`:
- For scoring model changes: create a feature flag that splits incoming accounts 50/50 between current model and variant model. Run both scoring models in parallel for 2 weeks. Compare conversion rates.
- For outreach changes: use Instantly A/B testing to split outreach variants. Run for 100+ sends per variant.
- For pipeline changes: implement the change on 50% of flow through n8n branch nodes.

Maximum 1 active experiment at a time. Minimum duration: 7 days or 100 samples per variant.

**Phase 4 — Evaluate (on experiment completion):**
Pull results from PostHog. Apply the decision framework:
- **Adopt:** Variant outperforms control by >=5% with 95% confidence. Update the live configuration.
- **Iterate:** Variant shows directional improvement but not statistically significant. Generate a refined hypothesis.
- **Revert:** Variant underperforms. Restore control. Wait 7 days before testing the same variable.
- **Extend:** Insufficient data. Continue the experiment for another period.

Log all decisions in Attio with full reasoning.

**Phase 5 — Report (weekly cron):**
Generate a weekly optimization brief covering:
- Experiments completed and their outcomes
- Net impact on primary KPI (Hot:Cold conversion ratio)
- Current estimated distance from local maximum
- Signal source performance ranking
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Deploy play-specific health monitoring

Run the `autonomous-optimization` drill to build:

- **Signal pipeline dashboard** in PostHog with 6 panels: signal volume by source, score distribution, signal-to-outreach time, outreach funnel by tier, scoring accuracy comparison, and decay impact
- **Weekly health check** n8n workflow that compares all metrics to rolling averages and flags anomalies
- **Monthly scoring audit** that computes precision and recall of the scoring model and recommends recalibration when accuracy drops

The health monitor feeds anomalies directly into the autonomous optimization loop (Phase 1).

### 3. Build the executive dashboard

Run the `dashboard-builder` drill to create a high-level "Intent Signal ROI" dashboard:

- **Pipeline attributed to intent**: total deal value from accounts sourced via intent signals
- **Cost per intent-sourced meeting**: total tool spend / meetings from intent outreach
- **Intent lift**: conversion rate multiplier of intent vs cold outreach, trended monthly
- **Time to ROI**: cumulative tool cost vs cumulative deal value from intent-sourced accounts
- **Optimization trajectory**: chart of experiment results over time, showing convergence toward local maximum

### 4. Manage convergence

The autonomous optimization loop should detect convergence — when 3 consecutive experiments produce <2% improvement. At convergence:

1. The play has reached its local maximum for current market conditions
2. Reduce the monitoring cron from daily to weekly
3. Reduce experiment frequency from continuous to monthly maintenance checks
4. Generate a convergence report:
   - Current performance (all KPIs with benchmarks)
   - Optimizations implemented (list of all winning experiments)
   - What would require strategic change to improve further (new channels, new signal sources, product changes)
5. Shift agent effort to other plays that have not yet converged

If market conditions change (new competitor, product pivot, ICP shift), reset convergence status and resume active optimization.

### 5. Handle model drift

Intent signals degrade over time as markets evolve. The autonomous agent must detect and respond to drift:

- **Signal source degradation**: if a source that previously produced 30% of Hot accounts drops to 10%, investigate whether the source is broken or the market shifted
- **Outreach fatigue**: if reply rates trend down despite stable scoring accuracy, the market is developing resistance to your messaging patterns. Trigger a complete messaging refresh experiment.
- **ICP evolution**: if accounts that score Hot are converting at lower rates, your ICP may have shifted. Flag for human strategic review — the scoring model assumes a stable ICP.
- **Competitive displacement**: if G2 "compare" signals shift from your product to a new competitor, the buying landscape changed. Alert the team and add the new competitor to monitoring.

## Time Estimate

- 15 hours: configure autonomous optimization loop (all 5 phases)
- 8 hours: build intent signal health monitor (dashboard + weekly + monthly workflows)
- 5 hours: build executive ROI dashboard
- 60 hours: ongoing monitoring, experiment management, and analysis over 6 months (~10 hr/month)
- 20 hours: responding to anomalies, recalibrating models, handling drift
- 12 hours: convergence analysis, documentation, and strategic recommendations

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| RB2B Pro+ | Website visitor identification | $149/mo |
| Clay Explorer/Pro | Intent scoring + enrichment | $149-349/mo |
| Instantly Hypergrowth | Email sequencing at scale | $77-286/mo |
| PostHog | Analytics, experiments, anomaly detection | Scale plan $0+ (usage-based) |
| Attio | CRM, deal tracking, optimization logging | Pro $29/user/mo |
| n8n | Automation (6+ workflows) | Pro $60/mo |
| G2 Buyer Intent | Third-party intent signals | Included in G2 paid profile |
| Anthropic API | Hypothesis generation + evaluation (Claude) | ~$20-50/mo at optimization volume |

**Total play-specific cost: ~$300-600/mo** (excluding optional Bombora)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `autonomous-optimization` — play-specific monitoring for signal pipeline health, scoring accuracy, and conversion tracking
- `dashboard-builder` — executive ROI dashboard showing intent signal pipeline value
