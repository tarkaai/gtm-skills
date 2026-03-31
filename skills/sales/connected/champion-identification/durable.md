---
name: champion-identification-durable
description: >
  Champion Identification & Development — Durable Intelligence. Always-on AI agents continuously
  optimize champion identification, recruitment, enablement, and multi-threading. The autonomous
  optimization loop detects metric anomalies, generates improvement hypotheses, runs A/B experiments,
  and auto-implements winners. Weekly optimization briefs track convergence toward the local maximum.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving champion impact (>=40% win rate lift) over 6 months with <2% variance in successive optimization cycles, indicating convergence at the local maximum"
kpis: ["Champion win rate lift (sustained)", "Autonomous experiment win rate", "Champion prediction accuracy", "Multi-threading depth trend", "Optimization convergence rate"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - autonomous-optimization
  - champion-program-reporting
---

# Champion Identification & Development — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Always-on AI agents finding the local maximum. The champion program runs itself: profiling, recruitment, enablement, health monitoring, and multi-threading all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in champion KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement — at that point, the champion program has reached its optimal performance given the current market conditions.

**Pass threshold:** Sustained or improving champion impact (>=40% win rate lift) over 6 months with <2% variance in successive optimization cycles, indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Champion prediction accuracy improves over time (profiling correctly identifies people who become active champions)
- Convergence signal: last 3 experiments produced <2% improvement each

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the champion program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check champion program KPIs:
  - Champion recruitment rate (candidates → recruited)
  - Champion activation rate (recruited → active)
  - Champion disengagement rate (active → disengaged)
  - Win rate lift (champion vs non-champion deals)
  - Multi-threading depth (stakeholders per champion deal)
  - Enablement forward rate
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current recruitment messaging, enablement assets, profiling criteria, multi-threading approach
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "Recruitment reply rate dropped 25%. Hypothesis: email subject lines have fatigued after 8 weeks of the same pattern. Test new subject line framework."
  - "Champion activation rate plateaued at 55%. Hypothesis: enablement kit is too long. Test a 1-page summary vs full kit."
  - "Multi-threading depth declining. Hypothesis: champions at companies with 200+ employees need a different introduction template than those at 50-person companies."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate tool:
  - If testing recruitment messaging: create new Instantly sequence variant
  - If testing enablement format: create new Loops sequence variant
  - If testing profiling criteria: adjust Clay scoring weights
  - If testing multi-threading approach: modify the introduction template
- Set experiment duration: minimum 7 days or 50+ samples per variant
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
  - Net impact on champion KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Champion Program Reporting

Run the `champion-program-reporting` drill:
- Build the PostHog "Champion Program Impact" dashboard (6 panels)
- Build Attio saved views (deals at risk, champion-powered, recruitment pipeline)
- Set up monthly ROI calculation workflow
- Configure weekly metrics export that feeds the autonomous optimization loop

The reporting layer provides the data substrate that the optimization loop reads. Without accurate reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the champion program:

- **Rate limit:** Maximum 1 active experiment at a time on the champion program
- **Revert threshold:** If champion win rate lift drops below 20% during any experiment, auto-revert immediately
- **Human approval required for:**
  - Changes to champion profiling criteria that affect which titles/roles are targeted
  - Changes to enablement content that alters the product value proposition
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All champion events must have PostHog tracking before experiments can target them

### 4. Predictive Champion Identification

As the optimization loop accumulates data over months, build predictive capability:

- Train on historical data: which champion candidates (by profile, signals, and company attributes) actually became active champions?
- Refine the profiling scoring model based on prediction accuracy:
  - Track `champion_prediction_accuracy`: % of candidates scored 75+ who reach Active status
  - If accuracy < 50%, the scoring model needs recalibration — the optimizer should generate a hypothesis about which signal weights to adjust
- Eventually, the profiling model should be able to predict: "At companies like {company}, the most effective champion is a {title} in {department} who has been there {tenure} and recently {signal}"

Log prediction accuracy as a PostHog metric so the optimizer can track and improve it.

### 5. Monitor Convergence

The optimization loop should detect when the champion program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Champion program optimized. Current win rate lift: {X}%. Current multi-threading depth: {Y}. Further gains require strategic changes (new channels, new buyer personas, product positioning changes) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 6. Handle Strategic Shifts

When external conditions change (new product launch, new market segment, competitor move), the optimizer should detect the shift via metric anomalies and recommend a strategic review:

- If champion recruitment rate drops >30% across all accounts: market conditions may have changed
- If win rate lift decreases despite healthy champion engagement: the competitive landscape may have shifted
- In these cases: alert the founder that tactical optimization is insufficient and strategic review is needed. Provide the data to support the diagnosis.

## Time Estimate

- 15 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 10 hours: Champion program reporting dashboard and ROI calculation
- 5 hours: Predictive model initial calibration
- 80 hours: Ongoing optimization over 6 months (~3 hours/week for monitoring, experiment design, evaluation)
- 10 hours: Monthly strategic reviews (human reviews optimization brief, approves high-risk changes)
- 10 hours: Convergence analysis and maintenance mode transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — champion tracking, experiment logging, reporting | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — champion profiling, stakeholder search | $185/mo (Launch) or $495/mo (Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| Instantly | Cold email — recruitment and stakeholder outreach | $97/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Loom | Video — champion enablement walkthroughs | $12.50/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Email — enablement sequences | Paid tier — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — optimization loop, health monitoring, reporting | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| LinkedIn Sales Navigator | Prospecting — stakeholder identification | $99.99/mo (Core) — [business.linkedin.com/sales-solutions](https://business.linkedin.com/sales-solutions/compare-plans) |
| Anthropic API | AI — engagement scoring, hypothesis generation, evaluation | Usage-based, ~$3/1M input tokens (Claude Sonnet) — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$300-700/mo. Primary cost drivers: Clay ($185-495), Instantly ($97), LinkedIn Sales Navigator ($100), n8n Pro ($60), Anthropic API (~$20-50/mo for scoring and hypothesis generation).

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `champion-program-reporting` — comprehensive reporting on champion program effectiveness: win rate correlation, recruitment efficiency, multi-threading impact, program ROI. Provides the data layer the optimization loop reads from.
