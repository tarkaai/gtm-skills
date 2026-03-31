---
name: roi-skepticism-objection-durable
description: >
  ROI Skepticism Handling — Durable Intelligence. Always-on AI agents finding the
  local maximum of ROI skepticism resolution. The autonomous-optimization drill
  runs the core loop: detect metric anomalies, generate improvement hypotheses,
  run A/B experiments, evaluate results, and auto-implement winners. Weekly
  optimization briefs. Quarterly accuracy calibration auto-corrects model
  projections. Converges when successive experiments produce <2% improvement.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving ROI skepticism resolution (>=80%) and post-sale accuracy (>=75%) over 6 months via continuous autonomous optimization and self-calibrating models"
kpis: ["ROI skepticism resolution trend", "Post-sale ROI accuracy trend", "Agent experiment win rate", "Model self-calibration effectiveness", "Optimization convergence rate"]
slug: "roi-skepticism-objection"
install: "npx gtm-skills add sales/aligned/roi-skepticism-objection"
drills:
  - autonomous-optimization
  - roi-skepticism-intelligence-monitor
---

# ROI Skepticism Handling — Durable Intelligence

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

ROI skepticism resolution sustains or improves over 6 months without manual optimization. The autonomous optimization loop finds the local maximum: the best proof assets, presentation formats, follow-up sequences, persona-specific narratives, and model calibration for your market. Self-calibrating ROI models get more accurate over time as post-sale data feeds back into projections. Weekly optimization briefs explain what changed and why. The system converges when 3 consecutive experiments produce < 2% improvement.

## Leading Indicators

- Autonomous optimization loop runs without human intervention for 4+ consecutive weeks
- Experiment win rate > 40% (at least 2 of every 5 experiments produce a measurable improvement)
- Weekly optimization brief generated every Monday with clear metrics and explanations
- No metric drops > 20% for more than 3 consecutive days without auto-detection and response
- Post-sale ROI accuracy improves quarter over quarter as calibration adjustments accumulate
- Model acceptance rate improves as over-projected claims are automatically corrected
- Convergence signals appear: successive experiments produce diminishing returns

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the ROI skepticism handling play. This is the drill that makes Durable fundamentally different from Scalable. It creates the always-on monitor-diagnose-experiment-evaluate-implement loop.

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs: resolution rate, model acceptance rate, proof asset engagement, post-sale accuracy, and persona-specific resolution rates
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: pull current ROI handling configuration from Attio (proof assets in use, follow-up sequences, model parameters, calibration factors, A/B test winners from Scalable)
2. Pull 8-week ROI skepticism metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + context. The `roi-skepticism-intelligence-monitor` drill feeds domain-specific hypotheses. Examples:
   - "Model acceptance rate dropped because the primary case study is 6+ months old. Experiment: replace with a customer validated in the last 90 days."
   - "CFO resolution rate (42%) is dragging down overall resolution. Experiment: generate CFO-specific ROI narratives emphasizing NPV and cost-avoidance rather than revenue-increase."
   - "Post-sale accuracy for the revenue_increase driver dropped to 48%. Experiment: apply a 0.65x calibration factor to revenue projections and test whether calibrated models have higher prospect acceptance."
   - "Collaborative calculator usage declined from 70% to 45% — sellers are reverting to PDF business cases. Experiment: auto-default to calculator format and measure resolution rate difference."
4. Receive 3 ranked hypotheses with expected impact and risk levels
5. Store hypotheses in Attio as notes on the play's campaign record
6. If top hypothesis has risk = "high": send Slack alert for human review and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment using `posthog-experiments`: create a feature flag that splits qualifying deals between control (current) and variant (hypothesis change)
3. Implement the variant. Examples:
   - If hypothesis is "calibrated models increase acceptance": agent adjusts `roi-model-generation` prompt to include calibration factors for the variant group
   - If hypothesis is "persona-specific narratives improve CFO resolution": agent routes CFO-persona deals in the variant to `roi-narrative-generation` with cost-avoidance framing
   - If hypothesis is "newer case studies improve proof engagement": agent swaps the case study attachment in the proof_demand follow-up sequence
   - If hypothesis is "pre-emptive presentation prevents skepticism": agent adjusts the predictive scoring threshold to trigger earlier for the variant group
4. Set experiment duration: minimum 14 days or until 20+ deals per variant, whichever is longer (ROI skepticism is a subset of all deals, so sample sizes are smaller)
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt**: Update live configuration to use the winning variant. Log the change and measured improvement. Move to Phase 5.
   - **Iterate**: Result was directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
   - **Revert**: Disable the variant, restore control. Log the failure with analysis. Return to Phase 1 monitoring.
   - **Extend**: Keep the experiment running for another 14 days if sample size insufficient.
4. Store the full evaluation in Attio: decision, confidence interval, reasoning, and impact on primary KPIs

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on primary KPIs (resolution rate, model acceptance, accuracy)
   - Active experiments and expected completion dates
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Maintain the ROI skepticism monitoring system

Run the `roi-skepticism-intelligence-monitor` drill continuously. This is the play-specific monitoring layer that feeds the autonomous optimization loop with domain context. At Durable level, the monitor provides:

1. **8-panel dashboard**: resolution rate trends, model acceptance, proof asset engagement, time-to-resolution, collaborative model funnel, post-sale accuracy scatter, persona effectiveness heatmap, revenue preserved scorecard
2. **Daily anomaly detection**: flags resolution rate drops, model acceptance declines, proof asset staleness, accuracy degradation, and persona-specific issues
3. **Domain-specific hypotheses**: when anomalies are detected, generates ROI-skepticism-specific hypotheses (not generic optimization hypotheses) that reference proof assets, model calibration, persona framing, and accuracy data
4. **Weekly intelligence report**: summarizes ROI skepticism metrics, top/worst proof assets, persona breakdown, revenue impact, and recommended actions
5. **Quarterly accuracy calibration**: runs `roi-accuracy-scoring` across all measured deals, computes correction factors per value driver, and automatically updates `roi-model-generation` prompts. This creates the self-correcting feedback loop where models improve automatically over time.

The quarterly calibration is what makes this play uniquely powerful at Durable. Most companies' ROI claims get less credible over time as market conditions change. Self-calibrating models get more credible because they are continuously corrected by real customer data.

### 3. Apply guardrails

Follow the autonomous-optimization guardrails strictly:

- **Rate limit**: Maximum 1 active experiment at a time. ROI skepticism deal volume is lower than total deal volume, so stacking experiments produces unreadable results.
- **Revert threshold**: If resolution rate drops > 30% during an experiment, auto-revert immediately.
- **Human approval required for**:
  - Changes to ROI model methodology (calibration factors > 0.3x adjustment)
  - Changes to the post-sale accuracy measurement approach
  - Customer-facing proof assets that reference specific customer data (even anonymized)
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown**: After a failed experiment, wait 14 days before testing the same variable again.
- **Maximum experiments per month**: 2 (ROI skepticism is a subset of all deals; sample sizes need longer to reach significance).
- **Accuracy floor**: Never auto-implement a calibration that would cause projected ROI to drop below the pain-to-price breakeven point. If calibration suggests the product does not deliver positive ROI for a segment, flag for strategic review rather than auto-adjusting.

### 4. Detect convergence

The optimization loop detects convergence when:
- 3 consecutive experiments produce < 2% improvement on resolution rate or model acceptance
- Post-sale accuracy has been stable within +/-5% for 2+ quarters
- No new anomalies detected for 4+ weeks
- All persona-specific resolution rates are within 15% of overall average (no segment being left behind)

At convergence:
1. The play has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment frequency from 2/month to 1/month (maintenance mode)
4. Continue quarterly accuracy calibration (this never stops — market conditions change)
5. Generate convergence report: "ROI skepticism handling is optimized. Current performance: [metrics]. Post-sale accuracy: [X]%. Further gains require strategic changes (new product capabilities, new market segments, pricing model changes) rather than tactical optimization."
6. Post convergence report to Slack and store in Attio

### 5. Evaluate sustainability

After 6 months:
- Primary: Resolution rate sustained at >= 80% (no persistent drops below this threshold)
- Primary: Post-sale ROI accuracy >= 75% mean (improving from Scalable's >= 70%)
- Secondary: At least 6 experiments completed with >= 40% win rate
- Secondary: Weekly optimization briefs generated for all 26 weeks
- Secondary: Quarterly accuracy calibration ran 2x with measurable accuracy improvement
- Secondary: Convergence detected or clear upward trend still active

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay despite optimization, diagnose: is the problem market shift (buyer expectations changed), competitive pressure (competitors now offer comparable ROI proof), product change (features changed but ROI models were not updated), or data degradation (post-sale measurement coverage declining).

## Time Estimate

- 15 hours: initial setup (autonomous optimization loop, enhanced monitoring, dashboard, guardrails, quarterly calibration workflow)
- 4 hours/month: review weekly optimization briefs and approve high-risk experiments: 24 hours total
- 2 hours/month: monthly strategic review of ROI handling approach and experiment results: 12 hours total
- 3 hours/quarter: quarterly accuracy calibration review and model adjustment approval: 6 hours total
- 15 hours/week declining to 5 hours/week: ongoing ROI presentations by founder at scale: ~93 hours total over 6 months
- **Total: ~150 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, experiment logs, optimization history, accuracy tracking | Plus $29/user/mo |
| PostHog | Analytics — funnel tracking, experiments, feature flags, anomaly detection, accuracy analysis | Usage-based; ~$100-250/mo at this volume |
| Fireflies | Transcription — all calls for auto-detection and quality scoring | Business $19/user/mo |
| n8n | Automation — optimization loop, monitoring, auto-generation pipeline, calibration workflows | Pro $60/mo cloud; or free self-hosted |
| Instantly | Email sequences — follow-up delivery at scale | Hypergrowth $77.6/mo |
| Clay | Enrichment — company data, persona enrichment, competitive intel | Explorer $149/mo |
| Anthropic API | AI — hypothesis generation, experiment evaluation, model generation, calibration, narrative generation | ~$100-250/mo (daily monitoring + experiments + model generation + calibration) |

**Estimated play-specific cost at Durable:** ~$300-700/mo (PostHog usage + Clay + Instantly + Anthropic API for optimization loop + n8n Pro)

## Drills Referenced

- `autonomous-optimization` — the always-on monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum of ROI skepticism resolution effectiveness
- `roi-skepticism-intelligence-monitor` — continuous monitoring of ROI skepticism patterns, model effectiveness, proof asset engagement, persona-specific resolution, and post-sale accuracy with quarterly self-calibration
