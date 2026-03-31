---
name: experiment-impact-reporting
description: Aggregate experiment results into business impact reports showing cumulative lift, win rates, and ROI
category: Experimentation
tools:
  - PostHog
  - Anthropic
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - hypothesis-generation
  - attio-reporting
---

# Experiment Impact Reporting

This drill produces reports that translate individual experiment outcomes into business impact. It answers the question every stakeholder asks: "Is all this testing actually making a difference?" The report aggregates cumulative lift, tracks win rates, calculates the ROI of the testing program, and identifies which product areas yield the highest returns from experimentation.

## Prerequisites

- At least 5 completed experiments with results logged in Attio (run `ab-test-orchestrator` or `experiment-pipeline-automation` first)
- PostHog with experiment result data
- Anthropic API key for narrative generation

## Input

- Time period for the report (default: last 30 days)
- Attio experiment records with: hypothesis, result, primary metric lift, confidence level, decision (adopted/reverted/iterated)

## Steps

### 1. Extract experiment outcomes from Attio

Query Attio for all experiments completed in the reporting period. For each experiment, pull:
- Hypothesis statement
- Primary metric: baseline value, variant value, absolute lift, relative lift, confidence
- Secondary metrics: any notable changes
- Decision: adopted, reverted, iterated, or abandoned
- Duration: days from launch to completion
- Product area: which part of the product was tested

### 2. Calculate aggregate metrics

Compute the following for the reporting period:

**Experiment velocity:** Total experiments completed / weeks in period. Target: at least 2 per month at Scalable, 4+ per month at Durable.

**Win rate:** Experiments with adopted results / total experiments completed. Healthy range: 25-40%. Below 25% suggests hypotheses are too speculative. Above 50% suggests the team is testing incremental changes and missing bigger opportunities.

**Cumulative lift:** For each metric that had adopted experiments, sum the individual lifts. Example: if three experiments improved activation rate by +1.2pp, +0.8pp, and +0.5pp, cumulative lift = +2.5pp.

**Testing ROI:** Estimate revenue impact of cumulative lift. Example: if activation rate improved 2.5pp and each activated user generates $50/mo in LTV, ROI = (new_activated_users * $50) / testing_program_cost.

**Cycle time:** Median days from hypothesis creation to experiment completion. Shorter is better — target under 21 days.

### 3. Identify highest-yield product areas

Group experiments by product area (onboarding, pricing, feature adoption, retention flows, etc.). For each area, compute:
- Number of experiments run
- Win rate within that area
- Average lift per winning experiment
- Total cumulative lift

Rank areas by total cumulative lift. This reveals where experimentation produces the most impact and where to focus future hypothesis generation.

### 4. Generate the narrative report

Using the `hypothesis-generation` fundamental (repurposed for analysis), generate a narrative summary:

```
## Experiment Program Report — [Period]

**Velocity:** [X] experiments completed ([Y] per week)
**Win rate:** [Z]% ([W] winners of [X] total)
**Cumulative lift:**
- Activation rate: +[A]pp (from [B]% to [C]%)
- Trial conversion: +[D]pp (from [E]% to [F]%)
- Feature adoption: +[G]pp

**Top performing area:** [Area] — [N] experiments, [lift]

**Key learnings:**
- [Learning 1 from winning experiments]
- [Learning 2 from losing experiments — what did NOT work]
- [Learning 3 — pattern across experiments]

**Recommendations for next period:**
- [Focus area 1 based on highest-yield analysis]
- [Hypothesis type to prioritize based on win rate patterns]
- [Operational improvement if cycle time is too long]
```

### 5. Log the report and distribute

Store the full report in Attio as a note on the A/B testing program record. Post a summary to Slack. For monthly reports, include a comparison to the previous month to show trend direction.

Using `posthog-dashboards`, update the experiment program dashboard with the latest aggregate metrics.

## Output

- Monthly or bi-weekly experiment impact report with aggregate metrics
- Product area ranking by experimentation yield
- Trend comparison to previous period
- Actionable recommendations for the next experiment cycle

## Triggers

- Run bi-weekly at Scalable level
- Run weekly at Durable level (integrated into the `autonomous-optimization` weekly brief)
