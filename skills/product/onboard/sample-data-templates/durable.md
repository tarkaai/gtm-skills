---
name: sample-data-templates-durable
description: >
  Sample Data Acceleration — Durable Intelligence. Autonomous optimization loop that continuously
  monitors sample data and template performance, detects metric anomalies, generates and tests
  improvement hypotheses, and auto-implements winners to sustain ≥80% interaction and ≥15pp
  activation lift as the product and user base evolve.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained ≥80% interaction rate and ≥15pp activation lift over 6 months via autonomous optimization"
kpis: ["Interaction rate (rolling 30-day)", "Activation lift vs. no-sample-data baseline", "Experiment velocity (experiments/month)", "Optimization convergence signal", "AI lift (cumulative improvement from auto-implemented changes)"]
slug: "sample-data-templates"
install: "npx gtm-skills add product/onboard/sample-data-templates"
drills:
  - autonomous-optimization
  - sample-data-engagement-monitor
  - nps-feedback-loop
---

# Sample Data Acceleration — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Success at Durable means: the sample data system sustains or improves its activation lift over 6 months without manual intervention. An autonomous optimization agent monitors metrics, detects degradation, generates hypotheses, runs experiments, and auto-implements winners. The system converges on its local maximum and adapts when the product, user base, or market changes.

## Leading Indicators

- Weekly optimization briefs show net-positive metric changes for 4+ consecutive weeks
- The agent detects and responds to metric anomalies within 24 hours
- Experiment win rate exceeds 30% (at least 1 in 3 experiments produces a meaningful improvement)
- Template gallery grows autonomously (new templates from user patterns, old templates retired)
- NPS scores for recently onboarded users sustain or improve quarter over quarter
- Convergence signal: when successive experiments produce <2% improvement for 3 consecutive experiments, the local maximum is reached

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. Configure it for the sample data play:

**Phase 1 — Monitor (daily via n8n cron):**

The agent checks these KPIs daily against their 4-week rolling averages:
- Sample data interaction rate (target: ≥80%)
- Activation lift vs. control baseline (target: ≥15pp)
- Template install-to-edit rate (target: ≥40%)
- Graduation rate: sample data cleared + real data created within 14 days (target: ≥50%)
- Per-persona interaction rates (target: within 10% of each other)

Classification rules:
- **Normal**: All KPIs within ±10% of rolling average
- **Plateau**: Any KPI within ±2% for 3+ consecutive weeks (performance stagnant)
- **Drop**: Any KPI declines >15% vs. rolling average (degradation detected)
- **Spike**: Any KPI improves >30% vs. rolling average (investigate why — external factor or internal change?)

If anomaly detected → trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

The agent gathers context:
1. Pull 8-week metric history from PostHog for the affected KPI
2. Pull recent product changes from the changelog (new features, UI changes, pricing changes)
3. Pull recent signup volume and source mix (a traffic source change can shift persona mix)
4. Run `hypothesis-generation` with anomaly data + context

Sample hypotheses the agent might generate:
- "Interaction rate dropped because a recent UI change moved sample data below the fold. Fix: restore above-fold placement."
- "Template install rate declined because the top template is now 6 months old and references outdated workflows. Fix: refresh template content."
- "Persona X interaction rate is falling because signup source Y (which skews to persona X) increased volume but the persona detection is misclassifying 30% of them. Fix: refine persona detection rules."
- "Graduation rate plateaued because the graduation prompt fires too early (after session 2). Fix: delay to session 4 when users have more context."

If top hypothesis has risk = "high" → alert team for human review. Otherwise → proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

Design and run the experiment:
1. Use PostHog experiments to create a feature flag splitting traffic between control (current) and variant (hypothesis change)
2. For sample data content changes: deploy the variant seed file to the treatment group
3. For template changes: deploy the updated template to 50% of new installs
4. For UX changes (prompt timing, placement, copy): use PostHog feature flags in the product code
5. Set minimum experiment duration: 7 days or 100+ users per variant, whichever is longer
6. Log experiment start in Attio: hypothesis, start date, expected duration, success metric, guardrails

Guardrails specific to this play:
- If activation rate drops >10pp during an experiment, auto-revert immediately
- If sample data injection errors exceed 1% during a content change experiment, auto-revert
- Never run more than 1 active experiment on sample data and 1 on templates simultaneously

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog
2. Run `experiment-evaluation`: statistical significance, practical significance, secondary metric impact
3. Decision matrix:
   - **Adopt**: Variant improves primary metric by ≥5% at 95% confidence with no secondary metric degradation → auto-implement. Update the seed file, template, or feature flag permanently.
   - **Iterate**: Variant shows directionally positive results (3-5% improvement) but not statistically significant → generate a refined hypothesis and re-test with a larger change.
   - **Revert**: Variant shows no improvement or hurts secondary metrics → disable variant, restore control. Wait 7 days before testing the same variable.
   - **Extend**: Borderline results, needs more data → keep running for another experiment period.
4. Store full evaluation in Attio: decision, confidence level, metric changes, reasoning.

**Phase 5 — Report (weekly via n8n cron):**

Generate a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running: status, current results (preliminary), expected completion date
- Experiments completed: results and decisions
- Net metric change from all adopted changes this week
- Cumulative AI lift: total activation lift improvement since Durable deployment began
- Convergence assessment: are successive experiments showing diminishing returns?
- Recommended focus for next week

Post the brief to Slack and store in Attio.

### 2. Maintain continuous engagement monitoring

Run the `sample-data-engagement-monitor` drill in continuous mode:

- Daily: interaction rate checks, template health scores, persona-level metrics
- Weekly: full cohort comparison reports, template lifecycle analysis (new installs, edits, deletions, archives)
- Monthly: deep-dive analysis comparing the current month's activation funnel to the pre-sample-data baseline. Track the long-term trend line of sample data's causal impact.

The engagement monitor feeds data into the autonomous optimization loop. If the monitor detects a metric below threshold, it triggers Phase 1.

### 3. Deploy NPS feedback for recently onboarded users

Run the `nps-feedback-loop` drill, targeted specifically at users who went through the sample data onboarding:

- Trigger the NPS survey 14 days after signup (post-activation window)
- Segment responses by: received sample data vs. did not, installed templates vs. did not, persona
- Feed detractor feedback into the optimization loop as additional context for Phase 2 diagnosis
- Track NPS for recently onboarded users as a quarterly trend metric

Specific NPS actions for this play:
- If detractors mention "the sample data was confusing" or "templates did not match my use case" → feed directly into hypothesis generation for sample data content changes
- If promoters mention "the sample project helped me understand the product" → document what specifically resonated and reinforce it
- If NPS for recently onboarded users declines quarter-over-quarter → trigger an urgent optimization cycle even if daily metrics look normal

### 4. Build adaptive sample data content

Set up a quarterly content refresh cycle automated by n8n:

1. Query PostHog for the current top activation paths by persona (which sample records get the most engagement, which get ignored)
2. Use the Anthropic API to regenerate low-engagement sample records with updated content (current dates, trending industry references, features released since the last refresh)
3. Validate the new seed file against the current product schema
4. Deploy the updated seed file behind a feature flag and run a 1-week canary test
5. If canary shows no regression, promote to 100%

This ensures sample data never becomes stale even without manual content authorship.

### 5. Evaluate sustainability

This level runs continuously. Monthly checkpoints:

- **Month 1-2**: Establish optimization rhythm. The agent should complete 2-4 experiments per month. Win rate may be low early as the system calibrates.
- **Month 3-4**: Optimization velocity should peak. The agent is running experiments confidently and auto-implementing winners. Cumulative AI lift should be measurable.
- **Month 5-6**: Watch for convergence. If 3 consecutive experiments produce <2% improvement, the system has reached its local maximum. Reduce experiment frequency and shift to maintenance mode.

**Pass threshold: Sustained ≥80% interaction rate and ≥15pp activation lift over 6 months.**

At convergence, the agent reports: "Sample data optimization has converged. Current performance: [interaction rate]%, [activation lift]pp. Further gains require strategic changes — new product features, new market segments, or fundamental onboarding redesign — rather than tactical sample data optimization."

## Time Estimate

- 15 hours: Configure autonomous optimization loop (5 phases) with play-specific parameters
- 10 hours: Set up continuous engagement monitoring in maintenance mode
- 8 hours: Deploy and configure NPS feedback loop for onboarded users
- 7 hours: Build adaptive content refresh automation
- 80 hours: Ongoing monitoring, experiment review, and human oversight over 6 months (~3 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, dashboards, anomaly detection, cohorts | Usage-based from $0.00005/event; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, content regeneration | Claude API: $15/MTok input, $75/MTok output for Opus; $3/$15 for Sonnet ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Intercom | In-app NPS surveys, optimization-driven message variants | Advanced: $85/seat/mo; Proactive Support: $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle emails, experiment variant emails | From $49/mo based on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop scheduling, monitoring workflows, content refresh | Self-hosted: Free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost: ~$150-500/mo** (dominated by Intercom Proactive Support and Anthropic API usage for hypothesis generation)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor → diagnose → experiment → evaluate → implement. Runs daily monitoring, triggers experiments on anomalies, auto-implements winners, generates weekly briefs. Converges when successive experiments produce <2% improvement.
- `sample-data-engagement-monitor` — continuous tracking of interaction rates, template health, persona metrics, and activation funnel performance feeding data into the optimization loop
- `nps-feedback-loop` — quarterly NPS for recently onboarded users, with detractor feedback routed into the optimization loop's hypothesis generation
