---
name: referral-funnel-monitor
description: Track referral funnel health from share to activation with segment breakdowns, drop-off diagnostics, and automated alerts
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-lists
  - attio-notes
---

# Referral Funnel Monitor

This drill builds always-on monitoring of the referral funnel: from referral link shared through referee signup, activation, and reward fulfillment. It identifies where referrals are leaking, which segments refer best, and when funnel performance changes.

## Prerequisites

- Referral program running with PostHog tracking at every funnel stage
- At least 50 referral links shared (sufficient volume for funnel analysis)
- n8n instance for scheduled monitoring

## Steps

### 1. Define the referral funnel stages

Using `posthog-funnels`, build the core referral funnel:

1. `referral_link_shared` -- referrer shares their unique link
2. `referral_link_clicked` -- someone clicks the shared link
3. `referral_signup_started` -- referee begins registration
4. `referral_signup_completed` -- referee creates account
5. `referral_activation_reached` -- referee hits the activation milestone
6. `referral_reward_issued` -- both parties receive their reward

Calculate conversion rates between each adjacent stage. The overall funnel conversion (shared to reward issued) is the referral program's core health metric.

### 2. Build segment breakdowns

Using `posthog-cohorts`, slice the funnel by:

- **Referrer tier**: Power users vs. standard users vs. new users. Which tier produces the highest conversion referrals?
- **Referral surface**: In-app prompt vs. email CTA vs. social share vs. direct link. Which surface produces referees who actually activate?
- **Referee source**: Was the referee a colleague at the same company (domain match), a social connection, or unknown? Company referrals typically convert at 2-3x the rate.
- **Time cohort**: Weekly cohorts to detect performance trends. Are newer referrals converting better or worse?

Store the top referrer list in `attio-lists` as "Top Referrers" for advocacy program recruitment.

### 3. Identify and diagnose drop-off points

For each funnel transition, set healthy benchmarks:

| Transition | Healthy Rate | Warning | Critical |
|-----------|-------------|---------|----------|
| Shared -> Clicked | 30%+ | 15-29% | <15% |
| Clicked -> Signup Started | 40%+ | 20-39% | <20% |
| Signup Started -> Completed | 70%+ | 50-69% | <50% |
| Completed -> Activated | 40%+ | 25-39% | <25% |
| Activated -> Reward Issued | 90%+ | 70-89% | <70% |

When a transition enters warning or critical:

- **Shared -> Clicked low**: The share message or channel is weak. Check which surfaces produce clicks and which do not. The referrer may be sharing to irrelevant audiences.
- **Clicked -> Signup low**: The referral landing page is not compelling, or the value proposition is unclear to cold visitors. Check landing page bounce rate.
- **Signup -> Completed low**: Registration friction is high. Check form completion rates and error rates.
- **Completed -> Activated low**: Standard onboarding is failing for referred users. Check if referred users get a different (better or worse) onboarding path.
- **Activated -> Reward low**: Reward fulfillment is broken. This is a system reliability issue. Fix immediately -- broken rewards destroy referral motivation.

### 4. Build the automated monitoring workflow

Using `n8n-scheduling`, create a daily workflow:

1. Query PostHog for 7-day rolling funnel conversion rates at each stage
2. Compare each transition against the healthy/warning/critical benchmarks
3. If all healthy: log a `referral_funnel_health_check` event to PostHog with status "healthy"
4. If any warning: log with status "warning" and include which stages are degraded
5. If any critical: log with status "critical", send Slack alert, and create an Attio note on the referral program record with diagnostic context

Using `n8n-triggers`, configure an immediate alert if:
- Overall funnel conversion (shared to reward) drops below 5% for 3 consecutive days
- Reward fulfillment rate drops below 80% (system reliability issue)
- Zero referral links shared in 48 hours (program may be broken or hidden)

### 5. Build the weekly referral report

Using `n8n-scheduling`, generate a Monday morning report:

- Total referrals this week vs. last week (volume trend)
- Funnel conversion rates by stage (efficiency trend)
- Top 5 referrers this week (recognize and reward)
- Referee activation rate vs. organic signup activation rate (quality comparison)
- Revenue attributed to referrals: new MRR from activated referees
- Referral CAC vs. other channel CAC
- Any funnel stages in warning or critical with diagnostic notes

Store the report in Attio and post to Slack.

### 6. Track referral program ROI

Using `posthog-custom-events`, compute and log weekly:

- **Referral CAC**: total reward cost / activated referees
- **Referral LTV ratio**: average LTV of referred customers / average LTV of organic customers (referred customers typically have 15-25% higher LTV)
- **Referral payback period**: months until referral reward cost is recovered from referee revenue
- **Viral coefficient**: average referrals per referrer * funnel conversion rate. If >1, the program is self-sustaining.

## Output

- 6-stage referral funnel with conversion rates between each stage
- Segment breakdowns by referrer tier, surface, referee source, and time cohort
- Diagnostic playbook for each funnel drop-off point
- Daily automated health check with Slack alerts for critical degradation
- Weekly referral report with volume, efficiency, and ROI metrics

## Triggers

Daily health check runs every morning via n8n cron. Weekly report runs Monday morning. Alert triggers fire in real-time on critical thresholds.
