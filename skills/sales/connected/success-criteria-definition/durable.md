---
name: success-criteria-definition-durable
description: >
  Success Criteria Definition — Durable Intelligence. Always-on AI agents continuously optimize
  success criteria definition, recommendation accuracy, and post-sale achievement tracking. The
  autonomous optimization loop detects metric anomalies, generates improvement hypotheses, runs
  A/B experiments, and auto-implements winners. Weekly optimization briefs track convergence
  toward the local maximum of criteria-driven deal acceleration and customer retention.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving close rate lift (>=20%) for criteria-defined deals over 6 months, with criteria achievability model accurate to within +-10%, and <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Close rate lift sustained", "Achievability model accuracy", "Post-sale achievement rate", "Autonomous experiment win rate", "Optimization convergence rate"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
drills:
  - autonomous-optimization
  - success-criteria-reporting
---

# Success Criteria Definition — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Always-on AI agents finding the local maximum. The success criteria program runs itself: extraction, recommendation, workshop preparation, plan generation, and post-sale tracking all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in criteria program KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement — at that point, the criteria program has reached its optimal performance given the current market conditions.

**Pass threshold:** Sustained or improving close rate lift (>=20%) for criteria-defined deals over 6 months, with criteria achievability model accurate to within +-10%, and <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Achievability model accuracy improves over time (predicted scores match actual achievement rates)
- Convergence signal: last 3 experiments produced <2% improvement each

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the success criteria program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check success criteria program KPIs:
  - Definition rate (% of Connected deals with criteria)
  - Workshop booking rate (scheduling message → booked call)
  - Mutual agreement rate (workshop → agreed plan)
  - Close rate lift (criteria deals vs non-criteria deals)
  - Post-sale achievement rate (% of criteria met)
  - Achievability model accuracy (predicted vs actual)
  - Recommendation acceptance rate (AI-recommended criteria adopted by prospects)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current scheduling messages, criteria templates, success plan format, recommendation model parameters
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "Workshop booking rate dropped 30%. Hypothesis: scheduling message has fatigued after 10 weeks. Test a new framing that leads with the prospect's specific pain point instead of generic 'alignment' language."
  - "Post-sale achievement rate for revenue criteria dropped to 40%. Hypothesis: the achievability model is overestimating revenue criteria for companies <50 employees. Recalibrate the model with company-size segmentation."
  - "Close rate lift plateaued at 18%. Hypothesis: the success plan format is too dense — prospects aren't reading it. Test a one-page visual summary vs the current table format."
  - "Recommendation acceptance rate declining. Hypothesis: AI recommendations are too generic for niche industries. Add industry-specific criteria templates for the top 3 verticals."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate tool:
  - If testing scheduling messages: create new Cal.com event type with different description
  - If testing criteria framing: modify the `success-criteria-extraction` prompt
  - If testing success plan format: create an alternative plan template
  - If testing recommendation model: adjust scoring weights in the intelligence engine
- Set experiment duration: minimum 7 days or 30+ samples per variant, whichever is longer
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
  - Net impact on success criteria KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Success Criteria Program Reporting

Run the `success-criteria-reporting` drill:
- Build the PostHog "Success Criteria Program" dashboard (6 panels)
- Build Attio saved views (deals missing criteria, at-risk criteria, lifecycle funnel)
- Set up weekly digest and monthly ROI report
- Configure the anomaly feed that triggers the optimization loop

The reporting layer provides the data substrate that the optimization loop reads. Without accurate reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the success criteria program:

- **Rate limit:** Maximum 1 active experiment at a time on the success criteria program
- **Revert threshold:** If definition rate drops below 60% or close rate lift drops below 10% during any experiment, auto-revert immediately
- **Human approval required for:**
  - Changes to the achievability scoring model that affect how aggressively criteria are recommended
  - Changes to the mutual success plan format that alter the customer-facing commitments
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All success criteria events must have PostHog tracking before experiments can target them

### 4. Predictive Criteria Intelligence

As the optimization loop accumulates data over months, build predictive capability:

- Train on historical data: which criteria combinations (by category, target aggressiveness, and company attributes) best predict won deals and high retention?
- Refine the recommendation model based on prediction accuracy:
  - Track `recommendation_prediction_accuracy`: % of deals where AI-recommended criteria correlated with the actual outcome
  - If accuracy < 60%, the recommendation model needs recalibration — the optimizer should generate a hypothesis about which input weights to adjust
- Eventually, the system should predict: "For {industry} companies with {headcount} employees buying for {use_case}, the optimal criteria mix is {category_1} + {category_2} with targets at {percentile} of similar deals. Expected achievement rate: {X}%. Expected close rate lift: {Y}%."

Log prediction accuracy as a PostHog metric so the optimizer can track and improve it.

### 5. Post-Sale Closed-Loop Optimization

Extend the optimization loop to post-sale outcomes:

- When criteria are marked "achieved" or "missed" in Attio, feed that data back to the intelligence engine
- The optimizer should detect patterns: "Deals where the 'time to value' criterion was set to <30 days achieved at 90%. Deals where it was set to <14 days achieved at only 45%. Recommendation: default to 30-day TTY targets for companies with complex integrations."
- When post-sale achievement rates change, the optimizer should trace back to which stage in the pre-sale process contributed: "Achievement rate dropped because the criteria defined in Q2 were more aggressive than Q1. The workshop scheduling experiment in week 12 may have caused prospects to accept higher targets without pushback."

### 6. Monitor Convergence

The optimization loop should detect when the success criteria program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Success criteria program optimized. Current close rate lift: {X}%. Current achievability accuracy: {Y}%. Current post-sale achievement rate: {Z}%. Further gains require strategic changes (new product capabilities, new market segments, new buyer personas) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 7. Handle Strategic Shifts

When external conditions change (new product launch, new market segment, competitor move), the optimizer should detect the shift via metric anomalies and recommend a strategic review:

- If definition rate drops >30% across all deals: the market's receptivity to success criteria workshops may have changed
- If close rate lift decreases despite healthy criteria definition: the competitive landscape may have shifted, making criteria less of a differentiator
- If post-sale achievement rates drop broadly: product capabilities or implementation quality may have changed
- In these cases: alert the founder that tactical optimization is insufficient and strategic review is needed. Provide the data to support the diagnosis.

## Time Estimate

- 15 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 10 hours: Success criteria reporting dashboard and ROI calculation
- 5 hours: Predictive intelligence model initial calibration
- 80 hours: Ongoing optimization over 6 months (~3 hours/week for monitoring, experiment design, evaluation)
- 10 hours: Monthly strategic reviews (human reviews optimization brief, approves high-risk changes)
- 10 hours: Convergence analysis and maintenance mode transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, criteria attributes, experiment logging, reporting | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Transcription — workshop calls at volume | $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling — workshop booking links | Free or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| n8n | Automation — optimization loop, health monitoring, reporting | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — extraction, recommendations, hypothesis generation, evaluation | Usage-based, ~$30-60/mo at Durable volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$200-400/mo. Primary cost drivers: Attio Pro ($59/user/mo), n8n Pro ($60/mo), Anthropic API (~$30-60/mo for extraction + optimization + evaluation), Fireflies Pro ($18/mo).

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `success-criteria-reporting` — comprehensive reporting on the success criteria program: definition rates, achievement rates, close rate correlation, program ROI. Provides the data layer the optimization loop reads from.
