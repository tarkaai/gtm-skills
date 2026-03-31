---
name: authority-verification-durable
description: >
  Authority Verification — Durable. Always-on AI agents find the local maximum of authority verification
  performance. The autonomous-optimization drill runs the core loop: detect metric anomalies, generate
  hypotheses, run experiments, evaluate results, and auto-implement winners. Stakeholder intelligence
  monitoring catches org changes before they derail deals.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable"
time: "8 hours setup + ongoing autonomous operation over 6 months"
outcome: "Authority verification rate sustained >=90% with deal velocity and close rate stable or improving over 6 months. Successive optimization experiments produce <2% improvement (convergence reached)."
kpis: ["Authority verification rate", "Deal velocity trend", "Close rate (verified authority)", "Multi-threading rate", "Authority classification accuracy", "Optimization experiment win rate", "Time to convergence"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
drills:
  - autonomous-optimization
  - stakeholder-intelligence-monitor
  - authority-verification-reporting
---

# Authority Verification — Durable

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The authority verification system runs autonomously at its local maximum. The `autonomous-optimization` drill monitors KPIs daily, detects when metrics plateau or drop, generates hypotheses for improvement, runs A/B experiments, and auto-implements winners. The `stakeholder-intelligence-monitor` catches org changes (Champion departures, new Economic Buyers, reorgs) before they derail deals. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement for 3 consecutive experiments — meaning the play has reached its best possible performance given current market conditions.

## Leading Indicators

- Autonomous optimization loop is generating and testing hypotheses without human intervention
- Org change detection is catching Champion departures and new EB arrivals within 7 days
- Weekly optimization briefs are showing diminishing experiment impact (convergence approaching)
- Authority classification accuracy is >=90% (the verified EB is the actual contract signer 9 out of 10 times)
- Guardrails have not been breached (no experiment caused >30% metric drop)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on improvement cycle:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check authority verification KPIs against 4-week rolling averages
2. Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
3. If normal: log to Attio, no action
4. If anomaly detected: trigger diagnosis

**Phase 2 — Diagnose (triggered by anomaly):**
1. Pull 8-week metric history from PostHog: verification rate, time to verification, EB engagement rate, multi-threading rate, deal velocity
2. Pull current configuration from Attio: which enrichment sources are active, what classification rules are in use, what A/B tests are running
3. Run `hypothesis-generation` with anomaly data + context. Receive 3 ranked hypotheses:
   - Example: "Verification rate dropped because Clay enrichment is returning stale data for companies with <20 employees — switch to Apollo for small companies"
   - Example: "EB engagement rate plateaued because all outreach uses the same ROI-focused template — test a peer-reference variant"
   - Example: "Multi-threading rate declined because the engagement scoring threshold is too aggressive — contacts going Dark after 14 days may need 21 days"
4. If top hypothesis is high risk (affects >50% of pipeline), send Slack alert for human approval and STOP
5. If low/medium risk, proceed to experiment

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using `posthog-experiments`: create a feature flag splitting traffic between control (current) and variant (hypothesis change)
2. Implement the variant change: update the enrichment source, modify the classification rule, swap the outreach template, or adjust the scoring threshold
3. Set experiment duration: minimum 7 days or 30 deals per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`: compare control vs. variant on the target metric
3. Decision:
   - **Adopt**: variant won with statistical significance. Update live configuration. Log the change.
   - **Iterate**: results inconclusive. Generate a refined hypothesis. Return to Phase 2.
   - **Revert**: variant lost or caused harm. Restore control. Log the failure. Return to Phase 1.
   - **Extend**: insufficient data. Keep running for another cycle.

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on primary KPIs
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post brief to Slack and store in Attio

### 2. Deploy stakeholder intelligence monitoring

Run the `stakeholder-intelligence-monitor` drill for always-on awareness of org changes:

1. **Weekly org change scan**: compare Clay enrichment results against stored stakeholder maps. Detect new arrivals, departures, and title changes at every active account.
2. **Impact classification**: for each change, assess deal impact using Claude:
   - Champion departed: CRITICAL. Alert immediately. Identify replacement.
   - New Economic Buyer arrived: HIGH. Engage within 48 hours.
   - Influencer promoted: POSITIVE. Re-engage with congratulations.
   - Procurement contact added: WATCH. Prepare for formal evaluation process.
3. **Sentiment trajectory tracking**: after each interaction (call, email), track whether stakeholder sentiment is improving, stable, or declining. Flag when an EB's sentiment shifts to Declining.
4. **Engagement decay detection**: alert when a key stakeholder's engagement score drops from Active to Cold within 7 days, or when deal_health_score drops >20 points in a week.
5. **Weekly intelligence brief**: compile org changes, sentiment shifts, engagement decay, and multi-threading health into a single report posted to Slack.

Feed intelligence monitor outputs into the autonomous optimization loop as signal inputs: org change frequency informs enrichment refresh cadence, sentiment trajectories inform outreach template experiments.

### 3. Deploy authority verification reporting

Run the `authority-verification-reporting` drill for play-specific monitoring:

1. Build a PostHog dashboard with: verification funnel, verification rate trend (12 weeks), time-to-verification distribution, authority accuracy tracking, and stale deals table
2. Set up the weekly n8n report workflow: pipeline coverage summary, velocity metrics, accuracy tracking, and specific recommendations for stuck deals
3. Configure real-time alerts: stale authority (deal >14 days without verification), high-value unverified (deal >$50K), misclassification (contract signer is not the tagged EB)
4. After 12+ weeks, build the authority-to-close correlation model: segment closed deals by verification timing and calculate win rate per segment. This model becomes the baseline for autonomous optimization experiments.

### 4. Configure guardrails

Set hard limits the optimization loop must respect:

- **Rate limit**: maximum 1 active experiment at a time. Never stack experiments on authority verification.
- **Revert threshold**: if verification rate drops >15% or deal velocity drops >20% during an experiment, auto-revert immediately.
- **Human approval required for**: changes to the stakeholder classification model, changes to enrichment sources, any experiment flagged high-risk.
- **Cooldown**: after a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.

### 5. Monitor for convergence

The optimization loop runs indefinitely. It should detect convergence: when 3 consecutive experiments produce <2% improvement on the target metric. At convergence:

1. The play has reached its local maximum
2. Reduce monitoring from daily to weekly
3. Generate a convergence report: "Authority verification is optimized. Current performance: {verification_rate}% verification rate, {avg_velocity} day velocity, {close_rate}% close rate. Further gains require strategic changes (new enrichment sources, different qualification criteria, product changes) rather than tactical optimization."
4. The intelligence monitor continues running to catch org changes and maintain the verification rate.

## Time Estimate

- Autonomous optimization loop setup: 3 hours
- Stakeholder intelligence monitor setup: 2 hours
- Authority verification reporting setup: 2 hours
- Guardrail configuration: 30 minutes
- Weekly review of optimization briefs (15 min/week for 6 months): 6 hours
- Human approval decisions when flagged (~2 per month at 15 min each): 3 hours

After setup, the system runs autonomously. Human involvement is limited to weekly brief review and occasional approval decisions.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with experiment logging, stakeholder data | Pro $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Continuous org enrichment and change detection | Growth plan $375/mo — [clay.com/pricing](https://clay.com/pricing) |
| n8n | Optimization loop, intelligence monitor, reporting | Pro $50/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Experiments, anomaly detection, dashboards | Growth plan — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude | Hypothesis generation, evaluation, classification | Pay-per-use ~$3/MTok input, ~$15/MTok output — [anthropic.com/pricing](https://anthropic.com/pricing) |
| Fireflies | Ongoing call transcription | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |

**Estimated play-specific cost:** $300-600/mo (Clay Growth + n8n Pro + Claude API usage are the main cost drivers; PostHog Growth may be needed for experiment volume)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum of authority verification performance
- `stakeholder-intelligence-monitor` — always-on monitoring of org changes, sentiment shifts, and engagement decay across all active deals
- `authority-verification-reporting` — weekly reporting on verification coverage, accuracy, and deal impact with real-time alerts for stale and high-value unverified deals
