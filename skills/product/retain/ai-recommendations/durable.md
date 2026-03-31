---
name: ai-recommendations-durable
description: >
  AI-Powered Recommendations — Durable Intelligence. Autonomous AI agent monitors
  recommendation health, detects degradation, generates improvement hypotheses,
  runs A/B experiments, and auto-implements winners. Sustains >=35% adoption over
  6 months. Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + autonomous operation over 6 months"
outcome: "Sustained or improving adoption rate >=35% over 6 months via autonomous AI optimization"
kpis: ["Recommendation adoption rate", "Experiment velocity", "AI-driven lift", "Model quality score", "Feature catalog health", "Convergence progress"]
slug: "ai-recommendations"
install: "npx gtm-skills add product/retain/ai-recommendations"
drills:
  - autonomous-optimization
  - recommendation-health-monitor
---

# AI-Powered Recommendations — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The recommendation engine runs autonomously. An AI agent monitors recommendation health daily, detects when adoption rates plateau or degrade, generates hypotheses for what to change, designs and runs A/B experiments, evaluates results, and auto-implements winners. The system sustains or improves >=35% adoption rate over 6 months without manual intervention. It converges when successive experiments produce <2% improvement for 3 consecutive experiments — at that point, the play has reached its local maximum.

## Leading Indicators

- Daily health monitoring runs without failures for 4+ consecutive weeks
- At least 1 experiment running at all times (the agent is always testing something)
- Experiment cycle time < 3 weeks (hypothesis to decision)
- Winning experiments produce measurable lift (>=2% adoption rate improvement)
- Feature catalog stays current (new features added within 7 days of ship)
- Segment drift detected and addressed within 1 optimization cycle
- Weekly briefs generate actionable insights (not just metric summaries)
- No metric drops >20% for more than 1 week without automatic intervention

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on improvement engine:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the recommendation system's primary KPIs: adoption rate, CTR, dismissal rate, feature discovery rate.
2. Compare last 2 weeks against the 4-week rolling average.
3. Classify: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase).
4. If normal: log to Attio, no action. If anomaly detected: trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Pull 8-week recommendation performance history from PostHog.
2. Gather current system configuration: active segments, recommendation strategies per segment, feature catalog, delivery timing, and message templates.
3. Run `hypothesis-generation` with the anomaly data and system context.
4. Receive 3 ranked hypotheses. Examples of recommendation-specific hypotheses:
   - "Adoption rate dropped because the feature catalog is stale — 3 new features shipped in the last month are not in the catalog."
   - "Single-Feature Users segment adoption plateaued because the complementary-feature strategy has exhausted obvious pairs. Switch to efficiency-tip strategy."
   - "Dismissal rate spiked because recommendation frequency is too high for Power Users who already know most features. Reduce to bi-weekly."
5. If the top hypothesis is high-risk (affects >50% of users or changes core recommendation logic): alert via Slack for human review. Otherwise proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Use `posthog-experiments` to create a feature flag splitting traffic between control (current) and variant (hypothesis implementation).
2. Implement the variant. For recommendation experiments this could mean: updating the feature catalog, changing the prompt strategy for a segment, adjusting delivery timing, or modifying message framing.
3. Set duration: minimum 7 days or 100+ users per variant, whichever is longer.
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog.
2. Run `experiment-evaluation` comparing control vs variant on adoption rate, CTR, and dismissal rate.
3. Decision:
   - **Adopt**: variant wins by >=2% on primary metric with 95% confidence. Update live configuration. Log the change.
   - **Iterate**: result is directionally positive but not significant. Generate a refined hypothesis and return to Phase 2.
   - **Revert**: variant performed worse. Restore control. Log the failure. Return to Phase 1 monitoring.
   - **Extend**: insufficient data. Continue the experiment for another period.

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made.
2. Calculate net metric change from all adopted changes this week.
3. Generate a weekly optimization brief: what changed, net impact, estimated distance from local maximum, recommended focus for next week.
4. Post to Slack and store in Attio.

### 2. Deploy recommendation-specific health monitoring

Run the `recommendation-health-monitor` drill to add the monitoring layer specific to this play:

1. Build the recommendation health dashboard in PostHog: adoption rate trend, per-segment adoption, suggestion quality by feature, dismissal velocity, feature catalog coverage, recommendation diversity, time to adoption, and segment drift.
2. Configure daily model quality monitoring: compute all recommendation health metrics, compare against thresholds, classify system state (healthy/degrading/unhealthy).
3. Set up weekly feature catalog staleness detection: identify stale features (not recommended in 30+ days), saturated features (>80% of target segment already uses them), and missing features (shipped but not in catalog).
4. Configure segment drift detection: compare weekly cluster distributions against the 4-week rolling average. Flag if any cluster shifts by >20%.

**Human action required:** When new product features ship, add them to the feature catalog with metadata (description, trigger event, prerequisite, benefit, plan required). This is the one manual input the system requires. Everything else is autonomous.

### 3. Configure guardrails

Apply the guardrails from the `autonomous-optimization` drill to this play:

- **Rate limit**: Maximum 1 active recommendation experiment at a time. Never stack.
- **Revert threshold**: If adoption rate drops >30% during any experiment, auto-revert immediately.
- **Human approval required for**: changes to recommendation frequency that affect >50% of users, removal of >3 features from the catalog at once, fundamental changes to the clustering model.
- **Cooldown**: After a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Feature catalog minimum**: Never let the active catalog drop below 8 features. If too many are stale or saturated, prioritize adding new features before removing old ones.

### 4. Monitor convergence

The system runs indefinitely. Track convergence:

- When 3 consecutive experiments produce <2% improvement, the play has reached its local maximum.
- At convergence: reduce monitoring frequency from daily to weekly. Reduce experiment cadence from continuous to monthly check-ins.
- Report to the team: "Recommendation system optimized. Current adoption rate: [X]%. Feature discovery rate: [Y]%. Further gains require strategic changes (new feature categories, new product capabilities, new user segments) rather than tactical optimization."
- Continue monitoring for degradation. If external factors (product changes, user base shifts, competitive landscape) cause metrics to drop, the system automatically re-enters active optimization.

## Time Estimate

- 8 hours: autonomous optimization loop setup (n8n workflows, PostHog experiments config, Attio integration)
- 6 hours: recommendation health dashboard and monitoring workflows
- 4 hours: guardrail configuration and convergence detection
- 2 hours: initial calibration and first optimization cycle review
- Ongoing: autonomous operation with weekly brief review (~30 min/week human oversight)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, experiments, anomaly detection, dashboards | Paid: usage-based, typically $0-450/mo depending on event volume — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude API | Recommendation generation, hypothesis generation, experiment evaluation, behavioral clustering | Sonnet 4.6: $3/$15 per 1M tokens; ~$40-150/mo at scale with daily monitoring + weekly generation (use prompt caching + batch API for up to 95% savings) — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Intercom | In-app recommendation delivery, segment-specific messages | Advanced: $85/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email fallback delivery | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost:** ~$90-200/mo (Claude API for autonomous monitoring + generation + experimentation, plus Loops)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop that detects metric anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners across the recommendation system
- `recommendation-health-monitor` — tracks recommendation-specific health signals (model quality, feature catalog staleness, segment drift, suggestion fatigue) and feeds anomalies into the autonomous optimization loop
