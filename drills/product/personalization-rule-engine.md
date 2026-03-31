---
name: personalization-rule-engine
description: Configure and deploy rule-based personalization that adapts in-app surfaces, messaging, and content per behavioral segment
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
fundamentals:
  - posthog-feature-flags
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-product-tours
  - intercom-user-properties
  - loops-sequences
  - n8n-triggers
  - n8n-workflow-basics
---

# Personalization Rule Engine

This drill builds the rule engine that maps behavioral segments to personalized product experiences. Given a user's segment (from the `user-behavior-segmentation` drill), the engine selects and delivers the right in-app messages, product tours, email sequences, feature emphasis, and content recommendations. It is the execution layer that sits between segmentation (who they are) and measurement (did it work).

## Input

- Behavioral segments assigned to users via the `user-behavior-segmentation` drill (stored as PostHog person properties and Intercom user properties)
- PostHog feature flags enabled
- Intercom configured with in-app messages and product tours
- Loops configured with triggered sequences
- n8n instance for orchestration

## Steps

### 1. Define the personalization surface map

For each behavioral segment, define what changes across three surfaces:

**Surface 1 — In-app experience (PostHog feature flags)**

Using `posthog-feature-flags`, create multivariate flags that control UI elements per segment:

- `personalization-dashboard-layout`: Controls which widgets appear on the user's dashboard. Power Builders see creation tools and activity feeds. Efficient Executors see task lists and quick-access shortcuts. Explorers see feature discovery cards and tips. Team Coordinators see team activity and management panels. Passive Consumers see curated content and getting-started prompts.
- `personalization-cta-variant`: Controls the primary CTA the user sees. Each segment gets a CTA that drives their next-best-action: Power Builders → "Start new project", Efficient Executors → "Continue where you left off", Explorers → "Try [underused feature]", Team Coordinators → "Review team activity", Passive Consumers → "Create your first [artifact]".
- `personalization-feature-emphasis`: Controls which features are highlighted in navigation or tooltips per segment.

Set each flag to distribute based on the `behavior_segment` person property.

### 2. Configure in-app messaging per segment

Using `intercom-in-app-messages`, create targeted messages for each segment:

**Power Builders:**
- Trigger: Weekly. Content: "Power tip: [advanced feature they haven't used]." Goal: expand feature breadth.
- Trigger: On usage milestone. Content: "You've created [N] items — unlock [next tier feature]." Goal: drive expansion.

**Efficient Executors:**
- Trigger: On login. Content: "Keyboard shortcuts for your most-used actions." Goal: speed up their workflow.
- Trigger: When session > 2x average. Content: "You're doing more today — would [automation feature] help?" Goal: increase efficiency.

**Explorers:**
- Trigger: After visiting 3+ feature areas without completing an action. Content: "Here's a 2-minute tour of [most relevant feature]." Goal: guide to activation.
- Trigger: After 14 days without settling on a primary workflow. Content: "Most users like you start with [feature]. Try it?" Goal: reduce decision paralysis.

**Team Coordinators:**
- Trigger: Weekly. Content: "Team health: [N] active this week, [N] items completed." Goal: reinforce management value.
- Trigger: When a team member goes inactive. Content: "[Name] hasn't logged in for 7 days — send them a nudge?" Goal: prevent team-level churn.

**Passive Consumers:**
- Trigger: On 3rd session with no creation action. Content: "Try creating your first [artifact] — it takes 2 minutes." Goal: convert to active usage.
- Trigger: After 14 days of passive-only behavior. Content: "People who create [artifacts] get [specific benefit]. Start now?" Goal: push past consumption.

Using `intercom-user-properties`, sync the `behavior_segment` property to Intercom for all message targeting.

### 3. Configure email sequences per segment

Using `loops-sequences`, create segment-specific drip sequences triggered by segment assignment:

**Sequence structure per segment (5 emails over 21 days):**

1. **Day 0 — Welcome to your path:** Explain what the product does best for their use case. One CTA.
2. **Day 3 — Quick win:** A specific, completable task that delivers value in under 5 minutes.
3. **Day 7 — Deeper dive:** A workflow tutorial for their primary workflow.
4. **Day 14 — Social proof:** A case study or testimonial from someone in their segment.
5. **Day 21 — Next level:** An upsell or expansion prompt tailored to their segment's next-best-action.

Each email references the user's actual product data where possible: items created, features used, time saved. Pull this data via n8n from PostHog and inject into Loops personalization variables.

### 4. Build the orchestration workflow in n8n

Using `n8n-triggers`, create a workflow that fires when a `behavior_segment_assigned` event arrives from PostHog:

1. **Read the segment assignment:** Extract `segment`, `previous_segment`, `primary_workflow` from the event
2. **Check for segment change:** If `segment != previous_segment`:
   a. Remove the user from the previous segment's Loops sequence (via Loops API)
   b. Add the user to the new segment's Loops sequence
   c. Update Intercom user properties with the new segment
   d. Log the transition in PostHog: `personalization_segment_transition` with `{old_segment, new_segment}`
3. **If new user (no previous segment):**
   a. Enroll in the segment's Loops sequence
   b. Set Intercom properties
   c. Log `personalization_first_assignment` event
4. **Rate limit:** Do not transition a user more than once per 7 days. If a user oscillates between segments, keep them in the current segment until stable for 7 days.

### 5. Instrument personalization events

Using `posthog-custom-events`, track every personalization touchpoint:

- `personalization_surface_shown` — `{surface: "dashboard"|"cta"|"tooltip", segment, variant}`
- `personalization_surface_engaged` — user clicked/interacted with a personalized surface
- `personalization_surface_dismissed` — user dismissed or ignored
- `personalization_message_shown` — Intercom in-app message was displayed
- `personalization_message_clicked` — user clicked CTA in the message
- `personalization_email_opened` — segment-specific email was opened
- `personalization_email_clicked` — segment-specific email CTA was clicked

These events feed the `threshold-engine` drill for pass/fail evaluation and the `ab-test-orchestrator` for optimization.

### 6. Define fallback behavior

Not every user will have a segment (new users before first classification, users with insufficient data). Define the fallback:

- Feature flags default to the "Explorer" variant (guides discovery)
- In-app messages default to the generic onboarding tour
- Email sequences default to the general welcome sequence
- Log `personalization_fallback_used` event to track fallback frequency

If fallback rate exceeds 20% of active users, the segmentation pipeline has coverage issues — investigate with the `user-behavior-segmentation` drill.

## Output

- PostHog feature flags controlling per-segment UI personalization
- Intercom in-app messages targeted by behavioral segment
- Loops email sequences for each segment
- n8n orchestration workflow for segment transition handling
- Full event instrumentation for measuring personalization effectiveness
- Fallback paths for unsegmented users

## Triggers

- Real-time: n8n workflow fires on every `behavior_segment_assigned` event
- Segment messaging review: monthly (update message copy, review engagement rates)
- Surface variant refresh: quarterly (redesign personalized surfaces based on A/B test results)
