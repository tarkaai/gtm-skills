---
name: roi-calculator-durable
description: >
  ROI Calculator & Business Case — Durable Intelligence. Autonomous agent
  continuously calibrates ROI models against realized customer outcomes, runs
  experiments on value framing, adapts to market conditions, and converges on
  the local maximum for ROI-driven deal conversion.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving ROI effectiveness (>=70% strong ROI, >=60% completion) over 6 months via continuous agent-driven calculator optimization, personalization, and accuracy improvement"
kpis: ["ROI projection accuracy", "Agent experiment win rate", "Business case conversion rate", "Realized vs projected ROI"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
drills:
  - autonomous-optimization
  - roi-prediction-accuracy
  - dashboard-builder
---

# ROI Calculator & Business Case — Durable Intelligence

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Outcomes

The ROI calculator system runs autonomously. An always-on agent monitors ROI model accuracy, detects when conversion rates plateau or drop, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The agent continuously calibrates projections against realized customer outcomes so ROI models become more accurate over time. The system converges on its local maximum — the best possible ROI-driven conversion rate given the current market, product, and competitive landscape. Target: sustained or improving effectiveness (>=70% strong ROI, >=60% completion, improving projection accuracy) over 6 months.

## Leading Indicators

- ROI projection accuracy trending upward (target: >=80% accuracy by month 6)
- Autonomous optimization loop running without intervention for 4+ consecutive weeks
- Experiment velocity: 2-4 experiments per month on ROI framing, delivery, and personalization
- Calibration adjustments applied at least quarterly based on realized ROI data
- Weekly optimization briefs generated and posted without human prompting
- Convergence detection: successive experiments producing diminishing returns signals the local maximum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on agent that manages the ROI calculator system. Configure it for this play's specific metrics:

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check the play's primary KPIs: ROI distribution (% of deals at >=5x), calculator completion rate, business case conversion rate, ROI reference rate
- Compare last 2 weeks against the 4-week rolling average
- Classify each KPI: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current ROI model configuration, winning A/B variants, recent calibration adjustments, deal volume and stage distribution
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data
- Receive 3 ranked hypotheses. Examples:
  - "Calculator completion rate dropped because the new value driver field added in last experiment creates friction — test removing it"
  - "ROI reference rate plateaued because business cases are too long — test a 1-page executive summary vs the current 3-page format"
  - "Projection accuracy declined because Q1 benchmark data is stale — re-calibrate with latest closed-won outcomes"
- If top hypothesis is high-risk (e.g., changes the ROI model formula): send Slack alert for human approval
- If low/medium risk: proceed automatically

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags
- Implement the variant (e.g., new ROI model prompt, new business case template, new delivery timing)
- Minimum duration: 7 days or 15+ deals per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Run `experiment-evaluation`
- Decision: Adopt (update live config), Iterate (new hypothesis building on results), Revert (restore control), or Extend (keep running)
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from adopted changes
- Generate weekly optimization brief: what changed, net impact on KPIs, current distance from estimated local maximum, recommended focus for next week
- Post to Slack and store in Attio

### 2. Scale prediction accuracy measurement

Expand the `roi-prediction-accuracy` drill to full maturity:

**Monthly accuracy cycle:**
1. Score all closed-won deals that are 90+ days post-close
2. Compute accuracy per value driver: time_savings, cost_reduction, revenue_increase, risk_mitigation
3. Identify systematic biases (are revenue_increase projections consistently 40% too high?)
4. Generate calibration recommendations
5. Apply calibrations to the `roi-model-generation` prompt

**Accuracy-driven model evolution:**
- When a value driver consistently over-projects (accuracy <70% for 2 consecutive quarters), apply a discount factor to that driver in all future models
- When a value driver consistently under-projects (actual >130% of projected), note it but keep projections conservative (better to over-deliver)
- When a new value driver emerges from customer data that was never projected, add it to the discovery question set and ROI model

**Cross-deal intelligence:**
- Build a lookup table: for a given industry + company size + primary pain category, what is the typical realized ROI? Use this to sanity-check new models.
- Surface this data to sellers: "Deals like this one typically realize {X}x ROI. Your projection of {Y}x is {above/below/in line with} the norm."

### 3. Build the ROI intelligence dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard purpose-built for the ROI calculator play:

**Dashboard panels:**
- ROI distribution: histogram of ROI values across all active deals (weekly)
- Calculator completion rate: trend line with threshold marker at 60% (daily)
- Business case conversion rate: % of business cases sent that result in deal advancement (weekly)
- ROI prediction accuracy: projected vs realized scatter plot for closed-won deals (monthly)
- Active experiment status: current A/B test with running results
- Autonomous optimization activity: anomalies detected, experiments run, changes adopted (weekly)
- Value driver contribution: which drivers produce the most savings across deals (monthly)
- Industry benchmark accuracy: how well benchmarks predict individual deal ROI (quarterly)

**Alerts:**
- Calculator completion rate drops below 50% for 3 consecutive days
- ROI prediction accuracy falls below 65% on the monthly report
- Auto-generation pipeline error rate exceeds 10%
- No experiments completed in the last 30 days (optimization has stalled)

### 4. Deploy adaptive personalization

Use accumulated data to personalize ROI calculators beyond what was possible at Scalable:

**Persona-based framing:**
- CFO/Finance: lead with payback period and TCO comparison, conservative scenario only
- VP Sales: lead with revenue impact and competitive win rate improvement, show upside scenario
- VP Operations: lead with time savings and FTE reallocation, show efficiency metrics
- CEO: lead with strategic value (market position, growth acceleration), executive summary only

**Industry-specific models:**
- Pre-populate industry benchmarks so prospects see their peers' outcomes
- Adjust value driver weights by industry (manufacturing → cost reduction; SaaS → revenue increase)
- Include industry-specific risk factors and mitigations in business cases

**Deal-size adaptation:**
- SMB (<$10K ACV): one-page ROI summary, no business case needed
- Mid-market ($10-100K ACV): ROI calculator + 2-page business case
- Enterprise (>$100K ACV): full ROI model + detailed business case + executive presentation deck

The agent tests personalization variants through the autonomous optimization loop (Phase 3).

### 5. Monitor for convergence

The optimization loop runs indefinitely. However, the agent should detect **convergence** — when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments). At convergence:

1. The ROI calculator system has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Report to the team: "The ROI calculator play is optimized. Current performance: {metrics}. Further gains require strategic changes (new value propositions, new market segments, product changes) rather than tactical optimization."
4. Continue accuracy measurement and calibration — the model should keep improving even after framing optimization converges

### 6. Evaluate sustainability

After 6 months, assess:
- Are all KPIs sustained at or above Scalable-level performance?
- Is ROI prediction accuracy improving quarter over quarter?
- Has the optimization loop converged, or is it still finding improvements?
- What is the agent experiment win rate (adopted / total experiments)?
- What is the net impact of all adopted changes over 6 months?

If metrics sustain or improve: the play is durable. The agent maintains performance autonomously.
If metrics decay: diagnose root cause — market saturation (prospects have seen your ROI pitch), model staleness (benchmarks outdated), or product changes (new features not reflected in value drivers). Address the root cause and restart the optimization loop.

## Time Estimate

- 25 hours: deploying autonomous optimization loop (n8n workflows, anomaly detection, hypothesis generation, experiment infrastructure)
- 15 hours: scaling prediction accuracy measurement and building the calibration pipeline
- 10 hours: building the ROI intelligence dashboard
- 15 hours: deploying adaptive personalization (persona templates, industry models, deal-size rules)
- 75 hours: monitoring, reviewing weekly briefs, approving high-risk experiments, and iterating over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, experiment logging, calibration data, audit trail | Standard stack (excluded) |
| PostHog | Anomaly detection, experiments, feature flags, dashboards, funnels | Standard stack (excluded) |
| n8n | Autonomous optimization loop, cron scheduling, workflow orchestration | Standard stack (excluded) |
| Anthropic Claude API | ROI model generation, business case generation, hypothesis generation, experiment evaluation | ~$80-200/mo at scale with optimization loop — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Clay | Enrichment for benchmark building and personalization | Growth: $495/mo — [pricing](https://www.clay.com/pricing) |

**Play-specific cost:** ~$575-695/mo (Claude API + Clay Growth)

## Drills Referenced

- `autonomous-optimization` — the core Durable drill: always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for ROI-driven deal conversion
- `roi-prediction-accuracy` — monthly accuracy measurement and calibration pipeline comparing projected vs realized ROI across closed-won deals
- `dashboard-builder` — builds the ROI intelligence dashboard with real-time visibility into calculator effectiveness, prediction accuracy, and optimization activity
