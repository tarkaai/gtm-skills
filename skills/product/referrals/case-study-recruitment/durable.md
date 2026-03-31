---
name: case-study-recruitment-durable
description: >
  Customer Story Pipeline — Durable Intelligence. Autonomous AI agents continuously
  optimize the recruitment pipeline, outreach messaging, content formats, and distribution
  targeting. The optimization loop detects metric anomalies, generates hypotheses, runs
  A/B experiments, evaluates results, and auto-implements winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving case study output and deal influence over 6 months via AI optimization"
kpis: ["Recruitment acceptance rate", "Case study completion rate", "Pipeline velocity", "Deal influence rate", "Experiment velocity", "AI lift"]
slug: "case-study-recruitment"
install: "npx gtm-skills add product/referrals/case-study-recruitment"
drills:
  - autonomous-optimization
  - case-study-recruitment-health-monitor
---

# Customer Story Pipeline — Durable Intelligence

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

The recruitment pipeline is self-optimizing. AI agents run the monitor-diagnose-experiment-evaluate-implement loop continuously. The pipeline sustains or improves its case study output and deal influence over 6 months without human strategic intervention. The agent finds the local maximum for each optimization surface: outreach messaging, scoring model weights, distribution targeting, content format mix, and interview scheduling patterns.

## Leading Indicators

- At least 2 A/B experiments running per month across the pipeline
- Optimization brief generated weekly with quantified impact of changes
- Autonomous scoring model recalibration producing measurable improvement in acceptance rate
- Deal influence rate trending upward quarter over quarter
- Convergence detection: agent identifies when a variable has reached its local maximum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the case study recruitment pipeline:

**Phase 1 — Monitor (daily via n8n cron):**
Configure anomaly detection on the pipeline's primary KPIs:
- Pipeline velocity (case studies/month)
- Outreach acceptance rate
- Deal influence rate (deals where case study assets were viewed before progression)
- Content engagement rate (aggregate clicks across all derivative assets)

Compare last 2 weeks against 4-week rolling average. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase). Log results to Attio. If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from the pipeline:
- Current scoring model weights and threshold from Attio
- Outreach sequence performance by touch (open rate, click rate, booking rate) from PostHog
- Distribution targeting rules and asset performance from PostHog
- Content format engagement rates from PostHog
- Interview scheduling patterns (day of week, time of day, no-show rate) from Cal.com data

Run hypothesis generation with the anomaly data and context. Receive 3 ranked hypotheses. Examples:
- "Acceptance rate declined because the outreach subject line has been unchanged for 8 weeks. Test a new subject referencing the candidate's specific top metric."
- "Pipeline velocity is plateaued because the candidate pool is concentrated in 2 verticals. Lowering the score threshold by 5 points for underrepresented verticals would add 8 candidates."
- "Deal influence rate dropped because the email snippet format does not include a metric in the first sentence. Restructuring to lead with the number should increase click-through."

Store hypotheses in Attio. If top hypothesis is high risk (affects >50% of pipeline or requires budget change), escalate for human review.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment:
- For outreach changes: split new candidates 50/50 between control (current) and variant (hypothesis) using PostHog feature flags. Minimum 10 candidates per variant or 14 days, whichever is longer.
- For scoring model changes: run the new model in shadow mode (score but do not act) for 2 weeks, then compare its candidate rankings against the production model's outcomes.
- For distribution changes: A/B test the new asset format or routing rule. Use PostHog experiments with deal influence as the primary metric.
- For content format changes: produce the variant format for the next 3 case studies alongside the control format. Measure engagement on both.

Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, risk level.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull experiment results. Evaluate:
- **Adopt**: variant outperforms control by >5% with statistical significance. Update production configuration. Log the change with before/after metrics.
- **Iterate**: results are mixed or inconclusive. Generate a refined hypothesis building on this result. Return to Phase 2.
- **Revert**: variant underperforms control by >10%. Disable variant, restore control. Log the failure and reason.
- **Extend**: sample size insufficient. Keep running for another period.

Store evaluation in Attio: decision, confidence level, net impact.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week and classification
- Hypotheses generated and their status
- Experiments running: current status, expected completion, early signals
- Experiments completed: decisions and net impact
- Cumulative AI lift: total improvement in each KPI attributable to optimization experiments since Durable began
- Distance from estimated local maximum (based on diminishing returns trend)
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure play-specific monitoring

Run the `case-study-recruitment-health-monitor` drill at Durable level:

1. Tighten health metric thresholds to reflect the optimized pipeline's higher baseline:
   - Outreach acceptance rate healthy: 35%+ (up from 25%)
   - Pipeline velocity healthy: 6+/month sustained
   - Time to publish healthy: <14 days (down from 21)
   - Deal influence rate: 40%+ of matching deals engaged with case study assets

2. Add Durable-specific metrics:
   - **Experiment velocity**: experiments completed per month (target: 2+)
   - **AI lift**: cumulative % improvement in each KPI since Durable started
   - **Convergence status**: how many optimization surfaces have converged (<2% improvement in last 3 experiments)

3. Configure Durable-specific interventions:
   - If AI lift is negative for 4 consecutive weeks, pause all experiments and run a full pipeline audit
   - If experiment velocity drops to 0 for 3 weeks, force a new hypothesis generation cycle
   - If convergence is detected on all surfaces, reduce monitoring to weekly and report: "Pipeline optimized. Current performance is [metrics]. Further gains require strategic changes."

### 3. Optimize the scoring model autonomously

The candidate scoring model's weights were set manually during Smoke and calibrated during Baseline. At Durable, the agent optimizes the weights continuously:

1. Every month, run a retroactive analysis: for all candidates scored in the last 90 days, which dimension scores best predicted acceptance and story quality?
2. If the correlation between a dimension and outcomes has shifted (e.g., timing signal is now more predictive than story potential), generate a hypothesis to adjust weights
3. Run the adjusted model in shadow mode for 2 weeks
4. If the adjusted model would have surfaced better candidates (higher predicted acceptance rate), adopt the new weights
5. Log every weight change in Attio with before/after weights and the evidence

### 4. Optimize outreach messaging autonomously

The agent tests and iterates on outreach messaging continuously:

1. Track per-touch performance: open rate, click rate, booking rate for each email in the sequence and the in-app nudge
2. Every 4 weeks, identify the lowest-performing touch
3. Generate 2 variant messages for that touch using the hypothesis generation fundamental
4. A/B test: split new candidates across control and variants
5. After 14 days or 15 candidates per variant, evaluate. Adopt winner. Log results.
6. Move to the next-lowest-performing touch

### 5. Evaluate durability

This level runs continuously. Monthly checkpoints:

- Is pipeline velocity sustained at 6+/month? If declining, check: candidate pool depletion (need user base growth), acceptance rate decay (outreach fatigue), or capacity constraint (writing backlog).
- Is deal influence rate sustained or improving? If declining, check: case study freshness (old stories lose relevance), distribution targeting (wrong deals being matched), or asset format (sales not using the assets).
- Are optimization experiments producing diminishing returns? If 3 consecutive experiments produce <2% improvement on a surface, that surface has converged. Document the local maximum and shift experimentation to other surfaces.

Convergence state: when all major optimization surfaces (scoring weights, outreach messaging, distribution targeting, content format) have converged, the pipeline has found its local maximum. The agent reports this and recommends whether strategic changes (new channels, new incentive structures, expansion into new customer segments) could unlock the next level of performance.

## Time Estimate

- 20 hours: autonomous optimization loop setup (monitoring, hypothesis generation, experiment infrastructure)
- 10 hours: health monitor enhancement for Durable thresholds
- 8 hours: scoring model auto-calibration pipeline
- 8 hours: outreach messaging A/B test automation
- 4 hours/month: weekly optimization brief review and strategic decisions
- 2 hours/month: experiment result review and adoption decisions
- 2 hours/month: convergence assessment

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Free tier (1M events/mo); Growth from $0 (pay per event) |
| Attio | Pipeline CRM, experiment logging, optimization audit trail | Free tier available |
| n8n | Optimization loop orchestration, scheduling, triggers | Self-hosted free; Cloud from $24/mo |
| Anthropic API | Hypothesis generation, experiment evaluation, brief writing | ~$15-50/mo based on optimization frequency |
| Loops | Outreach A/B variants, distribution emails | From $49/mo (1,000 contacts) |
| Intercom | In-app nudge variants, social proof experiments | From $85/seat/mo (Advanced for A/B) |
| Fireflies | Interview transcription | Pro $10/user/mo annual |
| Cal.com | Interview scheduling | Teams $15/user/mo |
| Ghost | Case study publishing | From $9/mo (starter) |

**Play-specific cost:** Loops ~$49/mo + Intercom ~$85/mo + Anthropic ~$30/mo + Fireflies ~$30/mo + Cal.com ~$45/mo = ~$239/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that makes this level self-improving
- `case-study-recruitment-health-monitor` — play-specific health metrics, diagnostics, and interventions tuned for Durable thresholds
