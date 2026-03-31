---
name: posthog-custom-events
description: Define and implement custom events for GTM measurement in PostHog
tool: PostHog
difficulty: Intermediate
---

# Track Custom Events in PostHog

## Prerequisites
- PostHog project set up with SDK installed (see `fundamentals/analytics/posthog-project-setup`)
- List of key user actions you need to track

## Steps

1. **Define your event taxonomy.** Create a consistent naming convention. Use object_action format: "signup_completed", "meeting_booked", "email_opened", "deal_created", "feature_activated". Never use spaces or capital letters. Document your event names in a shared spreadsheet.

2. **Identify GTM-critical events.** For each GTM motion, define the events that measure progress. Outbound: "email_sent", "email_replied", "meeting_booked". Product-led: "signup_completed", "onboarding_step_completed", "feature_first_used", "upgrade_initiated". Content: "blog_viewed", "resource_downloaded", "newsletter_subscribed".

3. **Add event properties.** Every event should include relevant properties. For "meeting_booked": { source: "outbound", channel: "email", campaign_id: "q1-cto-outreach" }. For "signup_completed": { plan: "free", referral_source: "google", landing_page: "/pricing" }. Properties enable slicing and filtering in analysis.

4. **Implement tracking calls.** In your application code, add `posthog.capture('event_name', { properties })` at the moment each action occurs. Place tracking on the server side for critical conversion events (payment, signup) to avoid browser-based tracking being blocked.

5. **Create event definitions.** In PostHog, go to Data Management > Events. Add descriptions and tags for each custom event. Mark important events as "Verified" so your team knows which events are reliable and well-defined.

6. **Validate event data.** After deploying, trigger each event manually and check PostHog's Live Events view. Verify the event name, properties, and user association are correct. Fix any issues before building dashboards or funnels on top of the data.
