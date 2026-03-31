---
name: ai-user-segmentation-durable
description: >
  AI Behavior Segmentation -- Durable Intelligence. Always-on AI agents autonomously
  optimize segmentation accuracy, personalization content, and retention outcomes.
  The autonomous-optimization loop detects metric anomalies, generates improvement
  hypotheses, runs A/B experiments, and auto-implements winners. Segment drift
  monitoring triggers cluster refreshes when behavior patterns shift. Converges
  when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving retention lift >=10% over 6 months with autonomous optimization; experiment velocity >=2/month"
kpis: ["Retention lift vs control (sustained)", "Experiment velocity", "Personalization conversion rate trend", "Segment drift status", "Autonomous optimization win rate"]
slug: "ai-user-segmentation"
install: "npx gtm-skills add product/retain/ai-user-segmentation"
drills:
  - autonomous-optimization
  - behavior-segmentation-pipeline
---
# AI Behavior Segmentation -- Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

The AI agent runs the entire segmentation-personalization-optimization loop without human intervention. `autonomous-optimization` monitors all play KPIs daily, detects when retention lift plateaus or personalization engagement drops, generates hypotheses for improvement, runs A/B experiments, and auto-implements winners. `autonomous-optimization` watches the segmentation model itself for degradation and triggers cluster refreshes when behavior patterns shift. Together, these drills find and maintain the local maximum of this play.

**Pass threshold:** Sustained or improving retention lift >=10% over 6 months with experiment velocity >=2 experiments per month. The play converges when 3 consecutive experiments produce <2% improvement -- at that point, the local maximum is reached.

## Leading Indicators

- `autonomous-optimization` loop fires daily monitoring without failures for 4+ consecutive weeks
- Experiment cycle time: <14 days from anomaly detection to experiment completion
- Win rate: >30% of experiments produce a statistically significant improvement
- Segment drift status stays "Healthy" for 4+ consecutive weeks
- Weekly optimization briefs generated and stored in Attio automatically
- No human intervention needed for 4+ consecutive weeks (excluding quarterly strategic reviews)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to set up the core Durable loop for this play:

**Phase 1 -- Monitor (daily n8n cron):**
Configure anomaly detection on these play-specific KPIs:
- Retention lift vs control (primary)
- Per-segment personalization conversion rate (segment_message_clicked / segment_message_shown)
- Segment stability (week-over-week consistency)
- Unclassified user rate
- Per-segment 14-day retention rate

Use `posthog-anomaly-detection` to compare last 2 weeks against 4-week rolling averages. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase).

**Phase 2 -- Diagnose (triggered by anomaly):**
When an anomaly is detected, the agent gathers context:
- Pull current segment definitions and sizes from PostHog
- Pull personalization config: which messages, emails, and tours are live per segment
- Pull 8-week metric history for the anomalous KPI
- Run `hypothesis-generation` to produce 3 ranked hypotheses for what to change

Segmentation-specific hypotheses the agent should consider:
- "Segment X's in-app message CTA is stale -- users have seen it too many times" -> test a new CTA
- "Segment Y's email sequence has declining open rates -- subject lines need refresh" -> test new subjects
- "The product tour for Segment Z has low completion rate -- it is too long" -> test a shorter tour
- "Segment boundaries have drifted -- cluster refresh needed" -> trigger `autonomous-optimization`
- "A new user behavior pattern has emerged that does not fit existing segments" -> run cluster discovery

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
Take the top-ranked hypothesis (risk = low or medium). Use PostHog feature flags to split the target segment: 50% control (current experience), 50% variant (hypothesis change). Run for minimum 7 days or 100+ samples per variant, whichever is longer. Log experiment start in Attio.

For personalization experiments, the agent can modify:
- In-app message copy, CTA text, and timing via Intercom API
- Email subject lines and body content via Loops API
- Product tour steps and flow via Intercom product tours
- Feature flag payloads (which features to highlight per segment) via PostHog API

The agent MUST NOT modify: segment definitions directly (that is `autonomous-optimization`'s job), billing or pricing, or core product functionality.

**Phase 4 -- Evaluate (triggered by experiment completion):**
Pull experiment results from PostHog. Run `experiment-evaluation` to decide:
- **Adopt:** Variant outperformed control with statistical significance. Update the live personalization config. Log the win.
- **Iterate:** Results inconclusive. Generate a new hypothesis building on this one. Return to Phase 2.
- **Revert:** Variant underperformed. Restore control config. Log the failure. Return to Phase 1.
- **Extend:** Not enough data yet. Continue for another 7 days.

**Phase 5 -- Report (weekly n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week
- Experiments running: status, hypothesis, early results
- Experiments completed: outcome, metric impact
- Net retention lift change from all adopted changes
- Current distance from estimated local maximum
- Segment health summary (from `autonomous-optimization`)
Store in Attio and post to Slack.

### 2. Deploy the segment drift monitor

Run the `autonomous-optimization` drill to set up always-on segment quality monitoring:

- Weekly health check (Monday 07:00 UTC): compute segment stability, size balance, retention divergence, and personalization engagement spread
- Automatic drift classification: Healthy / Degrading / Drifted
- On Degrading: AI-generated drift diagnosis with corrective hypotheses
- On Drifted: automatic cluster refresh and personalization pause until new segments are assigned

The drift monitor runs independently of `autonomous-optimization`. When it detects drift, it takes corrective action on the segmentation model itself, while `autonomous-optimization` handles the personalization content and targeting.

### 3. Configure guardrails

Set these limits in the n8n autonomous optimization workflow:

- **Rate limit:** Maximum 1 active experiment per segment at a time. Maximum 4 total experiments across all segments simultaneously.
- **Revert threshold:** If any segment's retention drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Any experiment affecting >50% of total users (e.g., changing the control/treatment split)
  - Merging or splitting segments (modifying the taxonomy)
  - Changes to email send frequency (spam risk)
- **Cooldown:** After a failed experiment, wait 7 days before testing a new hypothesis on the same segment + surface combination.
- **Monthly experiment cap:** 8 experiments total. If all fail in a month, pause and flag for human strategic review.
- **Cost guardrail:** If Claude API costs exceed $20/mo, reduce optimization frequency from daily to every-other-day monitoring.

### 4. Define convergence criteria

The play has reached its local maximum when:
- 3 consecutive experiments produce <2% improvement on any KPI
- Segment drift status is "Healthy" for 8+ consecutive weeks
- Retention lift has been stable (within +/-2pp) for 8+ weeks

At convergence:
1. Reduce `autonomous-optimization` monitoring from daily to weekly
2. Keep `autonomous-optimization` running weekly (behavior patterns can still shift)
3. Generate a final optimization report: total experiments run, total wins, cumulative retention lift, current segment definitions, and recommendation for when to re-activate daily optimization (e.g., after a major product launch or significant user growth)
4. Store the report in Attio. The play is optimized.

### 5. Evaluate sustainability

Run the `threshold-engine` drill quarterly:

- **Retention lift sustained:** >=10% lift vs control maintained for 6 months. Not just a one-time spike, but a durable improvement.
- **Experiment velocity:** >=2 experiments completed per month. The agent is actively seeking improvements, not idle.
- **Autonomous operation:** <2 human interventions per month (excluding quarterly reviews). The system runs itself.

This level runs continuously. If retention lift decays below 10% and the agent cannot self-correct within 4 weeks, escalate to human review. The likely cause is a strategic change needed (new product feature, new user segment, market shift) that is beyond the agent's optimization scope.

## Time Estimate

- 20 hours: Deploy autonomous optimization loop (monitoring, diagnosis, experimentation, evaluation, reporting)
- 10 hours: Deploy segment drift monitor with corrective actions
- 10 hours: Configure guardrails, convergence criteria, and escalation paths
- 20 hours: First 2 months of agent operation (monitoring, reviewing weekly briefs, handling escalations)
- 40 hours: Months 3-6 of agent operation (decreasing as the system converges)
- 20 hours: Quarterly reviews, strategic adjustments, final convergence report

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Daily monitoring, experiments, feature flags, dashboards | Growth plan ~$0-450/mo based on volume -- [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API (Anthropic) | Weekly clustering + daily monitoring + hypothesis generation + experiment evaluation | ~$5-15/mo -- [anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Intercom | Segment-specific in-app messages and tours (agent-managed) | ~$74-300/mo -- [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Segment-specific email sequences (agent-managed) | ~$49-99/mo -- [loops.so/pricing](https://loops.so/pricing) |
| n8n | Orchestration: daily monitoring, weekly segmentation, experiment management | Self-hosted (free) or Cloud ~$20/mo -- [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** ~$150-450/mo (Intercom and PostHog dominate; Claude API and n8n are marginal)

## Drills Referenced

- `autonomous-optimization` -- The core Durable loop: monitor -> diagnose -> experiment -> evaluate -> implement. Runs daily. Finds and maintains the local maximum.
- `autonomous-optimization` -- Watches segment quality, detects drift, triggers corrective cluster refreshes. Runs weekly.
- `behavior-segmentation-pipeline` -- The underlying weekly segmentation pipeline that the drift monitor and optimization loop depend on.
