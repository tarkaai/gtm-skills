---
name: gamification-engagement-baseline
description: >
  Gamified Product Experience — Baseline Run. Launch gamification to 50% of users
  with reward delivery automation. Run A/B against control group for 2 weeks.
  Measure participation and retention lift.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=50% participation AND >=15pp retention lift vs control group over 2 weeks"
kpis: ["Gamification participation rate", "Streak maintenance rate (7-day survival)", "Badge earn rate per active user", "Week-over-week retention (gamified vs control)"]
slug: "gamification-engagement"
install: "npx gtm-skills add product/retain/gamification-engagement"
drills:
  - gamification-reward-delivery
  - posthog-gtm-events
  - feature-adoption-monitor
---

# Gamified Product Experience — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

>=50% of gamification-enabled users interact with gamification mechanics AND gamified users retain at >=15 percentage points higher than the control group over 2 weeks. This proves gamification is an always-on retention mechanism, not a novelty.

## Leading Indicators

- Reward notifications (badge earned, streak milestone) have >30% click-through rate in Intercom
- Streak recovery nudge emails produce >15% return rate within 48 hours
- Users who earn 3+ badges in the first week retain at 2x the rate of 0-badge users
- Gamification onboarding funnel conversion (first points -> first badge) exceeds 60%

## Instructions

### 1. Set up reward delivery automation

Run the `gamification-reward-delivery` drill to build the notification layer:

- Configure Intercom in-app celebrations for badge earned, streak milestones (3, 7, 14 days), and level ups
- Set up Loops transactional emails for weekly streak summaries, silver/gold badge earned, and streak recovery nudges
- Build the n8n orchestration workflow that routes PostHog gamification events to the appropriate delivery channel
- Implement notification fatigue rules: max 3 in-app/day, max 2 emails/week, batch multiple badges into single notification

### 2. Standardize event taxonomy

Run the `posthog-gtm-events` drill to ensure gamification events follow the standard naming convention:

- Validate all gamification event names follow `object_action` snake_case format
- Add standard properties to all events: source (gamification), channel (product), stage (retain), level (baseline)
- Create event definitions in PostHog with descriptions and tags for team discoverability
- Build the retention funnel: `session_started` weekly with cohort breakdown (gamified vs control)

### 3. Launch 50/50 split

Expand the PostHog feature flag from Smoke test:

1. Update `gamification-enabled` flag to 50% rollout
2. Ensure the split is user-level (consistent per user across sessions)
3. Verify PostHog is capturing the `$feature_flag_called` event for both variants
4. Confirm reward delivery automation is working: trigger a test badge award and verify the Intercom message and PostHog event both fire

### 4. Monitor feature adoption in gamified group

Run the `feature-adoption-monitor` drill scoped to the gamification-enabled cohort:

- Track which gamification mechanics users adopt first (points, streaks, badges)
- Build the stalled-user detection: users who earned initial points but stopped engaging after 5+ days
- Configure interventions for stalled users: Intercom in-app nudge ("You're 1 action away from your next badge")
- Monitor tier progression velocity: how quickly users move from Level 1 to Level 2

### 5. Run for 2 weeks

During the 2-week run:

- Review the gamification dashboard daily for the first 3 days, then weekly
- Monitor reward delivery: check Intercom message delivery rates and Loops email open rates
- Watch for anomalies: sudden drops in streak starts, badge earning rate falling to zero, notification failures
- Do not change gamification mechanics or thresholds during the run period

### 6. Evaluate against threshold

After 2 weeks, compute:

- **Gamification participation rate**: users with >=1 gamification event / total gamification-enabled users. Target: >=50%
- **Retention lift**: week-over-week retention rate of gamified cohort minus control cohort. Target: >=15 percentage points
- **Secondary metrics**: streak 7-day survival rate, badge earn rate per active user, reward notification CTR

If PASS: the gamification system produces reliable engagement and retention signal at scale. Proceed to Scalable.
If FAIL on participation: reward delivery may not be reaching users (check Intercom delivery), or gamification UI is not prominent enough. If FAIL on retention: gamification drives engagement but not habit change -- review whether rewarded actions actually correlate with retention.

## Time Estimate

- 4 hours: reward delivery automation setup (n8n workflow + Intercom messages + Loops emails)
- 2 hours: event taxonomy standardization and validation
- 1 hour: feature flag expansion and verification
- 3 hours: feature adoption monitoring setup
- 2 hours: daily/weekly monitoring over 2 weeks
- 4 hours: final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, funnels, cohorts | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app reward celebrations, stalled-user nudges, onboarding checklist | Essential: $29/seat/mo; Proactive Support add-on: $349/mo if >500 messages ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Streak summary emails, badge notification emails, streak recovery nudges | Free up to 1,000 contacts; $49/mo for up to 5,000 contacts, unlimited sends ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Orchestration: route gamification events to Intercom and Loops | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost at this level:** $49-80/mo (Loops paid plan + n8n cloud if not self-hosted; Intercom and PostHog within existing plans)

## Drills Referenced

- `gamification-reward-delivery` — builds notification and celebration layer via Intercom and Loops
- `posthog-gtm-events` — standardizes event taxonomy for all gamification measurement
- `feature-adoption-monitor` — tracks which gamification mechanics users adopt and detects stalled users
