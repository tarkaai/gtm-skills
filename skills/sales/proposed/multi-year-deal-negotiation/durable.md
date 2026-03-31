---
name: multi-year-deal-negotiation-durable
description: >
  Multi-Year Deal Negotiation — Durable Intelligence. Always-on AI agents
  finding the local maximum: autonomous optimization detects metric anomalies
  in close rate, TCV, discount efficiency, and negotiation quality; generates
  improvement hypotheses; runs A/B experiments on deal structures, timing,
  and presentation; evaluates results; and auto-implements winners. Play-specific
  monitoring tracks negotiation patterns, discount creep, and pipeline health.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving multi-year close rate (>=30%) and TCV ratio (>=2x) over 6 months via continuous agent-driven deal structure optimization, negotiation intelligence, and pipeline health monitoring"
kpis: ["Multi-year close rate trend", "Average TCV trend", "Agent experiment win rate", "Discount efficiency trend", "Convergence progress"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
drills:
  - autonomous-optimization
---

# Multi-Year Deal Negotiation — Durable Intelligence

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The agent continuously optimizes every variable in the multi-year deal negotiation system: which discount levels maximize TCV without killing close rate, what term structures buyers prefer, which presentation format drives fastest closes, what timing relative to fiscal year end converts best, and how many concession rounds are optimal. The agent detects when any metric drifts, generates hypotheses grounded in negotiation data, runs experiments, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement on TCV-per-proposal — the play has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop running: daily monitoring, weekly hypothesis generation, experiments always active
- At least 1 experiment running at all times (no idle weeks after the first month)
- Weekly optimization brief generated and delivered every Monday
- Anomaly detection triggering within 24 hours of any metric shift >15%
- Convergence tracking: measuring diminishing returns across successive experiments
- 8-panel negotiation dashboard showing real-time health
- Behavioral cohorts refreshed monthly (quick closers, grinders, discount seekers, anchor holders)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the multi-year deal negotiation play. This creates the core loop:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection on the play's primary KPIs: multi-year close rate, average TCV, average discount, negotiation rounds, anchor-to-close ratio
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected -> trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull play context from Attio: current deal structure templates, scoring model performance, active experiments, pipeline composition
- Pull 8-week metric history from PostHog
- Pull behavioral cohort analysis from the `autonomous-optimization` (quick closers vs grinders patterns, segment performance, loss reasons)
- Run `hypothesis-generation` with negotiation-specific context. Example hypotheses:
  - "Close rate dropped 15% because 60% of proposals this month went to growth-segment accounts (ACV $10-15K) which historically close at 18% vs 35% for mid-market. Experiment: increase readiness score threshold for growth segment from 80 to 95."
  - "Average discount increased from 12% to 17% — anchor-to-close ratio fell from 0.88 to 0.78. Sellers are conceding faster. Experiment: add a 48-hour cooling period between concession rounds in the automation workflow."
  - "TCV is stable but negotiation rounds increased from 2.1 to 3.4 — proposals may be misaligned with buyer expectations. Experiment: test presenting 2 options instead of 3 to reduce decision friction."
  - "Revert-to-annual rate spiked to 45% — a new competitor launched monthly-only pricing. Experiment: add a 'competitive rate guarantee' incentive to 2-year terms."
- If top hypothesis is high risk (budget change >20% or targeting change >50%) -> send Slack alert for human review. Otherwise -> proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Create a PostHog experiment with feature flag splitting incoming proposals between control and variant
- Implement the variant in the proposal automation workflow (via n8n parameter changes, deal-term-modeling prompt adjustments, or scoring model weight changes)
- Set duration: minimum 7 days or 15+ proposals per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` with control vs variant data
- Primary metric: TCV-per-proposal (combines close rate and deal size into one metric)
- Secondary metrics: close rate, average discount, negotiation rounds, time to close
- Decision:
  - **Adopt:** TCV-per-proposal improved >=10% with p < 0.05. Update the live configuration. Log the change.
  - **Iterate:** Directionally positive but not significant. Refine the hypothesis and re-test.
  - **Revert:** TCV-per-proposal worse or close rate dropped >20%. Restore control. Log the failure.
  - **Extend:** Insufficient volume. Keep running for another evaluation period.
- Store decision with full reasoning in Attio

**Phase 5 — Report (weekly, Mondays via n8n cron):**
- Generate the weekly optimization brief covering: anomalies detected, hypotheses generated, experiments run, decisions made, net KPI impact, current distance from estimated local maximum
- Post to Slack, store in Attio

**Guardrails (enforced automatically):**
- Maximum 1 active experiment at a time on this play
- If TCV-per-proposal drops >30% during any experiment -> auto-revert immediately
- Human approval required for: discount policy changes >5pp, readiness scoring model weight changes, any "high risk" hypothesis
- After a failed experiment (revert), 7-day cooldown before testing the same variable
- Maximum 4 experiments per month. If all 4 fail -> pause optimization, flag for strategic review.

### 2. Deploy the negotiation intelligence monitor

Run the `autonomous-optimization` drill to create the play-specific monitoring layer:

**PostHog dashboard (8 panels):**
1. Multi-year close rate (weekly trend line with 4-week rolling average)
2. Average TCV trend (weekly)
3. Discount distribution (histogram — detect creep)
4. Negotiation efficiency (scatter: rounds vs anchor-to-close ratio)
5. Loss reason breakdown (stacked bar, monthly)
6. Pipeline conversion funnel (generated -> sent -> counter -> won)
7. Readiness score vs outcome (validates scoring model accuracy)
8. Revenue impact (committed TCV vs total pipeline)

**Daily anomaly detection (6 rules):**
- Close rate drop >20% -> High severity
- Discount increase >3pp -> High severity
- Negotiation rounds increase >50% -> Medium severity
- Revert-to-annual rate >40% -> High severity
- Time to close increase >5 days -> Medium severity
- Readiness score false positive rate >30% -> High severity

**Weekly intelligence report (Monday 9 AM):**
- Headline metric (best and worst)
- Negotiation quality metrics (anchor-to-close ratio, concessions per deal)
- Loss analysis (reasons, trends)
- Active experiments and status
- Anomalies with recommended actions
- One actionable recommendation

**Behavioral cohort analysis (monthly refresh):**
- Quick closers: what do they have in common?
- Grinders: what makes these deals drag?
- Discount seekers: can they be redirected to value-first negotiation?
- Anchor holders: what presentation method keeps them near the anchor?

This analysis feeds `hypothesis-generation` with domain-specific evidence. When the optimization loop asks "what should we experiment on?", the monitor provides the data.

### 3. Convergence detection and steady state

The optimization loop runs indefinitely, but detects when the play has reached its local maximum:

- Track the magnitude of TCV-per-proposal improvement from each successive experiment
- If 3 consecutive experiments produce <2% improvement:
  1. Declare convergence
  2. Reduce monitoring frequency from daily to weekly
  3. Generate a convergence report: "Multi-year deal negotiation is optimized. Current close rate: {X}%. Average TCV: ${Y}. TCV-per-proposal: ${Z}. Average discount: {W}%. Further gains require strategic changes (new pricing model, new product tier, new market segment) rather than tactical optimization."
  4. Switch to maintenance mode: weekly monitoring, monthly hypothesis generation

If the market changes (new competitor pricing, economic shift, product pricing change), the agent detects the resulting metric anomaly and re-enters the full optimization loop automatically.

### 4. Maintain and evolve the scoring model

Monthly, validate the readiness scoring model:
- Compare predicted readiness tier vs actual outcome for all proposals in the last 30 days
- If accuracy drops below 70%: retrain the weights using the latest closed-deal data
- Add new signals as patterns emerge from cohort analysis (e.g., if "procurement team active on LinkedIn" correlates with faster closes, add it as a signal)
- Remove signals that have lost predictive power

Update the Clay scoring formula and n8n workflow with revised weights. Log all model changes in Attio for audit trail.

## Time Estimate

- 20 hours: deploying autonomous optimization loop (n8n workflows, PostHog experiments, Attio integration)
- 15 hours: building the negotiation intelligence monitor (8-panel dashboard, anomaly detection, weekly reports)
- 10 hours: initial behavioral cohort analysis and pattern identification
- 60 hours: monitoring, reviewing experiment results, approving hypotheses, and iterating (spread over 6 months)
- 10 hours: scoring model maintenance and recalibration (monthly)
- 5 hours: convergence analysis and steady-state transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, experiment logging, optimization audit trail | Standard stack (excluded) |
| PostHog | Dashboards, anomaly detection, experiments, feature flags, cohorts | Standard stack (excluded) |
| n8n | Optimization loop orchestration, cron schedules, webhooks | Standard stack (excluded) |
| Clay | Readiness scoring, intent signals, account enrichment (continued from Scalable) | Launch: $185/mo — [pricing](https://www.clay.com/pricing) |
| Instantly | Email delivery for proposals and follow-ups (continued) | Hypergrowth: $97/mo — [pricing](https://instantly.ai/pricing) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, deal term generation, weekly reports, cohort analysis | ~$60-150/mo (daily monitoring + weekly reports + experiment cycles + proposals) — [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Play-specific cost:** ~$340-430/mo (Clay + Instantly + Claude API)
Agent compute is variable based on experiment velocity and monitoring frequency.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics -> detect anomalies -> generate hypotheses -> run experiments -> evaluate -> implement winners -> report weekly. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — play-specific monitoring: 8-panel dashboard, daily anomaly detection, weekly intelligence report, behavioral cohort analysis that feeds domain-specific hypotheses into the optimization loop
