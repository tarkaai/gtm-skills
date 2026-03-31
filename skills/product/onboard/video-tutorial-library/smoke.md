---
name: video-tutorial-library-smoke
description: >
  Video Tutorial Library — Smoke Test. Record 5 video tutorials for your highest-friction
  onboarding steps, embed them in-app and in email, and measure whether users who watch
  tutorials activate at a higher rate than those who do not.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=30% of exposed users start at least 1 tutorial AND tutorial watchers activate at >=1.5x the rate of non-watchers"
kpis: ["Video play rate (impressions to starts)", "Video completion rate (starts to 80%+ watched)", "Post-video activation rate (completed to action taken)", "Tutorial watcher vs non-watcher activation lift"]
slug: "video-tutorial-library"
install: "npx gtm-skills add product/onboard/video-tutorial-library"
drills:
  - video-content-pipeline
  - onboarding-sequence-design
  - threshold-engine
---

# Video Tutorial Library — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

At least 30% of users exposed to video tutorials start watching at least one. Users who complete a tutorial activate (perform the taught action) at 1.5x or higher the rate of users who skip the tutorial. This proves that video content accelerates onboarding before investing in a full library.

## Leading Indicators

- Users click on embedded video thumbnails (play rate > 30%)
- Users who start a tutorial watch at least 80% of it (completion rate > 60%)
- Users take the taught action within 30 minutes of completing a video
- Support ticket volume decreases for topics covered by tutorials

## Instructions

### 1. Identify the 5 highest-friction onboarding steps

Query PostHog for your onboarding funnel (from the `onboarding-sequence-design` drill). Identify the 5 steps with the largest drop-off rates. These are the tutorials that will have the most impact. Rank them by drop-off magnitude.

Example friction points:
- Initial data import (users do not know the file format)
- First core object creation (users do not understand the data model)
- Team invitation (users skip this but it drives retention)
- Integration setup (users abandon due to complexity)
- First workflow completion (users get lost mid-process)

### 2. Record 5 video tutorials

Run the `video-content-pipeline` drill for each of the 5 friction points:

For each tutorial:
1. Write a 3-point outline: what the user will learn, the exact steps, and the result they will see
2. Record with Loom in screen + camera mode. Keep each video under 3 minutes.
3. Open with a 10-second hook: "In the next 2 minutes, you'll learn how to [specific outcome]."
4. Walk through the exact click path. Move slowly. Narrate every click.
5. End with a clear CTA: "Now try it yourself -- click [specific button] to get started."
6. Edit in Descript: remove filler words, trim dead air, add captions
7. Export and publish to Loom with the naming convention: `[Tutorial] {Action verb} {feature}`

**Human action required:** Record each video yourself or designate a team member. The agent prepares outlines and post-production but cannot record the screencasts.

### 3. Embed tutorials in-app and in email

For in-app embedding:
- Add the Loom GIF thumbnail to the relevant product page where users encounter the friction point
- When clicked, open the Loom video in a modal or new tab
- Track impressions and clicks as PostHog events (the agent instruments `video_tutorial_impression` and `video_tutorial_started` events)

For email embedding:
- Update the onboarding email sequence (from `onboarding-sequence-design` drill) to include the relevant tutorial GIF thumbnail in the email that corresponds to each friction step
- Link the thumbnail to the Loom video with UTM parameters: `?utm_source=loops&utm_medium=email&utm_campaign=tutorial-smoke`

### 4. Instrument tracking

Implement the following PostHog events manually or via the tracking code:

```javascript
posthog.capture('video_tutorial_impression', {
  video_id: '{loom-id}',
  video_title: '{tutorial title}',
  video_category: 'onboarding',
  surface: 'in-app-embed'  // or 'email-link'
});

posthog.capture('video_tutorial_started', { /* same properties */ });
posthog.capture('video_tutorial_completed', { /* + watch_percentage */ });
posthog.capture('video_tutorial_activated', { /* + action_taken, minutes_after_video */ });
```

### 5. Run for 7 days and evaluate

Expose tutorials to 50-100 new users during the test week. Do not use feature flags yet -- show tutorials to all new users.

After 7 days, run the `threshold-engine` drill to evaluate:
- **Primary threshold:** >=30% play rate (of users who saw an impression, at least 30% started a video)
- **Secondary threshold:** Tutorial watchers activate at >=1.5x the rate of non-watchers

If PASS: proceed to Baseline. Document which tutorials had the highest completion and activation rates.
If FAIL: diagnose using the funnel. Low play rate = bad placement or thumbnails. Low completion = videos too long or poorly structured. Low activation = videos teach but do not motivate action. Fix the weakest link and re-run.

## Time Estimate

- 2 hours: identify friction points and write tutorial outlines
- 3 hours: record and edit 5 tutorials (30-40 min each including re-takes)
- 1 hour: embed in-app and in email, instrument tracking
- 1 hour: review data after 7 days, run threshold check
- 1 hour: document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record and host tutorial videos | Free (up to 25 videos, 5 min each). Business: $12.50/user/mo for unlimited. [loom.com/pricing](https://www.atlassian.com/software/loom/pricing) |
| Descript | Edit videos, remove filler words, add captions | Free (1hr transcription). Creator: $24/mo. [descript.com/pricing](https://www.descript.com/pricing) |
| PostHog | Track video events and build funnels | Free (1M events/mo). [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Lifecycle emails with embedded video thumbnails | Free (up to 1,000 contacts). $49/mo for more. [loops.so/pricing](https://loops.so/pricing) |

**Estimated cost at Smoke level:** $0 (free tiers sufficient for 5 videos and <100 users)

## Drills Referenced

- `video-content-pipeline` -- record, edit, and distribute the 5 tutorial videos
- `onboarding-sequence-design` -- integrate tutorial videos into the existing onboarding email sequence
- `threshold-engine` -- evaluate play rate and activation lift against pass thresholds
