---
name: case-study-recruitment-health-monitor
description: Monitor the case study recruitment funnel with diagnostic triggers, automated interventions, and weekly health reports
category: Advocacy
tools:
  - PostHog
  - n8n
  - Loops
  - Intercom
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - loops-transactional
  - intercom-in-app-messages
  - attio-lists
  - attio-notes
---

# Case Study Recruitment Health Monitor

This drill builds the play-specific monitoring layer for the case study recruitment pipeline. It complements the generic `autonomous-optimization` loop by tracking recruitment-specific metrics, diagnosing recruitment-specific failure modes, and triggering recruitment-specific interventions. The output is a daily health check that keeps the recruitment pipeline producing case studies at target rate.

## Prerequisites

- Case study candidate pipeline active for at least 4 weeks (baseline data required)
- PostHog tracking all recruitment funnel events
- n8n instance for scheduled monitoring
- Attio with candidate pipeline data

## Steps

### 1. Define the 7 recruitment health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Candidate pool size | Accounts with case_study_fit_score >= 70 | 20+ | 10-19 | <10 |
| Outreach acceptance rate | Interviews scheduled / outreach sequences completed | 25%+ | 15-24% | <15% |
| Outreach response rate | Any response (yes, no, alternative) / outreach sent | 40%+ | 25-39% | <25% |
| Interview completion rate | Interviews completed / interviews scheduled | 85%+ | 70-84% | <70% |
| Case study completion rate | Published case studies / interviews completed | 75%+ | 60-74% | <60% |
| Time to publish | Median days from interview to published case study | <21 days | 21-35 days | >35 days |
| Pipeline velocity | New case studies published per month | Target rate* | 50-99% of target | <50% of target |

*Target rate is set per level: Smoke = 3 total, Baseline = 3/month, Scalable = 6/month

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 7 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `case_study_health_check` event:

```javascript
posthog.capture('case_study_health_check', {
  candidate_pool_size: 24,
  candidate_pool_status: 'healthy',
  outreach_acceptance_rate: 0.28,
  outreach_acceptance_status: 'healthy',
  outreach_response_rate: 0.42,
  outreach_response_status: 'healthy',
  interview_completion_rate: 0.88,
  interview_completion_status: 'healthy',
  case_study_completion_rate: 0.70,
  case_study_completion_status: 'warning',
  time_to_publish_days: 18,
  time_to_publish_status: 'healthy',
  pipeline_velocity: 3.2,
  pipeline_velocity_status: 'healthy',
  overall_health: 'warning',
  metrics_critical: 0,
  metrics_warning: 1,
  metrics_healthy: 6
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Candidate pool shrinking:**
- Check if the product's overall user base is declining (upstream problem, not a recruitment problem)
- Check if the scoring model is too restrictive (recently fewer users crossing score 70)
- Check if too many candidates are in the 6-month cooldown after declining
- If cooldown backlog: consider shortening cooldown to 3 months for candidates who timed out without responding (vs. explicit declines)

**Outreach acceptance rate declining:**
- Check email open rates by touch number: is the first email failing (bad subject line) or the whole sequence (bad ask)?
- Check if the booking link is working (Cal.com availability)
- Compare acceptance rates by segment: is a particular industry or company size consistently declining? The value proposition may not resonate for that segment.
- Check competitive landscape: are competitors running their own case study programs and tapping the same customers?

**Interview completion rate declining:**
- Check no-show rate: are candidates booking but not showing up? If yes, strengthen the reminder sequence.
- Check reschedule rate: are candidates rescheduling multiple times? Reduce interview length or offer async alternatives.
- Check time-of-day patterns: are certain time slots getting more no-shows?

**Case study completion rate declining:**
- Check where the bottleneck is: interview-to-draft, draft-to-approval, or approval-to-publish
- If draft bottleneck: the writing queue is backing up. Flag capacity issue.
- If approval bottleneck: customers are slow to review. Add a 7-day follow-up nudge for draft approvals.
- If publish bottleneck: internal process issue. Flag for operations.

**Time to publish increasing:**
- Identify which stage is causing delays: drafting, customer review, internal review, or publishing
- Check if the number of revision rounds is increasing (customers requesting more changes)
- Check if the content team is capacity-constrained (more interviews than they can write up)

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Stale outreach subject lines**: if outreach open rate drops below 30% for 2 consecutive weeks, flag for subject line refresh. Store the underperforming subject line and the new variant in Attio for A/B tracking.
- **No-show prevention**: when an interview is scheduled, trigger a 3-touch reminder sequence via `loops-transactional`: 24 hours before, 1 hour before, and 5 minutes before with the video call link. If the candidate reschedules twice, offer to switch to async written format.
- **Draft approval nudge**: if a customer has not responded to a draft review request within 7 days, send a `loops-transactional` follow-up: "We want to make sure we captured your story accurately. Here's the draft — takes 5 minutes to review." If no response at 14 days, send a final nudge. At 21 days, mark as stalled and escalate.
- **Pipeline stall**: if no new case study has been published in 3 weeks, trigger an alert. Check the pipeline for bottlenecks and recommend specific actions: expand the candidate pool (lower score threshold temporarily), accelerate drafting (prioritize shorter formats), or unblock approvals.

### 5. Build the weekly health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady
3. Funnel snapshot: how many candidates at each stage (scored, in outreach, interview scheduled, interview done, draft in review, published)
4. Intervention outcomes: which automated interventions fired and what happened
5. Content gap analysis: which industries or use cases have zero or one case study, ranked by deal pipeline size in those segments
6. Recommendations: where the pipeline needs attention next
7. Store in Attio as a note on the case study program record
8. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 5+ consecutive days
- Outreach acceptance rate below 10% for 3 weeks (the ask or incentive needs strategic rethinking)
- Zero case studies published in 4 weeks (systemic pipeline failure)
- 3+ automated interventions fired in one week with no improvement
- Candidate pool below 5 (not enough eligible customers — may need to revisit scoring criteria or wait for user base growth)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 7 metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 4 automated interventions for common failure modes
- Weekly health report with funnel snapshot, trends, and content gap analysis
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
