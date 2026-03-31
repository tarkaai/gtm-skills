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

1. **Enable session recording via API.** Use the PostHog API to enable recordings in your project settings:
   ```
   PATCH /api/projects/<id>/
   { "session_recording_opt_in": true }
   ```
   Or enable during SDK init: `posthog.init('<key>', { session_recording: { maskAllInputs: true } })`. Configure the sampling rate: 100% for low-traffic sites, 10-20% for high-traffic sites.

2. **Set up recording filters.** Configure the SDK to focus on high-value pages: pricing page, signup flow, onboarding screens, and key feature pages. Exclude sensitive pages (account settings, payment forms) via SDK config:
   ```javascript
   posthog.init('<key>', {
     session_recording: { maskAllInputs: true, blockSelector: '.sensitive-data' }
   })
   ```

3. **Query recordings via API.** Use the PostHog API to find relevant recordings:
   ```
   GET /api/projects/<id>/session_recordings/?events=[{"id":"signup_started"}]&date_from=-7d
   ```
   Filter by: users who visited pricing but did not sign up, users who started onboarding but dropped off, or users who hit an error. Review 10-15 sessions per pattern to identify common friction points.

4. **Use event timeline data.** Each recording has an associated event timeline accessible via the API. Events are timestamped so you can jump to specific moments: hesitations, rage-clicks, or flow abandonment.

5. **Create playlists via API.** Save recordings to playlists for team review:
   ```
   POST /api/projects/<id>/session_recording_playlists/
   { "name": "Signup Friction", "description": "Users who abandoned signup form" }
   ```
   Share playlists with your product and design team for qualitative analysis.

6. **Connect recordings to funnels.** When analyzing a funnel (see `posthog-funnels`), use the API to fetch recordings of users who dropped off at a specific step. This combines quantitative (where they drop) with qualitative (why they drop) analysis.
