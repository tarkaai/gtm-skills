---
name: retention-cohort-analysis-baseline
description: >
  Retention Cohort Analytics — Baseline Run. Automate weekly cohort retention extraction and insight
  generation across multiple dimensions. First always-on pipeline targeting 3+ actioned insights
  over 2 weeks with measurable retention impact.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=3 insights actioned with measurable retention impact"
kpis: ["Retention by cohort", "Insights actioned", "Intervention-to-retention lift"]
slug: "retention-cohort-analysis"
install: "npx gtm-skills add product/retain/retention-cohort-analysis"
drills:
  - cohort-retention-extraction
  - cohort-insight-generation
  - posthog-gtm-events
---

# Retention Cohort Analytics — Baseline Run

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Turn the Smoke Test's manual cohort analysis into an always-on weekly pipeline. The agent extracts retention data across multiple cohort dimensions (signup week, acquisition channel, plan type), generates and ranks insights, and tracks whether insights get actioned. After 2 weeks, measure: does the pipeline produce 3+ actioned insights and can you detect retention impact from the interventions?

Pass threshold: 3+ insights actioned (moved from generated to executed) with at least 1 showing measurable retention impact (any positive delta between treatment and control).

## Leading Indicators

- Weekly extraction pipeline runs without errors for 2 consecutive weeks
- Insights generated per week trends to 2+ (the pipeline finds new patterns each run)
- At least 50% of generated insights get actioned within 7 days (the team is closing the loop)
- PostHog tracking events for the pipeline are flowing (`cohort_retention_extracted`, `cohort_insight_generated`, `cohort_insight_actioned`)

## Instructions

### 1. Instrument the cohort analysis pipeline events

Run the `posthog-gtm-events` drill to add tracking events specific to the retention cohort pipeline:

- `cohort_retention_extracted` — fired weekly when the extraction completes. Properties: `cohort_dimension`, `total_cohorts`, `divergent_count`, `extraction_date`
- `cohort_insight_generated` — fired for each insight produced. Properties: `insight_id`, `pattern`, `confidence`, `priority_score`, `cohort_label`
- `cohort_insight_actioned` — fired when an insight leads to an intervention. Properties: `insight_id`, `action_type` (feature_flag, intercom_message, loops_sequence, product_change)
- `cohort_insight_validated` — fired 14+ days after an insight was actioned, with the measured impact. Properties: `insight_id`, `retention_lift_pp`, `treatment_size`, `control_size`

These events enable tracking the full insight pipeline: generated -> actioned -> validated.

### 2. Automate weekly cohort extraction

Configure an n8n workflow that runs the `cohort-retention-extraction` drill weekly:

**Run 1 — Signup week dimension:**
Extract cohort survival data grouped by signup week. This catches temporal patterns (did a product change in a specific week improve or hurt retention?).

**Run 2 — Acquisition channel dimension:**
Extract cohort survival data grouped by acquisition channel (utm_source, referrer, or custom channel property). This catches channel quality patterns.

**Run 3 — Plan type dimension:**
Extract cohort survival data grouped by plan/pricing tier. This catches segment-level retention differences.

The three extractions run sequentially in one n8n workflow. Each produces a separate structured JSON output.

**Human action required:** After the first automated extraction, review the 3 outputs. Confirm the data looks correct across all dimensions. If a dimension has too few cohorts (fewer than 3 groups), replace it with a more useful dimension (company size, geography, onboarding completion status).

### 3. Automate weekly insight generation

Chain the `cohort-insight-generation` drill to run after extraction completes. The drill:

1. Takes all 3 dimension outputs as input
2. Cross-references patterns: does a cohort that underperforms on the signup-week dimension also underperform on the channel dimension? (Convergent evidence = higher confidence)
3. Generates ranked insights with intervention recommendations
4. Logs insights to Attio and PostHog

### 4. Set up the retention health monitor

Run the `cohort-retention-health-monitor` drill to build:

- A 7-panel PostHog dashboard covering overall retention trends, per-dimension comparisons, new cohort quality, and the insight-to-action pipeline
- Alerting for retention degradation (5%+ decline for 3 weeks) and alarm conditions (15%+ decline for 2 weeks)
- Weekly health briefs logged to Attio

This gives the team continuous visibility into retention health beyond the insights themselves.

### 5. Action insights and measure impact

For each generated insight with priority_score >= 7.0:

1. Create the recommended intervention: set up a PostHog feature flag, configure an Intercom message, modify a Loops sequence, or deploy a product change
2. Log the action as `cohort_insight_actioned` in PostHog
3. Set up a 50/50 A/B split where possible (treatment receives the intervention, control does not)
4. After 14 days, measure the retention delta between treatment and control for the targeted cohort
5. Log the result as `cohort_insight_validated` in PostHog and update the Attio note status

### 6. Evaluate at 2 weeks

After 2 weekly pipeline runs:

- Count actioned insights: how many insights moved from generated to actioned?
- Count validated insights: how many actioned insights have measured retention impact?
- Check the pass threshold: 3+ insights actioned AND 1+ showing measurable positive retention impact

If PASS, proceed to Scalable. If FAIL:
- If <3 actioned: the bottleneck is execution speed — prioritize the top-ranked insight and implement it immediately
- If 0 validated: interventions may need more time — extend the Baseline period by 2 weeks before concluding

## Time Estimate

- 3 hours: instrument pipeline events in PostHog
- 4 hours: configure n8n workflows for weekly extraction and insight generation
- 4 hours: set up the retention health monitor (dashboard, alerts, health briefs)
- 3 hours: action top insights (feature flags, messages, sequences)
- 2 hours: analyze 2-week results, validate impact, document

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Retention queries, cohorts, dashboards, feature flags, A/B splits | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude) | Weekly insight generation across 3 dimensions | ~$5-15/mo for weekly runs — [anthropic.com/pricing](https://anthropic.com/pricing) |
| n8n | Weekly automation orchestration | Self-hosted free; cloud from EUR20/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | Insight logging, health briefs, action tracking | Free for small teams; Pro $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost: $5-30/mo** (Anthropic API + n8n cloud if not self-hosted)

## Drills Referenced

- `cohort-retention-extraction` — automated weekly extraction across 3 cohort dimensions
- `cohort-insight-generation` — cross-dimensional insight generation with convergent evidence scoring
- `posthog-gtm-events` — instruments the cohort analysis pipeline events for tracking
