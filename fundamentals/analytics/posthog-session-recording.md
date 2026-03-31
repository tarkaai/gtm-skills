---
name: posthog-session-recording
description: Use PostHog session recordings to understand user behavior
tool: PostHog
difficulty: Beginner
---

# Use Session Recordings in PostHog

## Prerequisites
- PostHog project with web SDK installed
- Session recording enabled in project settings

## Steps

1. **Enable session recording.** In PostHog, go to Project Settings > Session Recording and toggle it on. Configure the sampling rate -- start with 100% for low-traffic sites or 10-20% for high-traffic sites. PostHog captures DOM changes, mouse movements, clicks, and console errors.

2. **Set up recording filters.** You do not need to record everything. Configure filters to focus on high-value pages: pricing page, signup flow, onboarding screens, and key feature pages. Exclude sensitive pages (account settings, payment forms) to protect user privacy.

3. **Watch recordings of key flows.** Go to Session Recordings and filter by: users who visited the pricing page but did not sign up, users who started onboarding but dropped off, or users who hit an error. Watch 10-15 sessions per pattern to identify common friction points.

4. **Use the event timeline.** Each recording shows a timeline of events the user triggered. Click on events to jump to that moment in the recording. This lets you quickly find the moments where users hesitated, rage-clicked, or abandoned a flow.

5. **Create playlists.** Save interesting recordings to playlists: "Signup Friction", "Onboarding Confusion", "Feature Discovery". Share playlists with your product and design team. Watching real user behavior is more persuasive than metrics alone when advocating for changes.

6. **Connect recordings to funnels.** When analyzing a funnel (see `fundamentals/analytics/posthog-funnels`), click into a drop-off step to see recordings of users who dropped off at that stage. This combines quantitative (where they drop) with qualitative (why they drop) analysis.
