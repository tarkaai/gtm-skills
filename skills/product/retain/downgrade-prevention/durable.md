---
name: downgrade-prevention-durable
description: >
  Downgrade Intervention — Durable Intelligence. Autonomous agent loop that monitors downgrade
  prevention metrics, generates improvement hypotheses, runs A/B experiments on detection
  thresholds, offer parameters, and intervention routing, and auto-implements winners.
  Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving prevention ≥45% over 6 months via AI"
kpis: ["Downgrade prevention rate", "MRR saved", "Cost per save", "Experiment velocity", "AI lift"]
slug: "downgrade-prevention"
install: "npx gtm-skills add product/retain/downgrade-prevention"
drills:
  - autonomous-optimization
  - downgrade-intervention-health-monitor
  - downgrade-intercept-flow
---

# Downgrade Intervention — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

The downgrade prevention system operates autonomously. An always-on agent loop monitors prevention metrics, detects when rates plateau or decline, generates hypotheses for improvement, runs A/B experiments on detection thresholds, offer parameters, messaging, and routing logic, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs. The system converges when successive experiments produce <2% improvement -- the play has found its local maximum.

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 1 experiment per month is auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted to Slack
- No manual tuning needed -- the agent handles detection drift, offer fatigue, and channel saturation automatically
- Guardrail alerts fire correctly when thresholds are breached (tested by simulating a metric drop)
- MRR saved per month is stable or increasing

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the downgrade prevention play. The optimization loop has 5 phases:

**Phase 1 -- Monitor (daily via n8n cron):**
The agent runs `posthog-anomaly-detection` on the play's core KPIs: overall prevention rate, prevention rate by tier, intercept page keep rate, offer acceptance rate, MRR saved, and cost per save. It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal, plateau, drop, or spike. If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
The agent gathers context: current detection thresholds, intervention routing rules, active offer parameters, 8-week metric history by segment. It runs `hypothesis-generation` to produce 3 ranked hypotheses for what to change. Examples of hypotheses the agent might generate for this play:

- "Increase the billing_page_visits signal weight from 15 to 25 -- 3 of the last 5 missed downgrades had 4+ billing page visits but were scored below the moderate threshold because this signal was underweighted"
- "Switch the moderate-tier intervention from in-app banner to email -- banner engagement dropped 35% over 4 weeks, suggesting banner fatigue. Email engagement for similar plays is still 28%+"
- "Replace the 20% discount offer with a 1-month free extension for Pro users -- discount acceptance plateaued at 15% while competitor [X] launched a similar pricing tier, making discounts feel like admissions of overpricing"
- "Add a 'talk to product' CTA for users whose top signal is support_frustration -- these users are not price-sensitive, they are experience-frustrated, and a discount does not address their root cause"

If the top hypothesis is high-risk (affects >50% of traffic or changes offer economics significantly), the agent sends a Slack alert and waits for human approval before proceeding.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
The agent implements the experiment using PostHog feature flags. It splits traffic between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 7 days or 50 samples per variant, whichever is longer.

For detection experiments: the agent adjusts signal weights or thresholds for the variant group and measures whether the adjusted model catches more true positives without increasing false positives.

For intervention experiments: the agent creates a variant message, offer, or channel routing and measures prevention rate for the variant vs. control.

For offer experiments: the agent tests a new offer type or parameter and measures acceptance rate, prevention rate, and 60-day retention.

**Phase 4 -- Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` to decide: adopt (implement the winner permanently), iterate (build on the result with a follow-up experiment), revert (the variant hurt performance), or extend (insufficient data, keep running).

Adopted changes are logged in Attio with full context: what changed, why, the experiment results, the confidence level, and the estimated MRR impact. This creates an audit trail of every system evolution.

**Phase 5 -- Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net metric change from all adopted changes
- Current MRR saved vs. target, with trend
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure downgrade-prevention-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add play-specific safeguards:

- **Offer budget cap:** Total discount value given per month must not exceed a configurable percentage of MRR saved. If discount costs exceed 40% of MRR retained, pause discount offers and switch to non-monetary interventions. Alert the team for pricing strategy review.
- **Offer fatigue detection:** If a specific offer type's acceptance rate drops below 5% for 3 consecutive weeks, retire that offer and flag for replacement. The user base has learned to ignore it.
- **Detection drift alert:** If the detection model's false positive rate exceeds 40% in the monthly calibration, pause all automated interventions for moderate-tier users (too many healthy users are being bothered). Recalibrate the model before resuming.
- **Intervention overload:** No single user should receive more than 5 intervention touches per 30-day period across all channels combined. If a user hits this cap and is still scored moderate+, escalate to human review (something else is wrong).
- **Revenue cannibalization check:** Monthly, compare MRR saved (value of prevented downgrades) against MRR discounted (value of retention offers given). If MRR discounted exceeds 30% of MRR saved, the offers are too generous and the system is retaining users at a net loss. Tighten offer parameters.
- **Competitor price change alert:** If downgrade rate spikes >50% within a 2-week window across all segments simultaneously, flag as potential external factor (competitor launched a cheaper alternative, market shift). Pause experiments and alert the team for strategic response.

### 3. Deploy the intervention health monitor at Durable cadence

Run the `downgrade-intervention-health-monitor` drill with enhanced frequency:
- Daily anomaly check: runs at 09:00 UTC (same as Baseline/Scalable)
- Weekly health brief: integrates with the `autonomous-optimization` weekly report
- Offer economics tracking: expanded to include ROI per offer variant (tracking experiment variants separately)
- MRR impact attribution: attributes MRR saved to specific interventions and experiments

The health monitor feeds data to the autonomous optimization loop. When it detects an anomaly (prevention rate drop, offer fatigue, channel saturation), that becomes the signal that triggers the optimization cycle's Phase 2.

### 4. Maintain and evolve interventions

The `downgrade-intercept-flow` drill continues to execute the current best intervention configuration at Durable level. The autonomous optimization loop may modify:

- Detection signal weights and tier thresholds
- In-app message copy, timing, and frequency caps
- Email sequence content, send timing, and subject lines
- Offer types, values, and eligibility rules
- Channel routing logic per segment
- Intercept page layout, copy framing, and CTA labels

Each modification is implemented as a PostHog feature flag variant so it can be tested and reverted cleanly.

### 5. Detect convergence

The autonomous optimization loop monitors experiment outcomes for convergence. When 3 consecutive experiments on the same variable produce <2% improvement:

1. That variable has reached its local maximum
2. Mark it as "converged" in Attio and reduce experiment frequency for that variable
3. Shift experiment focus to unconverged variables

Full convergence (all major variables converged) triggers a shift to maintenance mode:
- Daily detection and intervention continue as always-on
- Optimization loop slows from continuous to monthly checks
- The agent generates a convergence report:
  - Current performance levels for all KPIs
  - Total MRR saved since Durable started
  - Total improvement attributable to autonomous optimization vs. Scalable-level static system
  - Recommended strategic changes for further gains (new offer types, product changes, pricing restructure, new channels)

The agent still monitors for anomalies in maintenance mode. External changes (competitor launch, pricing restructure, major product release, seasonal shifts) can break convergence and re-activate the optimization loop.

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Prevention rate: sustained at or above 45%, or improving, across the full user base
- MRR saved: stable or increasing month over month
- Cost per save: stable or decreasing (efficiency improving)
- Experiment velocity: at least 2 experiments per month during active optimization
- AI lift: measurable improvement in prevention rate attributable to autonomous optimization vs. the Scalable-level static system

This level runs continuously. Review monthly: what improved, what converged, what external factors changed, and whether strategic changes are needed.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations)
- 10 hours: configure downgrade-specific guardrails and test them (simulate offer budget breach, detection drift, intervention overload)
- 10 hours: enhance health monitor for Durable cadence with MRR attribution
- 80 hours: ongoing monitoring, hypothesis review, guardrail management over 6 months (~3 hours/week)
- 20 hours: monthly strategic reviews, convergence analysis, offer economics audits
- 10 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards, cohorts | Free up to 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation, experiment evaluation, weekly briefs | ~$50-150/mo at Durable scale -- [anthropic.com/pricing](https://anthropic.com/pricing) |
| n8n | Optimization loop workflows, detection, intervention routing | Self-hosted free; Cloud from EUR20/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Loops | Intervention email sequences (modified by optimization loop) | $49/mo -- [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app interventions (modified by optimization loop) | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated play-specific cost: $150-400/mo** (Anthropic API for optimization + Loops + Intercom + retention offer discounts)

## Drills Referenced

- `autonomous-optimization` -- the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum
- `downgrade-intervention-health-monitor` -- monitors prevention rates, offer economics, and channel performance at Durable cadence, feeding signals to the optimization loop
- `downgrade-intercept-flow` -- executes the current best intervention configuration, updated by the optimization loop as experiments produce winners
