---
name: ai-personalization-baseline
description: >
  AI Product Personalization — Baseline Run. Deploy always-on segmentation pipeline
  and multi-surface personalization with automated event tracking.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: ">=50% personalization engagement rate AND >=10pp retention lift vs control at 14 days"
kpis: ["Personalization engagement rate", "14-day retention lift vs control", "Per-segment engagement rate", "Fallback rate"]
slug: "ai-personalization"
install: "npx gtm-skills add product/retain/ai-personalization"
drills:
  - posthog-gtm-events
  - onboarding-personalization
  - engagement-score-computation
---

# AI Product Personalization — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Personalization engagement rate reaches 50% or higher across all segments. Users in the personalized cohort retain at 14 days at a rate at least 10 percentage points higher than the control group. The segmentation and personalization pipelines run daily without manual intervention.

## Leading Indicators

- Daily segmentation pipeline fires successfully (no missed runs for 7+ consecutive days)
- Engagement scores compute daily and update CRM records
- Per-segment engagement rates are within 15pp of each other (no segment left behind)
- Fallback rate (users hitting generic experience) stays below 15%
- Per-surface engagement rates trend upward week-over-week for at least 2 of 3 weeks

## Instructions

### 1. Stand up the event tracking foundation

Run the `posthog-gtm-events` drill to instrument all personalization events properly:

1. Register event definitions in PostHog:
   - `personalization_surface_shown` — `{surface, segment, variant, is_control, user_engagement_score}`
   - `personalization_surface_engaged` — `{surface, segment, variant, action_type}`
   - `personalization_surface_dismissed` — `{surface, segment, variant, time_visible_seconds}`
   - `personalization_segment_transition` — `{old_segment, new_segment, trigger}`
   - `personalization_email_opened` — `{segment, sequence_name, email_number}`
   - `personalization_email_clicked` — `{segment, sequence_name, email_number, link_id}`
2. Build PostHog funnels:
   - `personalization_surface_shown` -> `personalization_surface_engaged` -> `activation_reached` (per segment)
   - `personalization_surface_shown` -> `personalization_surface_dismissed` (per segment — shows rejection rate)
3. Build a PostHog dashboard: "Personalization Baseline" with engagement rate trend, per-segment breakdown, fallback rate, and retention comparison (personalized vs control)

### 2. Deploy always-on segmentation and scoring

Upgrade the one-time segmentation batch from Smoke to an always-on pipeline:

Run the `engagement-score-computation` drill:
1. Deploy the daily n8n pipeline that computes per-user engagement scores (0-100)
2. Configure the four scoring dimensions: frequency, breadth, depth, recency
3. Write scores to Attio custom attributes and PostHog person properties
4. Create PostHog cohorts for each engagement tier (Power User, Engaged, Casual, At Risk, Dormant)

The behavioral segmentation pipeline (from `user-behavior-segmentation`, set up at Smoke) should now also run daily via n8n cron at 06:00 UTC. Verify both pipelines run in sequence: segmentation at 06:00, scoring at 07:00.

### 3. Expand personalization to multiple surfaces and channels

Run the `onboarding-personalization` drill to add persona-specific onboarding tours:

1. Build 3-4 persona-specific Intercom product tours (one per behavioral segment)
2. Route new users to the correct tour based on their `behavior_segment` PostHog property
3. Track tour events with segment context: `tour_started`, `tour_step_completed`, `tour_completed`, `tour_dismissed`
4. Set up a fallback tour for users without a segment assignment

Extend the personalization rule engine from Smoke:
1. Add a second personalized surface (e.g., sidebar recommendations, feature discovery tooltips, or contextual help)
2. Add segment-specific Loops email sequences (5 emails over 21 days per segment — see `personalization-rule-engine` drill for the structure)
3. Configure the n8n orchestration workflow that handles segment transitions: removes users from old sequences, enrolls in new ones, updates Intercom properties

### 4. Run the baseline with a proper control group

1. Set up the experiment: 70% personalized, 30% control (generic experience)
2. Use PostHog feature flags to enforce consistent variant assignment per user
3. Run for 3 weeks to collect 14-day retention data for users who entered in week 1
4. Monitor daily: check the PostHog dashboard for per-segment engagement rates, fallback rate, and retention divergence

### 5. Evaluate against threshold

Measure at the end of week 3:
- Primary: personalization engagement rate >= 50%
- Primary: 14-day retention lift >= 10pp (personalized cohort vs control)
- Guard: fallback rate < 15%
- Guard: no single segment engagement rate below 30%

If PASS, proceed to Scalable. If FAIL:
- If engagement is low across all segments: the personalized surfaces are not compelling enough. Redesign the variant content.
- If engagement is high but retention lift is low: users are clicking but not changing behavior. Redesign to drive deeper product actions, not just surface interactions.
- If one segment is dragging down the average: focus iteration on that segment's tour and messaging.

## Time Estimate

- 4 hours: event instrumentation, funnels, and dashboard setup
- 6 hours: daily segmentation and scoring pipeline deployment in n8n
- 6 hours: onboarding tour creation, second surface personalization, email sequences
- 2 hours: experiment setup and control group configuration
- 2 hours: 3-week monitoring and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, feature flags, experiments, cohorts | Free tier: 1M events/mo. Paid: ~$0.00005/event. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product tours, in-app messages, user properties | Essential: $29/seat/mo. Product Tours on Advanced: $85/seat/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Segment-specific email sequences | Starts at $49/mo (up to ~1K contacts). [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation for segmentation/scoring pipelines | Self-hosted: free. Cloud: starts at $24/mo. [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM for segment and score storage | Free for small teams. Paid: $29/seat/mo. [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost at Baseline:** $50-200/mo (Intercom Advanced seat + Loops starter + n8n cloud)

## Drills Referenced

- `posthog-gtm-events` — instrument all personalization events and build funnels/dashboards
- `onboarding-personalization` — build persona-specific product tours in Intercom
- `engagement-score-computation` — deploy daily per-user engagement scoring pipeline
