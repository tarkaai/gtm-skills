---
name: retention-cohort-analysis-durable
description: >
  Retention Cohort Analytics — Durable Intelligence. Autonomous agent loop that monitors cohort
  retention across all dimensions, generates improvement hypotheses, runs A/B experiments on
  interventions and cohort targeting, and auto-implements winners. Converges when successive
  experiments produce <2% retention improvement.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving cohort retention over 6 months via autonomous optimization"
kpis: ["Retention by cohort", "Experiment velocity", "Cumulative retention lift", "Convergence progress", "AI lift"]
slug: "retention-cohort-analysis"
install: "npx gtm-skills add product/retain/retention-cohort-analysis"
drills:
  - autonomous-optimization
  - cohort-retention-health-monitor
  - cohort-insight-generation
---

# Retention Cohort Analytics — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

The cohort retention analysis operates autonomously. An always-on agent loop monitors retention metrics across all cohort dimensions, detects when retention plateaus or declines in any dimension, generates hypotheses for improvement, runs A/B experiments on interventions and cohort targeting, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs. The system converges when successive experiments produce <2% retention improvement — the play has found its local maximum.

Pass threshold: sustained or improving cohort retention over 6 months. Experiment velocity of 2+ per month during active optimization. Measurable AI lift (improvement attributable to autonomous optimization vs. the Scalable-level static pipeline).

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 2 experiments per month are auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted
- No manual insight review needed — the agent handles the full pipeline from detection to implementation
- Guardrail alerts fire correctly when thresholds are breached
- Cumulative retention lift ledger shows positive trajectory

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the retention cohort analysis play. The optimization loop monitors retention-specific KPIs and runs the 5-phase cycle:

**Phase 1 — Monitor (daily via n8n cron):**

The agent queries PostHog for the play's core retention KPIs:
- Overall Week 4 retention rate (population level)
- Per-dimension Week 4 retention (acquisition channel, plan type, feature breadth, onboarding status)
- Insight-to-action pipeline throughput (insights generated / actioned / validated this week)
- Active experiment status and progress toward sample size

It compares the last 2 weeks against the 4-week rolling average using `posthog-anomaly-detection` and classifies each metric as normal, plateau, drop, or spike. If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

The agent gathers context:
- Current retention intervention configurations (which Intercom messages, Loops sequences, and feature flags are active)
- The retention lift ledger showing all past experiment outcomes
- The latest `cohort-retention-health-monitor` weekly brief
- 8-week metric history per dimension from PostHog

It runs `hypothesis-generation` with this context to produce 3 ranked hypotheses. Examples of hypotheses the agent might generate for this play:

- "Week 4 retention for paid-social cohorts dropped 18% after the landing page redesign on W12. The new page attracts users with different intent. Test: revert the CTA copy for paid-social traffic while keeping the new design."
- "Feature-breadth cohort '1 feature' has stagnated at 12% Week 4 retention for 6 weeks. Current tooltip intervention targets session 3 but data shows these users disengage after session 1. Test: move the feature discovery trigger to the end of session 1 instead of session 3."
- "Free-tier Week 8 retention spiked 25% last week. Investigate: correlates with the new template gallery launch. If confirmed, promote the template gallery more prominently to other underperforming cohorts."

If the top hypothesis is high-risk (affects >50% of users or changes a core intervention), the agent sends an alert and waits for human approval.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

The agent implements the experiment using PostHog feature flags. It splits the targeted cohort between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 14 days or 100 samples per variant for retention experiments (longer than typical because retention measurement requires time for users to either return or churn).

For intervention experiments: the agent creates a variant message/sequence and routes the targeted cohort segment to it. For targeting experiments: the agent adjusts which cohort dimension triggers the intervention and measures whether the new targeting captures more at-risk users.

**Phase 4 — Evaluate (triggered by experiment completion):**

The agent runs `experiment-evaluation` to decide: adopt, iterate, revert, or extend.

For retention experiments, evaluation requires extra care:
- Primary metric: Week 4 retention rate for the targeted cohort
- Secondary metrics: Week 1 retention (to catch activation regressions), engagement depth (sessions per user), and NPS score (to catch user satisfaction impacts)
- Guard metric: overall population retention (ensure the intervention for one cohort does not harm others)

Adopted changes are logged to the retention lift ledger in Attio with the full experimental context.

**Phase 5 — Report (weekly via n8n cron):**

The agent generates a weekly retention optimization brief:
- Anomalies detected this week and their classification per dimension
- Experiments running, completed, or queued
- Net cumulative retention lift from all adopted changes since Durable started
- Per-dimension convergence status: which dimensions are still being optimized vs. which have converged
- Recommended focus for next week

Post to the team's notification channel and store in Attio.

### 2. Configure retention-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add retention-specific safeguards:

- **Population retention floor:** If overall Week 4 retention drops below the Scalable-level baseline for 2 consecutive weeks, pause all experiments and revert the most recent adopted change. The optimization may have caused a regression that the per-cohort metrics did not catch.
- **Intervention fatigue:** If any cohort receives 3+ different intervention messages in a 30-day window, pause interventions for that cohort for 14 days. Over-messaging causes churn, not retention.
- **Dimension interaction:** If an experiment on one dimension (e.g., acquisition channel) changes retention in a different dimension (e.g., plan type), flag for human review. The dimensions may be correlated, and the agent should not optimize them independently.
- **Cohort size minimum:** Never run an experiment targeting a cohort with fewer than 50 users per variant. Insufficient sample size leads to false conclusions that pollute the optimization loop.
- **Experiment budget:** Maximum 3 concurrent experiments across all dimensions. More than 3 creates interaction effects that invalidate individual experiment results.

### 3. Enhance the health monitor for Durable cadence

Run the `cohort-retention-health-monitor` drill with Durable-level enhancements:

- Health check frequency: daily instead of weekly (the autonomous loop needs faster feedback)
- Calibration drift detection: daily comparison of predicted cohort performance vs. actual outcomes
- Convergence tracking: add a dashboard panel showing experiment outcomes over time — when the curve flattens (successive experiments produce <2% lift), the dimension has converged
- Integration with the autonomous optimization loop: the health monitor's anomaly detections feed directly into Phase 1 of the optimization cycle

### 4. Maintain insight generation at Durable quality

The `cohort-insight-generation` drill continues to run weekly, but at Durable level its output feeds the autonomous optimization loop rather than being reviewed by humans:

- Insights with priority_score >= 8.0 AND confidence = "high" go directly into the experiment queue
- Insights with priority_score 6.0-7.9 or confidence = "medium" are logged but not auto-queued (they become candidates if high-priority experiments are exhausted)
- Insights with priority_score < 6.0 are discarded

The agent calibrates the priority threshold over time: if too many experiments fail, raise the threshold. If the experiment queue runs empty (no high-priority insights), lower the threshold.

### 5. Detect convergence

The autonomous optimization loop monitors for convergence at two levels:

**Per-dimension convergence:** When 3 consecutive experiments on a single dimension produce <2% retention improvement, that dimension has reached its local maximum. The agent:
1. Logs the convergence event with the final retention level for that dimension
2. Reduces experiment frequency for that dimension from continuous to monthly maintenance checks
3. Continues monitoring for anomalies that would break convergence (external changes, product updates, market shifts)

**Full convergence:** When all active dimensions have converged, the play has reached its overall local maximum. The agent:
1. Generates a convergence report: current retention levels per dimension, total cumulative lift since Durable started, comparison to Scalable baseline
2. Shifts to maintenance mode: daily monitoring continues, but experiments only run when anomalies break convergence
3. Reports: "Cohort retention is optimized. Current performance: [per-dimension metrics]. Further gains require strategic changes (new product features, new acquisition channels, pricing changes) rather than tactical optimization."

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Overall retention: sustained at or above the level achieved at Scalable, or improving
- Per-dimension retention: no dimension below its Scalable-level baseline for 3+ consecutive weeks
- Experiment velocity: 2+ experiments per month during active optimization phases
- AI lift: measurable improvement attributable to autonomous optimization vs. the Scalable-level static pipeline (compare to the holdout control if one was maintained)
- Convergence progress: at least 3 dimensions converged or actively improving

This level runs continuously. Review monthly: what improved, what converged, what external factors changed, whether to add new dimensions.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, PostHog integrations, Anthropic prompts)
- 10 hours: configure retention-specific guardrails and test them with simulated anomalies
- 10 hours: enhance the health monitor for Durable cadence and convergence tracking
- 80 hours: ongoing monitoring, experiment review, guardrail management over 6 months (~3 hours/week)
- 20 hours: monthly strategic reviews and convergence analysis
- 10 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, cohorts, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude) | Daily monitoring, hypothesis generation, experiment evaluation, weekly briefs | ~$80-200/mo at Durable scale — [anthropic.com/pricing](https://anthropic.com/pricing) |
| n8n | Full autonomous pipeline orchestration (daily + weekly crons) | Self-hosted free; cloud from EUR20/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Loops | Intervention email sequences modified by the optimization loop | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages and product tours modified by the optimization loop | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated play-specific cost: $160-400/mo** (Anthropic API for optimization + monitoring + Loops + Intercom)

## Drills Referenced

- `autonomous-optimization` — the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for cohort retention
- `cohort-retention-health-monitor` — daily health checks, convergence tracking, and anomaly detection feeding the optimization loop
- `cohort-insight-generation` — automated insight pipeline feeding the experiment queue with priority-gated entries
