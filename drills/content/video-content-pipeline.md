---
name: video-content-pipeline
description: Record, edit, and distribute short-form video content for product demos and thought leadership
category: Content
tools:
  - Loom
  - Descript
  - PostHog
fundamentals:
  - loom-recording
  - descript-editing
  - posthog-event-tracking
---

# Video Content Pipeline

This drill builds a repeatable workflow for creating video content — product demos, tutorials, thought leadership clips, and customer testimonials. Video drives engagement and trust faster than text alone.

## Prerequisites

- Loom account for quick recordings
- Descript account for editing and transcription
- PostHog tracking on your video hosting pages
- A quiet recording environment with decent audio

## Steps

### 1. Define video types and cadence

Establish which video formats serve your GTM motion:

- **Product demos (2-5 min)**: Walk through a specific use case or feature. Best for mid-funnel prospects.
- **Quick tutorials (1-3 min)**: Show how to do one specific thing. Great for onboarding and support.
- **Thought leadership (3-7 min)**: Share an insight or opinion on an industry topic. Drives top-of-funnel awareness.
- **Customer testimonials (2-4 min)**: Let a customer explain their experience in their own words.

Set a cadence: 1-2 videos per week is sustainable for a small team.

### 2. Script and outline

Do not wing it. Write a brief outline for each video: opening hook (what the viewer will learn in 10 seconds), 3-5 key points, and a closing CTA. For product demos, plan the exact click path in advance. For thought leadership, write the opening and closing lines word-for-word but speak the middle naturally.

### 3. Record with Loom

Using the `loom-recording` fundamental, set up your recording. For product demos, use screen + camera. For thought leadership, use camera only or camera + slides. Keep recordings in one take when possible — imperfect-but-authentic beats over-produced. Loom's built-in tools let you trim dead air and add CTAs after recording.

### 4. Edit in Descript

Using the `descript-editing` fundamental, import your Loom recording for editing. Descript transcribes automatically — edit the text to edit the video. Remove filler words ("um", "uh"), cut long pauses, and trim the intro and outro to be tight. Add captions (80% of social video is watched without sound). Export clips of the best 30-60 second segments for social media.

### 5. Distribute across channels

Upload the full video to your website or blog. Post clips to LinkedIn and Twitter using the `social-content-pipeline` drill. Embed product demos in outreach emails (a personalized Loom in a cold email can double reply rates). Add tutorial videos to your onboarding flow.

### 6. Track engagement

Using `posthog-event-tracking`, track video plays, watch time, completion rate, and CTA clicks. Videos with high drop-off in the first 10 seconds need better hooks. Videos with high completion but low CTA clicks need stronger calls to action. Iterate based on data.
