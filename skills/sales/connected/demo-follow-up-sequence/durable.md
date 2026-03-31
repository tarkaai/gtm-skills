---
name: demo-follow-up-sequence-durable
description: >
  Demo Follow-Up Sequence — Durable Intelligence. Autonomous AI agents monitor follow-up performance,
  detect metric anomalies, generate improvement hypotheses, run A/B experiments, and auto-implement
  winners. A separate intelligence agent predicts optimal follow-up strategy per deal based on
  demo transcript analysis and historical outcome patterns.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "148 hours over 6 months"
outcome: "Demo-to-proposal conversion sustained or improving over 6 months with autonomous optimization converging (successive experiments produce <2% improvement)"
kpis: ["Demo-to-proposal conversion rate", "Next step booking rate", "AI prediction accuracy (predicted vs default strategy)", "Experiment throughput (experiments/month)", "Optimization convergence rate"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - autonomous-optimization
---

# Demo Follow-Up Sequence — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

The follow-up system finds and maintains its local maximum. The `autonomous-optimization` drill runs the core loop: monitor KPIs daily, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners. A separate the demo follow up intelligence workflow (see instructions below) agent predicts the optimal follow-up strategy for each new deal based on transcript analysis and historical outcome patterns. Weekly optimization briefs surface what changed and why. The system converges when successive experiments produce <2% improvement.

**Pass threshold:** Demo-to-proposal conversion sustained or improving over 6 months with autonomous optimization converging (successive experiments produce <2% improvement).

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- At least 2 experiments per month reach statistical significance
- AI-predicted follow-up strategies outperform default strategies by >=10% on next-step booking rate
- Weekly optimization briefs generated and delivered every Monday
- No metric anomaly goes undiagnosed for >48 hours
- Convergence signal: 3 consecutive experiments produce <2% lift (local maximum reached)

## Instructions

### 1. Deploy the Autonomous Optimization Loop

Run the `autonomous-optimization` drill configured for the demo follow-up sequence. This creates the always-on monitor-diagnose-experiment-evaluate-implement cycle.

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the follow-up sequence's primary KPIs:
   - Recap delivery speed (hours from demo to recap sent)
   - Sequence completion rate
   - Response rate by touch number
   - Next-step booking rate
   - Demo-to-proposal conversion rate
2. Compare the last 2 weeks against the 4-week rolling average
3. Classify each KPI: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If all normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: current cadence configuration, recent experiment results, volume changes, any external factors (holidays, product launches)
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + context. Receive 3 ranked hypotheses with expected impact and risk level
4. Store hypotheses in Attio
5. If top hypothesis risk is "high": send Slack alert for human review, STOP
6. If risk is "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment in PostHog: create feature flag for A/B split, define primary metric, set minimum sample size and duration (minimum 7 days or 50+ samples per variant)
3. Wire the experiment into the follow-up automation via n8n: at the relevant touch point, check the flag and serve control or variant
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`: statistical significance test, confidence interval, practical significance assessment
3. Decision:
   - **Adopt:** Update the live cadence configuration. Log the change and measured lift. Move to Phase 5.
   - **Iterate:** Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert:** Disable the variant, restore control. Log the failure. Return to Phase 1.
   - **Extend:** Keep running for another period if underpowered. Set a reminder.
4. Store the full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron, Monday 8 AM):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes
3. Generate the weekly optimization brief:
   - What changed and why
   - Net impact on primary KPIs
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

**Guardrails (enforced by n8n):**
- Maximum 1 active experiment at a time. Never stack experiments.
- If primary metric drops >30% during an experiment: auto-revert immediately.
- Human approval required for: audience/targeting changes affecting >50% of deals, any "high risk" hypothesis.
- Cooldown: after a failed experiment (revert), wait 7 days before testing the same variable again.
- Maximum 4 experiments per month. If all 4 fail: pause optimization, flag for strategic review.

### 2. Deploy the Follow-Up Intelligence Agent

Run the the demo follow up intelligence workflow (see instructions below) drill to create the per-deal prediction layer:

**Deal-level prediction (runs after every demo transcript is processed):**
1. Analyze the demo transcript: features shown, questions asked, concerns, interest signals, urgency, stakeholders
2. Match against historical outcome data: for past deals with similar characteristics, which follow-up approach produced the best results?
3. Predict the optimal follow-up strategy: cadence timing, content selection per touch, personalization anchors, recommended next-step type
4. Store the prediction in Attio as a deal note tagged `follow-up-intelligence`
5. Feed the prediction to the follow-up automation: if confidence is high, override the default cadence with the predicted strategy

**Outcome feedback loop (weekly):**
1. Pull all follow-up sequences completed in the last 7 days with their outcomes
2. Match outcomes to predictions made at sequence start
3. Calculate prediction accuracy and recalibrate the model

**Cross-deal pattern detection (weekly):**
1. Analyze 90 days of demo transcripts + follow-up outcomes
2. Identify winning patterns (demo characteristics + follow-up approaches that convert) and losing patterns
3. Surface timing insights, content insights, personalization insights, and risk signals
4. Update the prediction model with new patterns

**Real-time deal alerts:**
- Hot deal: prospect visits pricing page or watches recap video twice after follow-up → notify founder with recommended action
- Stall risk: high-score deal with no response after 2+ touches → flag for manual founder outreach
- Multi-thread signal: new person from prospect company engages with content → suggest direct outreach

### 3. Build the Intelligence Dashboard

Extend the Scalable dashboard with Durable-specific panels:

1. **Optimization loop status:** current phase (monitoring/diagnosing/experimenting/evaluating), days since last experiment, experiments this month
2. **Prediction accuracy:** AI-recommended strategy conversion vs default conversion (weekly trend line)
3. **Convergence tracker:** lift from each successive experiment (are returns diminishing?)
4. **Pattern shift detection:** are winning follow-up patterns changing over time? (signals market or product shifts)
5. **Cumulative optimization impact:** total lift from all adopted experiments since Durable start
6. **Deal score distribution:** histogram of intelligence scores vs actual outcomes (is the model well-calibrated?)

### 4. Manage Convergence

The optimization loop should detect when the follow-up sequence has reached its local maximum. Convergence criteria: 3 consecutive experiments produce <2% improvement on the primary metric.

When convergence is detected:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from continuous to monthly check-ins
3. Generate a convergence report:
   - Current optimized cadence configuration (timing, content, CTAs, personalization approach)
   - Final performance metrics vs Baseline performance (total lift achieved)
   - Recommendations: further gains require strategic changes (new channels, product changes, market expansion) rather than tactical optimization
4. The intelligence agent continues running per-deal predictions — even after tactical convergence, individual deal optimization still adds value

### 5. Monthly Strategic Review

The autonomous system handles tactical optimization. Monthly, the founder reviews strategic questions the system cannot answer:

- Should the follow-up sequence include a new channel (e.g., LinkedIn DM, personalized video)?
- Has the competitive landscape changed in ways that require new content types?
- Are there new prospect segments emerging that need different follow-up strategies?
- Should the product resource library be updated based on what follow-up assets perform best?

The system generates the data and recommendations; the founder makes strategic decisions. Log decisions in Attio. If strategic changes are made, the optimization loop treats them as new baseline and begins a new experiment cycle.

## Time Estimate

- 30 hours: Deploy autonomous optimization loop (n8n workflows, PostHog experiments, guardrails)
- 25 hours: Deploy follow-up intelligence agent (prediction model, feedback loop, pattern detection, alerts)
- 15 hours: Dashboard extension and convergence tracking
- 8 hours: Monthly strategic reviews (6 months x ~1.5 hours)
- 70 hours: Ongoing monitoring, experiment management, and system maintenance (~12 hours/month x 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Demo transcription | $18/user/mo Pro — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Attio | CRM — deal intelligence, optimization logs, pattern storage | $29/user/mo Plus — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Anomaly detection, experiments, dashboards, feature flags | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Optimization loop orchestration, daily monitoring, weekly reports | Self-hosted free or $24/mo Starter — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic | Claude API for hypothesis generation, experiment evaluation, deal prediction, pattern detection | Usage-based, ~$20-50/mo at Durable volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Loops | Transactional email delivery | $49/mo (5K contacts) — [loops.so/pricing](https://loops.so/pricing) |
| Instantly | Alternative: sequenced email at scale | $97/mo Hypergrowth — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Cal.com | Booking links | Free or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Recap videos with engagement tracking | $15/user/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |

**Estimated play-specific cost this level:** ~$155-250/mo. Core: Fireflies Pro ($18) + n8n ($24) + Loops ($49) + Anthropic API (~$35) + Loom ($15). The main cost increase from Scalable is higher Claude API usage for hypothesis generation, experiment evaluation, and per-deal prediction.

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum for any play's KPIs
- the demo follow up intelligence workflow (see instructions below) — AI agent that predicts optimal follow-up strategy per deal based on demo transcript analysis and historical outcome patterns
