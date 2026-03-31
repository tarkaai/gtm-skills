---
name: retargeting-campaigns-multi-platform-durable
description: >
  Multi-platform Retargeting — Durable Intelligence. Always-on AI agents monitor
  retargeting health, detect anomalies, generate improvement hypotheses, run A/B
  experiments, and auto-implement winners. The autonomous-optimization loop finds
  and maintains the local maximum of retargeting ROI across all platforms.
stage: "Marketing > Product Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained >=60 conversions/month and CPA trending flat or down over 12 months via autonomous creative, audience, and budget optimization"
kpis: ["Sustained monthly conversions", "CPA trend (flat or declining)", "Experiment win rate", "Time to anomaly resolution", "Convergence score"]
slug: "retargeting-campaigns-multi-platform"
install: "npx gtm-skills add marketing/product-aware/retargeting-campaigns-multi-platform"
drills:
  - autonomous-optimization
---

# Multi-platform Retargeting — Durable Intelligence

> **Stage:** Marketing → Product Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Achieve sustained retargeting performance at the local maximum: >=60 conversions/month with CPA trending flat or down over 12 months. The autonomous-optimization loop detects when performance degrades, generates hypotheses for why, runs controlled experiments, evaluates results, and auto-implements winners — all without human intervention for routine decisions. Human involvement is limited to approving high-risk changes and monthly strategic reviews.

## Leading Indicators

- Autonomous-optimization loop fires daily without errors (verify in n8n execution logs)
- Anomaly detection catches CPA spikes within 24 hours (before they compound into weekly performance drops)
- At least 1 experiment is running at all times (no idle periods longer than 7 days)
- Experiment win rate >= 30% over rolling 3-month window (if < 30%, the hypothesis generator needs retuning)
- Weekly optimization briefs are generated and posted to Slack every Monday
- No creative runs longer than 28 days without being replaced
- Cross-platform audience sync has zero failed runs in the last 30 days
- Convergence detection fires correctly when successive experiments produce < 2% improvement

## Instructions

### 1. Deploy the autonomous-optimization loop

Run the `autonomous-optimization` drill configured for retargeting:

**Phase 1 — Monitor (daily via n8n cron at 06:00 UTC):**

1. Use `posthog-anomaly-detection` to check the 5 core retargeting KPIs:
   - Blended CPA across all platforms
   - CTR by platform
   - Landing page conversion rate
   - Lead quality rate (% of conversions that become qualified leads in Attio)
   - Budget utilization rate (actual spend / allocated budget)

2. Compare last 14 days against 4-week rolling average. Classify each KPI:
   - **Normal**: within +/- 10% of average
   - **Plateau**: within +/- 2% for 3+ consecutive weeks
   - **Drop**: > 20% decline
   - **Spike**: > 50% increase (could be positive or negative depending on the metric)

3. If all KPIs are normal: log status to Attio, no action needed.
4. If any anomaly detected: pass the anomaly data to Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

1. Gather context via the `autonomous-optimization` drill:
   - Pull the retargeting health dashboard data from PostHog
   - Check creative fatigue status (any creatives with CTR declining > 30%)
   - Check audience exhaustion indicators (frequency > 5 on any segment)
   - Check budget utilization (underspend signals audience exhaustion)
   - Pull platform-level data from Meta, LinkedIn, and Google APIs

2. Run `hypothesis-generation` with context:
   ```
   Anomaly: {kpi} has {classification} — current value {value} vs. baseline {baseline}
   Platform breakdown: Meta CPA={x}, LinkedIn CPA={y}, Google CPA={z}
   Creative status: {N} active, {M} fatigued, oldest running {D} days
   Audience status: high-intent freq={f1}, medium-intent freq={f2}
   Budget: {utilization}% of allocated spend actually used

   Generate 3 ranked hypotheses for this anomaly.
   For each: the specific retargeting variable to change, the expected impact, risk level, and the experiment to run.
   ```

3. Store hypotheses in Attio. If top hypothesis has risk = "high" (budget change > 20%, major audience change, or total spend > $10,000/mo): send Slack alert for human review and STOP. If risk = "low" or "medium": proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Design the experiment based on the top hypothesis. Retargeting-specific experiment types:

   | Hypothesis Category | Experiment Design | Minimum Duration |
   |---|---|---|
   | Creative fatigue causing CTR drop | Launch 3 new variants, A/B test against current best performer | 14 days or 200 clicks per variant |
   | Audience exhaustion causing CPA rise | Test broadened audience window (14d -> 30d) vs. current | 14 days or 100 conversions per variant |
   | Platform mix suboptimal | Shift 20% budget from worst CPA platform to best, measure blended CPA | 14 days |
   | Landing page conversion rate dropped | A/B test new landing page variant via PostHog feature flag | 14 days or 200 visits per variant |
   | Frequency too high | Reduce frequency cap by 50%, measure CPA impact | 7 days |

2. Set up the experiment using `posthog-experiments` (for landing page tests) or the platform's native A/B testing (for creative/audience tests)
3. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, variant details

**Phase 4 — Evaluate (triggered by experiment reaching sample size or duration):**

1. Pull experiment results from PostHog or platform APIs
2. Run `experiment-evaluation`:
   - **Adopt**: Statistically significant winner (>= 95% confidence) with practical significance (>= 5% improvement). Implement the winning variant as the new default. Log the change.
   - **Iterate**: Directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert**: Variant performed worse than control. Disable variant, restore control. Enter 7-day cooldown before testing the same variable again.
   - **Extend**: Promising results but insufficient sample size. Extend experiment duration by 7 days.

3. Store full evaluation in Attio: decision, confidence level, metric impact, and reasoning.

**Phase 5 — Report (weekly via n8n cron, Monday 09:00 UTC):**

1. Aggregate all optimization activity for the week
2. Generate a weekly retargeting optimization brief using Claude:
   - Anomalies detected and how they were resolved
   - Experiments running: current status and preliminary results
   - Experiments completed: winner/loser, net impact on CPA and conversions
   - Creative rotation: ads launched, ads paused, current active creative count
   - Budget allocation: per-platform spend and CPA
   - Convergence status: are successive experiments producing diminishing returns?
   - Recommendation for next week's focus area
3. Post brief to Slack and store in Attio

### 2. Deploy the retargeting performance monitor

Run the `autonomous-optimization` drill to set up always-on monitoring that feeds the optimization loop:

1. Build the 6-panel PostHog dashboard: cross-platform CPA trend, creative performance decay, audience saturation, conversion funnel by platform, budget utilization, and lead quality score.

2. Configure daily health checks in n8n:
   - Creative fatigue detection (CTR decline > 30% from first-week average)
   - Audience exhaustion detection (frequency > 5 on Meta/Google, > 3 on LinkedIn)
   - CPA drift detection (CPA > 125% of 4-week baseline)

3. Set escalation rules:
   - Agent auto-handles: pausing fatigued creatives, refreshing exclusion lists, small budget shifts (< 10%)
   - Human approval required: pausing audience segments, budget changes > 20%, new creative launch, any change when monthly spend > $10,000

4. Generate weekly retargeting brief (integrated with the autonomous-optimization Phase 5 report)

### 3. Implement convergence detection

The optimization loop must detect when the play has reached its local maximum:

1. Track the last 6 experiments' net impact on blended CPA
2. If 3 consecutive experiments produce < 2% CPA improvement, flag as converged
3. When converged:
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment frequency from continuous to 1/month (seasonal/market checks)
   - Generate a convergence report: "Retargeting has reached local maximum. Current performance: {CPA}, {conversions/mo}, {CTR}. Further gains require strategic changes: new audience sources, product changes affecting conversion rate, or expansion to new platforms."
4. Post convergence report to Slack and Attio
5. Re-enter active optimization if any KPI degrades > 15% from converged baseline (market shift detection)

### 4. Monthly strategic review

**Human action required:** Monthly, review the agent's performance:

1. Pull the month's optimization activity from Attio: experiments run, win/loss ratio, net CPA change, total conversions
2. Review the agent's hypothesis quality: are hypotheses getting more targeted over time, or repeating the same ideas?
3. Check for strategic opportunities the agent cannot detect:
   - New ad platforms to test (TikTok, Reddit, etc.)
   - Product changes that affect landing page conversion rates
   - Competitive shifts that change what messaging resonates
   - Seasonal patterns that require proactive budget adjustments
4. Adjust the optimization parameters if needed: hypothesis generation prompt, experiment duration thresholds, risk classification rules
5. Update the retargeting strategy document in Attio with any strategic changes

## Time Estimate

- Autonomous-optimization loop setup and testing: 20 hours
- Retargeting performance monitor dashboard and alerts: 10 hours
- Convergence detection workflow: 5 hours
- Monthly strategic reviews (12 months x 3 hours): 36 hours
- Weekly brief review and action (52 weeks x 1 hour): 52 hours
- Experiment oversight and approval of high-risk changes: 30 hours
- Workflow maintenance and debugging over 12 months: 15 hours
- Quarterly strategy updates: 12 hours
- **Total: 180 hours over 12 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Meta Ads | Retargeting on Facebook/Instagram | Ad spend: $2,500-10,000/mo (agent-optimized). https://www.facebook.com/business/ads/pricing |
| LinkedIn Ads | Retargeting on LinkedIn | Ad spend: $1,500-5,000/mo. CPC $4.50-12. https://business.linkedin.com/advertise/ads/pricing |
| Google Ads | Retargeting on Display/YouTube | Ad spend: $1,000-5,000/mo. CPC $0.66-1.23 remarketing. https://ads.google.com/intl/en/home/pricing/ |
| PostHog | Tracking, experiments, anomaly detection, dashboards | Free up to 1M events/mo, then $0.00045/event. ~$50-100/mo at this volume. https://posthog.com/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly briefs | ~$30-60/mo at daily monitoring frequency. https://www.anthropic.com/pricing |
| Webflow | Landing page hosting and A/B variants | $14-29/mo. https://webflow.com/pricing |

**Estimated total cost: $5,000-20,000/mo ad spend + $95-190/mo tools = $5,095-20,190/month**

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — play-specific monitoring: creative fatigue detection, audience exhaustion alerts, cross-platform CPA tracking, and weekly retargeting health reporting

## Guardrails

- Maximum 1 active experiment per platform at a time
- If blended CPA exceeds 200% of baseline at any point, auto-pause all experiments and alert human
- Budget changes > 20% require human approval via Slack
- Maximum 4 experiments per platform per month — if all 4 fail, pause optimization and flag for strategic review
- After a failed experiment, 7-day cooldown before testing the same variable again
- Never modify audiences or budgets during the last 3 days of a running experiment
