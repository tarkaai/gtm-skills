---
name: executive-demo-durable
description: >
  Executive-Focused Demo — Durable Intelligence. Always-on AI agents finding the
  local maximum of exec demo effectiveness. The autonomous-optimization drill runs
  the core loop: detect metric anomalies per persona, generate improvement hypotheses,
  run A/B experiments on ROI narratives and demo structures, evaluate results, and
  auto-implement winners. Weekly optimization briefs. Converges when successive
  experiments produce <2% improvement.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving exec demo effectiveness (>=75% conversion, >=35% velocity lift) over 6 months via continuous autonomous optimization"
kpis: ["Exec demo conversion trend", "Agent experiment win rate", "Personalization impact", "Deal velocity by exec engagement"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
drills:
  - autonomous-optimization
  - exec-demo-performance-monitor
---

# Executive-Focused Demo — Durable Intelligence

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Exec demo effectiveness sustains or improves over 6 months without manual optimization. The autonomous optimization loop finds the local maximum per persona: the best ROI narrative, demo structure, follow-up sequence, and timing for each executive persona in your market. Weekly optimization briefs explain what changed and why. The system converges when 3 consecutive experiments produce <2% improvement.

## Leading Indicators

- Autonomous optimization loop runs without human intervention for 4+ consecutive weeks
- Experiment win rate >40% (at least 2 of every 5 experiments produce a measurable improvement)
- Weekly optimization brief is generated every Monday with clear per-persona metrics and explanations
- No metric drops >20% for more than 3 consecutive days without auto-detection and response
- Exec demo prep docs incorporate learnings from winning experiments automatically
- Per-persona conversion rates are stable or improving
- Convergence signals appear: successive experiments produce diminishing returns

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the executive-demo play. This is the drill that makes Durable fundamentally different from Scalable. It creates the always-on monitor-diagnose-experiment-evaluate-implement loop.

**Phase 1 -- Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs per persona: exec-demo-to-nextstep rate (overall and per persona), deal velocity lift, exec engagement score correlation with close rate, and ROI narrative effectiveness
2. Compare last 2 weeks against 4-week rolling average. Apply persona-level breakdowns: monitor CEO demos, CFO demos, and CTO demos independently
3. Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2. Include the specific persona and metric affected.

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context: pull current exec demo configuration from Attio (persona templates, ROI narratives, demo structure, follow-up sequences, A/B test winners from Scalable, exec engagement scoring weights)
2. Pull 8-week exec demo metric history from PostHog, segmented by persona
3. Run `hypothesis-generation` with anomaly data + persona context. Example hypotheses:
   - "CFO demo-to-proposal rate dropped because the payback period framing has been unchanged for 4 months and no longer differentiates us from competitors who now use similar language"
   - "CEO demo engagement declined because the peer proof points reference companies from 2025 -- execs want current year proof"
   - "CTO demos are running 25 minutes instead of 15-20, reducing nextstep rates because CTOs interpret long demos as complexity signals"
   - "Multi-exec deals are stalling because the alignment summary does not address the CFO-CEO priority conflict (growth vs cost cutting) explicitly enough"
4. Receive 3 ranked hypotheses with expected impact and risk levels
5. Store hypotheses in Attio as notes on the play's campaign record
6. If top hypothesis has risk = "high": send Slack alert for human review and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment using `posthog-experiments`: create a feature flag that splits exec demos between control (current) and variant (hypothesis change). Stratify by persona to ensure balanced allocation.
3. Implement the variant. Examples:
   - If hypothesis is "CFO payback framing needs refresh": agent generates a new ROI narrative variant for CFOs that leads with risk-adjusted TCO instead of simple payback period. Update the CFO persona template.
   - If hypothesis is "shorter CTO demos convert better": agent adjusts the CTO demo prep template to cover 1 deep technical outcome instead of 2 moderate ones, targeting 12-15 minutes.
   - If hypothesis is "updated peer proof improves CEO engagement": agent queries the case study library for the 3 most recent customer wins and updates the CEO peer proof point.
   - If hypothesis is "faster follow-up improves conversion": agent adjusts follow-up automation timing from 2 hours to 30 minutes post-demo for the target persona.
4. Set experiment duration: minimum 14 days or until 25+ exec demos per variant, whichever is longer. Exec demo volume is lower than email volume, so longer experiments are expected.
5. Log experiment start in Attio: hypothesis, target persona, start date, expected duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog, segmented by persona
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt**: Update the live persona template and ROI narrative to use the winning variant. Update the exec-demo-prep automation to incorporate the change. Log the change, the measured improvement, and the affected persona. Move to Phase 5.
   - **Iterate**: Result was directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert**: Disable the variant, restore control. Log the failure with analysis of why. Return to Phase 1 monitoring.
   - **Extend**: Keep the experiment running for another 14 days if sample size is insufficient.
4. Store the full evaluation in Attio: decision, confidence interval, reasoning, affected persona, and impact on primary KPIs

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected (by persona), hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week, broken down by persona
3. Generate weekly optimization brief:
   - Per-persona performance summary (CEO, CFO, CTO conversion rates and trends)
   - What changed this week and why
   - Net impact on primary KPIs (exec-demo-to-nextstep, deal velocity lift)
   - Active experiments and expected completion dates
   - Exec engagement score correlation update
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Maintain the exec demo performance monitoring system

Run the `exec-demo-performance-monitor` drill continuously. At Durable level, enhance monitoring:

1. **Persona trend detection**: Beyond anomaly detection, track long-term per-persona trends. Is CFO conversion slowly declining while CEO conversion is improving? This suggests market or competitive shifts affecting financial decision-makers specifically.
2. **Exec engagement score recalibration**: Monthly, recalculate the correlation between exec engagement score and deal close rate. If the correlation weakens, adjust scoring weights. The optimization loop can experiment with different weight distributions.
3. **Competitive signal aggregation**: If multiple execs across different deals mention the same competitor in the same week, flag a competitive trend. The optimization loop can test adjusted competitive positioning in the demo.
4. **Seasonality adjustment**: After 3+ months of data, the monitor adjusts baselines for seasonal patterns. Q4 budget freezes affect CFO conversion differently than CEO conversion. Do not flag predictable seasonal patterns as anomalies.
5. **ROI narrative fatigue detection**: Track how long each ROI narrative variant has been in use. After 3 months of the same framing, proactively flag for refresh even if metrics have not degraded yet (preemptive optimization).

### 3. Apply guardrails

Follow the autonomous-optimization guardrails strictly:

- **Rate limit**: Maximum 1 active experiment at a time. Exec demo volume is lower than email volume, so stacking experiments produces unreadable results.
- **Revert threshold**: If exec-demo-to-nextstep rate drops >30% during an experiment (for the affected persona), auto-revert immediately.
- **Human approval required for**:
  - Changes to the exec demo structure that affect all personas (not just one)
  - Changes to ROI narrative methodology (e.g., switching from conservative to moderate projections)
  - Any experiment the hypothesis generator flags as "high risk"
  - Changes to exec engagement scoring weights
- **Cooldown**: After a failed experiment, wait 14 days (not 7, due to lower exec demo volume) before testing the same variable for the same persona again.
- **Maximum experiments per month**: 2 (lower than the standard 4, because exec demo sample sizes are smaller and each experiment needs longer to reach significance).
- **Persona isolation**: Never change templates for two personas simultaneously. If a CEO experiment is running, do not start a CFO experiment until the CEO experiment completes.

### 4. Detect convergence

The optimization loop detects convergence when:
- 3 consecutive experiments produce <2% improvement on primary KPIs across all personas
- Per-persona exec-demo-to-nextstep rates have been stable within +/-3% for 8+ weeks
- No new anomalies detected for 4+ weeks
- Exec engagement score correlation with close rate has been stable for 4+ weeks

At convergence:
1. The play has reached its local maximum for current market conditions
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment frequency from 2/month to 1/month (maintenance mode)
4. Generate a convergence report:
   - "Exec demo play is optimized. Current per-persona performance: CEO {rate}%, CFO {rate}%, CTO {rate}%. Deal velocity lift: {rate}%. Exec engagement score correlation: {r}."
   - "Further gains require strategic changes (new product capabilities, new exec personas to target, new market segments) rather than tactical demo optimization."
   - Ranked list of what worked: top ROI narratives per persona, optimal demo duration, most effective follow-up format
5. Post convergence report to Slack and store in Attio

### 5. Evaluate sustainability

After 6 months:
- Primary: Exec-demo-to-nextstep rate sustained at >=75% (no persistent drops below this threshold for any persona)
- Primary: Exec-engaged deals close >=35% faster than non-exec deals (sustained)
- Secondary: At least 6 experiments completed, with >=40% win rate
- Secondary: Weekly optimization briefs generated for all 26 weeks
- Secondary: Convergence detected or clear upward trend still active
- Secondary: Per-persona optimization has identified the best ROI narrative, demo structure, and follow-up format for each persona

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay despite optimization, diagnose whether the issue is:
- **Market saturation**: Execs in your target market have seen too many similar demos. Test new positioning angles.
- **Competitive pressure**: A competitor has adopted similar exec demo strategies. Differentiate on depth of personalization or proof quality.
- **ICP drift**: Your product has evolved and the exec personas you target need to shift. Re-run persona analysis.
- **Exec fatigue**: The same execs are receiving multiple vendor demos with similar ROI framing. Test differentiated formats (async video briefings, interactive ROI calculators, executive roundtables).

## Time Estimate

- 15 hours: initial setup (autonomous optimization loop, enhanced monitoring, guardrails, persona-level configuration)
- 4 hours/month: review weekly optimization briefs and approve high-risk experiments (24 hours total)
- 2 hours/month: monthly strategic review of exec demo playbook and per-persona experiment results (12 hours total)
- 14 hours/week initially declining: ongoing exec demo execution by founder (84 hours total over 6 months, declining as team scales)
- **Total: ~135 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, experiment logs, persona templates, optimization history | Plus $29/user/mo |
| PostHog | Analytics -- funnel tracking, experiments, feature flags, anomaly detection, exec engagement dashboards | Usage-based; ~$50-200/mo at this volume |
| Fireflies | Transcription -- all exec demo calls recorded and analyzed for quality scoring | Business $19/user/mo |
| Cal.com | Scheduling -- exec demo booking | Free (1 user); Teams $15/user/mo |
| Clay | Enrichment -- exec research with automatic freshness refresh | Growth $349/mo (12,000 credits) |
| n8n | Automation -- optimization loop, monitoring, prep pipeline, follow-up, reporting | Pro $60/mo cloud; or free self-hosted |
| Anthropic API | AI -- hypothesis generation, experiment evaluation, ROI narrative generation, quality scoring, persona optimization | ~$75-200/mo (daily monitoring + experiment analysis + exec demo prep at volume) |

**Estimated play-specific cost at Durable:** ~$350-700/mo (Fireflies Business + Clay Growth + n8n Pro + PostHog usage + Anthropic API for optimization loop)

## Drills Referenced

- `autonomous-optimization` -- the always-on monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum of exec demo effectiveness per persona
- `exec-demo-performance-monitor` -- continuous monitoring of exec demo funnel with per-persona trend detection, exec engagement score recalibration, competitive signal aggregation, and ROI narrative fatigue detection
