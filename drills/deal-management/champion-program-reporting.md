---
name: champion-program-reporting
description: Generate comprehensive reporting on champion program effectiveness including win rate correlation, recruitment efficiency, and program ROI
category: Deal Management
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - attio-reporting
  - attio-deals
  - n8n-scheduling
---

# Champion Program Reporting

This drill builds the reporting layer that quantifies the impact of the champion identification program. It answers: "Are deals with champions actually closing faster and at higher rates?" and provides the data needed for the `autonomous-optimization` drill to optimize the program.

## Input

- Attio deal data with champion tracking attributes populated
- PostHog events from champion health monitoring
- At least 4 weeks of program data (minimum viable for statistical comparison)

## Steps

### 1. Build Champion Impact Dashboard in PostHog

Using `posthog-dashboards`, create a "Champion Program Impact" dashboard with these panels:

**Panel 1 — Win Rate Comparison (Bar Chart):**
Query: Compare closed-won rate for deals WHERE `champion_count` >= 1 vs deals WHERE `champion_count` = 0. Group by month.

```
Event: deal_closed
Breakdown: champion_win_correlation (true/false)
Metric: count where deal_result = "won" / total count
```

**Panel 2 — Deal Velocity Comparison (Line Chart):**
Query: Average days from Connected → Closed for deals with vs without active champions. Plot weekly.

```
Event: deal_stage_changed
Metric: avg(days_in_pipeline)
Breakdown: has_active_champion (true/false)
```

**Panel 3 — Champion Recruitment Funnel (Funnel):**
Using `posthog-funnels`, create a funnel:
1. `champion_status_changed` to "Candidate" (candidates identified)
2. `champion_email_sent` (recruitment initiated)
3. `champion_email_replied` (engagement)
4. `champion_status_changed` to "Recruited" (recruited)
5. `champion_status_changed` to "Active" (activated)

**Panel 4 — Champion Health Distribution (Pie Chart):**
Query: Current distribution of champion health across active deals.

```
Event: champion_score_updated (latest per champion)
Breakdown: health (strong/healthy/at_risk/disengaged)
```

**Panel 5 — Champion Enablement Effectiveness (Table):**
Query: For each enablement asset type, show:
- Delivery count
- Open rate
- Forward rate (champions sharing internally)
- Correlation with deal progression

**Panel 6 — Multi-Threading Impact (Scatter Plot):**
Query: Plot stakeholder count (x-axis) vs deal close rate (y-axis). Show the correlation between multi-threading depth and win probability.

### 2. Build Attio Pipeline Reports

Using `attio-reporting`, create saved views:

**Deals at Risk (No Champion):**
```
Filter: stage IN ("Connected", "Qualified", "Proposed") AND champion_count = 0
Sort: deal_value DESC
```

**Champion-Powered Deals:**
```
Filter: champion_count >= 1 AND champion_health IN ("Strong", "Healthy")
Sort: stage DESC, deal_value DESC
```

**Champion Recruitment Pipeline:**
```
Object: People
Filter: champion_status IN ("Candidate", "Recruited")
Sort: champion_score DESC
```

### 3. Calculate Program ROI

Build an n8n workflow using `n8n-scheduling` that runs monthly:

**Step 1:** Pull closed deals from Attio for the month, split by champion_win_correlation.

**Step 2:** Calculate:
- Win rate WITH champions: `won_with_champion / total_with_champion`
- Win rate WITHOUT champions: `won_without_champion / total_without_champion`
- Win rate lift: `(rate_with - rate_without) / rate_without * 100`
- Average deal velocity WITH champions (days to close)
- Average deal velocity WITHOUT champions
- Velocity improvement: `(velocity_without - velocity_with) / velocity_without * 100`

**Step 3:** Calculate program cost:
- Clay enrichment credits used for champion profiling
- Instantly sends for champion recruitment
- Loom recordings created
- Total agent compute time (n8n executions)
- Sum of tool costs attributable to champion program

**Step 4:** Calculate ROI:
- Additional revenue attributable to champion lift: `(win_rate_lift * total_pipeline_value) / 100`
- ROI: `(additional_revenue - program_cost) / program_cost * 100`

**Step 5:** Generate monthly report and store in Attio as a note. Post summary to Slack.

### 4. Weekly Optimization Data Export

Every Sunday, export the key metrics that the `autonomous-optimization` drill needs:

```json
{
  "period": "YYYY-MM-DD to YYYY-MM-DD",
  "metrics": {
    "win_rate_with_champion": 0.XX,
    "win_rate_without_champion": 0.XX,
    "win_rate_lift": XX%,
    "avg_velocity_with_champion_days": N,
    "avg_velocity_without_champion_days": N,
    "champion_recruitment_rate": 0.XX,
    "champion_activation_rate": 0.XX,
    "champion_disengagement_rate": 0.XX,
    "avg_stakeholders_per_deal_with_champion": N,
    "avg_stakeholders_per_deal_without_champion": N,
    "enablement_forward_rate": 0.XX,
    "program_cost_monthly": $N
  }
}
```

This data feeds directly into the autonomous optimization loop for hypothesis generation and experiment evaluation.

## Output

- PostHog dashboard: "Champion Program Impact" with 6 panels
- Attio saved views: deals at risk, champion-powered, recruitment pipeline
- Monthly ROI calculation with Slack notification
- Weekly metrics export for autonomous optimization

## Triggers

- Dashboard: always available, refreshes automatically
- Monthly ROI report: n8n cron, 1st of each month at 7:00 AM
- Weekly metrics export: n8n cron, Sunday at 11:00 PM
