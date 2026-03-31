---
name: holdout-groups-scalable
description: >
  Holdout Group Analysis — Scalable Automation. Expand holdout measurement to multiple
  metrics and segments, run parallel experiment streams against the treatment group,
  and use cohort analysis to identify which user segments benefit most from optimizations.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=15% cumulative lift sustained across 3+ metrics with 500+ users per group"
kpis: ["Cumulative lift % per metric", "Experiment velocity (experiments/month)", "Lift per segment", "Holdout integrity streak (consecutive passing weeks)"]
slug: "holdout-groups"
install: "npx gtm-skills add product/retain/holdout-groups"
drills:
  - holdout-lift-measurement
  - holdout-integrity-monitor
  - ab-test-orchestrator
  - cohort-retention-extraction
---

# Holdout Group Analysis — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Holdout measurement covers 3+ primary metrics simultaneously (retention, engagement, revenue). Experiment velocity reaches 4+ experiments per month against the treatment group. Lift is measured per user segment (plan type, acquisition channel, tenure) to identify where optimizations have the most impact. Cumulative lift reaches >=15% across primary metrics with 500+ users in each group, sustained over the 2-month window.

## Leading Indicators

- Multi-metric lift dashboard updating weekly with no manual intervention
- 4+ experiments shipping per month with holdout exclusion confirmed on each
- Segment-level lift analysis reveals which user populations benefit most
- Holdout integrity checks have passed for 6+ consecutive weeks
- No single experiment caused a net-negative impact on cumulative lift

## Instructions

### 1. Expand lift measurement to multiple metrics

Run the `holdout-lift-measurement` drill with an expanded metric set. Add to the existing primary metric:
- **Retention:** Week 1, Week 4, and Week 8 retention rates
- **Engagement:** Weekly active days per user, feature breadth (distinct features used)
- **Revenue:** Revenue per user, upgrade conversion rate, expansion revenue
- **Satisfaction:** NPS score (if tracked), support ticket rate

The weekly n8n workflow should compute lift for every metric and flag any metric where the holdout group is outperforming the treatment group (indicating an optimization backfired).

### 2. Add segment-level lift analysis

Using the `cohort-retention-extraction` drill, break the holdout vs treatment comparison down by user segments:
- **By plan type:** Free, Pro, Enterprise — do optimizations benefit all tiers equally?
- **By acquisition channel:** Organic, paid, referral — do users from different sources respond differently?
- **By tenure:** New users (< 30 days), mid-tenure (30-90 days), long-tenure (90+ days) — are optimizations helping retention of new users or re-engaging established users?

For each segment, compute the holdout lift independently. Store segment-level lift in Attio and add segment breakdown panels to the holdout PostHog dashboard.

### 3. Accelerate experiment velocity

Run the `ab-test-orchestrator` drill to systematize experiment execution. At Scalable level, the goal is 4+ experiments per month shipped to the treatment group:
- Maintain an experiment backlog ranked by expected impact
- Run experiments in parallel across different product surfaces (one on onboarding, one on feature discovery, one on retention messaging) — each must have its own feature flag with holdout exclusion
- Use PostHog's experiment significance calculator to right-size each test duration
- After each experiment, measure both: (a) the individual A/B test result and (b) the incremental change in cumulative holdout lift

For each experiment, verify holdout exclusion:
```
Confirm that the experiment's feature flag includes:
{"key": "$feature/global-holdout", "value": "holdout", "operator": "is_not"}
```

### 4. Run continuous integrity monitoring

The `holdout-integrity-monitor` drill continues running weekly. At Scalable level, add automated remediation:
- If contamination is detected, automatically disable the offending experiment's feature flag and send an alert
- If group size drifts, trigger a re-evaluation of the holdout flag's rollout percentage
- Track the integrity streak (consecutive weeks with all checks passing) as a KPI

### 5. Correlate experiments to cumulative lift

Build an attribution model: for each experiment shipped, measure the change in cumulative lift before and after the experiment concluded. Rank experiments by their contribution to cumulative lift.

Query pattern:
```sql
-- Lift in the 2 weeks before experiment X shipped
-- vs lift in the 2 weeks after experiment X concluded
-- Delta = experiment X's approximate contribution to cumulative lift
```

This attribution is approximate (experiments can interact), but it identifies which types of optimizations drive the most holdout lift. Use this to prioritize the experiment backlog.

### 6. Evaluate against threshold

After 2 months, assess:
- Cumulative lift >=15% on at least 3 primary metrics
- Both groups have 500+ active users
- Statistical significance p < 0.05 on all reported lift values
- Holdout integrity has been passing continuously
- Experiment velocity sustained at 4+/month

If PASS, proceed to Durable. If FAIL:
- If lift is 10-15%: accelerate experiment velocity or run higher-impact experiments. Extend by 1 month.
- If lift varies significantly by segment: focus experiments on the segments where lift is lowest.
- If a metric shows negative lift: investigate which experiments hurt that metric. Revert if necessary.

## Time Estimate

- 6 hours: expand metrics and configure segment-level analysis
- 4 hours: build experiment backlog and set up parallel experiment streams
- 24 hours: run 8+ experiments over 2 months (3 hours each)
- 6 hours: weekly review and attribution analysis (45 min/week x 8)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, dashboards, retention analysis | Free up to 1M flag requests/mo; usage-based beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automated weekly workflows, experiment orchestration | Pro: ~$60/mo for 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Lift insight generation via Claude | Sonnet 4.6: $3/$15 per MTok; ~$5-15/mo at this volume ([claude.com/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |

## Drills Referenced

- `holdout-lift-measurement` — multi-metric, segment-level lift computation with statistical significance
- `holdout-integrity-monitor` — weekly validation with automated remediation at Scalable level
- `ab-test-orchestrator` — systematic experiment execution with holdout exclusion enforcement
- `cohort-retention-extraction` — segment-level holdout vs treatment breakdown
