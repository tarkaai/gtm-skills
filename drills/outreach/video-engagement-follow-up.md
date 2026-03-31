---
name: video-engagement-follow-up
description: Automate follow-up sequences based on Loom video view analytics and engagement signals
category: Outreach
tools:
  - Loom
  - n8n
  - Attio
  - Instantly
  - PostHog
fundamentals:
  - loom-analytics
  - n8n-workflow-basics
  - n8n-triggers
  - attio-contacts
  - attio-deals
  - instantly-reply-detection
  - posthog-custom-events
---

# Video Engagement Follow-Up

This drill builds automated follow-up workflows that react to Loom video engagement data. Instead of following a fixed time-based email cadence, this drill routes prospects into different follow-up paths based on whether they watched the video, how much they watched, and whether they clicked the CTA.

## Input

- Active video outreach campaign (from `video-prospecting-outreach` drill)
- Loom Business account with viewer analytics
- n8n instance connected to Attio and Instantly
- PostHog tracking configured

## Steps

### 1. Set up Loom view data ingestion

Loom does not provide webhook-based real-time notifications via API. Build an n8n polling workflow using `n8n-workflow-basics`:

1. Create a cron-triggered workflow that runs every 4 hours during business days
2. For each active campaign video, query the Loom dashboard (scrape or use the SDK viewer data endpoint if available) to get:
   - List of viewers (email if identified, anonymous if not)
   - Watch percentage per viewer
   - CTA click events
3. Compare against the last poll to identify NEW view events
4. For each new view event, fire a PostHog event using `posthog-custom-events`:
   - Event: `video_viewed`
   - Properties: `prospect_email`, `video_id`, `watch_percentage`, `cta_clicked`, `campaign_slug`

### 2. Build the engagement-based routing workflow

Create an n8n workflow triggered by the `video_viewed` PostHog event (via webhook):

**Branch A -- High engagement (watched >75%):**
1. Using `attio-contacts`, update the contact: `video_engagement: high`, `video_watch_pct: {pct}`
2. Using `attio-deals`, create a deal or move existing deal to "Interested" stage
3. If they clicked the CTA: do nothing extra, the Cal.com booking handles it
4. If they did NOT click the CTA: pause the Instantly sequence for this prospect using `instantly-reply-detection` (treat as manual takeover), then generate a personalized follow-up email:
   ```
   Subject: Saw you watched my video, {first_name}

   Hey {first_name}, looks like you caught the video I sent.

   Want me to walk you through {specific_feature} live? Here are a few times: {cal_link}

   {your_name}
   ```
5. Send this follow-up via the founder's personal email (not Instantly) for authenticity

**Branch B -- Medium engagement (watched 25-75%):**
1. Update Attio: `video_engagement: medium`
2. Accelerate the Instantly sequence: move Email 2 forward to send within 24 hours instead of the default 3-day delay
3. Log in PostHog: `video_followup_accelerated` event

**Branch C -- Low engagement (watched <25%):**
1. Update Attio: `video_engagement: low`
2. Let the standard Instantly sequence continue on schedule
3. After the sequence completes with no reply, add to a re-engagement list for a different angle in 30 days

### 3. Handle "never watched" prospects

Create a separate n8n workflow using `n8n-scheduling`:

1. Run daily, 5 days after the initial video email was sent
2. Query prospects where `video_sent: true` AND `video_watched: false` AND no email reply
3. For these prospects, the video approach did not work. Send a text-only follow-up with a different angle (no video reference):
   ```
   Subject: {pain_point_headline}

   Hey {first_name},

   {two_sentence_value_prop_without_video_reference}

   Worth a quick chat? {cal_link}

   {your_name}
   ```
4. Update Attio: `video_approach: no_engagement`

### 4. Track follow-up effectiveness

Using `posthog-custom-events`, track which follow-up branch produces the most meetings:

- `video_followup_sent` -- properties: branch (high/medium/low/never_watched), prospect_email
- `video_followup_replied` -- properties: branch, sentiment
- `video_followup_meeting_booked` -- properties: branch, source (cal_link/direct_reply)

Build a PostHog insight comparing meeting conversion rate by engagement branch. This data validates whether video engagement scoring is predictive and calibrates the watch percentage thresholds.

### 5. Feed learnings back to video recording

After 2+ weeks of data:

- If high-engagement prospects (>75% watched) are NOT converting to meetings: the video content is engaging but the CTA or value prop is weak. Adjust the video script's closing section.
- If most prospects fall into "never watched": the email subject line or thumbnail is not compelling enough. Test different subject lines via `ab-test-orchestrator` drill.
- If medium-engagement (25-75%) is the largest bucket: videos are too long or lose viewers mid-way. Shorten videos and front-load the most compelling content.

## Output

- Automated n8n workflows that route prospects based on video engagement
- Personalized follow-up emails triggered by watch behavior
- Attio contact records enriched with video engagement data
- PostHog tracking of follow-up branch effectiveness
- Data-driven recommendations for video script and email optimization

## Triggers

The polling workflow runs every 4 hours on business days. Follow-up workflows trigger on each new view event. The "never watched" workflow runs daily.
