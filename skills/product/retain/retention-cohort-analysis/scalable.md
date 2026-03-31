---
name: retention-cohort-analysis-scalable
description: >
  Retention Cohort Analytics — Scalable Automation. Run systematic A/B tests on retention
  interventions informed by cohort insights. Scale to 5+ cohort dimensions, automate the
  full insight-to-experiment pipeline, and maintain improving retention across 500+ users.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=5 validated experiments with net positive retention lift"
kpis: ["Retention by cohort", "Experiments completed", "Net retention lift", "Insight-to-action velocity"]
slug: "retention-cohort-analysis"
install: "npx gtm-skills add product/retain/retention-cohort-analysis"
drills:
  - cohort-retention-extraction
  - cohort-insight-generation
  - ab-test-orchestrator
  - dashboard-builder
---

# Retention Cohort Analytics — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Scale the cohort analysis from a validated Baseline to full production coverage. Expand to 5+ cohort dimensions so no retention pattern goes undetected. Automate the full pipeline from insight generation to experiment execution. Run systematic A/B tests on the highest-priority retention interventions. After 2 months, measure: have you completed 5+ validated experiments with a net positive retention lift?

Pass threshold: 5+ experiments completed with validated results AND net positive retention lift (sum of all experiment outcomes is positive).

## Leading Indicators

- Extraction pipeline covers 5+ cohort dimensions weekly without errors
- Insight generation produces 3+ high-confidence insights per week across all dimensions
- At least 1 A/B test running at all times during the 2-month period
- Insight-to-experiment latency under 7 days (insights are tested within a week of generation)
- Dashboard shows improving retention trend in at least 2 dimensions

## Instructions

### 1. Expand cohort dimensions to 5+

The Baseline pipeline analyzed 3 dimensions (signup week, acquisition channel, plan type). Expand to capture all meaningful retention patterns:

Configure the `cohort-retention-extraction` drill to run weekly across these dimensions:

1. **Signup week** — temporal patterns, product change impacts
2. **Acquisition channel** — channel quality differences
3. **Plan type** — segment-level retention
4. **Onboarding completion status** — did the user finish onboarding? (Binary: complete/incomplete)
5. **Feature breadth** — number of distinct features used in first 14 days (bucketed: 1, 2-3, 4-5, 6+)
6. **Team size** — for B2B: solo user vs. 2-5 vs. 6+ team members (if applicable)
7. **Geography** — region or timezone bucket (if your product has geo-specific patterns)

Add dimensions based on what the Baseline insights suggested. If Baseline revealed that onboarding completion was the strongest predictor of Week 4 retention, make onboarding stages a dimension (not just complete/incomplete).

### 2. Automate the insight-to-experiment pipeline

Extend the n8n workflow to chain the full pipeline:

1. `cohort-retention-extraction` runs across all dimensions (weekly cron)
2. `cohort-insight-generation` processes all extraction outputs and produces ranked insights
3. For insights with priority_score >= 8.0 AND confidence = "high": automatically create a draft experiment in PostHog using the `ab-test-orchestrator` drill
4. Log the draft experiment for human review before activation

This reduces the manual bottleneck from Baseline. The agent does not activate experiments autonomously at Scalable level — it drafts them for human approval. This is the transition step before full autonomy at Durable.

**Human action required:** Review and approve or reject each draft experiment within 48 hours. Rejections should include a reason that feeds back into the insight generation context for future runs.

### 3. Run systematic A/B tests

Using the `ab-test-orchestrator` drill, execute a testing program:

**Test 1 (weeks 1-3): Onboarding intervention for underperforming cohorts**
If Baseline revealed that certain cohorts have an activation gap (low Week 1 retention), test a targeted onboarding intervention. Hypothesis: forcing the key activation action for underperforming cohorts improves Week 2 retention by 10+ percentage points.

**Test 2 (weeks 2-4): Channel-specific re-engagement**
If acquisition channel analysis showed that paid users churn faster, test channel-aware messaging. Hypothesis: re-engagement emails that reference the user's entry point ("You signed up after reading about [feature]") outperform generic re-engagement by 5+ percentage points in Week 4 retention.

**Test 3 (weeks 4-6): Feature discovery for habit-failure cohorts**
If cohorts with narrow feature usage (1-2 features) show habit failure at Week 3-4, test feature discovery nudges. Hypothesis: in-app tooltips highlighting relevant unused features reduce Week 4 churn by 8+ percentage points for narrow-usage cohorts.

**Test 4 (weeks 5-7): Cohort-specific email cadence**
Test whether the optimal email nurture cadence differs by retention pattern. Hypothesis: cohorts with value plateau (good early retention, late decline) respond to lower-frequency, higher-value emails, while habit-failure cohorts need higher-frequency activation nudges.

**Test 5 (weeks 6-8): Plan-tier intervention targeting**
Test whether retention interventions should differ by plan tier. Hypothesis: free-tier users respond to feature-gate messages ("Upgrade to access [feature]"), while paid users respond to success stories ("Teams like yours achieved [outcome]").

For each test: use PostHog feature flags for traffic splitting, measure both primary (retention rate) and secondary (engagement depth, NPS) metrics, and run until statistical significance at 95% confidence.

### 4. Scale the health monitor

Enhance the `dashboard-builder` drill for Scalable coverage:

- Add panels for each new cohort dimension
- Add an experiment tracking panel: active experiments, completed experiments, cumulative lift
- Configure the weekly health brief to include experiment status and cumulative impact
- Lower the degradation alert threshold from 15% to 10% — at Scalable level, you have more data and can detect smaller changes

### 5. Build the retention lift ledger

Track every validated experiment outcome in a cumulative ledger. For each completed experiment:

```json
{
  "experiment_id": "EXP-2026-004",
  "insight_id": "RCA-2026-W15-002",
  "hypothesis": "Feature discovery tooltips for narrow-usage cohorts",
  "dimension": "feature_breadth",
  "cohort_target": "1-2 features",
  "metric": "week_4_retention",
  "control_rate": 0.18,
  "treatment_rate": 0.24,
  "lift_pp": 6.0,
  "confidence": 0.97,
  "decision": "adopt",
  "users_impacted": 340
}
```

The cumulative ledger answers: "What is the total retention improvement attributable to the cohort analysis play?" This justifies the investment and demonstrates readiness for Durable.

### 6. Evaluate at 2 months

After 8 weeks:

- Count completed experiments: must be 5+
- Calculate net retention lift: sum of lift_pp for all adopted experiments (must be net positive)
- Per-dimension retention trend: is each dimension stable or improving?
- Insight-to-action velocity: median days from insight generation to experiment launch

If PASS (5+ experiments, net positive lift), proceed to Durable. If FAIL:
- If <5 experiments: the bottleneck is execution speed — simplify experiment setup or run lighter-weight tests
- If net negative lift: the insights are not translating to effective interventions — review the hypothesis generation prompts and the intervention templates

## Time Estimate

- 8 hours: expand extraction to 5+ dimensions, configure n8n workflows
- 10 hours: set up the automated insight-to-experiment pipeline
- 20 hours: run and monitor 5+ A/B tests (setup, monitoring, analysis)
- 8 hours: scale the health monitor and build the retention lift ledger
- 10 hours: weekly reviews, calibration, experiment approvals over 2 months
- 4 hours: final evaluation, documentation, Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Multi-dimension retention queries, experiments, feature flags, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude) | Weekly insight generation across 5+ dimensions, hypothesis refinement | ~$20-50/mo at scale — [anthropic.com/pricing](https://anthropic.com/pricing) |
| n8n | Full pipeline orchestration (extraction -> insights -> experiment drafting) | Self-hosted free; cloud from EUR20/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | In-app messages, product tours for retention interventions | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email sequences for re-engagement and nurture experiments | Free up to 1,000 contacts; $49/mo paid — [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost: $50-130/mo** (Anthropic API at scale + Loops if over free tier + Intercom if not already in stack)

## Drills Referenced

- `cohort-retention-extraction` — weekly extraction across 5+ cohort dimensions
- `cohort-insight-generation` — cross-dimensional insight generation feeding the experiment pipeline
- `ab-test-orchestrator` — systematic A/B testing of retention interventions
- `dashboard-builder` — scaled monitoring with experiment tracking and cumulative lift ledger
