---
name: public-share-health-monitor
description: Monitor branded public sharing metrics with diagnostic triggers, automated interventions, and escalation rules specific to share-driven acquisition
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

# Public Share Health Monitor

This drill builds the play-specific monitoring layer for branded public sharing. It complements the generic `autonomous-optimization` loop by tracking share-specific metrics, diagnosing share-specific problems, and triggering share-specific interventions. The output is a daily health check that keeps the public sharing loop running at peak performance.

## Prerequisites

- Public sharing feature live for at least 4 weeks at Scalable level (baseline data required)
- PostHog tracking all share events: `share_initiated`, `share_published`, `share_page_viewed`, `share_cta_clicked`, `share_signup_completed`, `share_user_activated`
- n8n instance for scheduled monitoring
- Attio with share attribution data

## Steps

### 1. Define the 8 share health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Share initiation rate | Users who clicked "share publicly" / active users this week | 15-30% | 10-14% | <10% |
| Share completion rate | Shares published / shares initiated | 70%+ | 50-69% | <50% |
| Share page view rate | Unique viewers per published share (7-day avg) | 5+ views/share | 2-4 views/share | <2 views/share |
| CTA click-through rate | CTA clicks / share page views | 8%+ | 4-7% | <4% |
| Share-to-signup conversion | Signups from share pages / share page views | 3%+ | 1-2.9% | <1% |
| New user activation rate | Activated users / signups from shares | 40%+ | 25-39% | <25% |
| Viral coefficient | New shares created by share-acquired users / original shares | 0.3+ | 0.1-0.29 | <0.1 |
| Share content freshness | Shares updated or created in last 30 days / total published shares | 40%+ | 20-39% | <20% |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `public_share_health_check` event:

```javascript
posthog.capture('public_share_health_check', {
  share_initiation_rate: 0.22,
  share_initiation_status: 'healthy',
  share_completion_rate: 0.65,
  share_completion_status: 'warning',
  cta_clickthrough: 0.09,
  cta_clickthrough_status: 'healthy',
  share_signup_conversion: 0.035,
  share_signup_status: 'healthy',
  viral_coefficient: 0.15,
  viral_coefficient_status: 'warning',
  overall_health: 'warning',
  metrics_critical: 0,
  metrics_warning: 2,
  metrics_healthy: 6
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Share initiation rate declining:**
- Check if active user count changed (denominator shift) or if fewer users are clicking "share publicly" (numerator problem)
- If numerator problem: check Intercom share prompt delivery rates. The prompt may be stale or buried.
- Segment by user cohort: are new users sharing less (onboarding problem) or power users sharing less (fatigue)?
- Check if a product change moved or obscured the share button (PostHog session recordings for share page views without share clicks)

**Share completion rate declining:**
- Analyze the share creation funnel: where are users dropping off between initiation and publish?
- Check for technical errors: API failures, slow load times, or broken preview generation
- Check if the share customization flow is too complex: compare completion rates for users who customize vs. users who use defaults

**CTA click-through rate declining:**
- Pull share page session recordings from PostHog: are viewers seeing the CTA?
- Check CTA placement: is the branded CTA above the fold on mobile?
- Compare CTR by share content type: some content types may produce higher-intent viewers
- Check referrer distribution: traffic from different channels (social, direct, search) converts differently

**Share-to-signup conversion declining:**
- Check the signup flow from share pages: is the form working? Are there errors?
- Compare conversion by device: mobile share pages may have a broken signup flow
- Check if the value proposition on the share page CTA matches what the viewer expects after clicking

**Viral coefficient declining:**
- Check if share-acquired users are reaching the "share publicly" feature: are they completing onboarding?
- If they reach the feature but do not share: the first-share experience for new users may need improvement
- Compare time-to-first-share for share-acquired users vs. organic signups

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Share prompt fatigue**: if share initiation rate drops below 12% for 2 consecutive weeks, rotate the in-app share prompt to a new variant using `intercom-in-app-messages`. Cycle through: achievement-based ("Share your [milestone]"), social-proof-based ("Join X users sharing publicly"), and utility-based ("Let others see your work")
- **Completion stall**: if share completion rate drops below 55%, trigger a simplified share flow: skip customization options and publish with defaults, with an "edit later" option. Implement via PostHog feature flag.
- **CTA decay**: if CTA click-through rate drops below 5% for 2 weeks, A/B test a new CTA copy and placement. Queue the test via PostHog experiments.
- **Viewer re-engagement**: if a share page viewer clicked the CTA but did not complete signup, trigger a `loops-transactional` email (if email was captured via partial form) with a direct link to complete registration. Fire within 1 hour of abandonment.
- **Viral loop boost**: if viral coefficient drops below 0.15, trigger an Intercom in-app message for share-acquired users who have been active for 7+ days but have not yet shared: "You discovered [Product] through a shared [content type]. Create yours and share it too."

### 5. Build the weekly share performance report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady vs. 4-week average
3. Top shares: the 5 most-viewed and 5 highest-converting shared pages this week
4. Intervention outcomes: which automated interventions fired and their measured impact
5. Viral loop analysis: how many new users came through shares, and how many of those went on to share themselves (second-generation shares)
6. Channel breakdown: where are share page viewers coming from (social platforms, direct links, search)
7. Recommendations: what the optimization loop should focus on next
8. Store in Attio as a note on the public-sharing campaign record
9. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 3+ consecutive days
- Share-to-signup conversion below 1% for 2 weeks (the share page CTA or signup flow may need redesign)
- Viral coefficient below 0.05 for 4 weeks (the viral loop is fundamentally broken)
- Share completion rate below 40% for 2 weeks (likely a technical issue)
- 3+ automated interventions fired in one week with no improvement (tactical fixes are not working, strategic review needed)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 share-specific metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 5 automated interventions for common share funnel failure modes
- Weekly performance report with trends, top shares, viral analysis, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
