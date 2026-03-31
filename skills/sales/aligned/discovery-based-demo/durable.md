---
name: discovery-based-demo-durable
description: >
  Discovery-Based Demo — Durable Intelligence. Always-on AI agents finding the
  local maximum of demo effectiveness. The autonomous-optimization drill runs the
  core loop: detect metric anomalies, generate improvement hypotheses, run A/B
  experiments, evaluate results, and auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving demo effectiveness (>=70% next-step, >=45% proposal conversion) over 6 months via continuous autonomous optimization"
kpis: ["Demo conversion trends", "Agent experiment win rate", "Demo engagement score", "Optimization convergence rate"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
drills:
  - autonomous-optimization
  - demo-performance-monitor
---

# Discovery-Based Demo — Durable Intelligence

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes

Demo effectiveness sustains or improves over 6 months without manual optimization. The autonomous optimization loop finds the local maximum: the best demo structure, pain narrative, follow-up sequence, and timing for your market. Weekly optimization briefs explain what changed and why. The system converges when 3 consecutive experiments produce <2% improvement.

## Leading Indicators

- Autonomous optimization loop runs without human intervention for 4+ consecutive weeks
- Experiment win rate >40% (at least 2 of every 5 experiments produce a measurable improvement)
- Weekly optimization brief is generated every Monday with clear metrics and explanations
- No metric drops >20% for more than 3 consecutive days without auto-detection and response
- Demo prep docs incorporate learnings from winning experiments automatically
- Convergence signals appear: successive experiments produce diminishing returns

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the discovery-based-demo play. This is the drill that makes Durable fundamentally different from Scalable. It creates the always-on monitor-diagnose-experiment-evaluate-implement loop.

**Phase 1 -- Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs: demo-to-nextstep rate, demo-to-proposal rate, pain coverage effectiveness, and recap video engagement
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context: pull current demo configuration from Attio (demo structure, pain-feature mappings, follow-up sequence, A/B test winners from Scalable)
2. Pull 8-week demo metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + context. Example hypotheses:
   - "Demo-to-proposal rate dropped because the follow-up email subject line has fatigued after 3 months of use"
   - "Pain coverage effectiveness declined because the product shipped Feature X which creates a better mapping for Pain Y, but the feature catalog was not updated"
   - "Prospect engagement dropped because demos are running 10 minutes longer than optimal (detected from duration data)"
4. Receive 3 ranked hypotheses with expected impact and risk levels
5. Store hypotheses in Attio as notes on the play's campaign record
6. If top hypothesis has risk = "high": send Slack alert for human review and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment using `posthog-experiments`: create a feature flag that splits prospects between control (current) and variant (hypothesis change)
3. Implement the variant. Examples:
   - If hypothesis is "shorter demos convert better": agent adjusts demo prep doc template to cover 2 pains instead of 3, reducing target duration
   - If hypothesis is "faster follow-up converts better": agent adjusts follow-up automation timing from 2 hours to 30 minutes post-demo
   - If hypothesis is "different opening converts better": agent updates demo prep template to use a new opening structure
4. Set experiment duration: minimum 14 days or until 25+ demos per variant, whichever is longer (demo volume is lower than email volume, so longer experiments are needed)
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt**: Update live demo prep templates and follow-up workflows to use the winning variant. Log the change and the measured improvement. Move to Phase 5.
   - **Iterate**: The result was directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert**: Disable the variant, restore control. Log the failure with analysis of why. Return to Phase 1 monitoring.
   - **Extend**: Keep the experiment running for another 14 days if sample size is insufficient.
4. Store the full evaluation in Attio: decision, confidence interval, reasoning, and impact on primary KPIs

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on primary KPIs (demo-to-nextstep, demo-to-proposal)
   - Active experiments and expected completion dates
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Maintain the demo performance monitoring system

Run the `demo-performance-monitor` drill continuously. At Durable level, enhance monitoring:

1. **Trend detection**: Beyond anomaly detection, track long-term trends. Is demo-to-proposal rate slowly declining (market shift) or slowly improving (optimization working)?
2. **Segment analysis**: Break down performance by prospect segment. Are enterprise prospects converting differently than SMB? Has a specific industry vertical started performing better? Surface segment-level opportunities.
3. **Competitive signal detection**: If multiple prospects mention the same competitor feature in discovery, flag it. The optimization loop can test demo responses to competitive pressure.
4. **Seasonality adjustment**: After 3+ months of data, the monitor adjusts baselines for seasonal patterns. Do not flag Q4 budget freezes as anomalies.

### 3. Apply guardrails

Follow the autonomous-optimization guardrails strictly:

- **Rate limit**: Maximum 1 active experiment at a time. Demo volume is lower than email volume, so stacking experiments produces unreadable results.
- **Revert threshold**: If demo-to-nextstep rate drops >30% during an experiment, auto-revert immediately.
- **Human approval required for**:
  - Changes to the demo structure that affect >50% of demos
  - Changes to the product feature catalog or pain mappings
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown**: After a failed experiment, wait 14 days (not 7, due to lower demo volume) before testing the same variable again.
- **Maximum experiments per month**: 2 (lower than the standard 4, because demo sample sizes are smaller and each experiment needs longer to reach significance).

### 4. Detect convergence

The optimization loop detects convergence when:
- 3 consecutive experiments produce <2% improvement on the primary KPIs
- The demo-to-nextstep rate has been stable within +/-3% for 8+ weeks
- No new anomalies have been detected for 4+ weeks

At convergence:
1. The play has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment frequency from 2/month to 1/month (maintenance mode)
4. Generate a convergence report: "Demo play is optimized. Current performance: [metrics]. Further gains require strategic changes (new product features, new ICP segments, new channels) rather than tactical demo optimization."
5. Post convergence report to Slack and store in Attio

### 5. Evaluate sustainability

After 6 months:
- Primary: Demo-to-nextstep rate sustained at >=70% (no persistent drops below this threshold)
- Primary: Demo-to-proposal rate sustained at >=45%
- Secondary: At least 6 experiments completed, with >=40% win rate
- Secondary: Weekly optimization briefs generated for all 26 weeks
- Secondary: Convergence detected or clear upward trend still active

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay despite optimization, diagnose whether the issue is market saturation, competitive pressure, ICP drift, or product-market fit shift.

## Time Estimate

- 15 hours: initial setup (autonomous optimization loop, enhanced monitoring, guardrails)
- 4 hours/month: review weekly optimization briefs and approve high-risk experiments (24 hours total)
- 2 hours/month: monthly strategic review of demo playbook and experiment results (12 hours total)
- 14 hours/week: ongoing demo execution by founder (scaled back as play is optimized) (84 hours total over 6 months, declining)
- **Total: ~135 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, experiment logs, optimization history | Plus $29/user/mo |
| PostHog | Analytics -- funnel tracking, experiments, feature flags, anomaly detection | Usage-based; ~$50-200/mo at this volume |
| Fireflies | Transcription -- all calls recorded and analyzed for quality scoring | Business $19/user/mo |
| Cal.com | Scheduling -- demo booking | Free (1 user); Teams $15/user/mo |
| Loom | Video -- recap videos with engagement tracking | Business $12.50/user/mo |
| n8n | Automation -- optimization loop, monitoring, prep pipeline, follow-up | Pro $60/mo cloud; or free self-hosted |
| Anthropic API | AI -- hypothesis generation, experiment evaluation, demo prep, quality scoring | ~$50-150/mo (daily monitoring + experiment analysis + demo prep) |

**Estimated play-specific cost at Durable:** ~$200-500/mo (Fireflies Business + Loom Business + n8n Pro + PostHog usage + Anthropic API for optimization loop)

## Drills Referenced

- `autonomous-optimization` -- the always-on monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum of demo effectiveness
- `demo-performance-monitor` -- continuous monitoring of the discovery-to-demo-to-deal funnel with segment analysis and trend detection
