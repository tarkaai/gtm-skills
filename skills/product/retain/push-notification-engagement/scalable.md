---
name: push-notification-engagement-scalable
description: >
  Push Notification Strategy — Scalable Automation. Scale push notifications to
  500+ subscribers with A/B testing, send-time optimization, feature-usage
  segments, and churn prevention integration.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥30% CTR sustained across 500+ subscribers with automated optimization"
kpis: ["Push CTR", "Opt-in rate", "DAU lift", "Segment metrics"]
slug: "push-notification-engagement"
install: "npx gtm-skills add product/retain/push-notification-engagement"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - dashboard-builder
---

# Push Notification Strategy — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
Push notification program reaches 500+ active subscribers across multiple segments. CTR remains at or above 30% even as subscriber volume increases — this is harder at scale because the long tail of less-engaged users dilutes CTR. Automated A/B testing identifies winning copy, timing, and deep links. Push is integrated with the churn prevention system as an intervention channel.

## Leading Indicators
- Subscriber count growing at >10% month-over-month
- A/B tests completing with statistical significance (200+ per variant)
- Send-time optimization producing >2pp CTR improvement vs fixed-time sends
- Churn prevention pushes achieving >20% save rate (at-risk users who re-engage)
- No single campaign has opt-out rate >1.5%/week
- Feature discovery pushes drive measurable adoption (>15% of recipients try the feature)

## Instructions

### 1. Scale segmentation to feature-level targeting
Run the the push notification segmentation workflow (see instructions below) drill at scale. Beyond the 4 engagement segments from Baseline, add:

**Feature-usage segments**: For each of your top 5 product features, create:
- "Uses X actively" (used in last 14 days)
- "Never tried X" (active user, never fired the event)
- "Stopped using X" (used before, not in last 14 days)

**Enrichment-enhanced segments**: Add company size, plan tier, and industry from Clay enrichment. A solo user on the free plan needs different push content than a 20-person team on the enterprise plan.

Update the n8n sync to handle 15-20 segments updating every 4 hours without hitting OneSignal API rate limits. Batch tag updates: group users and send in batches of 100.

### 2. Launch systematic A/B testing
Run the `ab-test-orchestrator` drill adapted for push notifications:

**Test queue** (run one test at a time, each for 7+ days with 200+ per variant):

1. **Copy length**: Short (< 10 words body) vs descriptive (15-25 words). Measure CTR.
2. **Personalization depth**: Generic copy vs copy including user's name + most-used feature. Measure CTR.
3. **Urgency framing**: Neutral ("Your report is ready") vs time-pressure ("Your report expires in 24 hours"). Measure CTR and downstream action rate.
4. **Send time**: Morning (9 AM local) vs user's peak-activity hour (derived from PostHog). Measure CTR.
5. **Deep link destination**: Feature home vs specific content item. Measure session depth after click.
6. **Emoji**: No emoji vs relevant emoji in title. Measure CTR.

For each test, implement the variants using `onesignal-ab-test` fundamental (manual variant via API for full control). Track both variants in PostHog with the `experiment_id` and `variant` properties.

After each test completes: adopt the winner across all campaigns. Document the result. Move to the next test.

### 3. Implement send-time optimization
Build per-user send-time optimization:

1. Query PostHog for each subscriber's session history: which hours and days do they typically open the app?
2. Calculate their peak-activity window (the 2-hour block with the highest session probability)
3. Store this as a OneSignal tag: `peak_hour_local` = "14" (2 PM)
4. Configure n8n to send scheduled pushes within each user's peak window instead of a fixed time
5. Measure CTR improvement of personalized send time vs the previous fixed-time approach

Re-calculate peak windows monthly — user habits shift seasonally.

### 4. Integrate push with churn prevention
Run the `churn-prevention` drill and add push as an intervention channel:

1. When the churn prevention system identifies an at-risk user (churn risk score 40-70), send a targeted push before the email intervention. Push is faster and higher-visibility than email.
2. Push copy for churn intervention should focus on specific value the user is losing: "Your team posted 3 updates while you were away" (social proof), "Your saved report from March 15 is still here" (sunk cost), "We added [feature they requested]" (responsiveness).
3. Track the save rate: what percentage of at-risk users who receive a push re-engage within 48 hours?
4. Compare push save rate vs email save rate for the same churn risk tier.

### 5. Deploy health monitoring
Run the `dashboard-builder` drill. At Scalable, the monitoring system should:

- Track all metrics from the drill's dashboard spec
- Alert on anomalies daily
- Auto-pause campaigns that exceed opt-out thresholds
- Generate weekly health digests
- Track the push lift metric (retention for subscribers vs non-subscribers)

### 6. Measure against threshold
After 2 months, evaluate:
- **Overall CTR**: ≥30% across 500+ subscribers (note: maintaining 30% at 500+ is harder than 35% at 200)
- **Per-segment CTR**: Every segment above 20%; at least 2 segments above 35%
- **DAU lift**: Sustained 15pp+ lift on push-send days
- **A/B test velocity**: At least 4 tests completed with actionable results
- **Churn save rate**: >20% of at-risk users re-engaged via push

## Time Estimate
- 10 hours: Scale segmentation (feature-level, enrichment, sync optimization)
- 15 hours: Design and run 6 A/B tests over 2 months (setup + analysis per test)
- 10 hours: Build send-time optimization (PostHog analysis, n8n workflow, OneSignal config)
- 10 hours: Integrate push with churn prevention system
- 10 hours: Deploy health monitoring dashboard and alerting
- 5 hours: Monthly reviews, threshold evaluation, documentation

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| OneSignal | Push delivery, segments, A/B variants | Growth: $19/mo + ~$2/mo per 500 web subscribers ($0.004/subscriber) |
| Clay | Enrichment data for segments | ~$50-150/mo depending on credits used |
| PostHog | Analytics, cohorts, experiment tracking | Standard stack — excluded |
| n8n | Automation, sync, send-time optimization | Standard stack — excluded |

## Drills Referenced
- `ab-test-orchestrator` — run systematic A/B tests on push copy, timing, and deep links
- the push notification segmentation workflow (see instructions below) — scale to feature-level and enrichment-enhanced segments
- `churn-prevention` — integrate push as a churn intervention channel
- `dashboard-builder` — deploy always-on monitoring, alerting, and weekly health digests
