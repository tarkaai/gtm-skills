---
name: ndr-cohort-tracking
description: Build always-on NDR tracking by cohort and segment with automated alerts for churn spikes, contraction surges, and expansion stalls
category: Revenue Ops
tools:
  - PostHog
  - Attio
  - n8n
  - Loops
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - posthog-retention-analysis
  - attio-custom-attributes
  - attio-lists
  - n8n-scheduling
  - n8n-workflow-basics
  - loops-transactional
---

# NDR Cohort Tracking

This drill builds always-on NDR monitoring that breaks retention down by signup cohort, plan tier, and usage segment. It detects when specific segments degrade before the aggregate number moves, enabling targeted intervention rather than blanket retention efforts.

This is the operational layer that sits on top of `ndr-baseline-measurement`. That drill computes the number; this drill watches it continuously and alerts when action is needed.

## Prerequisites

- `ndr-baseline-measurement` drill running and producing monthly NDR events in PostHog
- PostHog billing events (`subscription_created`, `subscription_cancelled`, `subscription_upgraded`, `subscription_downgraded`, `seat_added`, `seat_removed`) flowing consistently
- At least 3 months of NDR baseline data
- n8n instance for scheduled monitoring workflows

## Steps

### 1. Build the NDR dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Net Dollar Retention" with these panels:

**Panel 1 — NDR trend (line chart)**
- Monthly NDR for the last 12 months
- Overlay: GRR trend on the same chart (to separate retention from expansion effects)
- Threshold line at 100% (break-even) and at target (e.g., 115%)

**Panel 2 — NDR decomposition (stacked bar)**
- Monthly breakdown: churned MRR (red, negative), contraction MRR (orange, negative), expansion MRR (green, positive)
- Shows which component is driving NDR changes

**Panel 3 — NDR by signup cohort (heatmap)**
- Rows = signup month cohorts, columns = months since signup
- Cell value = NDR for that cohort at that age
- Highlights which cohort vintages retain best

**Panel 4 — NDR by plan tier (multi-line)**
- Separate NDR lines for each plan tier (free, starter, pro, enterprise)
- Reveals if specific plans have retention problems

**Panel 5 — Expansion funnel**
- Funnel: `feature_gate_hit` -> `upgrade_prompt_shown` -> `upgrade_started` -> `upgrade_completed`
- Shows where expansion revenue is being left on the table

**Panel 6 — Churn reasons (pie chart)**
- Distribution of `cancellation_reason` property from `subscription_cancelled` events
- Updated monthly to track whether reason distribution shifts

### 2. Build the weekly NDR monitoring workflow

Using `n8n-scheduling`, create a workflow that runs weekly (Monday 06:00 UTC):

1. Query PostHog for the trailing 4-week NDR components:
   - Churned MRR this week vs. 4-week average
   - Contraction MRR this week vs. 4-week average
   - Expansion MRR this week vs. 4-week average
   - New cancellation count vs. 4-week average
2. Detect anomalies:
   - **Churn spike:** Weekly churned MRR > 150% of 4-week average
   - **Contraction surge:** Weekly contraction MRR > 200% of 4-week average
   - **Expansion stall:** Weekly expansion MRR < 50% of 4-week average
   - **Logo churn spike:** Weekly cancellations > 200% of 4-week average
3. If any anomaly detected, proceed to step 3. If all normal, log the metrics and stop.

### 3. Diagnose anomalies

When an anomaly fires, the workflow automatically gathers context:

1. Pull the list of accounts that churned/contracted/expanded this week from PostHog
2. For each account, pull from Attio: plan tier, signup date, health score (if `health-score-model-design` is running), last support interaction
3. Using `posthog-cohorts`, check if the churned/contracted accounts cluster in a specific:
   - Signup cohort (bad onboarding for that cohort?)
   - Plan tier (pricing problem?)
   - Usage segment (feature gap?)
   - Geography (regional issue?)
4. Generate a structured anomaly report:

```
# NDR Anomaly Report — Week of [date]

## Alert Type: [Churn Spike / Contraction Surge / Expansion Stall]

## Numbers
- This week: [value]
- 4-week average: [value]
- Deviation: [+X%]

## Affected Accounts
| Account | Plan | MRR Lost | Months Active | Cancellation Reason | Health Score |
|---------|------|----------|---------------|-------------------|-------------|
| ...     | ...  | ...      | ...           | ...               | ...         |

## Pattern Analysis
- Cohort clustering: [yes/no — which cohort]
- Plan clustering: [yes/no — which plan]
- Reason clustering: [yes/no — which reason]

## Recommended Actions
- [Action 1 based on pattern]
- [Action 2 based on pattern]
```

### 4. Route alerts

Using `n8n-workflow-basics`, route the anomaly report:

- **Churn spike or logo churn spike:** Post to Slack #retention channel + create Attio task for head of customer success
- **Contraction surge:** Post to Slack #revenue channel + create Attio task for account management team
- **Expansion stall:** Post to Slack #growth channel + create Attio task for product team
- All alerts: store the report as a note in Attio on a "Net Retention" campaign record for historical tracking

### 5. Build segment-level early warning

Using `posthog-cohorts`, create dynamic cohorts that act as early warning groups:

- **New accounts (0-90 days):** Compute NDR separately for this group. Early churn indicates onboarding problems.
- **Mid-lifecycle (91-365 days):** Compute NDR separately. Churn here indicates product-market fit issues or missing features.
- **Mature (365+ days):** Compute NDR separately. Churn here indicates competitive displacement or pricing pressure.
- **High-value accounts (top 20% by MRR):** Compute NDR separately. A single enterprise churn can swing overall NDR — track these individually.

Using `attio-lists`, maintain lists for each segment and flag any account whose behavior deviates from segment norms.

### 6. Automate the monthly NDR report

Using `n8n-workflow-basics`, generate a monthly executive report:

```
# Net Dollar Retention Report — [Month Year]

## Headline
NDR: [X%] (target: [Y%]) — [up/down] [Z] points from last month

## Components
| Component | This Month | Last Month | Trend |
|-----------|-----------|------------|-------|
| Starting MRR | $X | $X | — |
| Churned MRR | -$X | -$X | [arrow] |
| Contraction MRR | -$X | -$X | [arrow] |
| Expansion MRR | +$X | +$X | [arrow] |
| Ending MRR | $X | $X | [arrow] |
| NDR | X% | X% | [arrow] |
| GRR | X% | X% | [arrow] |

## Cohort Performance
- Best performing cohort: [month] at [X%] NDR
- Worst performing cohort: [month] at [X%] NDR

## Actions Taken This Month
- [Intervention 1 and result]
- [Intervention 2 and result]

## Recommended Focus for Next Month
- [Priority 1]
- [Priority 2]
```

Send via `loops-transactional` to the leadership team and store in Attio.

## Output

- PostHog dashboard with 6 panels covering NDR trends, decomposition, cohorts, segments, expansion funnel, and churn reasons
- Weekly n8n workflow that detects NDR anomalies and generates diagnostic reports
- Segment-level early warning cohorts in PostHog
- Monthly executive NDR report delivered via email and stored in Attio
- Anomaly alert routing to the right team via Slack + Attio tasks

## Triggers

- Weekly monitoring: cron, Monday 06:00 UTC
- Monthly report: cron, 1st of each month 08:00 UTC
- Anomaly alerts: triggered by weekly monitoring workflow when thresholds are breached
