---
name: champion-program-health-monitor
description: Monitor community champion program health metrics with diagnostic triggers, automated interventions, and escalation rules
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

# Champion Program Health Monitor

This drill builds the play-specific monitoring layer for the community champions recognition program. It complements the generic `autonomous-optimization` loop by tracking champion-specific metrics, diagnosing champion-specific problems, and triggering champion-specific interventions. The output is a daily health check that keeps the champion program running at peak performance.

## Prerequisites

- Champion identification scoring and recognition pipeline active for at least 4 weeks (baseline data required)
- PostHog tracking all champion events (`champion_score_computed`, `champion_enrolled`, `champion_referral_link_shared`, `champion_content_published`, etc.)
- n8n instance for scheduled monitoring
- Attio with champion tier data

## Steps

### 1. Define the 8 champion program health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Champion pool growth | New score-50+ members this week / total community members | 3-8% of active members | <3% | <1% |
| Enrollment rate | Champions enrolled this week / eligible (score>=50, not enrolled) | 15-30% | <15% | <8% |
| Referral activation rate | Champions who shared referral link within 30 days / enrolled this month | 35%+ | 20-34% | <20% |
| Referral conversion | Referred signups activated / referral links clicked | 25%+ | 12-24% | <12% |
| Co-marketing acceptance | Co-marketing invitations accepted / sent this month | 40%+ | 25-39% | <25% |
| Champion retention | Champions with community activity in last 30 days / total champions | 75%+ | 55-74% | <55% |
| Champion score stability | % of champions whose score stayed >= 50 this month | 80%+ | 65-79% | <65% |
| Content yield | Co-marketing content pieces published per quarter | 8+ | 4-7 | <4 |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `champion_program_health_check` event:

```javascript
posthog.capture('champion_program_health_check', {
  pool_growth: 0.05,
  pool_growth_status: 'healthy',
  enrollment_rate: 0.22,
  enrollment_status: 'healthy',
  referral_activation: 0.28,
  referral_activation_status: 'warning',
  referral_conversion: 0.30,
  referral_conversion_status: 'healthy',
  comarketing_acceptance: 0.35,
  comarketing_status: 'warning',
  champion_retention: 0.80,
  champion_retention_status: 'healthy',
  score_stability: 0.85,
  score_stability_status: 'healthy',
  content_yield_qtd: 6,
  content_yield_status: 'healthy',
  overall_health: 'warning',
  metrics_critical: 0,
  metrics_warning: 2,
  metrics_healthy: 6
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Champion pool growth declining:**
- Check if overall community activity is declining (upstream problem) or if scoring thresholds are too high
- If community activity declining: the product engagement or community health is the problem, not the champion program. Flag for community team.
- If community healthy but fewer users scoring high: check if scoring calibration drifted. Re-validate the top 20 against manual assessment.

**Enrollment rate declining:**
- Check enrollment message delivery and click rates in Intercom and Loops
- Compare enrollment rates by channel (Slack vs Discord vs forum) to see if one channel's pipeline dried up
- Check if declined-enrollment users are increasing (the value proposition may be stale)

**Referral activation declining:**
- Check if champions are seeing the referral link (in-app message delivery rate)
- If seeing but not sharing: the referral incentive may not be motivating. Check what other programs in the space offer.
- If sharing but not converting: the referral landing page or onboarding for referred users is broken. Check the referee funnel.

**Co-marketing acceptance declining:**
- Check if invitations are being opened (Loops email open rate)
- Check if the opportunity types offered match champion strengths (are blog post invitations going to champions with low content scores?)
- Check if champions are in cool-down (too many recent asks). Review ask frequency vs burnout guardrails.

**Champion retention declining:**
- Cross-reference with product usage: are champions churning from the product or just from the community?
- If product churn: this is a churn risk, not a champion program problem. Route to churn prevention.
- If product active but community inactive: check if the community channels are still healthy. The champion may have moved to a different community or channel.

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Stale enrollment message**: if enrollment message click rate drops below 5%, automatically rotate to the next message variant in Intercom. Pre-configure 3 variants.
- **Referral activation stall**: if a cohort's 14-day referral activation rate is below 15%, trigger an extra nudge: a personalized Loops email showing the champion's community impact stats ("You've helped 23 people this month") with the referral CTA as secondary.
- **Co-marketing drought**: if no co-marketing content published in 21 days, trigger a simplified ask to the top 5 champions: a social amplification kit (pre-written posts with referral links) that takes <5 minutes instead of a blog post or webinar.
- **Lapsed champion**: if a champion's community activity drops to 0 for 21+ days and they are still an active product user, trigger a re-engagement message: "We miss your contributions in [channel]. The community has been asking about [topic you used to help with]."

### 5. Build the weekly health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady
3. Intervention outcomes: which automated interventions fired and what happened
4. Notable events: new Champions enrolled, top referrers, co-marketing content published
5. Recommendations: what the optimization loop should focus on next
6. Store in Attio as a note on the champion program record
7. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 3+ consecutive days
- Champion retention below 55% for 2 weeks (program may need structural redesign)
- Referral conversion below 12% for 4 weeks (incentive or landing page is broken)
- 3+ automated interventions fired in one week with no improvement (tactical fixes are not working)
- Champion pool growth at 0% for 4 weeks (scoring model or community health needs strategic review)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 4 automated interventions for common failure modes
- Weekly health report with trends, interventions, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
