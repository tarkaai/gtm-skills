---
name: advocacy-health-monitor
description: Monitor advocacy program health metrics with diagnostic triggers, automated interventions, and escalation rules
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

# Advocacy Health Monitor

This drill builds the play-specific monitoring layer for the power user program. It complements the generic `autonomous-optimization` loop by tracking advocacy-specific metrics, diagnosing advocacy-specific problems, and triggering advocacy-specific interventions. The output is a daily health check that keeps the advocacy program running at peak performance.

## Prerequisites

- Power user scoring and advocacy pipeline active for at least 4 weeks (baseline data required)
- PostHog tracking all advocacy events
- n8n instance for scheduled monitoring
- Attio with advocacy tier data

## Steps

### 1. Define the 8 advocacy health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Recruitment rate | New Insiders enrolled this week / eligible users | 10-25% of eligible | <10% | <5% |
| Activation rate | First action within 30 days / enrolled this month | 40%+ | 25-39% | <25% |
| Insider-to-Advocate conversion | Advocates promoted / Insiders enrolled 90+ days ago | 20%+ | 10-19% | <10% |
| Referral yield | Referrals per active advocate per quarter | 2+ | 1-1.9 | <1 |
| Referral conversion | Referred signups activated / referrals submitted | 30%+ | 15-29% | <15% |
| Advocate retention | Advocates with action in last 90 days / total advocates | 70%+ | 50-69% | <50% |
| Power user score stability | % of advocates whose score stayed >= 60 this month | 85%+ | 70-84% | <70% |
| Testimonial/content yield | Testimonials + case studies produced per quarter | 5+ | 2-4 | <2 |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `advocacy_health_check` event:

```javascript
posthog.capture('advocacy_health_check', {
  recruitment_rate: 0.18,
  recruitment_status: 'healthy',
  activation_rate: 0.35,
  activation_status: 'warning',
  advocate_conversion: 0.22,
  advocate_conversion_status: 'healthy',
  referral_yield: 1.4,
  referral_yield_status: 'warning',
  overall_health: 'warning',
  metrics_critical: 0,
  metrics_warning: 2,
  metrics_healthy: 6
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Recruitment rate declining:**
- Check if the eligible pool shrank (fewer users crossing score 60) or if enrollment is failing
- If pool shrank: the product engagement problem is upstream. Flag for product team.
- If enrollment failing: check Intercom enrollment message delivery rates and Loops sequence open rates. The invitation mechanic may be broken or stale.

**Activation rate declining:**
- Check the nudge sequence performance: are nudge emails being opened? Are in-app messages being seen?
- Compare activation rates by enrollment cohort: is it a recent-enrollee problem or across the board?
- Check if the "easiest ask" is still easy: are users finding the testimonial form or referral link?

**Referral yield declining:**
- Check if advocates are sharing referral links at all (link-share events in PostHog)
- If sharing but no conversions: the referred users are not signing up. Check the referral landing page or the incentive.
- If not sharing: the referral ask may be too buried or the reward is not motivating. Check last referral prompt open rates.

**Advocate retention declining:**
- Cross-reference with product usage: are advocates churning from the product or just from the program?
- If product churn: route to churn prevention. The advocacy problem is a symptom.
- If program churn only: check if benefits are still valuable. Survey lapsed advocates.

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Stale enrollment message**: if enrollment message click rate drops below 5%, automatically rotate to the next message variant in Intercom
- **Activation stall**: if a cohort's 14-day activation rate is below 20%, trigger an extra nudge: a personalized Loops email with the user's top feature and a one-click testimonial template
- **Referral drought**: if no referrals submitted in 14 days across all advocates, trigger an Intercom in-app message to top 10 advocates with a "refer and earn" reminder
- **Lapsed advocate**: if an advocate's last action is 90+ days ago and they are still actively using the product, trigger a re-engagement email with a new, fresh ask

### 5. Build the weekly health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady
3. Intervention outcomes: which automated interventions fired and what happened
4. Notable events: new Ambassadors, top referrers, milestone testimonials
5. Recommendations: what the optimization loop should focus on next
6. Store in Attio as a note on the advocacy program record
7. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 3+ consecutive days
- Advocate retention below 50% for 2 weeks (program may need structural redesign)
- Referral conversion below 10% for 4 weeks (incentive or landing page is broken)
- 3+ automated interventions fired in one week with no improvement (tactical fixes are not working)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 4 automated interventions for common failure modes
- Weekly health report with trends, interventions, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
