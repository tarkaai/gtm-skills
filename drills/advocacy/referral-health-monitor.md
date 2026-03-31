---
name: referral-health-monitor
description: Monitor referral program health metrics with diagnostic triggers, automated interventions, and escalation rules
category: Advocacy
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

# Referral Health Monitor

This drill builds the play-specific monitoring layer for the referral rewards program. It complements the generic `autonomous-optimization` loop by tracking referral-specific metrics, diagnosing referral-specific problems, and triggering referral-specific interventions. The output is a daily health check that keeps the referral program running at peak performance.

## Prerequisites

- Referral program running at Scalable level for at least 4 weeks (baseline data required)
- PostHog tracking all referral funnel events (link_generated through reward_issued)
- n8n instance for scheduled monitoring
- Attio with referral program data

## Steps

### 1. Define the 8 referral health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Referral rate | Users who shared a referral link / eligible users (trailing 4 weeks) | >=12% | 8-11% | <8% |
| Funnel conversion (share-to-signup) | Referral signups / referral links clicked | >=25% | 15-24% | <15% |
| Funnel conversion (signup-to-activate) | Referred users activated / referred users signed up | >=40% | 25-39% | <25% |
| Reward fulfillment rate | Rewards issued within 24h of activation / activations | >=95% | 85-94% | <85% |
| Viral coefficient | Average referrals per user * conversion rate | >=0.3 | 0.15-0.29 | <0.15 |
| Referrer retention | Referrers active 30 days after referring / total referrers | >=85% | 70-84% | <70% |
| Referee quality | Referred users retained at day 30 / referred users activated | >=50% | 35-49% | <35% |
| Reward cost efficiency | Total reward cost / total referred activated users | <=$X (set per product) | $X-1.5X | >$1.5X |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily health event:

```javascript
posthog.capture('referral_health_check', {
  referral_rate: 0.14,
  referral_rate_status: 'healthy',
  share_to_signup_conversion: 0.22,
  share_to_signup_status: 'warning',
  signup_to_activate_conversion: 0.43,
  signup_to_activate_status: 'healthy',
  reward_fulfillment_rate: 0.97,
  fulfillment_status: 'healthy',
  viral_coefficient: 0.28,
  viral_coefficient_status: 'warning',
  referrer_retention: 0.88,
  referrer_retention_status: 'healthy',
  referee_quality: 0.52,
  referee_quality_status: 'healthy',
  reward_cost_efficiency: 18.50,
  cost_efficiency_status: 'healthy',
  overall_health: 'warning',
  metrics_critical: 0,
  metrics_warning: 2,
  metrics_healthy: 6
});
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Referral rate declining:**
- Check if the eligible user pool shrank (fewer active users) or if sharing behavior dropped
- If pool shrank: upstream engagement problem. Flag for product team.
- If sharing dropped: check Intercom referral prompt delivery rates and Loops sequence open rates. The prompt may be stale or over-shown. Check if timing triggers still fire at the right moments.

**Share-to-signup conversion declining:**
- Check referral landing page load time and error rate
- Check if the referee reward is still competitive (compare to market)
- Segment by share channel: did a specific channel (email vs social vs copy) break?
- Check if referral link format changed or if UTM tracking broke

**Signup-to-activate conversion declining:**
- Check the general onboarding activation rate for all users. If both referred and organic declined, the problem is onboarding, not referral.
- If only referred users declined: check if the referee onboarding flow mentions the referral context and reward. Referred users who do not see their expected reward during onboarding drop off.
- Check time-to-activate distribution: are referred users taking longer? They may need different onboarding nudges.

**Reward fulfillment rate declining:**
- Check the n8n fulfillment workflow for errors (API failures, timeout, validation rejections)
- Check if fraud prevention rules are too aggressive (false positives blocking legitimate referrals)
- Check if the product API for applying rewards (credits, free months) is failing

**Viral coefficient declining:**
- Decompose: is it fewer referrals per user or lower conversion?
- If fewer referrals per user: advocacy fatigue. Users have referred everyone they know. Need to expand the eligible pool or find new referral surfaces.
- If lower conversion: the referee value proposition is weakening. Test a stronger referee incentive.

**Referrer retention declining:**
- Cross-reference with general product retention. If both decline, the problem is product, not referral.
- If only referrer retention declines: check if the referral experience was negative (reward not delivered, referral not tracked). Burned referrers churn faster than average.

**Referee quality declining:**
- Check where referred users are coming from. If referrers are gaming the system (referring low-quality leads for rewards), tighten activation requirements.
- Check if the referee segment profile has shifted: are referrals reaching a different audience than before?

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses to specific diagnostic results:

- **Stale referral prompt**: if Intercom referral prompt click rate drops below 3%, automatically rotate to the next message variant
- **Sharing drought**: if referral link shares drop 30%+ week over week, trigger a "limited-time bonus reward" campaign via Loops to the top 50 referrers: "Refer this week and earn double rewards"
- **Fulfillment failure**: if reward fulfillment rate drops below 90%, send an immediate Slack alert and auto-retry failed fulfillments. Send an apology + manual reward to any user who waited >48h.
- **Referee drop-off**: if signup-to-activate conversion drops below 30%, trigger an extra onboarding email to all pending referred users via `loops-transactional`: "Your friend {referrer_name} thought you'd love this. Complete setup to claim your {reward}."
- **Referrer burnout**: if a referrer's referral rate drops to 0 after previously referring 3+, send a personalized re-engagement email: "You've brought {count} friends to [product]. Here's a fresh referral link with a special offer for your next referral."

### 5. Build the weekly health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady
3. Intervention outcomes: which automated interventions fired and what happened
4. Top referrers this week and all-time leaderboard changes
5. Referral channel mix breakdown (email, social, direct link, in-app)
6. Reward cost summary: total rewards issued, average cost per acquisition via referral vs. other channels
7. Recommendations: what the autonomous optimization loop should focus on next
8. Store in Attio as a note on the referral program record
9. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 3+ consecutive days
- Viral coefficient below 0.1 for 2 weeks (program may need structural redesign of incentives)
- Reward fulfillment rate below 85% for 3 days (users are being burned; trust damage compounds)
- Referee quality below 30% for 4 weeks (program may be attracting the wrong audience or being gamed)
- Reward cost per acquisition exceeds 2x the cost from other channels (program is not cost-effective)
- 3+ automated interventions fired in one week with no improvement

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 metrics classified as healthy/warning/critical
- Diagnostic triggers for each declining metric
- 5 automated interventions for common referral failure modes
- Weekly health report with trends, interventions, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
