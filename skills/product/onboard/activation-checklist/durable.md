---
name: activation-checklist-durable
description: >
  Onboarding Checklist Workflow — Durable Intelligence. Deploy the autonomous-optimization
  loop to continuously detect metric anomalies, generate improvement hypotheses, run A/B
  experiments, and auto-implement winners. Sustain ≥ 60% completion over 6 months via AI agents.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "40 hours setup + ongoing agent compute over 6 months"
outcome: "Sustained or improving checklist completion ≥ 60% over 6 months via autonomous AI optimization"
kpis: ["Checklist completion rate (sustained ≥ 60%)", "Experiment velocity (target 3-4 per month)", "Cumulative AI-driven lift (target ≥ 10pp over 6 months)", "Convergence indicator (consecutive experiments < 2% improvement)", "NPS score among activated users (target ≥ 40)"]
slug: "activation-checklist"
install: "npx gtm-skills add product/onboard/activation-checklist"
drills:
  - autonomous-optimization
  - dashboard-builder
  - nps-feedback-loop
---

# Onboarding Checklist Workflow — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The activation checklist becomes a self-optimizing system. An AI agent continuously monitors onboarding metrics, detects anomalies, generates improvement hypotheses, designs and runs experiments, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs and converges toward the local maximum -- the best possible checklist performance given the current product, market, and user base.

Pass: Checklist completion rate sustains at ≥ 60% OR improves over 6 months, driven by autonomous AI optimization with minimal human intervention.
Fail: Completion rate decays below 55% for 3+ consecutive weeks despite optimization attempts, or the agent fails to run experiments for 4+ weeks.

## Leading Indicators

- Daily anomaly detection runs without failures for 7 consecutive days (the monitoring loop is stable)
- First autonomous experiment launches within 2 weeks of setup (the agent is generating actionable hypotheses)
- At least 1 of the first 3 experiments produces a statistically significant winner (the optimization is finding real gains)
- Weekly optimization briefs are generated on schedule with actionable recommendations (the reporting loop works)
- NPS among activated users is ≥ 40 (the checklist is not just completing users but satisfying them)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core of the Durable level. Configure it for the activation checklist play:

**Phase 1 — Monitor (daily via n8n cron):**

Build an n8n workflow using `n8n-scheduling` triggered daily at 09:00 UTC:

1. Use `posthog-anomaly-detection` to check the checklist's primary KPIs:
   - Overall completion rate (14-day rolling)
   - Per-step completion rates
   - Median time-to-activation
   - Email sequence engagement rates (open, click)
   - Stalled-user re-engagement rate
2. Compare last 2 weeks against 4-week rolling average.
3. Classify each KPI:
   - **Normal:** Within ±10% of rolling average. Log to Attio, no action.
   - **Plateau:** Within ±2% for 3+ weeks. Flag for optimization.
   - **Drop:** > 20% decline. Flag as urgent, trigger Phase 2.
   - **Spike:** > 50% increase. Investigate cause (may be external: product change, traffic spike).
4. If anomaly detected, trigger Phase 2 with the anomaly context.

**Phase 2 — Diagnose (triggered by anomaly):**

1. Gather context from Attio using `attio-notes`: pull the checklist's current configuration (step order, email timing, celebration copy, active experiments).
2. Pull 8-week metric history from PostHog using `posthog-dashboards`.
3. Run `hypothesis-generation` with:
   - The anomaly data (which KPI, direction, magnitude)
   - Current configuration
   - History of past experiments and their outcomes (from Attio)
   - Per-step drop-off data
4. Receive 3 ranked hypotheses. Each hypothesis includes: what to change, expected impact, risk level (low/medium/high), and which PostHog metric to measure.
5. Store hypotheses in Attio as notes on the play's record.
6. If top hypothesis has risk = "high" (e.g., changes affecting > 50% of users or requiring product code changes):
   - **Human action required:** Send alert to Slack with hypothesis details and ask for approval before proceeding.
7. If risk = "low" or "medium", proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis.
2. Use `posthog-experiments` to create a feature flag splitting traffic 50/50 between control and variant.
3. Implement the variant. Examples of what the agent can autonomously change:
   - Email subject lines and body copy (via Loops API using `loops-sequences`)
   - Email send timing (via n8n workflow schedule adjustment using `n8n-scheduling`)
   - In-app message copy and targeting rules (via Intercom API using `intercom-in-app-messages`)
   - Checklist step order (via PostHog feature flag controlling step rendering)
   - Celebration messages and CTAs (via Intercom API)
   - Stall intervention timing and copy (via n8n workflow + Loops)
4. Set experiment duration: minimum 7 days OR 200+ observations per variant, whichever is longer.
5. Log experiment start in Attio: hypothesis text, start date, expected end date, success criteria, variant description.

**Guardrails (CRITICAL):**
- Maximum 1 active experiment at a time. Never stack experiments.
- If checklist completion rate drops > 30% during an experiment, auto-revert immediately.
- Human approval required for: changes affecting > 50% of users, changes to the milestone definitions themselves, or any hypothesis flagged "high risk."
- After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.

**Phase 4 — Evaluate (triggered by experiment end):**

1. Pull experiment results from PostHog using `posthog-experiments`.
2. Run `experiment-evaluation` with control vs variant data:
   - Check statistical significance (95% confidence).
   - Check practical significance (is the improvement ≥ 2pp?).
   - Check secondary metrics (did the winner hurt retention, NPS, or engagement?).
3. Decision:
   - **Adopt:** Variant wins. Update live configuration permanently. Remove the feature flag. Log in Attio: hypothesis, result, confidence, new baseline metric.
   - **Iterate:** Result is directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** Variant lost or caused harm. Disable variant, restore control. Log failure. Return to Phase 1 monitoring. Apply 7-day cooldown on that variable.
   - **Extend:** Sample size insufficient. Keep running for 1 more period.

**Phase 5 — Report (weekly via n8n cron):**

Build an n8n workflow using `n8n-scheduling` triggered every Monday at 08:00 UTC:

1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments running, experiments completed, decisions made.
2. Calculate:
   - Net metric change from all adopted changes this week.
   - Cumulative metric change since Durable level began.
   - Current distance from estimated local maximum (based on diminishing returns trend).
3. Generate a weekly optimization brief using Claude (via `hypothesis-generation`):
   - What changed and why.
   - Net impact on completion rate and secondary KPIs.
   - Status of active experiments.
   - Recommended focus for next week.
   - Convergence status: are improvements diminishing?
4. Post the brief to Slack and store in Attio.

### 2. Build the onboarding health dashboard

Run the `dashboard-builder` drill. Create a PostHog dashboard using `posthog-dashboards` with the following panels:

**Row 1 — Headlines:**
| Panel | Metric | Visualization |
|-------|--------|--------------|
| Completion Rate (7d) | `activation-checklist_converted` / `activation-checklist_impression` | Trend line with 60% threshold marker |
| Median Time to Activation | Median `time_since_signup_hours` at conversion | Trend line |
| Active Experiment | Current experiment name and variant | Text card |

**Row 2 — Funnel Health:**
| Panel | Metric | Visualization |
|-------|--------|--------------|
| Checklist Step Funnel | Per-step completion rates | Funnel chart |
| Step Drop-off Trend | Per-step drop-off over 8 weeks | Multi-line trend |
| Completion by Segment | Completion rate by signup source and plan type | Bar chart |

**Row 3 — Email & Interventions:**
| Panel | Metric | Visualization |
|-------|--------|--------------|
| Email Sequence Performance | Open/click rate by email step | Bar chart |
| Stall Interventions | Interventions sent vs re-engagements | Stacked bar |
| Celebration CTA Performance | Click-through rate by milestone | Bar chart |

**Row 4 — Optimization History:**
| Panel | Metric | Visualization |
|-------|--------|--------------|
| Experiment Log | All experiments: name, dates, result, lift | Table |
| Cumulative AI Lift | Total completion rate improvement from adopted experiments | Trend line |
| Convergence Trend | Lift from last 5 experiments | Bar chart (shows diminishing returns) |

Set up alerts using `posthog-cohorts`:
- Completion rate drops below 55% for 3 consecutive days -> urgent Slack alert.
- Any step drop-off exceeds 40% -> warning Slack alert.
- Email bounce rate exceeds 5% -> warning Slack alert.
- Zero checklist impressions for 24 hours -> critical Slack alert (possible tracking breakage).

### 3. Launch the NPS feedback loop

Run the `nps-feedback-loop` drill. Configure NPS specifically for the onboarding checklist:

**Survey timing:**
Using `intercom-in-app-messages`, trigger the NPS survey 7 days after a user completes the checklist. Never survey during onboarding (too early) or users who did not complete the checklist (different problem).

**Survey format:**
- Question 1: "How likely are you to recommend [product] to a colleague?" (0-10)
- Question 2: "What was the hardest part of getting started?" (open text, required)

**Segment and analyze** using `posthog-cohorts`:
- Cross-reference NPS scores with checklist completion data: which steps did promoters complete fastest? Which steps do detractors cite as problematic?
- Compare NPS by signup source, plan type, and checklist variant (from experiments).

**Close the loop** using `loops-transactional`:
- **Promoters (9-10):** Thank them. Ask if they would write a review or refer a colleague. Route to the `referral-program` drill.
- **Passives (7-8):** Ask what one change would make them a promoter. Feed answers into the hypothesis generator.
- **Detractors (0-6):** Personal outreach from a team member within 48 hours. Log in Attio using `attio-notes` and assign follow-up. Feed their specific feedback into the optimization loop as a high-priority hypothesis.

**Feed NPS into the optimization loop:**
- Aggregate open-text responses monthly by theme: confusing step, too many steps, irrelevant step, missing help, technical issue.
- The most common detractor theme becomes a candidate hypothesis in Phase 2 of the autonomous optimization loop.

### 4. Monitor for convergence

The optimization loop runs indefinitely. However, detect convergence -- when the checklist has reached its local maximum:

**Convergence criteria:** 3 consecutive experiments produce < 2% improvement in the primary metric (completion rate).

**When convergence is detected:**
1. Reduce monitoring frequency from daily to weekly.
2. Reduce experiment frequency from 3-4/month to 1/month (maintenance experiments).
3. Generate a convergence report:
   - Current performance: completion rate, time-to-activation, NPS.
   - Total improvement since Durable started: cumulative lift from all adopted experiments.
   - What was optimized: list of all adopted changes.
   - What remains: any untested hypotheses or known issues.
   - Strategic recommendations: "Further gains require [product changes / new features / different user segments] rather than tactical optimization."
4. Post the convergence report to Slack and store in Attio.

**After convergence, continue monitoring for:**
- External shocks: product changes, traffic source changes, competitive shifts that affect the checklist.
- Seasonal patterns: onboarding behavior may vary by quarter.
- Gradual decay: if completion rate drops 5pp below the converged baseline, re-enter active optimization.

## Time Estimate

- Autonomous optimization loop setup (n8n workflows, PostHog configuration, Attio templates): 15 hours
- Dashboard build: 5 hours
- NPS feedback loop setup: 5 hours
- Testing all automation pipelines end-to-end: 5 hours
- Ongoing monitoring and brief review (6 months, ~2 hours/week): 50 hours
- Total: ~40 hours setup + ~50 hours ongoing over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards, cohorts | Free 1M events; paid starts at $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop scheduling, intervention routing, weekly reporting | Pro €60/mo for 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief generation | Claude API usage-based ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Intercom | In-app messages, NPS surveys, experiment variants | Essential $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Email experiments, NPS follow-ups, stall interventions | $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Experiment log, hypothesis tracking, NPS follow-up routing | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Durable:** $150-250 base (Intercom $29 + n8n $60 + Loops $49 + Anthropic API ~$10-50 for hypothesis generation and evaluation + PostHog overage if applicable). Agent compute costs are variable based on monitoring frequency and experiment volume.

## Drills Referenced

- `autonomous-optimization` -- the core always-on optimization loop: monitor metrics daily, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs, detect convergence
- `dashboard-builder` -- build a PostHog dashboard showing onboarding health, experiment history, and convergence trends in real time
- `nps-feedback-loop` -- collect NPS from activated users, close the loop per segment, and feed qualitative insights into the autonomous optimization hypothesis generator
