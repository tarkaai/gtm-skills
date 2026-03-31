---
name: outbound-with-short-video-baseline
description: >
  Outbound With Short Video — Baseline Run. Scale personalized Loom video outreach
  to 50-100 prospects with always-on email sequencing, automated video engagement
  tracking via PostHog, and engagement-based follow-up routing.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=10% video completion rate AND >=4 meetings booked over 2 weeks"
kpis: ["Video completion rate", "Thumbnail click-through rate", "Meetings booked from video", "Video-to-meeting conversion rate"]
slug: "outbound-with-short-video"
install: "npx gtm-skills add marketing/solution-aware/outbound-with-short-video"
drills:
  - video-prospecting-outreach
  - posthog-gtm-events
  - video-engagement-follow-up
  - cold-email-sequence
---

# Outbound With Short Video — Baseline Run

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Outcomes

Scale video outreach from the Smoke test's 15-25 prospects to 50-100 prospects over 2 weeks. Transition from manual tracking to always-on PostHog event tracking. Implement automated follow-up routing based on Loom video watch behavior (high/medium/low engagement). Validate that video outreach produces consistent results over a sustained period.

**Pass threshold:** >=10% video completion rate AND >=4 meetings booked over 2 weeks.

## Leading Indicators

- Video thumbnail click rate sustains >15% across multiple batches (not just one lucky send)
- Engagement-based follow-up (high-engagement branch) converts to meetings at 2x+ the rate of standard sequence
- Positive reply rate from video emails exceeds your text-only baseline by >=3 percentage points
- Loom CTA click rate >5% of video viewers (the in-video booking link is working)
- PostHog funnel shows clear video_sent -> video_viewed -> meeting_booked conversion path

## Instructions

### 1. Set up video outreach event tracking

Run the `posthog-gtm-events` drill to configure the video outreach event taxonomy in PostHog:

- `video_email_sent` — properties: campaign_id, prospect_tier, loom_video_id
- `video_email_opened` — properties: campaign_id, open_count
- `video_thumbnail_clicked` — properties: campaign_id, prospect_email
- `video_viewed` — properties: campaign_id, prospect_email, watch_percentage, cta_clicked
- `video_email_replied` — properties: campaign_id, sentiment, sequence_step
- `video_meeting_booked` — properties: campaign_id, source (cta_click/email_reply)

Connect Instantly webhooks to PostHog via n8n for email events. Set up a Loom polling workflow (every 4 hours) to capture view data and fire `video_viewed` events.

### 2. Record and send video batch 1 (Week 1)

Run the `video-prospecting-outreach` drill for a batch of 50 prospects:

1. Source 50 prospects from Clay matching the ICP validated in Smoke. Ensure each has at least one enrichment signal for personalization.
2. Record 50 personalized Loom videos (plan two recording sessions of 25 each, ~1 hour per session).
3. Build the Instantly campaign with 3-step video email sequence.
4. Launch sends on Monday-Wednesday of Week 1.

**Human action required:** Founder records the videos. Agent handles enrichment, email copy, campaign setup, and tracking.

### 3. Deploy engagement-based follow-up routing

Run the `video-engagement-follow-up` drill to build n8n workflows that react to Loom view data:

- **High engagement (>75% watched):** Pause the Instantly sequence. Send a personal follow-up from the founder's inbox within 24 hours: "Saw you caught my video — want to walk through it live?"
- **Medium engagement (25-75% watched):** Accelerate Email 2 to send within 24 hours instead of the default 3-day delay.
- **Low engagement (<25% watched):** Let the standard sequence continue.
- **Never watched (5+ days, no view):** Send a text-only follow-up with a different angle (no video reference).

### 4. Record and send video batch 2 (Week 2)

Repeat for another 50 prospects. Apply learnings from Week 1:

- If completion rate was low: shorten videos to 45-60 seconds
- If thumbnail click rate was low: test a different email subject line
- If CTA clicks were low: reposition the CTA earlier in the video
- If a specific ICP segment responded better: weight the second batch toward that segment

### 5. Run a cold-email-only control group

Using the `cold-email-sequence` drill, send text-only cold emails to a separate batch of 20-30 prospects from the same ICP. Use the same value proposition but without video. This control group measures the incremental lift of video over text-only outreach. Compare: reply rate, meeting rate, and time-to-meeting.

### 6. Evaluate against threshold

Review PostHog funnel data and Attio deal pipeline after 2 weeks:

- **Video completion rate:** >=10% of videos sent were watched >=75%
- **Meetings booked:** >=4 total from video outreach

Also evaluate:
- Video vs text-only comparison: Is video producing measurably better results?
- Which engagement branch produced the most meetings?
- Which ICP segments had the highest video watch rates?

If PASS: Proceed to Scalable. Document winning video script structure, best ICP segments, and optimal video length.

If FAIL: Diagnose:
- Completion rate OK but no meetings: CTA and follow-up need work
- Completion rate low: Videos not compelling; test shorter format or different hooks
- Text-only outperforms video: Video may not be the right channel for this ICP; consider pivoting

## Time Estimate

- PostHog event setup and n8n workflows: 2 hours
- Video recording (100 videos across 2 batches): 4 hours
- Campaign setup in Instantly (2 batches + control): 2 hours
- Daily monitoring and follow-up routing: 2 hours total
- Control group setup and analysis: 1 hour
- Evaluation and documentation: 1 hour
- **Total: ~12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record personalized prospect videos | $12.50/user/mo (Business, unlimited recordings) — [loom.com/pricing](https://www.loom.com/pricing) |
| Instantly | Cold email sequences with video embeds | $37/mo (Growth: 5,000 emails) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Prospect enrichment + AI video hooks | $185/mo (Launch: 2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Event tracking and funnel analysis | Free (1M events/mo) or $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation workflows for follow-up routing | Free (self-hosted) or $24/mo (cloud starter) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM for deal tracking | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Booking links for video CTAs | Free (basic) or $12/mo (Team) — [cal.com/pricing](https://cal.com/pricing) |

**Estimated Baseline cost:** ~$80-270/mo (Loom Business + Instantly Growth + Clay Launch if not already subscribed)

## Drills Referenced

- `video-prospecting-outreach` — record Loom videos and send via Instantly with embedded thumbnails
- `posthog-gtm-events` — set up video outreach event taxonomy in PostHog
- `video-engagement-follow-up` — automated follow-up routing based on Loom watch behavior
- `cold-email-sequence` — text-only control group for measuring video lift
