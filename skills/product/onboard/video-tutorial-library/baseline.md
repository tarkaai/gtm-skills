---
name: video-tutorial-library-baseline
description: >
  Video Tutorial Library — Baseline Run. Expand to 15+ tutorials with structured event tracking,
  always-on Loom-to-PostHog analytics sync, and automated email delivery. Run a controlled
  experiment comparing tutorial-exposed vs control users over 2 weeks.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=40% play rate AND >=8pp activation lift (tutorial watchers vs control) sustained over 2 weeks"
kpis: ["Video play rate", "Video completion rate", "Post-video activation rate", "Activation lift vs control group", "Tutorial coverage (% of onboarding steps with a video)"]
slug: "video-tutorial-library"
install: "npx gtm-skills add product/onboard/video-tutorial-library"
drills:
  - posthog-gtm-events
  - video-tutorial-engagement-tracking
  - onboarding-flow
---

# Video Tutorial Library — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

Play rate reaches 40%+ across all tutorial surfaces. Users who watch tutorials activate at least 8 percentage points higher than a control group that does not see tutorials. The Loom-to-PostHog analytics pipeline runs continuously without manual intervention.

## Leading Indicators

- Loom-to-PostHog sync runs every 6 hours without errors
- Per-video completion rates hold above 60% as library expands
- Email click-through rate on tutorial thumbnails exceeds 5%
- In-app tutorial impressions reach 80%+ of new signups
- PostHog funnel shows clear conversion from video_tutorial_completed to activation events

## Instructions

### 1. Expand the tutorial library to 15+ videos

Record tutorials for every major onboarding step, not just the top 5 friction points from Smoke. Cover:

- **Getting Started (4-5 videos):** Account setup, first core action, team invitation, profile configuration, initial settings
- **Core Workflows (5-6 videos):** One video per primary use case or workflow your product supports
- **Integrations (3-4 videos):** Setup guides for your top integrations
- **Tips & Shortcuts (2-3 videos):** Keyboard shortcuts, power-user tricks, time-saving features

Use the `video-content-pipeline` drill for each. Maintain the naming convention from Smoke: `[Tutorial] {Action verb} {feature}`.

Organize videos into Loom folders: Getting Started, Core Workflows, Integrations, Tips.

### 2. Set up the video event taxonomy

Run the `posthog-gtm-events` drill to implement the standard event taxonomy. Then run the `video-tutorial-engagement-tracking` drill to:

1. Implement the 4 video event types in your product code: `video_tutorial_impression`, `video_tutorial_started`, `video_tutorial_completed`, `video_tutorial_activated`
2. Build the Loom-to-PostHog sync workflow in n8n (runs every 6 hours)
3. Create the video tutorial funnel in PostHog
4. Build the 5 video engagement cohorts
5. Set person-level video engagement properties

### 3. Run a controlled experiment

Create a PostHog feature flag `video-tutorials-baseline`:
- 50% of new signups see tutorial videos embedded in-app and in email (treatment)
- 50% of new signups get the standard onboarding without video tutorials (control)

Ensure the flag is user-level (each user is consistently in the same group for their entire onboarding period).

### 4. Configure always-on delivery

For the treatment group:

**In-app delivery:**
Run the `onboarding-flow` drill to embed video tutorials at each onboarding step. Use Intercom in-app messages triggered by user state:
- User has not completed Step N after 1 session -> show tutorial for Step N as a tooltip with Loom GIF thumbnail
- User completes Step N -> dismiss the tutorial message for that step

**Email delivery:**
Update the onboarding email sequence to include the relevant tutorial video in each email. Each email gets the GIF thumbnail for the tutorial that matches that email's onboarding step. Place the thumbnail after the text CTA, not before (text-first for deliverability).

### 5. Monitor for 2 weeks

Review the following daily:
- Loom-to-PostHog sync health (n8n workflow execution history)
- Video tutorial funnel (play rate, completion rate, activation rate)
- Treatment vs control activation rates

Do not adjust anything mid-experiment. The only exception: if a video has <20% completion rate after 3 days, it is actively hurting the experience -- replace it with a shorter version.

### 6. Evaluate against thresholds

After 2 weeks with at least 100 users in each group:

**Primary threshold:** >=40% play rate in the treatment group (of users who see an impression, 40%+ start a video)

**Secondary threshold:** >=8 percentage point activation lift (if control activates at 30%, treatment must activate at 38%+)

If PASS on both: proceed to Scalable. Document per-video performance rankings and the activation lift number.
If PASS on play rate but FAIL on lift: tutorials are engaging but not driving action. Rewrite CTAs to link directly to the action. Add post-video deep links. Re-run for 1 more week.
If FAIL on play rate: placement or thumbnails are not compelling. Test different surfaces (help center, product tour integration, chatbot suggestion). Re-run.

## Time Estimate

- 8 hours: record 10 additional tutorials (expand from 5 to 15+)
- 4 hours: implement video event taxonomy and Loom-to-PostHog sync
- 3 hours: configure feature flag, in-app delivery, email delivery
- 2 hours: monitor over 2 weeks (15 min/day check)
- 3 hours: analyze results, document findings, prepare for Scalable

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record, host, and organize 15+ tutorial videos | Business: $12.50/user/mo (API access for analytics sync). [loom.com/pricing](https://www.atlassian.com/software/loom/pricing) |
| Descript | Edit videos, add captions, remove filler words | Creator: $24/mo (30hr transcription). [descript.com/pricing](https://www.descript.com/pricing) |
| PostHog | Video event tracking, funnels, feature flags, cohorts | Free (1M events/mo). [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Loom-to-PostHog sync workflow (every 6 hours) | Starter: ~$24/mo (2,500 executions). Self-hosted: free. [n8n.io/pricing](https://n8n.io/pricing/) |
| Loops | Onboarding emails with embedded tutorial thumbnails | $49/mo (1,000+ contacts). [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app tutorial recommendations | Essential: $29/seat/mo (annual). [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated cost at Baseline level:** $50-140/mo (Loom Business + Descript Creator + n8n Starter; PostHog free tier; Loops and Intercom if already in stack)

## Drills Referenced

- `posthog-gtm-events` -- implement the standard event taxonomy for video tracking
- `video-tutorial-engagement-tracking` -- instrument video events, build funnels, sync Loom analytics to PostHog
- `onboarding-flow` -- embed tutorials into the multi-channel onboarding experience
