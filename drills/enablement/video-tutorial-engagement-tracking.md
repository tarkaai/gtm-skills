---
name: video-tutorial-engagement-tracking
description: Instrument video tutorial events in PostHog, build engagement funnels, and connect Loom analytics to product metrics
category: Enablement
tools:
  - PostHog
  - Loom
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - loom-analytics
  - n8n-triggers
  - n8n-workflow-basics
---

# Video Tutorial Engagement Tracking

This drill instruments every video tutorial interaction in PostHog and connects Loom view data to downstream product metrics. The result is a complete picture: which tutorials are watched, how much of each is consumed, and whether watching correlates with activation.

## Input

- Loom video tutorials published and accessible in-app or via email
- PostHog tracking installed in the product with user identification
- n8n instance for syncing Loom analytics to PostHog
- At least 10 published video tutorials

## Steps

### 1. Define the video event taxonomy

Using `posthog-custom-events`, implement these events in your application:

```javascript
// When a video tutorial is shown to a user (in-app embed or email link rendered)
posthog.capture('video_tutorial_impression', {
  video_id: 'loom-video-id',
  video_title: 'Create your first project',
  video_category: 'getting-started',
  surface: 'in-app-embed',        // or 'email-link', 'help-center', 'product-tour'
  persona: 'new-user',             // user persona if known
  trigger: 'onboarding-step-3'     // what caused this video to appear
});

// When a user clicks play on a video
posthog.capture('video_tutorial_started', {
  video_id: 'loom-video-id',
  video_title: 'Create your first project',
  video_category: 'getting-started',
  surface: 'in-app-embed',
  persona: 'new-user',
  video_duration_seconds: 120
});

// When a user completes a video (watched >= 80%)
posthog.capture('video_tutorial_completed', {
  video_id: 'loom-video-id',
  video_title: 'Create your first project',
  video_category: 'getting-started',
  surface: 'in-app-embed',
  persona: 'new-user',
  watch_percentage: 92,
  video_duration_seconds: 120
});

// When a user takes the action the tutorial teaches (post-video activation)
posthog.capture('video_tutorial_activated', {
  video_id: 'loom-video-id',
  video_title: 'Create your first project',
  video_category: 'getting-started',
  action_taken: 'project_created',
  minutes_after_video: 5
});
```

### 2. Sync Loom analytics to PostHog

Using `n8n-triggers`, build a workflow triggered every 6 hours:

1. Query the Loom API for all tutorial video analytics: `GET /v1/videos/{video-id}/analytics` for each published tutorial
2. For each viewer in the Loom response, map the viewer email to a PostHog user ID
3. For viewers not yet tracked in PostHog (e.g., email-only viewers), capture a server-side event:

```json
{
  "event": "video_tutorial_viewed_loom",
  "distinct_id": "viewer-email@example.com",
  "properties": {
    "video_id": "loom-video-id",
    "watch_percentage": 85,
    "source": "loom-api-sync",
    "viewed_at": "2026-03-28T14:00:00Z"
  }
}
```

4. Use n8n's PostHog node or HTTP request to POST to `https://app.posthog.com/capture/`

### 3. Build the video tutorial funnel

Using `posthog-funnels`, create a funnel:

```
video_tutorial_impression
  -> video_tutorial_started     (play rate)
  -> video_tutorial_completed   (completion rate)
  -> video_tutorial_activated   (post-video activation)
```

Break down by:
- `video_category` (which topic areas perform best)
- `surface` (in-app vs email vs help center)
- `persona` (which user types engage most with video)
- Signup week (cohort analysis)

The largest drop-off in this funnel tells you where to focus:
- Low impression-to-start: video placement or thumbnail is ineffective
- Low start-to-complete: video is too long, poorly structured, or wrong topic
- Low complete-to-activate: video teaches but does not motivate action

### 4. Build video engagement cohorts

Using `posthog-cohorts`, create these reusable segments:

- **Video watchers**: Users who completed at least 1 tutorial in the last 14 days
- **Video skippers**: Users who saw an impression but never started (in last 14 days)
- **Video non-converters**: Users who completed tutorials but did not take the taught action
- **Video power learners**: Users who completed 3+ tutorials in their first 7 days
- **Never exposed**: Users who never saw a video tutorial impression (control group)

These cohorts enable A/B comparisons: do video watchers activate at a higher rate than skippers or never-exposed users?

### 5. Set up person properties for video engagement

Using `posthog-custom-events`, set person properties that accumulate:

```javascript
posthog.people.set({
  total_tutorials_watched: incrementBy(1),
  last_tutorial_watched: 'Create your first project',
  last_tutorial_date: '2026-03-28',
  tutorial_categories_completed: ['getting-started', 'core-workflows'],
  video_engagement_tier: 'active'   // none, passive (impressions only), active (1+ watched), power (3+ watched)
});
```

These properties feed into the `onboarding-personalization` and `video-tutorial-personalization` drills.

### 6. Measure video impact on activation

Create a PostHog insight comparing activation rate for:
- Users who watched at least 1 tutorial vs. users who did not
- Users who watched the specific tutorial for each activation step vs. those who skipped it

This proves (or disproves) that video tutorials actually improve activation. If video watchers do not activate at a higher rate, the tutorials need to be rewritten to be more action-oriented, or the post-video CTA needs to link directly to the action.

## Output

- Video event taxonomy implemented in PostHog (4 event types)
- Loom-to-PostHog analytics sync running every 6 hours via n8n
- Video tutorial funnel with category/surface/persona breakdowns
- 5 reusable video engagement cohorts
- Person-level video engagement properties
- Video impact on activation measurement

## Triggers

The Loom analytics sync runs every 6 hours via n8n cron. The funnel and cohorts are reviewed weekly. Re-run the taxonomy setup when adding new video categories or surfaces.
