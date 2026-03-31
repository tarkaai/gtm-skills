---
name: gamification-engagement-scalable
description: >
  Gamified Product Experience — Scalable Automation. Roll out to 100% of users.
  Personalize gamification by segment. Add leaderboards. A/B test mechanics.
  Sustain >=45% participation at 500+ users.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=45% participation sustained across 500+ users for 4+ consecutive weeks"
kpis: ["Gamification participation rate at scale", "Streak 14-day survival rate", "Badge earn rate by segment", "Leaderboard engagement rate", "Retention lift vs pre-gamification baseline"]
slug: "gamification-engagement"
install: "npx gtm-skills add product/retain/gamification-engagement"
drills:
  - ab-test-orchestrator
---

# Gamified Product Experience — Scalable Automation

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

>=45% gamification participation sustained across 500+ users for 4 or more consecutive weeks. Personalized challenge paths produce roughly equal badge earn rates across user segments. Leaderboards are live and engaging at least 20% of participants weekly.

## Leading Indicators

- Segment-specific challenge completion rates between 40-60% (calibrated correctly)
- Leaderboard has 3+ new entrants to top 10 each week (accessible competition)
- A/B tests reach statistical significance within 2 weeks (sufficient traffic)
- Streak 14-day survival rate exceeds 30%
- Gamification participation does not decline more than 5% week-over-week after full rollout

## Instructions

### 1. Personalize gamification by user segment

Run the the gamification personalization workflow (see instructions below) drill to segment users and calibrate difficulty:

- Analyze 4+ weeks of gamification data to identify behavioral segments: Sprinters (high initial velocity), Steady Builders (consistent pace), Slow Explorers (cautious adopters)
- Assign each user to a segment via PostHog person property `gamification_segment`
- Create PostHog feature flags controlling gamification parameters per segment: point multipliers, badge thresholds, streak grace periods, leaderboard visibility
- Build segment-specific Intercom messages for key moments: Sprinter plateau nudge, Builder streak encouragement, Explorer low-friction prompts
- Set up weekly personalized challenges via n8n: 3 challenges per user calibrated to their segment and unused features

### 2. A/B test gamification mechanics

Run the `ab-test-orchestrator` drill to systematically test and optimize:

**Test 1: Streak grace period**
- Hypothesis: "Allowing 1 missed day per week without breaking the streak will increase 14-day streak survival from 30% to 45%, because the primary cause of streak abandonment is a single accidental miss."
- Control: strict daily streak. Variant: 1 grace day per 7-day window.
- Primary metric: streak 14-day survival rate. Secondary: daily active rate.

**Test 2: Badge visibility**
- Hypothesis: "Showing earned badges on the user's public profile will increase badge pursuit rate by 20%, because social recognition amplifies intrinsic motivation."
- Control: badges visible only to the user. Variant: badges visible on profile.
- Primary metric: badges earned per active user per week.

**Test 3: Point decay**
- Hypothesis: "10% weekly point decay for inactive users will increase weekly return rate by 10pp, because loss aversion is a stronger motivator than reward pursuit."
- Control: no decay. Variant: 10% weekly decay on weeks with no activity.
- Primary metric: weekly return rate for users who missed 1+ days.

Run each test for minimum 2 weeks or until 500+ users per variant, whichever is longer. Implement winners, document losers.

### 3. Launch leaderboards

Run the the gamification leaderboard pipeline workflow (see instructions below) drill to add competitive engagement:

- Build the n8n computation pipeline: runs every 4 hours, queries PostHog for points earned, computes rankings, writes to product API
- Start with Weekly Global leaderboard only (resets every Monday)
- Implement weekly reset workflow: archive previous week, announce winners, clear standings
- Configure rank-change notifications via Intercom: entered top 10, moved up 5+ positions, weekly champion
- Add anti-gaming protections: 200 points/day cap, 5-minute action rate limit, anomaly flagging for 3x median scores
- Build leaderboard health panel on PostHog dashboard: participants trend, view rate, score gap between rank 1 and rank 10

### 4. Roll out to 100%

After personalization and leaderboards are configured:

1. Increase the `gamification-enabled` feature flag from 50% to 100%
2. Monitor the gamification dashboard closely for 72 hours post-rollout
3. Watch for: participation rate dip (normal temporarily as new users onboard), leaderboard score inflation, notification delivery failures at higher volume
4. Adjust Intercom message rate limits if notification volume increases beyond thresholds

### 5. Monitor at scale for 4+ weeks

Track weekly:

- Participation rate across all 500+ users (target: >=45%)
- Segment distribution: ensure no single segment is over-represented
- Challenge completion rates by segment (target: 40-60% each)
- Leaderboard engagement: views per participant, new top-10 entrants
- Streak survival curves: 3-day, 7-day, 14-day, 30-day survival rates
- Overall retention lift vs pre-gamification baseline

Flag if participation drops below 45% for any single week: diagnose whether the drop is in new users (onboarding issue), a specific segment (calibration issue), or across the board (gamification fatigue).

### 6. Evaluate against threshold

After 4+ consecutive weeks at 500+ users:

- **Primary**: >=45% participation rate sustained for 4 consecutive weeks
- **Secondary**: leaderboard engaging 20%+ of participants, badge earn rates within 20% across segments, streak 14-day survival >=30%

If PASS: gamification scales without proportional effort. Personalization and leaderboards handle heterogeneous user bases. Proceed to Durable.
If FAIL: identify the bottleneck. If participation is high but retention lift is weak, the gamified actions may not correlate with real product value. If participation drops at scale, onboarding or discoverability is the issue.

## Time Estimate

- 12 hours: personalization setup (segment analysis, feature flags, challenges)
- 15 hours: A/B test design, setup, monitoring, and evaluation (3 tests)
- 10 hours: leaderboard pipeline build and configuration
- 3 hours: 100% rollout and initial monitoring
- 8 hours: 4-week monitoring and weekly reviews
- 12 hours: iteration on test results and threshold fixes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, feature flags, experiments, cohorts, dashboards | Free for <1M events/mo; ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app celebrations, segment nudges, leaderboard notifications | Essential $29/seat/mo + Proactive Support $349/mo for outbound messages ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Streak emails, badge notifications, weekly digests | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Leaderboard computation, challenge generation, personalization jobs | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost at this level:** $75-400/mo (Intercom Proactive Support is the main cost driver; Loops and n8n remain low)

## Drills Referenced

- the gamification personalization workflow (see instructions below) — segments users and calibrates gamification difficulty per segment
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on gamification mechanics
- the gamification leaderboard pipeline workflow (see instructions below) — builds, computes, and serves leaderboards with weekly resets
