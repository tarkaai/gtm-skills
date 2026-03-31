---
name: testimonial-health-monitor
description: Monitor testimonial collection pipeline health with diagnostic triggers, automated interventions, and weekly reporting
category: Advocacy
tools:
  - PostHog
  - n8n
  - Attio
  - Intercom
  - Loops
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-lists
  - attio-notes
  - intercom-in-app-messages
  - loops-transactional
---

# Testimonial Health Monitor

This drill builds the play-specific monitoring layer for testimonial collection. It complements the generic `autonomous-optimization` loop by tracking testimonial-specific metrics, diagnosing collection pipeline problems, and triggering testimonial-specific interventions. The output is a daily health check that keeps the testimonial pipeline producing.

## Prerequisites

- Testimonial request pipeline active for at least 4 weeks (baseline data required)
- PostHog tracking all testimonial events (`testimonial_requested`, `testimonial_form_opened`, `testimonial_submitted`, `testimonial_published`)
- n8n instance for scheduled monitoring
- Attio with `testimonial_status` and `testimonial_quality_score` fields populated

## Steps

### 1. Define the 6 testimonial health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Request rate | Testimonial requests sent this week / eligible candidates | 15-30% of eligible | <15% | <8% |
| Form open rate | Form opens / requests sent (trailing 4 weeks) | 40%+ | 25-39% | <25% |
| Submission rate | Submissions / form opens (trailing 4 weeks) | 50%+ | 30-49% | <30% |
| Quality rate | Submissions with quality score >= 3.5 / total submissions | 60%+ | 40-59% | <40% |
| Video willingness | Submissions where willing_to_video = yes / total submissions | 20%+ | 10-19% | <10% |
| Inventory freshness | Testimonials published in last 90 days / total published | 30%+ (rotating) | 15-29% | <15% |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 6 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `testimonial_health_check` event:

```javascript
posthog.capture('testimonial_health_check', {
  request_rate: 0.22,
  request_rate_status: 'healthy',
  form_open_rate: 0.45,
  form_open_rate_status: 'healthy',
  submission_rate: 0.28,
  submission_rate_status: 'critical',
  quality_rate: 0.65,
  quality_rate_status: 'healthy',
  video_willingness: 0.15,
  video_willingness_status: 'warning',
  inventory_freshness: 0.35,
  inventory_freshness_status: 'healthy',
  overall_health: 'critical',
  metrics_critical: 1,
  metrics_warning: 1,
  metrics_healthy: 4
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Request rate declining:**
- Check if the eligible candidate pool shrank (fewer users hitting trigger events or passing cohort criteria)
- If pool shrank: the product engagement problem is upstream -- not a testimonial pipeline issue
- If pool stable but requests low: check if the n8n trigger workflow is firing correctly and if trigger events are still being emitted

**Form open rate declining:**
- Check Intercom in-app message delivery and impression rates
- Check Loops email open rates for the fallback request
- Compare open rates by trigger type: are milestone-triggered requests outperforming NPS-triggered ones? If so, deprioritize the weaker triggers.
- Check if the request copy has gone stale (same message for 60+ days)

**Submission rate declining:**
- Check Typeform analytics: where are users dropping off in the form?
- If drop-off at the "quantified impact" question: it may be too hard. Test making it optional.
- If drop-off at "problem before": the form may feel too long. Test a shorter version.
- Check mobile vs desktop completion rates -- if mobile is significantly lower, optimize the form for mobile.

**Quality rate declining:**
- Analyze which scoring dimensions are pulling the average down
- If specificity is low: add example text to the form fields ("e.g., Reduced our deployment time from 2 weeks to 2 hours")
- If quantification is low: add a dropdown for common metrics ("Time saved", "Revenue increased", "Cost reduced") before the free-text field
- If attribution is low: add a leading prompt ("How has [Product] specifically contributed to this result?")

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Stale request copy**: if in-app message click rate drops below 10% for 2 consecutive weeks, rotate to the next message variant in Intercom
- **Form abandonment spike**: if submission rate drops below 30%, automatically switch to the shorter form variant (3 questions instead of 8)
- **Low candidate pool**: if fewer than 10 eligible candidates exist for 2 consecutive weeks, temporarily lower the criteria (account age >= 30 days instead of 60, NPS >= 7 instead of 8)
- **Video drought**: if no video-willing submissions in 30 days, add a video incentive to the form thank-you screen ("Record a 60-second video and receive [incentive]")

### 5. Build the weekly testimonial report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Pipeline summary: requests sent, forms opened, submissions received, quality breakdown
3. Inventory status: total testimonials by quality tier, by industry, by use case. Flag gaps ("No testimonials from enterprise customers" or "No testimonials mentioning [feature X]")
4. Intervention outcomes: which automated interventions fired and what happened
5. Top testimonials of the week: highest quality score submissions with quotes
6. Recommendations: what the optimization loop should focus on next
7. Store in Attio as a note on the testimonial program record
8. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 5+ consecutive days
- Submission rate below 20% for 3 weeks (form may need redesign, not iteration)
- Zero submissions in any 2-week period (pipeline is broken)
- 3+ automated interventions fired in one week with no improvement (tactical fixes are not working)
- Quality rate below 30% for 4 weeks (the wrong users are being asked, or the form structure is fundamentally flawed)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 6 metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 4 automated interventions for common failure modes
- Weekly testimonial report with pipeline status, inventory gaps, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
