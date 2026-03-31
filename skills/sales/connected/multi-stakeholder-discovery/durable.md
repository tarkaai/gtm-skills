---
name: multi-stakeholder-discovery-durable
description: >
  Multi-Stakeholder Discovery Process — Durable Intelligence. Always-on AI agents continuously
  optimize multi-stakeholder discovery: stakeholder mapping accuracy, outreach effectiveness,
  discovery question quality, and consensus building strategies. The autonomous optimization
  loop detects metric anomalies, generates improvement hypotheses, runs A/B experiments, and
  auto-implements winners. Weekly optimization briefs track convergence toward the local maximum.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving consensus building (>=70% of deals reach consensus >=60 before proposal) and >=30% deal velocity improvement over 6 months with <2% variance in successive optimization cycles"
kpis: ["Consensus achievement rate (sustained)", "Autonomous experiment win rate", "Stakeholder engagement reply rate (optimized)", "Deal velocity improvement trend", "Optimization convergence rate"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
drills:
  - autonomous-optimization
---

# Multi-Stakeholder Discovery Process — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Always-on AI agents finding the local maximum. The multi-stakeholder discovery program runs itself: stakeholder mapping triggers automatically for new deals, outreach sequences adapt to what works, post-call extraction improves with each transcript, consensus tracking catches problems before they stall deals, and the reporting layer feeds continuous optimization. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in discovery KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement — the discovery process has reached peak performance for the current market.

**Pass threshold:** Sustained or improving consensus building (>=70% of deals reach consensus >=60 before proposal) and >=30% deal velocity improvement over 6 months with <2% variance in successive optimization cycles.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Stakeholder outreach reply rate improves quarter over quarter
- Consensus score at time of proposal trends upward across the pipeline
- Discovery question quality improves (measured by answer usefulness)
- Convergence signal: last 3 experiments each produced <2% improvement

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the multi-stakeholder discovery program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check discovery program KPIs:
  - Stakeholder outreach reply rate (by role)
  - Discovery call booking rate
  - Post-call extraction accuracy (spot-checked weekly)
  - Consensus score at time of proposal
  - Time from deal creation to >=75% stakeholder coverage
  - Deal velocity (multi-threaded vs single-threaded)
  - Engagement gap frequency (how often alerts fire)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current outreach templates, question generation prompts, consensus computation weights, engagement wave timing
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "Economic Buyer outreach reply rate dropped 30%. Hypothesis: the current template sounds too salesy. Test a template that leads with a specific insight from the technical team's discovery calls."
  - "Consensus scores are plateauing at 55 across the pipeline. Hypothesis: discovery questions for Influencers are too generic. Test role-specific questions that reference the prospect's tech stack."
  - "Time to full coverage increased from 12 to 18 days. Hypothesis: Wave 2 is delayed too long after Wave 1. Test reducing the gap from 10 days to 5 days."
  - "Post-call extraction is missing concern categories. Hypothesis: the extraction prompt does not ask about timeline concerns. Test adding timeline to the extraction schema."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate tool:
  - If testing outreach messaging: create new Instantly sequence variant
  - If testing discovery questions: update the Claude prompt with new parameters
  - If testing engagement wave timing: adjust n8n workflow delays
  - If testing consensus weights: modify the computation formula
  - If testing extraction prompts: update the sentiment extraction prompt
- Set experiment duration: minimum 7 days or 30+ deals processed per variant
- Log experiment in Attio with hypothesis, start date, duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update live configuration, log the change, move to Phase 5
- If Iterate: generate new hypothesis building on this result, return to Phase 2
- If Revert: restore control configuration, log failure, return to Phase 1
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on discovery KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Enhanced Reporting

Run the `autonomous-optimization` drill with Durable-level additions:

**Monthly ROI calculation:**
- Compare close rates: deals with comprehensive multi-stakeholder discovery (>=4 roles engaged, consensus >=60) vs deals without
- Compare deal velocity: average days to close for high-discovery vs low-discovery deals
- Compare deal size: average contract value for high-discovery vs low-discovery deals
- Estimate monthly ROI: (incremental revenue from improved close rate and velocity) - (total cost of discovery tooling and time)

**Optimization effectiveness reporting:**
- Track cumulative impact of all adopted experiments
- Chart the diminishing returns curve: each successive experiment's improvement %
- Predict when convergence will occur based on the improvement trend

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the discovery program:

- **Rate limit:** Maximum 1 active experiment at a time on the discovery program
- **Revert threshold:** If consensus achievement rate drops below 50% during any experiment, auto-revert immediately
- **Human approval required for:**
  - Changes to the stakeholder role classification criteria
  - Changes to the consensus score formula weights
  - Changes to the pre-proposal gate threshold
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All discovery events must have PostHog tracking before experiments can target them

### 4. Build Predictive Stakeholder Intelligence

As the optimization loop accumulates data over months, build predictive capabilities:

**Stakeholder structure prediction:**
- Analyze historical deals: at companies of similar size, industry, and complexity, what was the typical buying committee structure?
- Before the first discovery call at a new account, predict which roles will be involved and their likely priorities
- Track `stakeholder_prediction_accuracy`: % of predicted stakeholders who actually participate in the buying decision
- If accuracy < 60%, the prediction model needs more training data or different features

**Consensus trajectory prediction:**
- Based on the current stakeholder sentiment distribution, predict whether the deal will reach consensus >=60 by proposal time
- If prediction is "unlikely to reach consensus": proactively recommend which stakeholders to prioritize and what approach to take
- Track prediction accuracy and feed it back into the model

**Outreach timing optimization:**
- Learn the optimal timing for each engagement wave by analyzing which delays between waves produce the best reply rates
- This is data the optimization loop will naturally experiment on

### 5. Monitor Convergence

The optimization loop should detect when the discovery program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Multi-stakeholder discovery optimized. Current consensus achievement rate: {X}%. Current deal velocity improvement: {Y}%. Further gains require strategic changes (new buyer personas, new verticals, product positioning shifts) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 6. Handle Strategic Shifts

When external conditions change (new product launch, entering a new market segment, major competitor move), the optimizer should detect the shift via metric anomalies and respond:

- If stakeholder engagement patterns shift dramatically (new roles appearing, old roles disengaging): market conditions may have changed
- If consensus scores drop across the board despite healthy engagement: competitive landscape may have shifted
- In these cases: alert the founder that tactical optimization is insufficient and strategic review is needed. Provide data to support the diagnosis: "Since {date}, Economic Buyer reply rates dropped {X}% and the most common concern shifted from {old} to {new}. This suggests {analysis}."

## Time Estimate

- 12 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 8 hours: Enhanced reporting with monthly ROI and optimization effectiveness tracking
- 5 hours: Predictive intelligence initial calibration
- 70 hours: Ongoing optimization over 6 months (~2.5 hours/week for monitoring, experiment design, evaluation)
- 15 hours: Monthly strategic reviews (human reviews optimization brief, approves high-risk changes)
- 10 hours: Convergence analysis and maintenance mode transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — stakeholder tracking, experiment logging, reporting | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — stakeholder mapping, org chart research | $185/mo (Launch) or $495/mo (Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| Instantly | Cold email — stakeholder outreach sequences with A/B variants | $47/mo (Growth) or $97/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Cal.com | Scheduling — discovery call booking | Free or $15/user/mo (Teams) — [cal.com/pricing](https://cal.com/pricing) |
| Fireflies | Transcription — discovery call recording and extraction | $10/user/mo (Pro, annual) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — optimization loop, monitoring, reporting, orchestration | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — sentiment extraction, question generation, hypothesis generation, experiment evaluation | Usage-based, ~$3/MTok input (Sonnet 4.6) — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost this level:** ~$300-700/mo. Primary cost drivers: Clay ($185-495), Instantly ($47-97), n8n Pro ($60), Anthropic API (~$40-80/mo for optimization loop + extraction + generation).

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — comprehensive reporting on discovery effectiveness: coverage funnels, consensus distributions, win rate correlation, role engagement rates, program ROI. Provides the data layer the optimization loop reads from.
