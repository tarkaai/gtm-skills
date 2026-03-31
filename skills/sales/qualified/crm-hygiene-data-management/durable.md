---
name: crm-hygiene-data-management-durable
description: >
  CRM Hygiene & Data Quality — Durable Intelligence. Always-on AI agents autonomously optimize
  data quality rules, enrichment strategies, deduplication accuracy, and validation strictness.
  The autonomous optimization loop detects quality metric anomalies, generates improvement
  hypotheses, runs A/B experiments, and auto-implements winners. Weekly optimization briefs
  track convergence toward the local maximum.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Product"
level: "Durable Intelligence"
time: "110 hours over 6 months"
outcome: "Sustained or improving data quality (>=90%) over 6 months with <2% variance in successive optimization cycles, indicating convergence at the local maximum"
kpis: ["Data quality score trend", "Error prevention rate", "Agent correction accuracy", "Manual intervention rate", "Optimization convergence rate"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
drills:
  - autonomous-optimization
---

# CRM Hygiene & Data Quality — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Product

## Outcomes

Always-on AI agents finding the local maximum. The data quality system runs itself: validation, enrichment, deduplication, scoring, and reporting all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in data quality KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The system converges when successive experiments produce <2% improvement — at that point, data quality has reached its optimal level given the current CRM structure, enrichment sources, and team behavior.

**Pass threshold:** Sustained or improving data quality (>=90%) over 6 months with <2% variance in successive optimization cycles, indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs generated and posted to Slack
- At least 2 experiments per month initiated, evaluated, and decided
- Error prevention rate trending upward (issues caught before they enter the CRM)
- Manual intervention rate trending downward (fewer records requiring human fixes)
- Convergence signal: last 3 experiments each produced <2% improvement

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the data quality program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check data quality KPIs:
  - Average data quality score (overall and by record type)
  - Critical error rate (missing required fields)
  - Duplicate rate (new duplicates entering the system)
  - Stale record rate (deals with no activity 30+ days)
  - Enrichment success rate (% of auto-enrichment attempts that fill fields)
  - Manual intervention rate (manual fixes per week)
  - Auto-correction accuracy (% of auto-fixes that were not subsequently overridden by humans)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current validation rules, enrichment sources, dedup thresholds, scoring weights
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "Duplicate rate spiked 35%. Hypothesis: fuzzy name matching threshold of 80% is too loose after a recent hiring surge created many contacts with similar names at the same companies. Test tightening to 90%."
  - "Enrichment success rate dropped 20%. Hypothesis: primary data provider coverage has degraded for our target segment. Test switching provider priority order in the waterfall."
  - "Quality score plateaued at 91%. Hypothesis: the remaining 9% gap is concentrated in 'activity' score component. Test reducing the stale threshold from 30 days to 21 days to prompt more frequent engagement."
  - "Manual intervention rate increased 15%. Hypothesis: auto-correction is reverting valid entries because the email regex is too strict. Test relaxing the regex to allow subaddressing (user+tag@domain.com)."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting affected records between control and variant
- Implement the variant using the appropriate mechanism:
  - If testing validation rule changes: deploy variant rules in the n8n validation workflow behind the feature flag
  - If testing enrichment strategy: route variant records to a different Clay provider order
  - If testing dedup thresholds: apply variant matching criteria to new records only
  - If testing scoring weights: compute variant scores alongside control scores, compare which correlates better with sales outcomes
- Set experiment duration: minimum 7 days or 100+ affected records per variant
- Log experiment in Attio with hypothesis, start date, duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live configuration (validation rules, enrichment order, dedup thresholds, scoring weights). Log the change. Move to Phase 5
- If Iterate: generate a new hypothesis building on this result, return to Phase 2
- If Revert: restore control configuration, log failure, return to Phase 1
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on data quality KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Data Quality Reporting

Run the `autonomous-optimization` drill to build the data substrate the optimization loop reads from:

**PostHog Dashboard (6 panels):**
1. Quality Score Trend — line chart, 12 weeks, shows overall trajectory
2. Issue Breakdown — stacked bar by issue type (missing_field, invalid_value, stale, duplicate)
3. Duplicate Rate — line chart with target line
4. Stale Record Rate — line chart with target line
5. Enrichment Effectiveness — bar chart by enrichment source, average fields filled
6. Quality Score Distribution — histogram showing the shape of quality across the database

**Attio Views:**
1. "Records Needing Attention" — quality_score < 70, open deals only, sorted ascending
2. "Compliance by Owner" — grouped by deal owner, average quality score
3. "Enrichment Candidates" — 3+ required fields empty, active contacts

**Weekly Report (automated):**
- Overall quality score and delta from last week
- Top 3 issue types
- Per-rep compliance rankings
- Records cleaned/enriched/merged this week
- Duplicate merges completed

**Sales Outcome Correlation:**
- Win rate by quality score bucket (high/medium/low)
- Deal velocity by quality score bucket
- Forecast accuracy by quality score bucket

The reporting layer provides the signal the optimization loop monitors. Without accurate reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the data quality program:

- **Rate limit:** Maximum 1 active experiment at a time on the data quality program
- **Revert threshold:** If data quality score drops below 85% during any experiment, auto-revert immediately
- **Human approval required for:**
  - Changes to required field definitions (which fields are mandatory at each stage)
  - Changes to dedup matching that could cause false-positive merges (data loss risk)
  - Relaxing validation rules (allowing previously invalid values)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All data quality events must have PostHog tracking before experiments can target them

### 4. Build Predictive Data Quality

As the optimization loop accumulates data over months, build predictive capability:

- Train on historical patterns: which records tend to degrade? (e.g., records from certain sources, certain rep behaviors, certain stages)
- Build a "decay risk" score: predict which records will drop below quality thresholds in the next 2 weeks
- Proactively enrich or flag records before they become stale
- Track `decay_prediction_accuracy`: % of records predicted to degrade that actually did
- If accuracy < 50%, the prediction model needs recalibration — the optimizer should generate a hypothesis about which signals to add or weight differently

Log prediction accuracy as a PostHog metric so the optimizer can track and improve it.

### 5. Build Adaptive Enrichment Strategy

The optimizer should continuously refine which enrichment sources provide the best data:

- Track enrichment success rate by provider (via Clay waterfall step logging)
- Track enrichment accuracy by provider (how often enriched data is later overridden by manual correction)
- When a provider's accuracy drops below 70%, the optimizer should generate a hypothesis to deprioritize it in the waterfall
- When a new provider becomes available, test it on a subset of records and compare coverage + accuracy

### 6. Monitor Convergence

The optimization loop should detect when data quality has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current data quality is near-optimal given the current CRM structure and team behavior
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Data quality program optimized. Current quality score: {X}%. Current error prevention rate: {Y}%. Further gains require structural changes (CRM schema redesign, team process changes, new enrichment data sources) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 7. Handle Structural Shifts

When external conditions change (new reps onboarded, CRM migration, new product line, rapid hiring at customers), the optimizer should detect the shift via metric anomalies and recommend a strategic review:

- If quality score drops >15% across all record types: a structural change has occurred (new data entry patterns, bulk import of low-quality records)
- If duplicate rate spikes >3x: a new data source may be pushing records without dedup checks
- If enrichment success rate drops >30%: target market segment may have shifted, or a data provider has degraded
- In these cases: alert the founder that tactical optimization is insufficient and structural review is needed. Provide the data to support the diagnosis.

## Time Estimate

- 15 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 10 hours: Data quality reporting dashboard, Attio views, and sales correlation
- 5 hours: Predictive data quality model initial calibration
- 5 hours: Adaptive enrichment strategy configuration
- 55 hours: Ongoing optimization over 6 months (~2.5 hours/week for monitoring, experiment design, evaluation)
- 10 hours: Monthly strategic reviews (human reviews optimization brief, approves high-risk changes)
- 10 hours: Convergence analysis and maintenance mode transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — record storage, quality scores, experiment logging, views | $29/user/mo (Plus) or $86/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — auto-fill fields, adaptive waterfall, deduplication | $185/mo (Launch) or $495/mo (Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Automation — optimization loop, validation, enrichment, reporting | €60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection, feature flags | Free up to 1M events/mo, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | AI — hypothesis generation, experiment evaluation, predictive models | $3/1M input + $15/1M output tokens (Claude Sonnet 4.6) — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$300-700/mo. Primary drivers: Clay ($185-495/mo), n8n Pro ($60/mo), Anthropic API (~$20-50/mo for hypothesis generation and experiment evaluation).

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in data quality metrics, generate hypotheses, run A/B experiments on validation rules, enrichment strategies, and dedup thresholds, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — comprehensive reporting on data quality trends, issue breakdown, enrichment effectiveness, per-rep compliance, and sales outcome correlation. Provides the data layer the optimization loop reads from.
