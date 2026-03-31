---
name: ai-user-segmentation-baseline
description: >
  AI Behavior Segmentation -- Baseline Run. Automate the weekly segmentation pipeline and
  launch segment-specific personalized experiences via Intercom and Loops. First always-on
  automation targeting >=80% assignment accuracy and measurable personalization lift.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: ">=80% segment assignment accuracy (stability) and >=5% personalization lift in engagement rate"
kpis: ["Segment stability (week-over-week consistency)", "Personalization engagement rate", "Retention lift vs control", "Unclassified user rate"]
slug: "ai-user-segmentation"
install: "npx gtm-skills add product/retain/ai-user-segmentation"
drills:
  - behavior-segmentation-pipeline
  - segment-personalization-routing
  - posthog-gtm-events
  - threshold-engine
---
# AI Behavior Segmentation -- Baseline Run

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Turn the validated segmentation signal into always-on automation. The weekly segmentation pipeline runs automatically, and each segment receives personalized in-app messages, product tours, and email sequences. At this level, you prove that personalization driven by behavioral segments improves engagement beyond a generic experience.

**Pass threshold:** >=80% segment assignment accuracy (measured as week-over-week stability: >80% of users stay in the same segment) AND >=5% engagement lift from personalized experiences vs. a control group receiving generic content.

## Leading Indicators

- Weekly pipeline runs without manual intervention for 3 consecutive weeks
- Segment distribution stays balanced (no single segment >40%)
- Unclassified user rate <10% (improved from Smoke level)
- At least 3 segment-specific in-app messages are live and rendering
- Email sequence open rates per segment are measurably different (segments respond to different content)

## Instructions

### 1. Instrument segmentation events

Run the `posthog-gtm-events` drill to set up the event taxonomy for segmentation. Create these standard events:

- `behavior_segment_assigned` -- fired each time a user is assigned/re-assigned to a segment. Properties: `segment_id`, `segment_label`, `confidence`, `previous_segment_id`
- `behavior_segment_changed` -- fired when a user's segment changes from one to another. Properties: `old_segment`, `new_segment`, `reason`
- `segment_message_shown` -- personalized in-app message rendered. Properties: `segment_id`, `message_id`, `surface` (in_app/tour/email)
- `segment_message_clicked` -- user clicked CTA on personalized content. Properties: `segment_id`, `message_id`, `surface`
- `segment_tour_started`, `segment_tour_completed` -- product tour lifecycle per segment

Build a PostHog funnel: `segment_message_shown` -> `segment_message_clicked` -> target action completed. This measures personalization conversion per segment.

### 2. Automate the weekly segmentation pipeline

Run the `behavior-segmentation-pipeline` drill's step 9 (build the recurring pipeline). Set up the n8n workflow:

- **Weekly cron (Sunday 06:00 UTC):** Extract fresh behavior vectors, assign all active users to current cluster definitions, detect segment changes, update PostHog and Attio
- **Monthly cron (1st of month):** Re-run cluster discovery to check if segment definitions need updating

Validate the first automated run by comparing its output to your Smoke test assignments. Expect >75% overlap -- some movement is normal as behavior data refreshes, but wholesale reassignment means the model is unstable.

### 3. Set up the control group

Using PostHog feature flags, create a control group that does NOT receive personalized experiences:

- Flag key: `segment-personalization-enabled`
- Target: 80% of users get personalized experiences (treatment), 20% get the generic default (control)
- Do NOT split by segment -- the control group should be a random 20% across all segments

This control group is critical for measuring personalization lift. Without it, you cannot distinguish "personalization helped" from "these users were already engaged."

### 4. Build personalized experiences per segment

Run the `segment-personalization-routing` drill:

1. Define the personalization matrix (step 1) using the cluster definitions from your Smoke test. Each segment gets a distinct in-app message, feature highlight, and email sequence.

2. Configure Intercom in-app messages (step 3) for the top 3 segments by size. Start with 3 segments, not all of them -- you need enough volume per segment to measure results. Smaller segments can be added at Scalable level.

3. Configure Loops email sequences (step 5) for the same 3 segments. 4 emails over 14 days per segment, each focused on the segment's personalization strategy.

4. Set up the n8n routing workflow (step 6) so that when a user's segment changes, their Intercom targeting and Loops enrollment update automatically.

**Human action required:** Write the in-app message copy and email content for each segment. The drill provides the framework and structure, but the actual copy needs to be tailored to your product. Review the first batch of messages before going live.

### 5. Monitor stability and engagement for 3 weeks

Let the system run for 3 full weekly cycles. Each week, check:

- **Segment stability:** What % of users stayed in the same segment? Log this as a PostHog event.
- **Personalization engagement:** For users in the treatment group, what is the segment_message_clicked rate? Compare across segments.
- **Retention lift:** Compare 14-day retention of the treatment group (personalized) vs. control group (generic). Even small lifts at this stage are signal.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate after 3 weeks:

- **Segment stability:** >=80% of users remain in the same segment week-over-week across all 3 cycles. If <80%, the behavior vectors or clustering model needs tuning before proceeding.
- **Personalization lift:** >=5% higher engagement rate (segment_message_clicked / segment_message_shown) in the treatment group vs. the control group's equivalent generic message engagement.

If PASS: Proceed to Scalable. The automated pipeline is stable and personalization drives measurable engagement improvement.

If FAIL on stability: Review the behavior vector dimensions. Reduce noisy signals (e.g., remove time-of-day if it causes weekly fluctuation). Consider increasing the cluster assignment confidence threshold to 0.6 or 0.7.

If FAIL on engagement lift: Review the personalization content. Is it genuinely different per segment, or just superficially varied? Check if the control group's generic experience is already good enough that personalization adds little. Try bolder differentiation: different CTAs, different feature highlights, different email cadences.

## Time Estimate

- 3 hours: Instrument events and set up the segmentation event taxonomy
- 4 hours: Automate the weekly pipeline and validate first run
- 2 hours: Set up control group and feature flags
- 6 hours: Build personalized in-app messages and email sequences for 3 segments
- 2 hours: Configure n8n routing workflow
- 3 hours: Monitor 3 weekly cycles and evaluate results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Behavior extraction, cohorts, feature flags, analytics | Free tier (1M events/mo) or existing plan -- [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API (Anthropic) | Weekly clustering and assignment | ~$0.60/mo (4 weekly runs) -- [anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Intercom | Segment-specific in-app messages and tours | Starter ~$74/mo -- [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Segment-specific email sequences | Free tier (1,000 contacts) or Starter $49/mo -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** ~$50-125/mo (Intercom + Loops if beyond free tiers; Claude API is negligible)

## Drills Referenced

- `behavior-segmentation-pipeline` -- Automated weekly extraction, clustering, and assignment
- `segment-personalization-routing` -- Routes personalized experiences to each segment via Intercom and Loops
- `posthog-gtm-events` -- Standard event taxonomy for segmentation tracking
- `threshold-engine` -- Evaluates stability and engagement lift against pass thresholds
