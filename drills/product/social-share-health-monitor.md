---
name: social-share-health-monitor
description: Monitor social sharing metrics with diagnostic triggers, automated interventions, and escalation rules specific to viral growth loops
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

# Social Share Health Monitor

This drill builds the play-specific monitoring layer for built-in social sharing. It complements the generic `autonomous-optimization` loop by tracking sharing-specific metrics, diagnosing sharing-specific problems, and triggering sharing-specific interventions. The output is a daily health check that keeps the viral sharing loop running at peak performance.

## Prerequisites

- Social sharing features deployed and active for at least 4 weeks (baseline data required)
- PostHog tracking all share events (`share_widget_opened` through `share_referral_activated`)
- Share link system with attribution tracking operational
- n8n instance for scheduled monitoring

## Steps

### 1. Define the 8 sharing health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Share surface impression rate | Users who see a share button / DAU | 60%+ | 40-59% | <40% |
| Share initiation rate | share_widget_opened / share surface impressions | 8%+ | 4-7% | <4% |
| Share completion rate | share_action_completed / share_widget_opened | 50%+ | 30-49% | <30% |
| Share link CTR | share_link_clicked / share_action_completed | 15%+ | 8-14% | <8% |
| Viral signup rate | share_referral_signup / share_link_clicked | 10%+ | 5-9% | <5% |
| Viral activation rate | share_referral_activated / share_referral_signup | 40%+ | 25-39% | <25% |
| K-factor (viral coefficient) | (shares per user * conversion per share) rolling 4-week | 0.15+ | 0.08-0.14 | <0.08 |
| Sharer retention | Sharers who share again within 30 days / total sharers | 20%+ | 10-19% | <10% |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `share_health_check` event:

```javascript
posthog.capture('share_health_check', {
  share_initiation_rate: 0.09,
  share_initiation_status: 'healthy',
  share_completion_rate: 0.45,
  share_completion_status: 'warning',
  share_link_ctr: 0.12,
  share_link_ctr_status: 'warning',
  k_factor: 0.18,
  k_factor_status: 'healthy',
  overall_health: 'warning',
  metrics_critical: 0,
  metrics_warning: 2,
  metrics_healthy: 6
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Share initiation rate declining:**
- Check if share button visibility changed (product UI update moved or hid the button)
- Compare initiation rates by resource type: is one resource type pulling down the average?
- Check if the user cohort mix shifted (new users who do not know the feature vs power users who always shared)

**Share completion rate declining:**
- Check the share popover load time (slow modal kills conversion)
- Compare completion rates by channel: is one channel broken? (e.g., Twitter API change broke the share URL format)
- Check if "Copy link" still works (clipboard API permissions can change silently)

**Share link CTR declining:**
- Check OG preview card rendering on each platform (LinkedIn and Twitter change parsers periodically)
- Compare CTR by channel: identify which social platform's CTR dropped
- Check if share text quality declined (content generator producing lower-quality copy)

**Viral signup rate declining:**
- Check the shared resource landing page: is it loading correctly? Is the signup CTA visible?
- Check if the attribution cookie is being set correctly (browser privacy changes can break this)
- Compare signup rates by referrer channel: is the traffic quality different?

**K-factor declining:**
- K-factor is a composite metric. Decompose: is it fewer shares per user or lower conversion per share?
- If fewer shares: diagnose share initiation rate
- If lower conversion: diagnose share link CTR and viral signup rate

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses:

- **OG card broken**: if share link CTR drops below 8% for a specific channel, trigger an OG image re-validation test. Fetch the OG image URL with each social platform's debugger API. If the image is not rendering, re-generate and clear the cache.
- **Share prompt fatigue**: if share completion rate drops below 30% for a cohort, reduce share prompt frequency for that cohort by 50% for 2 weeks using Intercom audience rules.
- **Stale share text**: if share link CTR for AI-generated content drops below the static template baseline, switch to a new content generation prompt variant.
- **Viral drop revival**: if K-factor drops below 0.08 for 2 weeks, trigger a Loops campaign to the top 50 sharers with a "your shared content got {X} views — share your latest work?" re-engagement nudge.

### 5. Build the weekly sharing health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady
3. Funnel analysis: where in the share funnel are users dropping off this week vs last week?
4. Channel breakdown: share volume and CTR by channel (Twitter, LinkedIn, email, copy link)
5. Top shared resources: which content got shared the most and converted the best?
6. Intervention outcomes: which automated interventions fired and what happened?
7. K-factor trend: 4-week rolling K-factor with directional indicator
8. Store in Attio as a note on the social sharing program record
9. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 3+ consecutive days
- K-factor below 0.05 for 2 weeks (viral loop may be fundamentally broken)
- Share completion rate below 20% for 1 week (UI or technical issue likely)
- 3+ automated interventions fired in one week with no improvement
- OG card rendering broken on 2+ platforms simultaneously (may need engineering fix)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 sharing metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 4 automated interventions for common sharing failure modes
- Weekly health report with funnel analysis, channel breakdown, and K-factor trend
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
