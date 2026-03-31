---
name: conference-speaking-program-durable
description: >
  Conference Speaking — Durable. Autonomous AI agents continuously optimize conference
  targeting, proposal quality, content repurposing, and lead capture. The optimization loop
  detects metric anomalies, generates improvement hypotheses, runs experiments, and
  auto-implements winners. Weekly optimization briefs. Converges when experiments produce <2% improvement.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Events, Social"
level: "Durable"
time: "120 hours over 12 months"
outcome: "Sustained ≥15 leads per talk average with cost-per-lead declining quarter over quarter for 12 months"
kpis: ["Leads per talk (sustained)", "Cost per lead trend", "Proposal acceptance rate trend", "Content repurposing multiplier trend", "Optimization experiment win rate", "Time to convergence"]
slug: "conference-speaking-program"
install: "npx gtm-skills add marketing/problem-aware/conference-speaking-program"
drills:
  - autonomous-optimization
  - conference-cfp-pipeline
---

# Conference Speaking — Durable

> **Stage:** Marketing → ProblemAware | **Motion:** MicroEvents | **Channels:** Events, Social

## Outcomes

The speaking program runs on autopilot with AI agents finding the local maximum. The `autonomous-optimization` drill monitors all speaking KPIs daily, detects when metrics plateau or drop, generates hypotheses for improvement, designs and runs experiments, evaluates results, and auto-implements winners. The human reviews weekly optimization briefs and approves high-risk changes. The program converges when successive experiments produce <2% improvement -- meaning the agent has found the best possible performance given current market conditions.

## Leading Indicators

- Optimization loop fires daily with no manual intervention
- At least 1 experiment running at all times (until convergence)
- Weekly optimization brief generated every Monday
- Cost per lead trending down or stable quarter over quarter
- Acceptance rate trending up or stable
- Convergence signal: 3 consecutive experiments produce <2% improvement on any given KPI

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the speaking program:

**Phase 1 — Monitor (daily via n8n cron):**

1. Use `posthog-anomaly-detection` to check speaking program KPIs:
   - CFP acceptance rate (trailing 4 weeks vs 8-week rolling average)
   - Leads per talk (trailing 4 weeks vs 8-week rolling average)
   - Content repurposing multiplier (repurposed leads / live leads)
   - Post-talk email sequence open rate and click rate
   - Cost per lead
2. Classify each KPI: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
3. If all KPIs normal → log to Attio, no action
4. If any anomaly detected → trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**

1. Gather context: pull current speaking program configuration from Attio (target conference profile, proposal style, follow-up sequence, content repurposing cadence)
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` via Claude API with the anomaly data + context
4. Receive 3 ranked hypotheses. Examples of hypotheses the agent might generate:
   - "Acceptance rate dropped because we shifted to larger conferences (>2000 attendees) where competition is fiercer. Hypothesis: target mid-size conferences (200-1000) for the next 4 submissions."
   - "Leads per talk plateaued because companion page CTA is too weak. Hypothesis: replace generic 'Learn More' with a specific resource offer ('Get the code from my demo')."
   - "Content repurposing multiplier is declining because we're posting clips too late. Hypothesis: publish first clip within 48 hours of talk, not 7 days."
5. Store hypotheses in Attio
6. If top hypothesis is flagged "high risk" (e.g., changes targeting for >50% of submissions) → send Slack alert for human approval and STOP
7. If risk is "low" or "medium" → proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Design the experiment based on the hypothesis type:
   - **Proposal experiments:** A/B test proposal variants using `posthog-experiments` feature flags to assign CFPs to control vs variant style
   - **Lead capture experiments:** Test different companion page designs, CTA copy, or follow-up email sequences
   - **Targeting experiments:** Split next 10 CFP submissions between current conference profile and the hypothesized adjustment
   - **Content repurposing experiments:** Test posting cadence, clip length, or format (vertical vs square)
2. Set experiment duration: minimum 4 weeks or until 20+ data points per variant (whichever is longer)
3. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog
2. Run `experiment-evaluation` via Claude API
3. Decision:
   - **Adopt:** Update the live configuration. Example: if "result-first" proposal style beat "problem-first" by 15% acceptance rate, update the default proposal prompt.
   - **Iterate:** Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert:** Restore the control configuration. Log the failure. Return to Phase 1.
4. Store full evaluation in Attio with decision, confidence interval, and reasoning

**Phase 5 — Report (weekly via n8n cron, every Monday 9am):**

1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments running, decisions made
2. Calculate net metric change from all adopted changes
3. Generate weekly optimization brief via Claude:
   - What changed and why
   - Net impact on primary KPIs (leads per talk, acceptance rate, cost per lead)
   - Current estimated distance from local maximum
   - Recommended focus for next week
4. Post brief to Slack and store in Attio

### 2. Maintain the speaking performance monitor

The `autonomous-optimization` drill continues running from Scalable:

1. Dashboard stays live and auto-updates
2. Automated alerts continue firing (acceptance rate drops, lead capture failures, sequence underperformance)
3. Quarterly analysis continues generating program-level briefs
4. Talk topic lifecycle tracker flags topics ready for retirement or refresh

The optimization loop from step 1 uses this monitoring data as its input. The monitor surfaces the data; the optimization loop acts on it.

### 3. Keep the CFP pipeline fed

The `conference-cfp-pipeline` continues running on autopilot:

1. Bi-weekly CFP discovery (n8n cron → Clay refresh → score → generate proposals)
2. The optimization loop may update the proposal generation prompts, scoring weights, or target conference profiles based on experiment results
3. Human reviews batch-approved proposals twice per week
4. Volume target: 20-30 CFP submissions per quarter (the optimization loop determines the right mix of conference sizes, regions, and topics)

### 4. Guardrails (critical)

These guardrails prevent the optimization loop from causing damage:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold:** If any primary KPI drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Changes to the speaker bio or positioning
  - Targeting changes that shift >50% of submissions to a new conference profile
  - Budget changes >20%
  - Any hypothesis flagged "high risk"
- **Cooldown:** After a failed experiment (revert), wait 2 bi-weekly CFP cycles before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 2 (speaking program has slower feedback loops than email campaigns -- each experiment needs sufficient data).
- **Never optimize what is not measured:** If a KPI lacks PostHog tracking, fix tracking first.

### 5. Detect convergence

The optimization loop runs indefinitely until it detects convergence:

1. Track the impact of each experiment as a percentage improvement
2. When 3 consecutive experiments on the same KPI produce <2% improvement, that KPI has converged
3. When all primary KPIs have converged:
   - Reduce monitoring frequency from daily to weekly
   - Post convergence report: "Speaking program has reached local maximum. Current performance: [metrics]. Further gains require strategic changes (new markets, new talk formats, product changes) rather than tactical optimization."
4. Continue weekly monitoring to detect market shifts that might de-optimize the program (new competitors, audience shifts, conference landscape changes)

## Time Estimate

- 10 hours: Optimization loop setup (n8n workflows, Claude prompts, experiment infrastructure)
- 2 hours per month x 12 months: Human review of weekly briefs and high-risk approvals = 24 hours
- 2 hours per month x 12 months: Talk preparation and delivery = 24 hours
- 4 hours per quarter x 4 quarters: Quarterly strategic review = 16 hours
- 46 hours: Agent-automated work (monitoring, diagnosis, experiments, evaluation, reporting)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Automated CFP discovery and scoring | Launch: $185/mo (https://www.clay.com/pricing) |
| Descript | Talk content repurposing | Creator: $24/mo (https://www.descript.com/pricing) |
| Anthropic API | Optimization loop (hypothesis, evaluation, briefs) + proposals | ~$15-25/mo at Durable frequency |
| Cal.com | Booking links | Free or Team: $12/user/mo (https://cal.com/pricing) |
| Loops | Post-talk sequences | Free up to 1,000 contacts (https://loops.so/pricing) |
| Sessionize | Speaker profile management | Free for speakers (https://sessionize.com/pricing) |

**Total Durable budget:** Clay $185/mo + Descript $24/mo + Anthropic ~$20/mo = ~$229/mo

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate → auto-implement winners → report weekly
- `autonomous-optimization` — dashboard, alerts, quarterly analysis, and talk topic lifecycle tracking
- `conference-cfp-pipeline` — continuous CFP discovery and proposal generation, updated by optimization experiments
