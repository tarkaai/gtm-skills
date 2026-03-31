---
name: certification-health-monitor
description: Continuously monitor certification program health metrics, detect degradation, and trigger alerts for the autonomous optimization loop
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
  - attio-lists
---

# Certification Health Monitor

This drill provides the monitoring layer that feeds into the `autonomous-optimization` drill at the Durable level. It continuously tracks certification program health across all dimensions — enrollment, completion, retention impact, and content quality — and surfaces anomalies for the optimization loop to act on.

## Input

- Certification program running at Scalable level for at least 4 weeks (baseline data required)
- PostHog tracking all certification events from `certification-delivery-automation`
- n8n instance for scheduled monitoring
- Attio configured with certification contact properties

## Steps

### 1. Define health metrics and baselines

Establish rolling 4-week averages for each certification health metric:

| Metric | Calculation | Healthy Range |
|--------|------------|---------------|
| Enrollment rate | cert_program_enrolled / cert_program_viewed | >15% |
| Tier 1 completion rate | cert_tier_completed (tier=foundations) / cert_tier_started (tier=foundations) | >60% |
| Tier 2+ transition rate | cert_tier_started (tier=practitioner) / cert_badge_earned (tier=foundations) | >40% |
| Median time to Tier 1 completion | Median days from cert_tier_started to cert_tier_completed | <14 days |
| Module first-attempt pass rate | cert_assessment_completed (passed=true, attempts=1) / cert_assessment_completed (total) | >65% |
| Stall rate | Users with cert_tier_started but no activity in 14+ days / total active cert users | <25% |
| Certified retention lift | 30-day retention of certified users / 30-day retention of non-certified users | >1.2x |
| Badge-to-advocate rate | Users who shared or referred after badge / total badge earners | >10% |

Using `posthog-custom-events`, ensure all these metrics can be computed from existing events. If any metric cannot be calculated, add the missing events first.

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for each health metric using the last 14 days of data
2. Compare each metric to the 4-week rolling baseline using `posthog-anomaly-detection`
3. Classify each metric:
   - **Healthy:** Within ±10% of baseline
   - **Warning:** Declined 10-20% from baseline
   - **Critical:** Declined >20% from baseline
   - **Improving:** Increased >10% from baseline
4. For each Warning or Critical metric, capture context:
   - Which persona segments are affected
   - Which cohorts show the degradation
   - Which specific modules or tiers are impacted
5. Log the health check results in Attio using `attio-notes` on the certification campaign record
6. If any metric is Critical, trigger an alert (Slack or email) with the specific metric, current value, baseline value, and affected segments

### 3. Build the weekly health digest

Using `n8n-scheduling`, create a weekly cron workflow (runs Sunday evening):

1. Aggregate daily health checks from the past 7 days
2. Compute week-over-week trends for all metrics
3. Generate a structured health digest:

```
CERTIFICATION HEALTH — Week of {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENROLLMENT: {value} ({trend}% vs last week) — {status}
COMPLETION: {value} ({trend}% vs last week) — {status}
TRANSITION: {value} ({trend}% vs last week) — {status}
RETENTION LIFT: {value}x ({trend}% vs last week) — {status}

TOP ISSUE: {metric with worst trend}
  → Affected segment: {persona/cohort}
  → Suggested investigation: {specific area to diagnose}

EXPERIMENTS RUNNING: {count}
  → {experiment_name}: Day {N} of {total}, current delta: {value}

CERTIFICATIONS ISSUED THIS WEEK: {count} (target: {target})
```

4. Store the digest in Attio and post to Slack
5. If the digest shows 2+ weeks of declining metrics in the same area, flag it as a candidate for the `autonomous-optimization` loop

### 4. Build retention impact tracking

Using `posthog-cohorts`, maintain two standing cohorts:

- **Certified cohort:** All users with `cert_badge_earned` event (any tier)
- **Non-certified matched cohort:** Users with similar signup date, plan, and usage patterns who have NOT earned a badge

Using `posthog-dashboards`, track the retention curves for both cohorts side by side. The gap between the two curves is the "certification retention lift" — the primary business justification for the program.

If the lift drops below 1.1x for 4 consecutive weeks, flag the certification program for strategic review: the program may not be teaching the right skills, or it may be attracting already-engaged users (selection bias, not causation).

### 5. Build content quality monitoring

Using `n8n-scheduling`, create a weekly workflow:

1. Query PostHog for per-module metrics:
   - First-attempt pass rate
   - Average attempts per module
   - Time-to-complete distribution
   - Drop-off rate (started module but never completed assessment)
2. Flag anomalies:
   - Pass rate dropped >15% from 4-week average for a specific module
   - A single module accounts for >40% of all stalls
   - Time-to-complete doubled for a module (possible confusion or product change broke the assessment)
3. Store module health data in Attio
4. Feed flagged modules to the optimization loop as experiment candidates

### 6. Build the advocate tracking layer

Certified users should become advocates. Track:

Using `posthog-custom-events`:
- `cert_badge_shared` — User clicked "Share on LinkedIn" or similar after badge
- `cert_referral_sent` — Certified user invited another user
- `cert_referral_converted` — Referred user signed up

Using `attio-lists`, maintain a "Certified Advocates" list: certified users who have shared or referred. This list feeds into the `referral-program` and `nps-feedback-loop` drills as a high-value segment.

## Output

- Daily health check workflow in n8n monitoring 8 certification metrics
- Weekly health digest with trend analysis and experiment status
- Certified vs non-certified retention comparison in PostHog
- Per-module content quality monitoring
- Advocate tracking events and Attio list
- Alert system for Critical metric degradation

## Triggers

Daily health check runs every day at 6 AM via n8n cron. Weekly digest runs Sunday evening. Content quality check runs weekly. All monitoring feeds into the `autonomous-optimization` drill at Durable level.
