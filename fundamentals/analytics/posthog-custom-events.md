---
name: posthog-custom-events
description: Define and implement custom events for GTM measurement in PostHog
tool: PostHog
product: PostHog
difficulty: Intermediate
---

# Track Custom Events in PostHog

## Prerequisites
- PostHog project set up with SDK installed (see `posthog-project-setup`)
- List of key user actions you need to track

## Steps

1. **Define your event taxonomy.** Use a consistent `object_action` naming convention: `signup_completed`, `meeting_booked`, `email_opened`, `deal_created`, `feature_activated`. No spaces, no capitals. Document event names in a shared reference file in your repo.

2. **Identify GTM-critical events.** For each GTM motion, define the events that measure progress:
   - **Outbound:** `email_sent`, `email_replied`, `meeting_booked`
   - **Product-led:** `signup_completed`, `onboarding_step_completed`, `feature_first_used`, `upgrade_initiated`
   - **Content:** `blog_viewed`, `resource_downloaded`, `newsletter_subscribed`

3. **Add event properties.** Every event must include contextual properties:
   ```javascript
   posthog.capture('meeting_booked', {
     source: 'outbound',
     channel: 'email',
     campaign_id: 'q1-cto-outreach'
   })
   ```
   Properties enable filtering and breakdown in analysis.

4. **Implement tracking calls.** Add `posthog.capture('event_name', { properties })` at the moment each action occurs. For critical conversion events (payment, signup), use server-side tracking to avoid browser ad-blockers:
   ```python
   posthog.capture(distinct_id, 'signup_completed', {'plan': 'pro', 'source': 'organic'})
   ```

5. **Create event definitions via API.** Use the PostHog API to tag and describe events:
   ```
   POST /api/projects/<id>/event_definitions/
   { "name": "meeting_booked", "description": "User books a meeting via Cal.com", "tags": ["gtm", "outbound"] }
   ```
   Mark important events as verified so the team knows which events are reliable.

6. **Validate event data.** After deploying, trigger each event manually and use the PostHog MCP `query_events` operation or API to verify the event name, properties, and user association are correct. Fix any issues before building dashboards or funnels on the data.
