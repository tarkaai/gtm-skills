---
name: nps-health-monitor
description: Monitor NPS program health metrics with diagnostic triggers, automated interventions, and escalation rules
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
  - attio-lists
  - attio-notes
---

# NPS Health Monitor

This drill builds the NPS-specific monitoring layer for the Durable level. It complements the generic `autonomous-optimization` loop by tracking NPS-specific metrics, diagnosing NPS-specific problems, and triggering NPS-specific interventions. The output is a daily health check that keeps the NPS program running at peak performance.

## Prerequisites

- NPS program running at Scalable level for at least 4 weeks (baseline data required)
- PostHog tracking all NPS events (survey sent, submitted, response routed, loop closed)
- n8n instance for scheduled monitoring
- Attio with NPS response data synced

## Steps

### 1. Define the 8 NPS health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Overall NPS | (Promoters - Detractors) / Total * 100 | 40+ | 25-39 | <25 |
| Response rate | Responses / Surveys sent (trailing 30 days) | 40%+ | 25-39% | <25% |
| Survey coverage | % of eligible users surveyed this quarter | 50%+ | 30-49% | <30% |
| Detractor close rate | Detractors with completed follow-up / Total detractors (trailing 30 days) | 80%+ | 60-79% | <60% |
| Promoter activation rate | Promoters who took advocacy action / Total promoters (trailing 90 days) | 25%+ | 15-24% | <15% |
| NPS trend slope | Linear regression slope of weekly NPS over 12 weeks | Positive or flat | Negative, <-1 point/week | Negative, <-2 points/week |
| Theme concentration | Top detractor theme's share of all detractor responses | <40% (diverse) | 40-60% (concentrating) | >60% (single dominant issue) |
| Close-the-loop latency | Median hours from detractor response to first follow-up | <24 hours | 24-48 hours | >48 hours |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio using `attio-notes`, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `nps_health_check` event:

```json
{
  "event": "nps_health_check",
  "properties": {
    "overall_nps": 42,
    "nps_status": "healthy",
    "response_rate": 0.38,
    "response_rate_status": "warning",
    "survey_coverage": 0.55,
    "coverage_status": "healthy",
    "detractor_close_rate": 0.82,
    "close_rate_status": "healthy",
    "promoter_activation": 0.20,
    "activation_status": "warning",
    "nps_trend_slope": -0.5,
    "trend_status": "healthy",
    "theme_concentration": 0.35,
    "theme_status": "healthy",
    "close_loop_latency_hours": 18,
    "latency_status": "healthy",
    "overall_health": "warning",
    "metrics_critical": 0,
    "metrics_warning": 2,
    "metrics_healthy": 6
  }
}
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Response rate declining:**
- Check by channel: is in-app response rate dropping, email, or both?
- Check by segment: is one segment dragging down the average?
- Check survey timing: has the scheduling engine shifted toward less-responsive segments?
- If in-app dropping: verify Intercom survey is rendering correctly. Check if a product update broke the survey widget.
- If email dropping: check Loops deliverability metrics. Test if subject lines need rotation.

**Overall NPS declining:**
- Decompose: are promoters decreasing, detractors increasing, or both?
- If promoters decreasing: check if power users are experiencing new issues. Cross-reference with recent product releases.
- If detractors increasing: analyze open-text themes from the last 2 weeks. Is a new theme emerging?
- Check by segment: which segments are driving the decline?

**Detractor close rate declining:**
- Check if follow-up automation is firing correctly (n8n workflow health)
- Check if account owners are completing their assigned tasks in Attio
- If automation healthy but humans are slow: escalate to CS manager with specific accounts overdue

**Theme concentration spiking:**
- A single issue is dominating detractor feedback. Extract the top theme from open-text analysis.
- Cross-reference with: recent product changes, known outages, competitor launches, pricing changes
- Create an urgent Attio note: "NPS Alert: [X]% of detractors citing [theme]. Root cause analysis needed."
- If theme matches a known issue with a fix timeline, automatically update follow-up messaging to include the fix ETA

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Response rate below 30% for a segment**: rotate the survey copy for that segment. Switch from the current question to a variant. Use `intercom-in-app-messages` for in-app and `loops-transactional` for email.
- **Close-the-loop latency exceeding 48 hours**: send an escalation email to the account owner and their manager via Loops. Include the detractor's score, feedback, and hours elapsed.
- **Promoter activation below 15%**: increase the intensity of the promoter follow-up sequence. Add an extra nudge at day 7 via Intercom in-app message with a one-click review or referral action.
- **NPS declining 3 weeks in a row**: trigger a "deep dive" analysis. Pull all detractor open-text from the period, cluster by theme using Claude via n8n AI node, and generate a summary report. Post to Slack and store in Attio.

### 5. Build the weekly NPS health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: overall NPS movement, response rate trend, coverage progress toward quarterly target
3. Segment breakdown: NPS by segment with week-over-week change
4. Top 3 promoter quotes (for marketing and morale)
5. Top 3 detractor themes with response actions taken
6. Intervention outcomes: which automated interventions fired and what happened
7. Close-the-loop scorecard: % of detractors followed up within SLA
8. Recommendations for the `autonomous-optimization` loop: what variables to experiment on next
9. Store in Attio as a note on the NPS program record using `attio-notes`
10. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Overall NPS drops below 25 for 2+ consecutive weeks
- Response rate below 20% for any segment lasting 3+ weeks
- Detractor close rate below 50% for 2 weeks (follow-up system is broken)
- Theme concentration above 70% (a single catastrophic issue is dominating)
- 3+ automated interventions fired in one week with no improvement (tactical fixes are not working)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 NPS-specific metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 4 automated interventions for common NPS failure modes
- Weekly NPS health report with trends, themes, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
